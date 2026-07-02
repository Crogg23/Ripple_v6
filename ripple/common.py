"""Shared plumbing for every ripple subcommand: connection, Snowflake helpers,
pour detection, the 'since last time' state file, and cp1252-safe formatting.

Design rules (learned the hard way in this repo):
  * ripple uses COMPUTE_WH by default so it never queues behind a live pour on RIPPLE_WH.
  * output is ASCII-first (Windows consoles are cp1252 and crash on stray unicode).
  * anything that writes must first check pour_running() and refuse if a pour holds the log.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LIB = REPO / "library-onboarding"
STATE_PATH = REPO / "outputs" / "_ripple_state.json"

# library-onboarding holds snow.py / config.py; load its .env before importing them.
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))
try:
    from dotenv import load_dotenv
    load_dotenv(LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

# The session env leaves SNOWFLAKE_WAREHOUSE blank on purpose; default ripple to COMPUTE_WH
# so it self-defaults to the non-pour warehouse. RIPPLE_TASK_WAREHOUSE overrides.
TASK_WH = os.environ.get("RIPPLE_TASK_WAREHOUSE", "").strip() or "COMPUTE_WH"
os.environ.setdefault("SNOWFLAKE_WAREHOUSE", TASK_WH)

# Windows console is cp1252; emit UTF-8 with replacement so a stray glyph never crashes ripple.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # pragma: no cover
        pass


def now() -> datetime:
    return datetime.now(timezone.utc)


def now_iso() -> str:
    return now().isoformat()


# --------------------------------------------------------------- Snowflake
def connect(warehouse: str | None = None):
    """A Snowflake connection pinned to COMPUTE_WH (or RIPPLE_TASK_WAREHOUSE / the arg),
    so ripple never contends with a pour on RIPPLE_WH."""
    import snow  # library-onboarding/snow.py
    wh = (warehouse or TASK_WH).strip()
    conn = snow.connect()
    if wh and wh.replace("_", "").isalnum():
        try:
            conn.cursor().execute(f"USE WAREHOUSE {wh}")
        except Exception:  # pragma: no cover — best-effort; a bad WH shouldn't kill a read
            pass
    return conn


def rows(conn, sql: str, params: tuple = ()):  # list[tuple]
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        cur.close()


def dicts(conn, sql: str, params: tuple = ()):  # list[dict]
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def scalar(conn, sql: str, params: tuple = ()):
    r = rows(conn, sql, params)
    return r[0][0] if r and r[0] else None


def vstate(conn) -> dict[str, str]:
    """The whole V_STATE view as a {metric: value} dict — the derived source of truth."""
    try:
        return {m: v for m, v in rows(conn, "SELECT METRIC, VALUE FROM LIBRARY_META.REGISTRY.V_STATE")}
    except Exception:
        return {}


# --------------------------------------------------------------- pour detection
def pour_running() -> str | None:
    """Return the command line of a live onboarding pour (onboard.py) if one is running,
    else None. Windows tasklist can't see it behind python.exe — use Win32_Process."""
    try:
        if sys.platform.startswith("win"):
            ps = ("Get-CimInstance Win32_Process -Filter \"name='python.exe'\" | "
                  "Where-Object { $_.CommandLine -like '*onboard.py*' } | "
                  "Select-Object -First 1 -ExpandProperty CommandLine")
            out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                                 capture_output=True, text=True, timeout=15)
            line = (out.stdout or "").strip()
            return line or None
        out = subprocess.run(["pgrep", "-fal", "onboard.py"], capture_output=True, text=True, timeout=15)
        line = (out.stdout or "").strip().splitlines()
        return line[0] if line else None
    except Exception:
        return None


# --------------------------------------------------------------- 'since last time' state
def load_state() -> dict:
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    os.replace(tmp, STATE_PATH)


# --------------------------------------------------------------- ASCII-safe formatting
OK, WARN, BAD, DASH = "[OK]", "[!!]", "[XX]", "[--]"


def hr(char: str = "-", width: int = 74) -> str:
    return char * width


def header(title: str, width: int = 74) -> str:
    return f"{hr('=', width)}\n  {title}\n{hr('=', width)}"


def table(headers: list[str], data: list[list], widths: list[int] | None = None) -> str:
    """A plain ASCII table (no box-drawing glyphs — cp1252-safe)."""
    cols = len(headers)
    w = widths or [max(len(str(headers[i])), *(len(str(r[i])) for r in data)) if data
                   else len(str(headers[i])) for i in range(cols)]
    def fmt(r):
        return "  ".join(str(r[i]).ljust(w[i])[:w[i] + 20] for i in range(cols))
    out = [fmt(headers), "  ".join("-" * w[i] for i in range(cols))]
    out += [fmt(r) for r in data]
    return "\n".join(out)


def human_int(n) -> str:
    try:
        return f"{int(n):,}"
    except Exception:
        return str(n)
