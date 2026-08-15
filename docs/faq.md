# FAQ

## Is VAD a standard?

No. VAD is an early open proposal (draft v0.1). It is not an international,
academic, or certified framework.

## Does VAD ban AI agents?

No. VAD assumes AI will be used and focuses on keeping changes explainable and
recoverable. When an agent executes a change, keep agent execution evidence
scaled by [risk level](./risk-levels.md) (what ran, tools, MCP servers,
permissions, approvals, cost, ownership as applicable). That record is
cross-stage execution evidence, not a verification result. See
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

A **blocking ambiguity** is an unresolved requirement uncertainty that could
materially change implementation scope, acceptance criteria, security or privacy
behavior, data handling, permissions or authorization, externally observable
behavior, or rollback or operational risk. Non-blocking ambiguity may be
recorded as an accepted assumption.

Unresolved blocking ambiguity is a stop condition. Code generation must not
proceed until the ambiguity is either (1) clarified, or (2) explicitly accepted
by the responsible human as residual risk.

Inside Stage 1 (ending at Acceptance Criteria, not Implementation), detect
ambiguity, clarify, then write acceptance criteria. Do not fill every ambiguity
field merely because AI assistance was used.

## Does more verification always mean better VAD?

No. **Verification Cost** is the pre-merge effort required to establish
sufficient confidence—a process measure, not proof of correctness. Record it
against risk across the full change lifecycle, not only generation speed. Large
effort on low-risk work is waste; thin evidence on high-risk work is the
defect. Low-risk changes are not required to fill every verification-cost
field.

**Operational cost** is post-merge runtime / infrastructure cost and belongs
under Operational Evidence.

## Is a performance checkbox enough?

No. When performance, cost, or capacity is in scope, complete **Operational
Evidence**. Performance Evidence may include CPU, memory, queries, allocations,
latency, external API calls, and infrastructure cost. Record only the metrics
relevant to the change.

## Are AGENTS.md or CLAUDE.md rules part of VAD?

Persistent AI instructions (`AGENTS.md`, `CLAUDE.md`, repository instructions,
persistent system prompts, persistent agent rules) should carry instruction
provenance when this change **relied on or modified** them: why the rule
exists, what failure it prevents, scope, and when it may be removed. Temporary
conversational prompts are out of scope. Do not copy every existing instruction
file simply because it exists. Treat persistent instructions as maintainable
software artifacts, not permanent accumulated memory.

## May VAD artifacts include secrets?

No. Do not record secrets, tokens, credentials, private keys, or sensitive
payload contents. Record identifiers or references instead.
