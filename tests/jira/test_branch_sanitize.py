"""Property tests for sanitize_branch_part using Hypothesis."""

import re

from hypothesis import given, strategies as st

import jira_pipeline_cli as cli


@given(st.text())
def test_sanitize_idempotent(value):
    once = cli.sanitize_branch_part(value)
    twice = cli.sanitize_branch_part(once)
    assert once == twice


@given(st.text())
def test_sanitize_no_double_dashes(value):
    result = cli.sanitize_branch_part(value)
    assert "--" not in result


@given(st.text())
def test_sanitize_no_leading_or_trailing_dash(value):
    result = cli.sanitize_branch_part(value)
    assert not result.startswith("-")
    assert not result.endswith("-")


@given(st.text())
def test_sanitize_only_branch_safe_characters(value):
    result = cli.sanitize_branch_part(value)
    # Branch parts may contain a-z, 0-9, dot, underscore, slash, dash
    assert re.fullmatch(r"[a-z0-9._/\-]+", result) is not None


def test_sanitize_empty_string_returns_default():
    assert cli.sanitize_branch_part("") == "unknown-issue"


def test_sanitize_keeps_issue_key_intact():
    assert cli.sanitize_branch_part("APP-4827") == "app-4827"
