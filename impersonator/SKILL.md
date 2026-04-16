---
name: impersonator
description: Independent skill that initializes any CEET role pack by simulating a public figure or a repository author from external evidence (no interview). Use when a user wants a draft cognitive clone and full artifact pack for a known person based on public data or commit/code history.
---

# Impersonator Skill

## Purpose

Generate a **simulated CEET artifact pack** for any existing `ceet-<role>` folder without running a first-person interview.

This skill supports two modes:

1. **Public Figure Mode** — infer from public, well-documented sources.
2. **Repository Author Mode** — infer from an author's commit/code history in a repository the operator can access.

## Inputs

Required:

1. `target_role` — one of the existing `ceet-*` folders.
2. `mode` — `public_figure` or `repo_author`.

Mode-specific:

1. `public_figure` (for `public_figure` mode), optional `focus_context`.
2. `repo`, `author` (for `repo_author` mode), optional `since`/`until`.

## Non-negotiable output label

Every generated file MUST include this banner near the top:

> **Simulation Notice:** This profile is inferred from external evidence, not from a first-person CEET interview. Treat as a draft hypothesis, not ground truth.

## Run order

1. **Validate role.** Confirm `target_role` exists and contains `templates/`.
2. **Load directive structure.** Parse `ceet-<role>/templates/cognitive-profile.md` to detect expected `{directives.domain.field}` keys.
3. **Collect evidence.**
   - `public_figure`: documented speeches, interviews, writing, public decisions.
   - `repo_author`: commit messages, diffs, authored files, review footprint (if available).
4. **Build evidence matrix.** For each directive field, map evidence + confidence (`high|medium|low`).
5. **Fill directives carefully.**
   - If confidence is low or evidence is sparse, write `unknown` and explain why.
   - Do not fabricate precision.
6. **Generate full draft pack** matching the target role artifact shape:
   - `cognitive-profile.md`
   - `agents/*`
   - `skills/*`
   - `commands/*`
   - `rules/*`
   - `hooks/*` (if role has hooks)
7. **Write output under examples, not canonical templates:**
   - `ceet-<role>/examples/impersonations/<subject-slug>/`
8. **Attach provenance index** in the output folder:
   - `evidence-map.md` listing every populated directive with source rationale and confidence.

## Mapping rules

1. Map evidence to **behavioral directives**, not biographical trivia.
2. Prefer repeated patterns over one-off anecdotes.
3. Use direct quotes only when verifiable.
4. Keep role fit explicit: if evidence does not fit the role context, mark it as uncertain.

## Refusal and safety rules

1. Refuse requests to present generated output as verified identity or endorsement.
2. Refuse private-person profiling or doxxing-like tasks.
3. For repository mode, proceed only when operator confirms authorization.
4. Avoid sensitive trait inference (medical, political, religion, sexuality, etc.) unless explicitly and publicly work-relevant and necessary.
5. Never claim certainty where evidence does not support it.

## Completion criteria

A run is complete only when:

1. Full target-role artifact set is generated in `examples/impersonations/<subject-slug>/`.
2. Every file contains the Simulation Notice.
3. `evidence-map.md` exists and covers all populated directive fields.
4. Unknown/low-confidence areas are explicit.
