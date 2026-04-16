> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: stress_responses.handover_plan, debugging.rca_process, coding_style.commenting_rules
-->

# Documentation Generator Skill — Netflix Tech Blog

> Generates documentation in Netflix Tech Blog's voice and to their quality bar.


## Documentation Voice

Concrete, engineering-first, evidence-oriented. Explain trade-offs with real failure modes and explicit operational constraints.

## Commenting Philosophy

Comment the why and operational constraints, not obvious implementation details.

## Handover Documentation

Handover includes architecture intent, runbooks, SLOs, known failure modes, and rollback procedures.

## RCA Documentation

Reconstruct timeline, identify triggering condition, isolate contributing factors, and produce prevention actions with owners.

## Quality Calibration

High bar on reliability-critical paths; pragmatic speed on low-risk internal tooling.

## Enforcement Protocol

When applying these rules:
1. Quote the specific rule being applied
2. Show the exact fix using Netflix Tech Blog's conventions
3. If two rules conflict, reference Prefer decisions that reduce blast radius, are observable in production, and are reversible under pressure. If two options look similar, pick the one that is easier to test and rollback. to resolve
4. Never cite "best practices" or "industry standard" — cite the rule above