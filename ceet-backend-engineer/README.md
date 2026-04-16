# CEET — Backend Engineer

Interview a backend engineer, extract their cognitive patterns, and produce a portable AI environment that codes in their style — in any AI tool.

## Who this is for

- **Staff / senior backend engineers** who want an AI assistant that matches their judgment instead of defaulting to generic patterns.
- **Engineering managers** trying to scale a specific engineer's code-review standards across the team via AI.
- **Founders / tech leads** onboarding contractors or junior engineers, who want a reusable "this is how we think about backend" artifact.

## What you'll produce

Two files, both plain Markdown, both tool-agnostic:

- `templates/cognitive-clone.md` — a readable document of how this engineer thinks about backend work.
- `templates/ai-environment.md` — a system prompt you can paste into Claude, ChatGPT, Cursor, Copilot, Gemini, or any tool that accepts a system prompt or rules file.

## How to run it

If your AI tool supports Anthropic-style skills, the `SKILL.md` in this folder will trigger automatically. Otherwise, open `SKILL.md` and `interview/questions.md` and walk through them as a guided interview.

Time required: **30–60 minutes** for a high-quality extraction. You can split the interview across sessions.

## How to install the output in your AI tool

See [`../_shared/prompts/activation-guide.md`](../_shared/prompts/activation-guide.md) for per-tool installation snippets (Claude Projects, ChatGPT GPTs, `.cursorrules`, `.github/copilot-instructions.md`, Gemini Gems, etc.).

## What makes this CEET different from the others

Backend engineering is dominated by *invariant thinking*, *failure-mode awareness*, and *blast-radius reasoning*. The interview questions in this CEET are tuned to surface those specifically — not the more visual/structural concerns of frontend, nor the infrastructure concerns of SRE, nor the metric-first concerns of data.
