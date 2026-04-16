# Impersonator Mapping Protocol

This protocol defines how external evidence is converted into CEET directive values.

## 1. Parse target directive surface

1. Read `ceet-<role>/templates/cognitive-profile.md`.
2. Extract every `{directives.domain.field}` key.
3. Build a mapping worksheet with columns:
   - `directive_key`
   - `candidate_evidence`
   - `inference`
   - `confidence`
   - `notes`

## 2. Collect evidence

## Public Figure Mode

Allowed evidence:

1. Public talks/interviews.
2. Public writing/posts/books.
3. Publicly documented decisions and actions.

Disallowed:

1. Rumors/gossip.
2. Unsourced claims.
3. Fabricated quotes.

## Repository Author Mode

Allowed evidence:

1. Commit messages.
2. Diff patterns across authored changes.
3. File-level coding style and architecture tendencies.
4. PR review comments attributable to the author (if accessible).

Disallowed:

1. Inference from private HR context.
2. Non-work personal trait profiling.

## 3. Infer directive values

For each directive:

1. Prefer repeated signals over single anecdotes.
2. Keep role-context fit explicit.
3. Use work-language, not personality labels.
4. If evidence is weak, set `unknown`.

Confidence rubric:

1. `high` — multiple converging sources/patterns.
2. `medium` — partial evidence with plausible inference.
3. `low` — thin signal; keep conservative wording.

## 4. Generate artifacts

1. Populate `cognitive-profile.md` first.
2. Generate role artifact files from target template set.
3. Keep placeholders out of final drafts whenever evidence exists.
4. Preserve `unknown` where evidence is insufficient.

## 5. Provenance requirements

Create `evidence-map.md` in output folder with:

1. Directive key.
2. Evidence summary.
3. Confidence.
4. Rationale.
5. Gaps/unknowns.

## 6. Mandatory simulation label

Every generated file must include:

> **Simulation Notice:** This profile is inferred from external evidence, not from a first-person CEET interview. Treat as a draft hypothesis, not ground truth.
