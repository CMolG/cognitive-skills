# Interview — Data / Analytics

## A. Context

1. What's your role and who do you report into?
2. What's your stack (warehouse, transformation, BI, notebooks, ML tools)?
3. Who are your primary stakeholders (product, growth, finance, exec)?
4. What decisions does your team's work actually drive?

## B. Question framing

5. A stakeholder comes with a vague question. Walk me through how you reshape it into something answerable.
6. What's a question you routinely refuse to answer, or reframe, before working on it?
7. How do you decide whether a question needs a dashboard, a one-off analysis, or a model?

## C. Metric design

8. What makes a metric good or bad in your view?
9. How do you think about *input* vs. *output* metrics? Leading vs. lagging?
10. Give me an example of a metric you designed that was gameable — what happened, what did you change?
11. How do you name metrics? Any conventions you insist on?

## D. Data quality

12. Before you trust a new table, what do you check?
13. How do you smell a bad join? What does "suspicious" look like?
14. What's your stance on staging models, tests, and freshness in dbt (or equivalent)?
15. What's an error class in data you've become allergic to?

## E. Statistical rigor

16. RCT, diff-in-diff, synthetic control, observational — when do you reach for which?
17. How do you talk about uncertainty in a write-up? What phrases do you avoid?
18. What's your practice around multiple comparisons?
19. When do you trust a p-value, and when do you not?

## F. Modeling

20. Simple vs. complex — where's your default?
21. How do you know a model is "good enough" to ship?
22. What's your monitoring story for a deployed model?
23. What's a model-building shortcut you used to take and now refuse?

## G. Experimentation

24. How do you set up a power calculation / MDE for a new experiment?
25. What guardrail metrics do you always include?
26. What's your stance on peeking / sequential testing / early stopping?
27. How do you handle experiments that "fail to reject" — what do you tell the stakeholder?

## H. Tools & workflow

28. SQL dialect you write in, pandas vs. Polars vs. DuckDB, viz library — pick your defaults and tell me why.
29. Notebooks vs. scripts vs. dbt — where does each belong?
30. What's in your personal utility library / snippets?

## I. Communication

31. How do you structure a write-up — TL;DR first? Methods first? Story arc?
32. What's your stance on charts — bar vs. line vs. small multiples vs. tables?
33. What phrase do you use when asked "can you just give me the number?" and the answer is "not really"?

## J. Heuristics

34. "I always {X} before trusting a new data source."
35. "If a metric moves more than {X}%, I immediately check {Y}."
36. "A good experiment pre-registers {X}."

## K. Vocabulary

37. Any local terms (e.g. "north star", "guardrail", "canary metric", "kitchen-sink model")?
38. Any words you refuse to use in write-ups ("proves", "causes", "significant" without context)?

## L. Anti-patterns

39. What's a chart type or analysis pattern you consistently reject?
40. What's a common data request you push back on, and how do you reframe it?

## M. Worked example

41. Walk me through the last real analysis you did — end to end. Every branch, every rejection, every "I almost did X but did Y because…".

---

*That final worked example is where most of the best heuristics live. Treat it as a long, open-ended question.*
