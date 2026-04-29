---
name: autodiscover
description: Force every execution to detect the target CEET first, validate whether it is initialized, and route to the right CEET-local skills (including Jira skill interoperability) before proceeding.
---

# Autodiscover

Use this skill at the start of any execution that depends on a CEET context.

## Mandatory behavior

1. **Detect target CEET**
   - Identify which CEET is indicated by the user request, explicit name, path, or workflow context.
   - If no CEET can be determined confidently, stop and ask for clarification.

2. **Check CEET initialization**
   - Verify whether the detected CEET is already initialized in the current workspace/session.
   - Initialization means the CEET has an available, usable template/skill structure for execution.

3. **If CEET is not initialized**
   - Ask explicitly: **"¿Deseas inicializar este CEET ahora?"**
   - If the answer is **no**:
     - Stop the current CEET flow.
     - Instruct the agent to look for and use another skill because the current one is not the right fit.
   - If the answer is **yes**:
     - Initialize the CEET following the local repository workflow.
     - Continue with CEET-local skills after initialization completes.

4. **If CEET is initialized**
   - Use only the skills/templates contained inside that CEET as the primary execution context.
   - Keep traceability from user request -> CEET -> selected local skill(s).

## Jira compatibility

Autodiscover is compatible with the `jira-agentic-requirements-pipeline` skill.

- If the discovered context is Jira-driven, run autodiscovery first, then hand off to Jira pipeline flow.
- If Jira flow references a CEET that is not initialized, apply the same initialization question and branching rules.
- Preserve sequence integrity: autodiscover gating always runs before Jira requirement discovery actions.

## Guardrails

- Never skip CEET detection and initialization checks.
- Never assume initialization state.
- Never continue with a non-initialized CEET unless user confirms initialization.
- If user rejects initialization, explicitly report mismatch and route to another skill.
