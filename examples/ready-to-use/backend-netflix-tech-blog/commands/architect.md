> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: architecture.*, database.*, resilience.* -->

# /architect Command — Netflix Tech Blog

> Designs system architecture.

## Usage
/architect [args]

## Behavior

1. Default persistence: Make data invariants explicit in storage and contracts. Design for eventual correction when distributed writes diverge.
2. Decomposition: Decompose along ownership and failure isolation boundaries. Service boundaries should reduce—not multiply—coordination cost.
3. State management: Treat state transitions as first-class. Validate transitions, ensure idempotency, and emit audit-friendly events.
4. Build vs buy: Buy when capability is commodity and integration risk is acceptable. Build when reliability/performance constraints are core differentiators.
5. Concurrency: Prefer bounded concurrency with backpressure. Explicitly define queueing, timeout, and cancellation behavior.
6. Database: consistency, indexing, partitioning per my directives
7. Resilience patterns: idempotency, retry, DLQ, graceful degradation per my directives
8. Apply my decision framework: Prefer decisions that reduce blast radius, are observable in production, and are reversible under pressure. If two options look similar, pick the one that is easier to test and rollback.