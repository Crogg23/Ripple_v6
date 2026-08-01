"""Shared Reading Room UI plumbing — connection caches, the read helper with
the mandated failure UX, friendly-error mapping, and the generic decision
write-confirm-flash routine both desks call. NO SQL strings in this file
(queries.py owns every statement — the offline no-SQL scan covers this
module too) and no rendering logic (render.py owns it).
"""
from __future__ import annotations

import streamlit as st

import connections


def friendly_error(e: Exception) -> str:
    """A plain-English one-liner for a reviewer, with the raw exception
    shown separately for anyone who needs to debug it."""
    s = str(e).lower()
    if any(t in s for t in ("closed", "expired", "no longer exists",
                            "reset by peer", "could not connect",
                            "operationalerror")):
        return ("Can't reach the warehouse right now — it may have gone "
                "idle. Try again in a moment.")
    if "not authorized" in s or "insufficient privileges" in s:
        return "This role doesn't have access to that data."
    if "does not exist" in s:
        return ("A table or view this desk needs isn't provisioned yet — "
                "run scripts/provision_pattern_desk.sql and build_review, "
                "then reload.")
    if "compilation error" in s or "syntax error" in s:
        return "That query isn't valid SQL — this is a bug, not something you did."
    return "Something went wrong talking to the warehouse."


def show_error(banner, e: Exception, label: str = "details"):
    banner(friendly_error(e))
    with st.expander(label, expanded=False):
        st.code(str(e))


# ── lanes (cached per process; cleared + retried once if Snowflake killed
#    an idle session, so one expired connection never bricks the app) ────────
@st.cache_resource
def _reader():
    return connections.reader_connect()


@st.cache_resource
def _writer():
    return connections.writer_connect()


def read(name: str, sql: str, params: tuple = ()):  # -> list[dict]
    """Reader-lane query with the mandated failure UX: errors carry the
    query NAME, never a blank page. Retries exactly once on a dead cached
    connection (idle-killed sessions are normal weather)."""
    for attempt in (1, 2):
        try:
            cur = _reader().cursor()
            cur.execute(sql, params or None)
            cols = [d[0].lower() for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
        except Exception as exc:
            if attempt == 1:
                _reader.clear()  # drop the dead connection, reconnect once
                continue
            show_error(st.error, exc, label=f"query '{name}' — details")
            st.stop()


def sticky_radio_guard(key: str, valid_options):
    """Pop a stale widget value before st.radio reconciles session_state
    against new options (a just-decided item dropping out of the queue would
    otherwise raise instead of falling back to the default)."""
    if st.session_state.get(key) not in valid_options:
        st.session_state.pop(key, None)


def write_decision(insert_sql: str, confirm_sql: str, params: tuple,
                   target_id: str, flash_suffix: str = "") -> None:
    """The shared write path: run the insert (retrying once on a dead
    cached connection), read back the reviewer-scoped latest row, then flash+rerun
    on success / warn on a lost race / hard-error on an unreadable write.
    `params` comes from queries.decision_params / cohort_decision_params —
    positions 1 and 3 are the verdict and the cleaned reviewer name."""
    try:
        try:
            wcur = _writer().cursor()
            wcur.execute(insert_sql, params)
        except Exception:
            _writer.clear()  # dead cached connection — reconnect once
            wcur = _writer().cursor()
            wcur.execute(insert_sql, params)
        verdict, reviewer_clean = params[1], params[3]
        wcur.execute(confirm_sql, (target_id, reviewer_clean))
        landed = wcur.fetchone()
        if not landed:
            st.error("Insert reported success but the decision row is not "
                     "readable back — do NOT retry blindly; check "
                     "LIBRARY_META.REVIEW.DECISIONS.")
        elif landed[0] != verdict:
            # A newer row from this same reviewer already landed (e.g. a
            # double-submit from two tabs) between our write and this
            # read-back — the row we just wrote is real, but not the latest.
            st.warning(
                f"Your **{verdict}** on `{target_id}` was written, but a "
                f"newer decision (**{landed[0]}** by {landed[1]} at "
                f"{landed[2]}) has since landed for this reviewer on this "
                f"target — that one wins. Append-only: nothing was lost, "
                f"but check the row.")
            st.rerun()
        else:
            st.session_state["flash"] = (
                f"Recorded **{landed[0]}** on `{target_id}` by {landed[1]} "
                f"at {landed[2]} — append-only, latest verdict wins. (A "
                f"repeat click would add a harmless duplicate row, never "
                f"corrupt.){flash_suffix}")
            st.rerun()  # refetch the queue — the decided item drops out NOW
    except Exception as exc:
        show_error(st.error, exc, label="write failure details")
        if "expired" in str(exc).lower() or "auth" in str(exc).lower():
            st.info(connections.WRITER_REMEDIATION)


def decision_gate(writer_state: str, reviewer: str) -> bool:
    """Render the enable/disable hints for the decision buttons; return
    whether deciding is allowed. Shared by both desks so the messaging
    never drifts."""
    if writer_state == "ready" and not (reviewer or "").strip():
        st.info("Enter your reviewer name in the sidebar to enable the buttons.")
    elif writer_state != "ready":
        st.info("Buttons are disabled — the write lane isn't provisioned yet "
                "(see the banner at the top of the page).")
    return writer_state == "ready" and bool((reviewer or "").strip())
