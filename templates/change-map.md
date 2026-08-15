# Change Map

* **Feature / PR:**
* **Author:**
* **Reviewer:**
* **Risk level:**
* **Requirement contract:** (link)

## Summary

One short paragraph: what changed and why.

## File map

| File | Change | Reason | Risk | Verification |
| ---- | ------ | ------ | ---- | ------------ |
|      |        |        |      |              |

## Requirement links

Which acceptance criteria does each major edit satisfy?

## Dependencies / migrations

Schema, feature flags, config, client versions.

## Operational impact

Logging, metrics, alerts, quotas, cost.

## Change provenance

What changed, why, requirement link, risk, and how verification will be shown.

(The file map above is the primary change-provenance record.)

## Instruction Provenance

Persistent AI instructions such as `AGENTS.md`, `CLAUDE.md`, system prompts,
and repository rules used or changed by this work. Treat these as maintainable
software artifacts rather than permanent accumulated memory.

Record the reason for every meaningful instruction.

| Rule | Why it exists | Failure / risk it prevents | Introduced | Scope | Remove when |
| ---- | ------------- | -------------------------- | ---------- | ----- | ----------- |
|      |               |                            |            |       |             |

## Agent execution evidence (pointer)

Agent execution evidence is **cross-stage**. It records what executed the
change. It is **not** a verification result and **not** a workflow stage.

If an agent ran, complete the Agent Execution Evidence block in the
[Verification Report](./verification-report.md) (detail lives there as an
input to verification and accountability). Record a pointer here:

- Agent execution evidence: (link or N/A — no agent)
- Rollback owner:

## Rollback plan

Steps to disable or revert.
