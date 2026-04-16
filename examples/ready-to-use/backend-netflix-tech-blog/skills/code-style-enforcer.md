> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source:
  Role: backend-engineer
  Directives: coding_style.*
-->

# Code Style Enforcer Skill — Netflix Tech Blog

> Enforces Netflix Tech Blog's exact coding style — not 'strict mode' or 'balanced mode', this person's rules.


## Typing Rules

Prefer explicit types at service boundaries and shared contracts. Do not rely on implicit behavior for critical paths.

## Naming Conventions

Use domain-precise names that communicate intent and failure semantics. Avoid overloaded generic names.

## Error Handling Pattern

Handle errors as part of control flow. Include retry intent, terminal conditions, and actionable telemetry.

## File Organization

Organize by runtime ownership and bounded context, not by framework artifact type alone.

## Commenting Rules

Comment the why and operational constraints, not obvious implementation details.

## Paradigm Rules (OOP vs Functional)

Prefer simple, composable functions for data flow; use objects/interfaces where lifecycle or policy needs explicit boundaries.

## Enforcement Protocol

When applying these rules:
1. Quote the specific rule being applied
2. Show the exact fix using Netflix Tech Blog's conventions
3. If two rules conflict, reference Prefer decisions that reduce blast radius, are observable in production, and are reversible under pressure. If two options look similar, pick the one that is easier to test and rollback. to resolve
4. Never cite "best practices" or "industry standard" — cite the rule above