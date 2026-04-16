---
name: ceet-sales
description: Cognitive Extraction Engine for sales professionals — AEs, reps, sales leaders, solutions consultants. Use when a user wants to clone a seller's judgment — how they discover, qualify, handle objections, negotiate, close, and forecast. Trigger on phrases like "extract my sales thinking", "clone our top AE", "build an AI that drafts outreach like me", "interview me about sales discovery", "capture my objection playbook", "make a sales cognitive clone". Outputs are tool-agnostic.
---

# CEET — Sales

## What this skill does

Interview a sales professional. Produce a cognitive clone and AI environment that drafts outreach, discovery questions, objection responses, and proposals in their style.

## When to use

- The user wants an AI that writes emails / follow-ups / proposals in their voice, with their judgment about what to say to whom.
- A sales leader wants a top rep's pattern captured and scaled via AI.
- A founder-seller wants their discovery style preserved as hiring starts.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract** themes with an eye on **discovery** (it's the most undervalued part of great selling).
3. **Ask for deal stories** — a win, a loss, a messy one. The messy one usually reveals the most.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## Sales-specific things to listen for

- **ICP & qualification.** Their actual bar, how they disqualify fast, what they refuse to chase.
- **Discovery style.** The questions they always ask, what they listen for, how they avoid demo-leading.
- **Methodology.** MEDDICC / SPICED / Challenger / Sandler — what they use and how they customized it.
- **Objection patterns.** The 5-10 recurring objections and their responses (verbatim if possible).
- **Pricing & negotiation.** Anchor behavior, discount ladder, trade behavior.
- **Forecasting discipline.** What they count as committed vs. best-case.
- **Email / outreach voice.** Length, openers, subject lines, follow-up cadence.
- **Multi-threading instincts.** How and when they bring in exec / champion / economic buyer.
- **Handoff to CS.** What they tell the CS team, what they refuse to promise.
- **Losing posture.** What they do when a deal is slipping. What they refuse to do.

## Synthesis guardrails

- Capture their **discovery question set** verbatim.
- Include their **objection library** as do/say/don't-say triplets.
- Preserve **email voice** — short / long, signature, sign-off, reply patterns.
- Save outputs to `templates/`.
