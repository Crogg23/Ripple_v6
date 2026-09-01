"""Snowflake access for the connect engine.

Reuses the proven connection in library-onboarding/snow.py + config.py so there
is ONE source of truth for credentials (the gitignored library-onboarding/.env,
PAT-as-password). Connections are short-lived: open, query, close.
"""

from __future__ import annotations

import sys
from pathlib import Path
import re
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
    """Open a Snowflake connection (PAT-as-password via snow.connect).

    Lane pinning (2026-07-20): the spine is BUILD work and must never burn the
    serving warehouse. When SNOWFLAKE_ETL_WAREHOUSE is set (library-onboarding/
    .env), every connect() here pins to it; unset, it falls back to the default
    SNOWFLAKE_WAREHOUSE exactly as before.
    """
    import os

    etl_wh = (os.environ.get("SNOWFLAKE_ETL_WAREHOUSE") or "").strip() or None
    return snow.connect(warehouse=etl_wh)


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


_IDENT = re.compile(r"^[A-Z0-9_$]+$")


def ident(name: str) -> str:
    """Validate one SQL identifier for safe interpolation into DDL/DML text.

    Everything in connect/ builds SQL by f-string; the values are table and
    column names from our own registry, but nothing ENFORCED that before a
    reviewer had to prove it call site by call site (hiring review, connect
    W4). Uppercase alnum + underscore + $ or it raises -- no quoting games.
    """
    n = name.strip().upper()
    if not _IDENT.match(n):
        raise ValueError(f"unsafe SQL identifier: {name!r}")
    return n


def fqn(table: str) -> str:
    """Fully-qualified landing table name from a bare table or SOURCE_ID.
    Every part is validated by ident() -- an unsafe name raises here, not
    somewhere inside a MERGE five calls later."""
    t = table.strip().upper()
    if t.count(".") == 2:
        return ".".join(ident(p) for p in t.split("."))
    return f"{RAW_DB}.{RAW_SCHEMA}.{ident(t)}"
