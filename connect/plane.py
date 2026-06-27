"""The Plane — a Google-Earth flythrough of the warehouse, built on ER diagrams.

The force-graph version was an unreadable hairball. This is the same "fly through your
data" idea done right: as a navigable DATABASE SCHEMA. Three altitudes, click to dive,
pan/zoom at every level (mouse wheel = zoom, drag = pan, double-click = reset):

  ORBIT  → your join keys as bubbles (NPI, CCN, EIN, …) sized by how many datasets carry
           them, linked where they co-occur. "What bridges my data."
  KEY    → click a key → the ER diagram of every dataset that joins on it: boxes = tables,
           lines = MEASURED joins (the number = rows that actually match).
  TABLE  → click a table → just that dataset + everything it connects to, on which key.

Self-contained + offline: Mermaid is vendored next to the file. Zero Snowflake — it all
comes from outputs/connect_graph.json (cached by connect.cache_layout).

Run:  python3 -m connect plane
"""
from __future__ import annotations

import json
import shutil
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "outputs" / "connect_graph.json"
OUT = ROOT / "outputs" / "plane.html"
MERMAID_SRC = ROOT / "outputs" / "erd" / "mermaid.min.js"   # vendored by scripts/erd.py
MERMAID_DST = ROOT / "outputs" / "mermaid.min.js"

# Keys that get their own ORBIT bubble + KEY diagram (the real join keys, not NAME/ADDRESS).
ORBIT_KEYS = ["NPI", "CCN", "EIN", "NCES", "UEI", "CIK", "IMO", "MMSI", "FIPS", "ZIP", "NAICS"]
ENT_IDS = {"NPI", "CCN", "EIN", "UEI", "CIK", "IMO", "MMSI", "LEI", "NDC", "NCES"}
NEIGHBORS_CAP = 24   # TABLE view: cap a hub's neighbours so the card stays readable


def build_data(graph: dict) -> dict:
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = graph["edges"]

    deg = defaultdict(int)
    for e in edges:
        deg[e["a"]] += 1
        deg[e["b"]] += 1

    # node metadata the client needs
    NODES = {}
    for nid, n in nodes.items():
        NODES[nid] = {
            "keys": n.get("keys", []),
            "rows": n["rows"],
            "domain": n.get("domain", "other"),
            "deg": deg.get(nid, 0),
        }

    # per-key edge lists (for the KEY diagrams) — only for keys present
    keyedges = defaultdict(list)
    for e in edges:
        if e["key"] in ORBIT_KEYS:
            keyedges[e["key"]].append([e["a"], e["b"], int(e["matched"])])

    present = [k for k in ORBIT_KEYS if keyedges.get(k)]
    KEYS = []
    for k in present:
        ds = sorted({a for a, b, m in keyedges[k]} | {b for a, b, m in keyedges[k]})
        KEYS.append({"key": k, "count": len(ds), "links": len(keyedges[k])})

    # key co-occurrence (ORBIT links): how many datasets carry BOTH keys
    carriers = {k: {nid for nid, n in nodes.items() if k in n.get("keys", [])} for k in present}
    cooc = []
    for i, a in enumerate(present):
        for b in present[i + 1:]:
            n = len(carriers[a] & carriers[b])
            if n >= 3:
                cooc.append([a, b, n])

    # adjacency for TABLE cards: each node's strongest neighbours across ALL keys
    adj = defaultdict(list)
    for e in edges:
        adj[e["a"]].append([e["b"], e["key"], int(e["matched"])])
        adj[e["b"]].append([e["a"], e["key"], int(e["matched"])])
    ADJ = {}
    for nid, lst in adj.items():
        lst.sort(key=lambda t: -t[2])
        ADJ[nid] = lst[:NEIGHBORS_CAP]

    return {
        "KEYS": KEYS,
        "KEYEDGES": {k: keyedges[k] for k in present},
        "COOC": cooc,
        "NODES": NODES,
        "ADJ": ADJ,
        "ENT": sorted(ENT_IDS),
    }


_PAGE = r"""<!doctype html><html><head><meta charset="utf-8">
<title>The Plane — Ripple warehouse</title>
<script src="mermaid.min.js"></script>
<style>
  html,body{margin:0;height:100%;background:#0d1117;color:#e8eaed;
    font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;overflow:hidden}
  #bar{position:fixed;top:0;left:0;right:0;height:46px;display:flex;align-items:center;gap:14px;
    padding:0 16px;background:rgba(13,17,23,.92);border-bottom:1px solid #21262d;z-index:10}
  #bar b{font-size:15px} #crumb{color:#9aa0a6;font-size:13px}
  #crumb a{color:#4da6ff;text-decoration:none;cursor:pointer} #crumb a:hover{text-decoration:underline}
  .chip{background:#161b22;border:1px solid #30363d;color:#c9d1d9;border-radius:14px;padding:3px 10px;
    font-size:12px;cursor:pointer} .chip:hover{border-color:#4da6ff;color:#fff}
  .chip.on{background:#1f6feb;border-color:#1f6feb;color:#fff}
  #search{margin-left:auto;background:#161b22;border:1px solid #30363d;color:#e8eaed;border-radius:6px;
    padding:5px 9px;font-size:12px;width:230px}
  #stage{position:fixed;top:46px;left:0;right:0;bottom:0;overflow:hidden;cursor:grab}
  #stage.drag{cursor:grabbing}
  #canvas{transform-origin:0 0;position:absolute;left:0;top:0}
  #hint{position:fixed;right:14px;bottom:12px;color:#5c6370;font-size:11px;z-index:10}
  .mermaid{background:transparent}
  text{cursor:default}
  g.node{cursor:pointer} g.node:hover [class*=Box],g.node:hover rect{stroke:#4da6ff!important;stroke-width:2px}
</style></head><body>
<div id="bar">
  <b>The Plane</b>
  <span id="crumb"></span>
  <span id="chips" style="display:flex;gap:6px"></span>
  <input id="search" placeholder="search a dataset…" list="dslist" autocomplete="off">
  <datalist id="dslist"></datalist>
</div>
<div id="stage"><div id="canvas"></div></div>
<div id="hint">wheel = zoom · drag = pan · double-click = reset · click a box to dive</div>
<script>
const D = window.__PLANE__;
mermaid.initialize({startOnLoad:false, theme:'dark', securityLevel:'loose',
  er:{useMaxWidth:false}, flowchart:{useMaxWidth:false}, themeVariables:{fontSize:'14px'}});

const stage=document.getElementById('stage'), canvas=document.getElementById('canvas');
const crumb=document.getElementById('crumb'), chips=document.getElementById('chips');
let view={level:'orbit'};

// ---- diagram builders (return mermaid source) ----
function short(id){return id.replace(/^PORTAL_(SOC|ARC)_/,'').replace(/^(FED|INTL|XC|ST|LOC)_/,'')
  .replace(/_/g,' ').replace(/\b([0-9A-F]{8,})\b/i,m=>'·'+m.slice(-4)).toLowerCase()
  .replace(/\b\w/g,c=>c.toUpperCase());}

function orbitSrc(){
  let s='graph LR\n';
  for(const k of D.KEYS){ s+=`  ${k.key}(["${k.key}<br/>${k.count} datasets"])\n`;
    s+=`  click ${k.key} call planeKey("${k.key}")\n`; }
  for(const [a,b,n] of D.COOC){ s+=`  ${a} ---|${n}| ${b}\n`; }
  s+='  classDef k fill:#161b22,stroke:#1f6feb,color:#e8eaed,stroke-width:2px;\n';
  s+='  class '+D.KEYS.map(k=>k.key).join(',')+' k;\n';
  return s;
}
function entityBox(id){
  let s=`  ${id} {\n`;
  for(const key of (D.NODES[id]?.keys||[])) s+=`    ${D.ENT.includes(key)?'id':'col'} ${key}\n`;
  return s+'  }\n';
}
function keySrc(key){
  const E=D.KEYEDGES[key]||[];
  const ids=[...new Set(E.flatMap(([a,b])=>[a,b]))].sort();
  let s='erDiagram\n';
  for(const id of ids) s+=entityBox(id);
  const seen=new Set();
  for(const [a,b,m] of E.slice().sort((x,y)=>y[2]-x[2])){
    const k=a<b?a+'|'+b:b+'|'+a; if(seen.has(k))continue; seen.add(k);
    s+=`  ${a} }o--o{ ${b} : "${m.toLocaleString()}"\n`;
  }
  return s;
}
function tableSrc(id){
  const nb=D.ADJ[id]||[];
  let s='erDiagram\n'+entityBox(id);
  for(const [other] of nb) s+=entityBox(other);
  for(const [other,key,m] of nb) s+=`  ${id} }o--o{ ${other} : "${key} ${m.toLocaleString()}"\n`;
  return s;
}

// ---- pan / zoom ----
let scale=1,tx=0,ty=0;
function apply(){canvas.style.transform=`translate(${tx}px,${ty}px) scale(${scale})`;}
function reset(fit){
  scale=1;tx=0;ty=0;apply();                       // identity first so we measure true size
  const svg=canvas.querySelector('svg');
  if(svg&&fit){
    const bb=svg.getBoundingClientRect(), sw=stage.clientWidth, sh=stage.clientHeight;
    if(bb.width>1&&bb.height>1){
      // floor the zoom so a big schema lands READABLE + pannable, not fit-to-dust
      scale=Math.max(0.4, Math.min(sw/bb.width, sh/bb.height, 1.4)*0.92);
      tx=(sw-bb.width*scale)/2;            // may be negative → overflow pans
      ty=(bb.height*scale<sh)?(sh-bb.height*scale)/2:12;
    }
  }
  apply();
}
stage.addEventListener('wheel',e=>{e.preventDefault();
  const r=stage.getBoundingClientRect(), mx=e.clientX-r.left, my=e.clientY-r.top;
  const f=e.deltaY<0?1.12:1/1.12, ns=Math.min(Math.max(scale*f,0.08),8);
  tx=mx-(mx-tx)*(ns/scale); ty=my-(my-ty)*(ns/scale); scale=ns; apply();
},{passive:false});
let pan=null;
stage.addEventListener('mousedown',e=>{pan={x:e.clientX-tx,y:e.clientY-ty};stage.classList.add('drag');});
window.addEventListener('mousemove',e=>{if(pan){tx=e.clientX-pan.x;ty=e.clientY-pan.y;apply();}});
window.addEventListener('mouseup',()=>{pan=null;stage.classList.remove('drag');});
stage.addEventListener('dblclick',()=>reset(true));

// ---- navigation ----
window.planeKey=(k)=>{view={level:'key',key:k};render();};
window.planeTable=(t)=>{view={level:'table',table:t};render();};
function setCrumb(){
  let h=`<a onclick="planeOrbit()">ORBIT</a>`;
  if(view.level==='key') h+=` › ${view.key}`;
  if(view.level==='table') h+=` › <a onclick="planeTable('${view.table}')">${short(view.table)}</a>`;
  crumb.innerHTML=h;
}
window.planeOrbit=()=>{view={level:'orbit'};render();};

async function render(){
  let src;
  if(view.level==='orbit') src=orbitSrc();
  else if(view.level==='key') src=keySrc(view.key);
  else src=tableSrc(view.table);
  const {svg}=await mermaid.render('m'+Date.now(), src);
  canvas.innerHTML=svg;
  // bind clicks on ER entity boxes → dive into that table
  canvas.querySelectorAll('g.node').forEach(g=>{
    const m=(g.id||'').match(/entity-(.+)-\d+$/);
    if(m) g.addEventListener('click',ev=>{ev.stopPropagation();planeTable(m[1]);});
  });
  setCrumb();
  chips.querySelectorAll('.chip').forEach(c=>c.classList.toggle('on',c.dataset.k===view.key));
  requestAnimationFrame(()=>requestAnimationFrame(()=>reset(true)));  // fit after layout settles
}

// chips + search
for(const k of D.KEYS){ const c=document.createElement('span');
  c.className='chip';c.dataset.k=k.key;c.textContent=k.key;
  c.onclick=()=>planeKey(k.key); chips.appendChild(c); }
const dl=document.getElementById('dslist');
for(const id of Object.keys(D.NODES).sort()){ const o=document.createElement('option');o.value=id;dl.appendChild(o); }
document.getElementById('search').addEventListener('change',e=>{
  if(D.NODES[e.target.value]) planeTable(e.target.value);
});

render();
</script></body></html>"""


def render(open_browser: bool = True) -> Path:
    graph = json.loads(GRAPH.read_text())
    data = build_data(graph)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if MERMAID_SRC.exists() and not MERMAID_DST.exists():
        shutil.copy(MERMAID_SRC, MERMAID_DST)
    if not MERMAID_DST.exists():
        raise SystemExit("plane: mermaid.min.js missing — run `python3 scripts/erd.py` once to vendor it")

    page = _PAGE.replace(
        "const D = window.__PLANE__;",
        "window.__PLANE__=" + json.dumps(data, separators=(",", ":")) + ";\nconst D = window.__PLANE__;",
    )
    OUT.write_text(page, encoding="utf-8")
    mb = OUT.stat().st_size / 1_048_576
    print(f"wrote {OUT}  ({mb:.2f} MB)  ·  {len(data['KEYS'])} keys · {len(data['NODES'])} datasets")
    if open_browser:
        try:
            import webbrowser
            webbrowser.open(OUT.resolve().as_uri())
            print("opened in your browser")
        except Exception:
            print(f"open it manually: {OUT}")
    return OUT


if __name__ == "__main__":
    render()
