# CEET — Cognitive Extraction Engine Toolkit

A family of role-specific **Cognitive Extraction Engines**. Each CEET is a structured interview + synthesis skill that:

1. **Interviews** a person working in a given role with deep, role-specific questions.
2. **Extracts** their cognitive patterns — how they decide, what they pay attention to, what failure modes they watch for, which heuristics they use, and what "good" looks like to them.
3. **Synthesizes** an **Individual Cognitive Clone** — a portable artifact describing how *this specific person* thinks in *this specific role*.
4. **Generates** a **Personalized AI Environment** — prompts, rules, and guardrails that make any AI assistant mimic that person's judgment on their real work.

> CEETs produce **tool-agnostic outputs**. The generated cognitive clone and AI environment work in Claude, ChatGPT, Cursor, Copilot, Gemini, Perplexity, or any other AI tool — because the artifacts are plain Markdown + YAML, not wrapped in any vendor's proprietary format.


## Novedades destacadas

- **Pack listo para usar sin instalación**: `backend-netflix-tech-blog` para probar el enfoque CEET en minutos.
- **Skill independiente `impersonator`**: genera borradores simulados de packs CEET a partir de evidencia pública o historial de repositorios.
- **Cobertura de 15 roles profesionales** con scripts de entrevista, plantillas y ejemplos por rol.
- **Artefactos portables y agnósticos del proveedor** (`cognitive-clone.md` + `ai-environment.md`) para reutilizar en Claude, ChatGPT, Cursor, Copilot, Gemini y más.

## Guía de uso visual de SKILLS

> Cada skill tiene su propia subsección con un icono Material distinto, descripción, público objetivo y ejemplos de uso.

### ![hub](https://fonts.gstatic.com/s/i/materialicons/hub/v12/24px.svg) autodiscover
**Qué hace**: Descubre y enruta automáticamente flujos/skills según la tarea.  
**Enfocada a**: Usuarios que quieren reducir selección manual de skills.
- `Analiza este objetivo y dime qué skill conviene ejecutar primero.`
- `Rutea esta petición al flujo correcto sin que yo elija rol.`

### ![storage](https://fonts.gstatic.com/s/i/materialicons/storage/v10/24px.svg) ceet-backend-engineer
**Qué hace**: Extracción cognitiva para ingeniería backend (datos, APIs, invariantes).  
**Enfocada a**: Backend engineers y reviewers técnicos.
- `Genera un perfil cognitivo backend a partir de entrevista.`
- `Activa un entorno AI para revisar migraciones y contratos API.`

### ![brush](https://fonts.gstatic.com/s/i/materialicons/brush/v15/24px.svg) ceet-copywriter
**Qué hace**: Captura criterios de copy (voz, estructura, conversión).  
**Enfocada a**: Copywriters y equipos de contenido/brand.
- `Extrae mis reglas de tono para landings B2B.`
- `Crea prompts para reescritura con voz de marca.`

### ![support_agent](https://fonts.gstatic.com/s/i/materialicons/support_agent/v13/24px.svg) ceet-customer-success
**Qué hace**: Modela toma de decisiones en onboarding, retención y expansión.  
**Enfocada a**: CSMs, leads de soporte y postventa.
- `Sintetiza mi playbook de cuentas en riesgo.`
- `Genera reglas de priorización de health score.`

### ![insights](https://fonts.gstatic.com/s/i/materialicons/insights/v11/24px.svg) ceet-data-analytics
**Qué hace**: Extrae marcos de análisis, experimentación y métricas.  
**Enfocada a**: Analistas, data practitioners y equipos growth.
- `Convierte mi método de análisis en un cognitive clone.`
- `Crea comandos para revisar hipótesis y sesgos en dashboards.`

### ![cloud](https://fonts.gstatic.com/s/i/materialicons/cloud/v17/24px.svg) ceet-devops-sre
**Qué hace**: Captura criterios SRE/DevOps para operación, incidentes y fiabilidad.  
**Enfocada a**: SREs, platform engineers y on-call leads.
- `Modela cómo decido rollback vs forward-fix.`
- `Genera reglas para postmortems y cambios de alto riesgo.`

### ![payments](https://fonts.gstatic.com/s/i/materialicons/payments/v11/24px.svg) ceet-financial
**Qué hace**: Estructura heurísticas de finanzas (modelos, forecast, controles).  
**Enfocada a**: Equipos financieros y founders con foco en unit economics.
- `Extrae mi lógica para forecast trimestral.`
- `Crea prompts para validar supuestos de pricing y margen.`

### ![flag](https://fonts.gstatic.com/s/i/materialicons/flag/v18/24px.svg) ceet-founder-ceo
**Qué hace**: Sintetiza criterios de estrategia, narrativa y diseño organizativo.  
**Enfocada a**: Founders, CEOs y staff estratégico.
- `Documenta mi proceso para decidir apuestas estratégicas.`
- `Genera un entorno AI para preparar decisiones de capital.`

### ![web](https://fonts.gstatic.com/s/i/materialicons/web/v13/24px.svg) ceet-frontend-engineer
**Qué hace**: Extrae patrones de decisión en UI state, rendering y accesibilidad.  
**Enfocada a**: Frontend engineers y product teams web.
- `Crea un clone para revisión de performance en frontend.`
- `Define reglas de accesibilidad y calidad de interacción.`

### ![gavel](https://fonts.gstatic.com/s/i/materialicons/gavel/v12/24px.svg) ceet-legal-compliance
**Qué hace**: Captura criterios de riesgo legal, políticas y compliance.  
**Enfocada a**: Legal ops, compliance officers y equipos de riesgo.
- `Extrae mi checklist de revisión contractual.`
- `Genera directivas para clasificación de riesgo regulatorio.`

### ![campaign](https://fonts.gstatic.com/s/i/materialicons/campaign/v11/24px.svg) ceet-marketing
**Qué hace**: Modela razonamiento de posicionamiento, canales y embudos.  
**Enfocada a**: Marketers de performance y brand/growth leads.
- `Sintetiza mi estrategia de adquisición multicanal.`
- `Crea prompts para auditoría de funnel y mensajes.`

### ![groups](https://fonts.gstatic.com/s/i/materialicons/groups/v14/24px.svg) ceet-people-ops
**Qué hace**: Extrae criterios de hiring, performance y cultura.  
**Enfocada a**: RR.HH., People Ops y managers de talento.
- `Convierte mi framework de evaluación en reglas operativas.`
- `Genera artefactos para onboarding y desarrollo profesional.`

### ![assignment](https://fonts.gstatic.com/s/i/materialicons/assignment/v16/24px.svg) ceet-product-manager
**Qué hace**: Captura marcos de priorización, discovery y roadmap.  
**Enfocada a**: Product managers y product leads.
- `Extrae cómo decido prioridad entre deuda técnica y features.`
- `Crea comandos para preparar RFCs y decisiones de alcance.`

### ![handshake](https://fonts.gstatic.com/s/i/materialicons/handshake/v1/24px.svg) ceet-sales
**Qué hace**: Estructura playbooks de discovery, objeciones y cierre.  
**Enfocada a**: SDR/AE, ventas consultivas y revenue teams.
- `Modela mi proceso para calificar oportunidades enterprise.`
- `Genera guías de respuesta a objeciones por segmento.`

### ![lan](https://fonts.gstatic.com/s/i/materialicons/lan/v7/24px.svg) ceet-sub-agent-orchestration
**Qué hace**: Define coordinación de subagentes y reparto de tareas cognitivas.  
**Enfocada a**: Equipos que diseñan sistemas multiagente.
- `Diseña una orquestación de agentes para auditoría técnica.`
- `Establece reglas de handoff entre agentes especialistas.`

### ![palette](https://fonts.gstatic.com/s/i/materialicons/palette/v14/24px.svg) ceet-ui-designer
**Qué hace**: Captura criterio visual sobre sistemas de diseño, componentes y motion.  
**Enfocada a**: UI designers y design systems teams.
- `Extrae mis principios para consistencia visual cross-product.`
- `Genera prompts para revisión de jerarquía y contraste.`

### ![psychology](https://fonts.gstatic.com/s/i/materialicons/psychology/v10/24px.svg) ceet-ux-researcher
**Qué hace**: Modela pensamiento de investigación conductual y síntesis de hallazgos.  
**Enfocada a**: UX researchers y product discovery squads.
- `Convierte mis entrevistas en reglas de decisión de producto.`
- `Genera una plantilla para síntesis de patrones de comportamiento.`

### ![theater_comedy](https://fonts.gstatic.com/s/i/materialicons/theater_comedy/v6/24px.svg) impersonator
**Qué hace**: Inicializa packs CEET simulados con evidencia pública o historial de repositorios.  
**Enfocada a**: Usuarios que necesitan un borrador rápido sin entrevista en vivo.
- `Crea un pack inicial para un autor técnico conocido.`
- `Genera un draft de cognitive profile desde un repositorio.`

### ![schema](https://fonts.gstatic.com/s/i/materialicons/schema/v7/24px.svg) jira-agentic-requirements-pipeline
**Qué hace**: Estructura un pipeline agéntico de requisitos basado en Jira.  
**Enfocada a**: Equipos de producto/ingeniería con operación centrada en Jira.
- `Define un flujo desde intake hasta ticket refinado.`
- `Genera políticas de calidad para user stories en Jira.`

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
