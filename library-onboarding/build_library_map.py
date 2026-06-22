"""Build an interactive 'octopus map' of every LIBRARY_* database.

Queries INFORMATION_SCHEMA across all LIBRARY_* databases in the live Ripple
warehouse and renders a single self-contained HTML file (Plotly inlined, works
offline) with three linked views of the same hierarchy:

    LIBRARY (head)  ->  database  ->  schema  ->  table (column count)

    * Octopus   -- a radial node-link graph; click any node for a detail panel
    * Sunburst  -- click a wedge to drill in/out (native Plotly)
    * Treemap   -- nested rectangles, click to zoom

Run from the library-onboarding/ directory (needs config.py + snow.py):

    python build_library_map.py                  # -> ../outputs/library_map.html
    python build_library_map.py --out PATH.html  # custom destination

Re-runnable: as the Library grows, just run it again for a fresh map.
"""

from __future__ import annotations

import argparse
import json
import math
import os
from datetime import datetime

import snow

ROOT = "LIBRARY"

# --- colour helpers --------------------------------------------------------
PALETTE = ["#38bdf8", "#a78bfa", "#f472b6", "#fbbf24", "#34d399", "#fb7185", "#60a5fa", "#c084fc"]
KNOWN = {
    "LIBRARY_RAW": "#38bdf8",      # cyan   — raw landing
    "LIBRARY_STAGING": "#a78bfa",  # violet — dbt staging
    "LIBRARY_MARTS": "#f472b6",    # pink   — dbt marts
    "LIBRARY_META": "#fbbf24",     # amber  — catalog + logs
    "LIBRARY_TOOLS": "#94a3b8",    # slate  — MCP host (no data)
}


def db_color(db: str, i: int) -> str:
    return KNOWN.get(db, PALETTE[i % len(PALETTE)])


def _hex2rgb(h: str):
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))


def lighten(h: str, amt: float) -> str:
    r, g, b = _hex2rgb(h)
    r = int(r + (255 - r) * amt)
    g = int(g + (255 - g) * amt)
    b = int(b + (255 - b) * amt)
    return "#%02x%02x%02x" % (r, g, b)


def rgba(h: str, a: float) -> str:
    r, g, b = _hex2rgb(h)
    return f"rgba({r},{g},{b},{a})"


# --- formatting ------------------------------------------------------------
def fmt_int(n) -> str:
    return "—" if n is None else f"{int(n):,}"


def fmt_bytes(n) -> str:
    if n is None:
        return "—"
    n = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024 or unit == "TB":
            return (f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}")
        n /= 1024
    return f"{n:.1f} TB"


# --- data collection -------------------------------------------------------
def collect():
    """Return {db: {schema: {table: {type,rows,bytes,cols}}}} for LIBRARY_* dbs."""
    conn = snow.connect()
    cur = conn.cursor()
    try:
        cur.execute("show databases like 'LIBRARY_%'")
        dbs = sorted(r[1] for r in cur.fetchall())
        data: dict = {}
        for db in dbs:
            data[db] = {}
            cur.execute(
                f"""select table_schema, table_name, table_type, row_count, bytes
                    from {db}.information_schema.tables
                    where table_schema <> 'INFORMATION_SCHEMA'
                    order by table_schema, table_name"""
            )
            for sch, tbl, ttype, rows, byt in cur.fetchall():
                data[db].setdefault(sch, {})[tbl] = {
                    "type": ttype, "rows": rows, "bytes": byt, "cols": 0,
                }
            cur.execute(
                f"""select table_schema, table_name, count(*) c
                    from {db}.information_schema.columns
                    where table_schema <> 'INFORMATION_SCHEMA'
                    group by 1, 2"""
            )
            for sch, tbl, c in cur.fetchall():
                node = data[db].setdefault(sch, {}).setdefault(
                    tbl, {"type": "?", "rows": None, "bytes": None, "cols": 0}
                )
                node["cols"] = int(c)
        return dbs, data
    finally:
        cur.close()
        conn.close()


def totals(dbs, data):
    n_sch = sum(len(data[db]) for db in dbs)
    n_tbl = sum(len(t) for db in dbs for t in data[db].values())
    n_col = sum(i["cols"] for db in dbs for t in data[db].values() for i in t.values())
    return len(dbs), n_sch, n_tbl, n_col


# --- detail-panel HTML (for octopus click) ---------------------------------
def _detail(kind, title, path, rows):
    body = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows)
    return (
        f"<span class='dn'>{kind}</span><h3>{title}</h3>"
        f"<div class='dpath'>{path}</div><table class='dtab'>{body}</table>"
    )


# --- octopus (node-link) figure --------------------------------------------
def build_octopus(dbs, data, import_go):
    go = import_go
    # angular layout, weighted by leaf (table) count so big dbs get more arc
    def leaves(db):
        return max(sum(len(t) for t in data[db].values()), 1)

    total_w = sum(leaves(db) for db in dbs)
    gap = 0.12
    usable = 2 * math.pi - gap * len(dbs)
    R_DB, R_SCH, R_TBL = 1.15, 2.35, 3.7

    pos = {ROOT: (0.0, 0.0)}
    a = -math.pi / 2
    for db in dbs:
        span = usable * (leaves(db) / total_w)
        a0, a1 = a, a + span
        mid = (a0 + a1) / 2
        pos[db] = (R_DB * math.cos(mid), R_DB * math.sin(mid))
        schemas = data[db]
        if schemas:
            sch_w = sum(max(len(t), 1) for t in schemas.values())
            sa = a0
            for sch, tbls in schemas.items():
                sspan = span * (max(len(tbls), 1) / sch_w)
                s0, s1 = sa, sa + sspan
                smid = (s0 + s1) / 2
                pos[f"{db}/{sch}"] = (R_SCH * math.cos(smid), R_SCH * math.sin(smid))
                names = list(tbls.keys())
                n = len(names)
                for i, tbl in enumerate(names):
                    if n == 1:
                        tmid = smid
                    else:
                        pad = sspan * 0.14
                        tmid = (s0 + pad) + (s1 - pad - (s0 + pad)) * (i / (n - 1))
                    pos[f"{db}/{sch}/{tbl}"] = (R_TBL * math.cos(tmid), R_TBL * math.sin(tmid))
                sa = s1
        else:
            pos[f"{db}/(no tables)"] = (R_SCH * math.cos(mid), R_SCH * math.sin(mid))
        a = a1 + gap

    traces = []
    # tentacle edges, one coloured trace per database (drawn under the nodes)
    for i, db in enumerate(dbs):
        col = db_color(db, i)
        ex, ey = [], []

        def ln(p, c):
            x0, y0 = pos[p]
            x1, y1 = pos[c]
            ex.extend([x0, x1, None])
            ey.extend([y0, y1, None])

        ln(ROOT, db)
        if data[db]:
            for sch, tbls in data[db].items():
                ln(db, f"{db}/{sch}")
                for tbl in tbls:
                    ln(f"{db}/{sch}", f"{db}/{sch}/{tbl}")
        else:
            ln(db, f"{db}/(no tables)")
        traces.append(
            go.Scatter(x=ex, y=ey, mode="lines", hoverinfo="skip", showlegend=False,
                       line=dict(width=1.1, color=rgba(col, 0.40)))
        )

    # table (leaf) nodes
    tx, ty, tcol, tsize, tcd = [], [], [], [], []
    for i, db in enumerate(dbs):
        base = db_color(db, i)
        leafc = lighten(base, 0.50)
        for sch, tbls in data[db].items():
            for tbl, info in tbls.items():
                x, y = pos[f"{db}/{sch}/{tbl}"]
                tx.append(x); ty.append(y)
                tcol.append(leafc)
                tsize.append(6 + 1.4 * math.sqrt(info["cols"]))
                detail = _detail(
                    "TABLE" if "VIEW" not in (info["type"] or "") else "VIEW", tbl,
                    f"{db} · {sch}",
                    [("Type", info["type"]), ("Columns", fmt_int(info["cols"])),
                     ("Rows", fmt_int(info["rows"])), ("Size", fmt_bytes(info["bytes"]))],
                )
                tcd.append([db, sch, tbl, info["type"], fmt_int(info["cols"]),
                            fmt_int(info["rows"]), fmt_bytes(info["bytes"]), detail])
    traces.append(go.Scatter(
        x=tx, y=ty, mode="markers", name="tables", showlegend=False,
        marker=dict(size=tsize, color=tcol, line=dict(width=0.5, color="rgba(2,6,23,0.7)")),
        customdata=tcd,
        hovertemplate="<b>%{customdata[2]}</b><br>%{customdata[0]} · %{customdata[1]}"
        "<br>%{customdata[3]} · %{customdata[4]} cols"
        "<br>rows %{customdata[5]} · %{customdata[6]}<extra></extra>",
    ))

    # schema nodes
    sx, sy, scol, ssize, scd, stext = [], [], [], [], [], []
    for i, db in enumerate(dbs):
        base = db_color(db, i)
        midc = lighten(base, 0.22)
        for sch, tbls in data[db].items():
            x, y = pos[f"{db}/{sch}"]
            ncol = sum(t["cols"] for t in tbls.values())
            sx.append(x); sy.append(y); scol.append(midc)
            ssize.append(14 + 0.45 * math.sqrt(ncol))
            stext.append(sch)
            detail = _detail("SCHEMA", sch, db,
                             [("Tables / views", len(tbls)), ("Columns", fmt_int(ncol))])
            scd.append([db, sch, len(tbls), fmt_int(ncol), detail])
    traces.append(go.Scatter(
        x=sx, y=sy, mode="markers+text", name="schemas", showlegend=False,
        text=stext, textposition="top center",
        textfont=dict(size=9, color="rgba(226,232,240,0.75)"),
        marker=dict(size=ssize, color=scol, line=dict(width=1, color="rgba(2,6,23,0.8)")),
        customdata=scd,
        hovertemplate="<b>%{customdata[1]}</b><br>%{customdata[0]}"
        "<br>%{customdata[2]} tables · %{customdata[3]} cols<extra></extra>",
    ))

    # database nodes
    dx, dy, dcol, dsize, dcd, dtext = [], [], [], [], [], []
    for i, db in enumerate(dbs):
        x, y = pos[db]
        ncol = sum(t["cols"] for s in data[db].values() for t in s.values())
        ntbl = sum(len(s) for s in data[db].values())
        dx.append(x); dy.append(y); dcol.append(db_color(db, i))
        dsize.append(26 + 0.42 * math.sqrt(ncol))
        dtext.append(db.replace("LIBRARY_", ""))
        detail = _detail("DATABASE", db, "Ripple Library",
                         [("Schemas", len(data[db])), ("Tables / views", ntbl),
                          ("Columns", fmt_int(ncol))])
        dcd.append([db, len(data[db]), ntbl, fmt_int(ncol), detail])
    traces.append(go.Scatter(
        x=dx, y=dy, mode="markers+text", name="databases", showlegend=False,
        text=dtext, textposition="middle center",
        textfont=dict(size=10, color="#0b1220", family="Inter, system-ui, sans-serif"),
        marker=dict(size=dsize, color=dcol, line=dict(width=2, color="rgba(255,255,255,0.85)")),
        customdata=dcd,
        hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]} schemas · "
        "%{customdata[2]} tables · %{customdata[3]} cols<extra></extra>",
    ))

    # root (the head)
    nd, ns, nt, nc = totals(dbs, data)
    root_detail = _detail("LIBRARY", "Ripple Library", "Snowflake warehouse",
                          [("Databases", nd), ("Schemas", ns), ("Tables / views", nt),
                           ("Columns", fmt_int(nc))])
    traces.append(go.Scatter(
        x=[0], y=[0], mode="markers+text", name="library", showlegend=False,
        text=["🐙"], textposition="middle center", textfont=dict(size=26),
        marker=dict(size=54, color="#0b1220", line=dict(width=2.5, color="#5eead4")),
        customdata=[[nd, ns, nt, fmt_int(nc), root_detail]],
        hovertemplate="<b>Ripple Library</b><br>%{customdata[0]} databases · "
        "%{customdata[1]} schemas · %{customdata[2]} tables<extra></extra>",
    ))

    layout = go.Layout(
        paper_bgcolor="#0b1220", plot_bgcolor="#0b1220",
        margin=dict(l=8, r=8, t=8, b=8), autosize=True, hovermode="closest",
        xaxis=dict(visible=False, fixedrange=False),
        yaxis=dict(visible=False, scaleanchor="x", scaleratio=1),
        hoverlabel=dict(bgcolor="#0f172a", bordercolor="#334155",
                        font=dict(color="#e2e8f0", size=12)),
        font=dict(color="#e2e8f0"),
    )
    return go.Figure(data=traces, layout=layout)


# --- hierarchical (sunburst + treemap) figures -----------------------------
def build_hier(dbs, data, import_go):
    go = import_go
    ids, labels, parents, values, colors, cd = [], [], [], [], [], []

    def add(_id, label, parent, value, color, kind, extra):
        ids.append(_id); labels.append(label); parents.append(parent)
        values.append(value); colors.append(color); cd.append([kind, extra])

    root_total = 0
    for i, db in enumerate(dbs):
        base = db_color(db, i)
        schemas = data[db]
        db_total = 0
        if not schemas:
            add(f"{db}/(none)", "(no tables)", db, 1, "#475569", "empty", "MCP host — no data")
            db_total = 1
        for sch, tbls in schemas.items():
            sch_total = 0
            for tbl, info in tbls.items():
                v = max(info["cols"], 1)
                add(f"{db}/{sch}/{tbl}", tbl, f"{db}/{sch}", v, lighten(base, 0.50),
                    "table" if "VIEW" not in (info["type"] or "") else "view",
                    f"{fmt_int(info['cols'])} cols · {fmt_int(info['rows'])} rows · {fmt_bytes(info['bytes'])}")
                sch_total += v
            add(f"{db}/{sch}", sch, db, max(sch_total, 1), lighten(base, 0.22),
                "schema", f"{len(tbls)} tables · {fmt_int(sum(t['cols'] for t in tbls.values()))} cols")
            db_total += max(sch_total, 1)
        ntbl = sum(len(s) for s in schemas.values())
        ncol = sum(t["cols"] for s in schemas.values() for t in s.values())
        add(db, db, ROOT, max(db_total, 1), base, "database",
            f"{len(schemas)} schemas · {ntbl} tables · {fmt_int(ncol)} cols")
        root_total += max(db_total, 1)

    nd, ns, nt, nc = totals(dbs, data)
    ids.append(ROOT); labels.append("LIBRARY"); parents.append("")
    values.append(root_total); colors.append("#0b1220")
    cd.append(["library", f"{nd} dbs · {ns} schemas · {nt} tables · {fmt_int(nc)} cols"])

    htmpl = "<b>%{label}</b><br>%{customdata[0]}<br>%{customdata[1]}<br>Σ %{value} cols<extra></extra>"
    common = dict(ids=ids, labels=labels, parents=parents, values=values, customdata=cd,
                  branchvalues="total", hovertemplate=htmpl,
                  marker=dict(colors=colors, line=dict(width=1, color="#0b1220")))
    lay = go.Layout(paper_bgcolor="#0b1220", margin=dict(l=6, r=6, t=6, b=6), autosize=True,
                    font=dict(color="#e2e8f0"),
                    hoverlabel=dict(bgcolor="#0f172a", bordercolor="#334155",
                                    font=dict(color="#e2e8f0", size=12)))
    sun = go.Figure(data=[go.Sunburst(maxdepth=3, insidetextorientation="radial",
                                      textfont=dict(size=11), **common)], layout=lay)
    tree = go.Figure(data=[go.Treemap(maxdepth=3, tiling=dict(packing="squarify"),
                                      textfont=dict(size=12),
                                      pathbar=dict(visible=True), **common)], layout=lay)
    return sun, tree


# --- HTML assembly ---------------------------------------------------------
def render_html(dbs, data, plotlyjs, fig_octo, fig_sun, fig_tree):
    nd, ns, nt, nc = totals(dbs, data)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    stats = "".join(
        f"<div class='stat'><div class='num'>{v}</div><div class='lbl'>{l}</div></div>"
        for v, l in [(nd, "databases"), (ns, "schemas"), (nt, "tables / views"), (f"{nc:,}", "columns")]
    )
    legend = "".join(
        f"<span class='lg'><i style='background:{db_color(db, i)}'></i>"
        f"{db}<b>{sum(len(s) for s in data[db].values())}</b>t·"
        f"{sum(t['cols'] for s in data[db].values() for t in s.values()):,}c</span>"
        for i, db in enumerate(dbs)
    )

    tmpl = r"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Ripple Library — Octopus Map</title>
<style>
  :root { --bg:#0b1220; --panel:#0f172a; --line:#1e293b; --ink:#e2e8f0; --dim:#94a3b8; --accent:#5eead4; }
  * { box-sizing:border-box; }
  body { margin:0; background:var(--bg); color:var(--ink);
         font-family:Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif; }
  header { padding:18px 22px 10px; border-bottom:1px solid var(--line); }
  h1 { margin:0; font-size:20px; letter-spacing:.2px; }
  h1 .em { font-size:22px; }
  .sub { color:var(--dim); font-size:12.5px; margin-top:3px; }
  .stats { display:flex; gap:26px; margin:14px 0 6px; flex-wrap:wrap; }
  .stat .num { font-size:24px; font-weight:700; color:var(--accent); }
  .stat .lbl { font-size:11px; color:var(--dim); text-transform:uppercase; letter-spacing:.6px; }
  .legend { display:flex; gap:14px; flex-wrap:wrap; margin-top:8px; font-size:11.5px; color:var(--dim); }
  .lg { display:inline-flex; align-items:center; gap:6px; }
  .lg i { width:11px; height:11px; border-radius:3px; display:inline-block; }
  .lg b { color:var(--ink); font-weight:600; margin:0 1px; }
  .tabs { display:flex; gap:8px; padding:12px 22px 0; }
  .tab { background:var(--panel); color:var(--dim); border:1px solid var(--line);
         padding:8px 16px; border-radius:9px 9px 0 0; cursor:pointer; font-size:13px; font-weight:600; }
  .tab:hover { color:var(--ink); }
  .tab.on { color:var(--bg); background:var(--accent); border-color:var(--accent); }
  .wrap { display:flex; gap:0; padding:0 22px 18px; }
  .stage { flex:1; min-width:0; border:1px solid var(--line); border-radius:0 10px 10px 10px;
           background:#070d18; position:relative; }
  .plot { width:100%; height:78vh; }
  .plot.hidden { display:none; }
  .panel { width:300px; flex:0 0 300px; margin-left:14px; background:var(--panel);
           border:1px solid var(--line); border-radius:10px; padding:16px 16px 20px; align-self:flex-start; }
  .panel .hint { color:var(--dim); font-size:12.5px; line-height:1.55; }
  .panel .dn { display:inline-block; font-size:10px; letter-spacing:1px; color:var(--accent);
               border:1px solid var(--accent); border-radius:5px; padding:1px 7px; text-transform:uppercase; }
  .panel h3 { margin:10px 0 2px; font-size:17px; word-break:break-all; }
  .panel .dpath { color:var(--dim); font-size:12px; margin-bottom:10px; }
  .dtab { width:100%; border-collapse:collapse; font-size:12.5px; }
  .dtab td { padding:5px 0; border-bottom:1px solid var(--line); }
  .dtab td:first-child { color:var(--dim); }
  .dtab td:last-child { text-align:right; font-variant-numeric:tabular-nums; }
  footer { color:var(--dim); font-size:11.5px; padding:0 22px 22px; line-height:1.5; }
  code { background:#0f172a; padding:1px 5px; border-radius:4px; color:#cbd5e1; }
  @media (max-width:900px){ .wrap{flex-direction:column;} .panel{width:auto;flex:auto;margin:14px 0 0;} }
</style>
<script type="text/javascript">__PLOTLYJS__</script>
</head>
<body>
<header>
  <h1><span class="em">🐙</span> Ripple Library — Octopus Map</h1>
  <div class="sub">Every <b>LIBRARY_*</b> database, schema, table &amp; column — live from <code>INFORMATION_SCHEMA</code>. Generated __STAMP__.</div>
  <div class="stats">__STATS__</div>
  <div class="legend">__LEGEND__</div>
</header>
<div class="tabs">
  <div class="tab on" data-t="octo">🐙 Octopus</div>
  <div class="tab" data-t="sun">☀️ Sunburst</div>
  <div class="tab" data-t="tree">▦ Treemap</div>
</div>
<div class="wrap">
  <div class="stage">
    <div id="octo" class="plot"></div>
    <div id="sun" class="plot hidden"></div>
    <div id="tree" class="plot hidden"></div>
  </div>
  <div class="panel" id="panel">
    <div class="hint"><b>Click any node</b> for details.<br><br>
      🐙 <b>Octopus</b> — the head is the Library; each tentacle is a database fanning out to its
      schemas and tables. Marker size = column count. Drag to pan, scroll to zoom.<br><br>
      ☀️ <b>Sunburst</b> / ▦ <b>Treemap</b> — click to drill into a database, click the centre/crumb to back out.</div>
  </div>
</div>
<footer>
  Source: <code>SHOW DATABASES LIKE 'LIBRARY_%'</code> + each database's <code>INFORMATION_SCHEMA.TABLES</code> /
  <code>.COLUMNS</code>. Wedge &amp; rectangle size = Σ columns in that subtree. Self-contained — Plotly is inlined, no network needed.
  Re-run <code>build_library_map.py</code> to refresh.
</footer>
<script type="text/javascript">
  var FIGS = { octo: __FIG_OCTO__, sun: __FIG_SUN__, tree: __FIG_TREE__ };
  var CFG  = { responsive:true, displaylogo:false,
               modeBarButtonsToRemove:['select2d','lasso2d'] };
  var drawn = {};
  function draw(id){
    if(drawn[id]) { Plotly.Plots.resize(document.getElementById(id)); return; }
    Plotly.newPlot(id, FIGS[id].data, FIGS[id].layout, CFG);
    drawn[id] = true;
    if(id==='octo'){
      document.getElementById('octo').on('plotly_click', function(ev){
        var cd = ev.points[0].customdata;
        if(cd && cd.length){ document.getElementById('panel').innerHTML = cd[cd.length-1]; }
      });
    }
  }
  draw('octo');
  document.querySelectorAll('.tab').forEach(function(t){
    t.addEventListener('click', function(){
      document.querySelectorAll('.tab').forEach(function(x){ x.classList.remove('on'); });
      t.classList.add('on');
      ['octo','sun','tree'].forEach(function(id){
        document.getElementById(id).classList.toggle('hidden', id!==t.dataset.t);
      });
      draw(t.dataset.t);
    });
  });
</script>
</body></html>"""

    return (
        tmpl.replace("__PLOTLYJS__", plotlyjs)
        .replace("__STAMP__", stamp)
        .replace("__STATS__", stats)
        .replace("__LEGEND__", legend)
        .replace("__FIG_OCTO__", fig_octo.to_json())
        .replace("__FIG_SUN__", fig_sun.to_json())
        .replace("__FIG_TREE__", fig_tree.to_json())
    )


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    default_out = os.path.normpath(os.path.join(here, "..", "outputs", "library_map.html"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=default_out, help="destination .html path")
    args = ap.parse_args()

    import plotly.graph_objects as go
    from plotly.offline import get_plotlyjs

    print("Querying INFORMATION_SCHEMA across LIBRARY_* databases ...")
    dbs, data = collect()
    nd, ns, nt, nc = totals(dbs, data)
    print(f"  {nd} databases · {ns} schemas · {nt} tables · {nc:,} columns")

    print("Building figures ...")
    fig_octo = build_octopus(dbs, data, go)
    fig_sun, fig_tree = build_hier(dbs, data, go)

    html = render_html(dbs, data, get_plotlyjs(), fig_octo, fig_sun, fig_tree)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)
    size_mb = os.path.getsize(args.out) / 1e6
    print(f"Wrote {args.out}  ({size_mb:.1f} MB, self-contained)")


if __name__ == "__main__":
    main()
