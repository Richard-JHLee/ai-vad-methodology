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

v0.2 does not add new stages or principles. It makes AI-assisted changes more inspectable by extending the evidence required across the existing lifecycle. It thickens three existing properties. See [RFC 0002](./rfcs/0002-vad-v0.2-evidence-model.md).

* **Traceable** — change provenance, instruction provenance, agent execution evidence.
* **Verifiable** — correctness, security, regression, operational evidence (including performance and operational cost), verification cost as a process measure.
* **Accountable** — human approval, execution ownership, rollback ownership.
