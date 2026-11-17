# VAD example: Python API verification decision

**Illustrative only.** This is a fictional walkthrough, not executable code, a
test run, or evidence of VAD effectiveness. Paths and checks below describe a
hypothetical Python service. No implementation or test files are supplied here.
It demonstrates [RFC 0003](../../rfcs/0003-verification-decisions.md) using the
existing artifacts; sections may live together in one PR description.

## 1. Requirement contract

**Change:** add an optional `limit` query parameter to `GET /items`.
**Owner:** API maintainer (illustrative role; assign a named human in real use).
**Risk:** Medium, assuming a read-only service with bounded responses and an
existing authorization boundary. Reclassify if analysis finds broader harm.

| Criterion | Expected behavior |
| --------- | ----------------- |
| AC-1 | Omitting `limit` retains the existing default of 20 and existing response shape. |
| AC-2 | Integer `limit` from 1 through 100 returns at most that many authorized items. |
| AC-3 | Values 0, 101, or non-integers return the established validation error (422). |
| AC-4 | Authentication remains required; results contain only the caller's tenant data. |

No writes, schema changes, new dependencies, sorting changes, or new roles.
Confirm these assumptions in the real system before coding. Recovery expectation:
revert the optional parameter support while preserving the original endpoint.

## 2. System map and pre-change checks

```text
Client → existing authentication → GET /items handler
       → tenant-scoped repository query → serializer → response
```

Inspect handler callers, repository filtering, and existing client tests. Confirm
the query applies the limit before materializing results and does not bypass
tenant filtering. The endpoint and its clients are in scope; unrelated write
paths are outside scope only after confirming no shared helper changes.

Run existing endpoint and tenant-isolation tests before editing when feasible.
Record their actual baseline results; none were run for this walkthrough.

## 3. Change map and controlled generation

| Hypothetical file | Planned change | Risk / verification |
| ----------------- | -------------- | ------------------- |
| `app/routes/items.py` | Validate and pass optional limit through existing query path | Default and invalid-input contract checks |
| `app/repositories/items.py` | Apply bounded limit to the existing tenant-scoped query | Tenant isolation and query-bound checks |
| `tests/test_items.py` | Cover AC-1 through AC-4 | Human reviews expected results against the contract |

Keep existing authorization and error handling. If query helpers are shared,
expand caller analysis and tests before proceeding. No new ADR is needed unless
an architectural decision emerges. Persistent instruction provenance: N/A in this
fictional scenario; real work records relied-on or modified instructions.

## 4. Verification report — deliberately incomplete

Candidate revision: not available; no implementation exists in this example.
Environment: not available. All applicable checks are **Not run**, not Pass.
Real reports must record revision, environment, execution time, observed result,
and accessible evidence references.

| Criterion / risk | Planned procedure | Expected | State / evidence |
| ---------------- | ----------------- | -------- | ---------------- |
| AC-1 | `pytest tests/test_items.py -k default` | Default 20 and unchanged response shape | Not run; illustrative command only |
| AC-2 | `pytest tests/test_items.py -k limit_bounds` | Limits 1 and 100 respected; query bounded before materialization | Not run; test and query inspection needed |
| AC-3 | `pytest tests/test_items.py -k invalid_limit` | 422 for 0, 101, and non-integers | Not run; illustrative command only |
| AC-4 | `pytest tests/test_items.py -k 'authentication or tenant'` | Unauthenticated requests denied; no cross-tenant results | Not run; illustrative command only |
| Schema migration | Inspect actual diff for schema / write changes | No migration in this scenario | N/A for the hypothetical plan; recheck actual diff |

Focused tests follow the endpoint and tenant boundary. A full suite is warranted
if the actual change touches shared query or validation infrastructure. Runtime
query size is in scope; correctness tests alone do not establish latency or cost.
Measure relevant operational impact before asserting it. Another model agreeing
with the code does not replace these checks or human review.

## 5. Decision, deployment, and recovery

**Decision: Not ready.** Required checks are Not run and there is no candidate or
human approval. This example does not authorize a release.

For a real release, name the approver, candidate revision, and rollback owner.
Specify a limited rollout, observation window, and numeric error/latency thresholds
based on the service's baseline and requirements before rollout. These values
remain unset here. Revert the candidate on a breached threshold; confirm the
original endpoint behavior afterward. There are no intended writes in this
scenario; if that assumption changes, reassess risk and data recovery.

After implementation or config changes, rerun affected checks and update the
decision. Until actual results and operational conditions are recorded, readiness
remains Not ready.
