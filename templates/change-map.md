# Change Map

* **Feature / PR:**
* **Author:**
* **Reviewer:**
* **Risk level:**
* **Requirement contract:** (link)

Do not record secrets, tokens, credentials, private keys, or sensitive payload
contents in VAD artifacts. Record references or identifiers instead when needed.

## Summary

One short paragraph: what changed and why.

## File map

The file map is the change-provenance record (what changed, why, risk, verification).

| File | Change | Reason | Risk | Verification |
| ---- | ------ | ------ | ---- | ------------ |
|      |        |        |      |              |

## Requirement links

Which acceptance criteria does each major edit satisfy?

## Dependencies / migrations

Schema, feature flags, config, client versions.

## Operational impact

Logging, metrics, alerts, quotas, cost.

## Instruction Provenance

Complete this section only if this change **relied on or modified** persistent
AI instructions. **N/A is acceptable otherwise.** Complete only when applicable
by risk or scope.

Persistent instructions include `AGENTS.md`, `CLAUDE.md`, repository
instructions, persistent system prompts, and persistent agent rules.

Temporary conversational prompts are out of scope.

Record the reason for every meaningful persistent instruction that this change
relied on or modified. Do not copy or document every existing instruction file
simply because it exists. Treat these as maintainable software artifacts rather
than permanent accumulated memory.

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
- Accountable / rollback owner: see Verification Report → Approval

## Rollback plan

Steps to disable or revert. Name of owner-of-record: see Verification Report →
Approval (do not create a second owner-of-record here).
