---
name: autodiscover
description: Force every execution to detect the target CEET first, validate whether it is initialized, and route to the right CEET-local skills (including Jira skill interoperability and sub-agent orchestration) before proceeding.
---

# Autodiscover

Use this skill at the start of any execution that depends on a CEET context.

## Mandatory behavior

1. **Detect target CEET (deterministic first, then judgment)**
   - Run `python3 autodiscover/scripts/detect.py --request "<user request>"`
     to get a structured `{detectedCEETs, initializedCEETs, scoring,
     recommendation}` report. The script scans the workspace for
     `ceet-*` folders and matches the request against per-role
     keywords. It is pure stdlib, no model needed.
   - Use the report's `recommendation.primary` as the starting point.
   - Override the script only if the user request contains an
     explicit CEET name or path that the keyword matcher missed —
     never silently disagree.
   - If `recommendation.primary` is `null`, stop and ask for
     clarification.

2. **Check CEET initialization**
   - Verify whether the detected CEET is already initialized in the current workspace/session.
   - Initialization means the CEET has an available, usable template/skill structure for execution.

3. **If CEET is not initialized**
   - Ask explicitly: **"Do you want to initialize this CEET now?"**
   - If the answer is **no**:
     - Ask explicitly before exiting CEET flow: **"You do not have your own CEET initialized. Do you want to use an example CEET before continuing without CEET?"**
     - If the answer is **yes**:
       - Select a relevant CEET example available in the repository.
       - Continue the execution under that example CEET context.
     - If the answer is **no**:
       - Stop the current CEET flow.
       - Instruct the agent to look for and use another skill because the current one is not the right fit.
   - If the answer is **yes**:
     - Initialize the CEET following the local repository workflow.
     - Continue with CEET-local skills after initialization completes.

4. **If CEET is initialized**
   - Use only the skills/templates contained inside that CEET as the primary execution context.
   - Keep traceability from user request -> CEET -> selected local skill(s).

5. **Complex task orchestration option**
   - If planning reveals a complex task with distinct specialized roles, ask explicitly: **"Do you want us to launch different subagent roles to execute this in parallel and then consolidate it?"**
   - If the answer is **yes**, hand off to the `ceet-sub-agent-orchestration` skill.
   - If the answer is **no**, continue with single-agent CEET execution.

## Sub-agent orchestration compatibility

Autodiscover is compatible with the `ceet-sub-agent-orchestration` skill.

- Use orchestration only when work can be decomposed into independent role-based tasks or partitioned safely.
- If required role CEETs are missing, orchestration should use preconfigured CEETs automatically without asking for per-role manual confirmation.
- The orchestrator validates all sub-agent outputs before final delivery.

## Jira compatibility

Autodiscover is compatible with the `jira-agentic-requirements-pipeline` skill.

- If the discovered context is Jira-driven, run autodiscovery first, then hand off to Jira pipeline flow.
- If Jira flow references a CEET that is not initialized, apply the same initialization question and branching rules.
- Preserve sequence integrity: autodiscover gating always runs before Jira requirement discovery actions.

## Guardrails

- Never skip CEET detection and initialization checks.
- Never assume initialization state.
- Never continue with a non-initialized CEET unless user confirms initialization or explicitly chooses an example CEET.
- If user rejects both initialization and example CEET usage, explicitly report mismatch and route to another skill.
- Never run sub-agent orchestration without clear task decomposition criteria.
