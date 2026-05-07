"""Make the meta-skill scripts importable from tests."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

for skill_scripts in [
    ROOT / "autodiscover" / "scripts",
    ROOT / "ceet-sub-agent-orchestration" / "scripts",
    ROOT / "impersonator" / "scripts",
]:
    if str(skill_scripts) not in sys.path:
        sys.path.insert(0, str(skill_scripts))
