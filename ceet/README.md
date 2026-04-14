# CEET — Cognitive Engineering Extraction Test

A GitHub Copilot CLI skill that conducts a 70-question deep-interview, builds an **individual cognitive clone** of a software engineer, and generates a fully personalized AI development environment.

## What This Is NOT

- NOT an archetype classifier ("You're a Pragmatic Architect!")
- NOT a bucket sorter (strict / balanced / pragmatic)
- NOT a score-range conditional system (if perfectionism >= 8 then strict_mode)

## What This IS

A cognitive cloning system. It captures one engineer's exact:
- Decision patterns (with their specific thresholds and exceptions)
- Coding style (with their specific naming, typing, error handling)
- Communication voice (their actual mentoring tone, not a template)
- Contradictions (where their answers conflict — the most valuable data)

And generates an AI development environment that behaves as THAT person would.

## Architecture

```
ceet-skill/
  .github/copilot/skills/
    ceet.md                     # Main skill — interview + synthesis + generation
  data/
    questions.json              # All 70 questions with metadata
    profile-schema.json         # JSON Schema for the cognitive profile
  templates/
    agents/                     # 5 agent templates
    skills/                     # 6 skill templates
    commands/                   # 10 command templates
    hooks/                      # 3 hook templates
    rules/                      # 6 global rule templates
    cognitive-profile.md        # Profile output template
```

## How It Works

### Phase 1: Interview (70 questions, 14 sections)
Questions asked in batches of 5, with adaptive probing. Every answer captured verbatim.

| Section | Questions | Covers |
|---------|-----------|--------|
| I. Architectural Philosophy | Q01-Q05 | Persistence, decomposition, state, build/buy, concurrency |
| II. Code Style | Q06-Q11 | Typing, naming, error handling, file org, comments, paradigm |
| III. Methodology | Q12-Q16 | TDD, testing pyramid, git, commits, refactoring |
| IV. Debugging | Q17-Q20 | Silent failures, logging, RCA, dependencies |
| V. Code Review | Q21-Q24 | PR size, nitpicks, mentoring, PM negotiation |
| VI. Personality | Q25-Q30 | Perfectionism, frustration, novelty, focus, flow, legacy |
| VII. Security | Q31-Q36 | Zero trust, secrets, CVEs, validation, XSS/CSRF, crypto |
| VIII. Performance | Q37-Q42 | Latency, memory leaks, caching, N+1, GC, render |
| IX. Database | Q43-Q48 | ACID/BASE, indexing, migrations, ORM, partitioning, time/money |
| X. Infrastructure | Q49-Q53 | Pipeline, deployment, IaC, alerting, ephemeral envs |
| XI. Chaos Engineering | Q54-Q58 | Idempotency, retry, DLQ, degradation, rate limits |
| XII. Tooling | Q59-Q62 | Editor, local env, scripting, mocking |
| XIII. Meta-Cognition | Q63-Q66 | Uncertainty, escalation, crisis, knowledge evolution |
| XIV. Stress Tests | Q67-Q70 | Hostile fork, ghost bug, PM pushback, handover |

### Phase 2: Individual Cognitive Synthesis
- Store ALL raw responses as ground truth
- Synthesize identity: cognitive signature, core values, decision framework, communication voice, frustration triggers, blind spots, contradictions
- Generate behavioral directives across 15 domains — in the engineer's voice, traceable to specific questions
- Calculate composite scores as visualization-only metadata (NEVER drives behavior)

### Phase 3: Configuration Generation
Templates use directive placeholders injected with the engineer's synthesized words. Zero conditional logic. Every generated file is unique to the individual.

**Output: 30 files** — 5 agents, 6 skills, 10 commands, 3 hooks, 6 global rules, cognitive profile (JSON + MD)

## Design Principles

1. **Verbatim over interpretation** — Store their exact words, not your summary
2. **Contradictions are features** — Tensions between answers reveal context-dependent thinking
3. **Directive injection over conditionals** — Templates inject the person's words, not branching logic
4. **Scores are metadata, not behavior** — Composite scores visualize, they never decide
5. **Every rule is traceable** — Every directive references the questions it was synthesized from
