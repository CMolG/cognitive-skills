# Synthesis Rules

> This document defines exactly how to turn raw interview responses into a cognitive profile and behavioral directives. Apply these rules rigorously — they are what prevents the system from sliding back into archetype classification.

---

## Rule 1: Verbatim Is Sacred

Raw responses must be stored **exactly** as the person said them.

- Do not fix grammar
- Do not shorten for concision
- Do not "clean up" language
- Do not paraphrase into a more "professional" version
- Do not merge multiple follow-ups into one synthesized response

If the person said "honestly I just vibe it" — that goes into `raw_responses` exactly as written. It is data, not embarrassment.

---

## Rule 2: Never Classify

At no point during synthesis do you assign the person to a category.

**Forbidden:**
- "You are a Pragmatic Architect"
- "You fit the Growth Marketer archetype"
- "Your style is Early Adopter"
- "Based on your answers, you are a Strict Reviewer"

**Required:**
- Capture the specific behavior they described
- Write it in their voice
- Reference the questions it came from

If you find yourself typing "this person is X type" — delete it and write what they actually do instead.

---

## Rule 3: Directive Voice = Person's Voice

Directives are written as if the person is explaining their own approach.

**Wrong (external description):**
> "This engineer prefers strict typing and blocks PRs that loosen type safety."

**Right (first-person directive):**
> "I use strict mode always. `any` requires a comment explaining why, reviewed by me. If a PR adds `any` without justification I block it — no exceptions for deadline pressure. [C06, C08]"

The AI loading this directive should be able to act on it without translation.

---

## Rule 4: Concrete Over Abstract

If the person gave a number, include the number. If they gave an example, include the example. If they named a tool, name the tool.

**Wrong:**
> "I care about performance for critical endpoints."

**Right:**
> "Anything user-facing above 200ms at p95 I profile. I use `perf`, then flamegraphs, then statistical profiling in that order. Database queries over 50ms get an EXPLAIN before I move on. [C37, C38]"

Abstraction removes the fingerprint. Specifics preserve it.

---

## Rule 5: Contradictions Are Data

When two answers genuinely conflict, **do not reconcile them into a clean position**. Record the tension.

Example contradiction entry:
```json
{
  "tension": "Self-reports 6/10 on perfectionism but always creates separate refactoring tickets even for small messes, and insists on strict typing with zero exceptions.",
  "question_a": "U12",
  "question_b": "C16",
  "resolution": "In code quality this person acts at 8–9/10 perfectionism. In shipping deadlines they drop to 5–6. The 6/10 self-report is a shipping-context self-image that does not reflect their code review behavior."
}
```

The AI using this profile should consult contradictions when a request spans both contexts.

---

## Rule 6: Traceability Is Mandatory

Every directive must include `[Q-ID]` references in square brackets to the source questions.

Example:
> "I hash passwords with Argon2id, memory cost 19 MiB, time cost 2, parallelism 1. bcrypt is acceptable on legacy systems with cost 12+ until they can migrate. I do not accept SHA-anything for passwords — I have had to argue this three times in my career. [C36, E22]"

Traceability means when someone asks "why does the agent behave this way?", the answer is always: "Because the person said X in question Q.".

---

## Rule 7: Scores Are Metadata

Composite scores on the radar chart are for human visualization. **They must not appear in any directive, agent, skill, command, rule, or hook**.

**Wrong (in a template):**
> "Since this person's security_paranoia is 9/10, enforce strict rules..."

**Right:**
> "I do not trust internal-network service-to-service calls. I require mTLS or signed JWTs with short TTL between internal services. [C31]"

Scores summarize. Directives decide.

---

## Rule 8: Identity Reflects All Answers

When writing `cognitive_signature`, `core_values`, and `decision_framework`, synthesize from the WHOLE interview. Do not write identity from just the universal questions — role-specific answers often reveal the strongest values.

Pattern to look for:
- A value the person mentions across 3+ unrelated questions is a core value, even if they never named it
- A phrase or metaphor the person repeats is a voice signature — preserve it
- A trade-off the person makes the same way across multiple questions is their decision framework

---

## Rule 9: Preserve Exceptions

The person's exceptions and edge cases are as important as their defaults. Every directive should include, where mentioned:

- The default rule
- The specific conditions under which they break it
- The specific conditions where they will not break it no matter what

Example:
> "I do not use emojis in commit messages. Exception: our team convention uses `:emoji:` prefixes and I comply to avoid churn. I never use emojis in code comments or customer-facing copy — that one I will not bend. [U11, C15]"

---

## Rule 10: Silence Is Also Data

What the person did NOT say matters.

When writing `blind_spots`, look for:
- Domains they treated as obvious that may not be
- Groups of questions they answered thinly
- Trade-offs they did not acknowledge
- Stakeholders they did not mention
- Edge cases they did not consider

Blind spots are NEVER derived from low scores. They are derived from the content of the answers themselves.

Example:
> "Across C43–C48 you described database design with strong performance instincts but never mentioned compliance, data retention policy, or deletion workflows. This may be a blind spot worth flagging when the AI works on data schemas in regulated environments."

---

## Rule 11: Do Not Generate Directives for Domains Not Covered

If a role's `directive-domains.json` includes a domain but the person's answers did not cover it, mark that domain as `"not_synthesized": true` with a note. Do not invent directives from thin air.

Example in profile:
```json
"directives": {
  "incident_response": {
    "_status": "not_synthesized",
    "_note": "Person did not answer questions C17–C20 in sufficient depth. Re-run interview to complete this domain."
  }
}
```

This keeps the clone honest about what it actually knows.

---

## Rule 12: Output Is Portable

Every generated artifact must be readable as standalone context by any AI system. That means:

- Full text, not placeholders, in the final output
- No references to "see other file" without the full content alongside
- No tool-specific syntax (no `@decorators`, no `::commands::`, no XML-only structures)
- Plain markdown headers and lists
- JSON only where structure matters (profile, raw responses)

Tool-specific wrappers (Claude project files, Copilot instructions, Cursor rules) are generated as **adapters** on top of the portable output. The portable output is always the source of truth.
