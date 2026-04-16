# Ready-to-use Pack — Backend Engineer (Netflix Tech Blog voice)

> **Simulation Notice:** This pack is inferred from Netflix public engineering materials (Tech Blog, conference talks). It is a simulated CEET profile, not a first-person interview. Treat as a draft hypothesis and review before production use.

A complete, copy-paste-ready CEET artifact pack for the **Backend Engineer** role, built from the public engineering voice of Netflix (reliability-first, progressive delivery, explicit invariants, safe rollback).

## What's in here

| File / folder | Purpose |
|---|---|
| `cognitive-profile.md` | Full cognitive profile (identity, values, decision framework, directives) |
| `agents/` | 5 role-specific agents (architect, code-reviewer, debugger, incident-responder, pair-programmer) |
| `skills/` | 6 role-specific skills (code-style-enforcer, database-reviewer, documentation-generator, performance-profiler, security-auditor, test-writer) |
| `commands/` | 10 slash commands (/architect, /debug, /handover, /incident, /migrate, /rca, /refactor, /review, /security-check, /test) |
| `rules/` | 6 global rule files (architecture, coding, communication, operational, security, testing) |
| `hooks/` | 3 git lifecycle hooks (pre-commit, pre-push, post-merge) |
| `evidence-map.md` | Directive-to-evidence mapping with confidence (`high` / `medium` / `low`) |

## How to use

### Fastest path — paste the profile into any AI tool

1. Copy the contents of [`cognitive-profile.md`](cognitive-profile.md).
2. Paste it into:
   - Claude project instructions, or
   - ChatGPT custom instructions / Custom GPT knowledge, or
   - `.cursorrules` at your repo root, or
   - `.github/copilot-instructions.md`, or
   - Any other AI tool's system prompt.
3. Ask it something like: *"Review this pull request for a database migration that renames `users.email` to `users.primary_email`."*

### Full environment — load the whole pack

Copy the folder structure into your AI tooling's native layout:

- Claude Code / Claude Desktop: `agents/`, `skills/`, `commands/`, `rules/`, `hooks/` map directly to your project's corresponding directories.
- Cursor: merge `rules/` into `.cursorrules`; keep the rest as reference.
- Copilot: merge `rules/` into `.github/copilot-instructions.md`.

## Why this pack is sharper than a generic backend prompt

A generic "backend engineer" prompt gives generic advice. This pack encodes a specific operator voice:

- Migrations get **expand/contract phases**, dual-write windows, and explicit rollback gates — not just "add tests".
- Reviews block on **invariant weakening** and **missing rollback strategy**, not style.
- Retries are **bounded with jitter and deadlines** — no retry storms.
- Alerts **page on user-impacting symptoms only**; predictive signals go to tickets.
- Caching requires **explicit invalidation + staleness policy**; no hidden consistency assumptions.

Full evidence mapping for each directive is in [`evidence-map.md`](evidence-map.md).

## Regenerating or producing a different voice

This pack was produced by the [`impersonator`](../../../impersonator/) skill in **public-figure mode** targeting `ceet-backend-engineer`. To generate an equivalent pack for a different voice (another company's public engineering writing, or a repo author), invoke the `impersonator` skill in your AI assistant with your chosen target and mode.
