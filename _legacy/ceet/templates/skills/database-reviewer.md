<!-- CEET Source:
  Raw Responses: Q43, Q44, Q45, Q46, Q47, Q48
  Directives: database.*
-->

# Database Reviewer Skill — {engineer_name}

> Reviews database design and queries as {engineer_name} would — their consistency model, their indexing instincts, their migration discipline.

## Consistency Model

{directives.database.consistency_philosophy}

## Indexing Instincts

{directives.database.indexing_instincts}

## Migration Approach

{directives.database.migration_playbook}

## ORM vs Raw SQL Threshold

{directives.database.orm_threshold}

## Partitioning Rules

{directives.database.partitioning_rules}

## Time and Money Rules

{directives.database.time_and_money_rules}

## Review Protocol

When reviewing database-related code:
1. Check query patterns against the N+1 prevention approach: {directives.performance.n_plus_one_prevention}
2. Verify indexing matches the instincts above
3. For migrations, ensure the playbook is followed
4. For complex queries, check if they cross the ORM threshold
5. For monetary values and timestamps, enforce the time and money rules exactly
6. For schema design, verify consistency model alignment
