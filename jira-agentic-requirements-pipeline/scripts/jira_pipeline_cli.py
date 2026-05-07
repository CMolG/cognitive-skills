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
CONTRACT_SCHEMA_VERSION = "1.0.0"

DEFAULT_BASELINE_BUDGET = 4
DEFAULT_SIGNAL_BUDGET = 6
DEFAULT_MAX_COMMENTS = 1000

# P0 templates that should always be candidates regardless of detected signals.
# These cover universally required decisions (objective, scope, rules, lifecycle).
BASELINE_TEMPLATE_IDS = {"BO-1", "FS-1", "BR-1", "SL-1"}

AMBIGUITY_MARKERS = [
    "tbd",
    "?",
    "we should",
    " or ",
    "alternatively",
    "maybe",
    "not sure",
    "to be defined",
    "pending",
    "unknown",
]

CONSTRAINT_KEYWORDS = [
    "only",
    "except",
    "unless",
    "all users",
    "legacy",
    "retry",
    "limit",
    "expire",
    "support",
    "compliance",
]


@dataclass
class JiraConfig:
    base_url: str
    email: str
    api_token: str


def load_json(path: Path) -> dict[str, Any]:
    """Read a UTF-8 JSON file and return its parsed object."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write `data` as pretty-printed UTF-8 JSON, creating parents as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_jira_config() -> JiraConfig:
    """Read Jira credentials from env vars or fail fast with a clear error."""
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


class JiraClient:
    """Thin wrapper around Jira REST API v3.

    The client owns transport (urllib) and authentication so tests can
    inject a fake by subclassing or by passing an alternative `client`
    object that exposes the same `get(path, query) -> dict` contract.
    """

    def __init__(self, config: JiraConfig, timeout: int = 30) -> None:
        self.config = config
        self.timeout = timeout

    def get(self, path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
        query_str = ""
        if query:
            query_str = "?" + urllib.parse.urlencode(query)

        url = f"{self.config.base_url}{path}{query_str}"
        auth = base64.b64encode(
            f"{self.config.email}:{self.config.api_token}".encode("utf-8")
        ).decode("ascii")

        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Basic {auth}")
        req.add_header("Accept", "application/json")

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise SystemExit(f"Jira HTTP {exc.code}: {body}") from exc


def jira_get(config: JiraConfig, path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
    """Perform an authenticated GET against Jira REST API and return JSON.

    Backward-compatible thin wrapper around `JiraClient.get`.
    """
    return JiraClient(config).get(path, query)


def extract_text_from_jira_node(node: Any) -> str:
    """Walk a Jira ADF node and concatenate every leaf text fragment."""
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


def fetch_issue(args: argparse.Namespace, client: "JiraClient | None" = None) -> int:
    """Fetch a Jira issue and its full comment history into a normalized JSON file."""
    if client is None:
        client = JiraClient(get_jira_config())
    payload = client.get(
        f"/rest/api/3/issue/{args.issue_key}",
        query={"fields": "summary,description,labels,customfield_10011,status"},
    )

    fields = payload.get("fields", {})
    max_comments = getattr(args, "max_comments", DEFAULT_MAX_COMMENTS)
    raw_comments = fetch_all_comments(client, args.issue_key, max_comments)

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
            for c in raw_comments
        ],
        "acceptanceCriteria": [],
        "fetchedAt": datetime.now(timezone.utc).isoformat(),
    }

    output = Path(args.output)
    write_json(output, normalized)
    print(f"Issue exported to {output}")
    return 0


def fetch_all_comments(
    client: "JiraClient",
    issue_key: str,
    max_comments: int,
    page_size: int = 100,
) -> list[dict[str, Any]]:
    """Page through Jira's comment endpoint until `total` or `max_comments`.

    Jira REST v3 returns at most 100 comments per page. The original
    implementation read only the first page, silently truncating context on
    active tickets. Here we loop with `startAt`, stopping when we have all
    comments or the cap is reached. A warning is emitted to stderr if the
    cap clipped the result.
    """
    collected: list[dict[str, Any]] = []
    start_at = 0
    total: int | None = None
    while True:
        remaining_cap = max_comments - len(collected)
        if remaining_cap <= 0:
            break
        page = client.get(
            f"/rest/api/3/issue/{issue_key}/comment",
            query={
                "startAt": str(start_at),
                "maxResults": str(min(page_size, remaining_cap)),
            },
        )
        page_comments = page.get("comments", []) or []
        collected.extend(page_comments)
        total = page.get("total", len(collected))
        start_at += len(page_comments)
        if not page_comments or start_at >= total:
            break

    if total is not None and total > len(collected):
        sys.stderr.write(
            f"warning: comment cap reached ({len(collected)} of {total}); "
            f"increase --max-comments to fetch all\n"
        )

    return collected


def discovery(args: argparse.Namespace) -> int:
    """Run rule-based requirement discovery and emit a TicketAnalysis JSON."""
    issue = load_json(Path(args.input))
    text = build_ticket_text(issue)

    detected_categories = detect_category_signals(text)

    analysis = {
        "schemaVersion": CONTRACT_SCHEMA_VERSION,
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
    """Concatenate title, description, labels and comments into a single lower-cased corpus."""
    chunks = [
        issue.get("title", ""),
        issue.get("description", ""),
        " ".join(issue.get("labels", [])),
    ]
    for comment in issue.get("comments", []):
        chunks.append(comment.get("body", ""))
    return " ".join(chunks).lower()


def infer_business_goal(title: str, description: str) -> str:
    """Pick a coarse business-goal label from keyword heuristics over the ticket text."""
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


def infer_ambiguity_level(text: str) -> dict[str, Any]:
    """Score ticket ambiguity from constraint density and explicit ambiguity markers.

    Returns a dict with:
      - level: HIGH | MEDIUM | LOW
      - constraintDensity: constraint hits per 100 words (float)
      - ambiguityMarkers: marker hits per 100 words (float)
      - signals: which constraint keywords and markers fired
    The downstream `base-branch-plan` can consume the components, not only
    the bucketed level.
    """
    word_count = max(len(text.split()), 1)
    constraint_hits = [kw for kw in CONSTRAINT_KEYWORDS if kw in text]
    marker_hits = [m for m in AMBIGUITY_MARKERS if m in text]

    constraint_density = round(len(constraint_hits) * 100 / word_count, 3)
    marker_density = round(len(marker_hits) * 100 / word_count, 3)

    if constraint_density < 0.4 and marker_density >= 0.4:
        level = "HIGH"
    elif constraint_density >= 1.2 and marker_density < 0.4:
        level = "LOW"
    else:
        level = "MEDIUM"

    return {
        "level": level,
        "constraintDensity": constraint_density,
        "ambiguityMarkers": marker_density,
        "signals": {
            "constraintKeywords": constraint_hits,
            "ambiguityMarkers": marker_hits,
        },
    }


def detect_entities(text: str) -> list[str]:
    """Return functional entities (user, account, notification, ...) detected in the ticket text."""
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
    """Infer the user-facing actions (start/cancel/retry/...) implied by the text."""
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
    """Infer the business flows (creation, review, retry, ...) likely affected by the ticket."""
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
    """Surface high-level requirement classes (mandatory, approval, communication, ...) from the text."""
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
    """Return the sorted categories whose keyword set fires against the ticket text."""
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
    """List decision keys (scope, expiration, communications, ...) missing from the text."""
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
    """Return the static catalog of business question templates."""
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
    """Build the prioritized BusinessQuestionSet for a discovery analysis."""
    analysis = load_json(Path(args.input))
    missing_decisions = set(analysis.get("missingBusinessDecisions", []))
    issue_key = analysis.get("issueKey")

    baseline_budget = getattr(args, "baseline_budget", DEFAULT_BASELINE_BUDGET)
    signal_budget = getattr(args, "signal_budget", DEFAULT_SIGNAL_BUDGET)

    required = select_required_templates(missing_decisions, baseline_budget, signal_budget)
    optional_future = sort_questions(
        [t for t in question_templates() if t["priority"] in {"P2", "P3"}]
    )

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
        "schemaVersion": CONTRACT_SCHEMA_VERSION,
        "issueKey": issue_key,
        "status": "WAITING_BUSINESS_INPUT",
        "summary": (
            "To prepare an AI base branch without product assumptions, "
            "business decisions are required for scope, behavior, compatibility, operations, and acceptance."
        ),
        "questions": questions_payload,
        "optionalFutureDecisions": optional_payload,
        "questionCount": len(questions_payload),
        "budgets": {
            "baseline": baseline_budget,
            "signal": signal_budget,
        },
        "generatedAt": datetime.now(timezone.utc).isoformat(),
    }

    write_json(Path(args.output), output)
    print(f"Business questions generated at {args.output} ({len(questions_payload)} required)")
    return 0


def select_required_templates(
    missing_decisions: set[str],
    baseline_budget: int,
    signal_budget: int,
) -> list[dict[str, Any]]:
    """Pick the required questions using a baseline + signal budget split.

    The baseline budget reserves slots for universally required P0 templates
    (objective/scope/rules/lifecycle). The signal budget is filled by
    templates whose declared signals intersect the ticket's missing
    decisions, ranked by match strength. Underused signal slots overflow
    into remaining P0/P1 templates so the pipeline never under-asks.
    """
    templates = question_templates()
    priority_rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}

    baseline_pool = [t for t in templates if t["template_id"] in BASELINE_TEMPLATE_IDS]
    baseline_pool.sort(key=lambda t: (priority_rank.get(t["priority"], 9), t["template_id"]))
    selected_baseline = baseline_pool[:baseline_budget]

    def signal_strength(t: dict[str, Any]) -> int:
        return len(set(t.get("signals", [])).intersection(missing_decisions))

    signal_candidates = [
        t for t in templates
        if t["template_id"] not in BASELINE_TEMPLATE_IDS and signal_strength(t) > 0
    ]
    signal_candidates.sort(
        key=lambda t: (-signal_strength(t), priority_rank.get(t["priority"], 9), t["template_id"])
    )
    selected_signal = signal_candidates[:signal_budget]

    remaining = signal_budget - len(selected_signal)
    if remaining > 0:
        already = {t["template_id"] for t in selected_baseline + selected_signal}
        overflow = [
            t for t in templates
            if t["template_id"] not in already
            and t.get("required", False)
            and t["priority"] in {"P0", "P1"}
        ]
        overflow.sort(key=lambda t: (priority_rank.get(t["priority"], 9), t["template_id"]))
        selected_signal.extend(overflow[:remaining])

    return selected_baseline + selected_signal


def should_include_template(template: dict[str, Any], missing_decisions: set[str]) -> bool:
    """Return True if a template is a candidate for inclusion.

    Kept for backward compatibility with older callers; the real selection
    logic now lives in `select_required_templates` and respects the
    baseline/signal budget split.
    """
    if template["template_id"] in BASELINE_TEMPLATE_IDS:
        return True
    signals = set(template.get("signals", []))
    return bool(signals.intersection(missing_decisions))


def sort_questions(questions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Sort questions by priority bucket then category for stable output."""
    priority_rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    return sorted(questions, key=lambda q: (priority_rank.get(q.get("priority", "P3"), 9), q.get("category", "")))


def collect_input(args: argparse.Namespace) -> int:
    """Walk the user through required questions interactively, persisting state per answer."""
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
    """Combine questions and captured answers into a FunctionalContract JSON."""
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

    # businessObjective/functionalScope are intentionally singular: the
    # functional contract represents one decision per ticket on these axes.
    # Every other field defaults to the plural form so additional answers
    # in the same category are preserved instead of silently dropped.
    mapped_categories = {
        "Business Objective",
        "Functional Scope",
        "Business Rules",
        "State Lifecycle",
        "User Experience",
        "Compatibility & Backward Compatibility",
        "Rollout & Transition",
        "Support & Backoffice",
        "Messages & Communications",
        "Risk, Fraud & Abuse",
        "Legal, Compliance & Privacy",
        "Data & Functional Reporting",
        "Acceptance Criteria",
        "Out of Scope",
    }
    unmapped_answers = [
        {
            "questionId": item.get("questionId"),
            "category": item.get("category"),
            "answer": item.get("answer"),
        }
        for item in answer_items
        if item.get("category") not in mapped_categories
    ]

    contract = {
        "schemaVersion": CONTRACT_SCHEMA_VERSION,
        "issueKey": question_set.get("issueKey"),
        "functionalContract": {
            "businessObjective": extract_answer_by_category(answer_items, "Business Objective"),
            "functionalScope": extract_answer_by_category(answer_items, "Functional Scope"),
            "businessRules": extract_answers_by_category(answer_items, "Business Rules"),
            "stateLifecycle": extract_answers_by_category(answer_items, "State Lifecycle"),
            "userExperience": extract_answers_by_category(answer_items, "User Experience"),
            "compatibility": extract_answers_by_category(answer_items, "Compatibility & Backward Compatibility"),
            "rollout": extract_answers_by_category(answer_items, "Rollout & Transition"),
            "supportAndBackoffice": extract_answers_by_category(answer_items, "Support & Backoffice"),
            "communications": extract_answers_by_category(answer_items, "Messages & Communications"),
            "riskAndAbuse": extract_answers_by_category(answer_items, "Risk, Fraud & Abuse"),
            "legalCompliancePrivacy": extract_answers_by_category(answer_items, "Legal, Compliance & Privacy"),
            "reporting": extract_answers_by_category(answer_items, "Data & Functional Reporting"),
            "acceptanceCriteria": extract_answers_by_category(answer_items, "Acceptance Criteria"),
            "outOfScope": extract_answers_by_category(answer_items, "Out of Scope"),
        },
        "source": "business_answers",
        "unmappedAnswers": unmapped_answers,
        "unresolvedItems": infer_unresolved_contract_items(answer_items),
        "resolvedAt": datetime.now(timezone.utc).isoformat(),
    }

    write_json(Path(args.output), contract)
    print(f"Functional contract generated at {args.output}")
    return 0


def extract_answer_by_category(answer_items: list[dict[str, Any]], category: str) -> str | None:
    """Return the first answer found for `category`, or None. Use for fields that must be singular."""
    for item in answer_items:
        if item.get("category") == category:
            return item.get("answer")
    return None


def extract_answers_by_category(answer_items: list[dict[str, Any]], category: str) -> list[str]:
    """Return every non-empty answer captured for `category` (preserving order)."""
    return [
        item["answer"]
        for item in answer_items
        if item.get("category") == category and item.get("answer")
    ]


def infer_unresolved_contract_items(answer_items: list[dict[str, Any]]) -> list[str]:
    """Flag answers containing TBD/unknown-style markers as unresolved contract items."""
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
    """Combine TicketAnalysis and FunctionalContract into a BaseBranchPlan JSON."""
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

    # `proposedBranchName` is a name suggestion only; this CLI never creates
    # the branch. The engineer creates it after reviewing the plan.
    plan = {
        "schemaVersion": CONTRACT_SCHEMA_VERSION,
        "issueKey": issue_key,
        "confidence": confidence,
        "proposedBranchName": f"ai/{sanitize_branch_part(issue_key)}-base",
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


# Fields the host model is allowed to refine in an LLM-augmented analysis
# patch. Anything outside this allowlist is rejected so the host model
# cannot rewrite identity fields (issueKey, schemaVersion) or volatile
# metadata (timestamps).
LLM_PATCH_ALLOWED_KEYS = {
    "businessGoal",
    "functionalEntities",
    "userActions",
    "possibleAffectedFlows",
    "explicitRequirements",
    "missingBusinessDecisions",
    "detectedCategories",
    "ambiguityLevel",
}

LLM_PATCH_LIST_KEYS = {
    "functionalEntities",
    "userActions",
    "possibleAffectedFlows",
    "explicitRequirements",
    "missingBusinessDecisions",
    "detectedCategories",
}


def merge_llm_suggestions(args: argparse.Namespace) -> int:
    """Merge a host-model patch into a TicketAnalysis without trusting it blindly.

    The host model produces `suggestions.json` after reading the
    rule-based `analysis.json`. This command applies the patch under
    three rules:
      - Only keys in `LLM_PATCH_ALLOWED_KEYS` are accepted; anything
        else is reported as `rejectedKeys` in the merged output.
      - For list-shaped fields (entities, flows, ...) the merge is the
        sorted union of rule-based + LLM suggestions, so additions
        compound and the deterministic core is never overwritten.
      - Everything else is replaced by the LLM value, but the original
        rule-based value is kept under `_ruleBased.<field>` for
        provenance.
    """
    analysis = load_json(Path(args.analysis))
    suggestions = load_json(Path(args.suggestions))

    rejected: list[str] = []
    accepted: list[str] = []
    rule_based_snapshot: dict[str, Any] = {}

    for key, value in suggestions.items():
        if key == "schemaVersion" or key == "issueKey":
            continue
        if key not in LLM_PATCH_ALLOWED_KEYS:
            rejected.append(key)
            continue

        rule_based_snapshot[key] = analysis.get(key)

        if key in LLM_PATCH_LIST_KEYS:
            existing = analysis.get(key) or []
            if not isinstance(value, list):
                rejected.append(key)
                continue
            merged = sorted({str(x) for x in list(existing) + list(value) if x is not None and x != ""})
            analysis[key] = merged
        else:
            analysis[key] = value
        accepted.append(key)

    analysis["_llmAugmentation"] = {
        "acceptedKeys": sorted(accepted),
        "rejectedKeys": sorted(rejected),
        "ruleBasedSnapshot": rule_based_snapshot,
        "appliedAt": datetime.now(timezone.utc).isoformat(),
    }

    output = Path(args.output) if args.output else Path(args.analysis)
    write_json(output, analysis)
    print(
        f"Merged LLM suggestions into {output} "
        f"(accepted={len(accepted)}, rejected={len(rejected)})"
    )
    return 0


def sanitize_branch_part(value: str) -> str:
    """Lower-case `value` and replace non-branch-safe characters with single dashes."""
    normalized = value.strip().lower()
    normalized = re.sub(r"[^a-z0-9._/-]+", "-", normalized)
    normalized = re.sub(r"-+", "-", normalized)
    return normalized.strip("-") or "unknown-issue"


def build_generic_implementation_scope(
    detected_flows: list[str],
    functional_contract: dict[str, Any],
) -> list[str]:
    """Build the bullet list of implementation scope items for the base-branch plan."""
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
    """Wire up the argparse hierarchy for the six pipeline subcommands."""
    parser = argparse.ArgumentParser(description="Agentic requirements pipeline for Jira")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_fetch = sub.add_parser("fetch-issue", help="Fetch issue from Jira")
    p_fetch.add_argument("issue_key")
    p_fetch.add_argument("--output", default="issue.json")
    p_fetch.add_argument(
        "--max-comments",
        type=int,
        default=DEFAULT_MAX_COMMENTS,
        help="Cap the number of comments fetched (default: 1000).",
    )
    p_fetch.set_defaults(func=fetch_issue)

    p_discovery = sub.add_parser("discovery", help="Analyze missing business requirements")
    p_discovery.add_argument("--input", required=True)
    p_discovery.add_argument("--output", default="ticket_analysis.json")
    p_discovery.set_defaults(func=discovery)

    p_questions = sub.add_parser("generate-questions", help="Generate prioritized business questions")
    p_questions.add_argument("--input", required=True)
    p_questions.add_argument("--output", default="business_questions.json")
    p_questions.add_argument(
        "--baseline-budget",
        type=int,
        default=DEFAULT_BASELINE_BUDGET,
        help="Slots reserved for universally required P0 templates (default: 4).",
    )
    p_questions.add_argument(
        "--signal-budget",
        type=int,
        default=DEFAULT_SIGNAL_BUDGET,
        help="Slots reserved for signal-driven templates (default: 6).",
    )
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

    p_merge = sub.add_parser(
        "merge-llm-suggestions",
        help="Merge an LLM-produced refinement patch into a TicketAnalysis (allowlist-validated)",
    )
    p_merge.add_argument("--analysis", required=True)
    p_merge.add_argument("--suggestions", required=True)
    p_merge.add_argument(
        "--output",
        default=None,
        help="Destination path. Defaults to overwriting --analysis in place.",
    )
    p_merge.set_defaults(func=merge_llm_suggestions)

    return parser


def main() -> int:
    """CLI entry point: parse arguments and dispatch to the chosen subcommand."""
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
