# Worked examples

Three end-to-end runs that show how the pipeline handles tickets at
different ambiguity levels. The fixtures live under
[`tests/jira/fixtures/`](../tests/jira/fixtures/) and are the same ones
used by the test suite, so the outputs are reproducible.

> All examples assume the CLI variable is set:
>
> ```bash
> CLI=jira-agentic-requirements-pipeline/scripts/jira_pipeline_cli.py
> ```

---

## Example 1 — A clean ticket → `READY_FOR_BASE_BRANCH`

Source: [`tests/jira/fixtures/issue_tight.json`](../tests/jira/fixtures/issue_tight.json).
The ticket specifies scope, success/error/expired/cancelled states,
limits, communications, audit trail, rollout, and acceptance.

```bash
python3 "$CLI" discovery --input tests/jira/fixtures/issue_tight.json --output analysis.json
python3 "$CLI" generate-questions --input analysis.json --output questions.json
# Answer all required questions (interactive) or synthesize answers in CI
python3 "$CLI" collect-input --input questions.json --state-file state.json --non-interactive
python3 "$CLI" resolve-contract --questions questions.json --answers state.json --output contract.json
python3 "$CLI" base-branch-plan --analysis analysis.json --contract contract.json --output plan.json
```

What you get:

- `analysis.ambiguityLevel.level` → `LOW` (constraint density `8.42`, no
  ambiguity markers).
- `analysis.missingBusinessDecisions` → `[]`. The ticket already
  describes every category the rule-based detector tracks.
- `plan.status` → `READY_FOR_BASE_BRANCH`, `confidence: 0.90`.
- `plan.proposedBranchName` → `ai/demo-100-base`. Note: the CLI does not
  create the branch — the engineer creates it after reviewing the plan.

---

## Example 2 — A near-empty ticket → `QUESTIONS_ONLY`

Source: [`tests/jira/fixtures/issue_empty.json`](../tests/jira/fixtures/issue_empty.json).
The ticket has only a title (`"Approval flow"`) and a description of
`"TBD"`.

```bash
python3 "$CLI" discovery --input tests/jira/fixtures/issue_empty.json --output analysis.json
python3 "$CLI" generate-questions --input analysis.json --output questions.json
```

The discovery output shows what is missing:

```json
{
  "schemaVersion": "1.0.0",
  "ambiguityLevel": {
    "level": "HIGH",
    "constraintDensity": 0.0,
    "ambiguityMarkers": 33.333,
    "signals": {
      "constraintKeywords": [],
      "ambiguityMarkers": ["tbd"]
    }
  },
  "missingBusinessDecisions": [
    "acceptance_criteria", "auditability", "communications",
    "compliance", "error_behavior", "expiration", "legacy_compatibility",
    "limits", "rollout", "scope", "success_behavior", "support_behavior"
  ]
}
```

Generated questions cover:

- The 4 baseline P0 templates (BO-1, FS-1, BR-1, SL-1).
- 6 signal-driven templates ranked by how strongly each one matches the
  missing decisions (CP-1, RL-1, SP-1, CM-1, LC-1, AC-1).

Stop here. Do not run `base-branch-plan` until the business has answered
the required questions.

---

## Example 3 — Ambiguity markers despite long text → `QUESTIONS_ONLY`

Source: [`tests/jira/fixtures/issue_ambiguous.json`](../tests/jira/fixtures/issue_ambiguous.json).
The text is reasonably long but every other sentence contains a marker
(`TBD`, `we should`, `maybe`, `not sure`, `pending`, `unknown`,
`alternatively`, `to be defined`).

```bash
python3 "$CLI" discovery --input tests/jira/fixtures/issue_ambiguous.json --output analysis.json
```

The new ambiguity-level rule rejects "long therefore specific":

```json
{
  "ambiguityLevel": {
    "level": "HIGH",
    "constraintDensity": 0.0,
    "ambiguityMarkers": 10.59,
    "signals": {
      "constraintKeywords": [],
      "ambiguityMarkers": ["tbd", "we should", " or ", "alternatively", "maybe", "not sure", "to be defined", "pending", "unknown"]
    }
  }
}
```

Both the constraint density and the marker density are reported, so
downstream tooling can react to the *shape* of the ambiguity instead of
treating every HIGH the same.

---

## Customizing question budgets

Two CLI flags control how the question selector splits its slots:

```bash
python3 "$CLI" generate-questions \
  --input analysis.json \
  --output questions.json \
  --baseline-budget 3 \
  --signal-budget 7
```

The `baseline-budget` reserves slots for the universally required P0
templates (BO-1 / FS-1 / BR-1 / SL-1, picked deterministically). The
`signal-budget` is filled with templates whose `signals` array
intersects the analysis' `missingBusinessDecisions`, ranked by match
strength. If the signal pool underfills, remaining P0/P1 templates
overflow into the empty slots so the pipeline never under-asks.
