# Evals

Deterministic evaluation harness for cognitive-skills. The harness has
no LLM dependency and never calls a model. The host model that
executes a task is whatever the user runs the skill with (Claude in
Cursor, ChatGPT, Gemini, etc.); this folder only scores the outputs
those models produce.

## Layout

```
evals/
├── README.md                  # this file
├── tasks/                     # task definitions (prompt + criteria + voice corpus)
│   ├── engineering-pr-review/
│   │   ├── prompt.md
│   │   ├── criteria.json
│   │   └── voice-corpus.txt
│   ├── product-prd-draft/
│   └── copy-headlines/
├── results/<run-id>/<task>/   # one Markdown file per arm
│   ├── baseline.md            # plain prompt, no skill
│   ├── ceet.md                # prompt + the relevant CEET pack
│   └── generic.md             # prompt + a non-CEET persona ("senior <role>")
└── scripts/
    ├── scoring.py             # length / phrase / section / voice metrics
    └── run.py                 # CLI runner; emits report.{json,md}
```

## How to run

1. Pick a `<run-id>` (e.g. `2026-05-15-claude-opus-4-7`).
2. For each task and each arm, paste the model's reply into
   `evals/results/<run-id>/<task>/<arm>.md`.
3. Score and report:

   ```bash
   python3 evals/scripts/run.py --run-id <run-id>
   ```

   This writes `report.json` and `report.md` next to the inputs.

4. To gate a release on the result:

   ```bash
   python3 evals/scripts/run.py --run-id <run-id> --gate --min-delta 0.05
   ```

   Exits non-zero unless the `ceet` arm beats `baseline` by
   `min-delta` on at least two-thirds of the tasks scored.

## Metrics

Every metric is deterministic. No external service.

- `wordCount` — tokenized word count.
- `lengthWithinBounds` — true if `wordCount` is between
  `criteria.minWords` and `criteria.maxWords`.
- `phraseCoverage` — fraction of `criteria.requiredPhrases` present
  (case-insensitive).
- `sectionCoverage` — fraction of `criteria.requiredSections`
  matched against Markdown headings.
- `voiceAlignment` — TF-cosine (stopwords removed) between the
  output and the task's `voice-corpus.txt`. Read as a *delta* between
  arms, not as an absolute score.
- `compositeScore` — mean of the three coverage scores above.

## Why no LLM judge

A separate judge model would conflate skill behavior with the judge's
preferences. The metrics here measure structure, vocabulary, and
required content — exactly the dimensions a skill is responsible for.
Quality calls beyond that are made by the human reviewing the report.

## Seed run

`results/seed-2026-05-07/` contains synthetic outputs for each arm so
the harness has a self-test fixture. It is not a benchmark — replace
the files there with real model outputs to produce real numbers.
