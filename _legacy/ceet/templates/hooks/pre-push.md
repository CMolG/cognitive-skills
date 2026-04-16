<!-- CEET Source:
  Raw Responses: Q12, Q13, Q31, Q35, Q37
  Directives: testing.*, security.*, performance.latency_standards
-->

# Pre-Push Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-push gates.

## Test Requirements

{directives.testing.tdd_reality}

{directives.testing.coverage_expectations}

Run the test suite. The minimum passing criteria is defined by the coverage expectations above.

## Security Scan

{directives.security.cve_response_plan}

{directives.security.web_security_defaults}

Run security scanning. Handle CVE findings per the CVE response plan above.

## Performance Check

{directives.performance.latency_standards}

If performance tests exist, verify endpoints meet the latency thresholds specified above.

## Push Gate

All checks above must pass before pushing. If a check fails:
1. Report which specific rule was violated
2. Reference the directive that defines the rule
3. Show the fix if possible
