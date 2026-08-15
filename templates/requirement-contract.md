# Requirement Contract

* **Project / feature:**
* **Owner:**
* **Risk level:** Low / Medium / High / Critical
* **Date:**
* **Related issue / ticket:**

## 1. Purpose

Why does this change exist?

## 2. Actors and permissions

Who can trigger the behavior? Who must be denied?

## 3. Inputs and outputs

| Input | Type / constraints | Output | Notes |
| ----- | ------------------ | ------ | ----- |
|       |                    |        |       |

## 4. Expected behavior

Describe the happy path step by step.

## 5. Failure conditions

What must fail closed? Error messages / codes?

## 6. Data rules

What is created, updated, deleted? Idempotency? Retention?

## 7. Security and privacy

Authn/authz, secrets, PII, audit logging.

## 8. Performance / limits

Latency, rate limits, payload size, cost constraints.

## 9. Requirement Ambiguity

Inside Stage 1 (not a new workflow stage):

Requirement Definition → Ambiguity Detection → Requirement Clarification
→ Acceptance Criteria → Implementation

- Known ambiguities:
- Missing information:
- Assumptions made:
- Questions requiring human clarification:
- Implicit requirements discovered:

Unresolved blocking ambiguity is a stop condition. Do not generate code until
it is resolved or explicitly accepted as residual risk. Depth scales by
[risk level](../docs/risk-levels.md). See
[RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).

## 10. Acceptance criteria

- [ ]
- [ ]

## 11. Recovery / rollback expectations

How do we disable or reverse this if it misbehaves?

## 12. Explicit non-goals

What will this change **not** do?
