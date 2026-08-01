"""The Ask room — pick a question, see its realm, write your own SQL, chart
it, keep it. A thin Streamlit shell over viz/* (guard, read lane, plugs,
safety, cards) plus the pack dictionary. No SQL is ever generated for the
user; the dictionary points, Chris drives.
"""
from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from viz import card as cardmod                    # noqa: E402
from viz import catalog as viz_catalog             # noqa: E402
from viz import plugs, safety, sqlrun              # noqa: E402
from playground import dictionary, packs, queries  # noqa: E402

_AUTO = "(auto)"


@st.cache_data(ttl=1800, show_spinner=False)
def _catalog_rows(fqns: tuple[str, ...]) -> dict[str, list[dict]]:
    """COLUMN_CATALOG rows grouped by fqn; {} when the table is absent/empty
    (the panel then degrades to a live profile)."""
    try:
        df, _ = sqlrun.run(queries.column_catalog_sql(list(fqns)),
                           limit_rows=5000)
    except Exception:
        return {}
    out: dict[str, list[dict]] = {}
    for rec in df.to_dict("records"):
        rec = {k.lower(): v for k, v in rec.items()}
        sv = rec.get("sample_values")
        if isinstance(sv, str):
            import json
            try:
                rec["sample_values"] = json.loads(sv)
            except Exception:
                rec["sample_values"] = None
        out.setdefault(rec["fqn"], []).append(rec)
    return out


@st.cache_data(ttl=1800, show_spinner=False)
def _live_count(fqn: str):
    try:
        df, _ = sqlrun.run(queries.live_count_sql(fqn), limit_rows=2)
        return int(df.iloc[0]["N"]) if len(df) else None
    except Exception:
        return None


def _live_profile_fallback(fqn: str) -> list[dict]:
    """When COLUMN_CATALOG has no rows for a table, profile it live so the
    panel is never empty — with a hint to build the durable catalog."""
    try:
        prof = viz_catalog.profile(fqn)
    except Exception:
        return []
    return [{"column_name": p["column"], "ordinal": i,
             "chart_role": p.get("role"), "sf_type": None,
             "nonnull_pct": p.get("nonnull_pct"),
             "plain_gloss": "", "detected_key": None, "key_tier": None,
             "sample_values": None, "profiled_at": None}
            for i, p in enumerate(prof, start=1)]


def _render_dictionary(pack: dict):
    st.markdown(f"### {pack['question']}")
    st.caption(pack["why"])

    fqns = tuple(t["fqn"] for t in pack["tables"])
    cat = _catalog_rows(fqns)
    counts = {f: _live_count(f) for f in fqns}
    degraded = [f for f in fqns if not cat.get(f)]
    if degraded:
        for f in degraded:
            cat[f] = _live_profile_fallback(f)
        st.caption("ℹ️ some tables have no durable dictionary rows yet — "
                   "showing a live profile. Run scripts/"
                   "build_column_catalog.py --apply for the full dictionary.")

    for panel in dictionary.pack_panels(pack, cat, counts):
        n = f"{panel['live_count']:,} rows" if panel["live_count"] is not None \
            else "row count unavailable"
        with st.expander(f"**{panel['name']}** — {n}", expanded=False):
            st.markdown(f"*{panel['role']}*")
            st.code(panel["fqn"], language=None)
            if panel["key_columns"]:
                st.markdown("**The columns that matter:**")
                for k in panel["key_columns"]:
                    st.markdown(f"- `{k['column']}`"
                                + (f" — {k['meaning']}" if k["meaning"] else ""))
            for j in panel["joins"]:
                st.markdown(f"- {j}")
            for trap in panel["traps"]:
                st.warning(trap)
            if panel["columns"]:
                st.markdown("**Every column, translated:**")
                st.dataframe(panel["columns"], use_container_width=True,
                             hide_index=True)
                if panel["profiled_at"]:
                    st.caption(f"dictionary profiled {panel['profiled_at']} — "
                               "refresh with build_column_catalog.py --only "
                               f"{panel['fqn']} --apply")

    if pack.get("observations"):
        st.markdown("**Worth knowing before you write SQL:**")
        for ob in pack["observations"]:
            st.markdown(f"- {ob}")


def _kwarg_editor(df, ranked, choice: str) -> dict:
    """Editable chart settings: start from the suggested kwargs, let Chris
    change x / y / color / labels / log scale. The dict returned here is the
    SAME dict the saved card gets — screen and artifact can never differ."""
    kwargs = dict(next(k for n, k, _ in ranked if n == choice))
    roles = plugs.column_roles(df)
    all_cols = list(df.columns)

    def _slot(label, key, wanted_kinds):
        options = [_AUTO] + [c for c in all_cols
                             if not wanted_kinds
                             or roles.get(c) in wanted_kinds] \
            if wanted_kinds else [_AUTO] + all_cols
        current = kwargs.get(key)
        idx = options.index(current) if current in options else 0
        pick = st.selectbox(label, options, index=idx, key=f"pg_{key}")
        if pick != _AUTO:
            kwargs[key] = pick
        elif key in kwargs:
            kwargs.pop(key, None)

    c1, c2, c3 = st.columns(3)
    with c1:
        if choice in ("bar", "line", "area", "scatter", "hist", "heatmap"):
            _slot("x axis", "x", None)
    with c2:
        if choice in ("bar", "line", "area", "scatter", "heatmap"):
            _slot("y axis", "y", None)
    with c3:
        if choice in ("bar", "line", "area", "scatter"):
            _slot("color by", "color", None)

    l1, l2, l3 = st.columns(3)
    labx = l1.text_input("x label (blank = column name)", key="pg_labx")
    laby = l2.text_input("y label (blank = column name)", key="pg_laby")
    logy = l3.checkbox("log scale (y)", key="pg_logy")
    labels = {}
    if labx and kwargs.get("x"):
        labels[kwargs["x"]] = labx
    if laby and kwargs.get("y"):
        labels[kwargs["y"]] = laby
    if labels:
        kwargs["labels"] = labels
    if logy and choice in ("bar", "line", "area", "scatter"):
        kwargs["log_y"] = True
    return kwargs


def render_ask():
    lane = sqlrun.lane_status()
    for note in lane["notes"]:
        (st.warning if note.startswith("[!!]") else st.caption)(note)

    ids = packs.pack_ids()
    labels = {p["id"]: p["question"] for p in packs.PACKS}
    left, right = st.columns([2, 3])

    with left:
        pick = st.selectbox("Pick a question", ids,
                            format_func=lambda i: labels[i], key="pg_pack")
        pack = packs.get_pack(pick)
        if pack and any("trap_stock_watcher_provenance" in t.get("traps", [])
                        for t in pack["tables"]):
            st.error("⚖️ **Journalism use only.** Financial-disclosure data "
                     "is legally restricted (5 USC 13107(c)(1)) — never for "
                     "any commercial product.")
        if pack:
            _render_dictionary(pack)

    with right:
        st.markdown("### Your SQL")
        st.caption("One read-only statement. The dictionary on the left "
                   "tells you where to look — the query is yours.")
        sql = st.text_area("SQL", height=220, key="pg_sql",
                           label_visibility="collapsed",
                           placeholder="select ... from ... group by ...")
        c1, c2 = st.columns([1, 3])
        run_it = c1.button("Run", type="primary", use_container_width=True)
        limit = c2.number_input("row cap", 100, 100_000, 10_000, step=1000)

        if run_it and sql.strip():
            try:
                df, meta = sqlrun.run(sql, limit_rows=int(limit))
                st.session_state["pg_result"] = (sql, df, meta, int(limit))
            except sqlrun.GuardError as e:
                st.error(str(e))
            except Exception as e:
                st.error("That query didn't run — check the SQL for a typo "
                         "or an unsupported statement.")
                with st.expander("details", expanded=False):
                    st.code(str(e))

        if "pg_result" not in st.session_state:
            return
        sql, df, meta, limit = st.session_state["pg_result"]
        st.caption(f"{len(df)} rows in {meta['elapsed_s']}s on "
                   f"{meta['warehouse']}"
                   + (" (truncated)" if meta["truncated"] else "")
                   + f" · {meta['budget']}")
        if dictionary.mentions_restricted(sql):
            st.error("⚖️ This result contains financial-disclosure data — "
                     "journalism use only (5 USC 13107(c)(1)).")

        classification = safety.classify_query(sql, df)
        ranked = plugs.suggest(df)
        names = [r[0] for r in ranked]
        choice = st.radio("chart type", names, horizontal=True, key="pg_plug",
                          help=" · ".join(f"{n}: {w}" for n, _, w in ranked))
        kwargs = _kwarg_editor(df, ranked, choice)

        tab_chart, tab_data, tab_code = st.tabs(["Chart", "Data", "Code"])
        with tab_chart:
            try:
                fig = plugs.PLUGS[choice](df, as_of=meta["as_of"], **kwargs)
            except Exception as e:
                st.error("That chart didn't render with these settings — "
                         "try different columns for x/y.")
                with st.expander("details", expanded=False):
                    st.code(str(e))
                return
            ba = safety.badge_args(classification)
            if ba:
                fig = safety.badge(fig, *ba)
                st.warning(f"{ba[0].upper()}: {ba[1]}")
            try:
                st.plotly_chart(fig, use_container_width=True, theme=None)
            except TypeError:
                st.plotly_chart(fig, use_container_width=True)
        with tab_data:
            st.dataframe(df.head(500), use_container_width=True,
                         hide_index=True)
        with tab_code:
            slug = st.text_input("investigation slug",
                                 value=st.session_state.get("pg_pack",
                                                            "playground"),
                                 key="pg_slug")
            if st.button("Save as card"):
                path = cardmod.new_card(slug=slug, sql=sql, plug=choice,
                                        plug_kwargs=kwargs,
                                        classification=classification,
                                        limit_rows=limit)
                st.success(f"card saved: {path} — edit it, run it, F5 the "
                           "tab. It appears under Saved cards.")
            preview = cardmod.render_body("qNN_preview.py", sql, choice,
                                          kwargs, classification,
                                          limit_rows=limit)
            st.code(preview, language="python")
