"""Tests for impersonator/scripts/validate_pack.py."""

from pathlib import Path

import validate_pack


REPO_ROOT = Path(__file__).resolve().parents[2]
NETFLIX_PACK = REPO_ROOT / "examples" / "ready-to-use" / "backend-netflix-tech-blog"
STARTER_PACK = REPO_ROOT / "examples" / "ready-to-use" / "backend-engineer-starter-pack"


def test_well_evidenced_pack_validates():
    errors = validate_pack.validate(NETFLIX_PACK)
    assert errors == [], f"unexpected validation errors: {errors}"


def test_unfilled_starter_pack_fails_validation():
    errors = validate_pack.validate(STARTER_PACK)
    assert errors  # must produce at least one error
    # Common starter-pack failure modes
    joined = " | ".join(errors)
    assert "Simulation Notice" in joined or "unfilled placeholder" in joined or "evidence-map" in joined


def test_missing_required_files_reported(tmp_path):
    pack = tmp_path / "empty-pack"
    pack.mkdir()
    errors = validate_pack.validate(pack)
    assert any("cognitive-profile.md" in e for e in errors)
    assert any("evidence-map.md" in e for e in errors)
    assert any("README.md" in e for e in errors)


def test_minimum_evidence_rows_enforced(tmp_path):
    pack = tmp_path / "thin-pack"
    pack.mkdir()
    (pack / "cognitive-profile.md").write_text(
        "Simulation Notice\n\n# Profile\n\nReferencing directives.architecture.foo\n"
    )
    (pack / "evidence-map.md").write_text(
        "# Evidence Map\n\n| Directive | Confidence | Evidence |\n|---|---|---|\n"
        "| `directives.architecture.foo` | high | source |\n"
    )
    (pack / "README.md").write_text("# Readme\n")
    errors = validate_pack.validate(pack)
    assert any("populated rows" in e for e in errors)
