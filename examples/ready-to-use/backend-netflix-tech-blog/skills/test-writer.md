> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: testing.*, tooling.mocking_vs_staging
-->

# Test Writer Skill — Netflix Tech Blog

> Writes tests exactly as Netflix Tech Blog would — their sequence, priority, coverage expectations, mocking stance.


## TDD Reality

Use TDD where logic is complex or risk is high. For infra-heavy changes, rely on layered tests plus staged production verification.

## Test Priority

Prioritize tests that guard invariants, migration safety, retry/idempotency semantics, and incident-prone paths.

## Coverage Expectations

Coverage is a signal, not a target. Demand high confidence on critical paths and failure modes.

## Mocking Philosophy

Mock at external boundaries; avoid mocking internal behavior that should be validated end-to-end.

## Local Development

Use mocks for fast unit feedback; use staging/prod-like validation for integration and resilience confidence.

## Enforcement Protocol

When applying these rules:
1. Quote the specific rule being applied
2. Show the exact fix using Netflix Tech Blog's conventions
3. If two rules conflict, reference Prefer decisions that reduce blast radius, are observable in production, and are reversible under pressure. If two options look similar, pick the one that is easier to test and rollback. to resolve
4. Never cite "best practices" or "industry standard" — cite the rule above