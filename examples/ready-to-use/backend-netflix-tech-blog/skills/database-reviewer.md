> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: database.*
-->

# Database Reviewer Skill — Netflix Tech Blog

> Reviews database decisions as Netflix Tech Blog would — their consistency instincts, indexing rules, migration approach.


## Consistency Model

Choose consistency model intentionally per domain invariant. Document where eventual consistency is acceptable.

## Indexing Instincts

Design indexes from real access patterns and cardinality, then validate with production-like traces.

## Migration Approach

Migrate with expand/contract phases, dual-writes when needed, and verified rollback points.

## ORM vs Raw SQL Threshold

Use ORM for standard CRUD productivity; drop to SQL for complex access patterns and performance-sensitive paths.

## Partitioning Rules

Partition by stable keys aligned to access paths and operational growth boundaries.

## Time and Money Rules

Optimize for operator time first on critical systems; optimize infra cost where safe and measurable.

## Enforcement Protocol

When applying these rules:
1. Quote the specific rule being applied
2. Show the exact fix using Netflix Tech Blog's conventions
3. If two rules conflict, reference Prefer decisions that reduce blast radius, are observable in production, and are reversible under pressure. If two options look similar, pick the one that is easier to test and rollback. to resolve
4. Never cite "best practices" or "industry standard" — cite the rule above