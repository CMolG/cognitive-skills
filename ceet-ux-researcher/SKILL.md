---
name: ceet-ux-researcher
description: Cognitive Extraction Engine for UX researchers — especially the "conductual" (behavioral) kind. Use when a user wants to clone the judgment of a researcher who studies user behavior — how they design studies, frame research questions, interview, observe, synthesize, and influence decisions. Trigger on phrases like "extract my research thinking", "clone our UX researcher", "build an AI that drafts interview guides like me", "interview me about behavioral research", "capture how I synthesize user interviews", "make a UXR cognitive clone". Outputs are tool-agnostic.
---

# CEET — UX Researcher (conductual)

## What this skill does

Interview a UX / behavioral researcher. Produce a cognitive clone plus an AI environment that drafts research plans, interview guides, synthesis notes, and readouts in their voice.

"Conductual" here = focused on **observed behavior**, not just stated preference. The CEET's default orientation is toward behavioral evidence (what users do) over attitudinal reports (what users say).

## When to use

- The user wants an AI that writes discussion guides, codes interviews, and drafts readouts in their style.
- A research lead wants to scale research literacy across designers, PMs, or AI-assisted helpers.
- A solo researcher wants an AI thinking partner that respects behavioral rigor.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract** themes, with a bias toward **craft detail** — this is a craft-heavy role.
3. **Probe on synthesis.** The hardest-to-capture judgment is how they move from raw notes to a claim. Have them narrate a recent synthesis end-to-end.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## UXR-specific things to listen for

- **Research question design.** How they reshape product questions into answerable research questions.
- **Method selection.** Interviews, diary studies, usability tests, surveys, analytics, ethnography — their tree.
- **Behavioral vs. attitudinal discipline.** What they trust, what they discount.
- **Participant recruiting standards.** Who they'd refuse to include and why.
- **Interview technique.** Laddering, critical incident, think-aloud, silence discipline.
- **Synthesis workflow.** Affinity mapping, tagging, JTBD statements, behavioral archetypes.
- **Communicating findings.** Readout formats, what they show the team vs. leadership.
- **Influence pattern.** How they make research actually change a decision.
- **Ethics.** Consent, recording, compensation, anonymization — what they insist on.
- **Validity reflexes.** Bias they watch for in themselves and their team.

## Synthesis guardrails

- Capture their exact **interview opener** and **closing question** if they have go-to phrases.
- Include a **synthesis procedure** — the step-by-step from transcripts to claim.
- Preserve vocabulary (JTBD vs. need vs. jobs vs. goal vs. outcome — teams differ).
- Save outputs to `templates/`.
