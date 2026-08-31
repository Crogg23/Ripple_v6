"""The shape counter is the only guard that never has an opinion.

These tests are the disproving check for it: they assert that a message which
breaks a countable rule is blocked, that a clean one passes silently, and that
`hooks off` and the loop guard both open the gate. If the counter ever starts
guessing, one of these goes red.
"""

from __future__ import annotations

import json
import os
import shutil
import uuid
import subprocess
import sys

import pytest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
CHECKER = REPO / ".claude" / "hooks" / "shape_check.py"
GATE = REPO / ".claude" / "hooks" / "shape-gate.sh"
OFF_SWITCH = REPO / ".claude" / "state" / "hooks.off"


def _check(message: str, session: str | None = None):
    if session is None:
        session = f"fresh-{uuid.uuid4()}"
    payload = json.dumps({"last_assistant_message": message, "session_id": session})
    proc = subprocess.run(
        [sys.executable, str(CHECKER)],
        input=payload,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(REPO)},
    )
    return proc.returncode, (proc.stderr or "").strip()


def _gate(message: str, hooks_off: bool = False):
    # A bare "bash" does not resolve through Python's spawn on Windows even when
    # it is on PATH, so hand subprocess the real binary.
    bash = shutil.which("bash")
    if bash is None:
        pytest.skip("no bash on this machine")
    OFF_SWITCH.parent.mkdir(parents=True, exist_ok=True)
    if hooks_off:
        OFF_SWITCH.touch()
    else:
        OFF_SWITCH.unlink(missing_ok=True)
    try:
        proc = subprocess.run(
            [bash, str(GATE)],
            input=json.dumps(
                {"last_assistant_message": message, "session_id": "gate-test"}
            ),
            capture_output=True,
            text=True,
            encoding="utf-8",
            env={**os.environ, "CLAUDE_PROJECT_DIR": str(REPO)},
        )
    finally:
        OFF_SWITCH.unlink(missing_ok=True)
    return proc.returncode, (proc.stderr or "").strip()


@pytest.fixture(autouse=True)
def _fresh_retry_budget():
    """The budget lives on disk, so a previous run would leak into this one."""
    for stale in (REPO / ".claude" / "state").glob("*.shape_tries"):
        stale.unlink(missing_ok=True)
    yield
    for stale in (REPO / ".claude" / "state").glob("*.shape_tries"):
        stale.unlink(missing_ok=True)


CLEAN = "## Header\n\nShort line here.\n\nAnother short line.\n\n- clean bullet\n"


def test_clean_message_passes_silently():
    code, err = _check(CLEAN)
    assert code == 0
    assert err == ""


def test_long_line_is_counted():
    long_line = "This line is deliberately far too long because it keeps adding clauses forever."
    code, err = _check(long_line)
    assert code == 2
    assert "words, max is 12" in err


def test_parenthesis_is_counted():
    code, err = _check("A line with (a parenthesis) in it.")
    assert code == 2
    assert "parenthesis" in err


def test_two_dashes_are_counted():
    code, err = _check("A line - with two - dashes.")
    assert code == 2
    assert "2 dashes" in err


def test_bare_path_is_counted():
    code, err = _check("The builder lives in connect/incremental.py today.")
    assert code == 2
    assert "path in chat" in err


def test_table_rows_are_exempt_from_the_word_count():
    table = (
        "| Source | What the loader does when the archive holds many parts |\n"
        "|---|---|\n"
        "| Zip specs | keeps only the single largest member, silently |\n"
    )
    code, err = _check(table)
    assert code == 0, err


def test_fenced_code_is_exempt():
    fenced = "Here it is.\n\n```\nfrom connect import db  # a path/inside.py and (parens)\n```\n"
    code, err = _check(fenced)
    assert code == 0, err


def test_one_report_link_is_allowed():
    code, err = _check("Receipts: [hire read](reports/engineering/hire_read.md)\n")
    assert code == 0, err


def test_second_report_link_is_blocked():
    two = "Receipts: [one](reports/a.md)\n\nAlso: [two](reports/b.md)\n"
    code, err = _check(two)
    assert code == 2
    assert "second report link" in err


def test_rewrites_are_still_counted():
    """The skeptic's blocker: attempt two used to sail through unchecked."""
    bad = "A line - with two - dashes."
    first = _check(bad, session="retry-a")
    second = _check(bad, session="retry-a")
    assert first[0] == 2
    assert second[0] == 2, "a broken rewrite must not stand"
    assert "Attempt 2" in second[1]


def test_retry_budget_runs_out_and_lets_it_stand():
    """And it must never trap the session in a rewrite loop."""
    bad = "A line - with two - dashes."
    codes = [_check(bad, session="retry-b")[0] for _ in range(5)]
    assert codes[:3] == [2, 2, 2]
    assert codes[3] == 0, "gate must give up after the budget"
    last = _check(bad, session="retry-b")
    assert last[0] == 2, "budget resets once it has given up"


def test_a_clean_rewrite_clears_the_budget():
    _check("A line - with two - dashes.", session="retry-c")
    assert _check(CLEAN, session="retry-c")[0] == 0
    assert "Attempt 1" in _check("A line - with two - dashes.", session="retry-c")[1]


def test_tight_em_dashes_are_counted():
    """Tight em-dashes were invisible. That was the whole dash rule in practice."""
    code, err = _check("Bar speak—plain words—short lines—here.")
    assert code == 2
    assert "dashes" in err


def test_hyphenated_words_are_still_legal():
    code, err = _check("A well-known short-form fresh-baked line.")
    assert code == 0, err


def test_long_link_text_cannot_smuggle_receipts():
    dump = "[Table shows 2.1M rows, 4 distinct ids, joins orphan, door two broken](reports/x.md)"
    code, err = _check(dump)
    assert code == 2, "a receipts dump must not ship as a pointer"


def test_windows_path_is_counted():
    code, err = _check(r"The file C:\Code\Ripple_v6\scripts was updated.")
    assert code == 2
    assert "path in chat" in err


def test_inline_code_does_not_hide_a_long_line():
    code, err = _check("`this is a very long backticked sentence that runs on` and on and on and on here.")
    assert code == 2
    assert "words" in err


def test_bare_url_is_not_a_path():
    code, err = _check("See https://example.com/a/b for it.")
    assert code == 0, err


def test_fullwidth_parens_are_counted():
    code, err = _check("A line with （fullwidth） parens.")
    assert code == 2
    assert "parenthesis" in err


def test_pipe_table_without_leading_pipe_is_exempt():
    code, err = _check("Source | what the loader does with many archive parts inside\n")
    assert code == 0, err


def test_gate_blocks_a_bad_message():
    code, err = _gate("A line - with two - dashes and (parens) here.")
    assert code == 2
    assert "shape counter blocked" in err


def test_gate_passes_a_clean_message():
    code, err = _gate(CLEAN)
    assert code == 0
    assert err == ""


def test_hooks_off_opens_the_gate():
    code, err = _gate("A line - with two - dashes and (parens).", hooks_off=True)
    assert code == 0
    assert err == ""


def test_hyphenated_label_before_a_report_link_is_allowed():
    """The gate's own first false positive: "Full write-up:" broke the label."""
    code, err = _check("Full write-up: [MAC_SETUP.md](docs/MAC_SETUP.md)\n")
    assert code == 0, err
