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

## v0.2 evidence terms (proposed)

These do not add a seventh core property. See
[RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).

| Term | Meaning |
| ---- | ------- |
| **Requirement Ambiguity / Clarification** | Unclear, conflicting, or missing requirement detail, and the record of questions asked plus answers received before generation. |
| **Instruction Provenance** | The origin of the instruction that authorized a change (issue, human prompt, agent task, amended instruction) and who approved it. |
| **Agent Execution Evidence** | Trace of agent actions: tools, targets, results, and stop or error events. |
| **Verification Cost** | Effort, tools, and coverage spent on verification, judged against risk. |
| **Performance Evidence** | Measured performance outcome with baseline, after value, environment, and source—not a checkbox alone. |
