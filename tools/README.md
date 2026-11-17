# VAD local CLI

A dependency-free reference implementation of the proposed
[verification decisions](../rfcs/0003-verification-decisions.md).
See the [architecture and development plan (Korean)](../docs/vad-cli-plan.md).

Requires Python 3.9+ and Git on your PATH, with at least one commit in the target
repository. No installation, server, account, or network connection is needed.
Run the commands from this repository; `--repo` can point to another Git repository.

## Quick start

```sh
python3 tools/vad.py --help
python3 tools/vad.py init limit-items --title "Bound item queries" --owner "Developer" --risk Medium
```

Edit **only the `plan` object** in `.vad/changes/limit-items.json`. The draft has
empty fields deliberately: an incomplete plan cannot be approved. For example:

```json
{
  "title": "Bound item queries",
  "owner": "Developer",
  "risk": "Medium",
  "purpose": "Keep item responses bounded while preserving the existing contract",
  "environment": "Local Python 3.13; fixture database; dependency versions recorded in lockfile",
  "recovery": "Revert the read-only change; no schema or write effects",
  "impact": {
    "paths": "GET /items -> authenticated handler -> tenant-scoped repository; callers checked",
    "data": "Read-only query; no writes or schema changes",
    "permissions": "Existing authentication and tenant filtering must remain enforced",
    "regression": "Default response and existing clients must remain compatible"
  },
  "criteria": {
    "AC-1": "Default remains 20; limits 1..100 apply before materialization; invalid limits return 422",
    "AC-2": "Unauthenticated access is denied and tenants cannot read each other's items"
  },
  "checks": {
    "contract": {
      "criteria": ["AC-1"],
      "procedure": "Run endpoint contract and repository query-bound tests",
      "expected": "Default, boundary and invalid-input cases meet AC-1"
    },
    "permissions": {
      "criteria": ["AC-2"],
      "procedure": "Run authentication and cross-tenant denial tests",
      "expected": "No unauthorized or cross-tenant results"
    }
  }
}
```

Replace the example with your actual requirement, callers, checks, environment,
and recovery plan. Keep `schema_version`, `results`, and `approvals` outside the
plan unchanged. Every criterion needs a check, and all listed checks are required.
If a category is outside scope, explain why in its impact field instead of leaving it blank.

Perform the planned checks yourself, then record what happened. The CLI does
**not** run tests or independently verify your assertions. For an unavailable
environment, record a gap instead of claiming a pass:

```sh
python3 tools/vad.py record limit-items --check contract --result Blocked --observed "Fixture database unavailable" --evidence "Local test prerequisite missing; verification not completed"
python3 tools/vad.py status limit-items
python3 tools/vad.py report limit-items
```

After executing the checks, record their actual results and sanitized evidence
references. Each `record` appends history. Supported states are **Pass**, **Fail**,
**Blocked**, **Not run**, **N/A**. N/A requires a scope-based explanation; it must
not be used for a missing environment or unattempted check. The tool requires
nonblank reasons but cannot judge whether an N/A explanation is truthful.

Only after all checks have current Pass/N/A results, a human reviewer can record:

```sh
python3 tools/vad.py approve limit-items --reviewer "Actual human reviewer" --attest-human-review
python3 tools/vad.py status limit-items
python3 tools/vad.py report limit-items > .vad/limit-items-report.md
```

`Ready` means a current **merge review record** exists. It never means production
safety or authenticated approval. `status` is informational and exits zero when
it can read the record, even for Not ready; do not use its exit code as a CI gate.
Invalid input and failed writes/approvals exit 1; argument errors exit 2.
High/Critical changes can be recorded and reported but cannot be approved in this
MVP. Residual-risk exceptions and deployment approval are not supported.

## Storage and freshness

Records live at `.vad/changes/ID.json` in the target Git repository. IDs contain
1–80 letters, digits, underscores or hyphens and start with a letter or digit.
Choose whether to commit sanitized records; the CLI never commits or pushes.
No source files, existing records, or old result entries are deleted by CLI commands.

Each result is bound to a SHA-256 fingerprint of source content and the entire
plan, including its environment description. Tracked files, deletions, executable
bits, symlinks, and non-ignored untracked files participate. `.vad/` is excluded so
recording evidence and exporting reports there do not make the evidence stale.
HEAD SHA is recorded as context, but a commit with unchanged source preserves
evidence. Source or plan changes invalidate old results conservatively; rerun
checks and record new results. Adding results also requires a new approval.

Submodules and unresolved merge conflicts are rejected. Ignored files, resolved
symlink target contents, installed dependencies, and external services are not
automatically fingerprinted. Update the environment description after relevant
external changes. Keep the source stable while running checks and recording them.
Do not put product code or requirements under `.vad/`.

Storage uses an exclusive writer lock and atomic file replacement. If interrupted,
confirm no VAD writer is active before manually removing a leftover `.vad/.lock`
directory. Malformed or unknown-schema records are rejected without overwriting
them. Restore committed records from Git if recovery is needed.

Records and reviewer names are editable local data, **not** a tamper-proof audit
log or identity system. Do not enter credentials, sensitive payloads, or raw
private logs. The CLI stores the text you supply; it does not redact it. Human
review of evidence and repository access controls remain necessary.

## Development verification

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Tests use disposable repositories and invoke the real CLI. They cover result
states, stale evidence, review invalidation, missing coverage, input validation,
history preservation, storage-path restrictions, locking, and write failure.
