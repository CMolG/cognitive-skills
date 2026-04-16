> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: debugging.*, resilience.*, infrastructure.*, meta_cognition.* -->

# /incident Command — Netflix Tech Blog

> Handles a production incident.

## Usage
/incident [args]

## Behavior

1. Crisis communication mode: Calm, timeline-driven, and action-oriented. Prioritize containment then root cause.
2. Alert classification: Page on user-impacting symptoms, ticket on predictive maintenance signals. Keep alerts actionable.
3. Diagnostic protocol: Assume silent failures exist until disproven. Trace request lifecycles with correlation IDs and verify each hop.
4. Mitigation: deployment rollback, graceful degradation, rate limits per my directives
5. RCA: Reconstruct timeline, identify triggering condition, isolate contributing factors, and produce prevention actions with owners.
6. Escalation: Escalate early on unresolved invariants, customer-impacting risk, and unclear ownership under incident pressure.