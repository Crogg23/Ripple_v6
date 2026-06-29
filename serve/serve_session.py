"""Data-access shim that works in BOTH Streamlit-in-Snowflake (SiS) and a local
Streamlit, behind one function: ``run_df(sql, params)``.

WHY a shim: Phase 1 ships as a *local* Streamlit (it reuses library-onboarding/
snow.py + the connect engine verbatim, and reads the 7MB connection graph off
disk). But the whole data layer is written so the SAME app can be lifted into
Streamlit-in-Snowflake later with zero query rewrites:

    * SiS         -> snowflake.snowpark.context.get_active_session()  (no creds,
                     no local files; we borrow the session's underlying
                     snowflake-connector connection so pyformat %s binds work)
    * local       -> snow.connect()  (PAT-as-password from library-onboarding/.env)

Both paths hand back a real ``snowflake.connector`` cursor, so every query in
serve_queries.py uses ordinary ``%s`` binds and runs unchanged in either home.

The serving connection is forced onto the read-only role + the dedicated
SERVE_WH so analyst reads can never (a) run as ACCOUNTADMIN or (b) contend with
ETL on RIPPLE_WH/DBT_WH. If SERVE_WH does not exist yet, it degrades to the
current warehouse and records a note for the sidebar System panel.
"""

from __future__ import annotations

import os
import sys
import threading
from pathlib import Path

import pandas as pd
import streamlit as st

# Serving identity — overridable via env, but defaulted to the validated read-only
# role and the dedicated serve warehouse (see serve_wh.sql).
SERVE_ROLE = os.getenv("RIPPLE_SERVE_ROLE", "CLAUDE_MCP_READONLY")
SERVE_WH = os.getenv("RIPPLE_SERVE_WH", "SERVE_WH")

# Collected once at connect time, surfaced in the sidebar so Chris can see exactly
# what the app is running as (role / warehouse / SERVE_WH active?).
BOOT_NOTES: list[str] = []

# The cached connection is shared across Streamlit's script-runner threads; a single
# connection's cursors are not safe to drive concurrently, so serialize queries.
_LOCK = threading.Lock()


def _repo_root() -> Path:
    """Repo root (this file lives in <repo>/serve/)."""
    return Path(__file__).resolve().parents[1]


def _connector_conn_from_snowpark(sess):
    """Borrow the underlying snowflake-connector connection from a Snowpark session.

    Recent Snowpark exposes it publicly as ``session.connection``; older builds
    keep it at ``session._conn._conn``. Either way it speaks pyformat ``%s`` binds,
    which is what lets one SQL string serve both runtimes.
    """
    conn = getattr(sess, "connection", None)
    if conn is not None:
        return conn
    return sess._conn._conn  # pragma: no cover - fallback for older snowpark


def _try(cur_or_sess, sql, is_snowpark: bool) -> bool:
    try:
        if is_snowpark:
            cur_or_sess.sql(sql).collect()
        else:
            cur_or_sess.execute(sql)
        return True
    except Exception:
        return False


@st.cache_resource(show_spinner="Connecting to the Library…")
def _handle():
    """Open (once) the serving connection. Returns (mode, connection).

    mode is 'snowpark' (SiS) or 'connector' (local). In both cases the returned
    object is a snowflake-connector *connection* whose .cursor() we reuse.
    """
    BOOT_NOTES.clear()

    # 1) Streamlit-in-Snowflake / Snowpark -------------------------------------
    try:
        from snowflake.snowpark.context import get_active_session

        sess = get_active_session()
        # Best-effort pin (SiS usually pins these already; never fatal here).
        if not _try(sess, f"USE ROLE {SERVE_ROLE}", True):
            BOOT_NOTES.append(f"role pin skipped (SiS owner role in effect)")
        serve_ok = _try(sess, f"USE WAREHOUSE {SERVE_WH}", True)
        BOOT_NOTES.append("mode: streamlit-in-snowflake")
        BOOT_NOTES.append(f"serve_wh: {'SERVE_WH' if serve_ok else 'session default'}")
        return ("snowpark", _connector_conn_from_snowpark(sess))
    except Exception:
        pass  # not in SiS -> fall through to local

    # 2) Local Streamlit -> reuse library-onboarding/snow.py -------------------
    lib = _repo_root() / "library-onboarding"
    if str(lib) not in sys.path:
        sys.path.insert(0, str(lib))
    try:
        from dotenv import load_dotenv

        load_dotenv(lib / ".env", override=True)
    except Exception:
        pass

    import snow  # library-onboarding/snow.py (PAT-as-password)

    conn = snow.connect()
    cur = conn.cursor()
    try:
        # Order matters: assume the read-only role BEFORE selecting its warehouse.
        if _try(cur, f"USE ROLE {SERVE_ROLE}", False):
            BOOT_NOTES.append(f"role: {SERVE_ROLE}")
        else:
            BOOT_NOTES.append(f"role pin FAILED (still default role) — check grants")
        if _try(cur, f"USE WAREHOUSE {SERVE_WH}", False):
            BOOT_NOTES.append("serve_wh: SERVE_WH (isolated)")
        else:
            # SERVE_WH not created yet (run serve_wh.sql) -> stay on whatever the
            # role can use so the app still boots; nudge to create it.
            _try(cur, f"USE WAREHOUSE {os.getenv('SNOWFLAKE_WAREHOUSE', 'RIPPLE_WH')}", False)
            BOOT_NOTES.append("serve_wh: NOT FOUND — using fallback WH (run serve_wh.sql)")
    finally:
        cur.close()
    BOOT_NOTES.insert(0, "mode: local streamlit")
    return ("connector", conn)


def _is_conn_error(exc: Exception) -> bool:
    s = f"{type(exc).__name__}: {exc}".lower()
    return any(t in s for t in (
        "closed", "expired", "session no longer", "authentication",
        "could not connect", "operationalerror", "reset by peer",
    ))


def _run(sql: str, params):
    mode, conn = _handle()
    with _LOCK:  # serialize cursors on the shared cached connection
        cur = conn.cursor()
        try:
            cur.execute(sql, params if params else None)
            cols = [c[0] for c in cur.description] if cur.description else []
            rows = cur.fetchall() if cur.description else []
            return pd.DataFrame(rows, columns=cols)
        finally:
            cur.close()


def run_df(sql: str, params=None) -> pd.DataFrame:
    """Execute a parameterized query, return a DataFrame. One retry on a stale
    connection (X-Small auto-suspends at 60s; the cached connection can drop)."""
    try:
        return _run(sql, params)
    except Exception as exc:
        if _is_conn_error(exc):
            _handle.clear()
            return _run(sql, params)
        raise


def boot_status() -> dict:
    """Cheap status line for the sidebar System panel (no heavy COUNTs at boot)."""
    df = run_df(
        "SELECT CURRENT_ROLE() AS ROLE, CURRENT_WAREHOUSE() AS WH, "
        "CURRENT_ACCOUNT() AS ACCT, CURRENT_REGION() AS REGION"
    )
    row = df.iloc[0].to_dict() if len(df) else {}
    row["notes"] = list(BOOT_NOTES)
    return row
