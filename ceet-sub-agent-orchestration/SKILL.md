---
name: ceet-sub-agent-orchestration
description: Orchestrate complex CEET executions by delegating independent role-based tasks to sub-agents, each with its own CEET context, and consolidating validated outputs.
---

# CEET Sub-Agent Orchestration

Use this skill when a task is complex enough to benefit from specialized parallel execution.

## Purpose

Act as a coordinator ("jefe") that plans, delegates, validates, and merges work produced by multiple specialized sub-agents.

## Mandatory workflow

1. **Assess orchestration fit**
   - Confirm the task contains multiple specialized roles or workstreams.
   - Prefer independent sub-tasks to avoid conflicts.

2. **Plan role-based decomposition**
   - Define explicit sub-agents by role.
   - Assign each one a clear, bounded scope, input, and expected output.
   - Ensure no sub-agent depends on another sub-agent's in-flight edits.

3. **Bind CEET per sub-agent**
   - Use a dedicated CEET context per role when available.
   - If a required CEET is missing for a role, use preconfigured CEETs automatically (no per-role manual confirmation).

4. **Conflict prevention strategy**
   - Default: split work into independent tasks operating on non-overlapping files.
   - If full independence is not possible:
     - Isolate each sub-agent in temporary folders/workspaces.
     - Let orchestrator reconcile and combine results after execution.

5. **Execute sub-agents**
   - Dispatch all defined role tasks.
   - Track outputs and execution status per role.

6. **Validate and consolidate (orchestrator responsibility)**
   - Review outputs for consistency, quality, and alignment with user goal.
   - Resolve overlaps or contradictions.
   - Merge into a single coherent final result.

7. **Return final integrated delivery**
   - Provide consolidated output plus a short execution trace (roles, tasks, merge decisions).

## Guardrails

- Never delegate without explicit role boundaries.
- Never allow uncontrolled overlapping edits between sub-agents.
- Never skip orchestrator validation before final output.
- Always prefer deterministic merge criteria over ad-hoc combination.
