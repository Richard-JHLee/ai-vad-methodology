# Requirement Contract

* **Project / feature:**
* **Owner:**
* **Risk level:** Low / Medium / High / Critical
* **Date:**
* **Related issue / ticket:**

Do not record secrets, tokens, credentials, private keys, or sensitive payload
contents in VAD artifacts. Record references or identifiers instead when needed.

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

Complete only when applicable by risk or scope. **N/A is acceptable when not
applicable.**

Inside Stage 1 (not a new workflow stage):

```text
Requirement Definition
  → Ambiguity Detection
  → Requirement Clarification
  → Acceptance Criteria
```

Implementation belongs to controlled code generation (Stage 4), not this stage.

A **blocking ambiguity** is an unresolved requirement uncertainty that could
materially change one or more of:

- implementation scope,
- acceptance criteria,
- security or privacy behavior,
- data handling,
- permissions or authorization,
- externally observable behavior,
- rollback or operational risk.

Non-blocking ambiguity may be recorded as an accepted assumption.

Unresolved blocking ambiguity is a stop condition. Code generation must not
proceed until the ambiguity is either (1) clarified, or (2) explicitly accepted
by the responsible human as residual risk.

Depth by [risk level](../docs/risk-levels.md):

* **Low:** one-line entry is sufficient when ambiguity exists; N/A is
  acceptable when requirements are clear. The five fields below are not
  mandatory.
* **Medium:** complete only when meaningful ambiguity, assumptions, or
  clarification exist. Do not fill this section merely because AI assistance
  was used.
* **High / Critical:** blocking ambiguity must be resolved or explicitly
  accepted as residual risk.

See [RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).

- Known ambiguities:
- Missing information:
- Assumptions made:
- Questions requiring human clarification:
- Implicit requirements discovered:
- Blocking? (Y/N) and disposition (clarified / accepted residual risk / N/A):

## 10. Acceptance criteria

- [ ]
- [ ]

## 11. Recovery / rollback expectations

How do we disable or reverse this if it misbehaves?

## 12. Explicit non-goals

What will this change **not** do?
