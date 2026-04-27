#!/usr/bin/env python3
"""CLI for an agentic requirements pipeline connected to Jira.

Commands:
- fetch-issue
- discovery
- generate-questions
- collect-input
- resolve-contract
- base-branch-plan
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_STATE_FILE = ".jira_requirement_state.json"
MAX_REQUIRED_QUESTIONS = 10
MIN_REQUIRED_QUESTIONS = 5


@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_jira_config() -> JiraConfig:
    base_url = os.getenv("JIRA_BASE_URL", "").strip().rstrip("/")
    email = os.getenv("JIRA_EMAIL", "").strip()
    api_token = os.getenv("JIRA_API_TOKEN", "").strip()

    missing: list[str] = []
    if not base_url:
        missing.append("JIRA_BASE_URL")
    if not email:
        missing.append("JIRA_EMAIL")
    if not api_token:
        missing.append("JIRA_API_TOKEN")

    if missing:
        raise SystemExit(f"Missing Jira environment variables: {', '.join(missing)}")

    return JiraConfig(base_url=base_url, email=email, api_token=api_token)


def jira_get(config: JiraConfig, path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
    query_str = ""
    if query:
        query_str = "?" + urllib.parse.urlencode(query)

    url = f"{config.base_url}{path}{query_str}"
    auth = base64.b64encode(f"{config.email}:{config.api_token}".encode("utf-8")).decode("ascii")

    req = urllib.request.Request(url)
    req.add_header("Authorization", f"Basic {auth}")
    req.add_header("Accept", "application/json")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise SystemExit(f"Jira HTTP {exc.code}: {body}") from exc


def extract_text_from_jira_node(node: Any) -> str:
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        return ""

    chunks: list[str] = []

    def walk(obj: Any) -> None:
        if isinstance(obj, dict):
            if obj.get("type") == "text" and obj.get("text"):
                chunks.append(obj["text"])
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    walk(node)
    return " ".join(chunks).strip()


def fetch_issue(args: argparse.Namespace) -> int:
    config = get_jira_config()
    payload = jira_get(
        config,
        f"/rest/api/3/issue/{args.issue_key}",
        query={"fields": "summary,description,labels,comment,customfield_10011,status"},
    )

    fields = payload.get("fields", {})
    comments = fields.get("comment", {}).get("comments", [])

    normalized = {
        "issueKey": payload.get("key"),
        "title": fields.get("summary", ""),
        "description": extract_text_from_jira_node(fields.get("description")),
        "labels": fields.get("labels", []),
        "epic": fields.get("customfield_10011"),
        "status": (fields.get("status") or {}).get("name"),
        "comments": [
            {
                "author": ((c.get("author") or {}).get("displayName") or "unknown"),
                "body": extract_text_from_jira_node(c.get("body")),
                "created": c.get("created"),
            }
            for c in comments
        ],
        "acceptanceCriteria": [],
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
    }

    output = Path(args.output)
    write_json(output, normalized)
    print(f"Issue exported to {output}")
    return 0


def discovery(args: argparse.Namespace) -> int:
    issue = load_json(Path(args.input))
    text = build_ticket_text(issue)

    detected_categories = detect_category_signals(text)

    analysis = {
        "issueKey": issue.get("issueKey"),
        "title": issue.get("title"),
        "businessGoal": infer_business_goal(issue.get("title", ""), issue.get("description", "")),
        "functionalEntities": detect_entities(text),
        "userActions": infer_user_actions(text),
        "possibleAffectedFlows": infer_possible_flows(text),
        "explicitRequirements": infer_explicit_requirements(text),
        "missingBusinessDecisions": infer_missing_decisions(text, detected_categories),
        "detectedCategories": detected_categories,
        "ambiguityLevel": infer_ambiguity_level(text),
    }

    write_json(Path(args.output), analysis)
    print(f"Requirement analysis generated at {args.output}")
    return 0


def build_ticket_text(issue: dict[str, Any]) -> str:
    chunks = [
        issue.get("title", ""),
        issue.get("description", ""),
        " ".join(issue.get("labels", [])),
    ]
    for comment in issue.get("comments", []):
        chunks.append(comment.get("body", ""))
    return " ".join(chunks).lower()


def infer_business_goal(title: str, description: str) -> str:
    text = f"{title} {description}".lower()
    if any(k in text for k in ["approve", "approval", "review", "validate"]):
        return "Add or improve a business approval/review step for a user-facing operation."
    if any(k in text for k in ["block", "limit", "abuse", "risk", "fraud"]):
        return "Reduce business risk and prevent misuse of a sensitive operation."
    if any(k in text for k in ["compliance", "legal", "privacy", "consent", "retention"]):
        return "Satisfy legal, compliance, privacy, or auditability requirements."
    if any(k in text for k in ["billing", "subscription", "plan", "price", "payment"]):
        return "Adjust commercial access, billing behavior, or plan-based functionality."
    if any(k in text for k in ["notification", "email", "sms", "push", "message"]):
        return "Improve communication behavior around a business operation."
    if any(k in text for k in ["dashboard", "report", "analytics", "metric", "kpi"]):
        return "Improve business visibility, reporting, or operational monitoring."
    return "Reduce requirement ambiguity and improve engineering readiness."


def infer_ambiguity_level(text: str) -> str:
    keywords = [
        "only", "except", "unless", "all users", "legacy", "retry", "limit", "expire", "support", "compliance"
    ]
    hits = sum(1 for kw in keywords if kw in text)
    if hits <= 2:
        return "HIGH"
    if hits <= 5:
        return "MEDIUM"
    return "LOW"


def detect_entities(text: str) -> list[str]:
    keywords = [
        "user",
        "customer",
        "admin",
        "support",
        "operator",
        "partner",
        "account",
        "operation",
        "request",
        "approval",
        "review",
        "notification",
        "message",
        "document",
        "content",
        "subscription",
        "plan",
        "payment",
        "report",
        "dashboard",
        "audit",
        "consent",
        "configuration",
        "feature flag",
    ]
    return sorted({kw for kw in keywords if kw in text})


def infer_user_actions(text: str) -> list[str]:
    actions: list[str] = []
    if any(k in text for k in ["create", "submit", "request", "start"]):
        actions.append("start operation")
    if any(k in text for k in ["confirm", "approve", "accept", "validate"]):
        actions.append("confirm or approve operation")
    if any(k in text for k in ["reject", "deny", "decline"]):
        actions.append("reject operation")
    if "cancel" in text:
        actions.append("cancel operation")
    if any(k in text for k in ["retry", "resend", "repeat"]):
        actions.append("retry operation")
    if any(k in text for k in ["view", "show", "display", "list"]):
        actions.append("view operation status")
    if any(k in text for k in ["edit", "update", "modify"]):
        actions.append("modify operation")
    if any(k in text for k in ["export", "download"]):
        actions.append("export operation data")
    if any(k in text for k in ["notify", "notification", "message", "email", "sms", "push"]):
        actions.append("receive communication")
    if not actions:
        actions.append("perform business operation")
    return sorted(set(actions))


def infer_possible_flows(text: str) -> list[str]:
    flows: list[str] = []
    if any(k in text for k in ["create", "submit", "request", "start"]):
        flows.append("operation creation")
    if any(k in text for k in ["approve", "review", "validate", "confirm"]):
        flows.append("operation review or confirmation")
    if any(k in text for k in ["cancel", "reject", "decline"]):
        flows.append("operation cancellation or rejection")
    if any(k in text for k in ["retry", "resend", "repeat"]):
        flows.append("retry or repetition flow")
    if any(k in text for k in ["legacy", "old app", "version", "compatibility"]):
        flows.append("compatibility flow")
    if any(k in text for k in ["support", "backoffice", "manual", "override", "unlock"]):
        flows.append("support operations")
    if any(k in text for k in ["email", "sms", "push", "notification", "message"]):
        flows.append("communication flow")
    if any(k in text for k in ["audit", "history", "trace"]):
        flows.append("auditability flow")
    if any(k in text for k in ["billing", "subscription", "plan", "price"]):
        flows.append("commercial access flow")
    if not flows:
        flows.append("primary business flow")
    return sorted(set(flows))


def infer_explicit_requirements(text: str) -> list[str]:
    reqs: list[str] = []
    if any(k in text for k in ["must", "should", "required", "mandatory"]):
        reqs.append("mandatory business behavior requested")
    if any(k in text for k in ["optional", "can", "may"]):
        reqs.append("optional business behavior requested")
    if any(k in text for k in ["approve", "approval", "review"]):
        reqs.append("approval or review behavior requested")
    if any(k in text for k in ["notify", "notification", "email", "sms", "push"]):
        reqs.append("communication behavior requested")
    if any(k in text for k in ["limit", "threshold", "max", "minimum"]):
        reqs.append("business limit or threshold requested")
    if any(k in text for k in ["legacy", "compatibility", "old app", "version"]):
        reqs.append("compatibility behavior requested")
    if any(k in text for k in ["config", "feature flag", "toggle", "setting"]):
        reqs.append("configurable activation requested")
    if any(k in text for k in ["audit", "history", "trace"]):
        reqs.append("auditability requested")
    return reqs


def detect_category_signals(text: str) -> list[str]:
    category_keywords: dict[str, list[str]] = {
        "Business Objective": ["goal", "outcome", "metric", "priority", "deadline"],
        "Functional Scope": ["all users", "country", "channel", "plan", "segment", "partner"],
        "Actors & Permissions": ["role", "support", "admin", "permission", "operator"],
        "Business Rules": ["limit", "attempt", "expire", "deadline", "window", "threshold", "retry", "repeat", "condition"],
        "State Lifecycle": ["state", "pending", "confirmed", "failed", "cancelled", "expired"],
        "Edge Cases": ["duplicate", "double click", "refresh", "connection", "concurrent"],
        "User Experience": ["message", "copy", "screen", "countdown", "error"],
        "Messages & Communications": ["message", "email", "sms", "push", "notification", "whatsapp", "communication"],
        "Support & Backoffice": ["backoffice", "support", "manual", "override", "unlock"],
        "Risk, Fraud & Abuse": ["fraud", "abuse", "risk", "suspicious", "block"],
        "Legal, Compliance & Privacy": ["legal", "compliance", "privacy", "gdpr", "consent"],
        "Pricing, Billing & Monetization": ["billing", "price", "plan", "subscription", "credit"],
        "Activation & Functional Configuration": ["feature flag", "toggle", "configuration", "rollout"],
        "Rollout & Transition": ["progressive", "beta", "migration", "transition", "rollback"],
        "Compatibility & Backward Compatibility": ["legacy", "old app", "version", "compatibility"],
        "Data & Functional Reporting": ["dashboard", "kpi", "report", "analytics", "export"],
        "Auditability & Traceability": ["audit", "trace", "history", "who", "when"],
        "Functional Error Handling": ["error", "timeout", "failure", "recover"],
        "Business External Dependencies": ["provider", "partner", "sla", "dependency"],
        "Internationalization & Localization": ["language", "country", "timezone", "currency"],
        "Accessibility & Usability": ["accessibility", "screen reader", "keyboard", "contrast"],
        "Perceived Performance": ["loading", "progress", "wait", "slow"],
        "Functional Security": ["verification", "authentication", "sensitive", "mask"],
        "Data Quality": ["mandatory", "validation", "format", "duplicate", "conflict"],
        "Priority, Severity & Criticality": ["critical", "severity", "impact", "urgent"],
        "Reversibility & Rollback": ["rollback", "disable", "revert", "fallback"],
        "Migration & Existing Data": ["existing", "historical", "backfill", "migrate"],
        "Out of Scope": ["out of scope", "not included", "later phase"],
        "Acceptance Criteria": ["acceptance", "qa", "done", "evidence"],
        "Rapid Decision": ["optional", "mandatory", "automatic", "manual"],
    }

    detected: list[str] = []
    for category, hints in category_keywords.items():
        if any(hint in text for hint in hints):
            detected.append(category)

    if "Business Objective" not in detected:
        detected.insert(0, "Business Objective")
    if "Functional Scope" not in detected:
        detected.append("Functional Scope")
    if "Business Rules" not in detected:
        detected.append("Business Rules")
    if "Acceptance Criteria" not in detected:
        detected.append("Acceptance Criteria")

    return sorted(set(detected))


def infer_missing_decisions(text: str, categories: list[str]) -> list[str]:
    checks = {
        "scope": ["all users", "country", "segment", "partner"],
        "success_behavior": ["success", "confirmed", "approved"],
        "error_behavior": ["error", "failed", "invalid"],
        "limits": ["max", "attempt", "limit", "threshold"],
        "expiration": ["expire", "minutes", "window", "ttl"],
        "legacy_compatibility": ["legacy", "old app", "version"],
        "support_behavior": ["support", "backoffice", "manual"],
        "communications": ["sms", "email", "push", "notification"],
        "compliance": ["legal", "consent", "privacy", "compliance"],
        "rollout": ["rollout", "beta", "progressive", "toggle"],
        "auditability": ["audit", "history", "trace"],
        "acceptance_criteria": ["qa", "acceptance", "done", "evidence"],
    }

    missing: list[str] = []
    for decision, hints in checks.items():
        if not any(h in text for h in hints):
            missing.append(decision)

    if "Risk, Fraud & Abuse" in categories and "limits" not in missing:
        if not any(k in text for k in ["block", "lock", "abuse"]):
            missing.append("risk_response")

    return sorted(set(missing))


def question_templates() -> list[dict[str, Any]]:
    return [
        {
            "template_id": "BO-1",
            "priority": "P0",
            "category": "Business Objective",
            "question": "What specific business outcome should improve after this change?",
            "whyItMatters": "Aligns implementation with a measurable business goal.",
            "suggestedAnswers": [
                "Reduce operational risk",
                "Improve conversion",
                "Reduce support workload",
                "Meet compliance requirements",
                "Improve user experience",
                "Other",
            ],
            "required": True,
            "blocksImplementation": True,
            "defaultIfUnanswered": None,
            "businessImpact": "product",
            "affectedActors": ["business", "product", "engineering"],
            "relatedAcceptanceCriteria": True,
            "signals": ["business objective"],
        },
        {
            "template_id": "FS-1",
            "priority": "P0",
            "category": "Functional Scope",
            "question": "Which users, countries, channels, plans, products, or partners are in scope?",
            "whyItMatters": "Defines where behavior changes and where it must stay unchanged.",
            "suggestedAnswers": [
                "All users",
                "Selected user segments",
                "Specific countries",
                "Specific channels",
                "Specific partners",
                "Specific plans/products",
                "Other",
            ],
            "required": True,
            "blocksImplementation": True,
            "defaultIfUnanswered": None,
            "businessImpact": "scope",
            "affectedActors": ["user", "support", "partner"],
            "relatedAcceptanceCriteria": True,
            "signals": ["scope"],
        },
        {
            "template_id": "BR-1",
            "priority": "P0",
            "category": "Business Rules",
            "question": "What exact business rules, limits, thresholds, deadlines, or conditions must apply?",
            "whyItMatters": "Defines the core behavior and avoids hidden product assumptions.",
            "suggestedAnswers": [
                "No special limits",
                "Use fixed limits",
                "Use limits by segment",
                "Use limits by country/channel",
                "Requires business definition",
            ],
            "required": True,
            "blocksImplementation": True,
            "defaultIfUnanswered": None,
            "businessImpact": "business_rule",
            "affectedActors": ["user", "support", "operations"],
            "relatedAcceptanceCriteria": True,
            "signals": ["limits", "expiration", "business_rules"],
        },
        {
            "template_id": "SL-1",
            "priority": "P0",
            "category": "State Lifecycle",
            "question": "What should happen when the operation succeeds, fails, is cancelled, expires, or remains pending?",
            "whyItMatters": "Defines the full lifecycle of the business operation.",
            "suggestedAnswers": [
                "Define all states in this ticket",
                "Use existing lifecycle",
                "Only success/error required",
                "Requires product decision",
            ],
            "required": True,
            "blocksImplementation": True,
            "defaultIfUnanswered": None,
            "businessImpact": "workflow",
            "affectedActors": ["user", "support", "operations"],
            "relatedAcceptanceCriteria": True,
            "signals": ["success_behavior", "error_behavior", "state_lifecycle"],
        },
        {
            "template_id": "UX-1",
            "priority": "P1",
            "category": "User Experience",
            "question": "What user-facing messages or screens are required for success, error, pending, blocked, and unavailable states?",
            "whyItMatters": "Defines user behavior and reduces support ambiguity.",
            "suggestedAnswers": [
                "Product-approved copy",
                "Temporary copy is acceptable",
                "Country-specific copy required",
                "No user-facing change",
                "Other",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "ux",
            "affectedActors": ["user", "support"],
            "relatedAcceptanceCriteria": True,
            "signals": ["error_behavior", "success_behavior", "ux"],
        },
        {
            "template_id": "CP-1",
            "priority": "P0",
            "category": "Compatibility & Backward Compatibility",
            "question": "What should happen for old clients, old app versions, existing integrations, or consumers that do not support the new behavior?",
            "whyItMatters": "Defines compatibility expectations and rollout safety.",
            "suggestedAnswers": [
                "Keep previous behavior",
                "Require client update",
                "Use fallback behavior",
                "Block unsupported clients",
                "Other",
            ],
            "required": True,
            "blocksImplementation": True,
            "defaultIfUnanswered": None,
            "businessImpact": "compatibility",
            "affectedActors": ["user", "partner", "support"],
            "relatedAcceptanceCriteria": True,
            "signals": ["legacy_compatibility"],
        },
        {
            "template_id": "RL-1",
            "priority": "P1",
            "category": "Rollout & Transition",
            "question": "Should rollout be immediate or progressive, and what business condition should trigger rollback?",
            "whyItMatters": "Defines launch strategy and limits blast radius.",
            "suggestedAnswers": [
                "Immediate rollout",
                "Progressive rollout",
                "Rollout by country/channel",
                "Internal beta first",
                "Other",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "rollout",
            "affectedActors": ["product", "operations", "support"],
            "relatedAcceptanceCriteria": True,
            "signals": ["rollout"],
        },
        {
            "template_id": "SP-1",
            "priority": "P1",
            "category": "Support & Backoffice",
            "question": "What must support or backoffice be able to view, retry, cancel, override, unlock, or audit?",
            "whyItMatters": "Defines operational readiness and incident handling.",
            "suggestedAnswers": [
                "No support/backoffice change",
                "Read-only visibility",
                "Manual retry/cancel",
                "Manual override",
                "Full operational management",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "operations",
            "affectedActors": ["support", "admin", "operations"],
            "relatedAcceptanceCriteria": True,
            "signals": ["support_behavior"],
        },
        {
            "template_id": "CM-1",
            "priority": "P1",
            "category": "Messages & Communications",
            "question": "Which communication channels must be used, when should they be triggered, and what happens if communication fails?",
            "whyItMatters": "Defines customer communication obligations and fallback behavior.",
            "suggestedAnswers": [
                "No communication required",
                "Email only",
                "SMS only",
                "Push/in-app only",
                "Multiple channels with fallback",
                "Other",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "communication",
            "affectedActors": ["user", "support"],
            "relatedAcceptanceCriteria": True,
            "signals": ["communications"],
        },
        {
            "template_id": "RS-1",
            "priority": "P1",
            "category": "Risk, Fraud & Abuse",
            "question": "What behavior should be considered suspicious or abusive, and what action should be taken when risk limits are exceeded?",
            "whyItMatters": "Prevents inconsistent risk responses.",
            "suggestedAnswers": [
                "No special risk handling",
                "Block operation",
                "Require manual review",
                "Temporarily restrict user",
                "Notify support",
                "Other",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "risk",
            "affectedActors": ["user", "support", "risk"],
            "relatedAcceptanceCriteria": True,
            "signals": ["risk_response"],
        },
        {
            "template_id": "LC-1",
            "priority": "P1",
            "category": "Legal, Compliance & Privacy",
            "question": "Are there legal, compliance, privacy, consent, retention, or audit obligations for this flow?",
            "whyItMatters": "Prevents release with missing legal or privacy requirements.",
            "suggestedAnswers": [
                "No additional obligations",
                "Consent required",
                "Retention rule required",
                "Audit trail required",
                "Legal review required",
                "Other",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "compliance",
            "affectedActors": ["legal", "support", "user"],
            "relatedAcceptanceCriteria": True,
            "signals": ["compliance"],
        },
        {
            "template_id": "DR-1",
            "priority": "P1",
            "category": "Data & Functional Reporting",
            "question": "Which business events, statuses, metrics, or reports must be tracked?",
            "whyItMatters": "Defines reporting, support, and audit expectations before implementation.",
            "suggestedAnswers": [
                "No reporting change",
                "Track success/error only",
                "Track full lifecycle",
                "Add support dimensions",
                "Add compliance dimensions",
                "Other",
            ],
            "required": True,
            "blocksImplementation": False,
            "defaultIfUnanswered": None,
            "businessImpact": "reporting",
            "affectedActors": ["business", "support", "compliance"],
            "relatedAcceptanceCriteria": True,
            "signals": ["auditability", "reporting"],
        },
        {
            "template_id": "AC-1",
            "priority": "P0",
            "category": "Acceptance Criteria",
            "question": "What minimum success, error, permission, compatibility, and edge cases must QA validate to accept this ticket?",
            "whyItMatters": "Defines done criteria and prevents hidden assumptions.",
            "suggestedAnswers": ["List minimum QA cases", "Link existing criteria", "Pending QA definition", "Other"],
            "required": True,
            "blocksImplementation": True,
            "defaultIfUnanswered": None,
            "businessImpact": "quality",
            "affectedActors": ["qa", "product", "engineering"],
            "relatedAcceptanceCriteria": True,
            "signals": ["acceptance_criteria"],
        },
        {
            "template_id": "PZ-1",
            "priority": "P3",
            "category": "Out of Scope",
            "question": "What is explicitly out of scope for this ticket and postponed to a future phase?",
            "whyItMatters": "Prevents scope creep and oversized base branches.",
            "suggestedAnswers": ["List exclusions", "No exclusions", "Future phase list"],
            "required": False,
            "blocksImplementation": False,
            "defaultIfUnanswered": "No explicit out-of-scope list provided",
            "businessImpact": "scope",
            "affectedActors": ["product", "engineering"],
            "relatedAcceptanceCriteria": False,
            "signals": ["scope"],
        },
    ]


def generate_questions(args: argparse.Namespace) -> int:
    analysis = load_json(Path(args.input))
    missing_decisions = set(analysis.get("missingBusinessDecisions", []))
    issue_key = analysis.get("issueKey")

    candidates = []
    for tpl in question_templates():
        if should_include_template(tpl, missing_decisions):
            candidates.append(tpl)

    if len(candidates) < MIN_REQUIRED_QUESTIONS:
        for tpl in question_templates():
            if tpl not in candidates and tpl["priority"] in {"P0", "P1"}:
                candidates.append(tpl)
            if len([c for c in candidates if c["required"]]) >= MIN_REQUIRED_QUESTIONS:
                break

    required = [q for q in candidates if q.get("required", False) and q["priority"] in {"P0", "P1"}]
    optional_future = [q for q in candidates if q["priority"] in {"P2", "P3"}]

    required = sort_questions(required)[:MAX_REQUIRED_QUESTIONS]
    optional_future = sort_questions(optional_future)

    questions_payload: list[dict[str, Any]] = []
    for idx, question in enumerate(required, start=1):
        payload = dict(question)
        payload["id"] = f"Q{idx}"
        payload.pop("signals", None)
        questions_payload.append(payload)

    optional_payload: list[dict[str, Any]] = []
    for question in optional_future:
        payload = dict(question)
        payload.pop("signals", None)
        optional_payload.append(payload)

    output = {
        "issueKey": issue_key,
        "status": "WAITING_BUSINESS_INPUT",
        "summary": (
            "To prepare an AI base branch without product assumptions, "
            "business decisions are required for scope, behavior, compatibility, operations, and acceptance."
        ),
        "questions": questions_payload,
        "optionalFutureDecisions": optional_payload,
        "questionCount": len(questions_payload),
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }

    write_json(Path(args.output), output)
    print(f"Business questions generated at {args.output} ({len(questions_payload)} required)")
    return 0


def should_include_template(template: dict[str, Any], missing_decisions: set[str]) -> bool:
    signals = set(template.get("signals", []))
    if signals.intersection(missing_decisions):
        return True
    if template["priority"] == "P0":
        return True
    return False


def sort_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority_rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    return sorted(questions, key=lambda q: (priority_rank.get(q.get("priority", "P3"), 9), q.get("category", "")))


def collect_input(args: argparse.Namespace) -> int:
    question_set = load_json(Path(args.input))
    state_file = Path(args.state_file)

    state = {
        "issueKey": question_set.get("issueKey"),
        "answers": {},
        "lastUpdated": datetime.now(timezone.utc).isoformat(),
    }

    if state_file.exists():
        saved = load_json(state_file)
        if saved.get("issueKey") == question_set.get("issueKey"):
            state = saved

    required_questions = [q for q in question_set.get("questions", []) if q.get("required", False)]

    if args.non_interactive:
        unanswered = [q["id"] for q in required_questions if q["id"] not in state.get("answers", {})]
        if unanswered:
            print(f"Missing required answers: {', '.join(unanswered)}")
            return 2
        print("All required questions are answered.")
        return 0

    print(f"Collecting answers for {question_set.get('issueKey')} (state file: {state_file})")
    print("State is persisted after each answer. Restart safely anytime.")

    for q in required_questions:
        qid = q["id"]
        if qid in state.get("answers", {}):
            continue

        print("\n" + "-" * 72)
        print(f"{qid} [{q['priority']} | {q['category']}]")
        print(textwrap.fill(q["question"], width=100))
        print(textwrap.fill(f"Why it matters: {q['whyItMatters']}", width=100))
        for option in q.get("suggestedAnswers", []):
            print(f"  - {option}")

        try:
            answer = input("Answer: ").strip()
        except (KeyboardInterrupt, EOFError):
            state["lastUpdated"] = datetime.now(timezone.utc).isoformat()
            write_json(state_file, state)
            print("\nSession interrupted. State saved; resume with the same command.")
            return 130

        if not answer:
            print("Empty answer, question remains pending.")
            continue

        state.setdefault("answers", {})[qid] = {
            "answer": answer,
            "capturedAt": datetime.now(timezone.utc).isoformat(),
            "priority": q.get("priority"),
            "category": q.get("category"),
        }
        state["lastUpdated"] = datetime.now(timezone.utc).isoformat()
        write_json(state_file, state)

    write_json(state_file, state)
    print("\nRequired answer capture completed.")
    return 0


def resolve_contract(args: argparse.Namespace) -> int:
    question_set = load_json(Path(args.questions))
    state = load_json(Path(args.answers))
    required_questions = [q for q in question_set.get("questions", []) if q.get("required", False)]
    unanswered = [q["id"] for q in required_questions if q["id"] not in state.get("answers", {})]
    if unanswered:
        print(f"Cannot resolve contract. Missing required answers: {', '.join(unanswered)}")
        return 2

    answers = state.get("answers", {})
    answer_items = []
    for question in question_set.get("questions", []):
        qid = question.get("id")
        answer = answers.get(qid, {}).get("answer")
        if not answer:
            continue
        answer_items.append(
            {
                "questionId": qid,
                "category": question.get("category"),
                "priority": question.get("priority"),
                "question": question.get("question"),
                "answer": answer,
                "businessImpact": question.get("businessImpact"),
                "blocksImplementation": question.get("blocksImplementation", False),
            }
        )

    contract = {
        "issueKey": question_set.get("issueKey"),
        "functionalContract": {
            "businessObjective": extract_answer_by_category(answer_items, "Business Objective"),
            "functionalScope": extract_answer_by_category(answer_items, "Functional Scope"),
            "businessRules": extract_answers_by_category(answer_items, "Business Rules"),
            "stateLifecycle": extract_answers_by_category(answer_items, "State Lifecycle"),
            "userExperience": extract_answers_by_category(answer_items, "User Experience"),
            "compatibility": extract_answer_by_category(answer_items, "Compatibility & Backward Compatibility"),
            "rollout": extract_answer_by_category(answer_items, "Rollout & Transition"),
            "supportAndBackoffice": extract_answer_by_category(answer_items, "Support & Backoffice"),
            "communications": extract_answer_by_category(answer_items, "Messages & Communications"),
            "riskAndAbuse": extract_answer_by_category(answer_items, "Risk, Fraud & Abuse"),
            "legalCompliancePrivacy": extract_answer_by_category(answer_items, "Legal, Compliance & Privacy"),
            "reporting": extract_answer_by_category(answer_items, "Data & Functional Reporting"),
            "acceptanceCriteria": extract_answer_by_category(answer_items, "Acceptance Criteria"),
            "outOfScope": extract_answer_by_category(answer_items, "Out of Scope"),
        },
        "source": "business_answers",
        "unresolvedItems": infer_unresolved_contract_items(answer_items),
        "resolvedAt": datetime.now(timezone.utc).isoformat(),
    }

    write_json(Path(args.output), contract)
    print(f"Functional contract generated at {args.output}")
    return 0


def extract_answer_by_category(answer_items: list[dict[str, Any]], category: str) -> str | None:
    for item in answer_items:
        if item.get("category") == category:
            return item.get("answer")
    return None


def extract_answers_by_category(answer_items: list[dict[str, Any]], category: str) -> list[str]:
    return [
        item["answer"]
        for item in answer_items
        if item.get("category") == category and item.get("answer")
    ]


def infer_unresolved_contract_items(answer_items: list[dict[str, Any]]) -> list[str]:
    unresolved_markers = [
        "unknown",
        "pending",
        "tbd",
        "to be defined",
        "not sure",
        "needs review",
        "requires confirmation",
    ]
    unresolved: list[str] = []
    for item in answer_items:
        answer = str(item.get("answer", "")).lower()
        if any(marker in answer for marker in unresolved_markers):
            unresolved.append(
                f"{item.get('questionId')} - {item.get('category')}: answer requires clarification"
            )
    return unresolved


def base_branch_plan(args: argparse.Namespace) -> int:
    analysis = load_json(Path(args.analysis))
    contract = load_json(Path(args.contract))

    issue_key = analysis.get("issueKey", "UNKNOWN")
    missing = len(analysis.get("missingBusinessDecisions", []))
    unresolved = len(contract.get("unresolvedItems", []))
    if unresolved > 0:
        confidence = 0.60
    elif missing <= 2:
        confidence = 0.90
    elif missing <= 5:
        confidence = 0.78
    else:
        confidence = 0.60

    detected_flows = analysis.get("possibleAffectedFlows", [])
    detected_entities = analysis.get("functionalEntities", [])
    functional_contract = contract.get("functionalContract", {})

    plan = {
        "issueKey": issue_key,
        "confidence": confidence,
        "branchName": f"ai/{sanitize_branch_part(issue_key)}-base",
        "implementationScope": build_generic_implementation_scope(detected_flows, functional_contract),
        "excludedScope": [
            "Unrelated UI redesign",
            "Cross-domain refactors not required by the ticket",
            "New unrelated dependencies",
            "Unapproved product expansion",
            "Unapproved reporting/dashboard expansion",
            "Unapproved manual operations",
        ],
        "detectedEntities": detected_entities,
        "detectedFlows": detected_flows,
        "requiresHumanReview": True,
        "functionalContractUsed": functional_contract,
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }

    if confidence < 0.65:
        plan["status"] = "QUESTIONS_ONLY"
        plan["note"] = "Confidence too low for base branch. Keep requirement discovery only."
    elif confidence < 0.85:
        plan["status"] = "PLAN_ONLY"
        plan["note"] = "Medium confidence. Generate technical plan but avoid autonomous coding."
    else:
        plan["status"] = "READY_FOR_BASE_BRANCH"

    write_json(Path(args.output), plan)
    print(f"Base branch plan generated at {args.output}")
    return 0


def sanitize_branch_part(value: str) -> str:
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9._/-]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized.strip("-") or "unknown-issue"


def build_generic_implementation_scope(
    detected_flows: list[str],
    functional_contract: dict[str, Any],
) -> list[str]:
    scope = [
        "Apply the business decisions captured in the functional contract",
        "Add or update the primary business flow required by the ticket",
        "Preserve existing behavior outside the confirmed functional scope",
        "Add baseline tests for success, error, and out-of-scope behavior",
        "Generate an implementation report with assumptions, decisions, risks, and review notes",
    ]

    if any("compatibility" in flow for flow in detected_flows):
        scope.append("Preserve backward-compatible behavior for existing consumers where required")
    if functional_contract.get("supportAndBackoffice"):
        scope.append("Add or update support/backoffice behavior only as explicitly confirmed")
    if functional_contract.get("communications"):
        scope.append("Add or update user/business communications only as explicitly confirmed")
    if functional_contract.get("reporting"):
        scope.append("Add or update functional tracking/reporting only as explicitly confirmed")
    if functional_contract.get("riskAndAbuse"):
        scope.append("Apply confirmed risk, abuse, or limit behavior")

    return scope


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Agentic requirements pipeline for Jira")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch-issue", help="Fetch issue from Jira")
    p_fetch.add_argument("issue_key")
    p_fetch.add_argument("--output", default="issue.json")
    p_fetch.set_defaults(func=fetch_issue)

    p_discovery = sub.add_parser("discovery", help="Analyze missing business requirements")
    p_discovery.add_argument("--input", required=True)
    p_discovery.add_argument("--output", default="ticket_analysis.json")
    p_discovery.set_defaults(func=discovery)

    p_questions = sub.add_parser("generate-questions", help="Generate prioritized business questions")
    p_questions.add_argument("--input", required=True)
    p_questions.add_argument("--output", default="business_questions.json")
    p_questions.set_defaults(func=generate_questions)

    p_collect = sub.add_parser("collect-input", help="Capture business answers with resumable state")
    p_collect.add_argument("--input", required=True)
    p_collect.add_argument("--state-file", default=DEFAULT_STATE_FILE)
    p_collect.add_argument("--non-interactive", action="store_true")
    p_collect.set_defaults(func=collect_input)

    p_resolve = sub.add_parser("resolve-contract", help="Resolve a functional contract from answers")
    p_resolve.add_argument("--questions", required=True)
    p_resolve.add_argument("--answers", required=True)
    p_resolve.add_argument("--output", default="functional_contract.json")
    p_resolve.set_defaults(func=resolve_contract)

    p_plan = sub.add_parser("base-branch-plan", help="Generate base branch implementation plan")
    p_plan.add_argument("--analysis", required=True)
    p_plan.add_argument("--contract", required=True)
    p_plan.add_argument("--output", default="base_branch_plan.json")
    p_plan.set_defaults(func=base_branch_plan)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
