> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: coding_style.* -->

# Global Rule: Coding Standards — Netflix Tech Blog

> Netflix Tech Blog's coding standards applied to ALL code generated, reviewed, or modified. No exceptions unless Netflix Tech Blog's own decision framework permits one.


## Type Safety

Prefer explicit types at service boundaries and shared contracts. Do not rely on implicit behavior for critical paths.

## Naming Conventions

Use domain-precise names that communicate intent and failure semantics. Avoid overloaded generic names.

## Error Handling

Handle errors as part of control flow. Include retry intent, terminal conditions, and actionable telemetry.

## File Organization

Organize by runtime ownership and bounded context, not by framework artifact type alone.

## Comments

Comment the why and operational constraints, not obvious implementation details.

## Paradigm (OOP vs Functional)

Prefer simple, composable functions for data flow; use objects/interfaces where lifecycle or policy needs explicit boundaries.

## Enforcement

These rules are non-negotiable within Netflix Tech Blog's AI environment. Every agent, skill, and command inherits them. Violations must be flagged with a reference to the specific rule above.