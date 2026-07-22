"""The Reading Room's two Snowflake lanes — reader and scoped writer.

READER  — SNOWFLAKE_SERVE_PAT + RIPPLE_SERVE_ROLE (default RIPPLE_READER) on
          SERVE_WH: the enforced read lane. Falls back to the repo's default
          reader credential (snow.connect's own precedence) for READS only.
WRITER  — RIPPLE_REVIEW_PAT + role RIPPLE_REVIEW_WRITER: INSERT+SELECT on
          LIBRARY_META.REVIEW.DECISIONS and nothing else.

THE NO-FALLBACK RULE (no exceptions): if RIPPLE_REVIEW_PAT is missing or
broken, the write lane reports it and the app runs read-only with a banner.
SNOWFLAKE_PAT / SNOWFLAKE_SERVE_PAT are NEVER used for writes — append-only
is the database's guarantee, and it only holds on the scoped role.

No streamlit imports here — this module stays pure so the offline tests can
exercise it without a browser or a network.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LIB = REPO / "library-onboarding"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from dotenv import load_dotenv

# override=True is the repo-wide rule: stale shell/container env never wins.
load_dotenv(LIB / ".env", override=True)

import snow  # noqa: E402  (the repo's single credential source of truth)

WRITER_PAT_ENV = "RIPPLE_REVIEW_PAT"
WRITER_ROLE = "RIPPLE_REVIEW_WRITER"
WRITER_REMEDIATION = (
    "Write lane not provisioned: mint a fresh PAT scoped to "
    "RIPPLE_REVIEW_WRITER (Snowsight — see scripts/provision_review_lane.sql), "
    "add it to library-onboarding/.env as RIPPLE_REVIEW_PAT, and restart. "
    "PAT expiry is normal weather here, not an emergency."
)

_SESSION_PARAMS = {"STATEMENT_TIMEOUT_IN_SECONDS": 300}


def _clamp_secondary_roles(conn):
    """`role=` pins only the PRIMARY role — with secondary roles active
    (often ALL by default) a session would union in every granted role and
    the append-only wall would be app-theater. Clamp both lanes to exactly
    the role they claim to be.

    Role-restricted PATs (this repo's standard mint) open a RESTRICTED
    session that refuses USE SECONDARY ROLES outright (error 003107) —
    while already pinning one role harder than the clamp does. That path
    is accepted only on proof: CURRENT_SECONDARY_ROLES() must come back
    empty, otherwise refuse the connection."""
    cur = conn.cursor()
    try:
        cur.execute("USE SECONDARY ROLES NONE")
        return conn
    except Exception:
        cur.execute("SELECT CURRENT_SECONDARY_ROLES()")
        row = cur.fetchone()
        active = json.loads(row[0] or "{}").get("roles") if row else None
        if active == "":
            return conn  # restricted session, provably zero secondary roles
        raise RuntimeError(
            "Cannot clamp secondary roles and the session reports active "
            f"secondary roles ({active!r}) — refusing to run with a wider "
            "role set than the lane claims.")


def reader_connect():
    """The read lane. Prefers the serve PAT; read-only either way (role
    pinned to the reader role, secondary roles clamped)."""
    pat = (os.environ.get("SNOWFLAKE_SERVE_PAT") or "").strip() or None
    return _clamp_secondary_roles(snow.connect(
        pat=pat,
        role=os.environ.get("RIPPLE_SERVE_ROLE", "RIPPLE_READER"),
        warehouse=os.environ.get("RIPPLE_SERVE_WH", "SERVE_WH"),
        session_parameters=_SESSION_PARAMS,
    ))


def writer_status() -> tuple[str, str]:
    """('ready'|'missing', message) — checked WITHOUT connecting, so a
    missing PAT can never stall the UI. 'ready' means the env var exists;
    the first INSERT is the real proof (and its failure UX names this
    module's remediation)."""
    if not (os.environ.get(WRITER_PAT_ENV) or "").strip():
        return "missing", WRITER_REMEDIATION
    return "ready", "write lane configured (RIPPLE_REVIEW_PAT present)"


def writer_connect():
    """The write lane. Raises (never falls back) when unprovisioned."""
    state, msg = writer_status()
    if state != "ready":
        raise RuntimeError(msg)
    return _clamp_secondary_roles(snow.connect(
        pat=os.environ[WRITER_PAT_ENV].strip(),
        role=WRITER_ROLE,
        warehouse=os.environ.get("RIPPLE_SERVE_WH", "SERVE_WH"),
        session_parameters=_SESSION_PARAMS,
    ))
