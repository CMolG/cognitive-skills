<!-- CEET Source:
  Raw Responses: Q19, Q20, Q49
  Directives: debugging.dependency_resolution, infrastructure.ideal_pipeline
-->

# Post-Merge Hook — {engineer_name}

> Runs {engineer_name}'s exact post-merge verification.

## Dependency Check

{directives.debugging.dependency_resolution}

After merge, verify all dependencies are consistent. If conflicts are detected, apply the resolution approach above.

## Pipeline Verification

{directives.infrastructure.ideal_pipeline}

Verify the pipeline is executing as expected per the ideal pipeline definition above.

## Post-Merge Actions

1. Run dependency installation/lock file update
2. Check for new environment variables or secrets needed
3. Run smoke tests if available
4. Report any drift from the pipeline definition
