> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: security.* -->

# /security-check Command — Netflix Tech Blog

> Runs a security audit.

## Usage
/security-check [args]

## Behavior

1. Zero trust check: Assume every boundary can be hostile. Validate identity, authorize per action, and limit implicit trust zones.
2. Secret scan: No secrets in code or logs. Use managed secret stores, scoped credentials, and rotation paths.
3. CVE scan: Triage by exploitability and exposure, prioritize internet-facing/runtime paths, and patch with rollback-ready deployment plans.
4. Input validation: Validate input at boundaries with explicit schemas. Fail closed for unknown/untrusted payloads.
5. Web security: Default to secure headers, strict input handling, and least-privilege service communication.
6. Crypto check: Use battle-tested libraries and managed key services; avoid custom cryptographic design.