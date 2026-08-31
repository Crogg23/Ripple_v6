"""The shape counter is the only guard that never has an opinion.

These tests are the disproving check for it. The counter runs as a Stop hook,
which fires AFTER the message has already been printed to Chris's terminal, so
blocking there cannot unprint anything — it can only force a rewrite that shows
up as a SECOND copy. That is why every test below asserts exit code 0: the
counter must never block. It writes what it found to a per-session carry file,
and the prompt hook injects that at the top of the next turn.

So the contract under test is: exit 0 always, carry file written when broken,
carry file absent when clean.
"""

from __future__ import annotations

import json
import os
import re
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


def _carry_path(session: str) -> Path:
    safe = re.sub(r"[^\w.\-]", "_", session)
    return REPO / ".claude" / "state" / f"{safe}.shape_carry"


def _check(message: str, session: str | None = None):
    """Run the counter and return (exit code, what it parked for next turn).

    The second element used to be stderr. It is now the carry file's contents,
    because that is where findings go under the non-blocking contract.
    """
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
    carry = _carry_path(session)
    parked = carry.read_text(encoding="utf-8").strip() if carry.exists() else ""
    return proc.returncode, parked


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
    carry = _carry_path("gate-test")
    parked = carry.read_text(encoding="utf-8").strip() if carry.exists() else ""
    return proc.returncode, parked


@pytest.fixture(autouse=True)
def _fresh_carry_files():
    """Carry files live on disk, so a previous run would leak into this one."""
    state = REPO / ".claude" / "state"
    for pattern in ("*.shape_carry", "*.shape_tries"):
        for stale in state.glob(pattern):
            stale.unlink(missing_ok=True)
    yield
    for pattern in ("*.shape_carry", "*.shape_tries"):
        for stale in state.glob(pattern):
            stale.unlink(missing_ok=True)


CLEAN = "## Header\n\nShort line here.\n\nAnother short line.\n\n- clean bullet\n"


def test_clean_message_passes_silently():
    code, err = _check(CLEAN)
    assert code == 0
    assert err == ""


def test_long_line_is_counted():
    long_line = "This line is deliberately far too long because it keeps adding clauses forever."
    code, err = _check(long_line)
    assert code == 0, "the counter must never block"
    assert "words, max is 12" in err


def test_parenthesis_is_counted():
    code, err = _check("A line with (a parenthesis) in it.")
    assert code == 0, "the counter must never block"
    assert "parenthesis" in err


def test_two_dashes_are_counted():
    code, err = _check("A line - with two - dashes.")
    assert code == 0, "the counter must never block"
    assert "2 dashes" in err


def test_bare_path_is_counted():
    code, err = _check("The builder lives in connect/incremental.py today.")
    assert code == 0, "the counter must never block"
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
    assert code == 0, "the counter must never block"
    assert "second report link" in err


def test_a_repeat_offence_is_parked_again():
    """The old retry budget is gone; there is nothing left to run out.

    Under the blocking design a rewrite loop was possible, so the counter kept a
    budget and surrendered after three tries. Nothing blocks now, so every turn
    is judged fresh on its own and the same break parks the same note again.
    """
    bad = "A line - with two - dashes."
    first = _check(bad, session="retry-a")
    second = _check(bad, session="retry-a")
    assert first[0] == 0 and second[0] == 0
    assert "2 dashes" in first[1]
    assert "2 dashes" in second[1]
    assert "Attempt" not in second[1], "no retry counter should survive"


def test_a_clean_turn_clears_the_carry_file():
    """A clean message must not leave last turn's complaint lying around."""
    _check("A line - with two - dashes.", session="retry-c")
    assert _carry_path("retry-c").exists()
    code, parked = _check(CLEAN, session="retry-c")
    assert code == 0
    assert parked == ""
    assert not _carry_path("retry-c").exists()


def test_the_counter_never_blocks_however_broken():
    """The double-output bug in one assertion.

    Blocking here printed the message, then the rewrite. Whatever the counter
    finds, its exit code stays 0 so Chris only ever sees one copy.
    """
    worst = chr(10).join(
        [
            "This line is far too long and it keeps adding clauses forever",
            "A line - with two - dashes and (parens) here",
            "See connect/incremental.py and reports/a.md and reports/b.md",
        ]
    )
    code, parked = _check(worst)
    assert code == 0, "a Stop hook that blocks prints the message twice"
    assert parked, "but it must still record what it found"


def test_tight_em_dashes_are_counted():
    """Tight em-dashes were invisible. That was the whole dash rule in practice."""
    code, err = _check("Bar speak—plain words—short lines—here.")
    assert code == 0, "the counter must never block"
    assert "dashes" in err


def test_hyphenated_words_are_still_legal():
    code, err = _check("A well-known short-form fresh-baked line.")
    assert code == 0, err


def test_long_link_text_cannot_smuggle_receipts():
    dump = "[Table shows 2.1M rows, 4 distinct ids, joins orphan, door two broken](reports/x.md)"
    code, err = _check(dump)
    assert err, "a receipts dump must not ship as a pointer"


def test_windows_path_is_counted():
    code, err = _check(r"The file C:\Code\Ripple_v6\scripts was updated.")
    assert code == 0, "the counter must never block"
    assert "path in chat" in err


def test_inline_code_does_not_hide_a_long_line():
    code, err = _check("`this is a very long backticked sentence that runs on` and on and on and on here.")
    assert code == 0, "the counter must never block"
    assert "words" in err


def test_bare_url_is_not_a_path():
    code, err = _check("See https://example.com/a/b for it.")
    assert code == 0, err


def test_fullwidth_parens_are_counted():
    code, err = _check("A line with （fullwidth） parens.")
    assert code == 0, "the counter must never block"
    assert "parenthesis" in err


def test_pipe_table_without_leading_pipe_is_exempt():
    code, err = _check("Source | what the loader does with many archive parts inside\n")
    assert code == 0, err


def test_gate_parks_a_bad_message_without_blocking():
    code, err = _gate("A line - with two - dashes and (parens) here.")
    assert code == 0, "the counter must never block"
    assert "on your LAST message" in err
    assert "parenthesis" in err and "2 dashes" in err


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
