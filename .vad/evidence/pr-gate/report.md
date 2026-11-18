# VAD merge verification report

Decision: Not ready

Self-reported evidence and review; no production readiness claim.

## Verification

All planned checks have current passing or N/A records.

## Human review

Pending: no approval record matches the current source, plan and results.

## Next steps

After verification, a responsible human must review the plan and evidence before recording approval. Do not fabricate or automatically grant approval.

## Full record

    {
      "status": {
        "decision": "Not ready",
        "gate": "merge",
        "context": "367346c967bb9b6586e885ece4405e0f4334558fc46f1519f972db8da0b91474",
        "gaps": [],
        "human_review_recorded": false,
        "note": "Self-reported records, not authenticated identity or proof of correctness"
      },
      "record": {
        "schema_version": 1,
        "plan": {
          "title": "Actual PR VAD gate and main branch protection",
          "owner": "Richard Lee; review pending for this change",
          "risk": "Medium",
          "purpose": "Require a current VAD record plus passing Python tests for main PRs and demonstrate both blocked and allowed paths on an actual PR.",
          "environment": "Local macOS Python 3.13.2; GitHub Ubuntu 24.04 Python 3.9 and 3.13; GitHub Actions contents:read; administrator API used only for requested branch protection.",
          "recovery": "Restore the saved previous main protection settings if needed; revert the PR workflow and selector helper together. No VAD record schema or user data migration.",
          "impact": {
            "paths": "PR workflow -> selected_change_id -> existing paths ID validation -> existing check/report. Main protection requires the three actual check-run names.",
            "data": "Add one CI selection pointer and a new change record. Preserve all historical records and approvals; do not reuse past approval for this new source.",
            "permissions": "Read-only Actions, no persisted checkout credentials, no pull_request_target. Requested repository administration enables main branch protection. Existing PR #3 must also satisfy new policy.",
            "regression": "Manual input and reusable workflow remain supported; strict PR check gets a unique name so manual success cannot satisfy it. Default PR merge tree is verified; missing or invalid pointer blocks."
          },
          "criteria": {
            "AC-1": "PRs targeting main automatically run a strict VAD PR gate for a validated .vad/ci-change-id selection.",
            "AC-2": "Missing, malformed and symlinked selection files fail; dynamic IDs cannot inject workflow outputs.",
            "AC-3": "Actual PR without current human approval is blocked while diagnostics remain available.",
            "AC-4": "Main requires the observed VAD PR gate and both Python test contexts, up-to-date base, PR changes, no admin bypass, no force-push/deletion.",
            "AC-5": "Existing CLI, manual gate, source freshness and read-only checks remain intact; human approval remains explicit."
          },
          "checks": {
            "regression": {
              "criteria": [
                "AC-1",
                "AC-2",
                "AC-5"
              ],
              "procedure": "Run CLI integration suite and selector cases locally; verify both Python matrix jobs on actual PR.",
              "expected": "All tests pass; invalid selector cases reject; manual explicit IDs still validate."
            },
            "docs": {
              "criteria": [
                "AC-4",
                "AC-5"
              ],
              "procedure": "Check YAML, Python 3.9 syntax, local Markdown targets, documented JSON and whitespace. Review planned protection settings and saved previous policy.",
              "expected": "Documentation and configuration match the implemented policy; no unsupported claim of native reviewer authentication."
            },
            "pr-blocking": {
              "criteria": [
                "AC-1",
                "AC-3"
              ],
              "procedure": "Open actual PR, observe failed VAD PR gate from missing verification/approval and successful diagnostics export.",
              "expected": "Actual PR cannot satisfy readiness before review; no fabricated approval."
            },
            "protection": {
              "criteria": [
                "AC-4"
              ],
              "procedure": "Apply requested main protection using actual GitHub Actions check names; GET policy and inspect actual PR merge state while VAD fails.",
              "expected": "Required contexts and admin enforcement match intended policy; PR is blocked without bypass."
            }
          },
          "agent_execution": {
            "initiating_human": "User requested actual PR validation and branch protection/required checks",
            "agent": "Codex; model identifier not recorded",
            "tools": "Python, Git, GitHub CLI, GitHub REST API",
            "approval": "New change awaits explicit human review; prior Richard Lee approval is not reused."
          }
        },
        "results": [
          {
            "check": "regression",
            "state": "Pass",
            "observed": "33 local CLI tests passed and both Python 3.9/3.13 jobs succeeded on actual PR #5.",
            "evidence": ".vad/evidence/pr-gate/local-tests.txt; .vad/evidence/pr-gate/pr-ci-success.json",
            "context": "367346c967bb9b6586e885ece4405e0f4334558fc46f1519f972db8da0b91474",
            "time": "2026-11-18T02:53:55.677329+00:00",
            "head": "20ee1ad63043d2a5d478a82b342c17a13f711df0"
          },
          {
            "check": "docs",
            "state": "Pass",
            "observed": "PASS: YAML and Python 3.9 syntax checked; 32 Markdown files and 110 local links checked; actual selection step rejects newline injection; protection readback and PR BLOCKED state match intended policy.",
            "evidence": ".vad/evidence/pr-gate/docs-checks.txt; .vad/evidence/pr-gate/protection-before.json",
            "context": "367346c967bb9b6586e885ece4405e0f4334558fc46f1519f972db8da0b91474",
            "time": "2026-11-18T02:53:55.828924+00:00",
            "head": "20ee1ad63043d2a5d478a82b342c17a13f711df0"
          },
          {
            "check": "pr-blocking",
            "state": "Pass",
            "observed": "Actual pull_request run selected ci-pr-enforcement, matched the local source context, refused missing verification/approval and uploaded its report.",
            "evidence": ".vad/evidence/pr-gate/negative-run/check.json; .vad/evidence/pr-gate/negative-run/report.md",
            "context": "367346c967bb9b6586e885ece4405e0f4334558fc46f1519f972db8da0b91474",
            "time": "2026-11-18T02:53:55.982752+00:00",
            "head": "20ee1ad63043d2a5d478a82b342c17a13f711df0"
          },
          {
            "check": "protection",
            "state": "Pass",
            "observed": "Main protection readback confirms all three GitHub Actions App-bound checks, strict base, administrator enforcement, PR requirement and blocked PR #5 while VAD fails.",
            "evidence": ".vad/evidence/pr-gate/protection-readback.json; .vad/evidence/pr-gate/protected-pr-blocked.json",
            "context": "367346c967bb9b6586e885ece4405e0f4334558fc46f1519f972db8da0b91474",
            "time": "2026-11-18T02:53:56.136296+00:00",
            "head": "20ee1ad63043d2a5d478a82b342c17a13f711df0"
          }
        ],
        "approvals": []
      }
    }
