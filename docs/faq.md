# FAQ

## Is VAD a standard?

No. VAD is an early open proposal (draft v0.1). It is not an international,
academic, or certified framework.

## Does VAD ban AI agents?

No. VAD assumes AI will be used and focuses on keeping changes explainable and
recoverable.

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
