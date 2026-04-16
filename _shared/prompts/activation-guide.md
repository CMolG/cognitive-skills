# Activation guide — installing a CEET output in any AI tool

After a CEET produces `cognitive-clone.md` and `ai-environment.md`, use the snippets below to load them into the tool of your choice. Nothing here is vendor-locked — the files are plain Markdown.

## Claude (claude.ai, Claude Projects, Claude API)

- **Claude Projects:** Open the Project → *Edit* → paste the contents of `ai-environment.md` into **Custom Instructions**.
- **Claude API / SDK:** Pass `ai-environment.md` as the `system` prompt string. Optionally include `cognitive-clone.md` as an attached file or the first user message for deeper context.
- **Claude.ai chat:** Start the conversation with: *"Use the following as your operating context:"* and paste `ai-environment.md`.

## ChatGPT (chatgpt.com, custom GPTs, API)

- **Custom GPT:** Create a new GPT → paste `ai-environment.md` into **Instructions**. Upload `cognitive-clone.md` to **Knowledge** for retrieval.
- **Custom instructions:** Paste into the *"How would you like ChatGPT to respond?"* field.
- **OpenAI API:** Use `ai-environment.md` as the `system` role message.

## Cursor

Create `.cursorrules` at the repo root and paste the contents of `ai-environment.md`. Cursor will include it as context in every request.

## GitHub Copilot

Create `.github/copilot-instructions.md` at the repo root and paste `ai-environment.md`. Copilot Chat will use it automatically.

## Gemini (Gems, API)

- **Gems:** Create a new Gem → paste `ai-environment.md` into the instructions.
- **Gemini API:** Use as `systemInstruction`.

## Perplexity

Paste `ai-environment.md` into the Collection's system prompt, or prepend it to each query.

## Any other tool

If the tool accepts a system prompt, a "persona" field, or a rules file, paste `ai-environment.md`. If it only accepts a first-turn user message, start the conversation with:

```
Use the following as your persistent operating context for everything that follows:

<paste ai-environment.md here>
```

## Maintenance

Re-run the CEET when any of the following change:

- The person's role, team, or company
- Their stack or primary tools
- Lessons from a major incident or success
- Quarterly, as a default refresh cadence

Bump the `version` in both files each time and archive the previous version.
