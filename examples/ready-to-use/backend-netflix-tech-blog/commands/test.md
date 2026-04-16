> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: testing.*, tooling.mocking_vs_staging -->

# /test Command — Netflix Tech Blog

> Writes tests.

## Usage
/test [args]

## Behavior

1. Follow my TDD reality: Use TDD where logic is complex or risk is high. For infra-heavy changes, rely on layered tests plus staged production verification.
2. Prioritize: Prioritize tests that guard invariants, migration safety, retry/idempotency semantics, and incident-prone paths.
3. Coverage bar: Coverage is a signal, not a target. Demand high confidence on critical paths and failure modes.
4. Mocking approach: Mock at external boundaries; avoid mocking internal behavior that should be validated end-to-end.
5. Local dev strategy: Use mocks for fast unit feedback; use staging/prod-like validation for integration and resilience confidence.