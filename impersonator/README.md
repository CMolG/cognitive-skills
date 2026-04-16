# Impersonator

Independent **skill** for bootstrapping any CEET role pack from external evidence instead of interview responses. Runs inside any AI assistant that loads Anthropic-style skills — no Python, CLI, or binaries required.

## What it does

Given a `target_role` and a subject, it generates a **simulated full CEET draft pack** (cognitive profile + agents + skills + commands + rules + hooks where applicable), plus an `evidence-map.md` that documents how each directive was derived and at what confidence level.

## Modes

1. **Public Figure Mode**
   - Input: public figure or public engineering voice (e.g., Netflix Tech Blog).
   - Sources: public, documented materials only (blog posts, talks, papers, public code).

2. **Repository Author Mode**
   - Input: repository + author identity. Operator must confirm authorization.
   - Sources: commit history, diffs, authored code patterns, review traces when available.

## Output location

Generated content goes to:

`examples/ready-to-use/<output-slug>/`

This keeps canonical role templates unchanged and produces reviewable, copy-paste-ready draft packs that downstream users can drop into Claude, ChatGPT, Cursor, Copilot, Gemini, or any AI tool.

## Output files

1. `cognitive-profile.md`
2. `agents/*.md`
3. `skills/*.md`
4. `commands/*.md`
5. `rules/*.md`
6. `hooks/*.md` (only if target role has hooks)
7. `evidence-map.md` (directive-to-evidence mapping with `high` / `medium` / `low` confidence)
8. `README.md` (pack usage instructions for end users)

## How to run it

1. Open this folder's `SKILL.md` in your AI assistant (or ensure skills auto-load from the repo).
2. Ask the assistant to run the `impersonator` skill with:
   - `target_role` — e.g., `ceet-backend-engineer`
   - `mode` — `public_figure` or `repo_author`
   - Subject identifier(s) per mode
   - `output_slug` — e.g., `backend-netflix-tech-blog`

## Example output

See [`../examples/ready-to-use/backend-netflix-tech-blog/`](../examples/ready-to-use/backend-netflix-tech-blog/) — a full backend-engineer pack generated from Netflix's public engineering voice.

## Safety and quality

1. Every output file contains a simulation disclaimer.
2. Sparse evidence is marked `unknown`.
3. Confidence is explicit (`high|medium|low`) per directive.
4. No claims of true identity or endorsement.
5. Repository-author mode requires operator authorization confirmation.

## Related docs

1. [`docs/mapping-protocol.md`](docs/mapping-protocol.md) — how evidence is mapped to directives.
2. [`docs/safety-policy.md`](docs/safety-policy.md) — refusal criteria and sensitive-trait handling.
