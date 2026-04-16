<!-- CEET Source:
  Raw Responses: Q06, Q08, Q15, Q32, Q35
  Directives: coding_style.typing_rules, coding_style.error_handling_rules, security.secret_management_rules, git_workflow.commit_message_format
-->

# Pre-Commit Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-commit standards. Not "strict" or "relaxed" — THEIR specific rules.

## Commit Message Format

{directives.git_workflow.commit_message_format}

Example:
{directives.git_workflow.commit_message_example}

Reject any commit message that does not match this format.

## Type Safety Check

{directives.coding_style.typing_rules}

Run the type checker with the strictness level specified above. Block commits that violate these typing rules.

## Error Handling Check

{directives.coding_style.error_handling_rules}

Verify new code follows this error handling pattern. Flag deviations.

## Secret Detection

{directives.security.secret_management_rules}

Block any commit containing:
- API keys, tokens, passwords in source files
- .env files with real credentials
- Any pattern that violates the secret management rules above

## Quality Gate

{directives.personality.quality_calibration}

Apply this quality calibration as the overall gate. Do not enforce higher standards than {engineer_name} would on a normal day.
