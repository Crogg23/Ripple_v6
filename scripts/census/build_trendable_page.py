"""Render the trendable inventory as one browsable page.

Every table and column in the warehouse that can be placed on a time axis, in a
form that can be scanned, filtered and sorted rather than read. 953 columns
across 403 tables.

Reads reports/time_index/TRENDABLE.csv. Writes a self-contained HTML file.
No warehouse, no network.
"""
import csv
import html
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plain_english as pe  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "reports", "time_index", "TRENDABLE.csv")

ACRONYMS = {
    "FED", "INTL", "ST", "XC", "US", "UK", "CA", "TX", "NYC", "IE", "ES", "IT", "FR",
    "DEA", "EPA", "CMS", "FDA", "SEC", "FEC", "IRS", "DOL", "DOT", "FAA", "FRA",
    "NHTSA", "MSHA", "OSHA", "NPDES", "RCRA", "SDWA", "ICIS", "AQS", "FRS", "ECHO",
    "HUD", "SBA", "PPP", "FDIC", "NCUA", "GLEIF", "LEI", "ICIJ", "NIH", "NSF",
    "SBIR", "STTR", "USGS", "NOAA", "NARA", "FBI", "ICE", "DHS", "CFPB", "CPSC",
    "NEISS", "MAUDE", "GUDID", "PMA", "NPDB", "HRSA", "POS", "CCN", "NPI", "EIN",
    "FJC", "IDB", "CL", "OWID", "ROR", "OSF", "PBGC", "FAC", "DTS", "EIA", "NID",
    "GNIS", "ITIS", "BORME", "CRO", "NAAG", "FTC", "SAM", "ARCOS", "HMDA", "SOD",
    "FOICU", "OFLC", "LCR", "SNC", "SE", "PS", "CS", "PN", "VIO", "API", "AAD",
    "WRA", "CDE", "UCDP", "GED", "ISTAT", "AIS", "IMO", "MF", "13F", "527", "990",
    "8871", "8872", "5500", "861", "860", "SDWIS", "NPL", "TRI", "GHG", "MRF",
    "HPT", "SNF", "FQHC", "RHC", "OPT", "IN", "DFE", "PN", "PGM", "SYS", "ID",
}


def humanize(source):
    parts = [p for p in source.split("_") if p]
    out = []
    for p in parts:
        if p.upper() in ACRONYMS or (len(p) <= 3 and p.isupper()):
            out.append(p.upper())
        elif p.isdigit():
            out.append(p)
        else:
            out.append(p.capitalize())
    return " ".join(out)


def humanize_col(col):
    parts = [p for p in col.split("_") if p]
    out = []
    for p in parts:
        out.append(p.upper() if p.upper() in ACRONYMS else p.capitalize())
    return " ".join(out)


MEANS = {
    "happened": ("when it happened", "happened"),
    "reported": ("when it was reported", "reported"),
    "decided": ("when it was decided", "decided"),
    "span_start": ("start of a period", "start"),
    "span_end": ("end of a period", "end"),
}
GRAINS = {
    "day": ("daily", "day"),
    "month": ("monthly", "month"),
    "quarter": ("quarterly", "quarter"),
    "year": ("yearly only", "year"),
}


def load():
    recs = []
    for r in csv.DictReader(open(SRC, encoding="utf-8")):
        schema, table = r["table"].split(".", 1)
        source = table[len(schema) + 2:] if table.upper().startswith(schema.upper() + "__") else table
        rows = int(r["rows"] or 0)
        vals = int(r["values"] or 0)
        y0 = r["from"][:4]
        y1 = r["to"][:4]
        recs.append({
            "d": schema,                                   # domain
            "t": table,                                    # real table name
            "h": humanize(source),                         # readable label
            "c": r["column"],                              # real column name
            "ch": humanize_col(r["column"]),               # readable column
            "m": r["means"],
            "g": r["grain"],
            "n": rows,
            "v": vals,
            "f": round(vals / rows, 4) if rows else 0,     # fill rate
            "y0": int(y0) if y0.isdigit() else None,
            "y1": int(y1) if y1.isdigit() else None,
            "wd": pe.TABLES.get(source.upper()) or pe.readable_source(source),
            "wn": pe.field_gloss(source, r["column"]),
        })
    return recs


def build(recs, out_path):
    domains = sorted({r["d"] for r in recs})
    n_tables = len({r["t"] for r in recs})
    n_rows_total = sum({r["t"]: r["n"] for r in recs}.values())
    data = json.dumps(recs, separators=(",", ":"))

    def chip_row(mapping, cls):
        return "".join(
            '<button class="chip {c}" data-{c}="{k}" aria-pressed="true">'
            '<span class="dot"></span>{lbl}</button>'.format(c=cls, k=k, lbl=html.escape(v[0]))
            for k, v in mapping.items())

    opts = "".join('<option value="{0}">{0}</option>'.format(html.escape(d)) for d in domains)

    css = """
:root{
  --ground:#E9EDF1; --surface:#FFFFFF; --surface-2:#F4F6F9;
  --ink:#0F1620; --ink-2:#3D4A57; --ink-3:#6B7885;
  --line:#D3DAE1; --line-2:#E4E9EE;
  --accent:#0B6E75; --accent-soft:#0B6E7514; --warn:#9C5A16;
  --happened:#0B6E75; --reported:#2C5F9E; --decided:#5A4FA3;
  --span_start:#4A7043; --span_end:#96562F;
  --bar:#0B6E7526; --bar-fill:#0B6E75;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --ground:#0A0F15; --surface:#121A23; --surface-2:#18222D;
    --ink:#E6ECF2; --ink-2:#A9B6C3; --ink-3:#798794;
    --line:#243140; --line-2:#1C2733;
    --accent:#4FC0C6; --accent-soft:#4FC0C61F; --warn:#D69A4C;
    --happened:#4FC0C6; --reported:#7FA8E0; --decided:#A79BE8;
    --span_start:#8FBF84; --span_end:#DE9670;
    --bar:#4FC0C62E; --bar-fill:#4FC0C6;
  }
}
:root[data-theme="dark"]{
  --ground:#0A0F15; --surface:#121A23; --surface-2:#18222D;
  --ink:#E6ECF2; --ink-2:#A9B6C3; --ink-3:#798794;
  --line:#243140; --line-2:#1C2733;
  --accent:#4FC0C6; --accent-soft:#4FC0C61F; --warn:#D69A4C;
  --happened:#4FC0C6; --reported:#7FA8E0; --decided:#A79BE8;
  --span_start:#8FBF84; --span_end:#DE9670;
  --bar:#4FC0C62E; --bar-fill:#4FC0C6;
}

*{box-sizing:border-box}
body{
  margin:0; background:var(--ground); color:var(--ink);
  font-family:"IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  font-size:15px; line-height:1.5;
}
.wrap{max-width:1220px;margin:0 auto;padding:0 20px 80px}

header.masthead{padding:44px 0 26px;border-bottom:1px solid var(--line)}
.eyebrow{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:11px;
  letter-spacing:.16em; text-transform:uppercase; color:var(--ink-3); margin:0 0 14px;
}
h1{
  font-family:"Newsreader",Georgia,serif; font-weight:400; font-size:clamp(34px,5.2vw,54px);
  line-height:1.04; letter-spacing:-.015em; margin:0 0 14px; text-wrap:balance;
}
.standfirst{max-width:62ch;color:var(--ink-2);margin:0 0 30px;font-size:16.5px}
.stats{display:flex;flex-wrap:wrap;gap:38px}
.stat .num{
  font-family:"Newsreader",Georgia,serif; font-size:36px; line-height:1;
  font-variant-numeric:tabular-nums; color:var(--accent);
}
.stat .lab{
  font-family:"IBM Plex Mono",ui-monospace,monospace; font-size:10.5px;
  letter-spacing:.13em; text-transform:uppercase; color:var(--ink-3); margin-top:7px;
}

.controls{
  position:sticky; top:0; z-index:20; background:var(--ground);
  border-bottom:1px solid var(--line); padding:16px 0 14px;
  display:flex; flex-direction:column; gap:12px;
}
.row1{display:flex;gap:12px;flex-wrap:wrap;align-items:center}
input[type=search],select{
  font:inherit; font-size:14px; color:var(--ink); background:var(--surface);
  border:1px solid var(--line); border-radius:3px; padding:8px 11px;
}
input[type=search]{flex:1;min-width:230px}
input[type=search]:focus-visible,select:focus-visible,.chip:focus-visible{
  outline:2px solid var(--accent); outline-offset:2px;
}
.chips{display:flex;gap:7px;flex-wrap:wrap;align-items:center}
.chipset-label{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:10px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);margin-right:2px;
}
.chip{
  font:inherit;font-size:12.5px;cursor:pointer;background:var(--surface);
  color:var(--ink-2);border:1px solid var(--line);border-radius:100px;
  padding:5px 12px 5px 9px;display:inline-flex;align-items:center;gap:7px;
}
.chip .dot{width:8px;height:8px;border-radius:50%;background:var(--ink-3);flex:none}
.chip[aria-pressed="false"]{opacity:.4}
.chip.mean[data-mean="happened"] .dot{background:var(--happened)}
.chip.mean[data-mean="reported"] .dot{background:var(--reported)}
.chip.mean[data-mean="decided"] .dot{background:var(--decided)}
.chip.mean[data-mean="span_start"] .dot{background:var(--span_start)}
.chip.mean[data-mean="span_end"] .dot{background:var(--span_end)}
.chip.grain[data-grain="day"] .dot{background:var(--accent)}
.chip.grain[data-grain="month"] .dot{background:var(--accent);opacity:.7}
.chip.grain[data-grain="quarter"] .dot{background:var(--accent);opacity:.5}
.chip.grain[data-grain="year"] .dot{background:var(--warn)}
.count{
  margin-left:auto;font-family:"IBM Plex Mono",ui-monospace,monospace;
  font-size:12px;color:var(--ink-3);font-variant-numeric:tabular-nums;
}

.tablewrap{overflow-x:auto;margin-top:22px}
table{width:100%;border-collapse:collapse;min-width:1050px}
thead th{
  position:sticky;top:118px;z-index:10;background:var(--ground);
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-weight:500;font-size:10.5px;
  letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);
  text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);white-space:nowrap;
}
thead th.sortable{cursor:pointer;user-select:none}
thead th.sortable:hover{color:var(--ink)}
thead th .arrow{opacity:0;margin-left:4px}
thead th.active{color:var(--accent)}
thead th.active .arrow{opacity:1}
tbody tr{border-bottom:1px solid var(--line-2)}
tbody tr:hover{background:var(--surface-2)}
td{padding:14px 12px;vertical-align:top}
.tname{font-weight:600;line-height:1.3}
.plain{margin:4px 0 0;font-size:13px;line-height:1.42;color:var(--ink-2);max-width:46ch}
.treal,.creal{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11px;
  color:var(--ink-3);word-break:break-all;display:block;margin-top:3px;
}
.cname{line-height:1.3}
.tag{
  display:inline-block;font-size:11.5px;padding:2px 9px;border-radius:100px;
  border:1px solid currentColor;white-space:nowrap;
}
.tag.m-happened{color:var(--happened)} .tag.m-reported{color:var(--reported)}
.tag.m-decided{color:var(--decided)} .tag.m-span_start{color:var(--span_start)}
.tag.m-span_end{color:var(--span_end)}
.grainlab{font-size:12.5px;color:var(--ink-2);white-space:nowrap}
.grainlab.coarse{color:var(--warn)}
.num{
  font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:12.5px;
  font-variant-numeric:tabular-nums;text-align:right;white-space:nowrap;
}
.fill{display:flex;align-items:center;gap:8px;justify-content:flex-end}
.fillbar{width:34px;height:5px;background:var(--bar);border-radius:3px;flex:none;overflow:hidden}
.fillbar span{display:block;height:100%;background:var(--bar-fill)}
.fill.low .fillbar span{background:var(--warn)}
.fill.low .pct{color:var(--warn)}
.pct{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;
     font-variant-numeric:tabular-nums;color:var(--ink-3);width:38px;text-align:right}

.span{display:flex;align-items:center;gap:9px;min-width:210px}
.track{position:relative;flex:1;height:16px}
.track::before{
  content:"";position:absolute;left:0;right:0;top:7px;height:1px;background:var(--line);
}
.track i{
  position:absolute;top:5px;height:5px;background:var(--bar-fill);
  border-radius:3px;min-width:3px;
}
.track b{
  position:absolute;top:0;bottom:0;width:1px;background:var(--line);opacity:.85;
}
.yrs{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:11.5px;
     color:var(--ink-3);font-variant-numeric:tabular-nums;white-space:nowrap;width:92px}
.early{color:var(--warn)}

.axis{display:flex;justify-content:space-between;margin:2px 0 0;padding-left:0}
.axis span{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:9.5px;color:var(--ink-3)}

.note{
  margin-top:34px;padding:20px 22px;background:var(--surface);
  border:1px solid var(--line);border-radius:4px;max-width:68ch;
}
.note h2{
  font-family:"Newsreader",Georgia,serif;font-weight:400;font-size:21px;margin:0 0 10px;
}
.note p{margin:0 0 10px;color:var(--ink-2);font-size:14.5px}
.note p:last-child{margin-bottom:0}
.note strong{color:var(--ink)}
.empty{padding:60px 0;text-align:center;color:var(--ink-3)}
@media (max-width:720px){
  thead th{top:0;position:static}
  .controls{position:static}
}
"""

    js = """
const DATA = __DATA__;
const MEANLAB = __MEANLAB__;
const GRAINLAB = __GRAINLAB__;
const AX0 = 1900, AX1 = 2030;

const state = {
  q:"", domain:"", sort:"n", dir:-1,
  means:new Set(Object.keys(MEANLAB)),
  grains:new Set(Object.keys(GRAINLAB)),
};

const fmt = n => n.toLocaleString("en-US");
const tbody = document.getElementById("rows");
const countEl = document.getElementById("count");

function pos(y){
  const c = Math.max(AX0, Math.min(AX1, y));
  return ((c - AX0) / (AX1 - AX0)) * 100;
}

function rowHTML(r){
  const early = (r.y0 !== null && r.y0 < AX0);
  const left = r.y0===null?0:pos(r.y0);
  const right = r.y1===null?left:pos(r.y1);
  const lowFill = r.f < 0.5;
  return `<tr>
    <td>
      <div class="tname">${r.h}</div>
      <p class="plain">${r.wd}</p>
      <span class="treal">${r.t}</span>
    </td>
    <td>
      <div class="cname">${r.ch}</div>
      <p class="plain">${r.wn}</p>
      <span class="creal">${r.c}</span>
    </td>
    <td><span class="tag m-${r.m}">${MEANLAB[r.m]}</span></td>
    <td><span class="grainlab${r.g==="year"?" coarse":""}">${GRAINLAB[r.g]}</span></td>
    <td class="num">${fmt(r.n)}</td>
    <td>
      <div class="fill${lowFill?" low":""}">
        <span class="pct">${(r.f*100).toFixed(r.f<0.1?1:0)}%</span>
        <span class="fillbar"><span style="width:${Math.max(2,r.f*100)}%"></span></span>
      </div>
    </td>
    <td>
      <div class="span">
        <span class="yrs${early?" early":""}">${r.y0===null?"—":(early?"◄"+r.y0:r.y0)}–${r.y1===null?"—":r.y1}</span>
        <span class="track"><b style="left:${pos(2000)}%"></b><i style="left:${left}%;width:${Math.max(0.6,right-left)}%"></i></span>
      </div>
    </td>
  </tr>`;
}

function apply(){
  const q = state.q.toLowerCase();
  let rows = DATA.filter(r =>
    state.means.has(r.m) && state.grains.has(r.g) &&
    (!state.domain || r.d === state.domain) &&
    (!q || r.t.toLowerCase().includes(q) || r.c.toLowerCase().includes(q) ||
      r.h.toLowerCase().includes(q) || r.ch.toLowerCase().includes(q) ||
      r.wd.toLowerCase().includes(q) || r.wn.toLowerCase().includes(q))
  );
  const k = state.sort, dir = state.dir;
  rows.sort((a,b)=>{
    let x=a[k], y=b[k];
    if(k==="t"||k==="h"||k==="c"){ x=String(x).toLowerCase(); y=String(y).toLowerCase(); }
    if(x===null) x = -Infinity; if(y===null) y = -Infinity;
    return x<y ? -dir : x>y ? dir : 0;
  });
  const tabs = new Set(rows.map(r=>r.t));
  countEl.textContent = `${fmt(rows.length)} columns · ${fmt(tabs.size)} tables`;
  tbody.innerHTML = rows.length
    ? rows.map(rowHTML).join("")
    : `<tr><td colspan="7" class="empty">Nothing matches those filters.</td></tr>`;
}

document.getElementById("q").addEventListener("input", e=>{ state.q=e.target.value; apply(); });
document.getElementById("domain").addEventListener("change", e=>{ state.domain=e.target.value; apply(); });

document.querySelectorAll(".chip.mean").forEach(el=>{
  el.addEventListener("click", ()=>{
    const k = el.dataset.mean, on = el.getAttribute("aria-pressed")==="true";
    el.setAttribute("aria-pressed", String(!on));
    on ? state.means.delete(k) : state.means.add(k);
    apply();
  });
});
document.querySelectorAll(".chip.grain").forEach(el=>{
  el.addEventListener("click", ()=>{
    const k = el.dataset.grain, on = el.getAttribute("aria-pressed")==="true";
    el.setAttribute("aria-pressed", String(!on));
    on ? state.grains.delete(k) : state.grains.add(k);
    apply();
  });
});
document.querySelectorAll("th.sortable").forEach(th=>{
  th.addEventListener("click", ()=>{
    const k = th.dataset.k;
    if(state.sort===k){ state.dir *= -1; }
    else { state.sort=k; state.dir = (k==="h"||k==="c") ? 1 : -1; }
    document.querySelectorAll("th.sortable").forEach(o=>o.classList.toggle("active", o===th));
    th.querySelector(".arrow").textContent = state.dir===1 ? "\\u2191" : "\\u2193";
    apply();
  });
});

apply();
"""
    js = (js.replace("__DATA__", data)
            .replace("__MEANLAB__", json.dumps({k: v[0] for k, v in MEANS.items()}))
            .replace("__GRAINLAB__", json.dumps({k: v[0] for k, v in GRAINS.items()})))

    doc = """<title>Every Clock We Hold</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300;6..72,400&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>%CSS%</style>

<div class="wrap">
  <header class="masthead">
    <p class="eyebrow">The Ripple warehouse · measured 20 August 2026</p>
    <h1>Every clock we hold</h1>
    <p class="standfirst">Every table and every column in the warehouse that can be put on a
      time axis — what the date actually means, how precise it really is, how much of the
      column is filled in, and the years it covers. Nothing is selected or ranked. This is
      the whole net.</p>
    <div class="stats">
      <div class="stat"><div class="num">%NCOL%</div><div class="lab">Trendable columns</div></div>
      <div class="stat"><div class="num">%NTAB%</div><div class="lab">Tables</div></div>
      <div class="stat"><div class="num">%NROW%</div><div class="lab">Rows behind them</div></div>
      <div class="stat"><div class="num">%NDOM%</div><div class="lab">Subject areas</div></div>
    </div>
  </header>

  <div class="controls">
    <div class="row1">
      <input type="search" id="q" placeholder="Search anything — a subject, a table, a column…" aria-label="Search tables and columns">
      <select id="domain" aria-label="Filter by subject area">
        <option value="">All subject areas</option>
        %OPTS%
      </select>
      <span class="count" id="count"></span>
    </div>
    <div class="chips"><span class="chipset-label">Means</span>%MEANCHIPS%</div>
    <div class="chips"><span class="chipset-label">Precision</span>%GRAINCHIPS%</div>
  </div>

  <div class="tablewrap">
    <table>
      <thead>
        <tr>
          <th class="sortable" data-k="h" style="width:27%">What the data is<span class="arrow"></span></th>
          <th class="sortable" data-k="c" style="width:24%">What the date is<span class="arrow"></span></th>
          <th>What the date means</th>
          <th>Precision</th>
          <th class="sortable active" data-k="n" style="text-align:right">Rows<span class="arrow">↓</span></th>
          <th class="sortable" data-k="f" style="text-align:right">Filled in<span class="arrow"></span></th>
          <th class="sortable" data-k="y0">Covers<span class="arrow"></span></th>
        </tr>
      </thead>
      <tbody id="rows"></tbody>
    </table>
  </div>

  <div class="note">
    <h2>Three things to read off this before charting anything</h2>
    <p><strong>Filled in</strong> is the one that bites. A column can be perfectly good and
      still be blank on 99% of rows — court dockets carry an argument date on 0.3% of
      cases. Trend that and you are charting the handful of cases someone bothered to fill
      in, not the courts.</p>
    <p><strong>Precision</strong> matters more than it looks. 217 of these columns give one
      point per year and nothing finer. They are bars by year, never daily lines — mixing
      them with daily sources invents a spike every 1 January.</p>
    <p><strong>What the date means</strong> is not interchangeable. Adding a “when it
      happened” column to a “when it was reported” column sums two different questions.
      Start and end dates mark the edges of a period, so counting them as events double-counts
      the same thing twice.</p>
  </div>
</div>
<script>%JS%</script>
"""
    doc = (doc.replace("%CSS%", css)
              .replace("%JS%", js)
              .replace("%OPTS%", opts)
              .replace("%MEANCHIPS%", chip_row(MEANS, "mean"))
              .replace("%GRAINCHIPS%", chip_row(GRAINS, "grain"))
              .replace("%NCOL%", "{:,}".format(len(recs)))
              .replace("%NTAB%", "{:,}".format(n_tables))
              .replace("%NROW%", "{:.0f}M".format(n_rows_total / 1e6))
              .replace("%NDOM%", str(len(domains))))
    open(out_path, "w", encoding="utf-8").write(doc)
    return out_path, len(recs), n_tables, n_rows_total


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(REPO, "trendable.html")
    recs = load()
    p, ncol, ntab, nrow = build(recs, out)
    print("wrote {}  ({} columns, {} tables, {:,} rows)".format(p, ncol, ntab, nrow))
