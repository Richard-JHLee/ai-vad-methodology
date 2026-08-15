# VAD Workflow

VAD defines seven primary stages. Evidence fields proposed in
[RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md) attach to these stages;
they do not add an eighth stage.

```text
1. Requirement Definition
2. System Analysis
3. Change Scope Limitation
4. Controlled Code Generation
5. Change Mapping
6. Automated and Human Verification
7. Progressive Deployment
```

## 1. Requirement Definition

Define expected behavior before generation: purpose, inputs/outputs, roles,
failure conditions, data rules, security, performance, and recovery.

Inside this stage (not a new top-level stage):

```text
Requirement Definition
  → Ambiguity Detection
  → Requirement Clarification
  → Acceptance Criteria
  → Implementation
```

Record requirement ambiguity: known ambiguities, missing information,
assumptions, questions requiring human clarification, and implicit
requirements discovered. Unresolved blocking ambiguity is a stop condition.

**Key question:** What exactly should happen, and when should it fail?

Artifact: [requirement-contract.md](../templates/requirement-contract.md)

## 2. System Analysis

Map related files, entry points, APIs, data flow, auth boundaries, jobs, and
clients before editing.

**Key question:** Which parts of the system could be affected?

Artifact: [system-map.md](../templates/system-map.md)

## 3. Change Scope Limitation

Keep changes small enough for humans to review. Default guidance:

* one feature or concern,
* roughly three to five primary files when practical,
* no unrelated refactoring or hidden upgrades.

Larger changes need stronger evidence and clearer decomposition.

## 4. Controlled Code Generation

AI implements only the approved requirement and scope. Before coding, it should
state planned files, non-goals, assumptions, risks, and tests. Developers review
that plan before accepting implementation.

Persistent AI instructions relied on during generation (`AGENTS.md`,
`CLAUDE.md`, system prompts, repository rules) should carry **instruction
provenance**. If an agent executes the work, produce **agent execution
evidence** as the work happens. That evidence is cross-stage: it records what
executed the change. It is not a verification result and not an eighth stage.

## 5. Change Mapping

Produce a change map covering:

* **change provenance** — what changed, why, requirement link, risks, how it
  was verified,
* **instruction provenance** — persistent AI instructions used or changed,
* **a pointer to agent execution evidence** when an agent ran.

Artifact: [change-map.md](../templates/change-map.md)

## 6. Automated and Human Verification

Verify in layers. These layers are verification results:

* correctness (static and functional),
* security,
* regression,
* performance evidence,
* operational cost,
* verification cost.

**Performance evidence:** for performance-sensitive changes, record measurable
runtime impact (CPU, memory, queries, allocations, latency, external API
calls, infrastructure cost). Passing functional tests does not prove that
generated code is operationally efficient.

**Verification cost:** evaluate not only whether a change is correct, but also
how expensive it is to verify. AI-assisted productivity must be evaluated
across the full change lifecycle, not only at the point of code generation.
A change is not necessarily more productive if faster generation creates
disproportionate review, verification, or operational cost. Depth scales by
[risk level](./risk-levels.md); Low-risk work is not required to fill every
field.

**Key principle:** AI-generated tests are inputs, not final results.

Artifact: [verification-report.md](../templates/verification-report.md)

## Agent execution evidence (cross-stage)

Not a workflow stage. Not a verification result.

Agent execution evidence is produced during agent execution and referenced by
both the Change Map (pointer) and the Verification Report (detail). It records
what executed the change: initiating human, agent/model, delegated agents,
tools, MCP servers, permissions, external systems, generated artifacts,
verification results used as inputs, human approvals, execution cost, and
rollback owner.

It serves as **input** to verification and accountability (Traceable,
Accountable). Depth: only when an agent ran.

## 7. Progressive Deployment

Passing tests is not production safety. Roll out by risk:

```text
Local → Development → Internal users → Limited production → Broader release
```

Observe and recover here: health metrics, error-rate thresholds, automatic
rollback, and named owners. This is Recoverable, not an eighth stage.

**Key question:** Can this change be stopped or reversed before it affects every user?

## Completion criteria

A responsible developer should be able to explain purpose, scope, impact,
failure modes, evidence, recovery, and ownership. See [README.md](../README.md).

## Stop conditions

Stop when scope expands unexpectedly, a security boundary is unclear, data loss
is possible, required tests cannot run, rollback is unavailable for high-risk
work, assumptions cannot be verified, or blocking requirement ambiguity remains
unresolved.
