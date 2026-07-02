#!/usr/bin/env python3
"""Ripple backend window — a LIVE, clickable local view of the library + insights.

Stdlib only (no Flask/Streamlit — stays in-stack). Read-only against Snowflake.
  • Insights: every detector hit; click one -> the ACTUAL underlying rows (the ban
    record + the active rows it joined to).
  • Library: every loaded source; click -> 25 real sample rows + measured data quality.
  • Compare: pick two sources -> columns/rows/quality side by side + hard-key OVERLAP.
  • Connections: a map of what links to what (sources joined by shared hard IDs).

    python3 scripts/dashboard_server.py            # serves http://localhost:8765 (auto-opens)

Single short-lived process; ctrl-C to stop. Drill-ins/overlap are cached in-memory.
"""
import sys, json, threading, webbrowser, math
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

sys.path.insert(0, "c:/Code/Ripple_v6")
from connect import db, leads
from connect.keys import normalize_sql, quote_ident, NORM_RULES
from connect.leads_specs import JOBS

PORT = 8765
META = {"_INGESTED_AT", "_SOURCE_RUN_ID", "_SRC_SHA256"}
HARD = ["NPI", "EIN", "CCN", "UEI", "CIK", "IMO", "MMSI", "LEI", "DUNS"]  # real IDs (skip ZIP/NAME/FIPS)

# One label per rule in leads_specs.JOBS. Archive-honest copy: the AIS data is a
# US-coastal ARCHIVE, so "appears in" — never "broadcasting" / "still".
RULE_LABEL = {
    "banned_but_operating":              "Banned providers on facility rosters",
    "banned_but_paid":                   "Banned providers in Open Payments records",
    "excluded_but_billing":              "Banned providers in Part D prescriber records",
    "sanctioned_vessel_broadcasting":    "Sanctioned ships in the AIS archive",
    "sanctioned_vessel_broadcasting_v2": "Sanctioned ships in the AIS archive (OFAC ∪ OpenSanctions)",
    "debarred_but_funded":               "Debarred firms holding federal contract awards",
    "sec_filer_in_irs_bmf":              "SEC filers whose EIN appears in the IRS exempt-org roster",
}
# story-relevant columns for each detector's drill-in (left = the flag, right = the active
# rows). Rules whose right side is a staging view fall back to SELECT * (the column check
# only sees LIBRARY_RAW), which is fine at these row limits.
DETAIL = {
    "banned_but_operating": {
        "left":  ["LASTNAME", "FIRSTNAME", "EXCLTYPE", "EXCLDATE", "NPI", "STATE"],
        "right": ["PROVIDER_LAST_NAME", "PROVIDER_FIRST_NAME", "CCN", "FACILITY_TYPE"], "rlimit": 200},
    "banned_but_paid": {
        "left":  ["LASTNAME", "FIRSTNAME", "EXCLTYPE", "EXCLDATE", "NPI", "STATE"],
        "right": ["COVERED_RECIPIENT_LAST_NAME", "COVERED_RECIPIENT_FIRST_NAME",
                  "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME",
                  "NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE",
                  "TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS", "DATE_OF_PAYMENT", "PROGRAM_YEAR",
                  "NPI"], "rlimit": 200},
    "excluded_but_billing": {
        "left":  ["LASTNAME", "FIRSTNAME", "EXCLTYPE", "EXCLDATE", "WVRSTATE", "NPI", "STATE"],
        "right": ["PRSCRBR_LAST_ORG_NAME", "PRSCRBR_FIRST_NAME", "TOT_CLMS",
                  "TOT_DRUG_CST", "OPIOID_TOT_DRUG_CST", "NPI"], "rlimit": 200},
    "sanctioned_vessel_broadcasting": {
        "left":  ["SDN_NAME", "PROGRAM", "VESS_FLAG", "TONNAGE", "IMO"],
        "right": ["VESSELNAME", "BASEDATETIME", "LAT", "LON", "SOG", "IMO"], "rlimit": 150},
    "sanctioned_vessel_broadcasting_v2": {
        "left":  ["VESSEL_NAME", "SANCTION_SOURCE", "PROGRAM", "FLAG", "IMO"],
        "right": ["VESSELNAME", "BASEDATETIME", "LAT", "LON", "SOG", "IMO"], "rlimit": 150},
    "debarred_but_funded": {
        "left":  ["ENTITY_NAME", "CLASSIFICATION", "EXCLUSION_TYPE", "EXCLUDING_AGENCY", "UEI"],
        "right": ["RECIPIENT_NAME", "AWARDING_AGENCY_NAME", "FEDERAL_ACTION_OBLIGATION",
                  "ACTION_DATE", "AWARD_ID_PIID", "RECIPIENT_UEI"], "rlimit": 300},
    "sec_filer_in_irs_bmf": {
        "left":  ["NAME", "CIK", "SIC", "FORM", "EIN"],
        "right": ["NAME", "CITY", "STATE", "SUBSECTION", "NTEE_CD", "EIN"], "rlimit": 300},
}

# ----------------------------------------------------------------- db (1 conn + lock)
_lock = threading.Lock(); _conn = None
def _c():
    global _conn
    if _conn is None or _conn.is_closed():
        _conn = db.connect()
    return _conn
def q(sql, params=None):
    with _lock:
        for attempt in (0, 1):
            try:
                cur = _c().cursor()
                try:
                    cur.execute(sql, params or ())
                    cols = [d[0] for d in cur.description] if cur.description else []
                    return cols, cur.fetchall()
                finally:
                    cur.close()
            except Exception:
                global _conn
                _conn = None
                if attempt: raise
def qd(sql, params=None):
    cols, rows = q(sql, params)
    return [dict(zip(cols, r)) for r in rows]

_cache = {}
def cached(key, fn):
    if key not in _cache: _cache[key] = fn()
    return _cache[key]

# ----------------------------------------------------------------- data
def _published():
    """THE safety chokepoint: every insights read routes through leads.published() —
    STATUS='active' plus the DECISIONS anti-join — so a rejected / retracted / stale
    lead can never render here. Same retry-once-on-dead-connection dance as q()."""
    global _conn
    with _lock:
        for attempt in (0, 1):
            try:
                return leads.published(_c())
            except Exception:
                _conn = None
                if attempt: raise

def _shape_insight(r):
    """PURE (no DB): one gated LEADS row (UPPER keys, EVIDENCE as JSON text) -> API dict."""
    try: ev = json.loads(r.get("EVIDENCE") or "[]")
    except Exception: ev = []
    labels = []
    for o in ev[:10]:
        if isinstance(o, dict):
            v = o.get("facility") or o.get("recipient_name") or o.get("ais_name")
            if not v:
                for kk, vv in o.items():
                    if isinstance(vv, str) and vv and kk not in ("ccn", "uei", "npi", "imo", "key"):
                        v = vv; break
            if v: labels.append(str(v))
    return {"lead_id": r["LEAD_ID"], "rule": r["RULE_NAME"],
            "label": RULE_LABEL.get(r["RULE_NAME"], r["RULE_NAME"]),
            "key_type": r["LEFT_KEY_TYPE"], "key_value": r["LEFT_KEY_VALUE"],
            "title": r["TITLE"], "score": float(r["SCORE"] or 0),
            "status": r.get("STATUS") or "active",
            "review": r.get("REVIEW_STATE", "pending"),
            "published": bool(r.get("PUBLISHED", False)),
            "evidence": list(dict.fromkeys(labels))}

def insights():
    rows = sorted(_published(), key=lambda r: (r["RULE_NAME"], -float(r["SCORE"] or 0)))
    return [_shape_insight(r) for r in rows]

def _sel(table, cols):
    have = {c for c, in q(f"""SELECT column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
                              WHERE table_schema='LANDING' AND table_name='{table}'""")[1]}
    return [c for c in cols if c in have] or ["*"]

def insight_detail(lead_id):
    # The libel firewall applies to the drill-in too: a rejected / retracted / stale lead's
    # detail page must refuse to render — even from cache. The gate is checked FRESH on
    # every call (verdicts flip between clicks); only a lead that passes gets the cached
    # row fetch, and the cache key carries the review state so a later verdict flip can
    # never be served a page cached under the old one.
    lead = next((r for r in _published() if r["LEAD_ID"] == lead_id), None)
    if lead is None:
        return {"error": "lead not available — unpublished, stale, or suppressed by review"}
    rule, val, title = lead["RULE_NAME"], lead["LEFT_KEY_VALUE"], lead["TITLE"]
    if rule not in JOBS:
        return {"error": f"no live spec for rule {rule}"}
    def build():
        spec, det = JOBS[rule], DETAIL.get(rule, {})
        def side(S, cols, limit):
            tbl, kc, key = S["table"], S["key_col"], S["key"]
            sel = ", ".join(quote_ident(x) for x in _sel(tbl, cols)) if cols else "*"
            pred = f"{normalize_sql(key, quote_ident(kc))} = %s"
            c2, rows = q(f"SELECT {sel} FROM {db.fqn(tbl)} WHERE {pred} LIMIT {limit}", (val,))
            return {"table": tbl, "cols": c2, "rows": [[("" if v is None else str(v)) for v in row] for row in rows]}
        return {"title": title, "rule": rule, "review": lead.get("REVIEW_STATE", "pending"),
                "left": side(spec["left"], det.get("left"), 10),
                "right": side(spec["right"], det.get("right"), det.get("rlimit", 100))}
    return cached(f"ins:{lead_id}:{lead.get('REVIEW_STATE', 'pending')}", build)

def library():
    rows = qd("""SELECT source_id, name, domain_primary, lifecycle, landed_row_count,
                        ARRAY_TO_STRING(join_keys_std,', ') keys, join_key_tier
                 FROM LIBRARY_META.REGISTRY.CATALOG WHERE lifecycle IN ('landed','modeled')
                 ORDER BY landed_row_count DESC NULLS LAST""")
    return [{k.lower(): v for k, v in r.items()} for r in rows]

def _colmap():
    def build():
        m = {}
        for sid, col in q("""SELECT table_name, column_name FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS
                             WHERE table_schema='LANDING' ORDER BY ordinal_position""")[1]:
            m.setdefault(sid, []).append(col)
        return m
    return cached("colmap", build)

def data_quality():
    def build():
        out = {}
        for s in library():
            t = s["source_id"].upper(); cols = [x for x in _colmap().get(t, []) if x not in META]
            if not cols: out[s["source_id"]] = {"dq": "?", "popn": 0, "ncol": 0}; continue
            pred = " AND ".join(f'(NULLIF(TRIM("{x}"),\'\') IS NULL)' for x in cols)
            sel = ",".join(f'COUNT_IF(NULLIF(TRIM("{x}"),\'\') IS NOT NULL)' for x in cols)
            try:
                r = q(f"SELECT COUNT(*),COUNT_IF({pred}),{sel} FROM LIBRARY_RAW.LANDING.{t} SAMPLE (500 ROWS)")[1][0]
                n, blank, pops = r[0], r[1], r[2:]
                popn = sum(1 for p in pops if p > 0)
                dq = "EMPTY" if (not n or blank / n > 0.95 or popn == 0) else \
                     ("PARTIAL" if popn < max(3, len(cols) * 0.5) else "OK")
                out[s["source_id"]] = {"dq": dq, "popn": popn, "ncol": len(cols)}
            except Exception:
                out[s["source_id"]] = {"dq": "?", "popn": 0, "ncol": len(cols)}
        return out
    return cached("dq", build)

def source_detail(sid):
    t = sid.upper(); cols = [x for x in _colmap().get(t, []) if x not in META][:30]
    sel = ", ".join(quote_ident(x) for x in cols) or "*"
    c2, rows = q(f"SELECT {sel} FROM {db.fqn(t)} SAMPLE (25 ROWS)")
    cnt = q(f"SELECT COUNT(*) FROM {db.fqn(t)}")[1][0][0]
    return {"sid": sid, "count": cnt, "cols": c2,
            "rows": [[("" if v is None else str(v)) for v in r] for r in rows]}

def compare(a, b):
    def one(sid):
        t = sid.upper(); cols = [x for x in _colmap().get(t, []) if x not in META]
        cnt = q(f"SELECT COUNT(*) FROM {db.fqn(t)}")[1][0][0]
        m = qd("""SELECT domain_primary d, ARRAY_TO_STRING(join_keys_std,', ') k, join_key_tier t
                  FROM LIBRARY_META.REGISTRY.CATALOG WHERE source_id=%s""", (sid,))
        m = m[0] if m else {"D": "", "K": "", "T": ""}
        keys = [x.strip() for x in (m["K"] or "").split(",") if x.strip()]
        return {"sid": sid, "domain": m["D"], "rows": cnt, "ncol": len(cols), "keys": keys, "tier": m["T"]}
    A, B = one(a), one(b)
    shared = []
    for key in [k for k in A["keys"] if k in B["keys"] and k in NORM_RULES]:
        ta, tb = a.upper(), b.upper()
        kca = [x for x in _colmap().get(ta, []) if x.upper() == key.upper() or x.upper().endswith("__" + key) or key in x.upper()]
        kcb = [x for x in _colmap().get(tb, []) if x.upper() == key.upper() or x.upper().endswith("__" + key) or key in x.upper()]
        if not kca or not kcb: continue
        na, nb = normalize_sql(key, quote_ident(kca[0])), normalize_sql(key, quote_ident(kcb[0]))
        try:
            ov = q(f"""WITH x AS (SELECT DISTINCT {na} v FROM {db.fqn(ta)} WHERE {na} IS NOT NULL),
                            y AS (SELECT DISTINCT {nb} v FROM {db.fqn(tb)} WHERE {nb} IS NOT NULL)
                       SELECT (SELECT COUNT(*) FROM x),(SELECT COUNT(*) FROM y),
                              (SELECT COUNT(*) FROM x JOIN y USING(v))""")[1][0]
            shared.append({"key": key, "a_distinct": ov[0], "b_distinct": ov[1], "overlap": ov[2]})
        except Exception:
            shared.append({"key": key, "a_distinct": None, "b_distinct": None, "overlap": None})
    return {"a": A, "b": B, "shared": shared}

def links():
    def build():
        rows = qd("""SELECT k.source_id sid, k.join_key key, c.domain_primary dom
                     FROM LIBRARY_META.REGISTRY.V_SOURCE_KEY k
                     JOIN LIBRARY_META.REGISTRY.CATALOG c USING(source_id)
                     WHERE c.lifecycle IN ('landed','modeled') AND k.join_key IN ({})"""
                  .format(",".join("'%s'" % h for h in HARD)))
        bykey = {}; dom = {}; nodes = {}
        for r in rows:
            bykey.setdefault(r["KEY"], set()).add(r["SID"])
            dom[r["SID"]] = r["DOM"]; nodes.setdefault(r["SID"], set())
        edges = {}
        for key, srcs in bykey.items():
            srcs = sorted(srcs)
            for i in range(len(srcs)):
                for j in range(i + 1, len(srcs)):
                    p = (srcs[i], srcs[j]); edges.setdefault(p, set()).add(key)
                    nodes[srcs[i]].add(srcs[j]); nodes[srcs[j]].add(srcs[i])
        # circular layout grouped by domain (deterministic, no networkx)
        doms = sorted(set(dom.values())); di = {d: k for k, d in enumerate(doms)}
        byd = {}
        for s in nodes: byd.setdefault(dom[s], []).append(s)
        pos = {}
        for d, ss in byd.items():
            cx, cy = math.cos(2 * math.pi * di[d] / max(len(doms), 1)), math.sin(2 * math.pi * di[d] / max(len(doms), 1))
            for k, s in enumerate(sorted(ss)):
                a = 2 * math.pi * k / max(len(ss), 1)
                pos[s] = (cx * 3 + math.cos(a) * 0.9, cy * 3 + math.sin(a) * 0.9)
        N = [{"id": s, "x": pos[s][0], "y": pos[s][1], "domain": dom[s], "deg": len(nodes[s])} for s in nodes]
        E = [{"a": a, "b": b, "keys": sorted(ks)} for (a, b), ks in edges.items()]
        return {"nodes": N, "edges": E}
    return cached("links", build)

# ----------------------------------------------------------------- HTTP
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(200); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b))); self.end_headers(); self.wfile.write(b)
    def do_GET(self):
        u = urlparse(self.path); p = u.path; qs = parse_qs(u.query)
        try:
            if p == "/" or p == "/index.html": return self._send(PAGE_HTML, "text/html; charset=utf-8")
            if p == "/api/insights": return self._send(json.dumps(insights()))
            if p == "/api/insight": return self._send(json.dumps(insight_detail(qs["id"][0])))
            if p == "/api/library": return self._send(json.dumps(library()))
            if p == "/api/dq": return self._send(json.dumps(data_quality()))
            if p == "/api/source": return self._send(json.dumps(source_detail(qs["sid"][0])))
            if p == "/api/compare": return self._send(json.dumps(compare(qs["a"][0], qs["b"][0])))
            if p == "/api/links": return self._send(json.dumps(links()))
            self.send_response(404); self.end_headers()
        except Exception as ex:
            self._send(json.dumps({"error": str(ex)[:300]}))

PAGE_HTML = r"""<!doctype html><html><head><meta charset="utf-8"><title>Ripple — backend</title>
<script src="https://cdn.plot.ly/plotly-2.30.0.min.js"></script>
<style>
:root{--bg:#0d1117;--panel:#161b22;--line:#21262d;--tx:#c9d1d9;--mut:#6e7681;--ac:#2f81f7;--ok:#3fb950;--warn:#d29922;--bad:#f85149}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--tx);font:14px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:22px 20px 80px}h1{font-size:21px;margin:0}
nav{display:flex;gap:8px;margin:16px 0 18px}nav button{background:var(--panel);border:1px solid var(--line);color:var(--tx);padding:8px 16px;border-radius:8px;cursor:pointer;font-size:13px}
nav button.on{background:var(--ac);color:#fff;border-color:var(--ac)}
.sub{color:var(--mut);font-size:12px}section{display:none}section.on{display:block}
table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:10px;overflow:hidden}
th,td{text-align:left;padding:8px 11px;border-bottom:1px solid var(--line);font-size:13px;vertical-align:top}
th{color:var(--mut);cursor:pointer;position:sticky;top:0;background:var(--panel)}tr:last-child td{border-bottom:none}
tbody tr{cursor:pointer}tbody tr:hover td{background:#1b2230}.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.muted{color:var(--mut);font-size:12px}.t{color:#e6edf3}a{color:var(--ac);text-decoration:none}a:hover{text-decoration:underline}
.tag{display:inline-block;padding:1px 7px;border-radius:20px;font-size:11px;font-weight:600}
.ok{background:rgba(63,185,80,.15);color:var(--ok)}.warn{background:rgba(210,153,34,.15);color:var(--warn)}.bad{background:rgba(248,81,73,.15);color:var(--bad)}
.chip{display:inline-block;padding:2px 9px;border-radius:6px;font-size:11px;font-weight:600;color:#fff}
.c-banned_but_operating{background:#8957e5}.c-sanctioned_vessel_broadcasting{background:#1f6feb}.c-debarred_but_funded{background:#bb4a1d}
.c-banned_but_paid{background:#2da44e}.c-excluded_but_billing{background:#d29922}.c-sanctioned_vessel_broadcasting_v2{background:#1a7f8e}
.bar{display:inline-block;width:54px;height:6px;background:#30363d;border-radius:3px;overflow:hidden;vertical-align:middle;margin-right:6px}.fill{height:100%;background:var(--ac)}
input.f,select{background:var(--panel);border:1px solid var(--line);color:var(--tx);border-radius:8px;padding:7px 11px;font-size:13px}input.f{width:300px;margin-bottom:10px}
#ov{position:fixed;inset:0;background:rgba(0,0,0,.6);display:none;z-index:9}#mod{position:fixed;top:4%;left:50%;transform:translateX(-50%);width:min(1100px,94vw);max-height:90vh;overflow:auto;background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:20px;z-index:10;display:none}
#mod h3{margin:2px 0 4px}.x{float:right;cursor:pointer;color:var(--mut);font-size:20px}
.dt{font-size:12px}.dt td,.dt th{padding:5px 8px}
.note{color:var(--mut);font-size:12px;margin:4px 0 10px}.flex{display:flex;gap:18px}.flex>div{flex:1}
.kpill{display:inline-block;background:#21262d;border-radius:6px;padding:2px 8px;margin:2px;font-size:12px}
</style></head><body><div class="wrap">
<h1>Ripple — your backend, live</h1>
<div class="sub">click any row to drill into the real data · everything read-only · localhost only</div>
<nav>
 <button class="on" onclick="tab('ins',this)">① Insights</button>
 <button onclick="tab('lib',this)">② Library</button>
 <button onclick="tab('cmp',this)">③ Compare</button>
 <button onclick="tab('lnk',this)">④ Connections</button>
</nav>

<section id="ins" class="on">
 <div class="note">Each row is a cross-dataset hit on a hard ID. <b>Click a row</b> to see the ban record + the active rows it matched.</div>
 <input class="f" placeholder="filter insights…" onkeyup="flt(this,'tIns')">
 <table id="tIns"><thead><tr><th>Detector</th><th>Finding</th><th>Score</th><th>Key</th></tr></thead><tbody></tbody></table>
</section>

<section id="lib">
 <div class="note"><span class="tag ok">OK</span> real · <span class="tag warn">PARTIAL</span> thin · <span class="tag bad">EMPTY</span> broken. <b>Click a source</b> for 25 live sample rows.</div>
 <input class="f" placeholder="filter sources…" onkeyup="flt(this,'tLib')">
 <table id="tLib"><thead><tr><th>Domain</th><th>Source</th><th>State</th><th>Rows</th><th>Quality</th><th>Keys</th></tr></thead><tbody></tbody></table>
</section>

<section id="cmp">
 <div class="note">Pick two sources — see them side by side and how many entities they actually <b>share</b> on a hard ID.</div>
 <div class="flex" style="align-items:end;margin-bottom:14px">
  <div><div class="muted">Source A</div><select id="cA" style="width:100%"></select></div>
  <div><div class="muted">Source B</div><select id="cB" style="width:100%"></select></div>
  <div style="flex:0"><button onclick="doCompare()" style="padding:8px 16px;background:var(--ac);border:none;color:#fff;border-radius:8px;cursor:pointer">Compare</button></div>
 </div>
 <div id="cmpOut"></div>
</section>

<section id="lnk">
 <div class="note">Every dot is a loaded source; a line means they share a hard ID (so a detector can join them). <b>Click a dot</b> to see its links.</div>
 <div id="graph" style="height:560px;background:var(--panel);border:1px solid var(--line);border-radius:10px"></div>
 <div id="linkInfo" class="note"></div>
</section>
</div>

<div id="ov" onclick="closeM()"></div><div id="mod"><span class="x" onclick="closeM()">×</span><div id="modBody"></div></div>

<script>
var DQ={};
function tab(id,btn){document.querySelectorAll('section').forEach(s=>s.classList.remove('on'));document.getElementById(id).classList.add('on');
 document.querySelectorAll('nav button').forEach(b=>b.classList.remove('on'));btn.classList.add('on');if(id==='lnk')drawGraph();}
function flt(inp,id){var v=inp.value.toLowerCase();document.querySelectorAll('#'+id+' tbody tr').forEach(r=>r.style.display=r.innerText.toLowerCase().includes(v)?'':'none');}
function esc(s){return (s==null?'':''+s).replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function tbl(cols,rows,cls){var h='<table class="'+(cls||'')+'"><thead><tr>'+cols.map(c=>'<th>'+esc(c)+'</th>').join('')+'</tr></thead><tbody>';
 h+=rows.map(r=>'<tr>'+r.map(v=>'<td>'+esc(v)+'</td>').join('')+'</tr>').join('')+'</tbody></table>';return h;}
function openM(html){document.getElementById('modBody').innerHTML=html;document.getElementById('ov').style.display='block';document.getElementById('mod').style.display='block';}
function closeM(){document.getElementById('ov').style.display='none';document.getElementById('mod').style.display='none';}

// INSIGHTS
fetch('/api/insights').then(r=>r.json()).then(d=>{
 var tb=document.querySelector('#tIns tbody');tb.innerHTML=d.map(L=>{
  var stale=L.status!=='active'?' <span class="tag warn">stale</span>':'';
  return '<tr onclick="drill(\''+L.lead_id+'\')"><td><span class="chip c-'+L.rule+'">'+esc(L.label)+'</span></td>'+
   '<td class="t">'+esc(L.title)+stale+'</td><td><span class="bar"><span class="fill" style="width:'+Math.round(L.score*100)+'%"></span></span><span class="muted">'+L.score.toFixed(2)+'</span></td>'+
   '<td class="muted">'+esc(L.key_type)+': '+esc(L.key_value)+'</td></tr>';}).join('');});
function drill(id){openM('<div class="muted">loading…</div>');fetch('/api/insight?id='+id).then(r=>r.json()).then(d=>{
 if(d.error){openM('error: '+d.error);return;}
 var h='<h3>'+esc(d.title)+'</h3><div class="note">The actual rows behind this hit — same entity on both sides.</div>';
 h+='<h4 style="color:#fff;margin:14px 0 4px">🚩 Flag record — '+esc(d.left.table)+'</h4>'+tbl(d.left.cols,d.left.rows,'dt');
 h+='<h4 style="color:#fff;margin:16px 0 4px">✅ Active records — '+esc(d.right.table)+' ('+d.right.rows.length+' shown)</h4>'+tbl(d.right.cols,d.right.rows,'dt');
 openM(h);});}

// LIBRARY
var LIB=[];
fetch('/api/library').then(r=>r.json()).then(d=>{LIB=d;
 var tb=document.querySelector('#tLib tbody');tb.innerHTML=d.map(s=>
  '<tr onclick="srcDrill(\''+s.source_id+'\')"><td>'+esc(s.domain_primary)+'</td><td class="t">'+esc(s.name||s.source_id)+'<br><span class="muted">'+esc(s.source_id)+'</span></td>'+
  '<td>'+esc(s.lifecycle)+'</td><td class="num">'+(s.landed_row_count==null?'':(+s.landed_row_count).toLocaleString())+'</td>'+
  '<td id="dq_'+s.source_id+'"><span class="muted">…</span></td><td class="muted">'+esc(s.keys||'')+'</td></tr>').join('');
 var opts=d.map(s=>'<option value="'+s.source_id+'">'+esc(s.source_id)+'</option>').join('');
 cA.innerHTML=opts;cB.innerHTML=opts;if(d[1])cB.value=d[1].source_id;
 fetch('/api/dq').then(r=>r.json()).then(dq=>{DQ=dq;for(var k in dq){var c=document.getElementById('dq_'+k);if(c){var x=dq[k];
   var cl=x.dq=='OK'?'ok':x.dq=='PARTIAL'?'warn':x.dq=='EMPTY'?'bad':'';c.innerHTML='<span class="tag '+cl+'">'+x.dq+'</span> <span class="muted">'+x.popn+'/'+x.ncol+'</span>';}}});});
function srcDrill(sid){openM('<div class="muted">loading 25 rows…</div>');fetch('/api/source?sid='+sid).then(r=>r.json()).then(d=>{
 openM('<h3>'+esc(sid)+'</h3><div class="note">'+(+d.count).toLocaleString()+' rows · showing 25 · first 30 cols</div>'+tbl(d.cols,d.rows,'dt'));});}

// COMPARE
function doCompare(){var a=cA.value,b=cB.value;document.getElementById('cmpOut').innerHTML='<div class="muted">comparing…</div>';
 fetch('/api/compare?a='+a+'&b='+b).then(r=>r.json()).then(d=>{
  function card(s){return '<div><h3>'+esc(s.sid)+'</h3><div class="muted">'+esc(s.domain)+' · tier '+esc(s.tier)+'</div>'+
   '<p>'+(+s.rows).toLocaleString()+' rows · '+s.ncol+' cols</p><div>'+s.keys.map(k=>'<span class="kpill">'+esc(k)+'</span>').join('')+'</div></div>';}
  var h='<div class="flex">'+card(d.a)+card(d.b)+'</div>';
  if(d.shared.length){h+='<h3 style="margin-top:18px">Shared hard IDs — how connected they really are</h3>';
   h+=tbl(['Key','A distinct','B distinct','OVERLAP'],d.shared.map(s=>[s.key,(s.a_distinct||0).toLocaleString(),(s.b_distinct||0).toLocaleString(),'<b style="color:var(--ok)">'+(s.overlap||0).toLocaleString()+'</b>']),'');}
  else h+='<p class="note">No shared hard ID — these two don\'t directly join (a detector couldn\'t link them on a hard key).</p>';
  document.getElementById('cmpOut').innerHTML=h;});}

// CONNECTIONS
var GG=null;
function drawGraph(){if(GG)return;GG={};fetch('/api/links').then(r=>r.json()).then(d=>{
 var pos={};d.nodes.forEach(n=>pos[n.id]=n);
 var doms=[...new Set(d.nodes.map(n=>n.domain))];var pal=['#2f81f7','#3fb950','#bb4a1d','#8957e5','#d29922','#1f6feb','#db61a2','#39c5cf','#f85149','#a371f7'];
 var col={};doms.forEach((x,i)=>col[x]=pal[i%pal.length]);
 var ex=[],ey=[];d.edges.forEach(e=>{ex.push(pos[e.a].x,pos[e.b].x,null);ey.push(pos[e.a].y,pos[e.b].y,null);});
 var et={x:ex,y:ey,mode:'lines',type:'scattergl',line:{color:'#30363d',width:1},hoverinfo:'none'};
 var nt={x:d.nodes.map(n=>n.x),y:d.nodes.map(n=>n.y),mode:'markers',type:'scattergl',
  text:d.nodes.map(n=>n.id+'  ('+n.deg+' links · '+n.domain+')'),hoverinfo:'text',
  marker:{size:d.nodes.map(n=>8+Math.min(n.deg,18)),color:d.nodes.map(n=>col[n.domain]),line:{color:'#0d1117',width:1}},customdata:d.nodes.map(n=>n.id)};
 var lay={paper_bgcolor:'#161b22',plot_bgcolor:'#161b22',showlegend:false,margin:{l:0,r:0,t:0,b:0},
  xaxis:{visible:false},yaxis:{visible:false},hoverlabel:{bgcolor:'#0d1117'}};
 Plotly.newPlot('graph',[et,nt],lay,{displayModeBar:false,responsive:true});
 document.getElementById('graph').on('plotly_click',function(ev){var id=ev.points[0].customdata;if(!id)return;
  var ns=d.edges.filter(e=>e.a==id||e.b==id).map(e=>{var o=e.a==id?e.b:e.a;return o+' <span class="muted">('+e.keys.join(', ')+')</span>';});
  document.getElementById('linkInfo').innerHTML='<b style="color:#fff">'+esc(id)+'</b> links to '+ns.length+': '+ns.join(' · ');});});}
</script></body></html>"""

if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), H)
    url = f"http://localhost:{PORT}"
    print(f"Ripple backend window → {url}  (ctrl-C to stop)")
    try: webbrowser.open(url)
    except Exception: pass
    srv.serve_forever()
