# Terminology

| Term | Meaning |
| ---- | ------- |
| **VAD** | Verifiable AI Development — a proposed methodology for AI-assisted changes that remain understandable, traceable, verifiable, limited, recoverable, and accountable. |
| **Requirement contract** | Explicit statement of intended behavior, constraints, failures, and acceptance criteria before generation. |
| **System map** | Concise map of components, flows, data, and trust boundaries relevant to a change. |
| **Change map** | Table or narrative linking files/edits to reasons, risks, and verification. |
| **ADR** | Architecture Decision Record — why a design choice was made and what was rejected. |
| **Verification report** | Evidence of static, functional, regression, and operational checks, plus residual risk. |
| **Controlled generation** | AI coding constrained to an approved requirement and scope, with a reviewed plan. |
| **Progressive deployment** | Staged rollout that can be stopped or reversed before full exposure. |
| **Human approval** | Explicit ownership by a person accountable for merge/release decisions. |
| **Untrusted AI output** | Default stance: generated code and AI-written tests are inputs until independently verified. |
| **Risk level** | Low / Medium / High / Critical classification that scales required controls. |
| **RFC** | Request for Comments — a numbered proposal to evolve VAD itself. |

Ambiguous terms should be defined in the requirement contract for a given project
rather than assumed from AI chat history.

## v0.2 reading of existing properties

These are stronger definitions of three existing properties. They do not add a
seventh core property. See [RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).

| Property | v0.2 reading |
| -------- | ------------ |
| **Traceable** | Change provenance, instruction provenance, and agent execution evidence. |
| **Verifiable** | Correctness, security, regression, performance evidence, operational cost, and verification cost. |
| **Accountable** | Human approval, execution ownership, and rollback ownership. |

## v0.2 evidence terms (proposed)

| Term | Meaning |
| ---- | ------- |
| **Requirement Ambiguity / Clarification** | Known ambiguities, missing information, assumptions, questions for humans, and implicit requirements captured inside Stage 1 before generation. |
| **Instruction Provenance** | Record for a persistent AI instruction (`AGENTS.md`, `CLAUDE.md`, system prompt, repository rule): the rule, why it exists, the failure or risk it prevents, when it was introduced, its scope, and when it may be removed. Instructions are maintainable artifacts, not accumulated memory. |
| **Agent Execution Evidence** | Cross-stage record of what executed the change (human, agent/model, tools, MCP servers, permissions, artifacts, approvals, cost, ownership). Produced during agent execution. Referenced by the Change Map and the Verification Report. Input to verification and accountability. **Not** a verification result and **not** an eighth workflow stage. |
| **Verification Cost** | How expensive a change is to verify across the full lifecycle (review iterations, comments, time to merge, tests, static analysis, human effort, unresolved uncertainty), judged against risk. Not mandatory field-by-field on Low-risk work. |
| **Performance Evidence** | Measured runtime and operational-cost impact (CPU, memory, queries, allocations, latency, external API calls, infrastructure cost)—not a checkbox alone. |
