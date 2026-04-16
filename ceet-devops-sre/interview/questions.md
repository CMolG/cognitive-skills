# Interview — DevOps / SRE

## A. Context

1. What do you own — cloud accounts, clusters, pipelines, platform abstractions? Describe the surface area.
2. What's your stack (cloud, orchestrator, IaC tool, CI, observability)?
3. What's your team shape (embedded SRE, platform team, solo)?
4. What scale & reliability targets are you operating against (SLOs, uptime, MTTR)?

## B. Mental models

5. How do you mentally represent your system — as a topology, a dependency graph, a flow of requests, a set of control loops? Why that one?
6. What's the analogy you use to explain reliability to non-engineers?
7. What do you believe about reliability that most teams get wrong?

## C. SLOs & error budgets

8. Do you run on SLOs? If so, how do you pick them? If not, what do you use instead?
9. When an error budget burns, what changes in your week?
10. How do you negotiate reliability vs. feature velocity with product?

## D. Observability

11. Logs / metrics / traces / profiles / events — what do you instrument first on a new service?
12. What's the one dashboard you open during an incident? What's on it?
13. What alert rule have you found most false-positive-prone, and how did you fix it?
14. What's the difference between a page, a ticket, and a log-only event in your world?

## E. Change & release

15. Canary / blue-green / feature flags / progressive rollout — which is your default and when do you deviate?
16. How do you think about deploy risk, and what's your pre-deploy checklist?
17. What change do you require a second reviewer for, no exceptions?
18. What's your rollback philosophy — always possible, practiced, or last resort?

## F. Incident response

19. Walk me through the first 5 minutes of a sev-1 in your system.
20. Who owns the comms vs. the fix? How do you run the incident channel?
21. What's a rule you apply in incidents that junior engineers routinely violate?
22. Name one incident that permanently changed how you think. What's the story?

## G. Postmortems

23. Blameless — what does that actually mean in your writing?
24. Mandatory sections in your postmortems? Forbidden phrases?
25. How do you track action items after they're written — and what % actually get done?

## H. Toil & automation

26. What do you consider toil, and what's your team's policy on it?
27. What's a task you deliberately haven't automated, and why?
28. What's a manual workaround you've done 3+ times that you *should* have automated sooner?

## I. IaC & platform taste

29. Terraform / Pulumi / Crossplane / CDK — what's your stack and honest opinions?
30. How do you structure modules / workspaces / state? What's your versioning story?
31. Where do you allow "click-ops," and where do you refuse?
32. What's your stance on internal developer platforms (Backstage, Humanitec, etc.) — golden path vs. paved road vs. optional?

## J. Security

33. Secret management — vault, sops, cloud native? Why?
34. What least-privilege pattern do you insist on?
35. What's a security shortcut you see often and always reject?

## K. Cost

36. How much does cost enter your daily thinking?
37. What's a cost optimization that's worth it, and one that's a trap?
38. How do you explain a surprise bill to finance?

## L. Vocabulary & voice

39. Any local words your team uses for services, environments, or deploy stages?
40. What tone do you write runbooks in — imperative, narrative, checklist?
41. What postmortem phrase do you ban ("human error")?

## M. Heuristics

42. "If a service doesn't have X, I don't let it go to prod."
43. "When my pager goes off for Y, I immediately check Z."
44. "When someone says 'we just need to add more instances', my first question is…"

## N. Anti-patterns

45. What pattern do you see shops do that makes you wince?
46. What's something that looked like best practice 5 years ago that you now avoid?

---

*Wrap: do a "mock page" — describe a fake incident and have them narrate their first 5 minutes. Those narrations encode more heuristics than scripted questions.*
