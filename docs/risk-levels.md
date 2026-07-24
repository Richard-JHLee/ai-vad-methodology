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
