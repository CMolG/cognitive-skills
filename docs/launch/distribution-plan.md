# Distribution plan

A short list of places to submit cognitive-skills once a tagged
release is out. Order matters: HN and Lobsters are the loudest,
directories are evergreen.

## Discussion sites

| Destination | Format | Notes |
|---|---|---|
| Hacker News | "Show HN: cognitive-skills — turn an expert's judgment into a portable AI prompt" | Submit between 14:00–17:00 UTC on a Tuesday/Wednesday. Lead with the demo, not the methodology. |
| Lobsters | Show post tagged `ai`, `practices`, `release` | Title without "Show:". Keep the body to 4 paragraphs. |
| r/MachineLearning | `[P]` flair, project category | Lead with the eval harness. The audience reacts well to "no LLM judge, deterministic metrics". |
| r/programming | Link post with a 2-line pitch | Avoid jargon in the title. Cite the PR-review before/after. |
| Reddit r/ChatGPT, r/ClaudeAI, r/Cursor | Same project, host-specific framing | Adapt the example to that tool's loading mechanism. |
| dev.to | Long-form article | Reuse `docs/launch/launch-post.md`, add screenshots of the harness output. |

## Awesome lists

| Destination | What to submit | Pull request location |
|---|---|---|
| `awesome-claude-skills` | A line under "Skill collections" with the repo URL | <https://github.com/awesome-lists/> (pick the most active fork) |
| `awesome-llm-tools` | "Cognitive extraction toolkit" entry | search the most-starred fork |
| `awesome-prompts` | Entry under "Role-based prompts" | one-liner describing CEETs |
| `awesome-skills` (Anthropic ecosystem) | Add the repo with a 1-sentence description | once the official list exists |

## Other surfaces

- **GitHub topics**: `claude-skills`, `cognitive-extraction`, `llm-prompts`, `system-prompt`, `jira-automation`, `agentic-pipeline`. Add via repo settings.
- **GitHub social preview**: render a 1280×640 image with the hero one-liner. Save under `docs/launch/social-preview.png` and configure in repo settings.
- **OpenGraph metadata** (if/when the project gets a landing page): `og:title`, `og:description`, `og:image`.
- **Anthropic skill registry / MCP App registry**: monitor for the right submission channel; not yet a clear destination as of 2026-05-07.

## Pre-launch checklist

- [ ] All tests green: `pytest tests/ -q`
- [ ] CHANGELOG entry for the release version
- [ ] Tag created (`git tag v1.2.0 && git push --tags`)
- [ ] README hero matches launch post phrasing
- [ ] `examples/ready-to-use/demo-jira-pipeline.sh` records cleanly:
      `asciinema rec demo.cast --command "bash examples/ready-to-use/demo-jira-pipeline.sh"`
- [ ] Demo GIF embedded in the README under the 60-second example
- [ ] Eval seed report exists and is linked from the README

## Post-launch

- Reply to every top-level comment on HN within the first 4 hours.
- If the eval-harness-without-judge angle gets traction, write a
  follow-up post focused on "why we did not use LLM-as-judge" with
  the receipts.
- Watch issues; the most useful early signal is which CEETs people
  open first (it tells you which roles people want to extract).
