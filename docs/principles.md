# VAD Core Principles

See also the overview in [README.md](../README.md).

VAD is organized around one completion rule:

> A software change is not complete until a developer can explain its purpose,
> impact, failure points, verification evidence, and recovery plan.

## Ten principles

1. **Analyze before generating code.**  
   Understand the existing system before asking AI to modify it.

2. **Limit the scope of each change.**  
   Prefer one concern per change. If you cannot explain it clearly, split it.

3. **Separate feature work from unrelated refactoring.**  
   Do not hide cleanup, dependency upgrades, or formatting in the same change.

4. **Record the reason for every meaningful change.**  
   Link code edits to requirements, decisions, and risks.

5. **Treat AI output as untrusted until verified.**  
   Generation is not validation.

6. **Do not allow AI to be the only reviewer of AI-generated code.**  
   Human ownership of approval remains mandatory.

7. **Include operational and recovery requirements.**  
   Logging, monitoring, rollback, and incident response are part of the change.

8. **Deploy high-risk changes progressively.**  
   Local → development → limited users → broader rollout.

9. **Keep final approval under human responsibility.**  
   Tools assist; people approve.

10. **Prefer explainable changes over large opaque changes.**  
    Speed without explainability increases long-term risk.

## What these principles are not

They are not a ban on AI agents, a replacement for Agile/DevOps/TDD, or a claim
that following VAD makes code safe by itself. They complement existing
engineering practice when AI accelerates change volume.

v0.2 does not add new stages or principles. It makes AI-assisted changes more
inspectable by extending the evidence required across the existing lifecycle.
Evidence fields attach to existing stages: requirement ambiguity,
instruction provenance, verification cost (a process measure), and
operational evidence (parent heading for performance and operational cost).
Agent execution evidence is cross-stage (referenced by the Change Map and
Verification Report); it is not a verification result and not an eighth
stage. None of this adds a seventh core property or an eleventh principle. See
[RFC 0002](../rfcs/0002-vad-v0.2-evidence-model.md).
