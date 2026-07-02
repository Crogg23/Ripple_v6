#!/usr/bin/env python3
"""Build a single self-contained HTML page so Chris can SEE the backend:
every detector insight (with evidence + a verify link) and the whole landed Library
(with a measured data-quality flag). Read-only. No server, no deps — double-click the file.

    python3 scripts/build_dashboard.py            # -> outputs/ripple_dashboard.html
    open outputs/ripple_dashboard.html            # (macOS) view it

Re-run any time to refresh. Data-quality is sampled (<=500 rows/table) to stay cheap
against the 15-credit cap.
"""
import sys, warnings, json, html
warnings.filterwarnings("ignore")
sys.path.insert(0, "c:/Code/Ripple_v6")
from connect import db
from connect import leads as leads_engine

OUT = "c:/Code/Ripple_v6/outputs/ripple_dashboard.html"
META = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"}
c = db.connect()

# ---------------------------------------------------------------- INSIGHTS (LEADS)
# THE safety chokepoint: leads.published() = STATUS='active' + the DECISIONS anti-join,
# so a rejected / retracted / stale lead can never land on this page. Never query the
# LEADS table directly here.
leads = sorted(leads_engine.published(c),
               key=lambda r: (r["RULE_NAME"], -float(r["SCORE"] or 0)))
for L in leads:
    L["EV"] = L.get("EVIDENCE") or "[]"
    L["SEEN"] = str(L.get("LAST_SEEN") or "")[:10]
    L["STATUS"] = L.get("STATUS") or "active"

# One label per rule in leads_specs.JOBS. Archive-honest copy: the AIS data is a
# US-coastal ARCHIVE, so "appears in" — never "still broadcasting".
RULE_LABEL = {
    "banned_but_operating":              ("Banned providers on facility rosters", "OIG-excluded provider × CMS facility roster, joined on NPI"),
    "banned_but_paid":                   ("Banned providers in Open Payments records", "OIG-excluded provider × CMS Open Payments (all years), joined on NPI"),
    "excluded_but_billing":              ("Banned providers in Part D prescriber records", "OIG-excluded provider × Medicare Part D prescribers, joined on NPI"),
    "sanctioned_vessel_broadcasting":    ("Sanctioned ships in the AIS archive", "OFAC-sanctioned hull × NOAA AIS archive (US-coastal), joined on IMO"),
    "sanctioned_vessel_broadcasting_v2": ("Sanctioned ships in the AIS archive (OFAC ∪ OpenSanctions)", "Sanctioned hull (OFAC ∪ OpenSanctions) × NOAA AIS archive (US-coastal), joined on IMO"),
    "debarred_but_funded":               ("Debarred firms holding federal contract awards", "SAM debarment × USASpending awards, joined on UEI"),
}

def verify_url(ktype, kval):
    k = (ktype or "").upper(); v = html.escape(str(kval or ""))
    if k == "NPI": return f"https://npiregistry.cms.hhs.gov/provider-view/{v}"
    if k == "IMO": return f"https://www.marinetraffic.com/en/ais/details/ships/imo:{v}"
    if k == "UEI": return f"https://sam.gov/search/?keywords={v}"
    return ""

def evidence_str(ev_json):
    try:
        arr = json.loads(ev_json) if ev_json else []
    except Exception:
        return ""
    bits = []
    for o in arr[:8]:
        if not isinstance(o, dict): continue
        # prefer the human label, else first non-id string
        lab = o.get("facility") or o.get("recipient_name") or o.get("ais_name")
        if not lab:
            for kk, vv in o.items():
                if isinstance(vv, str) and vv and kk not in ("ccn", "key", "uei", "npi", "imo"):
                    lab = vv; break
        if lab: bits.append(str(lab))
    seen = list(dict.fromkeys(bits))
    s = " · ".join(seen[:6])
    return s + (f"  (+{len(arr)-6} more)" if len(arr) > 6 else "")

# ---------------------------------------------------------------- LIBRARY (catalog + sampled DQ)
srcs = db.dicts(c, """
    SELECT source_id, name, domain_primary, lifecycle, landed_row_count,
           ARRAY_TO_STRING(join_keys_std,', ') keys, join_key_tier
    FROM LIBRARY_META.REGISTRY.CATALOG
    WHERE lifecycle IN ('landed','modeled') ORDER BY landed_row_count DESC NULLS LAST""")
srcs = [{k.lower(): v for k, v in r.items()} for r in srcs]   # Snowflake returns UPPER keys

# columns per landing table (one round-trip)
colmap = {}
for sid, col in db.rows(c, """SELECT table_name, column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
                              WHERE table_schema='LANDING' ORDER BY ordinal_position"""):
    colmap.setdefault(sid, []).append(col)

def data_quality(sid):
    t = sid.upper(); cols = [x for x in colmap.get(t, []) if x not in META]
    if not cols: return ("?", 0, 0)
    pred = " AND ".join(f'(NULLIF(TRIM("{x}"),\'\') IS NULL)' for x in cols)
    sel = ",".join(f'COUNT_IF(NULLIF(TRIM("{x}"),\'\') IS NOT NULL)' for x in cols)
    try:
        r = db.rows(c, f"SELECT COUNT(*), COUNT_IF({pred}), {sel} FROM LIBRARY_RAW.LANDING.{t} SAMPLE (500 ROWS)")[0]
        n, blank, pops = r[0], r[1], r[2:]
        if not n: return ("EMPTY", 0, len(cols))
        popn = sum(1 for p in pops if p > 0)
        if blank / n > 0.95 or popn == 0: return ("EMPTY", popn, len(cols))
        if popn < max(3, len(cols) * 0.5): return ("PARTIAL", popn, len(cols))
        return ("OK", popn, len(cols))
    except Exception:
        return ("?", 0, len(cols))

for s in srcs:
    dq, popn, ncol = data_quality(s["source_id"])
    s["dq"], s["popn"], s["ncol"] = dq, popn, ncol

# ---------------------------------------------------------------- DOMAINS
doms = db.dicts(c, "SELECT domain, sources_primary, landed, total_rows FROM LIBRARY_META.REGISTRY.V_DOMAIN_SUMMARY ORDER BY landed DESC, sources_primary DESC")
doms = [{k.lower(): v for k, v in r.items()} for r in doms]
asof = db.rows(c, "SELECT CURRENT_TIMESTAMP()::DATE")[0][0]
c.close()

# ---------------------------------------------------------------- stat tiles
n_loaded = sum(1 for s in srcs if s["dq"] == "OK")
n_broken = sum(1 for s in srcs if s["dq"] in ("EMPTY", "PARTIAL"))
n_rows   = sum(int(s["landed_row_count"] or 0) for s in srcs if s["dq"] == "OK")
n_ins    = len(leads)

# ---------------------------------------------------------------- render
e = html.escape
def fmt(n):
    try: return f"{int(n):,}"
    except Exception: return ""

rows_ins = []
for L in leads:
    lab, how = RULE_LABEL.get(L["RULE_NAME"], (L["RULE_NAME"], ""))
    vu = verify_url(L["LEFT_KEY_TYPE"], L["LEFT_KEY_VALUE"])
    vlink = f'<a href="{vu}" target="_blank">verify ↗</a>' if vu else ""
    sc = float(L["SCORE"] or 0)
    bar = f'<div class="bar"><div class="fill" style="width:{int(sc*100)}%"></div></div>'
    stale = "" if L["STATUS"] == "active" else ' <span class="tag stale">stale</span>'
    rows_ins.append(f"""<tr data-rule="{e(L['RULE_NAME'])}">
      <td><span class="chip c-{e(L['RULE_NAME'])}">{e(lab)}</span></td>
      <td class="t">{e(L['TITLE'])}{stale}</td>
      <td>{bar}<span class="muted">{sc:.2f}</span></td>
      <td class="ev">{e(evidence_str(L['EV']))}</td>
      <td class="vk"><span class="muted">{e(L['LEFT_KEY_TYPE'])}: {e(L['LEFT_KEY_VALUE'])}</span><br>{vlink}</td>
    </tr>""")

dqcolor = {"OK": "ok", "PARTIAL": "warn", "EMPTY": "bad", "?": "muted"}
rows_lib = []
for s in srcs:
    dq = s["dq"]
    rows_lib.append(f"""<tr>
      <td>{e(s['domain_primary'] or '')}</td>
      <td class="t">{e(s['name'] or s['source_id'])}<br><span class="muted">{e(s['source_id'])}</span></td>
      <td>{e(s['lifecycle'])}</td>
      <td class="num">{fmt(s['landed_row_count'])}</td>
      <td><span class="tag {dqcolor.get(dq,'muted')}">{dq}</span> <span class="muted">{s['popn']}/{s['ncol']} cols</span></td>
      <td class="muted">{e(s['keys'] or '')}</td>
    </tr>""")

maxd = max((int(d["sources_primary"] or 0) for d in doms), default=1)
rows_dom = []
for d in doms:
    sp = int(d["sources_primary"] or 0); ld = int(d["landed"] or 0)
    w = int(100 * sp / maxd)
    rows_dom.append(f"""<tr>
      <td class="t">{e(d['domain'])}</td>
      <td style="width:55%"><div class="dbar"><div class="dfill" style="width:{w}%"></div>
        <div class="dfill ld" style="width:{int(100*ld/maxd)}%"></div></div></td>
      <td class="num">{sp} <span class="muted">src</span></td>
      <td class="num">{ld} <span class="muted">loaded</span></td>
      <td class="num muted">{fmt(d['total_rows'])} rows</td>
    </tr>""")

HTML = f"""<!doctype html><html><head><meta charset="utf-8">
<title>Ripple — backend</title>
<style>
:root{{--bg:#0d1117;--panel:#161b22;--line:#21262d;--tx:#c9d1d9;--mut:#6e7681;--ac:#2f81f7;--ok:#3fb950;--warn:#d29922;--bad:#f85149}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--tx);font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif}}
.wrap{{max-width:1180px;margin:0 auto;padding:28px 20px 80px}}
h1{{font-size:22px;margin:0 0 2px}} h2{{font-size:15px;margin:34px 0 10px;color:#fff}}
.sub{{color:var(--mut);font-size:12px;margin-bottom:18px}}
.tiles{{display:flex;gap:12px;flex-wrap:wrap;margin:18px 0}}
.tile{{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px 18px;min-width:150px}}
.tile .n{{font-size:26px;font-weight:700;color:#fff}} .tile .l{{color:var(--mut);font-size:12px}}
table{{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}}
th,td{{text-align:left;padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top;font-size:13px}}
th{{color:var(--mut);font-weight:600;cursor:pointer;user-select:none;position:sticky;top:0;background:var(--panel)}}
tr:last-child td{{border-bottom:none}} tr:hover td{{background:#1b2230}}
.t{{color:#e6edf3}} .num{{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}}
.muted{{color:var(--mut);font-size:12px}} .ev{{color:#adbac7;font-size:12px;max-width:330px}}
.vk{{white-space:nowrap}} a{{color:var(--ac);text-decoration:none}} a:hover{{text-decoration:underline}}
.bar{{display:inline-block;width:60px;height:6px;background:#30363d;border-radius:3px;overflow:hidden;vertical-align:middle;margin-right:6px}}
.fill{{height:100%;background:var(--ac)}}
.tag{{display:inline-block;padding:1px 7px;border-radius:20px;font-size:11px;font-weight:600}}
.tag.ok{{background:rgba(63,185,80,.15);color:var(--ok)}} .tag.warn{{background:rgba(210,153,34,.15);color:var(--warn)}}
.tag.bad{{background:rgba(248,81,73,.15);color:var(--bad)}} .tag.stale{{background:rgba(210,153,34,.15);color:var(--warn)}}
.tag.muted{{background:#21262d;color:var(--mut)}}
.chip{{display:inline-block;padding:2px 9px;border-radius:6px;font-size:11px;font-weight:600;color:#fff}}
.c-banned_but_operating{{background:#8957e5}} .c-sanctioned_vessel_broadcasting{{background:#1f6feb}} .c-debarred_but_funded{{background:#bb4a1d}}
.c-banned_but_paid{{background:#2da44e}} .c-excluded_but_billing{{background:#d29922}} .c-sanctioned_vessel_broadcasting_v2{{background:#1a7f8e}}
.dbar{{position:relative;height:14px;background:#21262d;border-radius:4px}}
.dfill{{position:absolute;left:0;top:0;height:100%;background:#30475e;border-radius:4px}} .dfill.ld{{background:var(--ok)}}
input.f{{background:var(--panel);border:1px solid var(--line);color:var(--tx);border-radius:8px;padding:7px 11px;width:280px;margin-bottom:10px;font-size:13px}}
.note{{color:var(--mut);font-size:12px;margin:6px 0 0}}
</style></head><body><div class="wrap">
<h1>Ripple — your backend, at a glance</h1>
<div class="sub">as of {asof} · regenerate any time with <code>python3 scripts/build_dashboard.py</code> · every insight links out so you can check it yourself</div>

<div class="tiles">
  <div class="tile"><div class="n">{n_ins}</div><div class="l">live insights (detector hits)</div></div>
  <div class="tile"><div class="n">{n_loaded}</div><div class="l">sources with real data</div></div>
  <div class="tile"><div class="n" style="color:var(--bad)">{n_broken}</div><div class="l">loaded but empty/partial</div></div>
  <div class="tile"><div class="n">{fmt(n_rows)}</div><div class="l">real rows behind them</div></div>
</div>

<h2>① Your insights — what the detectors found</h2>
<div class="note">Each row is a cross-dataset hit on a hard ID (no name-guessing). Click <b>verify</b> to check it at the source.</div>
<input class="f" placeholder="filter insights… (e.g. hospital, vessel, debarred)" onkeyup="flt(this,'tIns')">
<table id="tIns"><thead><tr><th>Detector</th><th>Finding</th><th>Score</th><th>Evidence</th><th>Verify</th></tr></thead>
<tbody>{''.join(rows_ins)}</tbody></table>

<h2>② Your library — what data is actually in there</h2>
<div class="note"><span class="tag ok">OK</span> real data · <span class="tag warn">PARTIAL</span> some columns missing · <span class="tag bad">EMPTY</span> looks loaded but isn't (re-ingest). Sampled live.</div>
<input class="f" placeholder="filter sources… (e.g. cms, sanctions, vessel)" onkeyup="flt(this,'tLib')">
<table id="tLib"><thead><tr><th>Domain</th><th>Source</th><th>State</th><th>Rows</th><th>Data quality</th><th>Join keys</th></tr></thead>
<tbody>{''.join(rows_lib)}</tbody></table>

<h2>③ Your domains — coverage by topic</h2>
<div class="note">Bar = sources scouted/tagged; green = actually loaded.</div>
<table id="tDom"><thead><tr><th>Domain</th><th>Coverage</th><th>Sources</th><th>Loaded</th><th>Rows</th></tr></thead>
<tbody>{''.join(rows_dom)}</tbody></table>

<script>
function flt(inp,id){{var q=inp.value.toLowerCase();document.querySelectorAll('#'+id+' tbody tr').forEach(function(r){{r.style.display=r.innerText.toLowerCase().indexOf(q)>-1?'':'none';}});}}
document.querySelectorAll('th').forEach(function(th){{th.addEventListener('click',function(){{
 var tb=th.closest('table').querySelector('tbody'),i=[...th.parentNode.children].indexOf(th),
 rs=[...tb.rows],asc=th._asc=!th._asc;
 rs.sort(function(a,b){{var x=a.cells[i].innerText.replace(/[,$]/g,''),y=b.cells[i].innerText.replace(/[,$]/g,'');
 var nx=parseFloat(x),ny=parseFloat(y);if(!isNaN(nx)&&!isNaN(ny))return asc?nx-ny:ny-nx;
 return asc?x.localeCompare(y):y.localeCompare(x);}});rs.forEach(function(r){{tb.appendChild(r);}});}});}});
</script>
</div></body></html>"""

with open(OUT, "w") as f:
    f.write(HTML)
print(f"wrote {OUT}")
print(f"  {n_ins} insights · {n_loaded} OK sources · {n_broken} broken · {fmt(n_rows)} real rows")
