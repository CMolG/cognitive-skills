# Artifact contracts

This file is the canonical reference for every artifact this repository
emits. Any change to the shape of an artifact must update both this file
and the source it lives next to.

## Versioning policy

Every artifact carries a top-level `schemaVersion` field on JSON outputs
and a YAML front-matter `schemaVersion` on Markdown outputs. The version
follows [SemVer](https://semver.org/):

- **Patch** — clarifications, additional examples, fixed typos in
  documentation. No code change required to consume the artifact.
- **Minor** — backward-compatible additions: new optional fields, new
  enum members, new artifact types. Old consumers continue to work.
- **Major** — breaking change: rename, removal, type change of an
  existing field, or change in the meaning of an existing value.
  Generated artifacts must record the schema version they were produced
  under so older runs remain interpretable.

Bumping rules:

1. Add the change to `CHANGELOG.md` under `### Added`, `### Changed`,
   or `### Removed`.
2. Update the version in code (e.g. `CONTRACT_SCHEMA_VERSION` in
   `jira_pipeline_cli.py`) and in the example payloads here.
3. If the bump is a major, add a migration note describing how
   consumers should adapt.

## Jira pipeline contracts

Detailed examples and field-by-field descriptions live in
[`jira-agentic-requirements-pipeline/references/contracts.md`](../jira-agentic-requirements-pipeline/references/contracts.md).

The pipeline emits four JSON artifacts, each with `schemaVersion: "1.0.0"`:

| Artifact | Producer | Consumer |
|---|---|---|
| `TicketAnalysis` | `discovery` | `generate-questions`, `base-branch-plan` |
| `BusinessQuestionSet` | `generate-questions` | `collect-input`, `resolve-contract` |
| `FunctionalContract` | `resolve-contract` | `base-branch-plan` |
| `BaseBranchPlan` | `base-branch-plan` | engineer review |

### `BusinessQuestionSet.budgets`

```json
{
  "baseline": 4,
  "signal": 6
}
```

Records the budget split used by the question selector. Lets downstream
tools (or future evaluations) reason about how the question pool was
constructed.

### `FunctionalContract.unmappedAnswers`

```json
[
  {"questionId": "Q11", "category": "Pricing, Billing & Monetization", "answer": "Free for the first 30 days"}
]
```

Captures any answer whose category does not map onto a declared field
in `functionalContract`. Without this list those answers would be
silently dropped — see `resolve_contract` in `jira_pipeline_cli.py`.

### `BaseBranchPlan.proposedBranchName`

The CLI never creates a Git branch. The field is a name suggestion
only; the engineer creates the branch manually after reviewing the
plan, and is free to rename it.

## Cognitive profile front-matter

Every `cognitive-profile.md` template starts with:

```yaml
---
schemaVersion: "1.0.0"
artifactType: cognitive-profile
---
```

Adding new front-matter keys is a minor bump. Renaming or removing
existing keys is a major bump.

## Orchestration contracts

The `ceet-sub-agent-orchestration` skill enforces two contracts before
dispatching work and after each sub-agent returns. Validation is
deterministic and runs through
[`ceet-sub-agent-orchestration/scripts/validate_handoff.py`](../ceet-sub-agent-orchestration/scripts/validate_handoff.py).

### `OrchestrationPlan`

```json
{
  "schemaVersion": "1.0.0",
  "planId": "plan-2026-05-07-001",
  "goal": "Refactor the checkout flow with parallel role-scoped reviews",
  "tasks": [
    {
      "id": "T1",
      "role": "ceet-backend-engineer",
      "scope": "Audit the order-service migration plan",
      "expectedArtifacts": ["report"],
      "dependsOn": []
    },
    {
      "id": "T2",
      "role": "ceet-frontend-engineer",
      "scope": "Audit the checkout component for accessibility",
      "expectedArtifacts": ["report"],
      "dependsOn": []
    },
    {
      "id": "T3",
      "role": "ceet-devops-sre",
      "scope": "Wire alerts for the new error budget",
      "expectedArtifacts": ["diff", "report"],
      "dependsOn": ["T1"]
    }
  ]
}
```

Constraints:

- `tasks` must be non-empty, with unique `id` values.
- Each task's `expectedArtifacts` must be non-empty.
- `dependsOn` may reference earlier tasks only — forward dependencies
  are rejected.

### `SubAgentResult`

```json
{
  "schemaVersion": "1.0.0",
  "planId": "plan-2026-05-07-001",
  "taskId": "T1",
  "role": "ceet-backend-engineer",
  "status": "completed",
  "artifacts": [
    {"path": "reports/T1-backend-audit.md", "kind": "report"}
  ],
  "summary": "Migration plan is safe under the documented dual-write window."
}
```

Constraints:

- `status` is one of `completed | failed | skipped`.
- `completed` requires at least one entry under `artifacts`.
- `failed` requires a non-empty `error` field.
- Artifact `kind` is one of `file | diff | report | decision`.

The orchestrator must reject any plan or result that fails validation
and stop the run rather than merge partial output.
