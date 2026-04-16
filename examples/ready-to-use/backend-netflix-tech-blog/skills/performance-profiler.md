> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: performance.*
-->

# Performance Profiler Skill — Netflix Tech Blog

> Profiles and optimizes performance using Netflix Tech Blog's exact thresholds and methodology.


## Latency Standards

Define and enforce SLO-aligned latency budgets for p50/p95/p99 on critical endpoints.

## Memory Leak Playbook

Use heap profiling under realistic load, compare snapshots, and isolate retention growth to ownership boundaries.

## Caching Rules

Cache with explicit invalidation and staleness policy. Never hide consistency assumptions.

## N+1 Prevention

Detect and prevent fan-out query amplification through query planning, batching, and prefetch strategies.

## GC Philosophy

Tune allocation patterns first, then runtime settings. Reduce object churn on hot paths.

## Frontend Render Rules

Backend perspective: shape APIs for predictable client render workloads and efficient pagination/streaming.

## Enforcement Protocol

When applying these rules:
1. Quote the specific rule being applied
2. Show the exact fix using Netflix Tech Blog's conventions
3. If two rules conflict, reference Prefer decisions that reduce blast radius, are observable in production, and are reversible under pressure. If two options look similar, pick the one that is easier to test and rollback. to resolve
4. Never cite "best practices" or "industry standard" — cite the rule above