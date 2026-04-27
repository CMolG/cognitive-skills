# Full Business Question Catalog

Use this catalog to generate **non-technical** business questions from Jira tickets.

## Base filtering rule

Ask business questions only when the answer changes one or more of:

- user behavior
- product behavior
- support/backoffice operations
- legal/compliance/privacy obligations
- risk/fraud controls
- pricing/billing/plan behavior
- communications and messaging
- reporting/auditability/traceability
- rollout/migration/rollback
- UX/copy/acceptance criteria

Do **not** ask business users about implementation details (classes, methods, tables, endpoints, frameworks, libraries, architecture patterns, cache/queue internals), unless they have direct visible business impact.

---

## 1) Business Objective
- What business problem are we solving?
- What outcome should improve?
- What metric should move?
- What happens if we do nothing?

## 2) Functional Scope
- Which users/countries/channels/plans/partners are in scope?
- Does it apply to existing operations or only new ones?
- What is explicitly out of scope?

## 3) Actors & Permissions
- Who can trigger, view, override, retry, cancel, or unlock?
- How do permissions differ across user/support/admin/partner?
- What must be auditable by actor?

## 4) Business Rules
- What conditions allow or block the action?
- Which limits/thresholds/expirations/retries apply?
- What happens on duplicate/repeated/concurrent operations?

## 5) State Lifecycle
- Which states exist?
- Which transitions are allowed/blocked?
- What happens on success/error/timeout/expiration/cancelation?

## 6) Edge Cases
- What happens on double submit, refresh, reconnect, multi-device, late callback?
- What happens if data changes mid-flow?

## 7) User Experience
- What does user see before/during/after?
- Which copy is required for success/error/blocked/expired?
- Is retry/cancel/help/countdown needed?

## 8) Messages & Communications
- Which channels are required (email/SMS/push/WhatsApp/in-app)?
- When should communication be sent?
- What happens if communication fails?

## 9) Support & Backoffice
- What must support see and do?
- Are manual actions allowed (retry/cancel/unlock/override)?
- Which reason/history fields are mandatory?

## 10) Risk, Fraud & Abuse
- What is suspicious behavior?
- What limits apply (user/device/IP/account/time window)?
- What happens when risk limits are exceeded?

## 11) Legal, Compliance & Privacy
- Are consent/disclaimer/retention/audit requirements involved?
- What personal/sensitive data is processed?
- Who can access it and for how long?

## 12) Pricing, Billing & Monetization
- Is feature available across all plans?
- Does it affect credits, subscriptions, trial, refund, upsell?
- Is there additional charge or commercial limit?

## 13) Activation & Functional Configuration
- Is feature always on or configurable?
- Is activation segmented by country/user/channel/partner/percentage?
- What is default behavior if config is missing?

## 14) Rollout & Transition
- Is rollout immediate or progressive?
- Is there beta/coexistence with legacy flow?
- What triggers rollback and who approves?

## 15) Compatibility & Backward Compatibility
- What happens for old app versions and old integrations?
- Must legacy behavior remain? For how long?
- Is there minimum supported version?

## 16) Data & Functional Reporting
- What data/events must be stored and visible?
- Which KPI/report/dashboard is affected?
- Which segmentation is required (country/plan/channel/partner)?

## 17) Auditability & Traceability
- Who did what, when, from where, and why?
- Which sequence must be reconstructable?
- What retention is required?

## 18) Functional Error Handling
- Which errors are recoverable vs blocking?
- Which errors require support/manual operation?
- Which message must be shown for each case?

## 19) Business External Dependencies
- Is there dependency on provider/partner/legal/support/operations?
- What happens when dependency is unavailable?
- Is fallback continuation allowed?

## 20) Internationalization & Localization
- Are behavior/texts/formats/timezones country or language-specific?
- Who validates translations?
- Are temporary texts allowed?

## 21) Accessibility & Usability
- Are there accessibility constraints (screen reader, keyboard, contrast)?
- Is mobile/small-screen usability required?
- What level of explanatory guidance is required?

## 22) Perceived Performance
- How long can user wait before frustration?
- Should loading/progress/timeout be visible?
- Is background completion accepted?

## 23) Functional Security
- Is additional confirmation/authentication required?
- Should behavior vary by risk level?
- Is masking/notification/revocation required?

## 24) Data Quality
- Which fields are mandatory and valid?
- How to handle duplicates and conflicts?
- Should invalid data provide corrective guidance?

## 25) Priority, Severity & Criticality
- If it fails, what is business severity?
- Should support/on-call be pre-informed?
- Is low-traffic release window required?

## 26) Reversibility & Rollback
- Can feature be disabled safely?
- What happens to in-flight operations?
- Who decides rollback and on which threshold?

## 27) Migration & Existing Data
- Are existing users/operations/historical records affected?
- Is backfill/cleanup/transformation required?
- Are exceptions expected and how handled?

## 28) Out of Scope
- What is explicitly not part of this ticket?
- What is postponed to next phase?

## 29) Acceptance Criteria
- What minimum success/error/edge cases must QA validate?
- Who provides functional approval?
- What evidence is required for completion?

## 30) Rapid Decision Questions
- Mandatory vs optional?
- Visible vs hidden?
- Automatic vs manual?
- Immediate vs deferred?
- Rollout now vs later phase?

---

## Question generation schema

For every generated question include:

```json
{
  "category": "Business Rules",
  "question": "How many failed attempts are allowed before blocking the operation?",
  "whyItMatters": "Defines risk policy and avoids product assumptions.",
  "suggestedAnswers": ["3", "5", "10", "Unlimited", "Other"],
  "required": true,
  "blocksImplementation": true,
  "defaultIfUnanswered": null,
  "businessImpact": "risk",
  "affectedActors": ["user", "support"],
  "relatedAcceptanceCriteria": true
}
```

## Prioritization

- **P0 (blocks implementation):** cannot implement safely without answer.
- **P1 (blocks acceptance):** needed for QA/support/operational readiness.
- **P2 (solution quality):** valuable but not mandatory for first base branch.
- **P3 (future phase):** detect and store as optional future decisions.

## Output policy

1. Detect all potentially affected categories.
2. Draft broad internal question set.
3. Deduplicate and remove inferable technical questions.
4. Prioritize P0/P1 first.
5. Publish **5-10 required questions max**.
6. Add optional collapsed future decisions list.
