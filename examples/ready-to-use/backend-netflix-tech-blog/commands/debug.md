> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: debugging.*, performance.memory_leak_playbook -->

# /debug Command — Netflix Tech Blog

> Debugs a problem using Netflix Tech Blog's exact diagnostic process.

## Usage
/debug [args]

## Behavior

1. Apply my silent failure protocol: Assume silent failures exist until disproven. Trace request lifecycles with correlation IDs and verify each hop.
2. Use my logging philosophy: Logs should explain state transitions and failure context, not just stack traces.
3. For memory issues: Use heap profiling under realistic load, compare snapshots, and isolate retention growth to ownership boundaries.
4. For dependency issues: Pin and audit dependency changes. Prefer deterministic build inputs and explicit compatibility validation.
5. For ghost bugs: Chase nondeterminism via controlled replay, percentile slicing, and environment parity checks.
6. Escalate if: Escalate early on unresolved invariants, customer-impacting risk, and unclear ownership under incident pressure.