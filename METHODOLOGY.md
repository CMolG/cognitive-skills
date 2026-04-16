# CEET Methodology

How a Cognitive Extraction Engine converts a conversation with a role-holder into a portable cognitive clone and a working AI environment.

## Why role-specific CEETs

A single generic "software professional" skill underfits every role. A backend engineer's cognitive model (systems, invariants, blast radius, data integrity) is almost disjoint from a copywriter's (voice, audience state-of-mind, conversion, brand consistency). Even inside engineering, a frontend engineer and an SRE watch for fundamentally different failure signals.

Each CEET is tuned to:

- The **artifacts** that role produces (code, docs, designs, contracts, forecasts, campaigns…)
- The **failure modes** that role is paid to prevent
- The **heuristics** that experienced practitioners use and novices don't
- The **tools and rituals** that role lives inside day-to-day

## The four stages

### 1. Interview

Each CEET ships a role-specific question set in `interview/questions.md`. Questions are grouped into:

- **Context** — where do you work, what do you own, what's your stack/toolkit
- **Decision patterns** — how do you choose between options, what tradeoffs recur
- **Quality bar** — what does "great" look like, what do you reject
- **Failure modes** — what have you seen go wrong, what do you now watch for
- **Heuristics & principles** — the personal rules you've built up
- **Anti-patterns** — what you actively avoid and why
- **Taste** — subjective preferences that make your work *yours*

The interview should feel conversational. The goal isn't to fill a form — it's to surface the *implicit* knowledge the person would never think to write down.

### 2. Extract

After the interview, the AI:

- Groups raw answers into themes
- Names each recurring heuristic
- Notes contradictions (these are usually where the best insights hide)
- Pulls out the person's vocabulary — the specific words they use for concepts
- Identifies the decisions they make **differently from the textbook**

### 3. Synthesize — the Cognitive Clone

The core output. Schema lives in [`_shared/templates/cognitive-clone.template.md`](_shared/templates/cognitive-clone.template.md). A cognitive clone has six sections:

1. **Identity & Context** — who, role, domain, stack, company shape
2. **Mental Models** — the models they use to think (e.g. "backend is a state machine", "copy is a conversation you're interrupting")
3. **Heuristics** — named, reusable rules of thumb
4. **Decision Procedures** — step-by-step workflows for recurring decisions
5. **Quality Signals** — how they tell good from bad
6. **Vocabulary & Voice** — the words they use, the tone they take

### 4. Activate — the AI Environment

The cognitive clone is rewritten as a **system-prompt-ready** file: [`_shared/templates/ai-environment.template.md`](_shared/templates/ai-environment.template.md). It's tool-agnostic Markdown with a YAML header that can be dropped into any AI assistant.

Installation snippets for each target tool live in [`_shared/prompts/activation-guide.md`](_shared/prompts/activation-guide.md).

## Design principles

- **Role depth over breadth.** Better to ask 15 sharp role-specific questions than 50 generic ones.
- **Tool-neutral artifacts.** Nothing in the output assumes a specific AI vendor.
- **The clone is a document, not a prompt.** It should be readable by a human and usable by any model.
- **Make the implicit explicit.** The highest-value answers are the ones the person has never said out loud.
- **Update-friendly.** The clone is a living file. Re-run the CEET quarterly or after major role changes.

## When to use which CEET

Pick the CEET that matches the person's **primary accountability**, not their title. A "full-stack engineer" who spends 80% of their time on APIs and data should run the backend CEET. A "marketing manager" who actually writes most of the copy should run the copywriter CEET (or both).

If a person wears two hats, run two CEETs and merge the resulting clones by hand. Don't try to build a hybrid in one session — the interview questions drive the quality of the extraction, and a merged question set dilutes both.
