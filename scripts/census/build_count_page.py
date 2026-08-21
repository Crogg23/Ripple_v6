"""Render the 'number of X' list as one searchable page.

Reads reports/count_possibilities.json and writes a single self-contained HTML
file. Every entry carries the plain-English question, what the number actually
means, the table it comes from, and copy-ready SQL.

The shape of the page is what makes 17,000 entries usable:
  * you land on the 647 datasets, not on 17,000 counts
  * opening a dataset shows only its counts, grouped by question type
  * a count is one line until you click it, and the copy button works closed
  * searching jumps straight to matching counts across every dataset

The data is packed table-first (the dataset description repeats ~25 times per
table otherwise) and rendered on demand, so the page stays light.
"""
from __future__ import annotations

import html
import json
import os
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(REPO, "reports", "count_possibilities.json")
OUT = os.path.join(REPO, "reports", "count_possibilities.html")

KIND_ORDER = [
    "How many in total",
    "How many per year",
    "How many different things",
    "How many each one has",
    "How many different things per year",
    "How many arrived and left",
    "How many of each kind",
    "How the mix moved",
    "How many in each place",
    "How many different things per place",
    "How many are flagged",
    "How many kinds exist",
    "How many have a value",
    "How many show up more than once",
    "How many pass a threshold",
    "How many are missing it",
    "How many across two tables",
]

# Short labels for the filter row and the group headings -- the full kind names
# are too long to sit in a chip.
KIND_CHIP = {
    "How many in total": "the total",
    "How many per year": "per year",
    "How many different things": "distinct things",
    "How many each one has": "each one's share",
    "How many different things per year": "things per year",
    "How many arrived and left": "new arrivals",
    "How many of each kind": "by kind",
    "How the mix moved": "mix over time",
    "How many in each place": "by place",
    "How many different things per place": "things per place",
    "How many are flagged": "flags",
    "How many kinds exist": "how many kinds",
    "How many have a value": "fill check",
    "How many show up more than once": "duplicates",
    "How many pass a threshold": "over a threshold",
    "How many are missing it": "blanks",
    "How many across two tables": "needs a join",
}


NO_DESCRIPTION = "No plain-English description has been written for this dataset yet."


def pack():
    d = json.load(open(SRC, encoding="utf-8"))
    per_table = Counter(e["table"] for e in d["entries"])
    tables, index = [], {}
    for t in d["tables"]:
        index[t["table"]] = len(tables)
        tables.append([t["table"], t["subject"], t["dataset"], t["noun"],
                       t["rows"] if t["rows"] is not None else -1,
                       1 if t["noun_known"] else 0,
                       per_table.get(t["table"], 0),
                       0 if t["dataset"].startswith(NO_DESCRIPTION[:40]) else 1])
    kinds = {k: i for i, k in enumerate(KIND_ORDER)}
    entries = []
    for e in d["entries"]:
        entries.append([index[e["table"]], kinds.get(e["kind"], len(KIND_ORDER)),
                        e["question"], e["means"], e["sql"],
                        0 if e["needs"] == "one table" else 1])
    return tables, entries, KIND_ORDER + ["Other"]


def build():
    tables, entries, kinds = pack()
    subjects = sorted({t[1] for t in tables})
    payload = json.dumps({"t": tables, "e": entries, "k": kinds,
                          "c": [KIND_CHIP.get(k, k) for k in kinds]},
                         separators=(",", ":"), ensure_ascii=False)
    options = "".join(f'<option value="{html.escape(s)}">{html.escape(s)}</option>'
                      for s in subjects)
    kindchips = "".join(
        f'<button class="chip" data-kind="{i}" aria-pressed="false">'
        f'{html.escape(KIND_CHIP.get(k, k))}</button>'
        for i, k in enumerate(kinds) if k != "Other")
    doc = TEMPLATE.replace("__PAYLOAD__", payload)
    doc = doc.replace("__OPTIONS__", options).replace("__KINDCHIPS__", kindchips)
    doc = doc.replace("__N_COUNTS__", f"{len(entries):,}")
    doc = doc.replace("__N_TABLES__", f"{len(tables):,}")
    doc = doc.replace("__N_UNDESCRIBED__", f"{sum(1 for t in tables if not t[7]):,}")
    doc = doc.replace("__N_JOINS__", f"{sum(1 for e in entries if e[5]):,}")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return OUT, len(entries), len(tables)


TEMPLATE = r"""<title>Things You Can Count</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
  --ground:#f4f7f7; --surface:#ffffff; --sunk:#eef2f3; --ink:#111d23; --ink-2:#3c4f59;
  --muted:#6c7f89; --accent:#0c6a64; --line:#dbe4e5; --flag:#84560f; --flag-soft:#f5ebd9;
  --hover:#e8eef0;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:#0b1316; --surface:#111e23; --sunk:#0d181c; --ink:#e2eaea; --ink-2:#b3c4c8;
    --muted:#7e939c; --accent:#4cc0b5; --line:#20313a; --flag:#dcb46b; --flag-soft:#2a2214;
    --hover:#16252b;
  }
}
:root[data-theme="dark"] {
  --ground:#0b1316; --surface:#111e23; --sunk:#0d181c; --ink:#e2eaea; --ink-2:#b3c4c8;
  --muted:#7e939c; --accent:#4cc0b5; --line:#20313a; --flag:#dcb46b; --flag-soft:#2a2214;
  --hover:#16252b;
}
* { box-sizing:border-box; }
body {
  background:var(--ground); color:var(--ink); margin:0;
  font-family:"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size:16px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
.wrap { max-width:900px; margin:0 auto; padding:0 24px 72px; }
header.top { padding:28px 0 12px; }
.eyebrow {
  font-family:"IBM Plex Mono", monospace; font-size:11px; letter-spacing:0.14em;
  text-transform:uppercase; color:var(--accent); margin:0 0 6px;
}
h1 {
  font-family:Newsreader, Georgia, serif; font-weight:500;
  font-size:clamp(24px, 4vw, 32px); line-height:1.1; letter-spacing:-0.015em;
  margin:0 0 6px; text-wrap:balance;
}
.lede { font-size:14.5px; color:var(--ink-2); margin:0; max-width:70ch; }
.lede strong { color:var(--ink); font-weight:600; }

/* ---- one control bar ---------------------------------------------------- */
.bar {
  position:sticky; top:0; z-index:30; background:var(--ground);
  padding:10px 0 8px; border-bottom:1px solid var(--line); margin-top:14px;
}
.row1 { display:flex; gap:8px; align-items:stretch; }
#q {
  flex:1 1 auto; min-width:0; padding:11px 13px; font:inherit; font-size:15px;
  color:var(--ink); background:var(--surface); border:1px solid var(--line); border-radius:3px;
}
#q:focus { outline:2px solid var(--accent); outline-offset:1px; border-color:var(--accent); }
#q::placeholder { color:var(--muted); }
#subject {
  flex:0 0 auto; max-width:42%; padding:11px 10px; font:inherit; font-size:14px;
  color:var(--ink); background:var(--surface); border:1px solid var(--line);
  border-radius:3px; cursor:pointer;
}
#subject:focus { outline:2px solid var(--accent); outline-offset:1px; }
#kinds { display:flex; gap:5px; overflow-x:auto; padding:9px 1px 2px; scrollbar-width:thin; }
#kinds.hidden { display:none; }
.chip {
  font:inherit; font-size:12px; padding:4px 10px; border-radius:999px; cursor:pointer;
  color:var(--ink-2); white-space:nowrap; background:transparent;
  border:1px solid var(--line); flex:0 0 auto;
}
.chip:hover { border-color:var(--accent); color:var(--accent); }
.chip[aria-pressed="true"] { background:var(--accent); border-color:var(--accent); color:var(--ground); }
.chip:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }

/* ---- breadcrumb + tally ------------------------------------------------- */
.status {
  display:flex; align-items:baseline; justify-content:space-between; gap:16px;
  flex-wrap:wrap; padding:10px 0 2px;
}
#crumb { font-size:14px; color:var(--ink-2); }
#crumb button {
  font:inherit; font-size:14px; color:var(--accent); background:none; border:none;
  padding:0; cursor:pointer; text-decoration:underline; text-underline-offset:2px;
}
#crumb button:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
#tally {
  font-family:"IBM Plex Mono", monospace; font-size:12px; color:var(--muted);
  font-variant-numeric:tabular-nums; flex:0 0 auto;
}

/* ---- the dataset index, which is where you land ------------------------- */
.ds {
  display:block; width:100%; text-align:left; font:inherit; cursor:pointer;
  background:none; border:none; border-top:1px solid var(--line);
  padding:9px 8px 8px; color:inherit;
}
.ds:hover { background:var(--hover); }
.ds:focus-visible { outline:2px solid var(--accent); outline-offset:-2px; }
.ds .name {
  font-family:Newsreader, Georgia, serif; font-size:16px; font-weight:500;
  line-height:1.2; letter-spacing:-0.005em; display:block; margin-bottom:1px;
}
.ds .about {
  display:block; color:var(--ink-2); font-size:13px; margin-bottom:3px;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}
.ds .meta {
  font-family:"IBM Plex Mono", monospace; font-size:11px; color:var(--muted);
  font-variant-numeric:tabular-nums;
}
.ds .meta b { color:var(--accent); font-weight:500; }
.ds .meta .dot { opacity:0.5; padding:0 4px; }

/* ---- an opened dataset -------------------------------------------------- */
.head { padding:14px 0 3px; }
.head h2 {
  font-family:Newsreader, Georgia, serif; font-weight:500; font-size:22px;
  letter-spacing:-0.012em; margin:0 0 3px; text-wrap:balance;
}
.head .about { margin:0 0 5px; color:var(--ink-2); font-size:13.5px; max-width:70ch; }
.head .src {
  font-family:"IBM Plex Mono", monospace; font-size:11px; color:var(--muted);
  margin:0; font-variant-numeric:tabular-nums; word-break:break-all;
}
.head .src .dot { opacity:0.5; padding:0 4px; }
.groupname {
  font-family:"IBM Plex Mono", monospace; font-size:10px; letter-spacing:0.12em;
  text-transform:uppercase; color:var(--muted); margin:12px 0 0; padding:0 8px;
}

/* ---- one count: a single line until it is opened ------------------------ */
.item { border-top:1px solid var(--line); }
.qrow { display:flex; align-items:flex-start; gap:8px; }
.qbtn {
  flex:1 1 auto; min-width:0; text-align:left; font:inherit; cursor:pointer;
  background:none; border:none; padding:6px 0 6px 8px; color:inherit;
  font-family:"IBM Plex Sans", sans-serif; font-size:14px; line-height:1.35;
  letter-spacing:-0.002em; display:flex; gap:8px; align-items:baseline;
}
.qbtn:hover { color:var(--accent); }
.qbtn:focus-visible { outline:2px solid var(--accent); outline-offset:-2px; }
.qbtn .caret {
  flex:0 0 auto; font-family:"IBM Plex Mono", monospace; font-size:11px;
  color:var(--muted); width:9px;
}
.item.open .qbtn, .item.open .qbtn .caret { color:var(--accent); }
.copy {
  flex:0 0 auto; margin:6px 8px 0 0; font:inherit; font-size:10.5px;
  font-family:"IBM Plex Mono", monospace; letter-spacing:0.04em;
  padding:2px 8px; border-radius:3px; cursor:pointer; align-self:flex-start;
  background:var(--surface); color:var(--muted); border:1px solid var(--line);
  min-width:56px; text-align:center;
}
.copy:hover { color:var(--accent); border-color:var(--accent); }
.copy:focus-visible { outline:2px solid var(--accent); outline-offset:2px; }
.detail { display:none; padding:0 8px 12px 25px; }
.item.open .detail { display:block; }
.detail .means { margin:0 0 8px; color:var(--ink-2); font-size:13px; max-width:70ch; }
.detail .from {
  font-family:"IBM Plex Mono", monospace; font-size:11px; color:var(--muted);
  margin:0 0 6px; word-break:break-all;
}
pre {
  margin:0; padding:10px 12px; background:var(--sunk); border:1px solid var(--line);
  border-radius:3px; overflow-x:auto;
  font-family:"IBM Plex Mono", monospace; font-size:12px; line-height:1.5;
  color:var(--ink); white-space:pre;
}
.needs {
  display:inline-block; margin:7px 0 0; padding:2px 8px; border-radius:3px;
  background:var(--flag-soft); color:var(--flag);
  font-family:"IBM Plex Mono", monospace; font-size:10.5px;
}

#more {
  display:block; width:100%; margin:26px 0 0; padding:13px; cursor:pointer;
  font:inherit; font-size:14px; color:var(--accent); background:var(--surface);
  border:1px solid var(--line); border-radius:3px;
}
#more:hover { border-color:var(--accent); }
#more[hidden] { display:none; }
.empty { padding:44px 8px; color:var(--muted); font-size:15px; }
.note {
  margin-top:32px; padding:16px 20px; background:var(--surface);
  border:1px solid var(--line); border-radius:4px;
}
.note h2 { font-family:Newsreader, Georgia, serif; font-weight:500; margin:0 0 9px; font-size:17px; }
.note ul { margin:0; padding-left:17px; }
.note li { margin:0 0 6px; color:var(--ink-2); font-size:13.5px; line-height:1.45; max-width:68ch; }
.note li:last-child { margin-bottom:0; }
.note strong { color:var(--ink); font-weight:600; }
#top {
  position:fixed; right:20px; bottom:20px; z-index:40; display:none;
  font:inherit; font-size:12px; font-family:"IBM Plex Mono", monospace;
  padding:8px 12px; border-radius:3px; cursor:pointer;
  background:var(--surface); color:var(--ink-2); border:1px solid var(--line);
  box-shadow:0 1px 4px rgba(0,0,0,0.14);
}
#top:hover { color:var(--accent); border-color:var(--accent); }
#top.show { display:block; }
@media (max-width:620px) {
  .row1 { flex-wrap:wrap; }
  #subject { max-width:100%; width:100%; }
  .qbtn { font-size:15px; }
}
@media (prefers-reduced-motion:reduce) { * { scroll-behavior:auto !important; } }
</style>

<div class="wrap">
<header class="top">
  <p class="eyebrow">Every count in the warehouse</p>
  <h1>__N_COUNTS__ things you can count</h1>
  <p class="lede">Every &ldquo;number of X&rdquo; across <strong>__N_TABLES__ datasets</strong> &mdash; click for the SQL, or just hit copy. Nothing here has been run.</p>
</header>

<div class="bar">
  <div class="row1">
    <input id="q" type="search" placeholder="Search everything &mdash; judge, mine, opioid, per year&hellip;    press /" autocomplete="off">
    <select id="subject" aria-label="Filter by subject">
      <option value="">All subjects</option>
      __OPTIONS__
    </select>
  </div>
  <div id="kinds" class="hidden">
    <button class="chip" data-kind="" aria-pressed="true">every question</button>
    __KINDCHIPS__
  </div>
</div>

<div class="status">
  <span id="crumb"></span>
  <span id="tally"></span>
</div>

<div id="results"></div>
<button id="more" hidden>Show more</button>

<div class="note">
  <h2>Before you trust a number</h2>
  <ul>
    <li><strong>Rows &ne; things.</strong> Check &ldquo;different things&rdquo; against the row count &mdash; a big gap means one thing shows up many times.</li>
    <li><strong>Blank &ne; zero.</strong> Run the &ldquo;missing&rdquo; count first, or a breakdown quietly drops rows and still looks clean.</li>
    <li><strong>Rising counts often mean rising coverage,</strong> not a rising world &mdash; check the per-year &ldquo;different things&rdquo; count too.</li>
    <li><strong>__N_JOINS__ counts need two tables,</strong> marked below. Padded zeros and placeholders have faked matches here before.</li>
    <li><strong>__N_UNDESCRIBED__ datasets have no description yet.</strong> The counts are still right &mdash; the write-up just isn't done.</li>
  </ul>
</div>
</div>

<button id="top" type="button">&uarr; top</button>

<script id="data" type="application/json">__PAYLOAD__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const T = DATA.t, E = DATA.e, K = DATA.k, C = DATA.c;
const PAGE = 150;

// Search text per count, and per dataset for the index view.
const hay = E.map(e => (e[2] + ' ' + e[3] + ' ' + T[e[0]][0] + ' ' + T[e[0]][2]).toLowerCase());
const tHay = T.map(t => (t[0] + ' ' + t[2] + ' ' + t[3] + ' ' + t[1]).toLowerCase());

// Counts grouped by dataset, and the dataset order: biggest first.
const byTable = T.map(() => []);
E.forEach((e, i) => byTable[e[0]].push(i));
const tOrder = T.map((t, i) => i).sort((a, b) => T[b][4] - T[a][4]);
const tRank = new Array(T.length);
tOrder.forEach((idx, rank) => { tRank[idx] = rank; });

const q = document.getElementById('q');
const subjectSel = document.getElementById('subject');
const kindsRow = document.getElementById('kinds');
const results = document.getElementById('results');
const crumb = document.getElementById('crumb');
const tally = document.getElementById('tally');
const more = document.getElementById('more');
const topBtn = document.getElementById('top');

let subject = '', kind = '', openTable = -1, shown = 0, matches = [], mode = 'index';

function esc(s) {
  return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}
function rowText(n) { return n < 0 ? 'row count unknown' : n.toLocaleString() + ' rows'; }
function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

// The bit of the table name that identifies the source: HEALTH.HEALTH__FED_CMS_NPPES
// becomes 'fed cms nppes'. Used to tell two datasets apart when their plain
// nouns are the same, and as the title for the ones with no description written.
function shortName(fqn) {
  const tail = fqn.split('.').pop();
  return (tail.includes('__') ? tail.split('__').slice(1).join(' ') : tail)
    .replace(/_/g, ' ').toLowerCase();
}
// t[5] is 0 when nobody has written down what a row of this table is. Calling
// 217 different datasets 'Record' in a list makes the list useless.
function title(t) { return t[5] ? cap(t[3]) : cap(shortName(t[0])); }
// 217 identical grey sentences saying 'no description written' is noise in a list.
function about(t) { return t[7] ? t[2] : 'No description written for this one yet.'; }
function terms() { const s = q.value.trim().toLowerCase(); return s ? s.split(/\s+/) : []; }
function hit(text, ts) { for (const w of ts) if (!text.includes(w)) return false; return true; }
function backLink() { return '<button type="button" id="back">&larr; all datasets</button>'; }

/* ---------- which of the three views is on screen ------------------------ */
function update() {
  const ts = terms();
  mode = openTable >= 0 ? 'dataset' : (ts.length ? 'search' : 'index');
  kindsRow.classList.toggle('hidden', mode === 'index');
  shown = 0;
  results.innerHTML = '';
  more.hidden = true;
  if (mode === 'index') renderIndex(ts);
  else computeCounts(ts);
}

/* ---------- the landing view: the datasets themselves -------------------- */
function renderIndex(ts) {
  const list = tOrder.filter(i =>
    (!subject || T[i][1] === subject) && T[i][6] > 0 && (!ts.length || hit(tHay[i], ts)));
  crumb.textContent = 'Every dataset, biggest first. Click one to see its counts.';
  tally.textContent = list.length.toLocaleString() + ' datasets · ' +
    E.length.toLocaleString() + ' counts';
  if (!list.length) {
    results.innerHTML = '<p class="empty">No dataset matches that.</p>';
    return;
  }
  results.innerHTML = list.map(i => {
    const t = T[i];
    return '<button class="ds" data-table="' + i + '" type="button">' +
      '<span class="name">' + esc(title(t)) + '</span>' +
      '<span class="about">' + esc(about(t)) + '</span>' +
      '<span class="meta"><b>' + t[6] + ' counts</b><span class="dot">&middot;</span>' +
      rowText(t[4]) + '<span class="dot">&middot;</span>' + esc(t[1]) +
      // Only worth repeating when it is not already the heading.
      (title(t).toLowerCase() !== shortName(t[0])
        ? '<span class="dot">&middot;</span>' + esc(shortName(t[0])) : '') +
      '</span></button>';
  }).join('');
}

/* ---------- counts, inside one dataset or across a search ---------------- */
function computeCounts(ts) {
  const pool = openTable >= 0 ? byTable[openTable] : E.map((_, i) => i);
  matches = [];
  for (const i of pool) {
    const e = E[i], t = T[e[0]];
    if (openTable < 0 && subject && t[1] !== subject) continue;
    if (kind !== '' && e[1] !== +kind) continue;
    if (ts.length && !hit(hay[i], ts)) continue;
    matches.push(i);
  }
  matches.sort((a, b) =>
    (tRank[E[a][0]] - tRank[E[b][0]]) || (E[a][1] - E[b][1]) || (a - b));

  if (openTable >= 0) {
    const t = T[openTable];
    crumb.innerHTML = backLink();
    results.innerHTML =
      '<div class="head"><h2>' + esc(title(t)) + '</h2>' +
      '<p class="about">' + esc(about(t)) + '</p>' +
      '<p class="src">' + esc(t[0]) + '<span class="dot">&middot;</span>' + esc(t[1]) +
      '<span class="dot">&middot;</span>' + rowText(t[4]) + '</p></div>';
  } else {
    crumb.innerHTML = backLink() + '&nbsp; matches across every dataset';
  }
  tally.textContent = matches.length.toLocaleString() + ' count' +
    (matches.length === 1 ? '' : 's');
  if (!matches.length) {
    results.insertAdjacentHTML('beforeend',
      '<p class="empty">Nothing matches. Try a plainer word &mdash; the questions are written in ordinary English.</p>');
    return;
  }
  renderCounts();
}

function renderCounts() {
  const end = Math.min(shown + PAGE, matches.length);
  let out = '';
  let lastTable = shown > 0 ? E[matches[shown - 1]][0] : -1;
  let lastKind = shown > 0 ? E[matches[shown - 1]][1] : -1;
  for (let i = shown; i < end; i++) {
    const idx = matches[i], e = E[idx], t = T[e[0]];
    if (openTable < 0 && e[0] !== lastTable) {
      out += '<p class="groupname">' + esc(title(t)) + ' &nbsp;&middot;&nbsp; ' + esc(t[0]) + '</p>';
      lastTable = e[0]; lastKind = -1;
    }
    if (openTable >= 0 && e[1] !== lastKind) {
      out += '<p class="groupname">' + esc(C[e[1]] || K[e[1]]) + '</p>';
      lastKind = e[1];
    }
    out += '<div class="item" data-i="' + idx + '">' +
      '<div class="qrow">' +
        '<button class="qbtn" type="button" aria-expanded="false">' +
          '<span class="caret" aria-hidden="true">+</span><span>' + esc(e[2]) + '</span>' +
        '</button>' +
        '<button class="copy" type="button" title="Copy the SQL">copy</button>' +
      '</div>' +
      '<div class="detail">' +
        '<p class="means">' + esc(e[3]) + '</p>' +
        (openTable < 0 ? '<p class="from">' + esc(t[0]) + '</p>' : '') +
        '<pre>' + esc(e[4]) + '</pre>' +
        (e[5] ? '<span class="needs">needs two tables joined</span>' : '') +
      '</div></div>';
  }
  results.insertAdjacentHTML('beforeend', out);
  shown = end;
  more.hidden = shown >= matches.length;
  more.textContent = 'Show the other ' + (matches.length - shown).toLocaleString();
}

/* ---------- interaction -------------------------------------------------- */
function setOpen(item, open) {
  const qbtn = item.querySelector('.qbtn');
  item.classList.toggle('open', open);
  qbtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  qbtn.querySelector('.caret').textContent = open ? '−' : '+';
}

// Copy-to-clipboard has to work three ways: the modern async API, the classic
// textarea+execCommand trick (which still works inside a sandboxed iframe when
// the async API is blocked by permissions policy), and — if both are refused —
// reveal and select the SQL so a manual ctrl+C still works. Never leave the
// button dead.
function copySQL(sql, btn, item) {
  const succeed = () => {
    btn.textContent = 'copied';
    setTimeout(() => { btn.textContent = 'copy'; }, 1400);
  };
  const revealAndSelect = () => {
    if (!item.classList.contains('open')) setOpen(item, true);
    try {
      const range = document.createRange();
      range.selectNodeContents(item.querySelector('pre'));
      const sel = getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
    } catch (e) {}
    btn.textContent = 'ctrl+c';
  };
  const execFallback = () => {
    const ta = document.createElement('textarea');
    ta.value = sql;
    ta.setAttribute('readonly', '');
    ta.style.cssText = 'position:fixed;top:-1000px;opacity:0;';
    document.body.appendChild(ta);
    ta.focus();
    ta.select();
    let ok = false;
    try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
    document.body.removeChild(ta);
    if (ok) succeed(); else revealAndSelect();
  };
  try {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(sql).then(succeed, execFallback);
    } else {
      execFallback();
    }
  } catch (e) {
    execFallback();
  }
}

results.addEventListener('click', ev => {
  const ds = ev.target.closest('.ds');
  if (ds) {
    openTable = +ds.dataset.table; kind = ''; setKindChip('');
    update(); scrollTo({top: 0}); return;
  }
  const copy = ev.target.closest('.copy');
  if (copy) {
    const item = copy.closest('.item');
    const sql = E[+item.dataset.i][4];
    copySQL(sql, copy, item);
    return;
  }
  const qbtn = ev.target.closest('.qbtn');
  if (qbtn) {
    const item = qbtn.closest('.item');
    setOpen(item, !item.classList.contains('open'));
  }
});

crumb.addEventListener('click', ev => {
  if (ev.target.id === 'back') {
    openTable = -1; kind = ''; setKindChip(''); update(); scrollTo({top: 0});
  }
});

function setKindChip(val) {
  kindsRow.querySelectorAll('.chip').forEach(x =>
    x.setAttribute('aria-pressed', x.dataset.kind === val ? 'true' : 'false'));
}
kindsRow.addEventListener('click', ev => {
  const c = ev.target.closest('.chip');
  if (!c) return;
  kind = c.dataset.kind;
  setKindChip(kind);
  update();
});

subjectSel.addEventListener('change', () => {
  subject = subjectSel.value;
  openTable = -1;
  update();
});

let timer;
q.addEventListener('input', () => { clearTimeout(timer); timer = setTimeout(update, 130); });
more.addEventListener('click', renderCounts);

addEventListener('keydown', ev => {
  if (ev.key === '/' && document.activeElement !== q) {
    ev.preventDefault(); q.focus(); q.select();
  } else if (ev.key === 'Escape') {
    if (document.activeElement === q && q.value) { q.value = ''; update(); }
    else if (openTable >= 0) { openTable = -1; update(); scrollTo({top: 0}); }
  }
});

addEventListener('scroll', () => { topBtn.classList.toggle('show', scrollY > 900); });
topBtn.addEventListener('click', () => scrollTo({top: 0, behavior: 'smooth'}));

update();
</script>
"""


if __name__ == "__main__":
    path, n, t = build()
    print(f"{n:,} counts across {t:,} tables -> {path} "
          f"({os.path.getsize(path)/1e6:.1f} MB)")
