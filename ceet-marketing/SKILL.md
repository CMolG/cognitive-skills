---
name: ceet-marketing
description: Cognitive Extraction Engine for marketers — growth, brand, demand-gen, product marketing. Use when a user wants to clone a marketer's judgment about positioning, channels, funnels, campaigns, and growth loops. Trigger on phrases like "extract my marketing thinking", "clone our head of growth", "build an AI that plans campaigns like me", "interview me about positioning", "capture my growth playbook", "make a marketing cognitive clone". Outputs are tool-agnostic.
---

# CEET — Marketing

## What this skill does

Interview a marketer. Produce a cognitive clone and AI environment that reasons about positioning, channels, campaigns, funnels, and growth in their style.

## When to use

- The user wants an AI that drafts campaigns, briefs agencies, or plans GTM in their voice.
- A head of marketing wants to scale their playbook across team members and AI tools.
- A PMM wants narratives and launch plans drafted to their standards.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract.** Marketers often conflate *positioning* with *messaging* with *tactics* — separate them during interview.
3. **Ask for win and loss stories.** Both teach more than theory.
4. **Synthesize** into `../_shared/templates/cognitive-clone.template.md`.
5. **Activate** into `../_shared/templates/ai-environment.template.md`. Save to `templates/`.
6. **Hand off** via `../_shared/prompts/activation-guide.md`.

## Marketing-specific things to listen for

- **Positioning frame.** Category, alternative, ICP, unique value — which lens is dominant?
- **ICP rigor.** Who's in, who's explicitly out, what makes a bad-fit customer.
- **Channel philosophy.** Paid / organic / community / sales-led / PLG — their mix and why.
- **Funnel model.** AARRR, bowtie, jobs funnel, GTM partnership with sales.
- **Brand vs. demand.** How they split budget and attention. What they refuse to measure by ROI.
- **Attribution honesty.** What they actually believe vs. what they report to the board.
- **Creative bar.** What makes a great campaign, piece of content, event.
- **Growth loops.** Do they think in loops, funnels, or both?
- **Messaging hierarchy.** The one line, the three pillars, the taglines, and how they cascade.
- **Competitive stance.** How they position against alternatives without naming names.

## Synthesis guardrails

- Separate **positioning statements** from **messaging pillars** from **campaign headlines**. The AI should know the level it's writing at.
- Capture their **ICP refusals** (who they don't sell to) — often more revealing than the ICP they claim.
- Save outputs to `templates/`.
