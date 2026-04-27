---
name: jira-agentic-requirements-pipeline
description: Run a two-phase agentic requirements pipeline connected to Jira (Requirement Discovery and Base Branch Generation). Use when a team wants to analyze Jira tickets, detect business ambiguity, generate structured non-technical business questions, collect business answers from CLI with resumable session state, resolve a functional contract, and prepare a constrained base-branch plan with traceability and guardrails.
---

# Jira Agentic Requirements Pipeline

Execute this workflow to convert ambiguous Jira tickets into actionable engineering inputs without inventing product decisions.

## Mandatory flow (run in order)

1. Fetch Jira issue with `scripts/jira_pipeline_cli.py fetch-issue`.
2. Run requirement discovery with `scripts/jira_pipeline_cli.py discovery`.
3. Generate business questions with `scripts/jira_pipeline_cli.py generate-questions`.
4. Collect business answers in terminal with `scripts/jira_pipeline_cli.py collect-input`.
5. Resolve functional contract with `scripts/jira_pipeline_cli.py resolve-contract`.
6. Build base-branch plan with `scripts/jira_pipeline_cli.py base-branch-plan`.

If required answers are missing, stop in phase 1 and do not plan implementation.

## Decision rules

- Ask only functional/product/operations questions.
- Infer architecture and implementation details from repository patterns.
- Keep required questions small and prioritized (typically 5-10).
- If inference confidence is low (`< 0.65`), generate questions only and request human review.
- Never auto-merge.

## Jira integration

Set environment variables:

- `JIRA_BASE_URL` (example: `https://company.atlassian.net`)
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`

The CLI uses Jira REST API v3.

## CLI mode without losing session state

For business input in terminal:

- Run `collect-input` with `--state-file`.
- State is persisted after each answer.
- If terminal closes or receives `Ctrl+C`, rerun and continue from the next pending question.
- Use `--non-interactive` to validate required completeness in CI or automation.

## References and templates

- Internal contracts: `references/contracts.md`
- Full business question catalog and prioritization: `references/question-catalog.md`
- Jira/report templates: `templates/`

## Guardrails

- Phase 1 is read-only for code changes.
- Phase 2 can prepare a base branch plan/report but must not merge.
- Keep mandatory traceability: ticket -> questions -> answers -> functional contract -> implementation plan.
