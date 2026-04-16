> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: debugging.dependency_resolution, infrastructure.ideal_pipeline
-->

# post-merge Hook — Netflix Tech Blog

> Enforces Netflix Tech Blog's exact post-merge standards.

## Trigger

After every merge


## Dependency Check

Pin and audit dependency changes. Prefer deterministic build inputs and explicit compatibility validation.

After merge, verify all dependencies are consistent.

## Pipeline Verification

Automated lint/test/build/security checks, immutable artifacts, staged deploys, and post-deploy health gates.

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