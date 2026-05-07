"""Tests for evals/scripts/scoring.py."""

import scoring


def test_word_count_excludes_punctuation():
    assert scoring.word_count("Hello, world! Foo's bar.") == 4


def test_section_count_counts_markdown_headings():
    text = "# A\n\n## B\n\nbody\n\n### C\n"
    assert scoring.section_count(text) == 3


def test_required_phrase_hits_is_case_insensitive():
    text = "We use a Feature Flag with dual-write."
    result = scoring.required_phrase_hits(text, ["feature flag", "dual-write", "missing"])
    assert result == {"feature flag": True, "dual-write": True, "missing": False}


def test_voice_alignment_high_for_overlapping_vocabulary():
    corpus = "expand contract dual-write feature flag rollback blast radius"
    output = "Use expand and contract with a feature flag and a rollback toggle."
    other = "Looks fine, ship it. Senior engineer here."
    aligned = scoring.voice_alignment(output, corpus)
    misaligned = scoring.voice_alignment(other, corpus)
    assert aligned > misaligned
    assert aligned > 0.05


def test_score_output_full_pipeline():
    text = (
        "# Summary\n"
        "Reject as written. We need expand and contract with a feature flag.\n"
        "## Risk\n"
        "Lock contention on the unique index. Backfill must batch.\n"
        "## Rollback\n"
        "The plan has none. Add a toggle.\n"
    )
    criteria = {
        "minWords": 5,
        "maxWords": 1000,
        "requiredSections": ["summary", "risk", "rollback"],
        "requiredPhrases": ["expand", "contract", "feature flag", "rollback", "missing-term"],
    }
    result = scoring.score_output(text, criteria, corpus="expand contract feature flag rollback")
    assert result["sectionCoverage"] == 1.0
    # 4 of 5 phrases present
    assert result["phraseCoverage"] == 0.8
    assert result["lengthWithinBounds"] is True
    assert result["voiceAlignment"] > 0.0
    assert 0.0 <= result["compositeScore"] <= 1.0


def test_score_output_flags_length_violation():
    criteria = {"minWords": 1000, "maxWords": 2000, "requiredPhrases": [], "requiredSections": []}
    result = scoring.score_output("only ten words here for this test of the scorer", criteria, corpus=None)
    assert result["lengthWithinBounds"] is False
