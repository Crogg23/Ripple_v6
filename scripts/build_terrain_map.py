"""Build the connection terrain map from CONNECT_EDGES.

Runs AFTER `python -m connect discover` (or `connect all`) completes. Produces:
  outputs/terrain_map.html — interactive D3 force-directed visualization

    python3 scripts/build_terrain_map.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "connect"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402

OUTPUTS = _REPO / "outputs"

# ---------------------------------------------------------------------------
# Human-readable domain names (Vsauce-style: curiosity, not jargon)
# ---------------------------------------------------------------------------
DOMAIN_LABELS = {
    "health_medicine": "Healthcare",
    "money_in_politics": "Money in Politics",
    "money_finance": "Money & Finance",
    "economy_labor_trade": "Economy & Labor",
    "justice_courts": "Courts & Justice",
    "crime_security": "Crime & Security",
    "transport_movement": "Planes, Trains & Ships",
    "energy_environment": "Energy & Environment",
    "education": "Education",
    "housing_social": "Housing & Social Services",
    "spending_budget": "Government Spending",
    "corporate_entities": "Who Owns What",
    "immigration_migration": "Immigration",
    "government_power": "Government & Power",
    "sanctions_enforcement": "Who's Banned",
    "elections_voting": "Elections & Voting",
    "science_research": "Science & Research",
    "history_culture": "History & Culture",
}

# ---------------------------------------------------------------------------
# "So What?" templates — what each connection type ENABLES you to ask
# ---------------------------------------------------------------------------
SO_WHAT_BY_PAIR = {
    # Key: frozenset of two source_ids -> custom "so what" text
    frozenset({"FCC_LICENSING", "FEC_INDIV_CONTRIBUTIONS"}):
        "Trace whether telecom and broadcast license holders donate to the lawmakers who regulate them.",
    frozenset({"FCC_LICENSING", "FEC_BULK_DATA_INDIV_CONTRIBUTIONS"}):
        "Trace whether telecom and broadcast license holders donate to the lawmakers who regulate them.",
    frozenset({"EPA_ECHO", "IRS_BMF"}):
        "Find nonprofits claiming tax-exempt status while racking up EPA violations.",
    frozenset({"EPA_ECHO", "USASPENDING_CONTRACTS"}):
        "Find companies getting government contracts while under environmental enforcement action.",
    frozenset({"EPA_ECHO", "USASPENDING_CONTRACTS_FULL"}):
        "Find companies getting government contracts while under environmental enforcement action.",
    frozenset({"SEC_EDGAR_COMPANY_TICKERS", "SEC_EDGAR_FINANCIALS"}):
        "Connect a company's identity to its full financial filings — revenue, debt, everything.",
    frozenset({"SEC_EDGAR_COMPANY_TICKERS", "SEC_EDGAR_INSIDERS"}):
        "See exactly who sold stock before bad earnings. Every insider trade linked to the company.",
    frozenset({"FAA_REGISTRY", "FCC_LICENSING"}):
        "People or companies with both aircraft and radio/telecom licenses. Aviation + telecommunications overlap.",
    frozenset({"CMS_NPPES", "CMS_OPEN_PAYMENTS"}):
        "See exactly how much money each doctor received from drug companies. Every payment, every doctor.",
    frozenset({"CMS_NPPES", "CMS_PARTD_PRESCRIBER_DRUG"}):
        "What drugs does each doctor prescribe, and at what volume? Connect prescribing patterns to provider identity.",
    frozenset({"FEC_INDIV_CONTRIBUTIONS", "VERA_INCARCERATION_TRENDS"}):
        "Overlay campaign donations with incarceration data — who funds criminal justice policy at the county level?",
    frozenset({"FEC_BULK_DATA_INDIV_CONTRIBUTIONS", "VERA_INCARCERATION_TRENDS"}):
        "Overlay campaign donations with incarceration data — who funds criminal justice policy at the county level?",
}


def _so_what(a: str, b: str, key: str, tier: str) -> str:
    """Generate a 'so what?' line: what this connection ENABLES you to do."""
    # Strip prefix for lookup
    a_short = a.replace("FED_", "").replace("XC_", "").replace("INTL_", "")
    b_short = b.replace("FED_", "").replace("XC_", "").replace("INTL_", "")
    pair = frozenset({a_short, b_short})
    if pair in SO_WHAT_BY_PAIR:
        return SO_WHAT_BY_PAIR[pair]

    # Generic "so what" based on tier/key
    if tier == "STEEL":
        return f"Hard-ID link. You can JOIN these datasets right now and get exact entity-level answers."
    elif tier == "CORROBORATED" and "NAME" in key:
        return "Same name at the same location in both datasets — strong enough for investigative leads, not proof."
    elif tier == "GEO":
        return "Geographic overlap — useful for regional analysis and county-level comparisons."
    return "A proven connection path between these two worlds of data."


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------

def _fetch_domain_edges(cur) -> list[dict]:
    """Cross-domain edges aggregated to domain level."""
    cur.execute("""
        SELECT
            COALESCE(ra.DOMAIN_PRIMARY, 'unknown') AS domain_a,
            COALESCE(rb.DOMAIN_PRIMARY, 'unknown') AS domain_b,
            COUNT(*) AS edge_count,
            SUM(e.MATCHED) AS total_shared
        FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY ra ON UPPER(ra.SOURCE_ID) = e.A
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY rb ON UPPER(rb.SOURCE_ID) = e.B
        WHERE e.A NOT LIKE 'PORTAL_%' AND e.B NOT LIKE 'PORTAL_%'
          AND COALESCE(ra.DOMAIN_PRIMARY, 'x') != COALESCE(rb.DOMAIN_PRIMARY, 'y')
          AND NOT (e.KEY = 'ZIP' AND e.TIER = 'GEO')
          AND e.CONFIDENCE >= 0.3
        GROUP BY 1, 2
        HAVING SUM(e.MATCHED) >= 50
        ORDER BY total_shared DESC
    """)
    return [{"s": r[0], "t": r[1], "n": r[2], "w": r[3]} for r in cur.fetchall()]


def _fetch_domain_nodes(cur) -> list[dict]:
    """Node weights from cross-domain connection weight."""
    cur.execute("""
        WITH edges AS (
            SELECT e.A, e.B, e.MATCHED,
                COALESCE(ra.DOMAIN_PRIMARY, 'unknown') AS da,
                COALESCE(rb.DOMAIN_PRIMARY, 'unknown') AS db
            FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
            LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY ra ON UPPER(ra.SOURCE_ID) = e.A
            LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY rb ON UPPER(rb.SOURCE_ID) = e.B
            WHERE e.A NOT LIKE 'PORTAL_%' AND e.B NOT LIKE 'PORTAL_%'
              AND COALESCE(ra.DOMAIN_PRIMARY, 'x') != COALESCE(rb.DOMAIN_PRIMARY, 'y')
              AND NOT (e.KEY = 'ZIP' AND e.TIER = 'GEO')
              AND e.CONFIDENCE >= 0.3
        )
        SELECT domain, SUM(w) AS weight FROM (
            SELECT da AS domain, SUM(MATCHED) AS w FROM edges GROUP BY da
            UNION ALL
            SELECT db AS domain, SUM(MATCHED) AS w FROM edges GROUP BY db
        ) GROUP BY domain ORDER BY weight DESC
    """)
    return [{"id": r[0], "w": r[1]} for r in cur.fetchall()]


def _fetch_top_source_edges(cur, limit: int = 15) -> list[dict]:
    """Top cross-domain source pairs with human-readable context."""
    cur.execute(f"""
        SELECT e.A, e.B, e.KEY, e.TIER, e.MATCHED, e.CONFIDENCE,
            COALESCE(ra.DOMAIN_PRIMARY, 'unknown') AS domain_a,
            COALESCE(rb.DOMAIN_PRIMARY, 'unknown') AS domain_b,
            COALESCE(ra.NAME, e.A) AS name_a,
            COALESCE(rb.NAME, e.B) AS name_b
        FROM LIBRARY_META."CONNECT".CONNECT_EDGES e
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY ra ON UPPER(ra.SOURCE_ID) = e.A
        LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY rb ON UPPER(rb.SOURCE_ID) = e.B
        WHERE e.A NOT LIKE 'PORTAL_%' AND e.B NOT LIKE 'PORTAL_%'
          AND COALESCE(ra.DOMAIN_PRIMARY, 'x') != COALESCE(rb.DOMAIN_PRIMARY, 'y')
          AND NOT (e.KEY = 'ZIP' AND e.TIER = 'GEO')
          AND e.CONFIDENCE >= 0.3
        ORDER BY e.MATCHED DESC
        LIMIT {limit}
    """)
    results = []
    for r in cur.fetchall():
        a, b, key, tier, matched, conf, da, db, name_a, name_b = r
        friendly = _friendly_name(a, b, name_a, name_b)
        explain = _explain_text(a, b, key, tier, matched, name_a, name_b, da, db)
        so_what = _so_what(a, b, key, tier)
        results.append({
            "a": a, "b": b, "key": key, "tier": tier, "matched": matched,
            "friendly": friendly, "explain": explain, "so_what": so_what,
        })
    return results


def _fetch_coverage(cur) -> dict:
    """Stats on what's connected vs. what's still dark."""
    cur.execute("""
        WITH all_tables AS (
            SELECT TABLE_NAME, ROW_COUNT
            FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
            WHERE TABLE_SCHEMA = 'LANDING' AND TABLE_NAME NOT LIKE 'PORTAL_%'
        ),
        connected AS (
            SELECT DISTINCT src FROM (
                SELECT A AS src FROM LIBRARY_META."CONNECT".CONNECT_EDGES
                UNION SELECT B AS src FROM LIBRARY_META."CONNECT".CONNECT_EDGES
            )
        )
        SELECT
            COUNT(*) AS total_tables,
            SUM(ROW_COUNT) AS total_rows,
            SUM(CASE WHEN c.src IS NOT NULL THEN 1 ELSE 0 END) AS connected_tables,
            SUM(CASE WHEN c.src IS NOT NULL THEN ROW_COUNT ELSE 0 END) AS connected_rows,
            SUM(CASE WHEN c.src IS NULL THEN 1 ELSE 0 END) AS dark_tables,
            SUM(CASE WHEN c.src IS NULL THEN ROW_COUNT ELSE 0 END) AS dark_rows
        FROM all_tables a
        LEFT JOIN connected c ON c.src = a.TABLE_NAME
    """)
    r = cur.fetchone()
    # Top dark tables
    cur.execute("""
        WITH connected AS (
            SELECT DISTINCT src FROM (
                SELECT A AS src FROM LIBRARY_META."CONNECT".CONNECT_EDGES
                UNION SELECT B AS src FROM LIBRARY_META."CONNECT".CONNECT_EDGES
            )
        )
        SELECT t.TABLE_NAME, t.ROW_COUNT
        FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES t
        LEFT JOIN connected c ON c.src = t.TABLE_NAME
        WHERE t.TABLE_SCHEMA = 'LANDING'
          AND t.TABLE_NAME NOT LIKE 'PORTAL_%'
          AND c.src IS NULL
        ORDER BY t.ROW_COUNT DESC
        LIMIT 5
    """)
    dark_tables = [{"name": row[0], "rows": row[1]} for row in cur.fetchall()]

    return {
        "total_tables": r[0], "total_rows": r[1],
        "connected_tables": r[2], "connected_rows": r[3],
        "dark_tables": r[4], "dark_rows": r[5],
        "top_dark": dark_tables,
    }


def _fetch_bridges(cur) -> list[dict]:
    """Bridge entities from ENTITY_INDEX (only works if spine has been built)."""
    try:
        cur.execute("SELECT COUNT(*) FROM LIBRARY_META.\"CONNECT\".ENTITY_INDEX")
        count = cur.fetchone()[0]
        if count == 0:
            return []
    except Exception:
        return []

    cur.execute("""
        SELECT
            ei.ENTITY_ID,
            ei.ENTITY_TYPE,
            MAX(ei.DISPLAY_LABEL) AS display_label,
            COUNT(DISTINCT r.DOMAIN_PRIMARY) AS domain_count,
            COUNT(DISTINCT ei.SOURCE_TABLE) AS source_count,
            ARRAY_TO_STRING(ARRAY_AGG(DISTINCT r.DOMAIN_PRIMARY), ', ') AS domains_str
        FROM LIBRARY_META."CONNECT".ENTITY_INDEX ei
        JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY r
          ON UPPER(r.SOURCE_ID) = ei.SOURCE_TABLE
        WHERE r.DOMAIN_PRIMARY IS NOT NULL
        GROUP BY 1, 2
        HAVING COUNT(DISTINCT r.DOMAIN_PRIMARY) >= 3
        ORDER BY domain_count DESC, source_count DESC
        LIMIT 30
    """)
    return [{"id": r[0], "type": r[1], "label": r[2], "domains": r[3],
             "sources": r[4], "domain_list": r[5]} for r in cur.fetchall()]


# ---------------------------------------------------------------------------
# Text generators — Vsauce style: lead with surprise, explain second
# ---------------------------------------------------------------------------

def _short_name(source_id: str) -> str:
    """Strip FED_/XC_/INTL_ prefix and format for display."""
    for prefix in ("FED_", "XC_", "INTL_"):
        if source_id.startswith(prefix):
            source_id = source_id[len(prefix):]
            break
    return source_id.replace("_", " ").title()


def _friendly_name(a: str, b: str, name_a: str, name_b: str) -> str:
    """Generate a human-readable connection title."""
    sa = name_a[:45] if name_a and name_a != a else _short_name(a)
    sb = name_b[:45] if name_b and name_b != b else _short_name(b)
    return f"{sa} \u2194 {sb}"


def _explain_text(a: str, b: str, key: str, tier: str, matched: int,
                  name_a: str, name_b: str, domain_a: str, domain_b: str) -> str:
    """Plain-English explanation. Lead with the human insight, not the mechanism."""
    m = f"{matched:,}"
    na = _short_name(a)
    nb = _short_name(b)
    da = DOMAIN_LABELS.get(domain_a, domain_a)
    db = DOMAIN_LABELS.get(domain_b, domain_b)

    if tier == "STEEL":
        return (f"{m} entities appear in both datasets with the exact same ID number. "
                f"Not a guess — a proven, deterministic match. "
                f"The same real-world entity, verified across {da} and {db}.")
    elif tier == "CORROBORATED" and "NAME" in key and "ZIP" in key:
        return (f"{m} entities share the same name AND the same ZIP code in both datasets. "
                f"That's not a coincidence at scale — it's the same organizations showing up "
                f"in {da} records and {db} records simultaneously.")
    elif tier == "CORROBORATED" and "FIPS" in key:
        return (f"{m} entities corroborated by name at the county level. "
                f"Same name, same county — connecting {da} with {db}.")
    elif tier == "GEO" and "FIPS" in key:
        return (f"{m} counties appear in both datasets. Not entity-matching — this tells "
                f"you where {da} and {db} data geographically overlaps for regional analysis.")
    elif tier == "GEO":
        return (f"{m} geographic areas shared between datasets. Enables regional "
                f"cross-analysis between {da} and {db}.")
    else:
        return (f"{m} matches connecting {da} with {db}. "
                f"Linked via {key} — a pathway between two worlds of data.")


# ---------------------------------------------------------------------------
# HTML Rendering
# ---------------------------------------------------------------------------

def render_terrain_map(cur) -> str:
    """Build the terrain map HTML from CONNECT_EDGES data."""
    print("Fetching cross-domain edges...")
    domain_edges = _fetch_domain_edges(cur)
    print(f"  -> {len(domain_edges)} domain corridors")

    print("Computing node weights...")
    domain_nodes = _fetch_domain_nodes(cur)
    print(f"  -> {len(domain_nodes)} domains with connections")

    print("Fetching top source-level edges...")
    source_edges = _fetch_top_source_edges(cur, limit=15)
    print(f"  -> {len(source_edges)} strongest source pairs")

    print("Fetching coverage stats...")
    coverage = _fetch_coverage(cur)
    print(f"  -> {coverage['connected_tables']}/{coverage['total_tables']} tables connected, "
          f"{coverage['dark_tables']} still dark")

    print("Checking for bridge entities...")
    bridges = _fetch_bridges(cur)
    print(f"  -> {len(bridges)} bridge entities")

    html = _build_html(domain_nodes, domain_edges, source_edges, bridges, coverage)
    out_path = OUTPUTS / "terrain_map.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  -> {out_path}")
    return str(out_path)


def _build_html(domain_nodes, domain_edges, source_edges, bridges, coverage) -> str:
    """Render the self-contained HTML terrain map — Vsauce style."""
    dn_json = json.dumps(domain_nodes)
    de_json = json.dumps(domain_edges)
    se_json = json.dumps(source_edges, ensure_ascii=False)
    br_json = json.dumps(bridges)
    cov_json = json.dumps(coverage)
    domain_labels_json = json.dumps(DOMAIN_LABELS)

    n_domains = len(domain_nodes)
    n_corridors = len(domain_edges)
    n_sources = len(source_edges)

    total_rows = coverage["total_rows"]
    connected_pct = round(100 * coverage["connected_rows"] / total_rows) if total_rows else 0
    dark_pct = 100 - connected_pct

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="snowflake-source" content="cortex-agent-authored">
<title>Ripple Connection Terrain Map</title>
<script type="application/json" id="snowflake-report-metadata">
{{
  "generated": "{__import__('datetime').date.today().isoformat()}",
  "intent": "Cross-domain entity connection topology for Ripple data warehouse",
  "dataSources": [
    {{"type": "query", "warehouse": "RIPPLE_WH", "sql": "SELECT ... FROM LIBRARY_META.CONNECT.CONNECT_EDGES ... WHERE cross-domain, confidence >= 0.3"}}
  ]
}}
</script>
<style>
:root {{ color-scheme: light dark; }}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: light-dark(#f8f9fa, #0a0a0f); color: light-dark(#1f2937, #e0e0e0); }}
#header {{ padding: 24px 30px 16px; border-bottom: 1px solid light-dark(#ddd, #222); }}
#header h1 {{ font-size: 26px; font-weight: 600; margin-bottom: 8px; }}
#header .narrative {{ font-size: 14px; color: light-dark(#4b5563, #aaa); line-height: 1.5; max-width: 900px; }}
#header .narrative strong {{ color: light-dark(#1f2937, #e0e0e0); }}
#controls {{ padding: 10px 30px; display: flex; gap: 15px; align-items: center; border-bottom: 1px solid light-dark(#e5e7eb, #1a1a1a); }}
#controls button {{ padding: 6px 14px; border: 1px solid light-dark(#ccc, #333); background: light-dark(#fff, #1a1a2a); color: light-dark(#333, #ccc); border-radius: 4px; cursor: pointer; font-size: 12px; }}
#controls button.active {{ background: light-dark(#e0e7ff, #2a2a4a); border-color: light-dark(#6366f1, #556); color: light-dark(#1e1b4b, #fff); }}
#main {{ display: flex; height: calc(100vh - 160px); }}
#graph {{ flex: 1; }}
#panel {{ width: 420px; border-left: 1px solid light-dark(#ddd, #222); overflow-y: auto; padding: 20px; }}
#panel h2 {{ font-size: 13px; margin-bottom: 12px; color: light-dark(#666, #aaa); text-transform: uppercase; letter-spacing: 1px; }}
.edge-card {{ padding: 12px 14px; margin-bottom: 10px; background: light-dark(#fff, #111); border-radius: 6px; border-left: 4px solid #4a6; }}
.edge-card .friendly {{ font-size: 13px; font-weight: 600; color: light-dark(#1e293b, #e2e8f0); }}
.edge-card .explain {{ font-size: 12px; color: light-dark(#4b5563, #9ca3af); margin-top: 6px; line-height: 1.5; }}
.edge-card .so-what {{ font-size: 11px; color: light-dark(#7c3aed, #a78bfa); margin-top: 6px; font-style: italic; }}
.edge-card .badge {{ display: inline-block; font-size: 10px; padding: 2px 6px; border-radius: 3px; margin-top: 6px; }}
.badge-steel {{ background: light-dark(#dbeafe, #1e3a5f); color: light-dark(#1e40af, #93c5fd); }}
.badge-corroborated {{ background: light-dark(#dcfce7, #14532d); color: light-dark(#166534, #86efac); }}
.badge-geo {{ background: light-dark(#fef3c7, #451a03); color: light-dark(#92400e, #fcd34d); }}
.tier-steel {{ border-left-color: #3b82f6; }}
.tier-corroborated {{ border-left-color: #22c55e; }}
.tier-geo {{ border-left-color: #f59e0b; }}
.coverage-box {{ background: light-dark(#f3f4f6, #111); border-radius: 8px; padding: 14px; margin-bottom: 16px; border: 1px solid light-dark(#e5e7eb, #222); }}
.coverage-box h3 {{ font-size: 12px; color: light-dark(#6b7280, #888); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
.coverage-bar {{ height: 8px; border-radius: 4px; background: light-dark(#e5e7eb, #222); overflow: hidden; margin: 8px 0; }}
.coverage-bar .fill {{ height: 100%; border-radius: 4px; background: linear-gradient(90deg, #3b82f6, #22c55e); }}
.coverage-stat {{ font-size: 12px; color: light-dark(#4b5563, #9ca3af); line-height: 1.6; }}
.coverage-stat strong {{ color: light-dark(#1f2937, #e0e0e0); }}
.dark-table {{ font-size: 11px; color: light-dark(#6b7280, #777); padding: 3px 0; }}
.dark-table .rows {{ color: light-dark(#9ca3af, #555); }}
.bridge-card {{ padding: 8px 12px; margin-bottom: 6px; background: light-dark(#fff, #111); border-radius: 4px; border-left: 3px solid #a78bfa; }}
.bridge-card .label {{ font-size: 13px; font-weight: 500; }}
.bridge-card .meta {{ font-size: 11px; color: light-dark(#6b7280, #888); margin-top: 2px; }}
svg text {{ fill: light-dark(#374151, #ccc); font-size: 10px; }}
.link {{ stroke-opacity: 0.5; stroke: light-dark(#9ca3af, #444); }}
.source-link {{ stroke-opacity: 0.4; stroke: light-dark(#9ca3af, #555); }}
.node circle {{ stroke: light-dark(#e5e7eb, #333); stroke-width: 1px; }}
.node text {{ font-size: 9px; fill: light-dark(#6b7280, #aaa); }}
#stats {{ padding: 10px 30px; font-size: 12px; color: light-dark(#9ca3af, #666); position: fixed; bottom: 0; left: 0; right: 0; background: light-dark(#f8f9fa, #0a0a0f); border-top: 1px solid light-dark(#e5e7eb, #1a1a1a); }}
</style>
</head>
<body>
<div id="header">
  <h1>Where Does Your Data Secretly Connect?</h1>
  <p class="narrative">
    You have <strong>{total_rows:,} rows</strong> of public data across <strong>{coverage['total_tables']} datasets</strong>.
    This map shows where those datasets share the same real-world entities &mdash; the same people, companies, and places
    appearing in records that were never designed to talk to each other.
    Each line is a proven pathway: a question you can ask that spans two different worlds.
    Right now, <strong>{connected_pct}% of your data</strong> is illuminated. The rest is still in the dark.
  </p>
</div>
<div id="controls">
  <button class="active" id="btn-domain">By Topic</button>
  <button id="btn-source">By Dataset</button>
  <span style="color:light-dark(#d1d5db,#333); font-size:11px; margin: 0 4px;">|</span>
  <span style="font-size:12px; color:light-dark(#6b7280,#888);">{n_corridors} cross-topic pathways found</span>
</div>
<div id="main">
  <div id="graph"></div>
  <div id="panel">
    <div class="coverage-box">
      <h3>What You're Seeing (and What You're Not)</h3>
      <div class="coverage-bar"><div class="fill" style="width:{connected_pct}%"></div></div>
      <div class="coverage-stat">
        <strong>{connected_pct}% illuminated</strong> &mdash; {coverage['connected_tables']} datasets connected via hard IDs<br>
        <strong>{dark_pct}% in the dark</strong> &mdash; {coverage['dark_tables']} datasets can't link yet (only have names/addresses, no shared ID numbers)
      </div>
      <div style="margin-top:8px; font-size:11px; color:light-dark(#9ca3af,#555);">
        Biggest unconnected datasets:
      </div>
      <div id="dark-tables"></div>
    </div>

    <h2>Strongest Connections Found</h2>
    <div id="edges-list"></div>

    <h2 style="margin-top:20px;">Bridge Entities (appear in 3+ topics)</h2>
    <div id="bridges-list"></div>
  </div>
</div>
<div id="stats"></div>

<script src="/libs/d3@7.9.0/d3.min.js"></script>
<script>
if (typeof d3 === 'undefined') {{
  var s = document.createElement('script');
  s.src = 'https://d3js.org/d3.v7.min.js';
  s.onload = function() {{ init(); }};
  document.head.appendChild(s);
}} else {{ init(); }}

function init() {{

var domainNodes = {dn_json};
var domainEdges = {de_json};
var topSourceEdges = {se_json};
var bridges = {br_json};
var coverage = {cov_json};
var domainLabels = {domain_labels_json};

var domainColors = {{
  'health_medicine': '#4ecdc4', 'money_in_politics': '#ff6b6b',
  'money_finance': '#ffd93d', 'economy_labor_trade': '#6bcb77',
  'justice_courts': '#c084fc', 'crime_security': '#f97316',
  'transport_movement': '#38bdf8', 'energy_environment': '#22c55e',
  'education': '#a78bfa', 'housing_social': '#fb923c',
  'spending_budget': '#f472b6', 'corporate_entities': '#fbbf24',
  'immigration_migration': '#2dd4bf', 'government_power': '#818cf8',
  'sanctions_enforcement': '#ef4444', 'elections_voting': '#67e8f9',
  'science_research': '#86efac', 'history_culture': '#d4a574',
}};
function getColor(d) {{ return domainColors[d] || '#666'; }}
function getLabel(d) {{ return domainLabels[d] || d.replace(/_/g, ' '); }}

// Coverage: dark tables
var darkDiv = document.getElementById('dark-tables');
coverage.top_dark.forEach(function(t) {{
  darkDiv.innerHTML += '<div class="dark-table">' + t.name.replace(/^FED_/, '').replace(/_/g, ' ') +
    ' <span class="rows">(' + t.rows.toLocaleString() + ' rows)</span></div>';
}});

// Sidebar: edge cards
var edgesList = document.getElementById('edges-list');
topSourceEdges.forEach(function(e) {{
  var tierClass = 'tier-' + e.tier.toLowerCase();
  var badgeClass = 'badge-' + e.tier.toLowerCase();
  var tierLabel = e.tier === 'STEEL' ? 'Exact ID Match' : e.tier === 'CORROBORATED' ? 'Name + Location' : 'Geographic';
  edgesList.innerHTML += '<div class="edge-card ' + tierClass + '">' +
    '<div class="friendly">' + e.friendly + '</div>' +
    '<div class="explain">' + e.explain + '</div>' +
    '<div class="so-what">' + e.so_what + '</div>' +
    '<span class="badge ' + badgeClass + '">' + tierLabel + ' &mdash; ' + e.matched.toLocaleString() + ' shared</span>' +
    '</div>';
}});

// Sidebar: bridge entities
var bridgesList = document.getElementById('bridges-list');
if (bridges.length === 0) {{
  bridgesList.innerHTML = '<p style="font-size:12px;color:light-dark(#9ca3af,#666);line-height:1.5;">No bridge entities detected yet. These appear when the entity spine finds a single person, company, or place showing up across 3+ completely different topic areas.</p>';
}} else {{
  bridges.forEach(function(b) {{
    bridgesList.innerHTML += '<div class="bridge-card">' +
      '<div class="label">' + (b.label || b.id) + '</div>' +
      '<div class="meta">' + b.type + ' &mdash; appears in ' + b.domains + ' different topics across ' + b.sources + ' datasets</div>' +
      '<div class="meta" style="opacity:0.7">' + b.domain_list + '</div></div>';
  }});
}}

var graphEl = document.getElementById('graph');
var width = graphEl.clientWidth;
var height = graphEl.clientHeight;
var svg = d3.select('#graph').append('svg').attr('width', width).attr('height', height);
var simulation;

function showDomains() {{
  document.getElementById('btn-domain').classList.add('active');
  document.getElementById('btn-source').classList.remove('active');
  svg.selectAll('*').remove();

  var nodes = domainNodes.filter(function(n) {{ return n.w > 0; }}).map(function(d) {{ return Object.assign({{}}, d); }});
  var maxW = Math.max.apply(null, domainEdges.map(function(e) {{ return e.w; }}));
  var edges = domainEdges.map(function(e) {{
    return {{ source: e.s, target: e.t, weight: e.w, width: Math.max(1.5, (e.w / maxW) * 14) }};
  }});

  var connected = new Set();
  edges.forEach(function(e) {{ connected.add(e.source); connected.add(e.target); }});
  var filteredNodes = nodes.filter(function(n) {{ return connected.has(n.id); }});

  simulation = d3.forceSimulation(filteredNodes)
    .force('link', d3.forceLink(edges).id(function(d) {{ return d.id; }}).distance(140))
    .force('charge', d3.forceManyBody().strength(-500))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(50));

  var link = svg.append('g').selectAll('line')
    .data(edges).join('line')
    .attr('class', 'link')
    .attr('stroke-width', function(d) {{ return d.width; }});

  var maxNodeW = Math.max.apply(null, filteredNodes.map(function(n) {{ return n.w; }}));
  var node = svg.append('g').selectAll('g')
    .data(filteredNodes).join('g')
    .attr('class', 'node')
    .call(d3.drag()
      .on('start', function(e, d) {{ if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }})
      .on('drag', function(e, d) {{ d.fx = e.x; d.fy = e.y; }})
      .on('end', function(e, d) {{ if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }}));

  node.append('circle')
    .attr('r', function(d) {{ return 10 + Math.sqrt(d.w / maxNodeW) * 30; }})
    .attr('fill', function(d) {{ return getColor(d.id); }})
    .attr('opacity', 0.85);

  node.append('text')
    .attr('dx', function(d) {{ return 14 + Math.sqrt(d.w / maxNodeW) * 30; }})
    .attr('dy', 4)
    .text(function(d) {{ return getLabel(d.id); }});

  simulation.on('tick', function() {{
    link.attr('x1', function(d) {{ return d.source.x; }}).attr('y1', function(d) {{ return d.source.y; }})
        .attr('x2', function(d) {{ return d.target.x; }}).attr('y2', function(d) {{ return d.target.y; }});
    node.attr('transform', function(d) {{ return 'translate(' + d.x + ',' + d.y + ')'; }});
  }});

  document.getElementById('stats').textContent =
    'Topic view: ' + filteredNodes.length + ' topics connected by ' + edges.length + ' pathways. Thicker lines = more shared entities. Bigger circles = more total cross-topic connections.';
}}

function showSources() {{
  document.getElementById('btn-source').classList.add('active');
  document.getElementById('btn-domain').classList.remove('active');
  svg.selectAll('*').remove();

  var edges = topSourceEdges.map(function(e) {{
    return {{ source: e.a, target: e.b, weight: e.matched, width: Math.max(1, Math.log10(e.matched) * 2) }};
  }});

  var nodeSet = new Set();
  edges.forEach(function(e) {{ nodeSet.add(e.source); nodeSet.add(e.target); }});
  var nodes = Array.from(nodeSet).map(function(id) {{ return {{ id: id }}; }});

  simulation = d3.forceSimulation(nodes)
    .force('link', d3.forceLink(edges).id(function(d) {{ return d.id; }}).distance(80))
    .force('charge', d3.forceManyBody().strength(-200))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('collision', d3.forceCollide().radius(20));

  var link = svg.append('g').selectAll('line')
    .data(edges).join('line')
    .attr('class', 'link source-link')
    .attr('stroke-width', function(d) {{ return d.width; }});

  var node = svg.append('g').selectAll('g')
    .data(nodes).join('g')
    .attr('class', 'node')
    .call(d3.drag()
      .on('start', function(e, d) {{ if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; }})
      .on('drag', function(e, d) {{ d.fx = e.x; d.fy = e.y; }})
      .on('end', function(e, d) {{ if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; }}));

  node.append('circle').attr('r', 8).attr('fill', '#6b7280').attr('opacity', 0.9);
  node.append('text').attr('dx', 12).attr('dy', 4).style('font-size', '8px')
    .text(function(d) {{ return d.id.replace(/^FED_/, '').replace(/^XC_/, '').replace(/^INTL_/, '').replace(/_/g, ' '); }});

  simulation.on('tick', function() {{
    link.attr('x1', function(d) {{ return d.source.x; }}).attr('y1', function(d) {{ return d.source.y; }})
        .attr('x2', function(d) {{ return d.target.x; }}).attr('y2', function(d) {{ return d.target.y; }});
    node.attr('transform', function(d) {{ return 'translate(' + d.x + ',' + d.y + ')'; }});
  }});

  document.getElementById('stats').textContent =
    'Dataset view: ' + nodes.length + ' individual datasets, ' + edges.length + ' proven connections between them.';
}}

document.getElementById('btn-domain').addEventListener('click', showDomains);
document.getElementById('btn-source').addEventListener('click', showSources);
showDomains();

}} // end init
</script>
</body>
</html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    args = ap.parse_args()

    conn = snow.connect()
    try:
        cur = conn.cursor()
        render_terrain_map(cur)
        print("\nDone. Open outputs/terrain_map.html in a browser.")
        cur.close()
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
