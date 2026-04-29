<!-- CEET Source:
  Role: backend-engineer
  Directives: coding_style.typing_rules, security.secret_management_rules, git_workflow.commit_message_format
-->

# pre-commit Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-commit standards.

## Trigger

Before every commit


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

Verify new code follows this error handling pattern.

## Secret Detection

{directives.security.secret_management_rules}

Block any commit containing API keys, tokens, passwords in source files.

## Quality Gate

{directives.personality.quality_calibration}

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden