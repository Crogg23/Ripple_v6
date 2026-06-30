"""Ripple — the Reading Room (Phase 1 SERVE layer).

ONE Streamlit app that surfaces the already-built moat, live:
  • a SEARCH front door over entities (the 9.8M-entity backbone) + sources (CATALOG)
  • a live ENTITY DOSSIER — pull every cross-domain thread + affiliations, with a
    FRESHNESS badge + PROVENANCE receipt inline on every row, and a jump into the
    connection graph
  • the CONNECTION GRAPH, drawn live from the cached connect_graph.json (the 17MB
    frozen HTML is retired)
  • a SOURCE page — catalog metadata, freshness, the run-it-yourself receipt, and a
    25-row live sample

Deep-linkable: ?view=dossier&eid=ENT_… · ?view=source&src=fed_… · ?view=graph&focus=…
Run:  streamlit run serve/app.py     (see serve/README.md)
"""

from __future__ import annotations

import math

import streamlit as st

import serve_queries as q
import serve_graph as G
from serve_session import boot_status

st.set_page_config(page_title="Ripple — Reading Room", page_icon="📖", layout="wide")

# --------------------------------------------------------------------------- #
# Freshness badge vocabulary
# --------------------------------------------------------------------------- #
# NOTE: 'static' is forward-compat only — the freshness ledger collapses static-cadence
# sources to 'fresh' (build_freshness_ledger.freshness_state + V_SOURCE_FRESHNESS), so
# state never actually arrives as 'static' today; kept so the badge is ready if it does.
_BADGE = {
    "fresh": ("🟢", "fresh"), "static": ("🔵", "static"), "due": ("🟡", "due"),
    "overdue": ("🟠", "overdue"), "stale": ("🔴", "stale"), "dead": ("⚫", "dead"),
    "unknown": ("⚪", "recency unverified"),
}


def _int(x, default=0):
    """NaN/None-safe int(). A mixed int+NULL column from pd.DataFrame(cur.fetchall())
    arrives as float64 with float('nan'); `nan is not None` is True and `nan or 0` is
    nan, so a bare int(x) raises ValueError on the NULL rows. Route every nullable
    numeric through this so the NULL path falls back instead of crashing the render."""
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)):
            return default
        return int(x)
    except (TypeError, ValueError):
        return default


def goto(**params):
    st.query_params.clear()
    st.query_params.update({k: str(v) for k, v in params.items() if v is not None})
    st.rerun()


def _ts(x) -> str:
    return "" if x is None else str(x)[:19]


def fresh_caption(dec: dict) -> str:
    state = (dec or {}).get("freshness_state", "unknown")
    icon, label = _BADGE.get(state, _BADGE["unknown"])
    if state == "unknown":
        loaded = _ts(dec.get("loaded_at")) if dec else ""
        tail = f" · last loaded {loaded}" if loaded else " · never loaded"
        return f"{icon} {label}{tail}"
    bits = [f"{icon} {label}"]
    if dec.get("data_through"):
        bits.append(f"data through {_ts(dec['data_through'])}")
    if dec.get("data_age_days") is not None:
        bits.append(f"{int(dec['data_age_days'])}d old")
    if dec.get("cadence"):
        bits.append(str(dec["cadence"]))
    return " · ".join(bits)


def receipt_caption(dec: dict) -> str:
    if not dec or not dec.get("run_id"):
        return "receipt: no successful ingest run on record"
    rid = str(dec["run_id"])[:8]
    sha = (str(dec["sha256"])[:12] + "…") if dec.get("sha256") else "—"
    loaded = _ts(dec.get("loaded_at"))
    url = dec.get("source_url")
    link = f" · [verify source ↗]({url})" if url else ""
    return f"receipt: run `{rid}` · sha `{sha}` · loaded {loaded}{link}"


def render_decorated_source(source_id: str, dec: dict):
    """Freshness + provenance, inline, for one source."""
    st.caption(fresh_caption(dec.get(source_id.lower(), {})))
    st.caption(receipt_caption(dec.get(source_id.lower(), {})))


# --------------------------------------------------------------------------- #
# Sidebar — nav + System panel
# --------------------------------------------------------------------------- #
def sidebar():
    with st.sidebar:
        st.markdown("## 📖 Ripple\n**The Reading Room**")
        st.caption("Library of Alexandria for the investigative data analyst — "
                   "every public dataset, connected by identity.")
        if st.button("🔎  Search", use_container_width=True):
            goto(view="search")
        if st.button("🕸  Connection graph", use_container_width=True):
            goto(view="graph")
        st.divider()
        with st.expander("System", expanded=False):
            try:
                s = boot_status()
                st.write(f"**role** `{s.get('ROLE','?')}`")
                st.write(f"**warehouse** `{s.get('WH','?')}`")
                st.write(f"**account** `{s.get('ACCT','?')}` ({s.get('REGION','')})")
                for n in s.get("notes", []):
                    st.caption(n)
                fv = q.freshness_view_exists()
                st.caption("freshness ledger: " + ("✅ V_SOURCE_FRESHNESS live"
                           if fv else "⚪ absent — badges show 'recency unverified'"))
            except Exception as e:
                st.error(f"connection problem: {e}")
        st.caption("Phase 1 · read-only · defer NL→SQL / auth / case folders")


# --------------------------------------------------------------------------- #
# SEARCH
# --------------------------------------------------------------------------- #
def render_search():
    st.title("Search the Library")
    st.caption("Type a **name**, or paste a hard ID (NPI / CCN / UEI / CIK / IMO). "
               "Searches the 9.8M-entity backbone **and** the source catalog.")
    c1, c2 = st.columns([4, 1])
    term = c1.text_input("Search", value=st.query_params.get("q", ""),
                         placeholder="e.g.  memorial hospital   ·   1164450573   ·   cms open payments",
                         label_visibility="collapsed")
    kind = c2.selectbox("as", ["Name", "NPI", "CCN", "UEI", "CIK", "IMO"],
                        label_visibility="collapsed")
    if not term.strip():
        st.info("Enter a search above. Example entities: `alexander frank`, NPI `1164450573`.")
        return

    left, right = st.columns(2)

    # ---- entities --------------------------------------------------------
    with left:
        st.subheader("Entities")
        if kind in q.SEARCH_KEYS:
            df = q.resolve_hard_id(kind, term.strip())
            if df.empty:
                st.warning(f"No entity carries {kind} = `{term.strip()}` "
                           "(normalized). Try Name search, or check the digits.")
            else:
                if len(df) == 1:
                    r = df.iloc[0]
                    st.success(f"Exact match on {kind}.")
                    if st.button(f"Open dossier → **{r['KEY_VALUE']}** "
                                 f"({_int(r['SOURCE_COUNT'])} sources)",
                                 key="hit", use_container_width=True):
                        goto(view="dossier", eid=r["ENTITY_ID"])
                else:
                    for _, r in df.iterrows():
                        if st.button(f"{r['KEY_VALUE']} · {r['ENTITY_TYPE']} · "
                                     f"{_int(r['SOURCE_COUNT'])} sources",
                                     key=f"h{r['ENTITY_ID']}", use_container_width=True):
                            goto(view="dossier", eid=r["ENTITY_ID"])
        else:
            df = q.search_names(term.strip())
            if df.empty:
                st.warning("No entity name matches every word you typed.")
            else:
                st.caption(f"{len(df)} candidate(s) — multi-source entities first.")
                for _, r in df.iterrows():
                    sc = _int(r["SOURCE_COUNT"])
                    label = (f"**{r['CANONICAL_NAME']}** · {r['ENTITY_TYPE']} · "
                             f"{r['KEY_TYPE']}={r['KEY_VALUE']} · {sc} sources")
                    if st.button(label, key=f"n{r['ENTITY_ID']}", use_container_width=True):
                        goto(view="dossier", eid=r["ENTITY_ID"])

    # ---- sources ---------------------------------------------------------
    with right:
        st.subheader("Sources / datasets")
        sdf = q.search_sources(term.strip())
        if sdf.empty:
            st.caption("No landed/modeled source matches.")
        else:
            dec = q.decorations_for(tuple(sdf["SOURCE_ID"].tolist()))
            for _, r in sdf.iterrows():
                with st.container(border=True):
                    _rc = _int(r["LANDED_ROW_COUNT"], None)
                    rc = f"{_rc:,} rows" if _rc is not None else ""
                    st.markdown(f"**{r['NAME']}**  \n`{r['SOURCE_ID']}` · "
                                f"{r['DOMAIN_PRIMARY']} · {rc}")
                    render_decorated_source(r["SOURCE_ID"], dec)
                    if st.button("Open source", key=f"s{r['SOURCE_ID']}"):
                        goto(view="source", src=r["SOURCE_ID"])


# --------------------------------------------------------------------------- #
# DOSSIER
# --------------------------------------------------------------------------- #
def render_dossier(eid: str):
    golden, emap, sources = q.get_dossier(eid)
    if golden.empty:
        st.error(f"No entity `{eid}` in the spine.")
        if st.button("← Back to search"):
            goto(view="search")
        return
    g = golden.iloc[0]
    m = emap.iloc[0].to_dict() if not emap.empty else {}
    member_tables = q.safe_json(m.get("MEMBER_TABLES")) or []
    src_count = _int(m.get("SOURCE_COUNT")) or len(sources)

    if st.button("← Back to search", key="back_dossier"):
        goto(view="search")
    st.title(g.get("CANONICAL_NAME") or "(no name)")
    meta = f"**{g.get('ENTITY_TYPE','?')}** · {g.get('KEY_TYPE')}=`{g.get('KEY_VALUE')}` · `{eid}`"
    if g.get("CANONICAL_ADDR"):
        meta += f" · {g.get('CANONICAL_ADDR')}"
    st.markdown(meta)

    a, b, c = st.columns(3)
    a.metric("Appears across", f"{src_count} sources")
    b.metric("Cross-domain rows", f"{len(sources)}")
    c.metric("Identity built", _ts(g.get("BUILT_AT")))

    if member_tables:
        if st.button(f"🕸  Jump into the connection graph "
                     f"({len(member_tables)} source nodes)", type="primary"):
            goto(view="graph", focus=",".join(member_tables))

    # ---- every thread, with freshness + receipt inline -------------------
    st.subheader("Every thread")
    st.caption("Each row is one source this entity appears in — cross-domain. "
               "Freshness + the run-it-yourself receipt are attached to each.")
    src_ids = [str(s).lower() for s in sources["SOURCE_TABLE"].tolist()]
    dec = q.decorations_for(tuple(src_ids))

    last_dom = None
    for _, s in sources.iterrows():
        dom = s["DOMAIN"] or "—"
        if dom != last_dom:
            st.markdown(f"##### {dom}")
            last_dom = dom
        with st.container(border=True):
            head = f"**{s['SOURCE_TABLE']}**"
            if _int(s["ROW_COUNT"]) > 1:
                head += f"  ·  {_int(s['ROW_COUNT'])} rows"
            if s.get("DISPLAY_LABEL"):
                head += f"  ·  {s['DISPLAY_LABEL']}"
            st.markdown(head)
            pairs = q.preview_pairs(s.get("PREVIEW"))
            if pairs:
                st.caption(" · ".join(f"**{k}**: {v}" for k, v in pairs))
            d = dec.get(str(s["SOURCE_TABLE"]).lower(), {})
            cc1, cc2 = st.columns([3, 1])
            with cc1:
                st.caption(fresh_caption(d))
                st.caption(receipt_caption(d))
            with cc2:
                if st.button("Open source", key=f"d{s['SOURCE_TABLE']}"):
                    goto(view="source", src=str(s["SOURCE_TABLE"]).lower())

    # ---- affiliations (providers only) -----------------------------------
    if g.get("KEY_TYPE") == "NPI":
        st.subheader("Affiliated facilities")
        st.caption("A *works-at* relationship (provider → CMS facility), not identity — "
                   "each facility is its own entity. Source: FED_CMS_FACILITY_AFFILIATION.")
        try:
            aff = q.get_affiliations(g["KEY_VALUE"])
        except Exception as e:
            st.warning(f"Affiliations unavailable: {e}")
            aff = None
        if aff is not None and not aff.empty:
            for _, a_ in aff.iterrows():
                ccn = a_["CCN"]
                name = a_.get("CANONICAL_NAME") or "(unnamed facility)"
                addr = a_.get("CANONICAL_ADDR") or ""
                cols = st.columns([5, 1])
                cols[0].markdown(f"CCN `{ccn}` — **{name}**  \n{addr}")
                if cols[1].button("Dossier", key=f"aff{ccn}"):
                    goto(view="dossier", eid=q.entity_id_for("CCN", ccn))
        elif aff is not None:
            st.caption("No CMS facility affiliations on record for this provider.")


# --------------------------------------------------------------------------- #
# SOURCE
# --------------------------------------------------------------------------- #
def render_source(src: str):
    if st.button("← Back to search", key="back_source"):
        goto(view="search")
    df = q.get_source(src)
    if df.empty:
        st.error(f"Source `{src}` not in the catalog.")
        return
    r = df.iloc[0]
    st.title(r.get("NAME") or src)
    st.markdown(f"`{r['SOURCE_ID']}` · **{r.get('DOMAIN_PRIMARY')}** · "
                f"{r.get('JURISDICTION')} · {r.get('PUBLISHER') or ''}")
    cols = st.columns(4)
    cols[0].metric("Lifecycle", str(r.get("LIFECYCLE")))
    _lrc = _int(r.get("LANDED_ROW_COUNT"), None)
    cols[1].metric("Landed rows", f"{_lrc:,}" if _lrc is not None else "—")
    cols[2].metric("Key tier", str(r.get("JOIN_KEY_TIER") or "—"))
    cols[3].metric("Sample?", "yes" if r.get("IS_SAMPLE") else "no")
    keys = q.safe_json(r.get("JOIN_KEYS_STD")) or r.get("JOIN_KEYS_STD")
    if keys:
        st.caption(f"join keys: {', '.join(keys) if isinstance(keys, list) else keys}")
    if r.get("URL"):
        st.markdown(f"[publisher landing page ↗]({r['URL']})")

    st.subheader("Freshness & provenance")
    dec = q.decorations_for((r["SOURCE_ID"],))
    d = dec.get(str(r["SOURCE_ID"]).lower(), {})
    st.markdown(fresh_caption(d))
    st.markdown(receipt_caption(d))
    if d.get("run_id"):
        st.json({k: _ts(d.get(k)) if k == "loaded_at" else d.get(k)
                 for k in ("run_id", "sha256", "source_url", "loaded_at",
                           "run_rows", "file_bytes")}, expanded=False)

    st.subheader("Live sample (25 rows)")
    if str(r.get("LIFECYCLE")) not in ("landed", "modeled"):
        st.caption("Source isn't landed/modeled — no landing table to sample.")
        return
    try:
        samp = q.sample_rows(r["SOURCE_ID"])
        st.dataframe(samp, use_container_width=True, height=360)
    except Exception as e:
        st.warning(f"Couldn't sample the landing table: {e}")


# --------------------------------------------------------------------------- #
# GRAPH
# --------------------------------------------------------------------------- #
def render_graph():
    st.title("Connection graph")
    focus_raw = st.query_params.get("focus", "")
    focus = [t for t in focus_raw.split(",") if t] if focus_raw else None

    try:
        graph, asof = G.load_graph()
    except Exception as e:
        st.error(f"Couldn't load connect_graph.json: {e}")
        return
    try:
        enrich = q.catalog_enrichment()
    except Exception:
        enrich = {}

    top = st.columns([3, 2, 2])
    tiers = top[0].multiselect("Edge tiers", G.ALL_TIERS, default=G.DEFAULT_TIERS,
                               help="STEEL/STRONG/BRIDGE are the hard-ID spine. GEO/"
                                    "PROBABILISTIC are weaker — off by default.")
    include_samples = top[1].toggle("Include portal samples", value=bool(focus),
                                    help="655/764 nodes are open-data-portal samples; "
                                         "hidden by default so the core library shows.")
    if focus:
        if top[2].button("✕ Clear focus / show full graph"):
            goto(view="graph")
        st.caption(f"Showing the connection neighborhood of {len(focus)} source(s) "
                   "this entity appears in.")

    fig = G.build_figure(graph, tiers=tiers, include_samples=include_samples,
                         focus=focus, enrich=enrich, asof=asof)

    # Node click -> open that source (nodes are SOURCE tables).
    selected = None
    try:
        ev = st.plotly_chart(fig, use_container_width=True, on_select="rerun",
                             selection_mode="points", key="graph")
        pts = (ev or {}).get("selection", {}).get("points", [])
        if pts:
            selected = pts[0].get("customdata")
            if isinstance(selected, list):
                selected = selected[0]
    except TypeError:
        # Older Streamlit without on_select — render static.
        st.plotly_chart(fig, use_container_width=True)

    st.caption(f"Cached layout as of **{asof}** · {graph['meta']['edges']:,} measured "
               f"edges across {len(graph['nodes'])} source nodes · drag to pan, scroll to zoom. "
               "Snapshot — rerun `connect discover` + `cache_layout` to refresh.")

    # Reliable navigation fallback (works on any Streamlit version).
    nav = st.columns([3, 1])
    pick = nav[0].selectbox("Open a source from the graph",
                            options=[""] + sorted(n["id"] for n in graph["nodes"]),
                            index=0)
    target = selected or (pick or None)
    if target and nav[1].button("Open source", type="primary"):
        goto(view="source", src=target.lower())
    elif selected:
        st.info(f"Selected **{selected}** — click *Open source* to view it.")


# --------------------------------------------------------------------------- #
# Router
# --------------------------------------------------------------------------- #
def main():
    sidebar()
    view = st.query_params.get("view", "search")
    if view == "dossier" and st.query_params.get("eid"):
        render_dossier(st.query_params["eid"])
    elif view == "source" and st.query_params.get("src"):
        render_source(st.query_params["src"])
    elif view == "graph":
        render_graph()
    else:
        render_search()


main()
