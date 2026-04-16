# How to Use CEET

> A practical, step-by-step guide for running a CEET extraction.

---

## Step 1: Pick Your Role

Browse the `ceet-*/` folders at the project root and pick the one that best matches your primary working identity. You can run CEET multiple times — one per role — if you wear multiple hats.

Common pairings:
- Technical founder → `founder-ceo` + `backend-engineer` or `frontend-engineer`
- Designer-developer → `ui-designer` + `frontend-engineer`
- Growth person → `marketing` + `copywriter`
- Solo operator → `founder-ceo` + whatever else you spend most time on

Running multiple roles is deliberate: each produces its own profile. Do not try to merge.

---

## Step 2: Open the Role's Skill File in Your AI

Open `ceet-{your-role}/SKILL.md` in the AI assistant of your choice (Claude, ChatGPT, Cursor chat, etc.). These files are designed as interview scripts the AI will execute.

Tell the AI: **"Please run a CEET interview for me using this skill."**

The AI will:
1. Read `METHODOLOGY.md` (if linked) or ask you to paste it
2. Read the role's `questions.json`
3. Begin the interview — 15 universal questions first, then 40 core questions, then optionally 30 extension questions
4. Save responses verbatim, reflect between sections, probe when answers are generic

---

## Step 3: Answer Honestly and Specifically

Time investment: **60–90 minutes for core**, **+30–45 minutes for extension**.

Quality guidelines:

- **Be specific.** "I like clean code" is useless. "I set my linter to error on any `any` in TypeScript and I do not merge PRs that add them" is useful.
- **Use real examples.** Stories from the last 30 days beat abstract principles.
- **Include exceptions.** "I always X, except when Y" is gold.
- **Surface your contradictions.** If you say one thing in U01 and another in C16, the AI will notice — help it.
- **Do not perform.** The goal is not to look good. It is to be cloned accurately.

---

## Step 4: Review the Synthesis

After the interview, the AI will produce:

- `cognitive-profile.json` — machine-readable profile
- `cognitive-profile.md` — human-readable version

Read the `cognitive-profile.md`. Pay attention to:

- **Cognitive signature** — does it sound like you?
- **Core values** — are these actually your values, or did the AI invent?
- **Contradictions** — are these real, useful tensions?
- **Blind spots** — any that sting? (If yes, it is working.)

If something is wrong, push back. The AI should revise based on your correction, not argue.

---

## Step 5: Generate Artifacts

After profile approval, tell the AI: **"Generate my artifact bundle."**

It will produce the full bundle described in [`tool-integration.md`](tool-integration.md):

```
output/
├── cognitive-profile.json
├── cognitive-profile.md
├── agents/
├── skills/
├── commands/
├── rules/
├── hooks/              (engineering roles only)
└── _source_map.md
```

---

## Step 6: Load Into Your AI Tool

See `docs/tool-integration.md` for tool-specific instructions. Short version:

- **Claude:** Project knowledge
- **ChatGPT:** Custom Instructions or Custom GPT knowledge
- **Cursor:** `.cursor/rules/`
- **Copilot:** `.github/copilot/`
- **Windsurf:** `.windsurf/rules/`
- **Any other:** Paste the relevant files into the system prompt

---

## Step 7: Test the Clone

Ask your AI to do something you would normally do — a code review, a headline, a pricing decision, a hiring feedback note.

Red flags the clone is not you yet:

- Generic advice instead of your specific rules
- Textbook answers where you would give pointed ones
- Missing your voice, cadence, or catchphrases
- Making decisions the opposite way you would

When you spot these, identify which directive is weak. Edit `cognitive-profile.json` directly (or re-run the relevant question) and regenerate the affected artifacts.

---

## Step 8: Re-profile Periodically

Your cognitive profile drifts. Rules you had 2 years ago may no longer reflect how you work. Plan to re-run CEET **every 6–12 months**, or after a significant role change.

On re-run:
- Existing profile is loaded
- You are shown your previous answers for each question
- You say what has changed (if anything)
- Only affected directives and artifacts regenerate
- A `profile-changelog.md` records what moved

---

## FAQ

**Q: Can I skip the universal questions?**
No. They anchor the identity synthesis. Role questions without universal context produce shallow clones.

**Q: Can I do the interview in multiple sessions?**
Yes. Save progress between sections. Resume by pasting the partial raw-responses JSON.

**Q: What if my answers contradict?**
Good. Contradictions are the most valuable data CEET captures. The AI will surface them and ask clarifying questions, not punish them.

**Q: Can I run this on a colleague?**
Yes, if they consent. The output is a cognitive clone — treat it with the same sensitivity as a detailed personality profile.

**Q: What if I hate the synthesis?**
Tell the AI which parts feel wrong and why. The AI should revise based on your specific objection, not rewrite everything.

**Q: Can I hand-edit the profile?**
Yes. The profile is plain JSON + markdown. Edit directly. Just maintain the `[Q-ID]` traceability references so future re-profiling works.
