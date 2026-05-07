# Changelog

All notable changes to **cognitive-skills** are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- `CHANGELOG.md` documenting release history.
- `schemaVersion` field on every artifact contract emitted by the Jira pipeline
  (`TicketAnalysis`, `BusinessQuestionSet`, `FunctionalContract`, `BaseBranchPlan`)
  and on `cognitive-profile.md` template front-matter. Versioning rules are
  documented in `docs/contracts.md` (planned).
- `unmappedAnswers` array on the FunctionalContract so answers without a
  declared category mapping are preserved instead of silently dropped.
- `--baseline-budget` / `--signal-budget` flags on `generate-questions`,
  reserving slots for universally required P0 templates and signal-driven
  templates separately.
- `--max-comments` flag on `fetch-issue`. Comments are now fetched via the
  paginated `/issue/{key}/comment` endpoint instead of relying on the first
  page returned by `/issue/{key}`.
- One-line docstrings on every public function in `jira_pipeline_cli.py`.

### Changed
- `infer_ambiguity_level` now returns a dict with `level`,
  `constraintDensity`, `ambiguityMarkers`, and the signal breakdown — not just
  a HIGH/MEDIUM/LOW bucket. Density is normalized per 100 words and the level
  is derived from both constraint density and explicit ambiguity markers
  (`tbd`, `?`, `we should`, `maybe`, `not sure`, ...).
- `should_include_template` and the wider `generate-questions` pipeline now
  delegate selection to `select_required_templates`, which fills a baseline
  budget (default 4) of universally required P0 templates and a signal budget
  (default 6) of signal-driven templates, with overflow into remaining P0/P1
  templates if signals fail to fill the pool.
- `resolve-contract` defaults every list-shaped field to the plural extractor
  (`extract_answers_by_category`) so additional answers per category are
  preserved. `businessObjective` and `functionalScope` remain singular by
  design, with comments explaining why.
- `BaseBranchPlan.branchName` renamed to `BaseBranchPlan.proposedBranchName`.
  The CLI never creates a branch — the engineer creates it manually after
  reviewing the plan.

### Tests
- `pytest` + `hypothesis` test suite under `tests/jira/` covering inference,
  template selection, `JiraClient` pagination, branch sanitization (property
  tests), full-pipeline snapshots, CLI smoke tests, and CLI helpers. 41 tests
  at 84% line coverage on `jira_pipeline_cli.py`.
- GitHub Actions workflow `.github/workflows/test.yml` running pytest on
  Python 3.10/3.11/3.12 with a `--cov-fail-under=70` gate.

### Refactored
- Extracted Jira HTTP transport into a `JiraClient` class so tests can inject
  fakes; `jira_get` is kept as a thin backward-compatible wrapper.

### LLM-augmented mode
- New CLI subcommand `merge-llm-suggestions` that takes a host-model
  refinement patch (`suggestions.json`) and merges it into a
  `TicketAnalysis`. Allowlist-validated: only declared keys
  (`businessGoal`, `functionalEntities`, `userActions`, ...) are
  accepted. Lists are unioned, scalars are replaced with the rule-based
  value preserved under `_llmAugmentation.ruleBasedSnapshot`.
- New prompt template
  `jira-agentic-requirements-pipeline/templates/llm-augmentation-prompt.md`
  for the host model to follow when refining an analysis. The skill
  itself does not call any LLM API — the model invoking the skill does.

### Meta-skills
- `autodiscover/scripts/detect.py`: deterministic CEET detector. Scans
  the workspace for `ceet-*` folders, classifies each as initialized
  (templates present and/or generated pack under `examples/ready-to-use/`),
  matches the user request against per-role keywords (word-boundary
  matching, no substring false positives), and emits a JSON report
  with `detectedCEETs`, `initializedCEETs`, `scoring`, and
  `recommendation`.
- `ceet-sub-agent-orchestration/scripts/validate_handoff.py`: enforces
  the new `OrchestrationPlan` and `SubAgentResult` JSON contracts
  (documented in `docs/contracts.md`). Plan validation rejects
  duplicate task ids, forward dependencies, and missing artifacts;
  result validation rejects unknown statuses, completed-without-
  artifacts, and unknown artifact kinds.
- `impersonator/scripts/validate_pack.py`: enforces the impersonator's
  provenance contract before a generated pack ships. Verifies the
  Simulation Notice banner, a minimum number of evidence rows, the
  absence of unfilled `{directives.*}` placeholders, and that every
  directive cited in the cognitive profile is also cited in
  `evidence-map.md`. The published Netflix pack passes; an unfilled
  starter pack fails.

### Marketing & discoverability
- README hero rewritten: single-sentence value proposition, 60-second
  example block at the top, `What's new` summary linking the
  changelog. Redundant `Try it instantly` and `Quick Start` sections
  consolidated into one `Three ways to use this repo` section.
- Before/after table now shows real numbers from the eval harness'
  seed run (composite deltas of +0.27 / +0.03 / +0.23 for ceet vs
  baseline across the three benchmark tasks). Synthetic-output
  caveat called out explicitly.
- New `examples/ready-to-use/demo-jira-pipeline.sh`: a self-contained
  90-second demo of the Jira pipeline against a synthetic ticket
  fixture. No Jira credentials required. Records cleanly with
  `asciinema rec`.
- New `docs/launch/launch-post.md` (long-form post + HN/Lobsters/
  Reddit variants) and `docs/launch/distribution-plan.md` (where to
  submit, in what order, with a pre-launch checklist).

### Eval harness
- Deterministic eval harness under `evals/`. No LLM judge: the host
  model produces outputs (saved as Markdown per arm), and
  `evals/scripts/run.py` scores them with stdlib-only metrics:
  word/section count, required-phrase coverage, required-section
  coverage, and TF-cosine voice alignment against a per-task corpus.
- Three task definitions: `engineering-pr-review` (Postgres rename
  migration), `product-prd-draft` (admin 2FA), `copy-headlines`
  (B2B observability for SREs).
- Release-gate flag: `run.py --gate --min-delta 0.05` exits non-zero
  unless `ceet` beats `baseline` by `min-delta` on at least two-thirds
  of the tasks scored.
- Synthetic seed outputs under `evals/results/seed-2026-05-07/` so the
  harness self-tests on a checkout. The seed run shows ceet beating
  baseline on 3/3 tasks (deltas 0.03 / 0.23 / 0.27).

### Documentation
- New `Quick start` section in `jira-agentic-requirements-pipeline/SKILL.md`
  with copy-pastable env vars and the six pipeline commands.
- New `EXAMPLES.md` walking through three end-to-end runs (clean ticket,
  near-empty ticket, marker-dominated ticket) using the test fixtures.
- New `TROUBLESHOOTING.md` covering 401s, the `customfield_10011` epic
  field gotcha, comment cap warnings, and stale state files.
- New repo-level `docs/contracts.md` centralizing the artifact contracts
  and the SemVer-based versioning policy.
- README now shows the top-level CLI `--help` output and links to the
  skill's docs.

### Removed
- Duplicated `CONTIBUTING.md` (typo). Canonical guide is `CONTRIBUTING.md`.

## [1.1.1] - 2026-04-16

### Changed
- Replaced Spanish text with English across documentation.

## [1.1.0] - 2026-04-16

### Added
- Autodiscover skill with CEET initialization gating.
- Autodiscover flow and sub-agent orchestration skill.
- Realistic examples for many CEET skills and roles.

## [1.0.0] - 2026-04-16

### Added
- Initial public release of the Cognitive Extraction Engine Toolkit.
- 15 role-specific CEETs with interview scripts, templates, and examples.
- `impersonator` skill for simulated CEET initialization from public evidence.
- Jira agentic requirements pipeline (rule-based core).
- Methodology, synthesis rules, tool-integration, and extending guides.
