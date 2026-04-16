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

See [`METHODOLOGY.md`](METHODOLOGY.md) for the full methodology and each `ceet-<role>/` folder for the role-specific interview script, synthesis logic, templates, and examples.

## Using a CEET in any AI tool

The outputs of every CEET are two files:

- **`cognitive-clone.md`** — a portable, vendor-neutral description of how the person thinks in their role.
- **`ai-environment.md`** — a system-prompt-ready configuration you can paste into:
  - Claude Projects / custom instructions
  - ChatGPT custom GPTs / instructions
  - Cursor / Copilot rules files (`.cursorrules`, `.github/copilot-instructions.md`)
  - Gemini Gems / system prompts
  - Any other AI tool that accepts a system prompt or context file

## How to run a CEET

Pick the folder that matches the role, open its `SKILL.md`, and follow it. If you're using this inside an AI tool that supports Anthropic-style skills, the skill will trigger automatically when you ask for a cognitive extraction for that role.

See [`docs/how-to-use.md`](docs/how-to-use.md) for the full step-by-step guide.

## Each role folder structure

Every `ceet-<role>/` folder is fully self-contained:

```
ceet-<role>/
├── README.md                     # Role overview, interview flow, output artifacts
├── SKILL.md                      # AI-triggerable skill definition
├── interview/
│   └── questions.md              # Role-specific interview questions
├── templates/                    # Role-specific artifact templates
│   ├── agents/                   # 5 agent templates (e.g., code-reviewer, debugger)
│   ├── skills/                   # 5–6 skill templates (e.g., style-enforcer, test-writer)
│   ├── commands/                 # 8–10 command templates (e.g., /review, /debug)
│   ├── rules/                    # 5–6 global rule templates (e.g., coding-standards)
│   ├── hooks/                    # 3 hook templates (engineering roles only)
│   └── cognitive-profile.md      # Full cognitive profile template
└── examples/
    └── README.md                 # How to generate and use example outputs
```

All templates use `{directives.domain.field}` placeholders that are injected from the cognitive profile during generation — zero conditional logic.

## Documentation

| Document | What it covers |
|---|---|
| [`METHODOLOGY.md`](METHODOLOGY.md) | The four stages: interview → extract → synthesize → activate |
| [`docs/how-to-use.md`](docs/how-to-use.md) | Step-by-step guide for running a CEET extraction |
| [`docs/synthesis-rules.md`](docs/synthesis-rules.md) | 12 strict rules for converting interview responses to cognitive profiles |
| [`docs/tool-integration.md`](docs/tool-integration.md) | How to load outputs into Claude, ChatGPT, Cursor, Copilot, Gemini, and more |
| [`docs/extending.md`](docs/extending.md) | How to add a new role pack to the toolkit |

## Project status

This toolkit is under active construction. Each CEET folder is self-contained and will become a standalone skill package.
