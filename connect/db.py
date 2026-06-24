"""Snowflake access for the connect engine.

Reuses the proven connection in library-onboarding/snow.py + config.py so there
is ONE source of truth for credentials (the gitignored library-onboarding/.env,
PAT-as-password). Connections are short-lived: open, query, close.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Optional

_REPO = Path(__file__).resolve().parents[1]
_LIB = _REPO / "library-onboarding"

# Load library-onboarding/.env explicitly (config.load_dotenv looks at CWD, which
# is wrong when these scripts run from the repo root) BEFORE importing config.
try:
    from dotenv import load_dotenv

    load_dotenv(_LIB / ".env", override=True)
except Exception:  # pragma: no cover
    pass

if str(_LIB) not in sys.path:
    sys.path.insert(0, str(_LIB))

import snow  # noqa: E402  (library-onboarding/snow.py)

RAW_DB = "LIBRARY_RAW"
RAW_SCHEMA = "LANDING"


def connect():
    """Open a Snowflake connection (PAT-as-password via snow.connect)."""
    return snow.connect()


def rows(conn, sql: str, params: Optional[tuple] = None) -> list[tuple]:
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        return cur.fetchall()
    finally:
        cur.close()


def dicts(conn, sql: str, params: Optional[tuple] = None) -> list[dict[str, Any]]:
    cur = conn.cursor()
    try:
        cur.execute(sql, params or ())
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def scalar(conn, sql: str, params: Optional[tuple] = None):
    return snow.fetch_scalar(conn, sql, params)


def fqn(table: str) -> str:
    """Fully-qualified landing table name from a bare table or SOURCE_ID."""
    t = table.strip().upper()
    if t.count(".") == 2:
        return t
    return f"{RAW_DB}.{RAW_SCHEMA}.{t}"
