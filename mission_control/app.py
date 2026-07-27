"""Ripple — Mission Control.

One-page dashboard. Shows the state of the machine at a glance.
No interactivity needed. Open, look, close.

    streamlit run mission_control/app.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import streamlit as st

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))

from dotenv import load_dotenv
load_dotenv(REPO / "library-onboarding/.env", override=True)

import snow  # noqa: E402

st.set_page_config(page_title="Ripple — Mission Control", page_icon="📡", layout="wide")


@st.cache_resource
def _conn():
    # Use serve lane if configured; otherwise just use whatever .env has.
    # Skip RIPPLE_READER attempt entirely if no serve PAT is set (avoids
    # a slow failed-auth round trip on every load).
    serve_pat = (os.environ.get("SNOWFLAKE_SERVE_PAT") or "").strip() or None
    if serve_pat:
        try:
            conn = snow.connect(
                pat=serve_pat,
                role=os.environ.get("RIPPLE_SERVE_ROLE", "RIPPLE_READER"),
                warehouse=os.environ.get("RIPPLE_SERVE_WH", "SERVE_WH"),
            )
        except Exception:
            conn = snow.connect()
    else:
        conn = snow.connect()
    # grab session info for the connection panel
    cur = conn.cursor()
    cur.execute("SELECT CURRENT_ACCOUNT(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_USER()")
    info = cur.fetchone()
    return conn, {"account": info[0], "role": info[1], "warehouse": info[2], "user": info[3]}


def q(sql: str) -> list[tuple]:
    cur = _conn()[0].cursor()
    cur.execute(sql)
    return cur.fetchall()


# ─── LOAD ALL DATA IN 2 QUERIES ──────────────────────────────────────────────

state_rows = q("SELECT METRIC, VALUE FROM LIBRARY_META.REGISTRY.V_STATE")
STATE = {r[0]: r[1] for r in state_rows}

build_rows = q("SELECT METRIC, VALUE FROM LIBRARY_META.BUILD.V_BUILD_STATE")
BUILD = {r[0]: r[1] for r in build_rows}

conn_info = _conn()[1]


def s(metric: str) -> str:
    return STATE.get(metric, "—")


def fmt(n) -> str:
    try:
        return f"{int(n):,}"
    except (ValueError, TypeError):
        return str(n)


# ─── HEADER ───────────────────────────────────────────────────────────────────

st.markdown("# 📡 Mission Control")
st.caption("A live snapshot of everything in the Ripple data warehouse. Refresh the page for fresh numbers.")

# ─── CONNECTION ───────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Connection")
st.caption("Where this data lives and how we're talking to it right now.")
cc1, cc2, cc3, cc4 = st.columns(4)
cc1.markdown(f"**Account**  \n`{conn_info['account']}`")
cc2.markdown(f"**User**  \n`{conn_info['user']}`")
cc3.markdown(f"**Role**  \n`{conn_info['role']}`")
cc4.markdown(f"**Warehouse**  \n`{conn_info['warehouse']}`")

# ─── THE WAREHOUSE ────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### The Warehouse")
st.caption(
    "Raw government data we've collected. Every table is a different federal dataset "
    "(FDA drug reports, SEC filings, EPA facilities, etc.) loaded into one place."
)
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Rows", fmt(s("landing.rows")))
c2.metric("Landing Tables", fmt(s("landing.tables")))
c3.metric("Cataloged Sources", fmt(s("catalog.sources")))
c4.metric("Registered Sources", fmt(s("registry.sources")))

# ─── THE CONNECTION ENGINE ────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### The Connection Engine")
st.caption(
    "The part that finds the same person/company/facility across different databases. "
    "\"Entities\" are unique people or orgs. \"Edges\" are the links between databases "
    "that prove two records are the same entity."
)
e1, e2, e3 = st.columns(3)
e1.metric("Resolved Entities", fmt(s("connect.entities")))
e2.metric("Cross-Database Links", fmt(s("connect.edges")))
e3.metric("Incremental Edges", fmt(s("connect.edges_inc")))

# ─── LEADS ────────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Active Leads")
st.caption(
    "Red flags the system found automatically — e.g., a doctor who got banned "
    "but is still receiving government payments. Each detector looks for a specific "
    "type of contradiction across databases."
)

lead_metrics = sorted(
    [(k, int(v)) for k, v in STATE.items() if k.endswith(".active") and k.startswith("leads.")],
    key=lambda x: -x[1]
)

if lead_metrics:
    cols = st.columns(min(len(lead_metrics), 4))
    for i, (metric, val) in enumerate(lead_metrics):
        name = metric.replace("leads.", "").replace(".active", "").replace("_", " ").title()
        cols[i % len(cols)].metric(name, fmt(val))
else:
    st.info("No active leads found.")

total_leads = sum(v for _, v in lead_metrics)
st.caption(f"**{total_leads:,} total active leads** across {len(lead_metrics)} detectors")

# ─── BUILD HEALTH ─────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Build Health")
st.caption(
    "Known issues and pending to-dos for the system itself. "
    "Blockers = things that need fixing before we can move forward. "
    "Defects = known bugs or data problems, tracked but not urgent."
)

bc1, bc2, bc3 = st.columns(3)
blockers = int(BUILD.get("defects_blocker", 0))
defects = int(BUILD.get("defects_open", 0))
actions = int(BUILD.get("actions_pending", 0))

bc1.metric("Blockers", blockers)
bc2.metric("Open Defects", defects)
bc3.metric("Pending Actions", actions)

if blockers > 0:
    st.error(f"🚨 {blockers} blocker(s) — something needs fixing before we move forward")
elif defects > 5:
    st.warning(f"⚠️ {defects} open defects — nothing blocking, but the pile is growing")
else:
    st.success("All clear — no blockers, defect count is manageable")

# ─── SOURCE PIPELINE ──────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Source Pipeline")
st.caption(
    "Every government dataset moves through these stages before it's usable. "
    "Think of it as a funnel: discovered → downloaded → cleaned → ready to query."
)

stages = ["queued", "scouted", "sampled", "landed", "modeled"]
labels = {
    "queued": "Queued (waiting)",
    "scouted": "Scouted (found)",
    "sampled": "Sampled (previewed)",
    "landed": "Landed (downloaded)",
    "modeled": "Modeled (cleaned & ready)",
}
stage_vals = {st_name: int(s(f"taps.{st_name}") or 0) for st_name in stages}

cols = st.columns(len(stages))
for i, st_name in enumerate(stages):
    cols[i].metric(labels[st_name], fmt(stage_vals[st_name]))

total_sources = sum(stage_vals.values())
failed = int(s('taps.failed') or 0)
stale = int(s('taps.stale') or 0)
st.caption(
    f"**{total_sources:,} sources** total · "
    f"**{stage_vals['landed'] + stage_vals['modeled']}** ready to use · "
    f"**{failed}** failed · **{stale}** stale"
)

# ─── FRESHNESS ────────────────────────────────────────────────────────────────

st.markdown("---")
st.markdown("### Freshness")
st.caption(
    "How up-to-date things are. \"Stale marts\" = cleaned tables that are behind "
    "their raw source. \"Orphans\" = catalog entries with no actual data behind them."
)
fc1, fc2, fc3 = st.columns(3)
fc1.metric("Stale Marts", s("marts.stale_vs_landing"))
fc2.metric("Catalog Orphans", fmt(s("catalog.orphans")))
fc3.metric("Reading Room Views", fmt(s("reading_room.views")))

# ─── FOOTER ───────────────────────────────────────────────────────────────────

st.markdown("---")
st.caption(
    "Data pulled from `LIBRARY_META.REGISTRY.V_STATE` + `LIBRARY_META.BUILD.V_BUILD_STATE`. "
    "This page is read-only — it can't change anything."
)
