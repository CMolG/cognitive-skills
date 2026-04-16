> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: testing.*, security.*, performance.latency_standards
-->

# pre-push Hook — Netflix Tech Blog

> Enforces Netflix Tech Blog's exact pre-push standards.

## Trigger

Before every push


## Test Requirements

Use TDD where logic is complex or risk is high. For infra-heavy changes, rely on layered tests plus staged production verification.

Coverage is a signal, not a target. Demand high confidence on critical paths and failure modes.

Run the test suite. Minimum passing criteria defined by coverage expectations above.

## Security Scan

Triage by exploitability and exposure, prioritize internet-facing/runtime paths, and patch with rollback-ready deployment plans.

Default to secure headers, strict input handling, and least-privilege service communication.

Run security scanning. Handle CVE findings per the CVE response plan above.

## Performance Check

Define and enforce SLO-aligned latency budgets for p50/p95/p99 on critical endpoints.

If performance tests exist, verify endpoints meet the latency thresholds specified above.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden