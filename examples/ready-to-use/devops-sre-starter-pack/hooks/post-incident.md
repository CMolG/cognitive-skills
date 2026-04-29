<!-- CEET Source:
  Role: devops-sre
  Directives: postmortem.*
-->

# post-incident Hook — {engineer_name}

> Enforces {engineer_name}'s exact post-incident standards.

## Trigger

After every incident resolution


## Postmortem Trigger

{directives.postmortem.blameless_definition}

Schedule postmortem within 48h.

## Action Items

{directives.postmortem.action_tracking}

Create tracked action items.

## Communication

Send incident summary to stakeholders per comms ownership rules.

## On Failure

When a gate fails:
1. Report which specific rule was violated
2. Quote the directive that defines the rule
3. Show the fix if possible
4. Do not silently pass — block until resolved or explicitly overridden