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
| **Verifiable** | Correctness, security, regression, operational evidence (including performance and operational cost), and verification cost as a process measure. |
| **Accountable** | Human approval, execution ownership, and rollback ownership. |

## v0.2 evidence terms (proposed)

| Term | Meaning |
| ---- | ------- |
| **Blocking ambiguity** | An unresolved requirement uncertainty that could materially change implementation scope, acceptance criteria, security or privacy behavior, data handling, permissions or authorization, externally observable behavior, or rollback or operational risk. Non-blocking ambiguity may be recorded as an accepted assumption. Unresolved blocking ambiguity is a stop condition unless clarified or explicitly accepted as residual risk. |
| **Requirement Ambiguity / Clarification** | Known ambiguities, missing information, assumptions, questions for humans, and implicit requirements captured inside Stage 1 (ending at Acceptance Criteria) before generation. |
| **Instruction Provenance** | Record for a **persistent** AI instruction (`AGENTS.md`, `CLAUDE.md`, repository instruction, persistent system prompt, persistent agent rule): the rule, why it exists, the failure or risk it prevents, when it was introduced, its scope, and when it may be removed. Record per change only when this work **relied on or modified** such an instruction. Temporary conversational prompts are out of scope. Do not copy every existing instruction file simply because it exists. |
| **Agent Execution Evidence** | Cross-stage record of what executed the change. Produced during agent execution. Referenced by the Change Map (pointer) and the Verification Report (detail). Input to verification and accountability. **Not** a verification result, **not** an eighth workflow stage, **not** a sixth required artifact. Depth scales by risk. Canonical rollback owner lives in Verification Report → Approval; this record uses accountable owner. |
| **Verification Cost** | The **pre-merge** effort and resource cost required to establish sufficient confidence in a change. A lifecycle **process measure**, not evidence that the change is correct. Optional proxies may include reviewer iterations, review comments, time to merge (may include queue time), test execution cost, static-analysis finding count / resolution effort, human review effort, and unresolved verification uncertainty. Not mandatory field-by-field on Low-risk work. |
| **Operational Cost** | **Post-merge** runtime / infrastructure cost caused by the change. Lives under Operational Evidence, not as a separate verification result. |
| **Operational Evidence** | Parent heading for measured runtime and operational-cost impact. Performance Evidence may include CPU, memory, queries, allocations, latency, external API calls, and infrastructure cost. Record only metrics relevant to the change. Not a checkbox alone. |
