"""Compile the Library Data Dictionary — a standalone, double-clickable catalog.

Reads outputs/library.json (tables, edges, ladder) and
outputs/connect_fingerprints.json (per-table ID-column profiles) and writes
docs/library_dictionary.html: one self-contained file, no server, no network.

    python -m viz.compile_dictionary

What it is: the working data dictionary / catalog for all 1,043 tables.
Search anything, filter by shelf / presence / ID system, click a table for its
dossier (description, ID columns with fill rates, every verified link graded on
the ladder, an ER-style neighbourhood you can click through). The browser back
button works; every view is a #hash you can bookmark.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "library_dictionary.html")

# The Library's three inks (viz/palette.py) -- same meanings, same order.
LADDER_COLOUR = ["#fbc06a", "#eda748", "#d98d33", "#bd7327", "#9d5c1e", "#7d4818"]
STATE_COLOUR = ["#eef1f5", "#8fa0b5", "#5d6d80", "#41505f"]
STATE_NAME = ["Connected", "Measured, no match yet", "Nothing to match on yet", "Queued for charting"]
STATE_STORY = [
    "Has verified links -- part of the mesh.",
    "Carries a real ID and the search ran: nothing matched. A measured fact.",
    "No column works as a joinable ID yet. Getting a better column is the fix.",
    "Hasn't been through link discovery yet -- queued, not missed.",
]


def build_payload():
    with open(os.path.join(ROOT, "outputs", "library.json"), encoding="utf-8") as f:
        lib = json.load(f)
    with open(os.path.join(ROOT, "outputs", "connect_fingerprints.json"), encoding="utf-8") as f:
        fp = json.load(f)

    tables = []
    for t in lib["tables"]:
        cols = []
        for k in fp.get(t["n"], {}).get("keys", []):
            cols.append({
                "c": k.get("column"), "k": k.get("key"), "t": k.get("tier"),
                "p": round(k.get("populated_pct") or 0, 1),
                "d": k.get("distinct"), "nn": k.get("nonnull"),
                "lo": _clip(k.get("min")), "hi": _clip(k.get("max")),
            })
        cols.sort(key=lambda c: -(c["p"] or 0))
        tables.append({
            "n": t["n"], "desc": t.get("desc") or "", "dom": t.get("dom") or "UNFILED",
            "rows": t.get("rows") or 0, "state": t["state"], "keys": t.get("keys") or [],
            "cols": cols,
        })

    edges = [[e[0], e[1], e[2], e[3]] for e in lib["edges"]]
    payload = {
        "tables": tables,
        "edges": edges,
        "ladder": [{"name": l[0], "gloss": l[1]} for l in lib["ladder_labels"]],
        "stages": [{"label": s["label"], "count": s["count"], "role": s["role"]} for s in lib["stages"]],
        "meta": lib["meta"],
    }
    return payload


def _clip(v, n=42):
    if v is None:
        return None
    v = str(v)
    return v if len(v) <= n else v[: n - 1] + "…"


def main():
    payload = build_payload()
    blob = json.dumps(payload, separators=(",", ":"))
    html = TEMPLATE.replace("/*__PALETTE__*/", json.dumps({
        "ladder": LADDER_COLOUR, "state": STATE_COLOUR,
        "stateName": STATE_NAME, "stateStory": STATE_STORY,
    })).replace("/*__DATA__*/", blob)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    n_cols = sum(len(t["cols"]) for t in payload["tables"])
    print(f"wrote {OUT} ({os.path.getsize(OUT)/1024/1024:.1f} MB) -- "
          f"{len(payload['tables'])} tables, {len(payload['edges'])} links, {n_cols} profiled columns")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>The Library — Data Dictionary</title>
<style>
  :root{
    --surface:#0d1117; --panel:#0f1620; --panel2:#121a24; --panel3:#17202c;
    --ink:#e8eaed; --ink2:#9aa4b2; --ink3:#6b7684; --rule:rgba(255,255,255,.10);
    --amber:#eda748; --blue:#6da7ec;
  }
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{height:100%}
  body{background:var(--surface);color:var(--ink);
    font:14px/1.5 ui-sans-serif,system-ui,"Segoe UI",sans-serif;overflow:hidden}
  .mono{font-family:ui-monospace,Consolas,monospace}
  ::selection{background:rgba(237,167,72,.35)}

  /* ---------- frame: topbar / sidebar / main ---------- */
  #app{display:grid;grid-template-rows:auto 1fr;height:100vh}
  #topbar{display:flex;align-items:center;gap:14px;padding:10px 16px;
    background:var(--panel);border-bottom:1px solid var(--rule);flex-wrap:wrap}
  #topbar h1{font-size:15px;font-weight:600;letter-spacing:.04em;white-space:nowrap;cursor:pointer}
  #topbar h1 span{color:var(--amber)}
  #q{flex:1 1 260px;max-width:520px;background:var(--panel3);border:1px solid var(--rule);
    border-radius:6px;color:var(--ink);padding:7px 12px;font-size:14px;outline:none}
  #q:focus{border-color:var(--amber)}
  select{background:var(--panel3);border:1px solid var(--rule);border-radius:6px;
    color:var(--ink2);padding:6px 8px;font-size:12.5px;outline:none;max-width:170px}
  #count{font-size:12px;color:var(--ink3);white-space:nowrap;margin-left:auto}
  #body{display:grid;grid-template-columns:340px 1fr;min-height:0}
  @media(max-width:900px){#body{grid-template-columns:1fr}#main{display:none}}

  /* ---------- results list ---------- */
  #list{overflow-y:auto;border-right:1px solid var(--rule);background:var(--panel)}
  .row{padding:8px 14px;border-bottom:1px solid rgba(255,255,255,.04);cursor:pointer;display:flex;gap:10px;align-items:baseline}
  .row:hover{background:var(--panel2)}
  .row.sel{background:var(--panel3);box-shadow:inset 3px 0 0 var(--amber)}
  .dot{width:8px;height:8px;border-radius:50%;flex:none;align-self:center}
  .row .nm{font-family:ui-monospace,Consolas,monospace;font-size:12.5px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;flex:1}
  .row .meta{font-size:11px;color:var(--ink3);white-space:nowrap}
  .row .lk{color:var(--amber)}
  #more{padding:10px 14px;color:var(--ink3);font-size:12px}

  /* ---------- main / dossier ---------- */
  #main{overflow-y:auto;padding:22px 28px}
  .crumb{font-size:12px;color:var(--ink3);margin-bottom:10px}
  .crumb a{color:var(--blue);text-decoration:none;cursor:pointer}
  h2.tname{font-family:ui-monospace,Consolas,monospace;font-size:20px;font-weight:600;word-break:break-all}
  .badges{display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 6px}
  .badge{font-size:11.5px;padding:3px 10px;border-radius:999px;border:1px solid var(--rule);color:var(--ink2);background:var(--panel2)}
  .badge b{color:var(--ink);font-weight:600}
  .desc{color:var(--ink2);max-width:78ch;margin:8px 0 4px}
  .story{color:var(--ink3);font-size:12.5px;max-width:78ch}
  h3.sect{font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink3);
    margin:26px 0 10px;border-bottom:1px solid var(--rule);padding-bottom:6px}
  h3.sect .n{color:var(--amber)}

  table.cols{border-collapse:collapse;width:100%;font-size:12.5px}
  table.cols th{font-size:10.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink3);
    text-align:left;padding:5px 12px 5px 0;font-weight:500;white-space:nowrap}
  table.cols td{padding:5px 12px 5px 0;border-top:1px solid rgba(255,255,255,.05);vertical-align:top}
  table.cols td.c{font-family:ui-monospace,Consolas,monospace;color:var(--ink)}
  table.cols td.k{color:var(--blue);white-space:nowrap}
  table.cols td.num{font-variant-numeric:tabular-nums;white-space:nowrap}
  table.cols td.rng{color:var(--ink3);font-family:ui-monospace,Consolas,monospace;font-size:11px}
  .fill{display:inline-block;width:54px;height:5px;border-radius:3px;background:var(--panel3);
    vertical-align:middle;margin-right:6px;overflow:hidden}
  .fill i{display:block;height:100%;background:var(--blue)}
  .lowfill i{background:#7a5a2f}

  /* links */
  .linkgrp{margin-bottom:6px}
  .neigh{display:flex;gap:10px;align-items:baseline;padding:6px 0;border-top:1px solid rgba(255,255,255,.05);flex-wrap:wrap}
  .neigh a{font-family:ui-monospace,Consolas,monospace;font-size:12.5px;color:var(--ink);
    text-decoration:none;cursor:pointer}
  .neigh a:hover{color:var(--amber)}
  .grade{font-size:10.5px;padding:2px 8px;border-radius:999px;color:#1a1206;font-weight:600;white-space:nowrap}
  .gkey{font-family:ui-monospace,Consolas,monospace;font-size:11px;color:var(--ink3)}
  .neigh .nrows{margin-left:auto;font-size:11px;color:var(--ink3);white-space:nowrap}

  /* ego diagram */
  #ego{background:var(--panel);border:1px solid var(--rule);border-radius:8px;margin-top:6px}
  #ego text{font-family:ui-monospace,Consolas,monospace;fill:var(--ink2);cursor:pointer}
  #ego text:hover{fill:var(--amber)}
  #ego .ctr{fill:var(--ink);font-weight:600;cursor:default}

  /* overview */
  .stats{display:flex;gap:34px;flex-wrap:wrap;margin:8px 0 4px}
  .stat .n{font-size:26px;font-variant-numeric:tabular-nums}
  .stat .l{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--ink3)}
  .chips{display:flex;gap:8px;flex-wrap:wrap}
  .chip{font-size:12px;padding:4px 12px;border-radius:999px;border:1px solid var(--rule);
    color:var(--ink2);cursor:pointer;background:var(--panel2)}
  .chip:hover{border-color:var(--amber);color:var(--ink)}
  .chip b{color:var(--ink)}
  .ladderlegend{max-width:78ch}
  .lrow{display:flex;gap:12px;align-items:baseline;padding:5px 0;border-top:1px solid rgba(255,255,255,.05)}
  .lrow .gloss{color:var(--ink3);font-size:12.5px}
  .hint{color:var(--ink3);font-size:12px;margin-top:14px}
  kbd{background:var(--panel3);border:1px solid var(--rule);border-radius:4px;padding:1px 6px;font-size:11px}
</style>
</head>
<body>
<div id="app">
  <div id="topbar">
    <h1 onclick="go('')"><span>&#9670;</span> THE LIBRARY &mdash; DATA DICTIONARY</h1>
    <input id="q" type="search" placeholder="Search 1,043 tables &mdash; name, description, column, ID&hellip;  ( / )" autocomplete="off">
    <select id="fDom"><option value="">All shelves</option></select>
    <select id="fState"><option value="">Any presence</option></select>
    <select id="fKey"><option value="">Any ID system</option></select>
    <span id="count"></span>
  </div>
  <div id="body">
    <div id="list"></div>
    <div id="main"></div>
  </div>
</div>
<script>
"use strict";
const PAL = /*__PALETTE__*/;
const DATA = /*__DATA__*/;

/* ---------- indexes (built once) ---------- */
const T = DATA.tables;
const byName = new Map(T.map((t,i)=>[t.n,i]));
const nbrs = T.map(()=>new Map());       // idx -> Map(otherIdx -> [{tier,key}])
for(const [a,b,tier,key] of DATA.edges){
  if(!nbrs[a].get(b)) nbrs[a].set(b,[]);
  if(!nbrs[b].get(a)) nbrs[b].set(a,[]);
  nbrs[a].get(b).push({tier,key});
  nbrs[b].get(a).push({tier,key});
}
const hay = T.map(t=>(t.n+" "+t.desc+" "+t.keys.join(" ")+" "+
  t.cols.map(c=>c.c).join(" ")).toLowerCase());
const fmtRows = r => r>=1e6 ? (r/1e6).toFixed(1)+"M" : r.toLocaleString("en-US");

/* ---------- filters ---------- */
const doms=[...new Set(T.map(t=>t.dom))].sort();
const domCount={}; T.forEach(t=>domCount[t.dom]=(domCount[t.dom]||0)+1);
fDom.innerHTML='<option value="">All shelves</option>'+
  doms.map(d=>`<option>${d}</option>`).join("");
fState.innerHTML='<option value="">Any presence</option>'+
  PAL.stateName.map((s,i)=>`<option value="${i}">${s}</option>`).join("");
const keyset=[...new Set(T.flatMap(t=>t.keys))].sort();
fKey.innerHTML='<option value="">Any ID system</option>'+
  keyset.map(k=>`<option>${k}</option>`).join("");

/* ---------- state + routing (#t=NAME / #q=...) ---------- */
let sel=null;
function go(name){ location.hash = name ? "t="+encodeURIComponent(name) : ""; }
window.addEventListener("hashchange", route);
function route(){
  const m=location.hash.match(/t=([^&]+)/);
  sel = m ? decodeURIComponent(m[1]) : null;
  render();
  if(sel){ main.scrollTop=0; const r=document.querySelector(".row.sel"); if(r) r.scrollIntoView({block:"nearest"}); }
}

/* ---------- search / list ---------- */
let results=[];
function filterTables(){
  const q=(qEl.value||"").toLowerCase().trim();
  const d=fDom.value, s=fState.value, k=fKey.value;
  results=[];
  for(let i=0;i<T.length;i++){
    const t=T[i];
    if(d && t.dom!==d) continue;
    if(s!=="" && t.state!==+s) continue;
    if(k && !t.keys.includes(k)) continue;
    if(q && !hay[i].includes(q)) continue;
    results.push(i);
  }
  // connected first inside every view, then by rows
  results.sort((a,b)=> (T[a].state-T[b].state) || (T[b].rows-T[a].rows));
}
const LIST_CAP=500;
function renderList(){
  const frag=[];
  for(const i of results.slice(0,LIST_CAP)){
    const t=T[i];
    frag.push(`<div class="row${t.n===sel?" sel":""}" onclick="go('${t.n}')">`+
      `<span class="dot" style="background:${PAL.state[t.state]};opacity:${[1,.95,.85,.5][t.state]}"></span>`+
      `<span class="nm" title="${t.n}">${t.n}</span>`+
      `<span class="meta">${t.cols.length? "" : ""}${fmtRows(t.rows)}${nbrs[i].size?` &middot; <span class="lk">${nbrs[i].size}&#8599;</span>`:""}</span></div>`);
  }
  if(results.length>LIST_CAP) frag.push(`<div id="more">&hellip;and ${results.length-LIST_CAP} more &mdash; narrow the search</div>`);
  list.innerHTML=frag.join("");
  count.textContent = results.length===T.length ? T.length+" tables" : results.length+" of "+T.length;
}

/* ---------- dossier ---------- */
function gradeChip(tier){
  return `<span class="grade" style="background:${PAL.ladder[tier]}">${DATA.ladder[tier].name}</span>`;
}
function renderDossier(t,i){
  const st=t.state;
  let h=`<div class="crumb"><a onclick="go('')">&larr; catalog</a></div>`;
  h+=`<h2 class="tname">${t.n}</h2>`;
  h+=`<div class="badges">`+
     `<span class="badge" style="border-color:${PAL.state[st]}"><b>${PAL.stateName[st]}</b></span>`+
     `<span class="badge">shelf: <b>${t.dom}</b></span>`+
     `<span class="badge"><b>${fmtRows(t.rows)}</b> rows</span>`+
     (t.keys.length?`<span class="badge">speaks: <b>${t.keys.join(", ")}</b></span>`:"")+
     `</div>`;
  if(t.desc) h+=`<p class="desc">${t.desc}</p>`;
  h+=`<p class="story">${PAL.stateStory[st]}</p>`;

  /* ID columns — the dictionary */
  h+=`<h3 class="sect">ID columns profiled <span class="n">${t.cols.length}</span></h3>`;
  if(t.cols.length){
    h+=`<table class="cols"><tr><th>column</th><th>ID family</th><th>filled</th><th>distinct</th><th>range (sampled)</th></tr>`;
    for(const c of t.cols){
      const low=c.p<50;
      h+=`<tr><td class="c">${c.c}</td><td class="k">${c.k}</td>`+
         `<td class="num"><span class="fill${low?" lowfill":""}"><i style="width:${Math.max(2,c.p)}%"></i></span>${c.p}%</td>`+
         `<td class="num">${(c.d??"").toLocaleString?.("en-US")??c.d}</td>`+
         `<td class="rng">${c.lo??""}${c.hi?" &rarr; "+c.hi:""}</td></tr>`;
    }
    h+=`</table>`;
    h+=`<p class="hint">Profiled ID-bearing columns from the connect fingerprint sweep. Full column lists live in Snowflake
        (<span class="mono">ripple chart cols &lt;fqn&gt;</span>).</p>`;
  } else {
    h+=`<p class="story">No ID-bearing columns profiled on this table.</p>`;
  }

  /* connections */
  const nn=[...nbrs[i].entries()].map(([j,links])=>{
    const best=Math.min(...links.map(l=>l.tier));
    return {j,links,best};
  }).sort((a,b)=> a.best-b.best || b.links.length-a.links.length);
  h+=`<h3 class="sect">Verified connections <span class="n">${nn.length? nn.reduce((s,x)=>s+x.links.length,0):0}</span>${nn.length?` links to <span class="n">${nn.length}</span> tables`:""}</h3>`;
  if(nn.length){
    h+=egoSVG(i,nn);
    for(const {j,links} of nn){
      const o=T[j];
      const parts=links.sort((a,b)=>a.tier-b.tier)
        .map(l=>gradeChip(l.tier)+` <span class="gkey">${l.key}</span>`).join(" &nbsp; ");
      h+=`<div class="neigh"><a onclick="go('${o.n}')">${o.n}</a> ${parts}<span class="nrows">${o.dom} &middot; ${fmtRows(o.rows)} rows</span></div>`;
    }
  } else {
    h+=`<p class="story">${st===1?"The search ran; nothing matched yet — that's a measured fact, and it's on the follow-up list."
        :st===2?"Nothing to join on yet: none of its columns carry a usable ID."
        :st===3?"Queued: link discovery hasn't run over this table yet."
        :"No links recorded."}</p>`;
  }
  main.innerHTML=h;
}

/* ER-style ego diagram: selected table centre, neighbours on a ring,
   edge weight/colour strictly by best grade (the ladder, nothing else). */
function egoSVG(i,nn){
  const MAXR=24;
  const shown=nn.slice(0,MAXR), extra=nn.length-shown.length;
  const W=Math.min(940, Math.max(620, main.clientWidth-40)), H=Math.min(540, 260+shown.length*11);
  const cx=W/2, cy=H/2, rx=cx-210, ry=cy-42;
  let s=`<svg id="ego" width="100%" viewBox="0 0 ${W} ${H}">`;
  shown.forEach((x,idx)=>{
    const a=-Math.PI/2 + idx*2*Math.PI/shown.length;
    const nx=cx+rx*Math.cos(a), ny=cy+ry*Math.sin(a);
    x._x=nx; x._y=ny; x._a=a;
    const w=[3,2.6,2.2,1.5,1,0.7][x.best], op=[1,.95,.9,.75,.6,.5][x.best];
    s+=`<line x1="${cx}" y1="${cy}" x2="${nx}" y2="${ny}" stroke="${PAL.ladder[x.best]}" stroke-width="${w}" opacity="${op}"><title>${x.links.map(l=>l.key+" ("+DATA.ladder[l.tier].name+")").join(", ")}</title></line>`;
  });
  shown.forEach((x,idx)=>{
    const o=T[x.j], cos=Math.cos(x._a), sin=Math.sin(x._a);
    // push labels radially past the node; near the poles anchor middle,
    // clear the ring vertically, and stagger alternating rows so 12/6
    // o'clock neighbours can't collide
    const polar=Math.abs(cos)<0.4;
    const stag=polar?(idx%2?14:0):0;
    const lx=x._x+(polar?0:cos>0?11:-11);
    const ly=x._y+(polar?(sin>0?16+stag:-10-stag):4);
    const anch=polar?"middle":(cos>0?"start":"end");
    const nm=o.n.length>(polar?22:30)?o.n.slice(0,polar?21:29)+"…":o.n;
    s+=`<circle cx="${x._x}" cy="${x._y}" r="4.5" fill="${PAL.state[o.state]}"/>`;
    s+=`<text x="${lx}" y="${ly}" font-size="10.5" text-anchor="${anch}" onclick="go('${o.n}')"><title>${o.n}</title>${nm}</text>`;
  });
  const t=T[i], nm=t.n.length>34?t.n.slice(0,33)+"…":t.n;
  s+=`<circle cx="${cx}" cy="${cy}" r="7" fill="${PAL.state[t.state]}" stroke="#eda748" stroke-width="2"/>`;
  s+=`<text class="ctr" x="${cx}" y="${cy-14}" font-size="12" text-anchor="middle">${nm}</text>`;
  if(extra>0) s+=`<text x="${cx}" y="${H-12}" font-size="11" text-anchor="middle" style="cursor:default;fill:#6b7684">+ ${extra} more below</text>`;
  s+=`</svg>`;
  return s;
}

/* ---------- overview (home) ---------- */
function renderHome(){
  const m=DATA.meta;
  const nLinked=T.filter(t=>t.state===0).length;
  let h=`<h2 style="font-size:20px;font-weight:600">The catalog</h2>
  <div class="stats">
    <div class="stat"><div class="n">${T.length.toLocaleString()}</div><div class="l">tables</div></div>
    <div class="stat"><div class="n">${(T.reduce((s,t)=>s+t.rows,0)/1e6).toFixed(1)}M</div><div class="l">rows</div></div>
    <div class="stat"><div class="n">${DATA.edges.length.toLocaleString()}</div><div class="l">verified links</div></div>
    <div class="stat"><div class="n">${nLinked}</div><div class="l">connected tables</div></div>
    <div class="stat"><div class="n">${keyset.length}</div><div class="l">ID systems</div></div>
  </div>
  <p class="story">Click any table on the left, or start typing. Every number here comes from
  <span class="mono">outputs/library.json</span> and the fingerprint sweep &mdash; nothing invented.</p>

  <h3 class="sect">Shelves</h3><div class="chips">`+
  doms.map(d=>`<span class="chip" onclick="fDom.value='${d}';onFilter()"><b>${d}</b> ${domCount[d]}</span>`).join("")+
  `</div>
  <h3 class="sect">Presence</h3><div class="chips">`+
  PAL.stateName.map((sn,i2)=>{
    const c=T.filter(t=>t.state===i2).length;
    return `<span class="chip" onclick="fState.value='${i2}';onFilter()"><span class="dot" style="display:inline-block;background:${PAL.state[i2]};margin-right:6px"></span><b>${sn}</b> ${c}</span>`;
  }).join("")+
  `</div>
  <h3 class="sect">The ladder of proof</h3><div class="ladderlegend">`+
  DATA.ladder.map((l,i2)=>{
    const c=DATA.edges.filter(e=>e[2]===i2).length;
    return `<div class="lrow">${gradeChip(i2)}<b class="num">${c.toLocaleString()}</b><span class="gloss">${l.gloss}</span></div>`;
  }).join("")+
  `</div>
  <h3 class="sect">The build, in one line</h3>
  <p class="story">${DATA.stages.map(s=>s.label+" — "+s.count.toLocaleString()).join("  →  ")}
  &nbsp;(dbt objects; ${m.lineage_edges.toLocaleString()} hand-offs)</p>
  <p class="hint"><kbd>/</kbd> search &nbsp; <kbd>&uarr;</kbd><kbd>&darr;</kbd> move &nbsp; <kbd>Enter</kbd> open &nbsp; <kbd>Esc</kbd> clear &mdash; the browser back button retraces your steps.</p>`;
  main.innerHTML=h;
}

/* ---------- wiring ---------- */
const qEl=document.getElementById("q"), list=document.getElementById("list"),
      main=document.getElementById("main"), count=document.getElementById("count");
function onFilter(){ filterTables(); renderList(); if(!sel) renderHome(); }
qEl.addEventListener("input",onFilter);
[fDom,fState,fKey].forEach(el=>el.addEventListener("change",onFilter));
function render(){
  filterTables(); renderList();
  const i=sel!=null?byName.get(sel):undefined;
  if(i!==undefined) renderDossier(T[i],i); else renderHome();
}
document.addEventListener("keydown",e=>{
  if(e.key==="/" && document.activeElement!==qEl){ e.preventDefault(); qEl.focus(); qEl.select(); }
  else if(e.key==="Escape"){ qEl.value=""; fDom.value=fState.value=fKey.value=""; go(""); onFilter(); }
  else if((e.key==="ArrowDown"||e.key==="ArrowUp") && results.length){
    e.preventDefault();
    const cur=results.findIndex(i=>T[i].n===sel);
    const nxt=e.key==="ArrowDown"?Math.min(results.length-1,cur+1):Math.max(0,cur-1);
    go(T[results[nxt]].n);
  }
  else if(e.key==="Enter" && document.activeElement===qEl && results.length){ go(T[results[0]].n); }
});
route();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
