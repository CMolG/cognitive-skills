<!-- CEET Source:
  Role: {role}
  Skill: {skill_name}
  Raw Responses: {source_questions}
  Directives: {directive_paths}
-->

# {skill_name} Skill — {person_name}

> Focused capability that performs {skill_purpose} exactly as {person_name} would.

---

## Purpose

{skill_description}

---

## Directives

{skill_directives_block}

---

## Execution Protocol

When invoked for this skill:

1. Apply the directives above in order
2. Use {person_name}'s naming, formatting, and voice conventions throughout
3. Where a directive specifies a threshold or rule, enforce it exactly — no fuzzy approximation
4. Where a directive specifies an exception, honor the exception
5. If two directives conflict, consult `cognitive-profile.md` → `identity.decision_framework` to resolve

---

## Output Style

{communication_voice_summary}

---

## Escalation

{escalation_protocol_if_applicable}
