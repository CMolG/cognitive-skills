---
name: ceet-devops-sre
description: Cognitive Extraction Engine for DevOps and SRE practitioners. Use when a user wants to clone the judgment of an infrastructure, platform, or reliability engineer — how they think about CI/CD, observability, incident response, capacity planning, on-call, and reliability tradeoffs. Trigger on phrases like "extract my SRE thinking", "clone our platform engineer", "build an AI ops assistant that thinks like our oncall", "interview me about infrastructure", "capture how I run postmortems", or any request to distill DevOps/SRE judgment into a reusable AI configuration. Outputs are tool-agnostic.
---

# CEET — DevOps / SRE

## What this skill does

Interview a platform / infra / reliability engineer. Produce two tool-agnostic artifacts: a **cognitive clone** of how they think about infrastructure and reliability, and an **AI environment** that applies their judgment in any AI tool.

## When to use

- The user wants an AI that reviews Terraform/Kubernetes/Helm/pipeline code with their specific standards.
- A team wants a reusable "how our platform team thinks" artifact for AI assistants.
- The user is codifying incident-response and postmortem voice.

## Run order

1. **Read** `interview/questions.md`. Work theme by theme.
2. **Extract.** Tag: `#mental-model`, `#heuristic`, `#procedure`, `#quality`, `#anti-pattern`, `#vocabulary`.
3. **Ask for incident stories.** SRE judgment is overwhelmingly shaped by incidents — get 2-3 concrete ones.
4. **Synthesize** into `../_shared/templates/cognitive-clone.template.md`.
5. **Activate** into `../_shared/templates/ai-environment.template.md`. Save to `templates/`.
6. **Hand off** via `../_shared/prompts/activation-guide.md`.

## SRE-specific things to listen for

- **Error-budget thinking.** Do they run on SLOs? How do they negotiate with product?
- **Blast radius.** When changing infra, how do they bound the worst case?
- **Toil detection.** What do they consider toil, and what's their policy on automating vs. accepting it?
- **On-call philosophy.** What deserves a page vs. a ticket? What shame-free practices do they enforce?
- **Postmortem voice.** Blameless, narrative, action-item-driven — and what they refuse to include.
- **Observability layering.** Logs / metrics / traces / profiles — when each, what they instrument first.
- **Change management.** Canary / blue-green / feature flags / progressive delivery — their defaults.
- **IaC taste.** Terraform / Pulumi / Crossplane / CDK — opinions and reasons.
- **Cost vs. reliability tradeoffs.** When they push back on product, when they absorb cost.
- **Security reflexes.** Least-privilege instincts, secrets handling, what they refuse to review.

## Synthesis guardrails

- Include at least one **runbook-style decision procedure** (e.g. "When latency SLO burns, I…").
- Capture their **page / no-page criteria** explicitly — this shapes the AI's alerting advice.
- Keep specific vendor/tool names if they matter (they often do in this role).
- Save outputs to `templates/`.
