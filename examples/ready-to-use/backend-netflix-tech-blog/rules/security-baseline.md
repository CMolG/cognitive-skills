> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: security.* -->

# Global Rule: Security Baseline — Netflix Tech Blog

> Netflix Tech Blog's security baseline applied to all code and infrastructure decisions. No exceptions unless Netflix Tech Blog's own decision framework permits one.


## Zero Trust

Assume every boundary can be hostile. Validate identity, authorize per action, and limit implicit trust zones.

## Secret Management

No secrets in code or logs. Use managed secret stores, scoped credentials, and rotation paths.

## CVE Response

Triage by exploitability and exposure, prioritize internet-facing/runtime paths, and patch with rollback-ready deployment plans.

## Input Validation

Validate input at boundaries with explicit schemas. Fail closed for unknown/untrusted payloads.

## Web Security

Default to secure headers, strict input handling, and least-privilege service communication.

## Cryptography

Use battle-tested libraries and managed key services; avoid custom cryptographic design.

## Enforcement

These rules are non-negotiable within Netflix Tech Blog's AI environment. Every agent, skill, and command inherits them. Violations must be flagged with a reference to the specific rule above.