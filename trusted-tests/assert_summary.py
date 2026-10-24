"""Check the actual hosted Action's outcome and generated Markdown."""
import json
import os
from pathlib import Path
import re

case = os.environ["CASE_NAME"]
match = re.fullmatch(r"smoke/(neutral|grants|incomplete)", case)
assert match, f"Unknown test case: {case}"
case = match[1]
expected_outcome = "failure" if case == "incomplete" else "success"
assert os.environ["SCAN_OUTCOME"] == expected_outcome, os.environ["SCAN_OUTCOME"]
summary = (Path(os.environ["RUNNER_TEMP"]) / "wpc-summary.md").read_text()
title = {"neutral": "No supported privilege expansions detected", "grants": "Review suggested", "incomplete": "Analysis incomplete"}[case]
assert "## " + title in summary, summary
assert os.environ["EXPECTED_BASE"] in summary
assert os.environ["EXPECTED_HEAD"] in summary
if case == "grants":
    assert summary.count("| WF001 |") == 2, summary
    assert summary.count("| WF003 |") == 1, summary
    assert summary.count("| WF004 |") == 1, summary
    assert "SMOKE_DUMMY_TOKEN" in summary
    assert "workflow_run" in summary
else:
    assert not any(rule in summary for rule in ("WF001", "WF003", "WF004")), summary
if case == "neutral":
    assert "defaults stay fixed" in summary
if case == "incomplete":
    assert "Inherited token defaults are unknown" in summary
assert not (Path(os.environ["GITHUB_WORKSPACE"]) / "UNTRUSTED_CODE_EXECUTED").exists()
print("SMOKE_EVIDENCE=" + json.dumps({"passed": True, "case": case, "fork": os.environ["IS_FORK"],
    "base": os.environ["EXPECTED_BASE"], "head": os.environ["EXPECTED_HEAD"],
    "scanOutcome": os.environ["SCAN_OUTCOME"], "scannerCommit": os.environ["SCANNER_COMMIT"],
    "summary": summary}, sort_keys=True))
