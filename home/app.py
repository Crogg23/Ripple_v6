"""Ripple - one door.

Three rooms, no plumbing:

  FINDINGS   every wired cross-source pattern, live from the warehouse, sorted
             and filterable. This is where analysis starts WITHOUT writing SQL.
  LOOK UP    search any company/person/facility/ship -> everything the Library
             holds on them, across every source, with provenance.
  EXPLORE    the SQL room and the chart bench, for when you want the wheel.

This app deliberately owns no query logic of its own: FINDINGS reads the
persisted lead table the connect engine writes, LOOK UP reuses serve/'s tested
query layer. Nothing here can write to the warehouse, and nothing here is AI at
runtime - same house rules as every other surface.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

_ROOT = Path(__file__).resolve().parents[1]
for _p in (_ROOT, _ROOT / "serve"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(_ROOT / "library-onboarding" / ".env", override=True)

import serve_queries as sq  # noqa: E402  (serve/serve_queries.py)

from home import queries as Q  # noqa: E402

st.set_page_config(page_title="Ripple", page_icon="*", layout="wide")

def render_findings():
    st.title("Findings")
    st.caption("patterns the Library already connects across sources - nothing here "
               "is reviewed or published; it is where you start looking")

    counts = Q.rule_counts()
    if counts is None or counts.empty:
        st.warning("No findings are stored yet. Run the lead jobs to populate them.")
        return

    options = list(counts["RULE_NAME"])
    labels = {r: f"{Q.label_for(r)}  ({int(n):,})"
              for r, n in zip(counts["RULE_NAME"], counts["N"])}
    rule = st.selectbox("Pattern", options, format_func=lambda r: labels[r])

    row = counts[counts["RULE_NAME"] == rule].iloc[0]
    st.caption(f"last computed {row['LAST_RUN']:%Y-%m-%d %H:%M} - {int(row['N']):,} hits")

    limit = st.slider("How many to show", 25, 500, 100, step=25)
    df = Q.leads_for(rule, limit)
    if df is None or df.empty:
        st.info("No rows for this pattern.")
        return

    view = pd.DataFrame({
        "What was found": df["TITLE"],
        "How many records": df["EVIDENCE_COUNT"],
        "Detail": df["EVIDENCE"].map(Q.evidence_bits),
        "Confidence": df["SCORE"],
    })
    st.dataframe(view, width="stretch", hide_index=True)

    st.divider()
    pick = st.selectbox("Open one of these in Look up",
                        range(len(df)), format_func=lambda i: df["TITLE"].iloc[i])
    eid = df["LEFT_ENTITY_ID"].iloc[pick]
    if eid and st.button("Show everything the Library holds on this one"):
        st.session_state["room"] = "Look up"
        st.session_state["eid"] = eid
        st.rerun()

    with st.expander("Receipt - how this was computed"):
        st.write(f"As of: {df['AS_OF_DATE'].iloc[0]}")
        st.write(f"Query fingerprint: {df['SQL_SHA256'].iloc[0]}")
        st.caption("The exact SQL behind every row is stored next to it, so any "
                   "number here can be re-run and checked.")


def render_lookup():
    st.title("Look up")
    st.caption("a company, a person, a facility, a ship - everything the Library "
               "holds on them, across every source")

    eid = st.session_state.get("eid")
    term = st.text_input("Search by name, or paste an ID", key="lookup_term")

    if term:
        hits = sq.search_names(term, limit=25)
        if hits is None or len(hits) == 0:
            st.info("Nothing found under that name.")
            return
        idx = st.selectbox("Matches", range(len(hits)),
                           format_func=lambda i: (
                               f"{hits['CANONICAL_NAME'].iloc[i]} - "
                               f"{hits['ENTITY_TYPE'].iloc[i]} - "
                               f"in {int(hits['SOURCE_COUNT'].iloc[i])} sources"))
        eid = hits["ENTITY_ID"].iloc[idx]

    if not eid:
        return

    golden, _pairs, rows = sq.get_dossier(eid)
    if golden is not None and len(golden):
        g = golden.iloc[0]
        st.header(g.get("CANONICAL_NAME") or "(no name)")
        bits = [str(g.get("ENTITY_TYPE") or ""),
                f"identified by {g.get('KEY_TYPE','')} {g.get('KEY_VALUE','')}"]
        if g.get("CANONICAL_ADDR"):
            bits.append(str(g["CANONICAL_ADDR"]))
        st.caption(" - ".join(b for b in bits if b))

    if rows is None or len(rows) == 0:
        st.info("No cross-source rows for this one.")
        return

    st.subheader(f"Appears in {len(rows)} sources")
    for _, r in rows.iterrows():
        with st.container(border=True):
            st.markdown(f"**{r['SOURCE_TABLE']}** - {int(r.get('ROW_COUNT') or 0):,} rows")
            bits = Q.evidence_bits(r.get("PREVIEW"))
            if bits:
                st.caption(bits)


def render_explore():
    st.title("Explore")
    st.markdown(
        "- **Write your own query and chart it** - the Playground, at "
        "[127.0.0.1:8502](http://127.0.0.1:8502)\n"
        "- **Review and sign off findings** - the Reading Room, at "
        "[127.0.0.1:8890](http://127.0.0.1:8890)\n"
        "- **Build a chart from scratch** - the chart bench: `python bench/app.py`, "
        "then [127.0.0.1:8051](http://127.0.0.1:8051)")
    st.caption("These are separate apps on purpose - each one is tested on its own. "
               "This page is the map, not a wrapper.")


ROOMS = {"Findings": render_findings, "Look up": render_lookup, "Explore": render_explore}

with st.sidebar:
    st.markdown("### Ripple")
    # The room lives in session state under its own widget key, and the "open
    # this one in Look up" button writes that key before rerunning. Passing an
    # index as well would fight the stored value on every jump.
    st.session_state.setdefault("room", "Findings")
    room = st.radio("Room", list(ROOMS), key="room")
    st.caption("Nothing here writes to the warehouse. Nothing here is published.")

ROOMS[room]()
