# Verification Report

* **Feature / PR:**
* **Author:**
* **Approver:**
* **Risk level:**
* **Date:**

## 1. Static verification

| Check | Result | Notes |
| ----- | ------ | ----- |
| Build / compile | Pass / Fail / N/A | |
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

A checkbox is not performance evidence. When performance, capacity, or
infrastructure cost is in scope, complete Operational Evidence below.

## 5. AI-generated tests

List AI-written tests and what was independently reviewed or supplemented.

## 6. Known limitations and residual risk

-

## 7. Deployment conditions

Environments, flags, progressive rollout plan.

## 8. Approval

* Technical approver:
* (Critical) Independent reviewer:
* Rollback owner:

## Operational Evidence

For performance-sensitive changes, verification should consider measurable
runtime impact. Passing functional tests does not prove that generated code is
operationally efficient.

- CPU impact:
- Memory impact:
- Query impact:
- Latency impact:
- External API impact:
- Estimated infrastructure cost:
- Allocations:

## Verification Cost

AI-assisted development should evaluate not only whether a change is correct,
but also how expensive it is to verify.

AI-assisted productivity must be evaluated across the full change lifecycle,
not only at the point of code generation.

A change is not necessarily more productive if faster generation creates
disproportionate review, verification, or operational cost.

Faster generation is not an improvement if the saved generation cost is
transferred into disproportionate verification cost.

Fill fields in proportion to [risk level](../docs/risk-levels.md). Low-risk
changes are not required to measure every item.

- Reviewer iterations:
- Review comments:
- Time to merge:
- Test execution cost:
- Static-analysis findings:
- Human review effort:
- Unresolved verification uncertainty:

## Agent Execution Evidence (if applicable)

**Not a verification result.** This is cross-stage execution evidence produced
during agent execution and referenced from the
[Change Map](./change-map.md). It records what executed the change and serves
as **input** to verification and accountability. Omit if no agent ran. Do not
treat this block as an eighth workflow stage.

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
- Rollback owner:
