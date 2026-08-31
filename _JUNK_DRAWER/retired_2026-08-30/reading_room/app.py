"""Ripple — The Reading Room. Two desks, one router.

  CASE DESK    person/entity-grouped review of the hard-ID detectors —
               every claim about one person in one case file, decided
               per-claim (case_desk.py).
  PATTERN DESK cohort-grain review of the statistical detector — one verdict
               per peer cohort, member leads inherit unless individually
               decided (pattern_desk.py).

This file is UI routing ONLY: no SQL strings (queries.py owns SQL), no
rendering logic (render.py), no credential handling (connections.py), shared
plumbing in ui_common.py. Exactly one desk's code runs per rerun (a sidebar
radio, not st.tabs — tabs would execute BOTH desks' queries every click).

Run:  ./reading_room/run.sh   (or: streamlit run reading_room/app.py)
Local only. Nothing here can publish; verdicts are nominations, and the
write role physically cannot update or delete rows.

Stale-click safety: every decision form's key is the lead_id / cohort_id
being rendered — if the queue shifts between render and click, the old
form's submit is orphaned by its key and NO write happens.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

import connections  # noqa: E402
import queries  # noqa: E402
import case_desk  # noqa: E402
import pattern_desk  # noqa: E402
import ui_common  # noqa: E402

st.set_page_config(page_title="Ripple — The Reading Room", page_icon="🗂️",
                   layout="wide")

# ── header + lane banners ───────────────────────────────────────────────────
st.title("The Reading Room")
st.caption("lead review surface · every headline is a fixed SQL template · "
           "decisions are append-only rows, enforced by the database, not "
           "this app")

# Success flash from the previous run (st.rerun() wipes inline messages).
if st.session_state.get("flash"):
    st.success(st.session_state.pop("flash"))

writer_state, writer_msg = connections.writer_status()
if writer_state != "ready":
    st.warning(f"**Read-only mode.** {writer_msg}")

# ── portfolio header: both desks' open workloads, one round trip ────────────
portfolio = ui_common.read("portfolio", queries.PORTFOLIO_SQL)
if portfolio:
    p = portfolio[0]
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("People & entities (Case Desk)", f"{p.get('case_units') or 0:,}")
    m2.metric("… their open claims", f"{p.get('case_leads') or 0:,}")
    m3.metric("Cohorts (Pattern Desk)", f"{p.get('pattern_cohorts') or 0:,}")
    m4.metric("… establishments covered", f"{p.get('pattern_leads') or 0:,}")

# ── sidebar: desk switch + reviewer (desk modules add their own filters) ────
with st.sidebar:
    desk = st.radio("Desk", ["Case Desk", "Pattern Desk"], key="desk")
    st.divider()
    reviewer = st.text_input("Reviewer (required to decide)",
                             value=st.session_state.get("reviewer", ""))
    st.session_state["reviewer"] = reviewer
    st.divider()

# ── exactly one desk runs per rerun ─────────────────────────────────────────
if desk == "Pattern Desk":
    pattern_desk.render_desk(writer_state, reviewer)
else:
    case_desk.render_desk(writer_state, reviewer)
