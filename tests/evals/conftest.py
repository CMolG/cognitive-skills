"""Make eval scripts importable from tests."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVAL_SCRIPTS = ROOT / "evals" / "scripts"

if str(EVAL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(EVAL_SCRIPTS))
