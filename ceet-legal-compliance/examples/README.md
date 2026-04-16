# Examples — CEET Legal / Compliance

This directory contains example outputs from completed CEET extractions for the Legal / Compliance role.

## What you'll find here after running a CEET

After completing a CEET extraction, this directory will contain:

- **`cognitive-clone.md`** — Portable cognitive clone of the extracted individual
- **`ai-environment.md`** — System-prompt-ready configuration for any AI tool

## How to generate

1. Open `../SKILL.md` in your AI assistant
2. Tell the AI: "Please run a CEET interview for me using this skill."
3. Complete the interview (~60–90 minutes)
4. Review and approve the synthesis
5. The AI will generate all artifacts into this directory

## Using the output

See the activation guide for loading into specific AI tools:
- **Claude:** Paste into project knowledge
- **ChatGPT:** Custom Instructions or Custom GPT knowledge
- **Cursor:** `.cursorrules` at repo root
- **Copilot:** `.github/copilot-instructions.md`
- **Any tool:** Paste into system prompt
