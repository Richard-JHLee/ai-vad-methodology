Enable a strict VAD gate on pull requests to `main`. Each PR selects its record through `.vad/ci-change-id`; malformed or missing selection fails before workflow output is written. Manual readiness checks use a separate check name and cannot substitute for the PR gate.

The implementation reuses the existing CLI ID validation, source fingerprint, verification and human-review policy. Actions retain read-only permissions and do not persist checkout credentials.

Validation includes the CLI integration suite and an actual PR blocked before review, followed by current human approval and the passing gate. The requested main protection will require `VAD PR gate`, both Python matrix checks, an up-to-date base, PR-based changes, and administrator enforcement; force pushes and branch deletion are disabled. Separate GitHub reviewer count is zero for this single-maintainer repository; the VAD human-review record remains required.

Implementation plan and policy: `docs/vad-ci.md`. Evidence and previous protection snapshot: `.vad/evidence/pr-gate/`. Human approval for this new change is pending; prior approvals are not reused.
