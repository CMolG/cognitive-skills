> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: debugging.*, infrastructure.*, resilience.* -->

# Global Rule: Operational Runbook — Netflix Tech Blog

> Netflix Tech Blog's operational standards for debugging, incidents, and infrastructure. No exceptions unless Netflix Tech Blog's own decision framework permits one.


## Silent Failure Protocol

Assume silent failures exist until disproven. Trace request lifecycles with correlation IDs and verify each hop.

## Logging Standards

Logs should explain state transitions and failure context, not just stack traces.

## Alert Classification

Page on user-impacting symptoms, ticket on predictive maintenance signals. Keep alerts actionable.

## Deployment Philosophy

Progressive delivery with canaries and fast rollback over all-at-once deployments.

## Resilience Patterns

- Idempotency: Design write paths and handlers to be idempotent by key and operation semantics.
- Retry: Use bounded retries with jitter and deadline awareness; avoid retry storms.
- DLQ: Dead-letter with context-rich payloads, triage runbooks, and replay safety checks.
- Graceful Degradation: Prefer partial functionality over hard outages where correctness can be preserved.

## Escalation Protocol

Escalate early on unresolved invariants, customer-impacting risk, and unclear ownership under incident pressure.

## Enforcement

These rules are non-negotiable within Netflix Tech Blog's AI environment. Every agent, skill, and command inherits them. Violations must be flagged with a reference to the specific rule above.