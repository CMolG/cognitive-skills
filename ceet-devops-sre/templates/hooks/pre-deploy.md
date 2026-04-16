<!-- CEET Source:
  Role: devops-sre
  Directives: change_management.*, slo_management.*
-->

# pre-deploy Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-deploy standards.

## Trigger

Before every deployment


## Deployment Strategy

{directives.change_management.deployment_default}

{directives.change_management.canary_rules}

## SLO Check

{directives.slo_management.error_budget_policy}

Verify error budget allows this deployment.

## Rollback Plan

{directives.change_management.rollback_philosophy}

Confirm rollback path exists.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden