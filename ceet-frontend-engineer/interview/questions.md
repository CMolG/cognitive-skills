# Interview — Frontend Engineer

## A. Context

1. What surface do you own (marketing site, app, design system, internal tools)?
2. What's your framework + build + styling stack?
3. Who are your users (consumer, B2B, internal), and what's their typical device / network?
4. How large is your component library or design system, and are you a consumer or author of it?

## B. Mental models

5. When you see a new screen in a design file, what do you mentally break it into first — layout regions, components, data dependencies, or states?
6. Do you think of a component primarily as a *unit of data*, a *unit of markup*, a *unit of behavior*, or a *unit of visual identity*? Has that answer changed over your career?
7. How do you explain "reactive UI" to someone who's never written any?

## C. State

8. What goes in local state, what gets lifted, what belongs in a store, and what belongs in the URL?
9. Server state vs. client state — where do you draw the line, and what library/pattern do you reach for?
10. What's an anti-pattern around state that you see constantly in other people's code?
11. Tell me about a time you regretted a state choice. What did you learn?

## D. Component architecture

12. What makes a component "too big" for you? What's your refactor trigger?
13. How do you feel about prop-drilling, render props, slots, composition, and context? Rank them, roughly.
14. Do you design for *composition* or *configuration* first? Example?
15. What's a component pattern you reach for that most people don't?

## E. Styling & design system

16. Utility classes, CSS modules, CSS-in-JS, plain CSS, vanilla-extract — what's your stack and *why that one*?
17. How do you handle design tokens and theming?
18. What's your stance on custom components vs. using a UI kit (Radix, shadcn, Headless UI, Chakra, etc.)?
19. Where do you refuse to deviate from the design system, and where do you allow local overrides?

## F. Rendering & performance

20. SSR vs. SSG vs. CSR vs. streaming vs. islands — when do you pick which?
21. Which Web Vital do you chase first (LCP, INP, CLS)? What's your workflow when it regresses?
22. What's your approach to code-splitting and bundle size?
23. What images / media strategy do you default to?

## G. Accessibility

24. Walk me through what you check before merging a component. (If they don't say "keyboard," probe specifically.)
25. What ARIA pattern do you reach for most often, and which one do you consistently see people misuse?
26. What's your stance on "div soup"? How militant are you on semantic HTML?
27. What automated / manual a11y checks are in your workflow?

## H. Forms & validation

28. Where does validation live — on blur, on submit, on every keystroke? Why?
29. How do you design error states? Inline, summary, toast, field-level, or combination?
30. What's your default for controlled vs. uncontrolled inputs?

## I. Motion & micro-interactions

31. Where do you add motion deliberately? Where do you refuse?
32. What's a UI animation you consider a smell / overused?
33. Default duration, easing, and reduced-motion stance?

## J. Empty / loading / error

34. Do you design all four states (empty, loading, error, success)? If not, which do you skip and why?
35. Skeletons vs. spinners vs. optimistic UI — your defaults?

## K. Testing

36. Unit / component / integration / E2E / visual regression — what's your mix and where does each live?
37. What do you refuse to test? What do you over-test?
38. When do you reach for a Storybook-like tool, and what do you put in it?

## L. Taste & heroes

39. Name 2-3 websites or apps whose frontend craft you admire. What specifically?
40. What's a UI pattern that looks fashionable right now but you distrust?
41. What's a small detail (focus rings, loading behavior, hover states) you care about that others overlook?

## M. Anti-patterns

42. What do you consistently reject in PRs?
43. What's a pattern you outgrew — used to love, now avoid?

## N. Vocabulary

44. Any local vocabulary for components or patterns? (e.g. "composer", "island", "shell", "chrome"...)
45. Any words you refuse to use ("beautiful", "clean", "slick", "pop")?

---

*Wrap: have the interviewee read back the extracted mental models and heuristics. Re-interview anything that doesn't feel like them.*
