---
name: ceet-copywriter
description: Cognitive Extraction Engine for copywriters and UX writers. Use when a user wants to clone a writer's voice, editorial judgment, and conversion instincts — for marketing, product, email, landing pages, and microcopy. Trigger on phrases like "extract my copy voice", "clone our copywriter", "build an AI that writes in my tone", "interview me about writing", "capture my brand voice", "make a copywriter cognitive clone", or any request to distill writing judgment into a reusable AI configuration. Outputs are tool-agnostic.
---

# CEET — Copywriter

## What this skill does

Interview a writer (copywriter, UX writer, content designer, editorial lead). Produce a cognitive clone and an AI environment that drafts and edits in their voice and with their judgment.

## When to use

- The user wants AI that writes landing pages, emails, product copy, or microcopy in their voice.
- A brand wants to codify editorial standards for AI-assisted writing across teams.
- A solo writer wants reusable rules beyond a "brand voice doc."

## Run order

1. **Read** `interview/questions.md`.
2. **Extract.** Voice is best captured by contrast — ask what they *wouldn't* say, alongside what they would.
3. **Collect exemplars.** Favorite ads, emails, landing pages, authors, and three samples of their own work they're proud of.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md` with special attention to the **Vocabulary & Voice** section.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## Copywriter-specific things to listen for

- **Voice principles.** Not "friendly and professional" — the specific shape (contractions? semicolons? sentence length? rhythm?).
- **Hook & structure.** How they open a landing page / email / ad. Their AIDA-or-not.
- **Audience empathy.** How they imagine the reader. What they assume about attention.
- **Persuasion stance.** Proof, story, feature-benefit, provocation — which they favor.
- **Editing craft.** Ruthless cutting, cadence checks, reading aloud.
- **Conversion instincts.** CTAs, urgency, framing — where they go hard, where they refuse.
- **Brand voice codification.** Voice axes (serious↔playful, formal↔casual, reverent↔irreverent).
- **Banned words.** The list.
- **Dialogue with design.** How they work with visuals, where copy and design blend.
- **Heroes.** Writers / brands / ads they measure against.

## Synthesis guardrails

- Capture **do/don't pairs** (preferred vs. avoided phrases).
- Include their **sentence-level taste**: rhythm preferences, sentence length variance, punctuation choices.
- Include at least 3 **before/after examples** they walk you through — edits narrate voice better than rules.
- Save outputs to `templates/`.
