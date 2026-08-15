# ai-vad-methodology
Verifiiable AI Development  

# VAD — Verifiable AI Development

> A proposed open methodology for building AI-assisted software that remains understandable, traceable, verifiable, and recoverable by humans.

[한국어 문서](./README.ko.md) · [Core RFC](./rfcs/0001-vad-core.md) · [RFC 0002 Evidence Model](./rfcs/0002-vad-v0.2-evidence-model.md) · [Contributing](./CONTRIBUTING.md)

---

## Why VAD?

AI can generate code faster than developers can analyze it.

This creates a new software development problem.

The primary risk is no longer that AI cannot produce working code. The greater risk is that AI can rapidly produce code that appears to work while developers gradually lose the ability to explain:

* why the change was made,
* which parts of the system are affected,
* where the change may fail,
* how the system can be restored,
* and who is responsible for approving the result.

Traditional software development practices remain important, but AI-assisted development changes the scale and speed of code generation.

VAD proposes a development process designed around one central requirement:

> A software change is not complete until a developer can explain its purpose, impact, failure points, verification evidence, and recovery plan.

---

## What is VAD?

**VAD** stands for **Verifiable AI Development**.

It is a proposed methodology for controlling, reviewing, and operating software changes created with the assistance of AI coding tools and autonomous agents.

VAD does not attempt to prevent developers from using AI.

Instead, it aims to ensure that AI-generated changes remain:

* **Understandable** — humans can explain the system behavior.
* **Traceable** — changes can be connected to requirements and decisions.
* **Verifiable** — claims are supported by evidence and testing.
* **Limited** — change scope remains reviewable.
* **Recoverable** — failures can be detected and reversed.
* **Accountable** — human responsibility remains clearly defined.

v0.2 does not add properties. It thickens three of them. See [RFC 0002](./rfcs/0002-vad-v0.2-evidence-model.md).

* **Traceable** — change provenance, instruction provenance, agent execution evidence.
* **Verifiable** — correctness, security, regression, performance evidence, operational cost, verification cost.
* **Accountable** — human approval, execution ownership, rollback ownership.

---

## Status

VAD is currently an early-stage proposal.

```text
Current status: Draft
Version: 0.1
```

VAD is not an internationally recognized standard, academic standard, or officially certified software development framework.

It is being developed as an open proposal through:

* community discussion,
* practical implementation,
* criticism and counterexamples,
* incident analysis,
* and contributions from software developers.

Disagreement is welcome.

The goal is not to prove that VAD is already correct. The goal is to determine which practices are genuinely useful for AI-assisted software development.

---

# The VAD Workflow

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

---

## 1. Requirement Definition

Before asking AI to generate code, define the expected behavior.

The requirement should describe:

* the purpose of the feature,
* expected inputs and outputs,
* user roles and permissions,
* failure conditions,
* data modification rules,
* security requirements,
* performance expectations,
* and recovery requirements.

### Key question

> What exactly should happen, and under which conditions should it fail?

AI can implement an incorrect requirement very efficiently. Therefore, requirement quality is one of the most important controls in AI-assisted development.

Inside this stage (not a new top-level stage):

```text
Requirement Definition
  → Ambiguity Detection
  → Requirement Clarification
  → Acceptance Criteria
  → Implementation
```

Unresolved ambiguity is a stop condition. Record known ambiguities, missing information, assumptions, questions requiring human clarification, and implicit requirements before generating code. See [RFC 0002](./rfcs/0002-vad-v0.2-evidence-model.md).

---

## 2. System Analysis

The existing system must be analyzed before code generation begins.

The analysis should identify:

* related files,
* entry points,
* API routes,
* function and service calls,
* data flow,
* database changes,
* external dependencies,
* authentication and authorization boundaries,
* background processes,
* and affected clients.

### Required output

The AI or developer should produce a concise system map before implementation.

```text
Request
  ↓
Controller
  ↓
Application Service
  ↓
Domain Logic
  ↓
Repository
  ↓
Database
  ↓
Response
```

### Key question

> Which parts of the system could be affected by this change?

---

## 3. Change Scope Limitation

AI-generated changes should remain small enough for a human to review and understand.

Recommended default constraints:

* one feature or concern per change,
* approximately three to five primary files when practical,
* no unrelated refactoring,
* no hidden dependency upgrades,
* no formatting of unrelated files,
* and no simultaneous architectural redesign unless explicitly approved.

These are guidelines, not absolute limits. Larger changes require stronger review evidence and clearer decomposition.

### Key principle

> If a change is too large to explain clearly, it is too large to approve safely.

---

## 4. Controlled Code Generation

AI may generate code only within the approved requirement and change scope.

Before implementation, the AI should state:

1. which files it plans to modify,
2. why each file must change,
3. which files it will not modify,
4. which assumptions it is making,
5. which risks it expects,
6. and which tests it plans to add.

The developer should review this plan before accepting the generated implementation.

### Example instruction

```text
Analyze the existing implementation before writing code.

Before making changes, provide:

1. the relevant execution flow,
2. the files that must change,
3. the reason for each change,
4. possible security and data risks,
5. the proposed tests,
6. and the rollback approach.

Do not modify unrelated files.
Do not combine refactoring with feature development.
Stop and explain if the requested scope must expand.
```

Persistent AI instructions such as `AGENTS.md`, `CLAUDE.md`, system prompts, and repository rules should record **instruction provenance**: the rule, why it exists, the failure or risk it prevents, when it was introduced, its scope, and when it may be removed. Treat these as maintainable software artifacts, not permanent accumulated memory. See [RFC 0002](./rfcs/0002-vad-v0.2-evidence-model.md).

If an agent executes the work, produce **agent execution evidence** while the agent runs. That record is cross-stage (Change Map pointer + Verification Report detail). It is not a verification result and not an eighth workflow stage.

---

## 5. Change Mapping

Every AI-assisted change should include a change map.

A change map explains what changed and how the changes are connected.

### Example

| File                         | Change                   | Reason                     | Risk                       |
| ---------------------------- | ------------------------ | -------------------------- | -------------------------- |
| `routes/api.php`             | Added subscription route | Expose new API             | Unauthorized access        |
| `SubscriptionController.php` | Added endpoint           | Handle request             | Validation failure         |
| `SubscriptionService.php`    | Added business logic     | Process subscription state | Incorrect state transition |
| `SubscriptionTest.php`       | Added tests              | Verify expected behavior   | Missing edge case          |

The change map should answer:

* What changed?
* Why did it change?
* Which requirement does it satisfy?
* What could break?
* How was it verified?

Stage 5 also records **change provenance**, **instruction provenance**, and a **pointer to agent execution evidence** when an agent ran. Agent execution evidence itself is cross-stage; it is not a verification result.

---

## 6. Automated and Human Verification

AI-generated code should not be considered verified merely because AI generated tests for it.

VAD separates verification into multiple layers.

### 6.1 Static verification

Check:

* compilation,
* type safety,
* linting,
* dependency changes,
* unsafe APIs,
* secret exposure,
* and common security weaknesses.

### 6.2 Functional verification

Confirm:

* expected behavior,
* invalid input handling,
* permission rules,
* boundary conditions,
* and failure behavior.

### 6.3 Regression verification

Confirm that existing functionality still works.

Review:

* related APIs,
* existing user flows,
* database compatibility,
* older application versions,
* background jobs,
* and external integrations.

### 6.4 Operational verification

Confirm that the change can be safely operated.

Review:

* logging,
* monitoring,
* alerting,
* performance,
* external API usage,
* infrastructure cost,
* database migration safety,
* rollback readiness,
* and incident response procedures.

Stage 6 verification layers are:

* correctness,
* security,
* regression,
* performance evidence,
* operational cost,
* verification cost.

### Performance Evidence

For performance-sensitive changes, verification should consider measurable runtime impact.

Examples:

* CPU usage,
* memory usage,
* database queries,
* allocations,
* latency,
* external API calls,
* infrastructure cost.

Passing functional tests does not prove that generated code is operationally efficient.

### Verification Cost

AI-assisted development should evaluate not only whether a change is correct, but also how expensive it is to verify.

AI-assisted productivity must be evaluated across the full change lifecycle, not only at the point of code generation.

A change is not necessarily more productive if faster generation creates disproportionate review, verification, or operational cost.

Faster generation is not an improvement if the saved generation cost is transferred into disproportionate verification cost.

Evidence may include reviewer iterations, review comments, time to merge, test execution cost, static-analysis findings, human review effort, and unresolved verification uncertainty. These are **not** mandatory measurements for every Low-risk change. Depth follows [risk levels](./docs/risk-levels.md).

Agent execution evidence is **not** a Stage 6 verification layer. It is cross-stage execution evidence: input to verification and accountability, referenced from the Change Map and detailed in the Verification Report.

### Key principle

> AI-generated explanations and tests are verification inputs, not verification results.

---

## 7. Progressive Deployment

Passing tests does not prove that a change is safe in production.

High-impact changes should be deployed progressively.

A typical deployment path may be:

```text
Local Development
        ↓
Development Environment
        ↓
Internal Users
        ↓
Small User Group
        ↓
Expanded Rollout
        ↓
Full Production
```

Recommended controls include:

* feature flags,
* canary releases,
* staged rollouts,
* migration backups,
* health metrics,
* error-rate thresholds,
* automatic rollback conditions,
* and clearly assigned owners.

### Key question

> Can this change be stopped or reversed before it affects every user?

---

# VAD Completion Criteria

A change should not be considered complete only because:

* the code compiles,
* automated tests pass,
* the AI reports success,
* or the feature appears to work once.

A VAD-compliant change should allow a responsible developer to explain:

1. **Purpose** — Why was this change made?
2. **Scope** — What was changed?
3. **Impact** — Which systems and users may be affected?
4. **Failure** — Where and how could it fail?
5. **Evidence** — How was it verified?
6. **Recovery** — How can it be disabled or rolled back?
7. **Ownership** — Who approved and operates it?

---

# Required VAD Artifacts

VAD proposes five core artifacts.

## 1. Requirement Contract

Defines:

* purpose,
* behavior,
* inputs and outputs,
* permissions,
* constraints,
* failure conditions,
* acceptance criteria,
* and recovery expectations.

Template:

```text
templates/requirement-contract.md
```

## 2. System Map

Documents:

* components,
* execution flow,
* data flow,
* external systems,
* and trust boundaries.

Template:

```text
templates/system-map.md
```

## 3. Change Map

Documents:

* changed files,
* reasons,
* dependencies,
* risks,
* tests,
* and operational impact.

Template:

```text
templates/change-map.md
```

## 4. Architecture Decision Record

Records:

* the decision,
* context,
* alternatives,
* consequences,
* and rejected approaches.

Template:

```text
templates/adr-template.md
```

## 5. Verification Report

Records:

* verification methods,
* test results,
* known limitations,
* remaining risks,
* deployment conditions,
* and rollback readiness.

Template:

```text
templates/verification-report.md
```

---

# Risk-Based Application

Not every change requires the same level of process.

VAD should be applied according to risk.

| Risk level | Example                                                              | Recommended controls                                                    |
| ---------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| Low        | Text change, isolated UI adjustment                                  | Change map and basic test                                               |
| Medium     | New API, business-rule update                                        | Requirement contract, tests, impact analysis                            |
| High       | Authentication, payment, subscription, migration                     | Full VAD artifacts, security review, progressive rollout                |
| Critical   | Financial data, medical data, infrastructure, irreversible migration | Independent review, recovery exercise, monitoring and explicit approval |

The purpose of VAD is not to create unnecessary documentation.

The purpose is to increase control in proportion to potential damage.

---

# VAD Core Principles

1. **Analyze before generating code.**
2. **Limit the scope of each change.**
3. **Separate feature development from unrelated refactoring.**
4. **Record the reason for every meaningful change.**
5. **Treat AI output as untrusted until verified.**
6. **Do not allow AI to be the only reviewer of AI-generated code.**
7. **Include operational and recovery requirements.**
8. **Deploy high-risk changes progressively.**
9. **Keep final approval under human responsibility.**
10. **Prefer explainable changes over large opaque changes.**

---

# What VAD Is Not

VAD is not:

* a replacement for Agile,
* a replacement for DevOps,
* a replacement for test-driven development,
* a guarantee that AI-generated code is safe,
* a requirement to manually inspect every character,
* a ban on autonomous agents,
* or a completed industry standard.

VAD is intended to complement existing software engineering practices by introducing stronger controls for AI-generated change.

---

# Open Questions

VAD is intentionally open to debate.

The following questions require practical evidence and community discussion.

## Understanding and approval

* Should developers deploy AI-generated code they do not fully understand?
* How well should developers understand a change before approving it?
* Is understanding the architecture sufficient, or must every code path be reviewed?

## Verification

* Can AI-generated tests be accepted as independent verification?
* Should another AI model review the generated implementation?
* Which verification tasks must always be performed by humans?

## Change scope

* Should AI-generated changes be limited by file count?
* Is a line-count limit more useful than a file-count limit?
* How should large architectural changes be decomposed?

## Responsibility

* Who is accountable when an autonomous coding agent causes an incident?
* Should AI-assisted pull requests identify a human owner?
* How should organizations record AI involvement?

## Process

* Does VAD introduce too much overhead for small teams?
* Which VAD artifacts are essential?
* Which parts should be automated?
* How should VAD integrate with existing CI/CD workflows?

---

# First Discussion

## Should developers deploy AI-generated code they do not fully understand?

AI can generate code faster than developers can analyze it.

As AI-assisted development becomes more common, one fundamental question emerges:

> How well should a developer understand AI-generated code before approving it for production?

Is passing automated tests enough?

Should developers understand every code path?

Is understanding the architecture, impact scope, failure points, and rollback process sufficient?

Where should we draw the line between trust and verification?

Real-world experiences, counterarguments, failed approaches, and practical recommendations are welcome.

---

# Suggested Repository Structure

```text
ai-vad-methodology/
├── README.md
├── README.ko.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
│
├── docs/
│   ├── principles.md
│   ├── workflow.md
│   ├── risk-levels.md
│   ├── terminology.md
│   └── faq.md
│
├── rfcs/
│   ├── README.md
│   ├── 0001-vad-core.md
│   └── 0002-vad-v0.2-evidence-model.md
│
├── templates/
│   ├── requirement-contract.md
│   ├── system-map.md
│   ├── change-map.md
│   ├── adr-template.md
│   └── verification-report.md
│
└── examples/
    ├── laravel/
    ├── swift/
    ├── android/
    └── python/
```

---

# Contributing

Contributions are welcome from:

* software developers,
* architects,
* security engineers,
* DevOps and SRE practitioners,
* QA engineers,
* AI tool builders,
* researchers,
* engineering managers,
* and organizations applying AI-assisted development.

Useful contributions include:

* criticism of the methodology,
* counterexamples,
* real incident reports,
* implementation cases,
* improved templates,
* translations,
* automation tools,
* workflow integrations,
* and proposals to remove unnecessary steps.

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before submitting an issue or pull request.

---

# Example Contribution Format

```markdown
## Project environment

- Language and framework:
- AI development tool:
- Team size:
- Project size:
- Risk level:

## Task assigned to AI

Describe the feature or change.

## Problem encountered

Describe what failed or became difficult to understand.

## VAD practices applied

List the VAD stages or artifacts used.

## Result

Describe the measurable outcome.

## Unnecessary or excessive steps

Explain which parts of VAD created little value.

## Proposed improvement

Suggest a specific change to the methodology.
```

---

# Roadmap

## Draft v0.1

* Define the initial principles
* Publish the seven-stage workflow
* Publish the five core templates
* Collect community feedback
* Identify overlaps with existing engineering practices

## Draft v0.2

* Add real-world implementation examples
* Introduce risk-level guidance
* Create pull request and issue templates
* Define minimum verification criteria
* Evidence model (proposed): verification cost, performance evidence, instruction provenance, agent execution evidence, requirement ambiguity/clarification — [RFC 0002](./rfcs/0002-vad-v0.2-evidence-model.md)

## Draft v0.3

* Add CI/CD integration examples
* Add agent-based development workflows
* Publish incident and recovery case studies
* Evaluate measurable adoption criteria

## Future consideration

* Community working group
* Formal RFC review process
* Reference implementations
* Tooling integrations
* Independent case studies

---

# Origin and Attribution

VAD originated from discussions about the loss of human understanding and control when AI generates software changes faster than developers can analyze them.

The initial proposal was organized by **Richard J. H. Lee** with assistance from ChatGPT.

VAD should be described as:

> A proposed open methodology for verifiable and traceable AI-assisted software development.

It should not be represented as an internationally approved or academically certified standard.

---

# License

The methodology, documentation, diagrams, and templates in this repository are licensed under the:

**Creative Commons Attribution 4.0 International License — CC BY 4.0**

You may:

* use,
* copy,
* modify,
* translate,
* redistribute,
* and adapt the materials,

including for commercial purposes, provided that appropriate attribution is given.

Example source code placed in designated source-code directories may be licensed separately under the MIT License.

Unless otherwise stated:

* Documentation and methodology: **CC BY 4.0**
* Example source code: **MIT License**

See the [LICENSE](./LICENSE) file for details.

---

# Citation

When referencing VAD, the following format is recommended:

```text
VAD — Verifiable AI Development
An open methodology proposed by Richard J. H. Lee
https://github.com/Richard-JHLee/ai-vad-methodology
```

---

# Final Principle

> AI can generate the code.
> Humans must retain the ability to understand, verify, operate, and recover the system.

---

## Join the Discussion

Open a Discussion or Issue if you:

* disagree with a VAD principle,
* believe a step is unnecessary,
* have experienced an AI-generated production incident,
* have a better verification approach,
* or want to contribute an implementation example.

VAD should evolve through evidence, criticism, and practical use—not through agreement alone.
