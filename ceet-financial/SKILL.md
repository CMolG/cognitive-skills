---
name: ceet-financial
description: Cognitive Extraction Engine for finance professionals — CFOs, FP&A leads, controllers, finance ops, finance partners to product/sales. Use when a user wants to clone a finance operator's judgment — how they build models, run forecasts, reason about unit economics, set budgets, and say no to spend. Trigger on phrases like "extract my finance thinking", "clone our CFO", "build an AI that drafts board models like me", "interview me about FP&A", "capture my forecasting playbook", "make a finance cognitive clone". Outputs are tool-agnostic.
---

# CEET — Finance

## What this skill does

Interview a finance leader. Produce a cognitive clone and AI environment that reasons about models, forecasts, unit economics, budgeting, and capital allocation in their style.

## When to use

- The user wants an AI that drafts board memos, financial models, or scenario analyses in their voice.
- A CFO wants their judgment scaled across an FP&A team.
- A founder wants finance instincts captured before hiring a CFO.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract.** Finance judgment leans heavily on **assumptions** — probe on how each assumption is chosen.
3. **Ask for a scenario** — e.g. "walk me through how you'd re-forecast if revenue missed by 20%."
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## Finance-specific things to listen for

- **Model taste.** Monolithic vs. modular, driver-based vs. line-item, opinions on circular references, color/format conventions.
- **Assumption discipline.** Where they justify, where they approximate, where they refuse to guess.
- **Unit economics frame.** CAC, payback, LTV, contribution margin — which they actually trust.
- **Forecasting method.** Bottoms-up vs. tops-down, sales-led forecast vs. FP&A forecast, variance tolerance.
- **Budgeting philosophy.** Zero-based, last-year-plus, OKR-tied.
- **Capital allocation.** ROI hurdles, payback bars, strategic exceptions.
- **Board / investor voice.** What they emphasize, what they refuse to hide.
- **Controls & close.** Non-negotiables in month-end close.
- **Scenario modeling.** How they build base / bull / bear, sensitivity tables.
- **Pricing support.** When they get involved in pricing and what they argue for.

## Synthesis guardrails

- Capture their **model conventions** (naming, color coding, sheet structure, units).
- Include their **top 5 forecasting assumptions** and where each one comes from.
- Preserve their **board-voice phrases** — finance memos have a specific register.
- Save outputs to `templates/`.
