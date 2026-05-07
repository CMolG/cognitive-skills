# cognitive-skills: encoding human judgment as portable AI artifacts

> Draft launch post. The author is Carlos. Adapt the tone and length to
> the destination (HN comment-thread voice, Lobsters, r/MachineLearning,
> r/programming, Lobste.rs, blog post, dev.to). Keep the headline,
> swap the body framing as needed.

---

A common pattern shows up when a team adopts an AI assistant: the
junior engineer's review and the staff engineer's review converge to
the same broad checklist, because both are mediated by the same
generic system prompt. The model has no idea what the staff engineer
*notices first*. It treats every PR as a fresh case.

I built **cognitive-skills** as a way to encode the part of judgment
that does not survive a job description: the heuristics, the things a
practitioner pays attention to, the failure modes they watch for, what
"good" actually looks like to them. The output is a `cognitive-profile.md`
plus a few support artifacts — plain Markdown and YAML, no SDK, no API
key, no vendor lock-in. You paste it into Claude, ChatGPT, Cursor,
Copilot, Gemini, or whatever you are running, and the assistant starts
behaving like the person you interviewed.

## What's in the repo

- **15 role-specific Cognitive Extraction Engines (CEETs).** Backend,
  frontend, devops/SRE, data, product, UX, UI, copy, marketing, sales,
  customer success, finance, legal, people-ops, founder/CEO. Each one
  is a structured interview + synthesis kit + a templates/ folder.
- **A production-grade Jira requirements pipeline.** Six commands that
  turn ambiguous Jira tickets into validated functional contracts with
  traceability. Rule-based core (free, offline) plus an LLM-augmented
  refinement step where the host model patches the analysis through an
  allowlist-validated `merge-llm-suggestions` command. 85% test
  coverage on the CLI.
- **A deterministic eval harness.** Three benchmark tasks
  (engineering PR review, product PRD draft, copy headlines), no judge
  model. The metrics are required-phrase coverage, required-section
  coverage, and TF-cosine voice alignment vs a per-task corpus.
  Release-gate flag: `--gate --min-delta 0.05` exits non-zero unless
  `ceet` beats `baseline` on at least 2/3 tasks.
- **Three meta-skills.** `autodiscover` for routing a request to the
  right CEET, `ceet-sub-agent-orchestration` with validated
  `OrchestrationPlan` and `SubAgentResult` JSON contracts, and
  `impersonator` for drafting a CEET pack from public evidence — with
  a provenance enforcer that refuses to publish a pack whose
  cognitive-profile cites directives missing from `evidence-map.md`.

## Why no LLM in the skills themselves

A skill in this repo is a Markdown file plus (optional) deterministic
scripts. The LLM is whatever model the user invokes the skill with —
Claude in Cursor, ChatGPT, Gemini, etc. The repo never calls a model.
That is deliberate: it keeps the skills portable across hosts, keeps
the deterministic core free and reproducible, and avoids the "this
benchmark is mostly measuring my judge model" problem.

The Jira pipeline's "agentic" mode is exactly this: rule-based
discovery runs first, the host model produces a JSON patch refining
the analysis, the CLI validates the patch against an allowlist, and
the merged output keeps the rule-based version under
`_llmAugmentation.ruleBasedSnapshot` for provenance. No SDK, no API
key, no model-specific glue.

## Why no separate judge model in the eval

Same reason. The metrics in `evals/scripts/scoring.py` are stdlib-only
and reproducible: word count, required-phrase coverage,
required-section coverage, TF-cosine voice alignment. They measure
exactly what a CEET pack is responsible for — structure, vocabulary,
required content. Quality calls beyond that are made by the human
reading the report.

The seed run in `evals/results/seed-2026-05-07/` shows `ceet` beating
`baseline` on 3/3 tasks with composite deltas of +0.27, +0.03, +0.23.
Those are synthetic outputs — written by hand to self-test the harness,
not as a benchmark. Replace them with your own model's outputs and
re-run; the harness produces the same report format.

## Where this came from

The framing borrows from a few places: cognitive task analysis from
human-factors research, the "interview the expert" pattern from
knowledge-engineering, and the more recent "skills" architecture
(Claude skills, Cursor rules, custom GPTs). The contribution is the
combination: a fixed loop (interview → extract → synthesize → activate),
fixed contract shapes, deterministic enforcement on the things you can
enforce deterministically, and an explicit refusal to bind to any
specific model.

## What I want feedback on

1. The Jira pipeline is the most operational piece. If you have a Jira
   instance and an opinion on how the rule-based ambiguity scoring
   over-fires or under-fires, the test fixtures under
   `tests/jira/fixtures/` are easy to extend.
2. The eval harness is intentionally austere. If you have argued for
   or against LLM-as-judge in your own work, I would like to hear how
   you would design a stronger deterministic eval here.
3. The CEET portfolio is 15 roles, which is wide. The original plan
   suggested cutting it to 6+2 specialized skills. I kept the 15 and
   would like to know if anyone reads, for example, `ceet-people-ops`
   or `ceet-legal-compliance` and finds the depth lacking.

Repo: <https://github.com/CMolG/cognitive-skills>.

Changelog: [`CHANGELOG.md`](https://github.com/CMolG/cognitive-skills/blob/main/CHANGELOG.md).

---

## HN-comment-thread variant

> Built a small toolkit for encoding human judgment as portable AI
> artifacts — Markdown + YAML cognitive profiles you paste into Claude,
> ChatGPT, Cursor, Gemini, etc. Includes a Jira requirements pipeline
> with 85% test coverage and a deterministic eval harness (no LLM
> judge). Seed run shows the CEET arm beating baseline by +0.23 to +0.27
> composite on engineering and copy tasks. Repo:
> <https://github.com/CMolG/cognitive-skills>.

## r/programming variant

> Show r/programming: a toolkit that turns a domain expert's interview
> into a portable cognitive clone. Sample use case: paste the
> backend-netflix-tech-blog pack into Cursor, ask "review this PR for
> a Postgres column rename migration", and the assistant frames the
> review in expand/contract phases instead of "add tests, check
> rollback". Includes a production-grade Jira pipeline as the flagship
> skill. Free, no API keys, no vendor lock-in.

## Lobsters variant

> Project: cognitive-skills. Encodes a person's role-specific judgment
> as a portable Markdown + YAML system prompt. Ships with 15 role
> templates, a Jira requirements pipeline (rule-based + optional
> host-model refinement), and a deterministic eval harness with no
> LLM judge. The skills never call a model — the host you load them
> in is the model.
