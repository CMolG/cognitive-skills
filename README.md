# CEET — Cognitive Extraction Engine Toolkit

A family of role-specific **Cognitive Extraction Engines**. Each CEET is a structured interview + synthesis skill that:

1. **Interviews** a person working in a given role with deep, role-specific questions.
2. **Extracts** their cognitive patterns — how they decide, what they pay attention to, what failure modes they watch for, which heuristics they use, and what "good" looks like to them.
3. **Synthesizes** an **Individual Cognitive Clone** — a portable artifact describing how *this specific person* thinks in *this specific role*.
4. **Generates** a **Personalized AI Environment** — prompts, rules, and guardrails that make any AI assistant mimic that person's judgment on their real work.

> CEETs produce **tool-agnostic outputs**. The generated cognitive clone and AI environment work in Claude, ChatGPT, Cursor, Copilot, Gemini, Perplexity, or any other AI tool — because the artifacts are plain Markdown + YAML, not wrapped in any vendor's proprietary format.


## Featured updates

- **Ready-to-use pack with no installation**: `backend-netflix-tech-blog` to try the CEET approach in minutes.
- **Standalone skill `impersonator`**: generates simulated drafts of CEET packs from public evidence or repository history.
- **Coverage for 15 professional roles** with interview scripts, templates, and examples per role.
- **Portable provider-agnostic artifacts** (`cognitive-clone.md` + `ai-environment.md`) for reuse in Claude, ChatGPT, Cursor, Copilot, Gemini, and more.

## Visual usage guide for SKILLS

> Each skill has its own subsection with a distinct Material icon, description, target audience, and usage examples.

### ![hub](https://fonts.gstatic.com/s/i/materialicons/hub/v12/24px.svg) autodiscover
**What it does**: Discovers and automatically routes flows/skills according to the task.  
**Focused on**: Users who want to reduce manual skill selection.
- `Analyze this objective and tell me which skill should run first.`
- `Route this request to the correct flow without me choosing a role.`

### ![storage](https://fonts.gstatic.com/s/i/materialicons/storage/v10/24px.svg) ceet-backend-engineer
**What it does**: Cognitive extraction for backend engineering (data, APIs, invariants).  
**Focused on**: Backend engineers and technical reviewers.
- `Generate a backend cognitive profile from an interview.`
- `Activate an AI environment to review migrations and API contracts.`

### ![brush](https://fonts.gstatic.com/s/i/materialicons/brush/v15/24px.svg) ceet-copywriter
**What it does**: Captures copy criteria (voice, structure, conversion).  
**Focused on**: Copywriters and content/brand teams.
- `Extract my tone rules for B2B landing pages.`
- `Create prompts for rewrites with brand voice.`

### ![support_agent](https://fonts.gstatic.com/s/i/materialicons/support_agent/v13/24px.svg) ceet-customer-success
**What it does**: Models decision-making for onboarding, retention, and expansion.  
**Focused on**: CSMs, support leads, and post-sales teams.
- `Synthesize my at-risk account playbook.`
- `Generates health score prioritization rules.`

### ![insights](https://fonts.gstatic.com/s/i/materialicons/insights/v11/24px.svg) ceet-data-analytics
**What it does**: Extracts analysis, experimentation, and metrics frameworks.  
**Focused on**: Analysts, data practitioners, and growth teams.
- `Converts my analysis method into a cognitive clone.`
- `Creates commands to review hypotheses and biases in dashboards.`

### ![cloud](https://fonts.gstatic.com/s/i/materialicons/cloud/v17/24px.svg) ceet-devops-sre
**What it does**: Captures SRE/DevOps criteria for operations, incidents, and reliability.  
**Focused on**: SREs, platform engineers, and on-call leads.
- `Models how I decide rollback vs forward-fix.`
- `Generate rules for postmortems and high-risk changes.`

### ![payments](https://fonts.gstatic.com/s/i/materialicons/payments/v11/24px.svg) ceet-financial
**What it does**: Structures finance heuristics (models, forecast, controls).  
**Focused on**: Finance teams and founders focused on unit economics.
- `Extracts my logic for quarterly forecasting.`
- `Create prompts to validate pricing and margin assumptions.`

### ![flag](https://fonts.gstatic.com/s/i/materialicons/flag/v18/24px.svg) ceet-founder-ceo
**What it does**: Synthesizes strategy, narrative, and organizational design criteria.  
**Focused on**: Founders, CEOs, and strategic staff.
- `Documents my process for deciding strategic bets.`
- `Generate an AI environment to prepare capital decisions.`

### ![web](https://fonts.gstatic.com/s/i/materialicons/web/v13/24px.svg) ceet-frontend-engineer
**What it does**: Extracts decision patterns in UI state, rendering, and accessibility.  
**Focused on**: Frontend engineers and web product teams.
- `Creates a clone for frontend performance review.`
- `Defines accessibility and interaction quality rules.`

### ![gavel](https://fonts.gstatic.com/s/i/materialicons/gavel/v12/24px.svg) ceet-legal-compliance
**What it does**: Captures legal risk, policy, and compliance criteria.  
**Focused on**: Legal ops, compliance officers, and risk teams.
- `Extracts my contractual review checklist.`
- `Generates directives for regulatory risk classification.`

### ![campaign](https://fonts.gstatic.com/s/i/materialicons/campaign/v11/24px.svg) ceet-marketing
**What it does**: Models reasoning for positioning, channels, and funnels.  
**Focused on**: Performance marketers and brand/growth leads.
- `Synthesizes my multichannel acquisition strategy.`
- `Creates prompts for funnel and messaging audits.`

### ![groups](https://fonts.gstatic.com/s/i/materialicons/groups/v14/24px.svg) ceet-people-ops
**What it does**: Extracts hiring, performance, and culture criteria.  
**Focused on**: HR, People Ops, and talent managers.
- `Converts my evaluation framework into operational rules.`
- `Generate artifacts for onboarding and professional development.`

### ![assignment](https://fonts.gstatic.com/s/i/materialicons/assignment/v16/24px.svg) ceet-product-manager
**What it does**: Captures prioritization, discovery, and roadmap frameworks.  
**Focused on**: Product managers and product leads.
- `Extracts how I prioritize between technical debt and features.`
- `Create commands to prepare RFCs and scope decisions.`

### ![handshake](https://fonts.gstatic.com/s/i/materialicons/handshake/v1/24px.svg) ceet-sales
**What it does**: Structures discovery, objection handling, and closing playbooks.  
**Focused on**: SDR/AE, consultative sales, and revenue teams.
- `Model my process for qualifying enterprise opportunities.`
- `Generates objection response guides by segment.`

### ![lan](https://fonts.gstatic.com/s/i/materialicons/lan/v7/24px.svg) ceet-sub-agent-orchestration
**What it does**: Defines subagent coordination and distribution of cognitive tasks.  
**Focused on**: Teams that design multi-agent systems.
- `Designs agent orchestration for technical auditing.`
- `Set handoff rules between specialist agents.`

### ![palette](https://fonts.gstatic.com/s/i/materialicons/palette/v14/24px.svg) ceet-ui-designer
**What it does**: Captures visual criteria for design systems, components, and motion.  
**Focused on**: UI designers and design systems teams.
- `Extract my principles for cross-product visual consistency.`
- `Generates prompts for hierarchy and contrast reviews.`

### ![psychology](https://fonts.gstatic.com/s/i/materialicons/psychology/v10/24px.svg) ceet-ux-researcher
**What it does**: Models behavioral research thinking and findings synthesis.  
**Focused on**: UX researchers and product discovery squads.
- `Converts my interviews into product decision rules.`
- `Generates a template for synthesizing behavior patterns.`

### ![theater_comedy](https://fonts.gstatic.com/s/i/materialicons/theater_comedy/v6/24px.svg) impersonator
**What it does**: Initializes simulated CEET packs from public evidence or repository history.  
**Focused on**: Users who need a quick draft without a live interview.
- `Creates an initial pack for a known technical author.`
- `Generate a cognitive profile draft from a repository.`

### ![schema](https://fonts.gstatic.com/s/i/materialicons/schema/v7/24px.svg) jira-agentic-requirements-pipeline
**What it does**: Structures an agentic requirements pipeline based on Jira.  
**Focused on**: Product/engineering teams with Jira-centered operations.
- `Define a flow from intake to refined ticket.`
- `Generates quality policies for Jira user stories.`

## Try it instantly (No installation required)

Use the ready-to-use pack at [`examples/ready-to-use/backend-netflix-tech-blog/`](examples/ready-to-use/backend-netflix-tech-blog/).

1. Copy [`cognitive-profile.md`](examples/ready-to-use/backend-netflix-tech-blog/cognitive-profile.md) from that folder.
2. Paste it into your Cursor project rules, Claude project instructions, or any AI tool's system prompt.
3. Ask: **"Review this pull request for a database migration."**

> This pack is **`backend-netflix-tech-blog`**, a simulation built from publicly available Netflix engineering materials (Netflix Tech Blog / public talks). It is a study/demo artifact, not a first-person interview profile. Full provenance is in the pack's [`evidence-map.md`](examples/ready-to-use/backend-netflix-tech-blog/evidence-map.md).

## Quick Start

```bash
git clone https://github.com/CMolG/cognitive-skills.git
cd cognitive-skills
```

Then either:

1. **Use the ready-to-use pack directly** — open `examples/ready-to-use/backend-netflix-tech-blog/` and copy the files you need into your AI tool.
2. **Generate a new pack via the `impersonator` skill** — point any skill-aware AI assistant at [`impersonator/SKILL.md`](impersonator/SKILL.md) and ask it to build a pack for your chosen target role + subject (public figure or repo author). Output lands in `examples/ready-to-use/<your-slug>/`.
3. **Run a full CEET interview** for any of the 15 roles — open the role's `SKILL.md` and follow the interview flow for a first-person cognitive clone.

## Before and After: Base model vs CEET pack

**Prompt used in both cases:**

> "Review this pull request for a database migration that renames `users.email` to `users.primary_email`, backfills data, and adds a unique index."

| Base model (generic) | CEET pack (backend-netflix-tech-blog) |
|---|---|
| Recommends adding tests and checking migration rollback. | Breaks migration into expand/contract phases and explicitly asks for dual-write windows before rename cutover. |
| Mentions performance and downtime in general terms. | Calls out index build strategy, lock behavior, query plan verification, and rollback toggles under active traffic. |
| Suggests validating data after migration. | Requests invariant checks (`null`, duplicate, stale writer paths), replay safety, and observability signals for each phase. |
| Gives a broad checklist. | Prioritizes blast radius controls: canary rollout, feature flags, and explicit fail-fast criteria tied to SLO/error budget impact. |

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

## Independent skills

| Folder | Purpose |
|---|---|
| [`impersonator`](impersonator/) | Initialize any CEET role with a simulated draft pack inferred from public-figure evidence or repository-author commit/code history (no interview). |

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
| [`impersonator/README.md`](impersonator/README.md) | Independent non-interview skill for simulated CEET initialization |

## Project status

This toolkit is under active construction. Each CEET folder is self-contained and will become a standalone skill package.
