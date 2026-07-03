"""The Workbench — the Reading Room's fifth view: ask ANY question, get a chart.

A thin Streamlit shell over viz/* — ALL logic (guard, discovery, plugs, safety,
cards) lives in the viz package so the CLI and the Workbench cannot drift, and
streamlit's absence costs zero capability. Charts render with theme=None so the
figure Chris sees here is byte-identical to what `python <card>.py` produces —
a learning tool must never show one thing and generate another.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# streamlit puts serve/ on sys.path, not the repo root — mirror serve_session.
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from viz import card as cardmod          # noqa: E402
from viz import catalog, plugs, safety, sqlrun, theme  # noqa: E402


def render_workbench():
    st.markdown("## 🛠 Workbench")
    st.caption("Any table, any question, read-only. The chart you get is real "
               "Plotly code — the Code tab IS the artifact.")

    lane = sqlrun.lane_status()
    for note in lane["notes"]:
        (st.warning if note.startswith("[!!]") else st.caption)(note)

    with st.expander("Find something to chart", expanded=False):
        term = st.text_input("search the catalog", key="wb_find",
                             placeholder="opioid, politics, shipping, storm ...")
        if term:
            hits = catalog.find(term)
            st.dataframe(
                [{"name": h["name"], "kind": h["kind"], "domain": h["domain"],
                  "rows": h["rows"], "sample": h["is_sample"], "fqn": h["fqn"]}
                 for h in hits[:30]],
                use_container_width=True, hide_index=True)

    sql = st.text_area("SQL (one read-only statement)", height=160, key="wb_sql",
                       placeholder="SELECT state, COUNT(*) AS n FROM ... GROUP BY 1")
    c1, c2 = st.columns([1, 3])
    run_it = c1.button("Run", type="primary", use_container_width=True)
    limit = c2.number_input("row cap", 100, 100_000, 10_000, step=1000)

    if run_it and sql.strip():
        try:
            df, meta = sqlrun.run(sql, limit_rows=int(limit))
        except sqlrun.GuardError as e:
            st.error(str(e))
            return
        st.session_state["wb_result"] = (sql, df, meta, int(limit))

    if "wb_result" not in st.session_state:
        return
    sql, df, meta, limit = st.session_state["wb_result"]
    st.caption(f"{len(df)} rows in {meta['elapsed_s']}s on {meta['warehouse']}"
               + (" (truncated)" if meta["truncated"] else "") + f" · {meta['budget']}")

    classification = safety.classify_query(sql, df)
    ranked = plugs.suggest(df)
    names = [r[0] for r in ranked]
    choice = st.radio("plug", names, horizontal=True, key="wb_plug",
                      help=" · ".join(f"{n}: {w}" for n, _, w in ranked))
    kwargs = dict(next(k for n, k, _ in ranked if n == choice))

    tab_chart, tab_data, tab_code = st.tabs(["Chart", "Data", "Code"])
    with tab_chart:
        fig = plugs.PLUGS[choice](df, as_of=meta["as_of"], **kwargs)
        ba = safety.badge_args(classification)
        if ba:
            fig = safety.badge(fig, *ba)
            st.warning(f"{ba[0].upper()}: {ba[1]}")
        try:
            st.plotly_chart(fig, use_container_width=True, theme=None)
        except TypeError:  # older streamlit without theme=
            st.plotly_chart(fig, use_container_width=True)
    with tab_data:
        st.dataframe(df.head(500), use_container_width=True, hide_index=True)
    with tab_code:
        slug = st.text_input("investigation slug", value="workbench", key="wb_slug")
        if st.button("Save as card"):
            path = cardmod.new_card(slug=slug, sql=sql, plug=choice,
                                    plug_kwargs=kwargs, classification=classification,
                                    limit_rows=limit)
            st.success(f"card saved: {path} — edit it, run it, F5 the tab. "
                       f"`ripple chart eject` inlines the plug source.")
        # the preview is built by the SAME function as the save — including the
        # badge line, so a lead query's code never looks cleaner than its card
        preview = cardmod.render_body("qNN_preview.py", sql, choice, kwargs,
                                      classification, limit_rows=limit)
        st.code(preview, language="python")
