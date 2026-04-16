---
name: ceet-backend-engineer
description: Cognitive Extraction Engine for backend engineers. Use whenever a user wants to "clone" a backend engineer's judgment, capture how a senior server/API/data engineer thinks, build a personalized AI coding environment for backend work, or produce a portable cognitive profile of a backend practitioner. Trigger on phrases like "extract my backend style", "build an AI setup that codes like our staff backend engineer", "interview me about backend engineering", "make me a backend cognitive clone", or any request to distill backend engineering judgment into a reusable AI configuration. Outputs are tool-agnostic (Claude, ChatGPT, Cursor, Copilot, Gemini, etc.).
---

# CEET — Backend Engineer

## What this skill does

Conduct a structured interview with a backend engineer, extract the cognitive patterns behind their judgment, and produce two tool-agnostic artifacts:

1. **`cognitive-clone.md`** — how this person thinks about backend work.
2. **`ai-environment.md`** — a system-prompt-ready configuration usable in any AI tool.

## When to use

- The user says "build a backend cognitive clone", "extract how I think about backend", or "interview me so any AI can code like me".
- The user wants to onboard an AI assistant onto their backend codebase in *their* style, not a generic one.
- The user wants a portable artifact they can reuse across Claude, ChatGPT, Cursor, Copilot, Gemini, etc.

## Run order

1. **Read** `interview/questions.md`. Do not dump all questions at once — ask them conversationally, grouped by theme, and dig into specifics when an answer is vague.
2. **Extract.** As the interview progresses, keep private notes tagged by theme: `#mental-model`, `#heuristic`, `#procedure`, `#quality`, `#anti-pattern`, `#vocabulary`.
3. **Probe contradictions.** When the person says "it depends" or gives two answers, ask *what the depending variable is*. Those are usually the most valuable heuristics.
4. **Synthesize.** Fill in [`../_shared/templates/cognitive-clone.template.md`](../_shared/templates/cognitive-clone.template.md) using their own words wherever possible.
5. **Activate.** Transform the clone into [`../_shared/templates/ai-environment.template.md`](../_shared/templates/ai-environment.template.md). Save both into `templates/` (the user can move/rename later).
6. **Hand off.** Point the user at [`../_shared/prompts/activation-guide.md`](../_shared/prompts/activation-guide.md) so they can install the output in whichever AI tool they use.

## Backend-specific things to listen for

These are the cognitive signals that distinguish a senior backend engineer from a textbook one. Use them as prompts when the interview drifts generic:

- **Data integrity instincts.** Uniqueness, ordering, idempotency, exactly-once vs at-least-once thinking. How do they design for partial failure?
- **Blast radius thinking.** When they ship, what's their mental map of *what else could break*?
- **Invariant mindset.** Do they name invariants explicitly? Where do they enforce them (DB, app, queue)?
- **Latency vs consistency tradeoffs.** Concrete examples of when they picked each.
- **API shape judgment.** REST vs RPC vs event-driven — when and why. Versioning philosophy.
- **Storage choice heuristics.** Postgres vs Dynamo vs Kafka vs S3 — their mental decision tree.
- **Observability reflexes.** What do they instrument before deploying? What metric do they watch after?
- **Refactoring taste.** When they say "this needs a refactor," what's the signal?
- **Review lens.** What do they flag in other people's PRs?
- **Incident scar tissue.** Every senior backend engineer has 2-3 incidents that permanently changed how they code. Ask for them.

## Synthesis guardrails

- Keep the person's **own vocabulary**. If they say "poison message" instead of "bad event", the clone says "poison message".
- Distinguish **heuristics** (rules with exceptions) from **anti-patterns** (never do X).
- Quote specific examples inline — "rejects PRs that mutate args without a `_mut` suffix" beats "prefers immutability".
- Flag contradictions in section 8 ("Notes & Open Questions") rather than hiding them.

## Output location

Save both generated files to `templates/` in this folder (`cognitive-clone.md`, `ai-environment.md`). If the user wants them elsewhere, copy — don't move.

## When to stop

The interview is complete when the user can read back their own cognitive clone and say "yeah, that sounds like me." If they say "close, but I'd never say X that way," go back and re-interview the relevant section.
