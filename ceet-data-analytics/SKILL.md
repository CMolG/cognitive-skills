---
name: ceet-data-analytics
description: Cognitive Extraction Engine for data scientists, analytics engineers, and data analysts. Use whenever a user wants to clone the judgment of a data practitioner — how they frame questions, design metrics, build models, run experiments, pick tools (SQL / Python / dbt / notebooks), and reason about confidence and causality. Trigger on "extract my analytics thinking", "clone our data scientist", "build an AI analyst that thinks like me", "interview me about metrics and experiments", "make a data cognitive clone". Outputs are tool-agnostic.
---

# CEET — Data / Analytics

## What this skill does

Interview a data person (data scientist, analytics engineer, analyst, ML practitioner). Produce a tool-agnostic cognitive clone plus AI environment that reasons about data questions in their style.

## When to use

- The user wants an AI collaborator that writes SQL / dbt / notebook code with *their* conventions and *their* statistical rigor.
- A team wants to scale one data leader's analytical judgment across AI-assisted analysts.
- The user is codifying the organization's experimentation and metrics culture.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract.** Tag themes. Pay special attention to how they separate *descriptive / diagnostic / predictive / prescriptive* thinking.
3. **Ask for real analyses.** Have them walk through a recent analysis end-to-end — the choices they made, the ones they rejected.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## Data-specific things to listen for

- **Question framing.** How do they turn "what's going on with X" into a tractable, answerable question?
- **Metric design.** What makes a good metric to them? Cardinality, stability, gaming resistance.
- **Causal thinking.** RCT, diff-in-diff, synthetic control, observational — what they reach for and when.
- **Confidence & honesty.** How they communicate uncertainty. What they refuse to claim.
- **Data quality reflexes.** What they check before trusting a table. How they smell a bad join.
- **Modeling taste.** Simple vs. complex — when each. Thresholds for "good enough."
- **Reproducibility.** Notebooks vs. scripts vs. dbt models vs. dashboards — their workflow.
- **Stakeholder translation.** How they narrate numbers to non-technical audiences.
- **A/B experimentation.** Power calcs, MDE, guardrails, peeking — their discipline.
- **Tool taste.** SQL dialect preferences, pandas vs. Polars vs. DuckDB, viz library choices.

## Synthesis guardrails

- Capture their specific metric-naming conventions (e.g. snake_case, domain prefixes).
- Include at least one **worked example** in the clone — a named analysis and the choices they made — because data judgment is heavily example-driven.
- Save outputs to `templates/`.
