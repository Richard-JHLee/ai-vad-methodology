# Risk-Based Application

Not every change needs the same process depth. Apply VAD controls in proportion
to potential damage.

| Risk level | Example | Recommended controls |
| ---------- | ------- | -------------------- |
| **Low** | Copy change, isolated UI tweak | Change map + basic test |
| **Medium** | New API, business-rule update | Requirement contract, tests, impact analysis |
| **High** | Auth, payment, subscription, migration | Full VAD artifacts, security review, progressive rollout |
| **Critical** | Financial/medical data, infra, irreversible migration | Independent review, recovery exercise, monitoring, explicit approval |

## How to choose a level

Ask:

1. What is the worst plausible user or data harm?
2. Can the change be rolled back quickly?
3. Does it touch money, identity, privacy, or irreversible state?
4. How many systems and clients depend on the path?

When unsure, choose the higher level for the first release of a change, then
relax process for later low-risk iterations once the blast radius is known.

## Anti-patterns

* Treating every typo fix as Critical (process fatigue).
* Treating payment or auth changes as Low because “tests passed”.
* Skipping recovery planning because rollback “should be easy”.
* Filling every verification-cost field on a Low-risk change.
* Filling instruction provenance or requirement ambiguity merely because AI
  assistance was used.
* Copying every existing instruction file because it exists.
* Requiring the full agent-execution field list for every agent-assisted change.

## v0.2 evidence depth by risk

The six core properties and seven stages are unchanged. Evidence depth scales
with risk. See [RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md). Templates
must show N/A and risk captions; do not treat every blank as mandatory.

| Evidence | Low | Medium | High / Critical |
| -------- | --- | ------ | --------------- |
| Requirement ambiguity / clarification | One-liner if ambiguity exists; N/A if requirements are clear | Complete only if meaningful questions or assumptions exist | Blocking ambiguity resolved or explicitly accepted as residual risk |
| Instruction provenance | Only if this change relied on or modified persistent instructions | Only if this change relied on or modified persistent instructions | Same: do not document files merely because they exist |
| Agent execution evidence | If an agent ran: initiating human, agent/model, accountable owner | Add tools or persistent instructions when relevant | Full set when elevated permissions, MCP, external/production systems, or sensitive data |
| Verification cost | Skip or one line; not every proxy | Brief | Required; justify coverage vs risk |
| Operational evidence | Only metrics in scope | If performance, cost, or capacity is in scope | Required when performance, cost, or capacity is in scope |

Expensive ceremony is not the goal. Missing evidence on a high-risk change is.
Low-risk work must not be required to measure every verification-cost field.
Medium work must not trigger ambiguity and instruction-provenance sections
merely because AI assistance was used.
