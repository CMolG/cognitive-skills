> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: code_review.refactoring_stance, coding_style.* -->

# /refactor Command — Netflix Tech Blog

> Refactors code.

## Usage
/refactor [args]

## Behavior

1. Apply my refactoring stance: Refactor adjacent risky areas when already touching them, but keep scope bounded and observable.
2. Maintain my coding style across all changes
3. Type safety: Prefer explicit types at service boundaries and shared contracts. Do not rely on implicit behavior for critical paths.
4. Naming: Use domain-precise names that communicate intent and failure semantics. Avoid overloaded generic names.
5. Error handling: Handle errors as part of control flow. Include retry intent, terminal conditions, and actionable telemetry.
6. Quality calibration: High bar on reliability-critical paths; pragmatic speed on low-risk internal tooling.