<!-- CEET Source:
  Role: frontend-engineer
  Directives: performance.bundle_strategy
-->

# post-merge Hook — {engineer_name}

> Enforces {engineer_name}'s exact post-merge standards.

## Trigger

After every merge


## Bundle Size Check

{directives.performance.bundle_strategy}

Verify bundle size has not regressed after merge.

## Visual Regression

{directives.testing.visual_regression}

Run visual regression tests if available.

## Dependency Update

Check for new dependencies, verify lock file consistency, run smoke tests.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden