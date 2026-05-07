"""Shared test configuration: make the Jira CLI script importable."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JIRA_SCRIPTS = ROOT / "jira-agentic-requirements-pipeline" / "scripts"

if str(JIRA_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(JIRA_SCRIPTS))
