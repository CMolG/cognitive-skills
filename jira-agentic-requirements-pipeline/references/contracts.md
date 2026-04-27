# Internal contracts

## Example Data Policy

All examples in this document must use fictional, generic domains.

Do not use:
- real project names
- real issue keys
- real product flows
- real business rules
- real operational incidents
- real customer, company or domain-specific terminology
- examples derived from internal conversations, tickets, repositories or production systems

Examples should be intentionally neutral and non-identifiable.

Preferred fictional domains include:
- content_publishing
- course_enrollment
- warehouse_reservation
- appointment_booking
- subscription_upgrade
- document_review
- event_registration
- inventory_restock

## TicketAnalysis

```json
{
  "issueKey": "APP-4827",
  "title": "Enable approval step for premium content publishing",
  "detectedDomain": "content_publishing",
  "confidence": 0.88,
  "businessGoal": "Reduce accidental publication of premium content before final review",
  "missingBusinessDecisions": [
    "applicable_content_types",
    "approval_deadline",
    "reviewer_roles",
    "rejection_behavior",
    "notification_policy"
  ]
}
```

## BusinessQuestion

```json
{
  "id": "Q3",
  "priority": "P0",
  "category": "Business Rules",
  "question": "How many reviewers must approve premium content before it can be published?",
  "whyItMatters": "Defines the functional approval threshold and blocks implementation if unknown.",
  "suggestedAnswers": [
    "1 reviewer",
    "2 reviewers",
    "Majority of assigned reviewers",
    "All assigned reviewers",
    "Other"
  ],
  "required": true,
  "blocksImplementation": true,
  "defaultIfUnanswered": null,
  "businessImpact": "workflow_control",
  "affectedActors": ["content_editor", "reviewer", "publisher"],
  "relatedAcceptanceCriteria": true
}
```

## BusinessQuestionSet

```json
{
  "issueKey": "APP-4827",
  "status": "WAITING_BUSINESS_INPUT",
  "summary": "Business decisions are missing before a safe base-branch can be prepared for the publishing approval workflow.",
  "questions": [],
  "optionalFutureDecisions": []
}
```

## FunctionalContract

```json
{
  "issueKey": "APP-4827",
  "functionalContract": {
    "approvalRequiredFor": "premium_content_before_publication",
    "minimumApprovalsRequired": 2,
    "approvalDeadlineHours": 24,
    "allowSelfApproval": false,
    "rejectionRequiresReason": true,
    "notifyEditorsOnDecision": true,
    "featureToggleRequired": true
  }
}
```

## BaseBranchPlan

```json
{
  "branchName": "ai/APP-4827-premium-content-approval-base",
  "implementationScope": [
    "Add approval-required decision point before publishing premium content",
    "Add reviewer decision workflow",
    "Prevent publication until the required approval threshold is reached",
    "Record approval and rejection decisions with business-visible reasons",
    "Notify editors when content is approved or rejected"
  ],
  "excludedScope": [
    "editorial dashboard redesign",
    "advanced reviewer assignment rules",
    "bulk approval operations",
    "analytics reporting"
  ],
  "requiresHumanReview": true
}
```
