"""Every hook must survive a machine that has python3 but no `python`.

This is the macOS case. The hooks were written on Windows, where `python` is on
PATH; a stock Mac has only `python3`. Before the shared resolver, four hooks —
the git guard among them — exited 127 and the protection they provided silently
stopped existing. Nothing announced it.

Each test runs the hook with a PATH that contains ONLY python3, the way the Mac
looks, and asserts the hook still does its job.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
HOOKS = REPO / ".claude" / "hooks"
STATE = REPO / ".claude" / "state"

BASH = shutil.which("bash")
pytestmark = pytest.mark.skipif(BASH is None, reason="no bash on this machine")


@pytest.fixture
def mac_like(tmp_path):
    """A PATH where the interpreter is called python3 and `python` does not exist."""
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    shim = fake_bin / "python3"
    shim.write_text(f'#!/bin/sh\nexec "{sys.executable}" "$@"\n')
    shim.chmod(0o755)

    # Keep the shell's own utilities reachable, drop everything that could
    # supply a bare `python`.
    keep = [p for p in (os.environ.get("PATH") or "").split(os.pathsep) if "Python" not in p]
    return {
        **os.environ,
        "PATH": os.pathsep.join([str(fake_bin), *keep]),
        "CLAUDE_PROJECT_DIR": str(REPO),
    }


def _run(hook: str, payload: dict, env: dict):
    proc = subprocess.run(
        [BASH, str(HOOKS / hook)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env,
    )
    return proc.returncode, (proc.stdout or ""), (proc.stderr or "")


def test_git_guard_still_blocks_on_a_mac(mac_like):
    code, _, err = _run(
        "block-dangerous-git.sh",
        {"session_id": "mac", "tool_input": {"command": "git reset --hard origin/main"}},
        mac_like,
    )
    assert code == 2, f"git guard let a hard reset through: {err}"


def test_git_guard_still_allows_a_safe_command_on_a_mac(mac_like):
    code, _, err = _run(
        "block-dangerous-git.sh",
        {"session_id": "mac", "tool_input": {"command": "git status"}},
        mac_like,
    )
    assert code == 0, err


def test_warehouse_gate_still_blocks_on_a_mac(mac_like):
    code, _, err = _run(
        "warehouse-gate.sh",
        {"session_id": f"mac-{uuid.uuid4()}", "tool_input": {"command": "python -m connect spine"}},
        mac_like,
    )
    assert code == 2, f"warehouse gate let a spine command through: {err}"


def test_drawer_guard_still_stings_on_a_mac(mac_like):
    code, out, _ = _run(
        "drawer-guard.sh",
        {"session_id": "mac", "tool_input": {"file_path": str(REPO / "_JUNK_DRAWER" / "x.md")}},
        mac_like,
    )
    assert "junk drawer" in out.lower()


def test_corrections_still_inject_on_a_mac(mac_like):
    code, out, err = _run(
        "chris-words.sh", {"session_id": "mac", "prompt": "hello"}, mac_like
    )
    assert code == 0, err
    assert "corrections" in out.lower(), "Chris's corrections stopped reaching the prompt"


def test_shape_gate_still_counts_on_a_mac(mac_like):
    for stale in STATE.glob("*.shape_tries"):
        stale.unlink(missing_ok=True)
    code, _, err = _run(
        "shape-gate.sh",
        {"session_id": f"mac-{uuid.uuid4()}", "last_assistant_message": "A line - with two - dashes."},
        mac_like,
    )
    for stale in STATE.glob("*.shape_tries"):
        stale.unlink(missing_ok=True)
    assert code == 2, err


@pytest.fixture
def no_python():
    r"""A machine with no usable interpreter at all.

    PATH alone cannot express this on Windows, because py.EXE sits in
    C:\WINDOWS and that folder has to stay reachable for the shell to work.
    The resolver carries a documented test seam for exactly this case.
    """
    return {
        **os.environ,
        "RIPPLE_HOOKS_FAKE_NO_PYTHON": "1",
        "CLAUDE_PROJECT_DIR": str(REPO),
    }


def test_safety_gates_fail_closed_with_no_python(no_python):
    """A gate that cannot run must block, not wave things through."""
    for hook in ("block-dangerous-git.sh", "warehouse-gate.sh"):
        code, _, err = _run(hook, {"session_id": "none", "tool_input": {"command": "git status"}}, no_python)
        assert code == 2, f"{hook} failed open"
        assert "no working python" in err


def test_conveniences_fail_open_but_say_so(no_python):
    for hook in ("drawer-guard.sh", "shape-gate.sh", "chris-words.sh"):
        code, _, err = _run(hook, {"session_id": "none", "prompt": "hi"}, no_python)
        assert code == 0, f"{hook} blocked the session"
        assert "no working python" in err


def test_kill_switch_beats_a_missing_interpreter(no_python):
    """With no python, `hooks off` must still be able to open the warehouse gate."""
    STATE.mkdir(parents=True, exist_ok=True)
    off = STATE / "hooks.off"
    off.touch()
    try:
        code, _, err = _run(
            "warehouse-gate.sh",
            {"session_id": "none", "tool_input": {"command": "python -m connect spine"}},
            no_python,
        )
    finally:
        off.unlink(missing_ok=True)
    assert code == 0, err
