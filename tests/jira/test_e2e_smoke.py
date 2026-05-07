"""End-to-end smoke test: run all six CLI commands in sequence."""

import json
import subprocess
import sys
from pathlib import Path


CLI = Path(__file__).resolve().parents[2] / "jira-agentic-requirements-pipeline" / "scripts" / "jira_pipeline_cli.py"
FIXTURES = Path(__file__).parent / "fixtures"


def test_cli_runs_full_pipeline(tmp_path):
    issue_src = FIXTURES / "issue_tight.json"
    issue = tmp_path / "issue.json"
    issue.write_text(issue_src.read_text())

    analysis = tmp_path / "analysis.json"
    questions = tmp_path / "questions.json"
    contract = tmp_path / "contract.json"
    plan = tmp_path / "plan.json"

    def run(*args):
        result = subprocess.run(
            [sys.executable, str(CLI), *args],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0, (
            f"CLI command failed: {' '.join(args)}\nstdout: {result.stdout}\nstderr: {result.stderr}"
        )
        return result

    run("discovery", "--input", str(issue), "--output", str(analysis))
    run("generate-questions", "--input", str(analysis), "--output", str(questions))

    # Synthesize deterministic answers
    qs = json.loads(questions.read_text())
    state = {
        "issueKey": qs["issueKey"],
        "answers": {
            q["id"]: {"answer": f"Answer for {q['category']}", "category": q["category"], "priority": q["priority"]}
            for q in qs["questions"]
        },
    }
    state_path = tmp_path / "state.json"
    state_path.write_text(json.dumps(state))

    # collect-input in non-interactive mode just validates completeness
    run("collect-input", "--input", str(questions), "--state-file", str(state_path), "--non-interactive")
    run("resolve-contract", "--questions", str(questions), "--answers", str(state_path), "--output", str(contract))
    run("base-branch-plan", "--analysis", str(analysis), "--contract", str(contract), "--output", str(plan))

    plan_data = json.loads(plan.read_text())
    assert plan_data["status"] == "READY_FOR_BASE_BRANCH"
    assert plan_data["proposedBranchName"] == "ai/demo-100-base"
