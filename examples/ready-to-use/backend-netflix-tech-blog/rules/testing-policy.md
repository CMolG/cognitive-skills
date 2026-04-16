> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: testing.*, infrastructure.ideal_pipeline -->

# Global Rule: Testing Policy — Netflix Tech Blog

> Netflix Tech Blog's testing policy applied to all test generation and review. No exceptions unless Netflix Tech Blog's own decision framework permits one.


## TDD Approach

Use TDD where logic is complex or risk is high. For infra-heavy changes, rely on layered tests plus staged production verification.

## Test Priority

Prioritize tests that guard invariants, migration safety, retry/idempotency semantics, and incident-prone paths.

## Coverage Expectations

Coverage is a signal, not a target. Demand high confidence on critical paths and failure modes.

## Mocking Philosophy

Mock at external boundaries; avoid mocking internal behavior that should be validated end-to-end.

## Pipeline Integration

Automated lint/test/build/security checks, immutable artifacts, staged deploys, and post-deploy health gates.

## Enforcement

These rules are non-negotiable within Netflix Tech Blog's AI environment. Every agent, skill, and command inherits them. Violations must be flagged with a reference to the specific rule above.