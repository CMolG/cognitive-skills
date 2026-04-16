<!-- CEET Source:
  Role: frontend-engineer
  Directives: testing.*, performance.*, accessibility.*
-->

# pre-push Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-push standards.

## Trigger

Before every push


## Test Suite

{directives.testing.unit_component_e2e_mix}

{directives.testing.coverage_expectations}

## a11y Scan

{directives.accessibility.testing_approach}

## Performance Budget

{directives.performance.web_vitals_priority}

{directives.performance.bundle_strategy}

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden