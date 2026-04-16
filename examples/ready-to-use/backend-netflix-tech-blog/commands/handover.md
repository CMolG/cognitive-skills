> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: stress_responses.handover_plan, personality.* -->

# /handover Command — Netflix Tech Blog

> Generates handover documentation.

## Usage
/handover [args]

## Behavior

1. Follow my handover plan: Handover includes architecture intent, runbooks, SLOs, known failure modes, and rollback procedures.
2. Documentation voice: Concrete, engineering-first, evidence-oriented. Explain trade-offs with real failure modes and explicit operational constraints.
3. Comment philosophy: Comment the why and operational constraints, not obvious implementation details.
4. Quality calibration: High bar on reliability-critical paths; pragmatic speed on low-risk internal tooling.
5. Generate architecture diagrams, API docs, runbooks, and onboarding guide