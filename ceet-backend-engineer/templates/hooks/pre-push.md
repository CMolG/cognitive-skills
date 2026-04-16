<!-- CEET Source:
  Role: backend-engineer
  Directives: testing.*, security.*, performance.latency_standards
-->

# pre-push Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-push standards.

## Trigger

Before every push


## Test Requirements

{directives.testing.tdd_reality}

{directives.testing.coverage_expectations}

Run the test suite. Minimum passing criteria defined by coverage expectations above.

## Security Scan

{directives.security.cve_response_plan}

{directives.security.web_security_defaults}

Run security scanning. Handle CVE findings per the CVE response plan above.

## Performance Check

{directives.performance.latency_standards}

If performance tests exist, verify endpoints meet the latency thresholds specified above.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden