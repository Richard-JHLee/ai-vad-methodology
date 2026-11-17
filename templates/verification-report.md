# Verification Report

* **Feature / PR:**
* **Author:**
* **Approver:**
* **Risk level:**
* **Date:**

Do not record secrets, tokens, credentials, private keys, or sensitive payload
contents in VAD artifacts. Record references or identifiers instead when needed.

## Verification scope and evidence (proposed)

See [RFC 0003](../rfcs/0003-verification-decisions.md). Keep this compact for
Low-risk work; links to existing CI reports may supply the details.

* Candidate revision: (commit SHA, or base SHA + saved working-diff reference)
* Environment / relevant config and dependency versions:
* Affected callers, screens, APIs, data, permissions, existing behavior:
* Baseline checks / known pre-existing failures / unavailable checks:
* Check selection and reason for full suite, if used:

Use these states throughout this report:

| State | Meaning |
| ----- | ------- |
| Pass | Ran; observed result met the stated expectation in the recorded scope. |
| Fail | Ran; observed result did not meet the expectation. |
| Blocked | Could not run or finish; record the missing prerequisite. |
| Not run | Applicable but not attempted; record why and the remaining risk. |
| N/A | Outside the analyzed impact; record why. |

N/A does not mean an environment was unavailable. Blanks are not passing checks.
Use acceptance-criterion IDs or short descriptions. Derive expected behavior
from the requirement or established contract, not just the generated code.

| Criterion / risk | Command or manual procedure | Expected | Observed / state | Time / evidence reference |
| ---------------- | --------------------------- | -------- | ---------------- | ------------------------- |
| | | | | |

The sections below may reference these entries instead of duplicating evidence.
After code, requirement, dependency, config, or deployment-context changes,
rerun affected checks and explain why any retained evidence still applies.

## 1. Static verification

| Check | Result | Notes |
| ----- | ------ | ----- |
| Build / compile | | |
| Lint / types | | |
| Secrets / unsafe APIs | | |
| Dependency diff reviewed | | |

## 2. Functional verification

| Scenario | Result | Evidence |
| -------- | ------ | -------- |
| Happy path | | |
| Invalid input | | |
| Permission denied | | |
| Boundary / edge | | |

## 3. Regression verification

Related flows / APIs / jobs rechecked:

-

## 4. Operational verification

| Item | Ready? | Notes |
| ---- | ------ | ----- |
| Logging | | |
| Monitoring / alerts | | |
| Rollback / feature flag | | |
| Migration safety | | |

A checkbox is not operational evidence. When performance, capacity, or
infrastructure cost is in scope, complete Operational Evidence below.

## 5. AI-generated tests

List AI-written tests and what was independently reviewed or supplemented.

## 6. Known limitations and residual risk

-

## 7. Deployment conditions

* Target environment / rollout stages / flags:
* Health signals and stop / rollback thresholds:
* Observation window and person monitoring:
* Recovery steps and evidence of readiness: (include exercise for Critical)
* Data / external side-effect recovery: (code revert alone may not undo these)

Use N/A with a reason for items outside scope, such as deployment for a copy edit.

## 8. Approval / Accountability

Canonical rollback / accountable owner-of-record:

* Technical approver:
* (Critical) Independent reviewer:
* Rollback owner:

Proposed decision record (RFC 0003):

* Next gate: (merge / limited rollout / broader release)
* Decision: Ready / Not ready / Ready with accepted residual risk
* Approved candidate revision / approver / date: (pending until human approval)
* Unresolved Fail / Blocked / Not run entries:
* If an exception is allowed: gap, plausible harm, compensating controls,
  accepting human, follow-up owner and due date:

Required failed or missing checks default to Not ready. Exceptions do not change
check results to Pass or override non-waivable team controls. Approval does not
automatically apply to a changed candidate. Merge readiness is not production
validation; recovery must meet the release requirement before deployment.

## Operational Evidence

Complete only when applicable by risk or scope. **N/A is acceptable when not
applicable.** Record only the metrics relevant to the change.

**Operational Evidence** is the parent heading. **Performance Evidence** may
include the runtime metrics below. **Operational cost** is post-merge runtime
/ infrastructure cost caused by the change; record it here, not as a separate
verification result.

Passing functional tests does not prove that generated code is operationally
efficient.

- CPU impact:
- Memory impact:
- Query impact:
- Allocations:
- Latency impact:
- External API impact:
- Infrastructure cost:

## Verification Cost

Complete only when applicable by risk or scope. **N/A is acceptable when not
applicable.**

Verification Cost is a **lifecycle process measure**. It is **not** evidence
that the change is correct.

Definition: the **pre-merge** effort and resource cost required to establish
sufficient confidence in a change.

AI-assisted productivity must be evaluated across the full change lifecycle,
not only at the point of code generation.

A change is not necessarily more productive if faster generation creates
disproportionate review, verification, or operational cost.

Optional proxies (not a mandatory census). Static-analysis *findings* themselves
are verification results (section 1); the *count or effort* associated with
resolving them may be a Verification Cost input. Time to merge is an optional
proxy because it may include queue time.

Fill fields in proportion to [risk level](../docs/risk-levels.md). Low-risk
changes are not required to measure every item.

- Reviewer iterations:
- Review comments:
- Time to merge (optional proxy; may include queue time):
- Test execution cost:
- Static-analysis finding count / resolution effort:
- Human review effort:
- Unresolved verification uncertainty:

## Agent Execution Evidence (if applicable)

Complete only when applicable by risk or scope. **N/A is acceptable when not
applicable** (including when no agent ran).

**Not a verification result.** This is cross-stage execution context produced
during agent execution and referenced from the
[Change Map](./change-map.md). It is **input** to verification and
accountability. Do not treat this block as an eighth workflow stage or a sixth
required artifact. Do not require the full field list for every agent-assisted
change.

Depth by [risk level](../docs/risk-levels.md):

* **Low** (only if an agent executed the change): initiating human; agent /
  model; accountable owner.
* **Medium:** add tools or persistent instructions when relevant.
* **High / Critical:** use the full set when the agent accessed elevated
  permissions, MCP servers, external systems, production systems, or sensitive
  credentials or data.

- Initiating human:
- Agent / model used:
- Delegated agents:
- Tools invoked:
- MCP servers accessed:
- Permissions granted:
- External systems accessed:
- Generated artifacts:
- Verification results (inputs, not conclusions):
- Human approvals:
- Execution cost:
- Accountable owner: (same person as Approval → Rollback owner, or N/A)
