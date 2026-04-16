<!-- CEET Source:
  Raw Responses: Q12, Q13, Q60, Q62
  Directives: testing.*, git_workflow.*, tooling.mocking_vs_staging
-->

# Test Writer Skill — {engineer_name}

> Writes tests exactly as {engineer_name} would. Their sequence, their priority, their coverage expectations, their mocking stance.

## TDD Reality

{directives.testing.tdd_reality}

Follow this sequence when writing tests. Do not impose ideal TDD if the engineer does not practice it.

## Test Priority

{directives.testing.test_priority_rationale}

When time is limited, write THIS type of test first.

## Coverage Expectations

{directives.testing.coverage_expectations}

## Mocking Philosophy

### Test Doubles
{directives.testing.mocking_philosophy}

### Local Development
{directives.tooling.mocking_vs_staging}

## Test File Organization

Follow {engineer_name}'s file organization rules:
{directives.coding_style.file_organization_rules}

## Naming Conventions in Tests

Follow {engineer_name}'s naming rules:
{directives.coding_style.naming_rules}

## Generation Protocol

When writing tests:
1. Follow the TDD reality sequence above — not textbook TDD
2. Prioritize the test type specified above
3. Use mocking/staging approach specified above
4. Name test files and functions using the naming rules above
5. Include assertions that {engineer_name} would consider meaningful based on their coverage expectations
