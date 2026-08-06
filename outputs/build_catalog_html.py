import json

with open("outputs/id_catalog.json", encoding="utf-8") as f:
    rows = json.load(f)

def have_bucket(h):
    hl = h.lower()
    if hl.startswith("no") or hl.startswith("n/a"):
        return "No"
    if hl.startswith("yes") or hl.startswith("likely yes") or hl.startswith("plausibly yes") or hl.startswith("confirmed"):
        return "Likely/Yes"
    return "Unclear"

for r in rows:
    r["haveBucket"] = have_bucket(r["have"])

data_json = json.dumps(rows, ensure_ascii=False)

TEMPLATE = r"""<title>Ripple ID Catalog</title>
<style>
:root{color-scheme:light dark;--bg:#fff;--fg:#1a1a1a;--muted:#666;--border:#ddd;--card:#f7f7f8;--accent:#2563eb;}
@media (prefers-color-scheme: dark){:root{--bg:#15161a;--fg:#e8e8ea;--muted:#9a9aa2;--border:#33343a;--card:#1e1f24;--accent:#5b8def;}}
:root[data-theme="dark"]{--bg:#15161a;--fg:#e8e8ea;--muted:#9a9aa2;--border:#33343a;--card:#1e1f24;--accent:#5b8def;}
:root[data-theme="light"]{--bg:#fff;--fg:#1a1a1a;--muted:#666;--border:#ddd;--card:#f7f7f8;--accent:#2563eb;}
*{box-sizing:border-box;}
body{background:var(--bg);color:var(--fg);font-family:-apple-system,Segoe UI,Roboto,sans-serif;margin:0;padding:24px;}
h1{font-size:1.4rem;margin:0 0 4px;}
.sub{color:var(--muted);font-size:.9rem;margin-bottom:18px;}
.stats{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:18px;}
.stat{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:10px 16px;min-width:110px;}
.stat b{display:block;font-size:1.4rem;}
.stat span{color:var(--muted);font-size:.78rem;}
.controls{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:14px;align-items:center;}
select,input[type=text]{background:var(--card);color:var(--fg);border:1px solid var(--border);border-radius:8px;padding:7px 10px;font-size:.85rem;}
input[type=text]{flex:1;min-width:200px;}
.count{color:var(--muted);font-size:.82rem;margin-bottom:8px;}
.tablewrap{overflow-x:auto;border:1px solid var(--border);border-radius:10px;max-height:70vh;overflow-y:auto;}
table{border-collapse:collapse;width:100%;font-size:.82rem;}
th{position:sticky;top:0;background:var(--card);text-align:left;padding:8px 10px;border-bottom:1px solid var(--border);cursor:pointer;white-space:nowrap;z-index:1;}
th:hover{color:var(--accent);}
td{padding:7px 10px;border-bottom:1px solid var(--border);vertical-align:top;}
tr:hover td{background:rgba(128,128,128,0.08);}
.tag{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.72rem;font-weight:600;white-space:nowrap;}
.tier-STEEL{background:#16a34a22;color:#16a34a;}
.tier-STRONG{background:#2563eb22;color:#2563eb;}
.tier-WEAK{background:#9ca3af33;color:#6b7280;}
.have-Yes,.have-Likely\/Yes{background:#16a34a22;color:#16a34a;}
.have-No{background:#dc262622;color:#dc2626;}
.have-Unclear{background:#d9770622;color:#d97706;}
.harm{max-width:420px;color:var(--muted);}
.domain-col{white-space:nowrap;color:var(--muted);font-size:.78rem;}
footer{margin-top:16px;color:var(--muted);font-size:.78rem;}
</style>

<h1>Ripple - Full Identifier / Join-Key Catalog</h1>
<div class="sub">747 candidate IDs across 25 domains - 2026-08-05 exhaustive sweep - click column headers to sort, use filters below</div>

<div class="stats" id="stats"></div>

<div class="controls">
  <input type="text" id="search" placeholder="Search name or harm text...">
  <select id="domainFilter"><option value="">All domains</option></select>
  <select id="tierFilter"><option value="">All tiers</option></select>
  <select id="horizonFilter"><option value="">All horizons</option></select>
  <select id="haveFilter"><option value="">All already-have</option></select>
</div>

<div class="count" id="count"></div>
<div class="tablewrap">
<table id="tbl">
<thead><tr>
<th data-k="domain">Domain</th>
<th data-k="name">Name</th>
<th data-k="tier">Tier</th>
<th data-k="bulk">Bulk?</th>
<th data-k="horizon">Horizon</th>
<th data-k="haveBucket">Already Have?</th>
<th data-k="harm">Bridges to / Harm</th>
</tr></thead>
<tbody></tbody>
</table>
</div>

<footer>Tier: STEEL = hard unique ID - STRONG = looser opaque code - WEAK = fuzzy/borderline. Only 5 items in the whole catalog are SQL-verified (MSHA controller IDs, DOL OFLC case number, DOL SPONS_DFE_PN, OpenSanctions, OFAC) -- everything else is agent research, not confirmed against the warehouse yet.</footer>

<script>
const DATA = __DATA__;

const domainSel = document.getElementById('domainFilter');
const tierSel = document.getElementById('tierFilter');
const horizonSel = document.getElementById('horizonFilter');
const haveSel = document.getElementById('haveFilter');
const search = document.getElementById('search');
const tbody = document.querySelector('#tbl tbody');
const countEl = document.getElementById('count');
const statsEl = document.getElementById('stats');

function uniq(key){ return [...new Set(DATA.map(d=>d[key]))].sort(); }

function fillSelect(sel, key){
  uniq(key).forEach(v=>{
    const o = document.createElement('option');
    o.value = v; o.textContent = v;
    sel.appendChild(o);
  });
}
fillSelect(domainSel, 'domain');
fillSelect(tierSel, 'tier');
fillSelect(horizonSel, 'horizon');
fillSelect(haveSel, 'haveBucket');

let sortKey = 'domain', sortDir = 1;

function render(){
  const q = search.value.toLowerCase();
  const df = domainSel.value, tf = tierSel.value, hf = horizonSel.value, vf = haveSel.value;
  let rows = DATA.filter(d=>{
    if(df && d.domain!==df) return false;
    if(tf && d.tier!==tf) return false;
    if(hf && d.horizon!==hf) return false;
    if(vf && d.haveBucket!==vf) return false;
    if(q && !(d.name.toLowerCase().includes(q) || d.harm.toLowerCase().includes(q))) return false;
    return true;
  });
  rows.sort((a,b)=>{
    let av=a[sortKey], bv=b[sortKey];
    return av.localeCompare(bv)*sortDir;
  });
  countEl.textContent = rows.length + ' of ' + DATA.length + ' candidates shown';
  tbody.innerHTML = rows.map(r=>
    '<tr>' +
      '<td class="domain-col">'+r.domain+'</td>' +
      '<td><b>'+r.name+'</b></td>' +
      '<td><span class="tag tier-'+r.tier+'">'+r.tier+'</span></td>' +
      '<td>'+r.bulk+'</td>' +
      '<td>'+r.horizon+'</td>' +
      '<td><span class="tag have-'+r.haveBucket.replace('/','\\/')+'">'+r.haveBucket+'</span></td>' +
      '<td class="harm">'+r.harm+'</td>' +
    '</tr>'
  ).join('');

  const verified = 5;
  const steel = DATA.filter(d=>d.tier==='STEEL').length;
  const now = DATA.filter(d=>d.horizon==='now').length;
  const noHave = DATA.filter(d=>d.haveBucket==='No').length;
  statsEl.innerHTML =
    '<div class="stat"><b>'+DATA.length+'</b><span>total candidates</span></div>' +
    '<div class="stat"><b>25</b><span>domains covered</span></div>' +
    '<div class="stat"><b>'+steel+'</b><span>STEEL tier (hard unique ID)</span></div>' +
    '<div class="stat"><b>'+now+'</b><span>horizon = now</span></div>' +
    '<div class="stat"><b>'+noHave+'</b><span>confirmed new acquisitions</span></div>' +
    '<div class="stat"><b>'+verified+'</b><span>SQL-verified this sweep</span></div>';
}

document.querySelectorAll('th[data-k]').forEach(th=>{
  th.addEventListener('click', ()=>{
    const k = th.dataset.k;
    if(sortKey===k) sortDir*=-1; else {sortKey=k; sortDir=1;}
    render();
  });
});

[domainSel,tierSel,horizonSel,haveSel].forEach(s=>s.addEventListener('change', render));
search.addEventListener('input', render);

render();
</script>
"""

html = TEMPLATE.replace("__DATA__", data_json)

out_path = "C:/Users/wroge/AppData/Local/Temp/claude/c--Code-Ripple-v6/dcd7a54e-ceb1-4789-8db9-176e646ce411/scratchpad/id_catalog.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)
print("written", len(html))
