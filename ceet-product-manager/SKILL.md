---
name: ceet-product-manager
description: Cognitive Extraction Engine for product managers. Use when a user wants to clone the judgment of a PM — how they prioritize, frame problems, run discovery, write specs, manage stakeholders, define success, and say no. Trigger on phrases like "extract my PM thinking", "clone our head of product", "build an AI that writes PRDs like me", "interview me about product management", "capture how I prioritize", "make a product cognitive clone". Outputs are tool-agnostic.
---

# CEET — Product Manager

## What this skill does

Interview a product manager. Produce a cognitive clone and an AI environment that frames, prioritizes, writes, and communicates product work in their style.

## When to use

- The user wants an AI that drafts PRDs, reviews specs, or triages feedback the way they would.
- A CPO wants to scale their judgment across a team of PMs with AI support.
- A founding PM wants their product sense captured before the team grows.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract** themes: `#mental-model`, `#heuristic`, `#procedure`, `#quality`, `#anti-pattern`, `#vocabulary`.
3. **Push on "no".** PM judgment is defined as much by what they *refuse* as what they approve. Get concrete examples.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## PM-specific things to listen for

- **Problem framing.** How they distinguish a real problem from a requested solution.
- **Prioritization system.** RICE, WSJF, opportunity-solution tree, instinct, narrative — and how they actually use it vs. say they use it.
- **Discovery habits.** User interviews cadence, assumption mapping, opportunity backlog.
- **Roadmap philosophy.** Dates vs. outcomes vs. themes. Commitment vs. direction.
- **Specs / PRDs.** Their template, what they include, what they refuse to include.
- **Success metrics.** How they define it *before* shipping. What counts as "this didn't work."
- **Stakeholder management.** How they handle exec escalation, sales asks, eng pushback, design tension.
- **Saying no.** Their script, their framing, their last-resort move.
- **Cross-functional partnerships.** How they work with eng lead, design lead, data, GTM.
- **Judgment calls.** Build vs. buy, feature vs. fix, polish vs. ship, vertical vs. horizontal.

## Synthesis guardrails

- Capture their **prioritization procedure** step-by-step — this is the most reusable artifact for an AI.
- Include their **default PRD skeleton** verbatim if they have one.
- Preserve their **framing vocabulary** (problem statement vs. JTBD vs. opportunity, etc.).
- Save outputs to `templates/`.
