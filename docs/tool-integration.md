# Tool Integration Guide

> CEET outputs are plain markdown + JSON. This guide shows how to load them into popular AI assistants. The source of truth is always the portable output; the per-tool adapters below are convenience wrappers.

---

## Universal Output Bundle

Every CEET run produces:

```
{output_dir}/
├── cognitive-profile.json       # Structured profile (the ground truth)
├── cognitive-profile.md         # Human-readable version of the profile
├── agents/                      # Per-persona behavioral files
│   ├── {agent-1}.md
│   └── ...
├── skills/                      # Focused capability files
├── commands/                    # Named workflow shortcuts
├── rules/                       # Global principles applied everywhere
├── hooks/                       # (Engineering roles only) automation triggers
└── _source_map.md               # Every artifact's Q-ID references
```

These files are **plain text**. Any AI that accepts context can consume them.

---

## Claude (claude.ai, API, Desktop)

**Easiest:** create a Claude Project and add all of `{output_dir}/` as project knowledge.

Alternative: paste `cognitive-profile.md` + relevant `rules/*.md` into the system prompt or user instructions.

For long-running work, add the rules file inline at the start of each conversation:

```
> I am loading my cognitive profile. Please use these directives as my default working context.
>
> [paste contents of rules/coding-standards.md here]
> [paste contents of cognitive-profile.md here]
```

---

## ChatGPT (chat.openai.com, Custom GPTs)

**Custom Instructions:**
- "What would you like ChatGPT to know about you?" → paste the `identity` section of `cognitive-profile.md`
- "How would you like ChatGPT to respond?" → paste the `directives.communication_voice` + one rules file

**Custom GPT:**
- Add `cognitive-profile.json` and all `rules/*.md` as Knowledge files
- In the GPT's Instructions, reference: "Before responding, consult cognitive-profile.json for my decision framework and rules/ for my standards."

---

## Cursor

Place role-appropriate files in `.cursor/rules/`:

```
.cursor/rules/
├── coding-standards.mdc         # from rules/
├── architecture-principles.mdc  # from rules/ (engineering roles)
├── communication.mdc            # from rules/
└── profile.mdc                  # cognitive-profile.md
```

Add the YAML front-matter Cursor expects:

```
---
description: "Individual cognitive profile — behavioral directives"
globs: ["**/*"]
alwaysApply: true
---

{paste content here}
```

---

## GitHub Copilot

Place files in `.github/copilot/`:

```
.github/copilot/
├── instructions.md              # rules/ merged
├── agents/
├── skills/
└── profile.md
```

Reference `.github/copilot/instructions.md` in your repo's Copilot configuration.

---

## Windsurf

Place rules in `.windsurfrules` or `.windsurf/rules/`:

```
.windsurf/rules/
├── profile.md
├── communication.md
└── {role-specific}.md
```

---

## Aider

Use `--read` to pass profile files on startup:

```bash
aider --read cognitive-profile.md --read rules/coding-standards.md
```

Or create `.aider.conf.yml`:

```yaml
read:
  - cognitive-profile.md
  - rules/coding-standards.md
  - rules/architecture-principles.md
```

---

## Gemini / Google AI Studio

Paste `cognitive-profile.md` into the System Instructions field. For per-artifact loading, create separate Gems (system-instructed assistants) per agent in `agents/`.

---

## Generic / Custom Agents / Open-Source Tools

For any system that accepts a system prompt or context injection:

1. Start with: "You are working with {name}. Load their cognitive profile below and follow these directives for every response."
2. Concatenate `cognitive-profile.md` + all `rules/*.md`
3. For task-specific work, append the relevant `agents/{agent}.md` or `skills/{skill}.md`

---

## Non-Engineering Role Notes

For business roles (marketing, sales, financial, copywriter, etc.), there are no `hooks/` — those are engineering-only automation triggers. Everything else is the same pattern:

- Load `cognitive-profile.md` as the baseline identity
- Load the relevant `agents/*.md` for the specific sub-task (e.g., `agents/pricing-advisor.md`, `agents/headline-writer.md`)
- Load `rules/*.md` as always-on constraints
- Invoke `commands/*.md` as named workflows when relevant

---

## Updating

When the profile changes (via re-interview or directive edit):

1. Regenerate the bundle
2. Replace the files in your AI tool's context source
3. Most tools re-read on next session; some require explicit re-sync

A `profile-changelog.md` is produced on re-runs so you can see what changed.
