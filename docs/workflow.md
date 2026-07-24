# VAD Workflow

VAD defines seven primary stages.

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

## 5. Change Mapping

Produce a change map: what changed, why, requirement link, risks, and how it
was verified.

Artifact: [change-map.md](../templates/change-map.md)

## 6. Automated and Human Verification

Verify in layers:

* static (compile, lint, secrets, unsafe APIs),
* functional (behavior, permissions, boundaries),
* regression (related flows still work),
* operational (logs, monitors, rollback readiness).

**Key principle:** AI-generated tests are inputs, not final results.

Artifact: [verification-report.md](../templates/verification-report.md)

## 7. Progressive Deployment

Passing tests is not production safety. Roll out by risk:

```text
Local → Development → Internal users → Limited production → Broader release
```

**Key question:** Can this change be stopped or reversed before it affects every user?

## Completion criteria

A responsible developer should be able to explain purpose, scope, impact,
failure modes, evidence, recovery, and ownership. See [README.md](../README.md).
