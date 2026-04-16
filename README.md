# CEET — Cognitive Extraction Engine Toolkit

A family of role-specific **Cognitive Extraction Engines**. Each CEET is a structured interview + synthesis skill that:

1. **Interviews** a person working in a given role with deep, role-specific questions.
2. **Extracts** their cognitive patterns — how they decide, what they pay attention to, what failure modes they watch for, which heuristics they use, and what "good" looks like to them.
3. **Synthesizes** an **Individual Cognitive Clone** — a portable artifact describing how *this specific person* thinks in *this specific role*.
4. **Generates** a **Personalized AI Environment** — prompts, rules, and guardrails that make any AI assistant mimic that person's judgment on their real work.

> CEETs produce **tool-agnostic outputs**. The generated cognitive clone and AI environment work in Claude, ChatGPT, Cursor, Copilot, Gemini, Perplexity, or any other AI tool — because the artifacts are plain Markdown + YAML, not wrapped in any vendor's proprietary format.

## The 15 roles

| Folder | Role | Focus |
|---|---|---|
| [`ceet-backend-engineer`](ceet-backend-engineer/) | Backend Engineer | Systems, data, invariants, failure modes, APIs |
| [`ceet-frontend-engineer`](ceet-frontend-engineer/) | Frontend Engineer | UI state, rendering, accessibility, client perf |
| [`ceet-devops-sre`](ceet-devops-sre/) | DevOps / SRE | Infra, CI/CD, observability, incident response |
| [`ceet-data-analytics`](ceet-data-analytics/) | Data / Analytics | Metrics, hypotheses, experimentation, SQL/Python |
| [`ceet-product-manager`](ceet-product-manager/) | Product Manager | Prioritization, discovery, roadmap, stakeholders |
| [`ceet-ux-researcher`](ceet-ux-researcher/) | UX Researcher (conductual) | Behavior, interviews, synthesis, jobs-to-be-done |
| [`ceet-ui-designer`](ceet-ui-designer/) | UI Designer | Visual system, components, motion, craft |
| [`ceet-copywriter`](ceet-copywriter/) | Copywriter | Voice, structure, conversion, brand tone |
| [`ceet-marketing`](ceet-marketing/) | Marketing | Positioning, channels, funnels, growth loops |
| [`ceet-sales`](ceet-sales/) | Sales | Discovery, objections, pipeline, closing |
| [`ceet-customer-success`](ceet-customer-success/) | Customer Success | Onboarding, retention, expansion, health signals |
| [`ceet-financial`](ceet-financial/) | Finance | Models, unit economics, forecasting, controls |
| [`ceet-legal-compliance`](ceet-legal-compliance/) | Legal / Compliance | Contracts, risk, regulation, policy |
| [`ceet-people-ops`](ceet-people-ops/) | People Ops / HR | Hiring, performance, culture, policy design |
| [`ceet-founder-ceo`](ceet-founder-ceo/) | Founder / CEO | Strategy, capital, narrative, org design |

## The shared loop (every CEET follows this)

```
┌──────────────┐   ┌──────────────┐   ┌────────────────┐   ┌──────────────────┐
│  INTERVIEW   │ → │   EXTRACT    │ → │   SYNTHESIZE    │ → │    ACTIVATE      │
│ deep, Q+A    │   │ patterns &   │   │ cognitive clone │   │ portable AI env  │
│ role-scoped  │   │ heuristics   │   │ + decision map  │   │ for any AI tool  │
└──────────────┘   └──────────────┘   └────────────────┘   └──────────────────┘
```

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full methodology, [`_shared/`](./_shared/) for shared templates and prompts, and each `ceet-<role>/` folder for the role-specific interview script and synthesis logic.

## Using a CEET in any AI tool

The outputs of every CEET are two files:

- **`cognitive-clone.md`** — a portable, vendor-neutral description of how the person thinks in their role.
- **`ai-environment.md`** — a system-prompt-ready configuration you can paste into:
  - Claude Projects / custom instructions
  - ChatGPT custom GPTs / instructions
  - Cursor / Copilot rules files (`.cursorrules`, `.github/copilot-instructions.md`)
  - Gemini Gems / system prompts
  - Any other AI tool that accepts a system prompt or context file

See [`_shared/prompts/activation-guide.md`](./_shared/prompts/activation-guide.md) for per-tool installation snippets.

## How to run a CEET

Pick the folder that matches the role, open its `SKILL.md`, and follow it. If you're using this inside an AI tool that supports Anthropic-style skills, the skill will trigger automatically when you ask for a cognitive extraction for that role.

See [`docs/how-to-use.md`](docs/how-to-use.md) for the full step-by-step guide.

## Documentation

| Document | What it covers |
|---|---|
| [`METHODOLOGY.md`](METHODOLOGY.md) | The four stages: interview → extract → synthesize → activate |
| [`docs/how-to-use.md`](docs/how-to-use.md) | Step-by-step guide for running a CEET extraction |
| [`docs/synthesis-rules.md`](docs/synthesis-rules.md) | 12 strict rules for converting interview responses to cognitive profiles |
| [`docs/tool-integration.md`](docs/tool-integration.md) | How to load outputs into Claude, ChatGPT, Cursor, Copilot, Gemini, and more |
| [`docs/extending.md`](docs/extending.md) | How to add a new role pack to the toolkit |
| [`_shared/universal-questions.md`](_shared/universal-questions.md) | 15 universal questions asked for every role before role-specific questions |

## Shared infrastructure

```
_shared/
├── templates/
│   ├── cognitive-clone.template.md      # Cognitive clone output schema (8 sections)
│   ├── ai-environment.template.md       # System-prompt-ready environment template
│   ├── cognitive-profile-output.template.md  # Human-readable profile template
│   ├── agent.template.md                # Generic agent artifact template
│   ├── skill.template.md                # Generic skill artifact template
│   ├── command.template.md              # Generic command artifact template
│   ├── hook.template.md                 # Generic hook artifact template (engineering only)
│   ├── rule.template.md                 # Generic global rule template
│   └── source-map.template.md           # Traceability matrix template
├── prompts/
│   └── activation-guide.md              # Per-tool installation snippets
├── schemas/
│   ├── profile-schema.json              # JSON Schema for cognitive profiles
│   ├── directive-domains-backend.json   # Backend engineer directive domain mapping
│   └── directive-domains-frontend.json  # Frontend engineer directive domain mapping
└── universal-questions.md               # 15 cross-role identity questions (U01–U15)
```

## Project status

This toolkit is under active construction. Each CEET folder is self-contained and will become a standalone skill package.

The [`_legacy/ceet/`](_legacy/ceet/) directory preserves the original single-role (backend engineer) prototype that this toolkit evolved from — including its 30 fully-developed artifact templates, 70-question bank, and Copilot skill file.
