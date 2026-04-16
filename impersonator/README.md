# Impersonator

Independent skill for bootstrapping any CEET role from external evidence instead of interview responses.

## What it does

Given a `target_role` and a subject, it generates a **simulated full CEET draft pack** (cognitive profile + agents/skills/commands/rules/hooks where applicable).

## Modes

1. **Public Figure Mode**
   - Input: public figure name (example: Bill Gates), optional context window.
   - Sources: public, documented materials only.

2. **Repository Author Mode**
   - Input: repository + author identity.
   - Sources: commit history, diffs, authored code patterns, review traces when available.

## Output location

Generated content goes to:

`ceet-<target-role>/examples/impersonations/<subject-slug>/`

This keeps canonical role templates unchanged and produces reviewable drafts for initialization.

## Output files

1. `cognitive-profile.md`
2. `agents/*.md`
3. `skills/*.md`
4. `commands/*.md`
5. `rules/*.md`
6. `hooks/*.md` (only if target role has hooks)
7. `evidence-map.md` (directive-to-evidence mapping with confidence)

## Safety and quality

1. Every output file contains a simulation disclaimer.
2. Sparse evidence is marked `unknown`.
3. Confidence is explicit (`high|medium|low`).
4. No claims of true identity or endorsement.
5. Repository-author mode requires operator authorization confirmation.

## Related docs

1. [`docs/mapping-protocol.md`](docs/mapping-protocol.md)
2. [`docs/safety-policy.md`](docs/safety-policy.md)
