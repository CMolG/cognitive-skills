---
name: ceet-founder-ceo
description: Cognitive Extraction Engine for founders and CEOs. Use when a user wants to clone an executive's judgment — how they set strategy, allocate capital and attention, write narratives, make hiring calls, and decide under ambiguity. Trigger on phrases like "extract my founder thinking", "clone my CEO style", "build an AI that drafts board updates like me", "interview me about strategy", "capture my decision-making framework", "make a founder cognitive clone". Outputs are tool-agnostic.
---

# CEET — Founder / CEO

## What this skill does

Interview a founder, CEO, or top executive. Produce a cognitive clone and AI environment that reasons about strategy, capital, narrative, org, and decision-making in their style.

## When to use

- The founder wants AI help with board updates, all-hands, investor emails, org decisions, and strategic memos in their own voice.
- A scaling org wants the founder's judgment made accessible to leaders via AI context.
- An incoming CEO wants to codify their working philosophy up front.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract** themes with special attention to **how they allocate attention** — founders' scarcest resource.
3. **Probe on recent hard calls.** Their reasoning under pressure is the core artifact.
4. **Synthesize** into `../_shared/templates/cognitive-clone.template.md`.
5. **Activate** into `../_shared/templates/ai-environment.template.md`. Save to `templates/`.
6. **Hand off** via `../_shared/prompts/activation-guide.md`.

## Founder-specific things to listen for

- **Strategic frame.** The one-sentence theory of the business and how they stress-test it.
- **Capital allocation.** How they think about fundraising, dilution, runway, ROI on cash.
- **Attention allocation.** What they protect vs. delegate. How they manage their calendar.
- **Hiring bar.** What they hire on for the first 20 vs. 100 vs. 500 employees.
- **Narrative voice.** Board memo, investor update, customer email, all-hands — same person, different register.
- **Decision posture.** When they decide fast, when they wait, when they reverse.
- **Communication rituals.** How information flows up and down in their org.
- **Board relationship.** What they share, when, how they handle pressure.
- **Crisis reflexes.** What they do when things are on fire.
- **Personal operating system.** Calendar, journaling, reading, coaching.

## Synthesis guardrails

- Capture their **board update skeleton** verbatim if they have one.
- Include their **decision procedure for ambiguous calls** (e.g. "When I can't decide, I ask X, then Y, then commit").
- Preserve tone across audiences — investors, team, customers.
- Include the founder's **narrative style** — how they compress a quarter into two paragraphs.
- Save outputs to `templates/`.
