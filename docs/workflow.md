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
```

Implementation belongs to Stage 4 (Controlled Code Generation), not this stage.

A **blocking ambiguity** is an unresolved requirement uncertainty that could
materially change implementation scope, acceptance criteria, security or privacy
behavior, data handling, permissions or authorization, externally observable
behavior, or rollback or operational risk. Non-blocking ambiguity may be
recorded as an accepted assumption.

Unresolved blocking ambiguity is a stop condition. Code generation must not
proceed until the ambiguity is either (1) clarified, or (2) explicitly accepted
by the responsible human as residual risk.

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

Persistent AI instructions relied on or modified during generation
(`AGENTS.md`, `CLAUDE.md`, repository instructions, persistent system prompts,
persistent agent rules) should carry **instruction provenance**. Temporary
conversational prompts are out of scope. Record the reason for every meaningful
persistent instruction; do not document every instruction file simply because
it exists.

If an agent executes the work, produce **agent execution evidence** as the work
happens. That evidence is cross-stage: it records what executed the change. It
is not a verification result and not an eighth stage. Depth scales by
[risk level](./risk-levels.md).

## 5. Change Mapping

Produce a change map covering:

* **change provenance** — the file map (what changed, why, requirement link,
  risks, how it will be verified),
* **instruction provenance** — only persistent AI instructions this change
  relied on or modified,
* **a pointer to agent execution evidence** when an agent ran.

Artifact: [change-map.md](../templates/change-map.md)

## 6. Automated and Human Verification

Verify using evidence and measures. These are **not** all verification
*results*:

* correctness evidence (static and functional),
* security evidence,
* regression evidence,
* operational evidence (parent heading; includes performance evidence and
  **operational cost** — post-merge runtime / infrastructure cost),
* verification cost (lifecycle **process measure**, not evidence that the
  change is correct).

**Operational evidence:** for performance-sensitive changes, record only the
metrics relevant to the change (CPU, memory, queries, allocations, latency,
external API calls, infrastructure cost). Passing functional tests does not
prove that generated code is operationally efficient. N/A is acceptable when
performance, cost, or capacity is not in scope.

**Verification cost** is the **pre-merge** effort and resource cost required to
establish sufficient confidence in a change. AI-assisted productivity must be
evaluated across the full change lifecycle, not only at the point of code
generation. A change is not necessarily more productive if faster generation
creates disproportionate review, verification, or operational cost. Depth
scales by [risk level](./risk-levels.md); Low-risk work is not required to fill
every field. Optional proxies include reviewer iterations, review comments,
time to merge (may include queue time), test execution cost, static-analysis
finding *count* or resolution effort (the findings themselves are verification
results), human review effort, and unresolved verification uncertainty.

**Key principle:** AI-generated tests are inputs, not final results.

Artifact: [verification-report.md](../templates/verification-report.md)

## Agent execution evidence (cross-stage)

Not a workflow stage. Not a verification result. Not a sixth required artifact.

Agent execution evidence is produced during agent execution and referenced by
both the Change Map (pointer) and the Verification Report (detail). It records
what executed the change and serves as **input** to verification and
accountability (Traceable, Accountable). Canonical rollback owner lives in
Verification Report → Approval; this record uses **accountable owner**.

Do not record secrets, tokens, credentials, private keys, or sensitive payload
contents. Record identifiers or references instead.

Depth:

* **Low** (if an agent ran): initiating human, agent/model, accountable owner.
* **Medium:** add tools or persistent instructions when relevant.
* **High / Critical:** full set when the agent accessed elevated permissions,
  MCP servers, external systems, production systems, or sensitive data.

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
work, assumptions cannot be verified, or unresolved blocking ambiguity remains
(not clarified and not explicitly accepted as residual risk).
