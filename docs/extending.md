# Extending CEET with a New Role

> Adding a new role takes four files and about 2–4 hours of thoughtful work.

---

## When to Add a New Role

Add a role when:

- The existing 15 roles do not capture a distinct cognitive domain
- You need a significantly different set of questions, not just adjustments
- The directive domains differ meaningfully from existing roles

**Do not add a role** when the existing one covers 80% of what you need — instead, add questions to that role's extension bank.

---

## Required Files

Create `ceet-{your-new-role}/` with:

```
ceet-{your-new-role}/
├── README.md                  # What this role covers, who it fits
├── skill.md                   # Interview instructions
├── questions.json             # 40 core + 30 extension questions
└── directive-domains.json     # Which directive categories this role produces
```

---

## File 1: `README.md`

Template:

```markdown
# CEET Role Pack — {Role Name}

## Who This Is For

One paragraph describing the person this role pack extracts. Be specific about the working context, seniority range, and distinguishing cognitive concerns.

## What This Captures

Bulleted list of the 5–8 major cognitive domains this role pack covers.

## What This Does NOT Capture

Note any adjacent roles or domains that are intentionally out of scope — direct the user to the appropriate role pack.

## Sections Overview

Table mapping section number to title to question count to what it covers.

## Estimated Time

Core: X minutes. With extension: Y minutes.
```

---

## File 2: `skill.md`

The skill file is the interviewer script. It references `METHODOLOGY.md` and layers role-specific behaviors on top.

Required structure:

```markdown
# CEET {Role Name} — Interview Skill

## Purpose

One paragraph describing what this interview extracts.

## Reference

This skill implements the methodology defined in `METHODOLOGY.md` and the rules in `docs/synthesis-rules.md`. Read those first.

## Interview Opening Script

[Role-appropriate opening that references methodology.md's template but mentions the specific role]

## Section-by-Section Guide

For each section in questions.json, list:
- Section ID and title
- What you are listening for
- Which directive domains this section feeds
- Adaptive probing suggestions specific to this section

## Role-Specific Adaptive Behaviors

Patterns unique to this role's interviews. For example:
- Engineers often claim TDD practice they do not follow — probe
- Marketers often describe strategy in abstractions — pin down the real channel and real CAC
- Designers often defer to "taste" — ask what taste concretely means in their work

## Directive Synthesis Notes

For each directive domain in directive-domains.json, notes on how to synthesize from the raw responses. Which questions feed which directives? What patterns indicate which values?

## Artifacts to Generate

List the specific agents, skills, commands, rules, and (if engineering) hooks this role produces. For each, list which directives feed it.
```

---

## File 3: `questions.json`

Structure:

```json
{
  "meta": {
    "role": "your-new-role",
    "version": "1.0.0",
    "core_count": 40,
    "extension_count": 30,
    "estimated_core_minutes": 60,
    "estimated_extension_minutes": 40
  },
  "core_sections": [
    {
      "id": "C1",
      "title": "Section Title",
      "purpose": "What this section captures",
      "questions": [
        {
          "id": "C01",
          "slug": "short-slug",
          "title": "Short question title",
          "prompt": "The actual question asked to the person. Include specifics to push for: numbers, examples, exceptions.",
          "probes": [
            "If the answer is vague, ask: ...",
            "If the answer is textbook, ask: ..."
          ],
          "feeds_directives": ["domain.field1", "domain.field2"]
        }
      ]
    }
  ],
  "extension_sections": [
    {
      "id": "E1",
      "title": "Extension section title",
      "purpose": "Deeper coverage of specific domain",
      "questions": [ ... ]
    }
  ]
}
```

### Question Writing Rules

1. **Ask for specifics.** Bake "give a number", "give an example", "give an exception" into the prompt itself.
2. **Avoid yes/no questions.** Always ask for the reasoning.
3. **Favor real over ideal.** "What do you actually do" beats "what do you think is best".
4. **Include the boundary.** Every question should also elicit when the rule breaks.
5. **One concept per question.** Do not combine unrelated ideas.

---

## File 4: `directive-domains.json`

Structure:

```json
{
  "role": "your-new-role",
  "directive_domains": {
    "domain_name": {
      "description": "What this directive domain covers",
      "fields": {
        "field_name": {
          "description": "What this specific directive captures",
          "sourced_from": ["C01", "C02", "E05"]
        }
      }
    }
  },
  "artifacts": {
    "agents": [
      {
        "name": "agent-name",
        "purpose": "What this agent does",
        "consumes_directives": ["domain_name.field_name", "..."]
      }
    ],
    "skills": [ ... ],
    "commands": [ ... ],
    "rules": [ ... ],
    "hooks": [ ... ]
  },
  "composite_scores": [
    "score_name_1",
    "score_name_2",
    "..."
  ]
}
```

---

## Testing Your New Role

Before committing:

1. **Run the interview on yourself.** If you cannot complete it, the questions are wrong.
2. **Verify traceability.** Every directive should have at least 2 `sourced_from` questions.
3. **Check for archetypes.** Read every question and directive domain — if any sounds like "Type A vs Type B", rewrite.
4. **Verify tool-agnostic output.** No tool-specific syntax in templates.
5. **Write a sample profile.** Hand-produce one profile for a hypothetical person. Does it feel faithful?

---

## Style Consistency with Existing Roles

- Section counts: aim for 5–7 sections, 5–8 questions each for core
- Extension sections: 3–5 sections, 6–10 questions each
- Directive domains: aim for 6–10 domains per role
- Composite scores: aim for 12–16 role-relevant dimensions
