#!/usr/bin/env python3
"""Deterministic CEET detector for the autodiscover skill.

Scans the workspace for `ceet-*` folders, classifies each as
initialized or not, matches the user's request against per-role
keywords, and emits a JSON report the host model can consume before
deciding how to proceed.

Usage:
    python3 detect.py --workspace . --request "review my backend migration"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "1.0.0"

# Keywords associated with each role. Folder names contribute their
# tokens automatically; this map adds synonyms that are not literal
# substrings of the folder name. Keep entries lowercase.
ROLE_KEYWORDS: dict[str, list[str]] = {
    "ceet-backend-engineer": [
        "api", "backend", "database", "migration", "service",
        "rest", "graphql", "schema", "queue", "worker",
    ],
    "ceet-frontend-engineer": [
        "frontend", "ui", "component", "react", "vue", "svelte",
        "css", "browser", "render", "accessibility", "a11y",
    ],
    "ceet-devops-sre": [
        "infra", "infrastructure", "ci", "cd", "kubernetes", "k8s",
        "docker", "incident", "rollback", "observability", "metrics",
        "alert", "deploy", "pipeline", "sre",
    ],
    "ceet-data-analytics": [
        "data", "analytics", "metric", "dashboard", "sql", "etl",
        "experiment", "ab test", "hypothesis", "kpi",
    ],
    "ceet-product-manager": [
        "prd", "roadmap", "prioritization", "discovery", "stakeholder",
        "scope", "feature", "rfc",
    ],
    "ceet-ux-researcher": [
        "research", "interview", "synthesis", "behavior", "jtbd",
        "user research", "usability",
    ],
    "ceet-ui-designer": [
        "design", "visual", "component library", "design system",
        "motion", "typography", "layout",
    ],
    "ceet-copywriter": [
        "copy", "headline", "cta", "tone", "voice", "tagline",
        "subheadline", "rewrite",
    ],
    "ceet-marketing": [
        "marketing", "campaign", "growth", "funnel", "channel",
        "positioning", "conversion",
    ],
    "ceet-sales": [
        "sales", "discovery call", "objection", "pipeline", "close",
        "qualification", "demo",
    ],
    "ceet-customer-success": [
        "onboarding", "retention", "expansion", "churn",
        "customer success", "csm", "qbr", "health score",
    ],
    "ceet-financial": [
        "forecast", "budget", "unit economics", "margin", "pricing model",
        "p&l", "valuation",
    ],
    "ceet-legal-compliance": [
        "legal", "compliance", "contract", "policy", "gdpr", "consent",
        "privacy", "regulatory",
    ],
    "ceet-people-ops": [
        "hiring", "onboarding plan", "performance review", "compensation",
        "people ops", "hr",
    ],
    "ceet-founder-ceo": [
        "strategy", "narrative", "fundraising", "capital", "org design",
        "ceo", "founder",
    ],
}


def find_ceet_folders(workspace: Path) -> list[Path]:
    """Return every direct-child `ceet-*` folder under `workspace`."""
    return sorted(p for p in workspace.iterdir() if p.is_dir() and p.name.startswith("ceet-"))


def is_initialized(ceet_folder: Path, workspace: Path) -> tuple[bool, list[str]]:
    """A CEET counts as initialized if it ships a SKILL.md and a
    populated `templates/cognitive-profile.md`, OR if at least one
    generated pack exists under `examples/ready-to-use/`.
    """
    reasons: list[str] = []
    skill = ceet_folder / "SKILL.md"
    profile = ceet_folder / "templates" / "cognitive-profile.md"
    initialized = False
    if skill.exists() and profile.exists() and profile.stat().st_size > 200:
        initialized = True
        reasons.append("templates/cognitive-profile.md present")

    role = ceet_folder.name.removeprefix("ceet-")
    examples = workspace / "examples" / "ready-to-use"
    matching_packs: list[str] = []
    if examples.exists():
        for pack in examples.iterdir():
            if pack.is_dir() and role in pack.name:
                matching_packs.append(str(pack.relative_to(workspace)))
        if matching_packs:
            initialized = True
            reasons.append(f"{len(matching_packs)} example pack(s) under examples/ready-to-use/")

    return initialized, reasons + matching_packs


def tokenize(value: str) -> set[str]:
    """Lower-case `value`, split on non-alphanumeric, drop empties."""
    return {tok for tok in re.split(r"[^a-z0-9]+", value.lower()) if tok}


def score_request(request: str, ceet_folder: Path) -> tuple[int, list[str]]:
    """Score how well `request` matches a CEET, plus the matched signals.

    Matching uses word boundaries: keyword `ui` does not match `quick`,
    and folder token `backend` does not match `backendish`. Multi-word
    keywords (`design system`) still match because the regex spans
    spaces.
    """
    request_lc = request.lower()
    request_tokens = tokenize(request)
    folder_tokens = tokenize(ceet_folder.name.removeprefix("ceet-"))
    keywords = ROLE_KEYWORDS.get(ceet_folder.name, [])

    matched: list[str] = []

    for token in folder_tokens:
        if token in request_tokens:
            matched.append(f"folder:{token}")

    for kw in keywords:
        if re.search(rf"(?<![a-z0-9]){re.escape(kw)}(?![a-z0-9])", request_lc):
            matched.append(f"kw:{kw}")

    return len(matched), matched


def detect(workspace: Path, request: str) -> dict[str, Any]:
    """Build the full detection report."""
    ceets = find_ceet_folders(workspace)

    detected = []
    initialized: list[str] = []
    scoring: list[dict[str, Any]] = []

    for folder in ceets:
        score, matched = score_request(request, folder) if request else (0, [])
        is_init, reasons = is_initialized(folder, workspace)
        if is_init:
            initialized.append(folder.name)
        if score > 0:
            detected.append(folder.name)
        scoring.append({
            "ceet": folder.name,
            "score": score,
            "matched": matched,
            "initialized": is_init,
            "initializationReasons": reasons,
        })

    scoring.sort(key=lambda entry: (-entry["score"], entry["ceet"]))

    primary = None
    needs_init = False
    reason = None
    fallbacks: list[str] = []

    if scoring and scoring[0]["score"] > 0:
        primary = scoring[0]["ceet"]
        needs_init = not scoring[0]["initialized"]
        reason = (
            f"matched signals {scoring[0]['matched']}"
            if scoring[0]["matched"]
            else "best keyword score among detected CEETs"
        )
        fallbacks = [
            entry for entry in scoring[0]["initializationReasons"]
            if entry.startswith("examples/")
        ]
    elif not request:
        reason = "no request supplied; only enumeration produced"
    else:
        reason = "no CEET keywords matched the request"

    return {
        "schemaVersion": SCHEMA_VERSION,
        "workspace": str(workspace),
        "detectedCEETs": sorted(detected),
        "initializedCEETs": sorted(initialized),
        "scoring": scoring,
        "recommendation": {
            "primary": primary,
            "reason": reason,
            "needsInitialization": needs_init,
            "fallbacks": fallbacks,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic CEET detector for autodiscover.")
    parser.add_argument("--workspace", default=".", help="Workspace root to scan (default: cwd).")
    parser.add_argument("--request", default="", help="User request to match against role keywords.")
    parser.add_argument("--output", default=None, help="Write JSON to this file instead of stdout.")
    args = parser.parse_args()

    report = detect(Path(args.workspace).resolve(), args.request)
    payload = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
