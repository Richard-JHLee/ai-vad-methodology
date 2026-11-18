Require a current VAD record and passing CLI tests for PRs to `main`. Each PR selects its record through `.vad/ci-change-id`; invalid/missing/symlinked selection fails. Manual success uses a separate check name and cannot replace the PR gate.

The implementation reuses CLI validation and readiness policy. Actions remain read-only and do not persist checkout credentials. No record schema changes.

Validation: 33 local tests passed; Python 3.9 and 3.13 passed on this PR. The initial unapproved PR failed `VAD PR gate` and retained diagnostics. After main protection was applied, GitHub reported this PR as `BLOCKED` without a bypass.

Main now requires `VAD PR gate`, `tests (3.9)`, and `tests (3.13)` from the GitHub Actions App, an up-to-date base, PR-based changes, and administrator enforcement. Force pushes and deletion are disabled; conversations must be resolved. Additional GitHub reviewer count is zero for this single-maintainer repository. The explicit VAD human-review record remains required.

All current verification records are complete; human approval for this new source is pending. After review, verify the passing gate and merge normally without administrator bypass. Implementation and policy: `docs/vad-ci.md`; report: `.vad/evidence/pr-gate/report.md`; saved before/after policy: `.vad/evidence/pr-gate/`.
