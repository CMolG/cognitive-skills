---
name: ceet-ui-designer
description: Cognitive Extraction Engine for UI designers — product designers focused on visual system, components, typography, motion, and craft. Use when a user wants to clone a UI designer's taste and judgment — how they make visual decisions, set up systems, critique work, and balance brand with usability. Trigger on phrases like "extract my design taste", "clone our UI designer", "build an AI that critiques mocks like me", "interview me about visual design", "capture my design system philosophy", "make a UI cognitive clone". Outputs are tool-agnostic.
---

# CEET — UI Designer

## What this skill does

Interview a UI / product designer. Produce a cognitive clone plus AI environment that can critique mocks, propose component variants, and write design rationale in their voice.

## When to use

- The user wants an AI critique partner that matches their visual taste.
- A design lead wants to codify house style and scale it via AI.
- A founding designer wants their taste captured before the team scales.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract.** Because UI is so subjective, lean heavily on **examples**: ask them to name specific products, screens, moments they love/hate, and *why*.
3. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
4. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
5. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## UI-specific things to listen for

- **Grid & spacing taste.** 4pt / 8pt systems, tight vs. airy, ratio preferences.
- **Type systems.** Type scale, weights, line-height convictions, serif/sans preferences for context.
- **Color philosophy.** Saturated vs. desaturated, neutral ramps, semantic tokens, contrast bar.
- **Components.** What primitive does the system start from? How far do they build up before stopping?
- **Motion.** Where to add, where to resist, easing and duration defaults, reduced motion stance.
- **Craft details.** Focus states, hover states, loading states, empty states — which do they obsess over.
- **Icon & illustration taste.** Style, grid, line weight, illustration role.
- **Brand vs. usability.** Where do they let brand win? Where do they refuse?
- **Critique voice.** How do they give feedback? What words do they reach for?
- **Figma / tooling discipline.** Naming, auto-layout, variables, libraries, components vs. assets.

## Synthesis guardrails

- UI taste is best captured through **named exemplars** — products, sites, designers they respect. Include them.
- Capture the **critique vocabulary** verbatim ("this feels heavy", "the rhythm's off", "it's too polite").
- Include their token/naming conventions if any.
- Save outputs to `templates/`.
