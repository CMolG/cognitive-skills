<!-- CEET Source:
  Role: {role}
  Hook: {hook_name}
  Directives: {directive_paths}
  NOTE: Hooks apply only to engineering roles (backend, frontend, devops-sre, data-analytics).
-->

# {hook_name} Hook — {person_name}

> Automation trigger executed at {hook_trigger_point} using {person_name}'s exact gates.

---

## Trigger

{trigger_description}

---

## Gates

{numbered_gates_block}

---

## On Failure

When a gate fails:

1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden by the user
