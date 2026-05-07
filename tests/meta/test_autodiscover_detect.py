"""Tests for autodiscover/scripts/detect.py."""

from pathlib import Path

import detect


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_detect_finds_all_ceet_folders():
    folders = detect.find_ceet_folders(REPO_ROOT)
    names = {f.name for f in folders}
    # Subset check: at least the engineering trio is present.
    assert {"ceet-backend-engineer", "ceet-frontend-engineer", "ceet-devops-sre"} <= names


def test_detect_recommends_backend_for_api_request():
    report = detect.detect(REPO_ROOT, "review my backend api migration")
    assert report["recommendation"]["primary"] == "ceet-backend-engineer"
    assert "ceet-backend-engineer" in report["detectedCEETs"]
    matched = report["scoring"][0]["matched"]
    assert any(m.startswith("kw:") for m in matched)


def test_detect_recommends_copywriter_for_headline_request():
    report = detect.detect(REPO_ROOT, "rewrite my landing page headline")
    assert report["recommendation"]["primary"] == "ceet-copywriter"


def test_detect_returns_null_recommendation_for_unrelated_request():
    report = detect.detect(REPO_ROOT, "the quick brown fox")
    assert report["recommendation"]["primary"] is None
    assert report["detectedCEETs"] == []


def test_detect_marks_ceets_with_existing_packs_as_initialized():
    report = detect.detect(REPO_ROOT, "")
    # backend-engineer has a starter-pack and the netflix pack
    backend_entry = next(s for s in report["scoring"] if s["ceet"] == "ceet-backend-engineer")
    assert backend_entry["initialized"] is True
    assert any("examples/ready-to-use" in r for r in backend_entry["initializationReasons"])


def test_detect_schema_version_present():
    report = detect.detect(REPO_ROOT, "anything")
    assert report["schemaVersion"] == detect.SCHEMA_VERSION
