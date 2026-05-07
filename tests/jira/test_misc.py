"""Coverage for the smaller helpers and CLI plumbing."""

import json
from argparse import Namespace
from pathlib import Path

import pytest

import jira_pipeline_cli as cli


def test_get_jira_config_raises_when_env_missing(monkeypatch):
    monkeypatch.delenv("JIRA_BASE_URL", raising=False)
    monkeypatch.delenv("JIRA_EMAIL", raising=False)
    monkeypatch.delenv("JIRA_API_TOKEN", raising=False)
    with pytest.raises(SystemExit) as excinfo:
        cli.get_jira_config()
    assert "JIRA_BASE_URL" in str(excinfo.value)
    assert "JIRA_EMAIL" in str(excinfo.value)
    assert "JIRA_API_TOKEN" in str(excinfo.value)


def test_get_jira_config_strips_trailing_slash(monkeypatch):
    monkeypatch.setenv("JIRA_BASE_URL", "https://example.atlassian.net/")
    monkeypatch.setenv("JIRA_EMAIL", "u@example.com")
    monkeypatch.setenv("JIRA_API_TOKEN", "secret")
    config = cli.get_jira_config()
    assert config.base_url == "https://example.atlassian.net"


def test_extract_text_from_jira_node_handles_nested_adf():
    node = {
        "type": "doc",
        "content": [
            {"type": "paragraph", "content": [{"type": "text", "text": "hello"}]},
            {"type": "paragraph", "content": [{"type": "text", "text": "world"}]},
        ],
    }
    assert cli.extract_text_from_jira_node(node) == "hello world"


def test_extract_text_from_jira_node_handles_string_input():
    assert cli.extract_text_from_jira_node("plain string") == "plain string"


def test_extract_text_from_jira_node_handles_none():
    assert cli.extract_text_from_jira_node(None) == ""


def test_collect_input_non_interactive_passes_when_complete(tmp_path):
    questions_path = tmp_path / "q.json"
    questions_path.write_text(
        json.dumps(
            {
                "issueKey": "DEMO-1",
                "questions": [
                    {"id": "Q1", "category": "Business Objective", "priority": "P0", "required": True}
                ],
            }
        )
    )
    state_path = tmp_path / "state.json"
    state_path.write_text(
        json.dumps({"issueKey": "DEMO-1", "answers": {"Q1": {"answer": "ok"}}})
    )

    rc = cli.collect_input(
        Namespace(input=str(questions_path), state_file=str(state_path), non_interactive=True)
    )
    assert rc == 0


def test_collect_input_non_interactive_fails_when_incomplete(tmp_path, capsys):
    questions_path = tmp_path / "q.json"
    questions_path.write_text(
        json.dumps(
            {
                "issueKey": "DEMO-1",
                "questions": [
                    {"id": "Q1", "category": "Business Objective", "priority": "P0", "required": True},
                    {"id": "Q2", "category": "Functional Scope", "priority": "P0", "required": True},
                ],
            }
        )
    )
    state_path = tmp_path / "state.json"
    state_path.write_text(
        json.dumps({"issueKey": "DEMO-1", "answers": {"Q1": {"answer": "ok"}}})
    )

    rc = cli.collect_input(
        Namespace(input=str(questions_path), state_file=str(state_path), non_interactive=True)
    )
    assert rc == 2
    captured = capsys.readouterr()
    assert "Q2" in captured.out


def test_unresolved_items_detect_tbd_markers():
    items = [
        {"questionId": "Q1", "category": "Business Rules", "answer": "TBD: still pending"},
        {"questionId": "Q2", "category": "Functional Scope", "answer": "All paid users"},
    ]
    unresolved = cli.infer_unresolved_contract_items(items)
    assert any("Q1" in entry for entry in unresolved)
    assert not any("Q2" in entry for entry in unresolved)


def test_build_parser_lists_all_subcommands():
    parser = cli.build_parser()
    # parse_args raises SystemExit on no command — instead probe the choices
    sub = next(a for a in parser._actions if a.dest == "cmd")
    assert set(sub.choices) == {
        "fetch-issue",
        "discovery",
        "generate-questions",
        "collect-input",
        "resolve-contract",
        "base-branch-plan",
        "merge-llm-suggestions",
    }
