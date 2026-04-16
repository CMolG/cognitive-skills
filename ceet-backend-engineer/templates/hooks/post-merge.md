<!-- CEET Source:
  Role: backend-engineer
  Directives: debugging.dependency_resolution, infrastructure.ideal_pipeline
-->

# post-merge Hook — {engineer_name}

> Enforces {engineer_name}'s exact post-merge standards.

## Trigger

After every merge


## Dependency Check

{directives.debugging.dependency_resolution}

After merge, verify all dependencies are consistent.

## Pipeline Verification

{directives.infrastructure.ideal_pipeline}

Verify the pipeline is executing as expected.

## Post-Merge Actions

1. Run dependency installation/lock file update
2. Check for new environment variables or secrets needed
3. Run smoke tests if available
4. Report any drift from the pipeline definition

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden