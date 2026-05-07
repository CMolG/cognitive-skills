"""Tests that exercise the JiraClient seam without making real HTTP calls."""

import json
from argparse import Namespace
from pathlib import Path
from typing import Any

import jira_pipeline_cli as cli


class FakeJiraClient:
    """Drop-in replacement for JiraClient backed by a script of canned responses."""

    def __init__(self, responses: dict[str, list[dict[str, Any]]] | None = None) -> None:
        self.responses = responses or {}
        self.calls: list[tuple[str, dict[str, str] | None]] = []

    def get(self, path: str, query: dict[str, str] | None = None) -> dict[str, Any]:
        self.calls.append((path, query))
        queue = self.responses.get(path)
        if not queue:
            raise AssertionError(f"unexpected call to {path}")
        return queue.pop(0)


def test_fetch_all_comments_paginates_until_total():
    page1 = {"comments": [{"id": str(i)} for i in range(100)], "total": 250, "startAt": 0, "maxResults": 100}
    page2 = {"comments": [{"id": str(i)} for i in range(100, 200)], "total": 250, "startAt": 100, "maxResults": 100}
    page3 = {"comments": [{"id": str(i)} for i in range(200, 250)], "total": 250, "startAt": 200, "maxResults": 100}

    client = FakeJiraClient(
        {"/rest/api/3/issue/DEMO-1/comment": [page1, page2, page3]}
    )

    result = cli.fetch_all_comments(client, "DEMO-1", max_comments=1000)

    assert len(result) == 250
    assert result[0]["id"] == "0"
    assert result[-1]["id"] == "249"
    # 3 page calls
    assert len(client.calls) == 3


def test_fetch_all_comments_respects_cap_and_warns(capsys):
    page1 = {"comments": [{"id": str(i)} for i in range(50)], "total": 200, "startAt": 0, "maxResults": 50}

    client = FakeJiraClient(
        {"/rest/api/3/issue/DEMO-1/comment": [page1]}
    )

    result = cli.fetch_all_comments(client, "DEMO-1", max_comments=50)

    assert len(result) == 50
    captured = capsys.readouterr()
    assert "comment cap reached" in captured.err
    assert "200" in captured.err  # total surfaced in the warning


def test_fetch_all_comments_stops_when_total_reached():
    page1 = {"comments": [{"id": "1"}, {"id": "2"}], "total": 2, "startAt": 0, "maxResults": 100}

    client = FakeJiraClient(
        {"/rest/api/3/issue/DEMO-1/comment": [page1]}
    )

    result = cli.fetch_all_comments(client, "DEMO-1", max_comments=1000)

    assert len(result) == 2
    assert len(client.calls) == 1


def test_fetch_issue_normalizes_payload(tmp_path):
    issue_payload = {
        "key": "DEMO-1",
        "fields": {
            "summary": "Title",
            "description": {"content": [{"type": "paragraph", "content": [{"type": "text", "text": "body"}]}]},
            "labels": ["a", "b"],
            "customfield_10011": "EPIC-1",
            "status": {"name": "Open"},
        },
    }
    comments_payload = {
        "comments": [{"author": {"displayName": "alice"}, "body": "hi", "created": "2026-01-01T00:00:00Z"}],
        "total": 1,
        "startAt": 0,
        "maxResults": 100,
    }
    client = FakeJiraClient(
        {
            "/rest/api/3/issue/DEMO-1": [issue_payload],
            "/rest/api/3/issue/DEMO-1/comment": [comments_payload],
        }
    )

    output = tmp_path / "issue.json"
    args = Namespace(issue_key="DEMO-1", output=str(output), max_comments=1000)
    rc = cli.fetch_issue(args, client=client)

    assert rc == 0
    saved = json.loads(output.read_text())
    assert saved["issueKey"] == "DEMO-1"
    assert saved["title"] == "Title"
    assert saved["description"] == "body"
    assert saved["labels"] == ["a", "b"]
    assert saved["epic"] == "EPIC-1"
    assert saved["status"] == "Open"
    assert saved["comments"][0]["author"] == "alice"
    assert saved["comments"][0]["body"] == "hi"
