# Evidence Map

This mapping documents how public evidence was translated into backend directives.

| Directive | Confidence | Evidence |
|---|---|---|
| `directives.resilience.retry_strategy` | high | Public Netflix engineering discussions frequently emphasize resilient retries with safeguards against cascading failure. |
| `directives.infrastructure.deployment_philosophy` | high | Netflix public platform content consistently promotes progressive delivery and safe rollout patterns. |
| `directives.performance.caching_rules` | high | Caching strategy is a recurring public engineering topic, with explicit trade-offs around consistency and latency. |
| `directives.debugging.rca_process` | high | Incident learning and post-incident process discipline are central themes in public reliability writeups. |
| `directives.architecture.decomposition_philosophy` | medium | Public architecture material suggests decomposition around ownership and scale boundaries. |
| `directives.database.migration_playbook` | medium | Data migration guidance in public talks supports phased rollouts and rollback preparedness. |
| `directives.security.zero_trust_stance` | medium | Public cloud/security posture content indicates strong boundary validation and least-privilege direction. |
| `directives.code_review.blocking_criteria` | medium | Engineering culture materials indicate production-safety and operability concerns as review priorities. |
| `directives.testing.test_priority_rationale` | medium | Public engineering quality discussions prioritize critical-path and failure-mode confidence over vanity metrics. |
| `directives.meta_cognition.uncertainty_voice` | medium | Public writing style often frames trade-offs and assumptions explicitly rather than claiming certainty. |

> This output is a simulation and should be reviewed before production use.