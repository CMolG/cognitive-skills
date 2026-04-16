> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: coding_style.typing_rules, security.secret_management_rules, git_workflow.commit_message_format
-->

# pre-commit Hook — Netflix Tech Blog

> Enforces Netflix Tech Blog's exact pre-commit standards.

## Trigger

Before every commit


## Commit Message Format

Use clear intent-first commit messages: `<area>: <change>`, plus operational notes when relevant.

Example:
data-migration: add dual-write guardrail and rollback toggle

Reject any commit message that does not match this format.

## Type Safety Check

Prefer explicit types at service boundaries and shared contracts. Do not rely on implicit behavior for critical paths.

Run the type checker with the strictness level specified above. Block commits that violate these typing rules.

## Error Handling Check

Handle errors as part of control flow. Include retry intent, terminal conditions, and actionable telemetry.

Verify new code follows this error handling pattern.

## Secret Detection

No secrets in code or logs. Use managed secret stores, scoped credentials, and rotation paths.

Block any commit containing API keys, tokens, passwords in source files.

## Quality Gate

High bar on reliability-critical paths; pragmatic speed on low-risk internal tooling.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden