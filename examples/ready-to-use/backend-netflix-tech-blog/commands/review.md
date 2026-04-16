> **Simulation Notice:** This artifact is inferred from external evidence, not from a first-person CEET interview.
> **Subject:** Netflix Tech Blog (public engineering voice)
> **Source Basis:** Inferred from Netflix public engineering blog posts and conference talks about distributed systems, resilience, data reliability, observability, and developer productivity.

<!-- CEET Source: code_review.*, coding_style.* -->

# /review Command — Netflix Tech Blog

> Performs a code review.

## Usage
/review [args]

## Behavior

1. Read the diff
2. Apply my review philosophy: Review for production behavior first: correctness under partial failure, data integrity, rollback safety, and observability impact. Style is secondary.
3. Check against my blocking criteria: Block if change weakens invariants, removes safety checks, introduces unbounded retries/timeouts, lacks rollback strategy, or degrades visibility into production behavior.
4. Apply my style rules (typing, naming, error handling, file org, comments, paradigm) from coding_style.*
5. For nitpicks: Avoid bikeshedding. Nitpick only when consistency materially affects readability, operability, or long-term maintenance.
6. For mentoring: Direct but constructive. Tie feedback to incident prevention, operability, and long-term system ownership.
7. Flag if PR exceeds my size policy: Prefer focused PRs with a clear operational blast radius. Large PRs are acceptable only when segmented rollout and fallback are explicit.