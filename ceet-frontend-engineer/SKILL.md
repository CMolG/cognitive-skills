---
name: ceet-frontend-engineer
description: Cognitive Extraction Engine for frontend engineers. Use whenever a user wants to "clone" a frontend engineer's judgment about UI architecture, rendering, state, accessibility, and client-side performance, or build a personalized AI environment for frontend work that mirrors their specific taste and heuristics. Trigger on phrases like "extract my frontend style", "build an AI setup that writes components like me", "interview me about frontend engineering", "make a React/Vue/Svelte cognitive clone", "capture how I think about UI state", or any request to distill frontend judgment into a reusable AI configuration. Outputs are tool-agnostic (Claude, ChatGPT, Cursor, Copilot, Gemini, etc.).
---

# CEET — Frontend Engineer

## What this skill does

Interview a frontend engineer and produce two tool-agnostic artifacts: a **cognitive clone** describing how they think about UI work, and an **AI environment** usable as a system prompt in any AI tool.

## When to use

- The user wants an AI that writes components, styles, and interactions in *their* style — not generic React/Vue/Svelte boilerplate.
- The user is codifying team frontend conventions and wants a portable artifact.
- The user is onboarding collaborators and wants "this is how we build the UI" captured once.

## Run order

1. **Read** `interview/questions.md`. Walk through it conversationally, theme by theme.
2. **Extract.** Tag answers privately: `#mental-model`, `#heuristic`, `#procedure`, `#quality`, `#anti-pattern`, `#vocabulary`, `#taste`.
3. **Probe on taste.** Frontend has more visual/subjective judgment than backend. Ask for *examples of sites or components they love/hate* — taste is extracted more by example than by rule.
4. **Synthesize** into [`../_shared/templates/cognitive-clone.template.md`](../_shared/templates/cognitive-clone.template.md).
5. **Activate** into [`../_shared/templates/ai-environment.template.md`](../_shared/templates/ai-environment.template.md). Save both to `templates/`.
6. **Hand off** via [`../_shared/prompts/activation-guide.md`](../_shared/prompts/activation-guide.md).

## Frontend-specific things to listen for

- **State philosophy.** Local vs. lifted vs. global. When they reach for a store and when they refuse. URL as state. Server state vs. client state.
- **Component boundaries.** What makes a component "too big"? How do they factor?
- **Rendering mental model.** SSR / SSG / CSR / streaming / islands — when each, and why.
- **Accessibility reflexes.** Do they think keyboard-first? What do they audit before shipping?
- **Styling philosophy.** CSS-in-JS / utility classes / CSS modules / design tokens — and the taste behind the choice.
- **Performance instincts.** Which Web Vitals they chase first, what bundle patterns they distrust.
- **Forms & validation.** Where do they put validation? How do they design error states?
- **Motion & micro-interactions.** Where are they subtle, where bold, what do they refuse to animate?
- **Error & loading states.** Empty / loading / error / partial — do they design all four, or lazy into two?
- **Testing pyramid on frontend.** Unit vs. component vs. E2E vs. visual regression — their mix, their reasons.
- **Design handoff.** How tightly do they follow designs? Where do they push back and why?

## Synthesis guardrails

- Keep their vocabulary. If they call a styled primitive a "brick" or a "motif", that goes in the clone.
- Frontend taste is often *negative* — what they refuse to ship. Capture those anti-patterns verbatim.
- Accessibility: don't let them hand-wave. Ask for specifics (keyboard paths, focus traps, label conventions).
- Save outputs to `templates/`.

## When to stop

The user reads their clone and says "yes, but this component example — I'd actually structure it with X not Y." Fix it. Then stop.
