# FAQ

## Is VAD a standard?

No. VAD is an early open proposal (draft v0.1). It is not an international,
academic, or certified framework.

## Does VAD ban AI agents?

No. VAD assumes AI will be used and focuses on keeping changes explainable and
recoverable. When an agent executes a change, keep agent execution evidence
(what ran, tools, MCP servers, permissions, approvals, cost, ownership). That
record is cross-stage execution evidence, not a verification result. See
[RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).

## Do I need every artifact for every PR?

No. Use [risk levels](./risk-levels.md). Low-risk changes may need only a short
change map and a basic test.

## Are AI-generated tests enough?

No. They are useful inputs. VAD still expects human judgment and appropriate
independent checks for the risk level.

## Must I understand every line before merge?

That is an [open question](../README.md#open-questions). At minimum, a responsible
developer should explain purpose, scope, impact, failure points, evidence, and
recovery. Teams should document their own bar.

## Does VAD replace Agile, DevOps, or TDD?

No. It complements them when AI increases change speed and volume.

## Where do I start on a real project?

1. Pick risk level.
2. Fill the matching templates under `templates/`.
3. Constrain the AI prompt to approved scope.
4. Require a change map and verification notes in the PR.
5. Roll out progressively for High/Critical changes.

## Can I adapt VAD for my company?

Yes, under [CC-BY-4.0](../LICENSE). Please attribute the project and note
modifications.

## What if the requirement is ambiguous?

Treat unresolved blocking ambiguity as a stop condition. Inside Stage 1,
detect ambiguity, clarify, then write acceptance criteria before generating
code. Record known ambiguities, missing information, assumptions, questions,
and implicit requirements in the Requirement Contract.

## Does more verification always mean better VAD?

No. Record verification cost against risk across the full change lifecycle,
not only generation speed. Large effort on low-risk work is waste; thin
evidence on high-risk work is the defect. Low-risk changes are not required
to fill every verification-cost field.

## Is a performance checkbox enough?

No. When performance is in scope, record performance evidence: CPU, memory,
queries, allocations, latency, external API calls, and infrastructure cost as
applicable.

## Are AGENTS.md or CLAUDE.md rules part of VAD?

Persistent AI instructions should carry instruction provenance: why the rule
exists, what failure it prevents, scope, and when it may be removed. Treat
them as maintainable software artifacts, not permanent accumulated memory.
