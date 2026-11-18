"""Integration checks for the public CLI, using disposable Git repositories."""

import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


CLI = Path(__file__).resolve().parents[1] / "tools" / "vad.py"
spec = importlib.util.spec_from_file_location("vad", CLI)
vad = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vad)


class VadCLI(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.git("init", "-q")
        (self.root / "app.py").write_text("answer = 42\n")
        self.git("add", "app.py")
        self.git("commit", "-qm", "Initial source")
        self.path = self.root / ".vad" / "changes" / "demo.json"

    def git(self, *args, input_data=None):
        return subprocess.run(["git", "-c", "user.name=Test Reviewer", "-c",
            "user.email=reviewer@example.invalid", "-c", "commit.gpgsign=false",
            "-c", "core.hooksPath=/dev/null", "-C", str(self.root), *args],
            check=True, capture_output=True, input=input_data)

    def cli(self, *args, code=0):
        result = subprocess.run([sys.executable, str(CLI), "--repo", str(self.root), *args],
            capture_output=True, text=True,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stderr)
        return result

    def read(self):
        return json.loads(self.path.read_text())

    def write(self, document):
        self.path.write_text(json.dumps(document))

    def prepare(self, risk="Medium"):
        self.cli("init", "demo", "--title", "Answer contract", "--owner", "Developer", "--risk", risk)
        document = self.read()
        document["plan"].update({
            "purpose": "Preserve the answer contract", "environment": "Python test fixture; local",
            "recovery": "Revert app.py; no persistent writes",
            "impact": {"paths": "app.py and caller", "data": "No writes",
                "permissions": "No authorization boundary changed", "regression": "Existing answer remains 42"},
            "criteria": {"AC-1": "The answer is 42"},
            "checks": {"answer": {"criteria": ["AC-1"], "procedure": "Read app.py and check answer",
                "expected": "answer = 42"}}})
        self.write(document)

    def record(self, state="Pass"):
        return self.cli("record", "demo", "--check", "answer", "--result", state,
            "--observed", "Observed answer = 42" if state == "Pass" else "Scope or execution reason",
            "--evidence", "Sanitized manual review reference")

    def approve(self, code=0):
        return self.cli("approve", "demo", "--reviewer", "Human Reviewer",
                        "--attest-human-review", code=code)

    def state(self):
        return json.loads(self.cli("status", "demo").stdout)

    def test_check_requires_current_human_review_and_does_not_write(self):
        self.prepare()
        self.cli("check", "demo", code=1)
        self.record()
        self.assertFalse(json.loads(self.cli("check", "demo", code=1).stdout)["human_review_recorded"])
        self.approve()
        before = self.path.read_bytes()
        self.assertEqual(json.loads(self.cli("check", "demo").stdout), self.state())
        self.assertEqual(self.path.read_bytes(), before)
        self.assertFalse((self.root / ".vad" / ".lock").exists())
        self.record()
        self.cli("check", "demo", code=1)
        self.cli("status", "demo")

    def test_check_returns_policy_failure_for_result_gaps_and_high_risk(self):
        self.prepare()
        for result in vad.STATES:
            with self.subTest(result=result):
                self.record(result)
                if result in ("Pass", "N/A"):
                    self.approve()
                state = json.loads(self.cli("check", "demo", code=0 if result in ("Pass", "N/A") else 1).stdout)
                self.assertEqual(state["decision"], "Ready" if result in ("Pass", "N/A") else "Not ready")
        for risk in ("High", "Critical"):
            document = self.read()
            document["plan"]["risk"] = risk
            self.write(document)
            self.record()
            self.cli("check", "demo", code=1)

    def test_check_rejects_stale_source_and_plan(self):
        self.prepare()
        self.record()
        self.approve()
        (self.root / "app.py").write_text("answer = 43\n")
        self.cli("check", "demo", code=1)
        self.record()
        self.approve()
        document = self.read()
        document["plan"]["environment"] += " changed"
        self.write(document)
        self.cli("check", "demo", code=1)

    def test_check_distinguishes_input_errors_from_not_ready(self):
        self.cli("check", "missing", code=2)
        self.cli("check", "--", "--help", code=2)
        self.cli("check", "../outside", code=2)
        self.cli("init", "demo", "--title", "Draft", "--owner", "Developer")
        self.cli("check", "demo", code=1)
        self.path.write_text("broken JSON")
        self.cli("check", "demo", code=2)
        self.assertEqual(self.path.read_text(), "broken JSON")

    def test_check_rejects_storage_symlinks_and_unresolved_git_state(self):
        self.prepare()
        target = self.path.parent / "original.json"
        self.path.rename(target)
        self.path.symlink_to(target)
        self.cli("check", "demo", code=2)
        self.path.unlink()
        target.rename(self.path)
        head = self.git("rev-parse", "HEAD").stdout.strip().decode()
        self.git("update-index", "--add", "--cacheinfo", "160000," + head + ",module")
        self.cli("check", "demo", code=2)

    def test_plan_export_reads_draft_without_modifying_record(self):
        self.cli("init", "demo", "--title", "Draft", "--owner", "Developer")
        before = self.path.read_bytes()
        plan = json.loads(self.cli("plan", "demo").stdout)
        self.assertEqual(plan, self.read()["plan"])
        self.assertNotIn("results", plan)
        self.assertEqual(self.path.read_bytes(), before)

    def test_plan_import_completes_draft_and_preserves_existing_history(self):
        self.prepare()
        self.record()
        self.approve()
        original = self.read()
        plan_file = self.root / ".vad" / "input-plan.json"
        plan = original["plan"]
        plan["purpose"] = "Updated requirement"
        plan_file.write_text(json.dumps(plan))
        self.cli("plan", "demo", "--file", str(plan_file))
        imported = self.read()
        self.assertEqual(imported["plan"], plan)
        self.assertEqual(imported["results"], original["results"])
        self.assertEqual(imported["approvals"], original["approvals"])
        self.assertFalse(self.state()["human_review_recorded"])
        self.assertIn("stale evidence", " ".join(self.state()["gaps"]))
        self.record()
        self.approve()
        self.assertEqual(self.state()["decision"], "Ready")
        self.cli("init", "draft", "--title", "Draft", "--owner", "Developer")
        self.cli("plan", "draft", "--file", str(plan_file))
        draft = json.loads((self.path.parent / "draft.json").read_text())
        self.assertEqual(draft["plan"], plan)
        self.assertEqual(draft["results"], [])
        self.assertEqual(draft["approvals"], [])

    def test_identical_plan_import_preserves_current_approval(self):
        self.prepare()
        self.record()
        self.approve()
        plan_file = self.root / ".vad" / "input-plan.json"
        plan_file.write_text(self.cli("plan", "demo").stdout)
        before = self.state()
        self.cli("plan", "demo", "--file", str(plan_file))
        self.assertEqual(self.state(), before)

    def test_invalid_plan_imports_preserve_record_bytes(self):
        self.prepare()
        self.record()
        self.approve()
        original = self.path.read_bytes()
        plan_file = self.root / ".vad" / "input-plan.json"
        for content in ("bad JSON", "[]", "null", "42", "{}", json.dumps(self.read())):
            with self.subTest(content=content):
                plan_file.write_text(content)
                self.cli("plan", "demo", "--file", str(plan_file), code=1)
                self.assertEqual(self.path.read_bytes(), original)
        self.cli("plan", "demo", "--file", str(plan_file.parent / "missing.json"), code=1)
        self.assertEqual(self.path.read_bytes(), original)

    def test_plan_import_respects_writer_lock_and_storage_symlinks(self):
        self.prepare()
        plan_file = self.root / ".vad" / "input-plan.json"
        plan_file.write_text(json.dumps(self.read()["plan"]))
        original = self.path.read_bytes()
        lock = self.root / ".vad" / ".lock"
        lock.mkdir()
        self.cli("plan", "demo", "--file", str(plan_file), code=1)
        self.assertEqual(self.path.read_bytes(), original)
        lock.rmdir()
        target = self.path.parent / "original.json"
        self.path.rename(target)
        self.path.symlink_to(target)
        self.cli("plan", "demo", "--file", str(plan_file), code=1)
        self.cli("plan", "demo", code=1)
        self.assertEqual(target.read_bytes(), original)

    def test_draft_duplicate_and_no_data_loss(self):
        self.cli("init", "demo", "--title", "Draft", "--owner", "Developer")
        before = self.path.read_bytes()
        self.assertEqual(self.state()["decision"], "Not ready")
        self.approve(code=1)
        self.cli("init", "demo", "--title", "Overwrite", "--owner", "Other", code=1)
        self.assertEqual(self.path.read_bytes(), before)

    def test_complete_flow_requires_human_review_and_preserves_history(self):
        self.prepare()
        self.approve(code=1)
        self.record()
        self.assertEqual(self.state()["decision"], "Not ready")
        self.approve()
        self.assertEqual(self.state()["decision"], "Ready")
        self.record("Fail")
        self.assertEqual(self.state()["decision"], "Not ready")
        self.approve(code=1)
        self.record()
        self.assertEqual(self.state()["decision"], "Not ready")
        self.approve()
        self.assertEqual([r["state"] for r in self.read()["results"]], ["Pass", "Fail", "Pass"])
        self.assertEqual(len(self.read()["approvals"]), 2)

    def test_all_result_states(self):
        self.prepare()
        for result in vad.STATES:
            with self.subTest(result=result):
                self.record(result)
                self.approve(code=0 if result in ("Pass", "N/A") else 1)
                self.assertEqual(self.state()["decision"], "Ready" if result in ("Pass", "N/A") else "Not ready")

    def test_source_and_plan_changes_invalidate_results(self):
        self.prepare()
        self.record()
        self.approve()
        (self.root / "app.py").write_text("answer = 43\n")
        self.assertIn("stale evidence", " ".join(self.state()["gaps"]))
        self.approve(code=1)
        self.record()
        self.approve()
        for field in ("environment", "purpose", "recovery"):
            with self.subTest(field=field):
                document = self.read()
                document["plan"][field] += " updated"
                self.write(document)
                self.assertEqual(self.state()["decision"], "Not ready")
                self.approve(code=1)
                self.record()
                self.approve()

    def test_untracked_files_deletions_and_executable_bit_change_context(self):
        self.prepare()
        self.record()
        initial = self.state()["context"]
        (self.root / "new.py").write_text("new = True\n")
        self.assertNotEqual(self.state()["context"], initial)
        (self.root / "new.py").unlink()
        self.assertEqual(self.state()["context"], initial)
        (self.root / "app.py").chmod(0o755)
        self.assertNotEqual(self.state()["context"], initial)
        (self.root / "app.py").unlink()
        self.assertNotEqual(self.state()["context"], initial)

    def test_same_source_commit_and_vad_reports_do_not_invalidate_evidence(self):
        self.prepare()
        self.record()
        self.approve()
        initial = self.state()["context"]
        report = self.cli("report", "demo").stdout
        (self.root / ".vad" / "report.md").write_text(report)
        self.git("add", ".vad")
        self.git("commit", "-qm", "Record evidence")
        self.assertEqual(self.state()["context"], initial)
        self.assertEqual(self.state()["decision"], "Ready")

    def test_required_coverage_and_known_check_validation(self):
        self.prepare()
        self.cli("record", "demo", "--check", "unknown", "--result", "Pass",
            "--observed", "ok", "--evidence", "ref", code=1)
        document = self.read()
        document["plan"]["criteria"]["AC-2"] = "Denial path"
        self.write(document)
        self.assertIn("Criteria without checks", " ".join(self.state()["gaps"]))
        self.approve(code=1)

    def test_high_and_critical_are_recordable_but_not_approvable(self):
        self.prepare("High")
        self.record()
        self.approve(code=1)
        document = self.read()
        document["plan"]["risk"] = "Critical"
        self.write(document)
        self.record()
        self.approve(code=1)
        self.assertEqual(len(self.read()["results"]), 2)

    def test_blank_reasons_and_missing_attestation_are_rejected(self):
        self.prepare()
        self.cli("record", "demo", "--check", "answer", "--result", "N/A",
            "--observed", " ", "--evidence", "ref", code=1)
        self.assertEqual(self.read()["results"], [])
        self.record()
        self.cli("approve", "demo", "--reviewer", "Reviewer", code=2)
        self.cli("approve", "demo", "--reviewer", " ", "--attest-human-review", code=1)

    def test_storage_path_traversal_and_symlinks_are_rejected(self):
        self.cli("init", "../outside", "--title", "Bad", "--owner", "Owner", code=1)
        external = self.root / "external"
        external.mkdir()
        (self.root / ".vad").symlink_to(external, target_is_directory=True)
        self.cli("init", "demo", "--title", "Bad", "--owner", "Owner", code=1)
        self.assertEqual(list(external.iterdir()), [])

    def test_record_symlink_and_existing_lock_preserve_data(self):
        self.prepare()
        before = self.path.read_bytes()
        lock = self.root / ".vad" / ".lock"
        lock.mkdir()
        self.cli("record", "demo", "--check", "answer", "--result", "Pass",
            "--observed", "ok", "--evidence", "ref", code=1)
        self.assertEqual(self.path.read_bytes(), before)
        lock.rmdir()
        external = self.root / ".vad" / "original.json"
        self.path.rename(external)
        self.path.symlink_to(external)
        self.cli("status", "demo", code=1)
        self.assertEqual(external.read_bytes(), before)

    def test_corrupt_and_unsupported_data_fail_without_overwriting(self):
        self.prepare()
        original = self.read()
        variants = ["broken JSON", json.dumps({"schema_version": 99}),
                    json.dumps({**original, "results": [{"state": "Pass"}]}),
                    json.dumps({**original, "plan": []})]
        for content in variants:
            with self.subTest(content=content):
                self.path.write_text(content)
                self.cli("status", "demo", code=1)
                self.approve(code=1)
                self.assertEqual(self.path.read_text(), content)

    def test_invalid_plan_shapes_fail_closed(self):
        self.prepare()
        document = self.read()
        for field, value in [("criteria", []), ("checks", []), ("impact", []),
                             ("checks", {"bad": {"criteria": [None]}})]:
            with self.subTest(field=field):
                modified = {**document, "plan": {**document["plan"], field: value}}
                self.write(modified)
                self.assertEqual(self.state()["decision"], "Not ready")
                self.approve(code=1)

    def test_atomic_replace_failure_preserves_original_and_cleans_temporary(self):
        self.prepare()
        before = self.path.read_bytes()
        with patch.object(vad.os, "replace", side_effect=OSError("disk failure")):
            with self.assertRaises(OSError):
                vad.save(self.path, {"replacement": True})
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_report_does_not_interpret_user_markdown(self):
        self.prepare()
        document = self.read()
        document["plan"]["title"] = "<script>alert(1)</script>\n```"
        self.write(document)
        report = self.cli("report", "demo").stdout
        self.assertIn("Decision: Not ready", report)
        self.assertTrue(all(line.startswith("    ") for line in report.splitlines() if "<script>" in line))

    def test_report_explains_review_wait_and_stale_evidence_without_writing(self):
        self.prepare()
        self.record()
        before = self.path.read_bytes()
        report = self.cli("report", "demo").stdout
        self.assertIn("All planned checks have current", report)
        self.assertIn("Pending: no approval record", report)
        self.assertIn("responsible human must review", report)
        self.assertIn("## Next steps", report)
        self.assertEqual(self.path.read_bytes(), before)
        self.approve()
        report = self.cli("report", "demo").stdout
        self.assertIn("Current approval record present.", report)
        self.assertNotIn("Pending: no approval record", report)
        self.assertIn("Ready for the merge gate only", report)
        (self.root / "app.py").write_text("answer = 43\n")
        report = self.cli("report", "demo").stdout
        self.assertIn("stale evidence", report)
        self.assertIn("Pending: no approval record", report)
        self.assertIn("rerun affected checks", report)
        self.cli("check", "demo", code=1)

    def test_report_lists_draft_errors_and_keeps_untrusted_gaps_inert(self):
        self.cli("init", "demo", "--title", "Draft", "--owner", "Developer")
        before = self.path.read_bytes()
        report = self.cli("report", "demo").stdout
        self.assertIn("plan.purpose is required", report)
        self.assertEqual(self.path.read_bytes(), before)
        document = self.read()
        document["plan"]["criteria"] = {"<script>bad</script>\n::error::injected": "Expected"}
        self.write(document)
        report = self.cli("report", "demo").stdout
        self.assertTrue(all(line.startswith("    ") for line in report.splitlines() if "<script>" in line or "::error::injected" in line))

    def test_submodule_and_merge_conflicts_are_rejected(self):
        self.prepare()
        head = self.git("rev-parse", "HEAD").stdout.strip().decode()
        self.git("update-index", "--add", "--cacheinfo", "160000," + head + ",module")
        self.cli("status", "demo", code=1)
        self.git("update-index", "--force-remove", "module")
        blob = self.git("rev-parse", "HEAD:app.py").stdout.strip().decode()
        entries = "0 " + "0" * 40 + "\tapp.py\n"
        entries += "".join(f"100644 {blob} {stage}\tapp.py\n" for stage in (1, 2, 3))
        self.git("update-index", "--index-info", input_data=entries.encode())
        self.cli("status", "demo", code=1)

    def test_changes_directory_symlink_is_rejected(self):
        (self.root / ".vad").mkdir()
        external = self.root / "external"
        external.mkdir()
        (self.root / ".vad" / "changes").symlink_to(external, target_is_directory=True)
        self.cli("init", "demo", "--title", "Bad", "--owner", "Owner", code=1)
        self.assertEqual(list(external.iterdir()), [])

    def test_non_git_repository_and_missing_record_fail_cleanly(self):
        self.cli("status", "missing", code=1)
        outside = self.root / "outside"
        outside.mkdir()
        result = subprocess.run([sys.executable, str(CLI), "--repo", str(self.root.parent),
                                 "status", "demo"], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn("Traceback", result.stderr)


if __name__ == "__main__":
    unittest.main()
