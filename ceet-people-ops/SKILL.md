---
name: ceet-people-ops
description: Cognitive Extraction Engine for People / HR leaders — hiring, performance, comp, culture, org design. Use when a user wants to clone a People leader's judgment — how they design processes for hiring and feedback, how they diagnose culture, handle difficult conversations, and build org policy. Trigger on phrases like "extract my people ops thinking", "clone our head of people", "build an AI that drafts performance reviews like me", "interview me about culture", "capture my hiring rubric", "make a people-ops cognitive clone". Outputs are tool-agnostic.

NOTE: The outputs of this CEET describe *one person's reasoning* about People practices. They should not be treated as employment-law advice. The AI environment must preserve that disclaimer.
---

# CEET — People Ops / HR

## What this skill does

Interview a People leader (Head of People, People Partner, Talent leader). Produce a cognitive clone and AI environment that reasons about hiring, performance, comp, policy, and culture in their style.

## When to use

- The user wants AI help with job descriptions, rubrics, feedback drafts, review notes, policy drafts — in their voice.
- A People leader wants to scale their judgment across hiring managers and partners.
- A founder wants their culture and standards captured before a People function exists.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract** themes. Pay attention to tone — People work is high-stakes emotionally.
3. **Probe on hard cases.** A PIP, a layoff, a complaint — these reveal real judgment.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## People-Ops-specific things to listen for

- **Hiring bar.** What they hire on, what they refuse to compromise on.
- **Rubric design.** Signal vs. noise in interviews. Scorecard discipline.
- **Leveling & comp.** Framework, bands, transparency stance.
- **Performance philosophy.** Continuous feedback, formal reviews, calibration, ratings vs. narratives.
- **PIP stance.** When, how, and what they refuse to do.
- **Difficult conversations.** Framing, openers, preparation.
- **Culture diagnosis.** How they read a team — signals, not surveys.
- **Policy voice.** Formal, warm, terse, example-rich?
- **Org design.** Span of control, layers, when to split a team.
- **DEI posture.** What they measure, what they refuse to reduce to metrics.

## Synthesis guardrails

- Capture their **interview rubric** structure verbatim if they have one.
- Include their **performance review template** or skeleton.
- Preserve the **tone** they use in sensitive written communication.
- Include a **disclaimer block** in the AI environment — this is reasoning in their style, not HR / employment-law advice.
- Save outputs to `templates/`.
