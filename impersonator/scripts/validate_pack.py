#!/usr/bin/env python3
"""Validate a generated impersonator pack against its provenance contract.

The impersonator skill produces a pack under
`examples/ready-to-use/<slug>/`. This validator enforces the safety
rules documented in the skill so a pack with weak or missing
provenance fails fast and never lands.

Checks:
1. `evidence-map.md` exists and is non-trivial (≥ a minimum row count).
2. The Simulation Notice banner appears in `cognitive-profile.md`.
3. The README documents the pack and how to load it.
4. Every directive populated in the cognitive profile is covered by at
   least one row in `evidence-map.md` (heuristic: directive key
   appears as a substring of any evidence row).

Usage:
    python3 validate_pack.py path/to/examples/ready-to-use/<slug>
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


SIMULATION_NOTICE = "Simulation Notice"
DIRECTIVE_PATTERN = re.compile(r"\{([a-zA-Z0-9_.]+)\}")
MIN_EVIDENCE_ROWS = 5


def find_directives(profile_text: str) -> set[str]:
    """Extract every `{directives.x.y}` placeholder still present.

    Generated packs replace placeholders with prose; any remaining
    placeholders signal an incomplete fill, which we also report as a
    finding.
    """
    return set(DIRECTIVE_PATTERN.findall(profile_text))


def list_directive_keys_in_evidence(evidence_text: str) -> set[str]:
    """Return every `directives.x.y` token cited inside the evidence map."""
    return set(re.findall(r"directives\.[a-zA-Z0-9_.]+", evidence_text))


def list_directive_keys_in_profile(profile_text: str) -> set[str]:
    """Return every `directives.x.y` token cited inside the cognitive profile."""
    return set(re.findall(r"directives\.[a-zA-Z0-9_.]+", profile_text))


def validate(pack: Path) -> list[str]:
    errors: list[str] = []

    profile = pack / "cognitive-profile.md"
    evidence = pack / "evidence-map.md"
    readme = pack / "README.md"

    if not profile.exists():
        errors.append("cognitive-profile.md is missing")
    if not evidence.exists():
        errors.append("evidence-map.md is missing")
    if not readme.exists():
        errors.append("README.md is missing")

    if errors:
        return errors

    profile_text = profile.read_text(encoding="utf-8")
    evidence_text = evidence.read_text(encoding="utf-8")

    if SIMULATION_NOTICE not in profile_text:
        errors.append("cognitive-profile.md is missing the 'Simulation Notice' banner")

    # Count populated rows in the evidence table (rows that include "|" and a confidence cell).
    evidence_rows = [
        line for line in evidence_text.splitlines()
        if line.startswith("|") and "high" in line.lower() or "medium" in line.lower() or "low" in line.lower()
    ]
    if len(evidence_rows) < MIN_EVIDENCE_ROWS:
        errors.append(
            f"evidence-map.md has only {len(evidence_rows)} populated rows "
            f"(minimum: {MIN_EVIDENCE_ROWS})"
        )

    unfilled = find_directives(profile_text)
    if unfilled:
        errors.append(
            f"cognitive-profile.md has {len(unfilled)} unfilled placeholder(s): "
            + ", ".join(sorted(unfilled)[:5])
        )

    profile_keys = list_directive_keys_in_profile(profile_text)
    evidence_keys = list_directive_keys_in_evidence(evidence_text)
    uncited = profile_keys - evidence_keys
    if uncited:
        errors.append(
            f"{len(uncited)} directive(s) cited in profile but missing from evidence-map: "
            + ", ".join(sorted(uncited)[:5])
        )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an impersonator-generated pack.")
    parser.add_argument("pack", help="Path to the pack folder (e.g. examples/ready-to-use/<slug>).")
    args = parser.parse_args()

    pack = Path(args.pack).resolve()
    if not pack.is_dir():
        print(f"error: not a directory: {pack}", file=sys.stderr)
        return 2

    errors = validate(pack)
    if errors:
        print(f"pack {pack.name}: invalid", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"pack {pack.name}: ok")
    return 0


if __name__ == "__main__":
    sys.exit(main())
