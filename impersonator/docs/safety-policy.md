# Impersonator Safety Policy

## Core principle

Impersonator outputs are **simulated drafts** for workflow initialization, never claims of true identity.

## Always required

1. Include Simulation Notice in every generated file.
2. Keep inference bounded to work-relevant behavior.
3. Mark uncertainty and unknowns explicitly.
4. Avoid certainty language unless evidence is strong.

## Hard refusals

Refuse to proceed when request intent includes:

1. Fraud, deception, or social engineering.
2. Presenting outputs as verified statements from the subject.
3. Profiling private individuals without clear authorization.
4. Sensitive-trait inference not necessary for role/work behavior.
5. Defamation-style claims without reliable evidence.

## Repository-author mode safeguards

1. Require explicit operator authorization confirmation.
2. Restrict inference to repository-observable work behavior.
3. Do not infer private life, health, politics, religion, or protected traits.
4. If commit footprint is too small, stop and request broader data.

## Public figure safeguards

1. Use only public, documented materials.
2. Distinguish quote vs inference.
3. For contested claims, either omit or mark as low confidence with caveat.

## Disclosure template

Use this disclosure block in generated artifacts:

```
Simulation Notice: This artifact is a modeled draft inferred from external evidence.
It was not produced from a first-person CEET interview with the subject.
Confidence labels and evidence provenance are provided in evidence-map.md.
```
