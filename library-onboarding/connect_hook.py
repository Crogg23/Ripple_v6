"""Checkpoint 6 bridge: onboard.py -> the incremental CONNECT engine.

onboard.py runs with CWD = library-onboarding, where the top-level ``connect``
package (at the repo root) is NOT importable as-is. This thin wrapper shells out
to ``python -m connect.incremental connect-one`` from the repo root so the connect
engine keeps its OWN connection/role boundary (it writes to LIBRARY_META.CONNECT;
the onboarding agent is read-mostly there). Mirrors how connect/db.py bridges the
two directories.

Returns a small dict the checkpoint renderer can show. Never raises into the
onboarding flow on a soft failure — onboarding already succeeded at REGISTRY;
linking is a bonus that the heartbeat (`connect connect-changed`) will retry.
"""

from __future__ import annotations

import ast
import subprocess
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent


def connect_one(source_id: str, landing_table: str | None = None, timeout: int = 900) -> dict:
    """Link the just-landed table into the spine/graph. Bounded by the engine's
    PAIR_BUDGET so a high-fan-out table can't hang the onboarding step."""
    target = landing_table or source_id
    cmd = [sys.executable, "-m", "connect.incremental", "connect-one", "--source", target]
    try:
        proc = subprocess.run(cmd, cwd=str(_REPO), capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"status": f"connect timed out after {timeout}s (heartbeat will retry)", "ok": False}
    tail = (proc.stdout or "").strip().splitlines()
    summary = tail[-1] if tail else ""
    # the engine prints a `connect-one TABLE: {dict}` line; surface its dict if present
    detail = {}
    if ":" in summary and "{" in summary:
        try:
            detail = ast.literal_eval(summary[summary.index("{"):])
        except Exception:
            detail = {}
    return {
        "status": summary or (proc.stderr or "").strip()[-300:] or "no output",
        "ok": proc.returncode == 0,
        "mode": detail.get("mode", ""),
        "detail": detail,
        "stderr": (proc.stderr or "").strip()[-300:],
    }
