"""Unit tests for the rule-based inference functions in jira_pipeline_cli."""

import json
from pathlib import Path

import jira_pipeline_cli as cli


FIXTURES = Path(__file__).parent / "fixtures"


def load_text(fixture: str) -> str:
    issue = json.loads((FIXTURES / fixture).read_text())
    return cli.build_ticket_text(issue)


def test_ambiguity_level_returns_dict_shape():
    result = cli.infer_ambiguity_level(load_text("issue_tight.json"))
    assert set(result) == {"level", "constraintDensity", "ambiguityMarkers", "signals"}
    assert result["level"] in {"LOW", "MEDIUM", "HIGH"}
    assert isinstance(result["constraintDensity"], float)
    assert isinstance(result["ambiguityMarkers"], float)
    assert "constraintKeywords" in result["signals"]
    assert "ambiguityMarkers" in result["signals"]


def test_ambiguity_level_low_for_tight_ticket():
    assert cli.infer_ambiguity_level(load_text("issue_tight.json"))["level"] == "LOW"


def test_ambiguity_level_medium_for_mixed_ticket():
    assert cli.infer_ambiguity_level(load_text("issue_medium.json"))["level"] == "MEDIUM"


def test_ambiguity_level_high_for_near_empty_ticket():
    assert cli.infer_ambiguity_level(load_text("issue_empty.json"))["level"] == "HIGH"


def test_ambiguity_level_high_for_marker_dominated_ticket():
    """A long ticket dominated by markers (TBD, maybe, ...) and lacking
    constraint keywords should still rank HIGH despite its length."""
    text = load_text("issue_ambiguous.json")
    result = cli.infer_ambiguity_level(text)
    assert result["level"] == "HIGH"
    assert result["ambiguityMarkers"] > 0
    assert "tbd" in result["signals"]["ambiguityMarkers"]


def test_density_normalized_per_100_words():
    """Doubling the text length without changing keyword count must halve the density."""
    short = "limit retry expire"
    long = short + " " + " ".join(["filler"] * 100)
    short_density = cli.infer_ambiguity_level(short)["constraintDensity"]
    long_density = cli.infer_ambiguity_level(long)["constraintDensity"]
    assert short_density > long_density


def test_missing_decisions_for_empty_ticket():
    text = load_text("issue_empty.json")
    missing = cli.infer_missing_decisions(text, cli.detect_category_signals(text))
    # Near-empty title should miss most decisions.
    assert len(missing) >= 10


def test_select_required_templates_respects_baseline_budget():
    selected = cli.select_required_templates(missing_decisions=set(), baseline_budget=4, signal_budget=6)
    baseline_ids = {t["template_id"] for t in selected if t["template_id"] in cli.BASELINE_TEMPLATE_IDS}
    assert baseline_ids == {"BO-1", "FS-1", "BR-1", "SL-1"}


def test_select_required_templates_signal_overflow_into_baseline_p1():
    """When no signals match, signal slots overflow into remaining P0/P1 templates."""
    selected = cli.select_required_templates(missing_decisions=set(), baseline_budget=4, signal_budget=6)
    assert len(selected) == 10  # 4 baseline + 6 overflow
    overflow_ids = {t["template_id"] for t in selected if t["template_id"] not in cli.BASELINE_TEMPLATE_IDS}
    assert overflow_ids  # must be filled


def test_select_required_templates_signal_priority_match():
    """Templates whose signals match more missing decisions rank higher."""
    selected = cli.select_required_templates(
        missing_decisions={"compliance", "communications"}, baseline_budget=4, signal_budget=2
    )
    signal_only = [t for t in selected if t["template_id"] not in cli.BASELINE_TEMPLATE_IDS]
    ids = {t["template_id"] for t in signal_only}
    # CM-1 maps to communications, LC-1 maps to compliance — both should be picked
    assert {"CM-1", "LC-1"} <= ids
