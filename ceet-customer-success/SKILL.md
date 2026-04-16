---
name: ceet-customer-success
description: Cognitive Extraction Engine for Customer Success — CSMs, CS leaders, account managers focused on onboarding, adoption, retention, and expansion. Use when a user wants to clone a CS practitioner's judgment — how they read health signals, run QBRs, mitigate churn, and drive expansion. Trigger on phrases like "extract my CS thinking", "clone our top CSM", "build an AI that drafts QBRs like me", "interview me about retention", "capture my churn playbook", "make a customer success cognitive clone". Outputs are tool-agnostic.
---

# CEET — Customer Success

## What this skill does

Interview a CSM or CS leader. Produce a cognitive clone and AI environment that drafts onboarding plans, QBRs, at-risk playbooks, and renewal / expansion motions in their style.

## When to use

- The user wants an AI that writes customer-facing communication in their voice.
- A CS leader wants a top CSM's judgment captured and scaled.
- A founder wants retention instincts preserved as CS hiring starts.

## Run order

1. **Read** `interview/questions.md`.
2. **Extract.** CS judgment is heavily *pattern-based* — probe for the repeating customer archetypes they've seen.
3. **Ask for save stories and loss stories** — both are high-signal.
4. **Synthesize** into the role-specific `templates/cognitive-profile.md`.
5. **Activate** into the role-specific `templates/` directory. Save to `templates/`.
6. **Hand off** via [`../docs/tool-integration.md`](../docs/tool-integration.md).

## CS-specific things to listen for

- **Health scoring instincts.** Signals they trust beyond the dashboard.
- **Onboarding philosophy.** First-value milestone, time-to-value target, checklist vs. flexible.
- **Adoption framework.** How they think about rollout, stakeholder alignment, internal champion.
- **QBR voice.** Format, cadence, attendee criteria, what they refuse to put in.
- **At-risk playbook.** Signals, escalation path, exec sponsor pattern, trade offers.
- **Renewal motion.** How early they start, discount posture, multi-year stance.
- **Expansion triggers.** Who they upsell, when, how they avoid poisoning the relationship.
- **Escalation handling.** How they absorb anger, when they loop in exec / product.
- **Handoff from sales.** What they wish sales would stop promising.
- **Advocate creation.** How they spot and cultivate references.

## Synthesis guardrails

- Capture their **customer archetypes** (e.g. "lukewarm exec, excited champion, skeptical admin") and how they treat each.
- Include their **QBR skeleton** verbatim if they have one.
- Preserve **escalation vocabulary** (the words they use when a customer is angry).
- Save outputs to `templates/`.
