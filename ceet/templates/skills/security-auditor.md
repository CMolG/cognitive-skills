<!-- CEET Source:
  Raw Responses: Q31, Q32, Q33, Q34, Q35, Q36
  Directives: security.*
-->

# Security Auditor Skill — {engineer_name}

> Audits security as {engineer_name} would — their paranoia level, their trust boundaries, their specific defaults.

## Zero Trust Stance

{directives.security.zero_trust_stance}

## Secret Management

{directives.security.secret_management_rules}

## CVE Response

{directives.security.cve_response_plan}

## Input Validation

{directives.security.validation_philosophy}

## Web Security Defaults (CSRF/XSS)

{directives.security.web_security_defaults}

## Cryptography Defaults

{directives.security.cryptography_defaults}

## Audit Protocol

When reviewing code for security:
1. Check against EVERY rule above — they are {engineer_name}'s baseline, not optional recommendations
2. For secrets: flag anything that violates the secret management rules
3. For input validation: verify validation exists at the layers specified above
4. For dependencies: check CVEs against the CVE response plan
5. For web endpoints: verify CSRF/XSS protections match the web security defaults
6. For passwords/hashing: verify algorithm and cost match cryptography defaults
7. Rate severity using {engineer_name}'s actual risk tolerance, not a generic scale
