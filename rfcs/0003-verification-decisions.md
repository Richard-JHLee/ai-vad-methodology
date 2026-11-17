# RFC 0003: Verification Decisions

* **Status:** Draft
* **Created:** 2026-11-17
* **Relates to:** [RFC 0001](./0001-vad-core.md), [RFC 0002](./0002-vad-v0.2-evidence-model.md)

## Summary

Make verification claims inspectable: connect acceptance criteria and affected
paths to checks, bind results to the checked revision, distinguish missing
evidence from passing evidence, and record a human release decision.

This proposal extends the existing System Analysis, Verification, and Deployment
stages and Verification Report. It adds no stage, principle, or required artifact.
The documented core version remains Draft 0.1; this RFC is not an accepted standard.

## Motivation

The evidence model describes what to record but leaves several decisions implicit:
whether a check actually ran, whether its result covers the current change,
whether its expected behavior came from the requirement, and whether unresolved
gaps permit release. A list of green checks alone does not answer these questions.

These are design concerns, not measured claims about VAD's effectiveness.

## Proposal

### 1. Select checks from impact

Before implementation, trace entry points, callers, data, permissions, affected
screens and clients, and existing behavior. Select the smallest checks that cover
that impact, including relevant failure and denial paths. Run those checks on the
baseline when feasible to identify pre-existing failures; record limitations.
After implementation, run checks against the candidate change.

Use the full suite when shared foundations prevent a narrower scope, or focused
checks reveal a concrete regression risk. Record the reason. A full suite does
not replace impact analysis; narrow tests do not justify ignoring risky paths.

Risk classification follows plausible harm, exposure, and recoverability, not
file count. Reassess when callers, data effects, or permissions expand.

### 2. Bind claims to evidence

In the existing Verification Report, record:

* candidate revision (commit SHA, or base SHA plus saved working-diff reference),
* environment and relevant configuration or dependency versions,
* acceptance criterion or risk, command or manual procedure, expected behavior,
* observed result, time, and accessible evidence reference.

Use non-sensitive fixtures and redact outputs. A CI log or test report may supply
these details by reference. Low-risk work may use one compact entry. Do not copy
entire logs or create five separate documents for a typo fix.

Expected behavior must follow the requirement or an established contract, not
merely repeat the implementation. For a bug fix, reproduce the reported failure
before the fix when feasible. Another AI reviewer may help find errors, but is
not by itself independent evidence or a substitute for accountable human review.

### 3. Distinguish result states

| State | Meaning |
| ----- | ------- |
| Pass | Executed; observed behavior met the stated expectation in the recorded scope. |
| Fail | Executed; observed behavior did not meet the expectation. |
| Blocked | Could not execute or finish because a prerequisite was unavailable; give the reason. |
| Not run | Applicable but not attempted; give the reason and remaining risk. |
| N/A | Not applicable to the analyzed impact; give the reason. |

Blocked and Not run are verification gaps. N/A cannot stand in for an unavailable
environment or permission. Failed checks stay visible, including pre-existing
failures; a later pass records a new result rather than erasing history.

### 4. Reassess evidence after changes

Changes to code, requirements, dependencies, configuration, or deployment context
require a coverage review. Rerun affected checks and record why retained results
still apply. Do not carry approval forward automatically to a different candidate.

### 5. Separate verification from release

Record one human decision: **Ready**, **Not ready**, or **Ready with accepted
residual risk**, with approver, candidate revision, and date. Unresolved required
checks default to Not ready. An exception records the gap, plausible harm,
compensating controls, accountable human, and follow-up owner and due date.
It does not convert Fail, Blocked, or Not run to Pass. Teams may prohibit
exceptions for particular controls; VAD does not override those rules.

Ready means ready for the specified next gate, not proof of production safety.
For deployment, specify the environment, observable stop/rollback trigger,
observation window, and rollback owner where applicable. A code revert does not
undo data writes or external side effects: describe data recovery separately.
When recovery cannot meet the requirement, do not declare deployment ready.

## Adoption and validation

Use the updated [workflow](../docs/workflow.md),
[report template](../templates/verification-report.md), and
[illustrative walkthrough](../examples/python/README.md). Existing historical
reports need not be rewritten. Apply this proposal to new changes incrementally.

Evaluate it using real changes: can a reviewer locate the checked revision,
identify missing coverage, and explain the release decision? Record review effort,
escaped defects, and recovery outcomes with context before claiming improvement.
The walkthrough is illustrative and supplies no empirical validation.

## Alternatives and risks

* Always run all tests: may add cost without covering omitted requirements.
* Add a new evidence artifact: duplicates the Verification Report.
* Infer readiness from green CI: hides scope gaps and human responsibility.

Risks include template overhead, inaccessible evidence, and routine exceptions
that bypass verification. Keep Low-risk entries short, retain accessible sanitized
references according to team policy, and review outstanding exceptions.

## Open questions

* Which controls should organizations designate as non-waivable?
* What evidence retention period fits each system's risk and privacy constraints?
* How much reporting can existing CI supply without duplicating results?

## Decision

Pending discussion.
