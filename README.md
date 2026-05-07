# cognitive-skills

> Capture how a person thinks in their role, then make any AI tool think the same way for the same work.

A toolkit for **encoding human judgment as portable AI artifacts**. Run an interview, get a cognitive clone, paste it into Claude, ChatGPT, Cursor, Copilot, Gemini, or any tool that accepts a system prompt. The outputs are plain Markdown + YAML — no vendor lock-in, no SDK, no API key.

What ships in this repo:

- **15 role-specific Cognitive Extraction Engines (CEETs)** — interviews + synthesis templates for backend, frontend, devops/SRE, data, product, UX, UI, copy, marketing, sales, customer success, finance, legal, people-ops, and founder/CEO.
- **A production-grade Jira requirements pipeline** — six commands that turn ambiguous tickets into validated functional contracts with traceability, an LLM-augmented refinement step, and 85% test coverage.
- **A deterministic eval harness** — three benchmark tasks, no judge model, release-gate ready.
- **Three meta-skills** — auto-routing (`autodiscover`), sub-agent orchestration with validated handoff contracts, and the `impersonator` for drafting CEET packs from public evidence.

## 60-second example

```bash
git clone https://github.com/CMolG/cognitive-skills.git
cd cognitive-skills
```

Open [`examples/ready-to-use/backend-netflix-tech-blog/cognitive-profile.md`](examples/ready-to-use/backend-netflix-tech-blog/cognitive-profile.md), paste it into your AI tool's system prompt, and ask:

> "Review this pull request for a database migration that renames `users.email` to `users.primary_email`, backfills data, and adds a unique index."

You will get a review framed in expand-and-contract phases, dual-write windows, lock-build strategy, and rollback toggles — instead of a generic "add tests, check rollback" checklist. See the [before/after table](#before-and-after-base-model-vs-ceet-pack) below for the exact difference.

For the Jira pipeline specifically, watch the 90-second walkthrough:

```bash
bash examples/ready-to-use/demo-jira-pipeline.sh
```

It runs against a synthetic ticket fixture (no Jira credentials needed). Record cleanly with `asciinema rec` — see the script header for the exact command.

## What's new

- `1.2.0` (in progress) — Jira pipeline hardening: rule-based core fixed, LLM-augmented mode added, 76 tests at 82% coverage. Deterministic eval harness with three benchmark tasks. Meta-skills now have validated contracts (`OrchestrationPlan`, `SubAgentResult`) and a provenance enforcer for the impersonator. See [`CHANGELOG.md`](CHANGELOG.md).
- `1.1.x` — English documentation pass; autodiscover and sub-agent orchestration skills.
- `1.0.0` — Initial public release.

## Visual usage guide for SKILLS

> Each skill has its own subsection with a distinct Material icon, description, target audience, and usage examples.

# ![hub](https://api.iconify.design/material-symbols/hub.svg?width=48&height=48) 
### autodiscover
**What it does**: Discovers and automatically routes flows/skills according to the task.  
**Focused on**: Users who want to reduce manual skill selection.
- `Analyze this objective and tell me which skill should run first.`
- `Route this request to the correct flow without me choosing a role.`

# ![storage](https://api.iconify.design/material-symbols/storage.svg?width=48&height=48) 
### ceet-backend-engineer
**What it does**: Cognitive extraction for backend engineering (data, APIs, invariants).  
**Focused on**: Backend engineers and technical reviewers.
- `Generate a backend cognitive profile from an interview.`
- `Activate an AI environment to review migrations and API contracts.`

# ![brush](https://api.iconify.design/material-symbols/brush.svg?width=48&height=48) 
### ceet-copywriter
**What it does**: Captures copy criteria (voice, structure, conversion).  
**Focused on**: Copywriters and content/brand teams.
- `Extract my tone rules for B2B landing pages.`
- `Create prompts for rewrites with brand voice.`

# ![support_agent](https://api.iconify.design/material-symbols/support-agent.svg?width=48&height=48) 
### ceet-customer-success
**What it does**: Models decision-making for onboarding, retention, and expansion.  
**Focused on**: CSMs, support leads, and post-sales teams.
- `Synthesize my at-risk account playbook.`
- `Generates health score prioritization rules.`

# ![insights](https://api.iconify.design/material-symbols/insights.svg?width=48&height=48) 
### ceet-data-analytics
**What it does**: Extracts analysis, experimentation, and metrics frameworks.  
**Focused on**: Analysts, data practitioners, and growth teams.
- `Converts my analysis method into a cognitive clone.`
- `Creates commands to review hypotheses and biases in dashboards.`

# ![cloud](https://api.iconify.design/material-symbols/cloud.svg?width=48&height=48) 
### ceet-devops-sre
**What it does**: Captures SRE/DevOps criteria for operations, incidents, and reliability.  
**Focused on**: SREs, platform engineers, and on-call leads.
- `Models how I decide rollback vs forward-fix.`
- `Generate rules for postmortems and high-risk changes.`

# ![payments](https://api.iconify.design/material-symbols/payments.svg?width=48&height=48) 
### ceet-financial
**What it does**: Structures finance heuristics (models, forecast, controls).  
**Focused on**: Finance teams and founders focused on unit economics.
- `Extracts my logic for quarterly forecasting.`
- `Create prompts to validate pricing and margin assumptions.`

# ![flag](https://api.iconify.design/material-symbols/flag.svg?width=48&height=48) 
### ceet-founder-ceo
**What it does**: Synthesizes strategy, narrative, and organizational design criteria.  
**Focused on**: Founders, CEOs, and strategic staff.
- `Documents my process for deciding strategic bets.`
- `Generate an AI environment to prepare capital decisions.`

# ![web](https://api.iconify.design/material-symbols/web.svg?width=48&height=48) 
### ceet-frontend-engineer
**What it does**: Extracts decision patterns in UI state, rendering, and accessibility.  
**Focused on**: Frontend engineers and web product teams.
- `Creates a clone for frontend performance review.`
- `Defines accessibility and interaction quality rules.`

# ![gavel](https://api.iconify.design/material-symbols/gavel.svg?width=48&height=48) 
### ceet-legal-compliance
**What it does**: Captures legal risk, policy, and compliance criteria.  
**Focused on**: Legal ops, compliance officers, and risk teams.
- `Extracts my contractual review checklist.`
- `Generates directives for regulatory risk classification.`

# ![campaign](https://api.iconify.design/material-symbols/campaign.svg?width=48&height=48) 
### ceet-marketing
**What it does**: Models reasoning for positioning, channels, and funnels.  
**Focused on**: Performance marketers and brand/growth leads.
- `Synthesizes my multichannel acquisition strategy.`
- `Creates prompts for funnel and messaging audits.`

# ![groups](https://api.iconify.design/material-symbols/groups.svg?width=48&height=48) 
### ceet-people-ops
**What it does**: Extracts hiring, performance, and culture criteria.  
**Focused on**: HR, People Ops, and talent managers.
- `Converts my evaluation framework into operational rules.`
- `Generate artifacts for onboarding and professional development.`

# ![assignment](https://api.iconify.design/material-symbols/assignment.svg?width=48&height=48) 
### ceet-product-manager
**What it does**: Captures prioritization, discovery, and roadmap frameworks.  
**Focused on**: Product managers and product leads.
- `Extracts how I prioritize between technical debt and features.`
- `Create commands to prepare RFCs and scope decisions.`

# ![handshake](https://api.iconify.design/material-symbols/handshake.svg?width=48&height=48) 
### ceet-sales
**What it does**: Structures discovery, objection handling, and closing playbooks.  
**Focused on**: SDR/AE, consultative sales, and revenue teams.
- `Model my process for qualifying enterprise opportunities.`
- `Generates objection response guides by segment.`

# ![lan](https://api.iconify.design/material-symbols/lan.svg?width=48&height=48) 
### ceet-sub-agent-orchestration
**What it does**: Defines subagent coordination and distribution of cognitive tasks.  
**Focused on**: Teams that design multi-agent systems.
- `Designs agent orchestration for technical auditing.`
- `Set handoff rules between specialist agents.`

# ![palette](https://api.iconify.design/material-symbols/palette.svg?width=48&height=48) 
### ceet-ui-designer
**What it does**: Captures visual criteria for design systems, components, and motion.  
**Focused on**: UI designers and design systems teams.
- `Extract my principles for cross-product visual consistency.`
- `Generates prompts for hierarchy and contrast reviews.`

# ![psychology](https://api.iconify.design/material-symbols/psychology.svg?width=48&height=48) 
### ceet-ux-researcher
**What it does**: Models behavioral research thinking and findings synthesis.  
**Focused on**: UX researchers and product discovery squads.
- `Converts my interviews into product decision rules.`
- `Generates a template for synthesizing behavior patterns.`

# ![theater_comedy](https://api.iconify.design/material-symbols/theater-comedy.svg?width=48&height=48) 
### impersonator
**What it does**: Initializes simulated CEET packs from public evidence or repository history.  
**Focused on**: Users who need a quick draft without a live interview.
- `Creates an initial pack for a known technical author.`
- `Generate a cognitive profile draft from a repository.`

# ![schema](https://api.iconify.design/material-symbols/schema.svg?width=48&height=48) 
### jira-agentic-requirements-pipeline
**What it does**: Structures an agentic requirements pipeline based on Jira.  
**Focused on**: Product/engineering teams with Jira-centered operations.
- `Define a flow from intake to refined ticket.`
- `Generates quality policies for Jira user stories.`

The CLI is six subcommands. The top-level help lists them:

```text
$ python3 jira-agentic-requirements-pipeline/scripts/jira_pipeline_cli.py --help
usage: jira_pipeline_cli.py [-h]
                            {fetch-issue,discovery,generate-questions,collect-input,resolve-contract,base-branch-plan}
                            ...

Agentic requirements pipeline for Jira

positional arguments:
  {fetch-issue,discovery,generate-questions,collect-input,resolve-contract,base-branch-plan}
    fetch-issue         Fetch issue from Jira
    discovery           Analyze missing business requirements
    generate-questions  Generate prioritized business questions
    collect-input       Capture business answers with resumable state
    resolve-contract    Resolve a functional contract from answers
    base-branch-plan    Generate base branch implementation plan
```

Each subcommand has its own `--help` — for example,
`generate-questions --help` documents the `--baseline-budget` and
`--signal-budget` flags. See the skill's
[`SKILL.md`](jira-agentic-requirements-pipeline/SKILL.md),
[`EXAMPLES.md`](jira-agentic-requirements-pipeline/EXAMPLES.md), and
[`TROUBLESHOOTING.md`](jira-agentic-requirements-pipeline/TROUBLESHOOTING.md)
for the full quick start.

## Three ways to use this repo

1. **Use a ready-made pack** — open `examples/ready-to-use/backend-netflix-tech-blog/` (or any other pack) and copy `cognitive-profile.md` into your AI tool's system prompt. Provenance is in each pack's `evidence-map.md`.
2. **Draft a pack from public evidence** — point any skill-aware AI at [`impersonator/SKILL.md`](impersonator/SKILL.md). It generates a simulated pack for a public figure or repo author and runs through [`impersonator/scripts/validate_pack.py`](impersonator/scripts/validate_pack.py) before shipping.
3. **Run a real CEET interview** — open the role's `SKILL.md` and follow the interview flow. Output is a first-person cognitive clone.

## Before and after: base model vs CEET pack

Same prompt, two arms. Verifiable with the harness in [`evals/`](evals/).

**Prompt:**

> "Review this pull request for a database migration that renames `users.email` to `users.primary_email`, backfills data, and adds a unique index."

| Base model (generic) | CEET pack (`backend-netflix-tech-blog`) |
|---|---|
| Recommends adding tests and checking migration rollback. | Breaks migration into expand/contract phases and explicitly asks for dual-write windows before rename cutover. |
| Mentions performance and downtime in general terms. | Calls out index build strategy, lock behavior, query plan verification, and rollback toggles under active traffic. |
| Suggests validating data after migration. | Requests invariant checks (`null`, duplicate, stale writer paths), replay safety, and observability signals for each phase. |
| Gives a broad checklist. | Prioritizes blast radius controls: canary rollout, feature flags, and explicit fail-fast criteria tied to SLO/error budget impact. |

### Harness numbers (seed run, synthetic outputs)

The eval harness scores three benchmark tasks with deterministic metrics: required-phrase coverage, required-section coverage, and TF-cosine voice alignment vs a per-task corpus. Composite is the mean of the three.

| Task | baseline | ceet | generic | Δ ceet−baseline |
|---|---:|---:|---:|---:|
| `engineering-pr-review` | 0.59 | **0.85** | 0.44 | **+0.27** |
| `product-prd-draft` | 0.78 | **0.81** | 0.73 | +0.03 |
| `copy-headlines` | 0.54 | **0.77** | 0.41 | **+0.23** |

> The seed outputs under `evals/results/seed-2026-05-07/` are synthetic — written to self-test the harness, not as a benchmark. Replace them with outputs from your own model and re-run `python3 evals/scripts/run.py --run-id <your-id>` to produce real numbers. The release gate (`--gate --min-delta 0.05`) requires `ceet` to beat `baseline` on at least 2/3 tasks.

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
