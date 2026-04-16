<!-- CEET Source:
  Role: devops-sre
  Directives: observability.*, slo_management.*
-->

# post-deploy Hook — {engineer_name}

> Enforces {engineer_name}'s exact post-deploy standards.

## Trigger

After every deployment


## Observability Verification

{directives.observability.instrumentation_first}

Verify dashboards and alerts are live.

## SLO Verification

{directives.slo_management.burn_rate_response}

Monitor burn rate for 15 minutes.

## Canary Health

Check canary metrics against baseline. Auto-rollback if SLO burn rate exceeds threshold.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden