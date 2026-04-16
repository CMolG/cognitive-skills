# Interview — Backend Engineer

Ask conversationally. Don't dump all questions at once. Dig into specifics — follow-ups like "give me a recent example" are often more valuable than the scripted question itself.

## A. Context

1. Walk me through what you own end-to-end. What systems or services?
2. What's your primary stack (language, DB, queue, cache, hosting)?
3. How big is your team, and what's your seniority position inside it?
4. What scale are you operating at (rps, rows, events/day, p99 SLO)?

## B. Mental models

5. When you sit down to design a new service, what's the first thing you sketch — data model, API, sequence diagram, or something else? Why that first?
6. Do you think of your services more as "state machines," "pipelines," "event streams," or something else? Any analogy you'd use to explain your system to a new hire?
7. What's a concept you use to reason about backend work that you don't think most engineers use?

## C. Data integrity & correctness

8. Give me an example where you explicitly designed for *partial failure*. What did you do differently than the "happy path" version?
9. How do you think about idempotency — do you retrofit it or design it in upfront? When is it overkill?
10. When you see a new write path, what invariants do you immediately look for?
11. Where do you prefer to enforce constraints: database, application, message broker, or the UI? Why?

## D. Storage & API choice

12. Walk me through your decision tree for Postgres vs. something else (DynamoDB, Mongo, Redis, Kafka, S3, etc.).
13. REST vs. RPC vs. event-driven — what's your default, and what pushes you off the default?
14. How do you version APIs? What's your stance on breaking changes?
15. What's your default approach to pagination, filtering, and search? What smell makes you reject a proposed API shape?

## E. Performance & scale

16. When a service is slow, what's the first thing you check? Second?
17. Describe a time you picked *latency* over *consistency* (or vice versa) — what made the call?
18. What's your instinct around caching — where do you reach for it, where do you refuse to?
19. How do you decide when a query needs an index vs. a rewrite vs. a denormalization?

## F. Observability & ops

20. What do you instrument *before* shipping a new endpoint?
21. What metric or dashboard do you watch after a deploy?
22. What's your stance on log levels, structured logging, and what belongs in traces?
23. What alert would you never page on? What alert do you think everyone under-uses?

## G. Code review & quality

24. When you open a teammate's PR, what are the first three things your eye goes to?
25. What makes you say "this needs a refactor" — what's the trigger?
26. What's something you consistently flag in reviews that most engineers don't?
27. What's the difference between code you'd ship to prod vs. code you'd ship to a hackathon demo?

## H. Failure & scar tissue

28. Tell me about an incident that permanently changed how you code.
29. What's a bug you've shipped that you still think about?
30. What's a class of bug you've become allergic to, and how do you prevent it now?

## I. Heuristics & principles

31. What's a rule of thumb you apply that's *not* in a textbook?
32. Finish the sentence: "Most backend engineers get X wrong, and the fix is Y."
33. What's the shortest-worded piece of advice you'd give to a mid-level engineer joining your team?

## J. Vocabulary & voice

34. Are there words or phrases you deliberately avoid when writing docs or PR descriptions?
35. Are there terms you insist on (your team's local vocabulary for something standard)?
36. When you write a postmortem, what's the tone — clinical, narrative, blameless?

## K. Taste

37. What does a "beautiful" backend codebase look like to you? Name a real example if you have one.
38. What's something you do purely out of taste that you can't fully justify, but you'd fight to keep?

## L. Anti-patterns

39. What's the thing you refuse to do, no matter the pressure? (And what's the story behind the line?)
40. What's a pattern that looks clever but you've learned to distrust?

---

*Wrap: read the extracted themes back to the interviewee. If they don't recognize themselves, re-interview the misaligned section.*
