# RFC 0001: VAD Core

* **Status:** Draft
* **Version:** 0.1
* **Created:** 2026-07-24
* **License:** [CC-BY-4.0](../LICENSE)

## Summary

Define the core of **Verifiable AI Development (VAD)**: a seven-stage workflow,
five required artifact types (scaled by risk), and ten principles so that
AI-assisted software changes remain understandable, traceable, verifiable,
limited, recoverable, and accountable.

## Motivation

AI can generate code faster than humans can analyze it. The dominant risk is
not that AI fails to produce working code, but that teams lose the ability to
explain purpose, impact, failure modes, verification, and recovery.

Existing practices (Agile, DevOps, TDD) remain valuable but do not by themselves
constrain AI-accelerated change. VAD proposes explicit controls for that gap.

## Proposal

### Completion rule

A change is complete only when a responsible human can explain:

1. Purpose  
2. Scope  
3. Impact  
4. Failure modes  
5. Verification evidence  
6. Recovery / rollback  
7. Ownership  

### Workflow

1. Requirement Definition  
2. System Analysis  
3. Change Scope Limitation  
4. Controlled Code Generation  
5. Change Mapping  
6. Automated and Human Verification  
7. Progressive Deployment  

Details: [docs/workflow.md](../docs/workflow.md)

### Artifacts

| Artifact | Template |
| -------- | -------- |
| Requirement contract | [templates/requirement-contract.md](../templates/requirement-contract.md) |
| System map | [templates/system-map.md](../templates/system-map.md) |
| Change map | [templates/change-map.md](../templates/change-map.md) |
| ADR | [templates/adr-template.md](../templates/adr-template.md) |
| Verification report | [templates/verification-report.md](../templates/verification-report.md) |

Depth scales by [risk level](../docs/risk-levels.md).

### Principles

See [docs/principles.md](../docs/principles.md).

## Non-goals

* Replacing Agile, DevOps, or TDD  
* Guaranteeing AI-generated code is safe  
* Banning autonomous agents  
* Claiming VAD is an industry standard  

## Open questions

Tracked in [README.md — Open Questions](../README.md#open-questions).

## Alternatives considered

* **No process change** — relies only on existing PR review; insufficient when
  generation volume exceeds review capacity.  
* **Full manual coding only** — rejects AI productivity; out of scope.  
* **AI-only review loops** — conflicts with human accountability principle.

## Adoption guidance

Start with Medium+ risk changes, require change maps in PRs, and add progressive
rollout for High/Critical paths. Collect counterexamples and revise this RFC.

## References

* [README.md](../README.md)  
* [README.ko.md](../README.ko.md)  
* [RFC 0002: VAD v0.2 Evidence Model](./0002-vad-v0.2-evidence-model.md) — additive
  evidence fields; the six core properties, seven stages, and five required
  artifacts in this RFC are unchanged.
