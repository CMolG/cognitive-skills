<!-- CEET Source:
  Raw Responses: Q06, Q07, Q08, Q09, Q10, Q11
  Directives: coding_style.*
-->

# Code Style Enforcer Skill — {engineer_name}

> Enforces {engineer_name}'s exact coding style. Not "strict mode" or "balanced mode." THIS person's rules, with THEIR exceptions.

## Typing Rules

{directives.coding_style.typing_rules}

## Naming Conventions

{directives.coding_style.naming_rules}

Apply these conventions to ALL code generated or reviewed. Flag violations by referencing the convention above.

## Error Handling Pattern

{directives.coding_style.error_handling_rules}

When generating or reviewing error handling code, use ONLY this approach. Do not default to try/catch or Result types based on general best practices — use {engineer_name}'s stated preference.

## File Organization

{directives.coding_style.file_organization_rules}

When creating new files, follow this organization. When reviewing PRs, flag deviations.

## Commenting Rules

{directives.coding_style.commenting_rules}

## Paradigm Rules (OOP vs Functional)

{directives.coding_style.paradigm_rules}

## Enforcement Protocol

When reviewing code against these rules:
1. Quote the specific rule being violated
2. Show the exact fix using {engineer_name}'s conventions
3. If two rules conflict, reference {identity.decision_framework} to resolve
4. Never cite "best practices" or "industry standard" — cite the rule above
