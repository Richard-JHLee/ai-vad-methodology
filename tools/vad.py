#!/usr/bin/env python3
"""Local, self-reported VAD evidence and merge-review records. No test execution."""

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


STATES = ("Pass", "Fail", "Blocked", "Not run", "N/A")
RISKS = ("Low", "Medium", "High", "Critical")


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def now():
    return datetime.now(timezone.utc).isoformat()


def text(value):
    return isinstance(value, str) and bool(value.strip())


def git(root, *args):
    result = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    if result.returncode:
        raise ValueError("Git command failed: " + " ".join(args))
    return result.stdout


def source_snapshot(root):
    for entry in git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not entry:
            continue
        mode, _, stage = entry.split(b"\t", 1)[0].split()
        if mode == b"160000" or stage != b"0":
            raise ValueError("Submodules and unresolved merge conflicts are unsupported")
    names = set(git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z").split(b"\0"))
    snapshot = hashlib.sha256()
    for name in sorted(names - {b""}):
        if name == b".vad" or name.startswith(b".vad/"):
            continue
        path = root / os.fsdecode(name)
        if path.is_symlink():
            kind, content = b"link", os.fsencode(os.readlink(path))
        elif path.is_file():
            kind = b"executable" if path.stat().st_mode & 0o111 else b"file"
            content = path.read_bytes()
        elif not path.exists():
            kind, content = b"deleted", b""
        else:
            raise ValueError("Unsupported source entry: " + os.fsdecode(name))
        snapshot.update(name + b"\0" + kind + b"\0" + hashlib.sha256(content).digest())
    return snapshot.hexdigest()


def paths(root, change_id):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,79}", change_id):
        raise ValueError("ID must be 1-80 letters, digits, underscores or hyphens")
    directory = root / ".vad"
    changes = directory / "changes"
    record = changes / (change_id + ".json")
    for path in (directory, changes, record):
        if path.is_symlink():
            raise ValueError("VAD storage must not use symbolic links")
    return directory, changes, record


def selected_change_id(root, requested=""):
    if requested:
        paths(root, requested)
        return requested
    selection = root / ".vad" / "ci-change-id"
    if selection.parent.is_symlink() or selection.is_symlink():
        raise ValueError("VAD CI selection must not use symbolic links")
    change_id = selection.read_text(encoding="utf-8").strip()
    paths(root, change_id)
    return change_id


@contextmanager
def locked(directory):
    directory.mkdir(exist_ok=True)
    lock = directory / ".lock"
    try:
        lock.mkdir()
    except FileExistsError:
        raise ValueError("VAD storage is locked; check for a running writer before removing .vad/.lock") from None
    try:
        yield
    finally:
        lock.rmdir()


def save(path, document):
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         delete=False) as output:
            temporary = output.name
            json.dump(document, output, ensure_ascii=False, indent=2)
            output.write("\n")
            output.flush()
            os.fsync(output.fileno())
        os.replace(temporary, path)
    finally:
        if temporary and os.path.exists(temporary):
            os.unlink(temporary)


def load(path):
    document = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or type(document.get("schema_version")) is not int or document["schema_version"] != 1:
        raise ValueError("Unsupported or missing schema_version (expected 1)")
    if not isinstance(document.get("plan"), dict):
        raise ValueError("plan must be an object")
    for field in ("results", "approvals"):
        if not isinstance(document.get(field), list):
            raise ValueError(field + " must be a list")
        for item in document[field]:
            keys = (("check", "state", "observed", "evidence", "context", "time", "head")
                    if field == "results" else
                    ("reviewer", "context", "results_digest", "time", "gate"))
            if not isinstance(item, dict) or any(not text(item.get(key)) for key in keys):
                raise ValueError("Malformed " + field + " entry")
            if field == "results" and item["state"] not in STATES:
                raise ValueError("Unknown result state")
            if field == "approvals" and item["gate"] != "merge":
                raise ValueError("Only merge approvals are supported")
    return document


def plan_errors(plan):
    errors = []
    for field in ("title", "owner", "purpose", "environment", "recovery"):
        if not text(plan.get(field)):
            errors.append("plan." + field + " is required")
    if plan.get("risk") not in RISKS:
        errors.append("plan.risk must be Low, Medium, High or Critical")
    impact = plan.get("impact")
    if not isinstance(impact, dict) or any(not text(impact.get(key)) for key in ("paths", "data", "permissions", "regression")):
        errors.append("plan.impact requires paths, data, permissions and regression explanations")
    criteria = plan.get("criteria")
    if not isinstance(criteria, dict) or not criteria or any(not text(k) or not text(v) for k, v in criteria.items()):
        errors.append("plan.criteria requires criterion IDs and expected behavior")
        criteria = {}
    checks = plan.get("checks")
    covered = set()
    if not isinstance(checks, dict) or not checks:
        errors.append("plan.checks requires at least one check")
        checks = {}
    for name, check in checks.items():
        if not text(name) or not isinstance(check, dict):
            errors.append("Each check must be a named object")
            continue
        refs = check.get("criteria")
        if not isinstance(refs, list) or not refs or any(not isinstance(ref, str) or ref not in criteria for ref in refs):
            errors.append("Check " + name + " must reference existing criteria")
        else:
            covered.update(refs)
        if any(not text(check.get(key)) for key in ("procedure", "expected")):
            errors.append("Check " + name + " requires procedure and expected behavior")
    if set(criteria) - covered:
        errors.append("Criteria without checks: " + ", ".join(sorted(set(criteria) - covered)))
    return errors


def context(root, plan):
    # shortcut: invalidate all checks, add selective reuse only if rerun cost warrants it.
    return digest({"source": source_snapshot(root), "plan": plan})


def assess(document, current):
    plan = document["plan"]
    errors = plan_errors(plan)
    if errors:
        return errors
    if plan["risk"] in ("High", "Critical"):
        errors.append("High/Critical merge approval requires external review; unsupported in this MVP")
    for name in plan["checks"]:
        history = [item for item in document["results"] if item["check"] == name]
        if not history:
            errors.append(name + ": Not run (no recorded result)")
        elif history[-1]["context"] != current:
            errors.append(name + ": stale evidence; record verification for the current source and plan")
        elif history[-1]["state"] not in ("Pass", "N/A"):
            errors.append(name + ": " + history[-1]["state"])
    return errors


def status(document, current):
    gaps = assess(document, current)
    approval = document["approvals"][-1] if document["approvals"] else None
    approved = bool(approval and approval["context"] == current and
                    approval["results_digest"] == digest(document["results"]))
    return {"decision": "Ready" if not gaps and approved else "Not ready",
            "gate": "merge", "context": current, "gaps": gaps,
            "human_review_recorded": approved,
            "note": "Self-reported records, not authenticated identity or proof of correctness"}


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--repo", default=".", help="Target Git repository (default: current directory)")
    commands = cli.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create a draft plan; edit its plan object before recording results")
    init.add_argument("id")
    init.add_argument("--title", required=True)
    init.add_argument("--owner", required=True)
    init.add_argument("--risk", choices=RISKS, default="Medium")
    plan = commands.add_parser("plan", help="Export a plan, or import a validated plan without replacing history")
    plan.add_argument("id")
    plan.add_argument("--file", help="UTF-8 JSON file containing only the replacement plan object")
    record = commands.add_parser("record", help="Record a manually executed check or explain a gap")
    record.add_argument("id")
    record.add_argument("--check", required=True)
    record.add_argument("--result", choices=STATES, required=True)
    record.add_argument("--observed", required=True, help="Observed behavior, or reason for a gap/N/A")
    record.add_argument("--evidence", required=True, help="Sanitized reference or scope-based N/A reason")
    approve = commands.add_parser("approve", help="Record self-declared human merge review; Low/Medium only")
    approve.add_argument("id")
    approve.add_argument("--reviewer", required=True)
    approve.add_argument("--attest-human-review", action="store_true", required=True,
                         help="Declare that the named human reviewed the current plan and evidence")
    for name in ("status", "report", "check"):
        command = commands.add_parser(name)
        command.add_argument("id")
    return cli


def execute(args):
    root = Path(os.fsdecode(git(Path(args.repo), "rev-parse", "--show-toplevel")).strip()).resolve()
    directory, changes, path = paths(root, args.id)
    if args.command == "plan" and args.file is None:
        print(json.dumps(load(path)["plan"], ensure_ascii=False, indent=2))
        return
    if args.command in ("status", "report", "check"):
        document = load(path)
        state = status(document, context(root, document["plan"]))
        if args.command in ("status", "check"):
            print(json.dumps(state, ensure_ascii=False, indent=2))
            if args.command == "check":
                return 0 if state["decision"] == "Ready" else 1
        else:
            print("# VAD merge verification report\n")
            print("Decision: " + state["decision"])
            print("\nSelf-reported evidence and review; no production readiness claim.\n")
            print("## Verification\n")
            if state["gaps"]:
                for gap in state["gaps"]:
                    print("    " + json.dumps(gap, ensure_ascii=False))
            else:
                print("All planned checks have current passing or N/A records.")
            print("\n## Human review\n")
            print("Current approval record present." if state["human_review_recorded"]
                  else "Pending: no approval record matches the current source, plan and results.")
            print("\n## Next steps\n")
            if state["gaps"]:
                print("Resolve the listed gaps, rerun affected checks, and record actual results for the current source and plan.")
            if not state["human_review_recorded"]:
                print("After verification, a responsible human must review the plan and evidence before recording approval. Do not fabricate or automatically grant approval.")
            if state["decision"] == "Ready":
                print("Ready for the merge gate only; deployment readiness requires separate verification.")
            print("\n## Full record\n")
            # Indented JSON keeps user-entered Markdown/HTML inert in the report.
            print("\n".join("    " + line for line in json.dumps(
                {"status": state, "record": document}, ensure_ascii=False, indent=2).splitlines()))
        return
    with locked(directory):
        # Recheck storage after obtaining the writer lock.
        _, changes, path = paths(root, args.id)
        changes.mkdir(exist_ok=True)
        if args.command == "init":
            if path.exists():
                raise ValueError("Change already exists; existing data was preserved")
            if not text(args.title) or not text(args.owner):
                raise ValueError("Title and owner must not be blank")
            document = {"schema_version": 1, "plan": {
                "title": args.title, "owner": args.owner, "risk": args.risk,
                "purpose": "", "environment": "", "recovery": "",
                "impact": {"paths": "", "data": "", "permissions": "", "regression": ""},
                "criteria": {}, "checks": {}}, "results": [], "approvals": []}
        elif args.command == "plan":
            document = load(path)
            replacement = json.loads(Path(args.file).read_text(encoding="utf-8"))
            if not isinstance(replacement, dict):
                raise ValueError("Replacement plan must be a JSON object")
            errors = plan_errors(replacement)
            if errors:
                raise ValueError("; ".join(errors))
            document["plan"] = replacement
        else:
            document = load(path)
            errors = plan_errors(document["plan"])
            if errors:
                raise ValueError("; ".join(errors))
            current = context(root, document["plan"])
            if args.command == "record":
                if args.check not in document["plan"]["checks"]:
                    raise ValueError("Unknown check: " + args.check)
                if not text(args.observed) or not text(args.evidence):
                    raise ValueError("Observed behavior/reason and evidence must not be blank")
                document["results"].append({"check": args.check, "state": args.result,
                    "observed": args.observed, "evidence": args.evidence,
                    "context": current, "time": now(),
                    "head": os.fsdecode(git(root, "rev-parse", "HEAD")).strip()})
            else:
                errors = assess(document, current)
                if errors:
                    raise ValueError("Cannot approve: " + "; ".join(errors))
                if not text(args.reviewer):
                    raise ValueError("Reviewer must not be blank")
                # shortcut: reviewer identity is self-declared, authenticate before enforcing team release gates.
                document["approvals"].append({"reviewer": args.reviewer,
                    "context": current, "results_digest": digest(document["results"]),
                    "time": now(), "gate": "merge"})
        save(path, document)
    print(str(path))


def main():
    args = parser().parse_args()
    try:
        return execute(args) or 0
    except (OSError, ValueError) as error:
        print("vad: " + str(error), file=sys.stderr)
        return 2 if args.command == "check" else 1


if __name__ == "__main__":
    sys.exit(main())
