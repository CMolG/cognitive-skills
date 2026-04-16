> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: architecture.*, database.*, resilience.* -->

# Global Rule: Architecture Principles — Netflix Tech Blog

> Netflix Tech Blog's architectural principles applied when designing, reviewing, or discussing systems. No exceptions unless Netflix Tech Blog's own decision framework permits one.


## Persistence Default

Make data invariants explicit in storage and contracts. Design for eventual correction when distributed writes diverge.

## Decomposition

Decompose along ownership and failure isolation boundaries. Service boundaries should reduce—not multiply—coordination cost.

## State Management

Treat state transitions as first-class. Validate transitions, ensure idempotency, and emit audit-friendly events.

## Build vs Buy

Buy when capability is commodity and integration risk is acceptable. Build when reliability/performance constraints are core differentiators.

## Concurrency

Prefer bounded concurrency with backpressure. Explicitly define queueing, timeout, and cancellation behavior.

## Database Principles

- Consistency: Choose consistency model intentionally per domain invariant. Document where eventual consistency is acceptable.
- Indexing: Design indexes from real access patterns and cardinality, then validate with production-like traces.
- Time and Money: Optimize for operator time first on critical systems; optimize infra cost where safe and measurable.

## Resilience Principles

- Idempotency: Design write paths and handlers to be idempotent by key and operation semantics.
- Retry: Use bounded retries with jitter and deadline awareness; avoid retry storms.
- Graceful Degradation: Prefer partial functionality over hard outages where correctness can be preserved.

## Enforcement

These rules are non-negotiable within Netflix Tech Blog's AI environment. Every agent, skill, and command inherits them. Violations must be flagged with a reference to the specific rule above.