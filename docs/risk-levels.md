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

## v0.2 evidence depth by risk

The six core properties and seven stages are unchanged. Evidence depth scales
with risk. See [RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).

| Evidence | Low | Medium | High / Critical |
| -------- | --- | ------ | --------------- |
| Requirement ambiguity / clarification | Optional one-liner | Record if AI-assisted | Required; blocking questions must be resolved |
| Instruction provenance | If instruction files change | If AI-assisted | Required if instruction files exist or change |
| Agent execution evidence | If an agent ran | If an agent ran | Required whenever an agent ran |
| Verification cost | Skip or one line; not every measurable field | Brief | Required; justify coverage vs risk |
| Performance / operational evidence | Only if performance is in scope | If performance is in scope | Required when performance, cost, or capacity is in scope |

Expensive ceremony is not the goal. Missing evidence on a high-risk change is.
Low-risk work must not be required to measure every verification-cost field.
