<!-- CEET Source:
  Role: frontend-engineer
  Directives: typescript.*, styling.*, git_workflow.*
-->

# pre-commit Hook — {engineer_name}

> Enforces {engineer_name}'s exact pre-commit standards.

## Trigger

Before every commit


## Commit Message Format

{directives.git_workflow.commit_message_format}

## TypeScript Check

{directives.typescript.strictness_level}

{directives.typescript.any_policy}

## Styling Lint

{directives.styling.methodology}

## a11y Lint

{directives.accessibility.pre_merge_checklist}

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden