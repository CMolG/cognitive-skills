> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: database.migration_playbook, database.time_and_money_rules -->

# /migrate Command — Netflix Tech Blog

> Plans database migrations.

## Usage
/migrate [args]

## Behavior

1. Follow my migration playbook: Migrate with expand/contract phases, dual-writes when needed, and verified rollback points.
2. Apply my time and money rules: Optimize for operator time first on critical systems; optimize infra cost where safe and measurable.
3. Verify zero-downtime approach
4. Plan rollback strategy