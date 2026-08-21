"""Render one unified page: every count, cross-tab, share, and real join in one place.

Merges reports/count_possibilities.json (the plain-count tier) and
reports/count_possibilities_layer2.json (the cross-tab/share/real-join tiers,
plus reports/layer2_joins.json if the 206 real joins have been run) into a
single searchable page. Same shape, same design system as the two pages this
replaces -- land on the 647 datasets, open one to see its questions, one line
until you click it, copy button works closed -- with one change: a tier row
(count / cross & share / real join) and the kind row both sit on the landing
view now, not hidden until you open a dataset or start typing. That was the
one real usability gap found when both prior pages were tested by hand.

Does not touch count_possibilities.py, count_possibilities_layer2.py, or
run_layer2_joins.py -- the classification and question-generation logic is
untouched. This only changes how the same three files' output is presented.
"""
from __future__ import annotations

import csv
import html
import json
import os
import sys
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC1 = os.path.join(REPO, "reports", "count_possibilities.json")
SRC2 = os.path.join(REPO, "reports", "count_possibilities_layer2.json")
JOINS = os.path.join(REPO, "reports", "layer2_joins.json")
ALL_COLUMNS = os.path.join(REPO, "reports", "_all_columns.csv")
OUT = os.path.join(REPO, "reports", "count_possibilities_unified.html")

sys.path.insert(0, os.path.join(REPO, "scripts", "census"))
from count_naming import humanize  # noqa: E402
from count_possibilities import (  # noqa: E402
    classify, curated, entity_noun, KNOWN_IDS, PLUMBING, PLUMBING_EXACT,
)

# Nothing fancy: one plain-English word per role, reusing the same classifier
# already trusted for the count questions. Not a curated definition -- just
# enough to know what you're looking at before you write your own SQL.
ROLE_WORD = {
    "name": "a name", "category": "a category", "geo": "a place",
    "flag": "yes or no", "money": "a dollar amount", "quantity": "a number",
    "date": "a date", "other": "a text value",
}


def column_definition(fqn, name, dtype, noun):
    up = name.upper()
    gloss = curated(fqn, name)
    if gloss:
        return gloss
    role = classify(name, dtype)
    if role == "id":
        if up in KNOWN_IDS:
            return KNOWN_IDS[up][1]
        e = entity_noun(name, noun)
        if e:
            return f"identifies this {noun}" if e == noun else f"identifies a {e}"
        return "an identifier"
    if role == "skip":
        if PLUMBING.match(up) or up in PLUMBING_EXACT:
            return "internal tracking, not part of the underlying data"
        return "free text"
    return ROLE_WORD.get(role, "a value")


def load_columns():
    """Every column of every table, name + ordinal, straight from the warehouse."""
    cols = {}
    with open(ALL_COLUMNS, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            cols.setdefault((r["schema"], r["table"]), []).append(
                (r["column"], r["dtype"], int(r["ordinal"])))
    for k in cols:
        cols[k].sort(key=lambda c: c[2])
    return cols

# Tier 0: every kind from layer 1, unchanged order.
TIER0_KINDS = [
    "How many in total", "How many per year", "How many different things",
    "How many each one has", "How many different things per year",
    "How many arrived and left", "How many of each kind", "How the mix moved",
    "How many in each place", "How many different things per place",
    "How many are flagged", "How many kinds exist", "How many have a value",
    "How many show up more than once", "How many pass a threshold",
    "How many are missing it", "How many across two tables",
]
# Tier 1: layer 2's cross-tabs and shares. Tier 2: layer 2's proven-real joins.
TIER1_KINDS = [
    "Kind by place", "Place by year", "Category by category",
    "What percent is each kind", "What percent is each place",
    "What percent is flagged", "What percent repeats",
]
TIER2_KINDS = ["The real overlap"]

KIND_CHIP = {
    "How many in total": "the total", "How many per year": "per year",
    "How many different things": "distinct things", "How many each one has": "each one's share",
    "How many different things per year": "things per year", "How many arrived and left": "new arrivals",
    "How many of each kind": "by kind", "How the mix moved": "mix over time",
    "How many in each place": "by place", "How many different things per place": "things per place",
    "How many are flagged": "flags", "How many kinds exist": "how many kinds",
    "How many have a value": "fill check", "How many show up more than once": "duplicates",
    "How many pass a threshold": "over a threshold", "How many are missing it": "blanks",
    "How many across two tables": "needs a join",
    "Kind by place": "kind × place", "Place by year": "place × year",
    "Category by category": "kind × kind", "What percent is each kind": "kind share",
    "What percent is each place": "place share", "What percent is flagged": "flag share",
    "What percent repeats": "repeat rate", "The real overlap": "real join",
}

TIER_LABEL = ["plain counts", "cross & share", "real joins"]
NO_DESCRIPTION = "No plain-English description has been written for this dataset yet."


def load_joins():
    if not os.path.exists(JOINS):
        return []
    return json.load(open(JOINS, encoding="utf-8")).get("entries", [])


def pack():
    d1 = json.load(open(SRC1, encoding="utf-8"))
    d2 = json.load(open(SRC2, encoding="utf-8"))
    join_entries = load_joins()

    kinds = TIER0_KINDS + TIER1_KINDS + TIER2_KINDS + ["Other"]
    kind_i = {k: i for i, k in enumerate(kinds)}
    kind_tier = ([0] * len(TIER0_KINDS)) + ([1] * len(TIER1_KINDS)) + ([2] * len(TIER2_KINDS)) + [0]

    # All three sources describe the same 647 tables (verified: identical table
    # sets in both source JSONs). One merged table list, one merged entry list.
    tables_by_name = {t["table"]: t for t in d1["tables"]}
    all_entries = []
    for e in d1["entries"]:
        all_entries.append((e, 0, 0 if e["needs"] == "one table" else 1))
    for e in d2["entries"]:
        tier = 2 if e["kind"] == "The real overlap" else 1
        all_entries.append((e, tier, 1 if tier == 2 else 0))
    for e in join_entries:
        all_entries.append((e, 2, 1))

    per_table = Counter(e["table"] for e, _, _ in all_entries)
    per_table_tier = Counter()
    for e, tier, _ in all_entries:
        per_table_tier[(e["table"], tier)] += 1

    all_cols = load_columns()
    order = [t["table"] for t in d1["tables"]]  # both sources share one table order
    tables, index = [], {}
    for name in order:
        if per_table.get(name, 0) == 0:
            continue
        t = tables_by_name[name]
        index[name] = len(tables)
        schema, tbl = name.split(".", 1)
        fqn = f"LIBRARY_MARTS.{name}"
        colref = [[cname, column_definition(fqn, cname, dtype, t["noun"])]
                  for cname, dtype, _ in all_cols.get((schema, tbl), [])]
        tables.append([
            t["table"], t["subject"], t["dataset"], t["noun"],
            t["rows"] if t["rows"] is not None else -1,
            1 if t["noun_known"] else 0,
            per_table.get(name, 0),
            0 if t["dataset"].startswith(NO_DESCRIPTION[:40]) else 1,
            per_table_tier.get((name, 0), 0),
            per_table_tier.get((name, 1), 0),
            per_table_tier.get((name, 2), 0),
            colref,
        ])

    entries = []
    for e, tier, needs in all_entries:
        entries.append([
            index[e["table"]], kind_i.get(e["kind"], len(kinds) - 1),
            e["question"], e["means"], e["sql"], needs, tier,
        ])
    return tables, entries, kinds, kind_tier, len(join_entries)


def build():
    tables, entries, kinds, kind_tier, n_joins_run = pack()
    subjects = sorted({t[1] for t in tables})
    tier_counts = Counter(e[6] for e in entries)

    payload = json.dumps({
        "t": tables, "e": entries, "k": kinds,
        "c": [KIND_CHIP.get(k, k) for k in kinds],
        "kt": kind_tier,
    }, separators=(",", ":"), ensure_ascii=False)

    options = "".join(f'<option value="{html.escape(s)}">{html.escape(s)}</option>' for s in subjects)
    kindchips = "".join(
        f'<button class="chip" data-kind="{i}" data-tier="{kind_tier[i]}" aria-pressed="false">'
        f'{html.escape(KIND_CHIP.get(k, k))}</button>'
        for i, k in enumerate(kinds) if k != "Other")

    doc = TEMPLATE.replace("__PAYLOAD__", payload)
    doc = doc.replace("__OPTIONS__", options).replace("__KINDCHIPS__", kindchips)
    doc = doc.replace("__N_TOTAL__", f"{len(entries):,}")
    doc = doc.replace("__N_TABLES__", f"{len(tables):,}")
    doc = doc.replace("__N_TIER0__", f"{tier_counts.get(0, 0):,}")
    doc = doc.replace("__N_TIER1__", f"{tier_counts.get(1, 0):,}")
    doc = doc.replace("__N_TIER2__", f"{tier_counts.get(2, 0):,}")
    doc = doc.replace("__N_JOINS_TOTAL__", "206")
    if n_joins_run:
        join_note = (f'<strong>{n_joins_run:,} real joins have been run</strong> against the warehouse '
                      f"and show actual match/no-match counts.")
    else:
        join_note = ('<strong>The real joins have not been run yet.</strong> 206 pairs are queued and '
                      "priced, waiting on a go-ahead before touching the warehouse.")
    doc = doc.replace("__JOIN_NOTE__", join_note)
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)
    return OUT, len(entries), len(tables)


TEMPLATE = r"""<title>Ask The Warehouse</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lexend:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
:root {
  /* Chris's palette, 2026-08-20: #264653 #2a9d8f #e9c46a #f4a261 #e76f51 -- used
     directly as the ink/ui/t0/t1/t2 anchors below; everything else (neutrals,
     -soft tints, dark-mode steps) is derived from those five, not invented fresh. */
  --ground:#eef4f4; --surface:#ffffff; --sunk:#e2edee; --ink:#264653; --ink-2:#4c6b73;
  --muted:#7e969c; --line:#cddbdd; --hover:#e0edef;
  --ui:#2a9d8f;
  --t0:#e9c46a; --t0-soft:#faf1d9; --t1:#f4a261; --t1-soft:#fce8d5; --t2:#e76f51; --t2-soft:#fce1d8;
  /* Fixed regardless of theme: t0/t1/t2 are light fills (need dark text on top),
     --ui is a dark fill (needs light text on top) -- true in both light and dark mode. */
  --on-accent-dark:#1c333c; --on-accent-light:#fbfdfc;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:#1c2f36; --surface:#264653; --sunk:#16262b; --ink:#f3ede0; --ink-2:#c8d6d6;
    --muted:#8fa8ad; --line:#3a5b64; --hover:#2e4750;
    --ui:#4dbaa8;
    --t0:#e9c46a; --t0-soft:#3a3016; --t1:#f4a261; --t1-soft:#3a2916; --t2:#ef8368; --t2-soft:#3a2019;
  }
}
:root[data-theme="dark"] {
  --ground:#1c2f36; --surface:#264653; --sunk:#16262b; --ink:#f3ede0; --ink-2:#c8d6d6;
  --muted:#8fa8ad; --line:#3a5b64; --hover:#2e4750;
  --ui:#4dbaa8;
  --t0:#e9c46a; --t0-soft:#3a3016; --t1:#f4a261; --t1-soft:#3a2916; --t2:#ef8368; --t2-soft:#3a2019;
}
* { box-sizing:border-box; }
body {
  background:var(--ground); color:var(--ink); margin:0;
  font-family:"Lexend", system-ui, -apple-system, "Segoe UI", sans-serif;
  font-size:16px; line-height:1.6; -webkit-font-smoothing:antialiased;
}
.wrap { max-width:920px; margin:0 auto; padding:0 24px 72px; }
header.top { padding:28px 0 12px; }
.eyebrow {
  font-family:"IBM Plex Mono", monospace; font-size:11px; letter-spacing:0.14em;
  text-transform:uppercase; color:var(--ui); margin:0 0 6px;
}
h1 {
  font-family:"Lexend", sans-serif; font-weight:600;
  font-size:clamp(24px, 4vw, 32px); line-height:1.2; letter-spacing:0;
  margin:0 0 6px; text-wrap:balance;
}
.lede { font-size:14.5px; color:var(--ink-2); margin:0; max-width:72ch; }
.lede strong { color:var(--ink); font-weight:600; }

/* ---- one control bar: search+subject, then tier, then kind ---------------- */
.bar {
  position:sticky; top:10px; z-index:30; background:var(--surface);
  padding:12px 14px 10px; border:1px solid var(--line); border-radius:8px;
  margin-top:14px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
}
.row1 { display:flex; gap:8px; align-items:stretch; }
#q {
  flex:1 1 auto; min-width:0; padding:11px 13px; font:inherit; font-size:15px;
  color:var(--ink); background:var(--surface); border:1px solid var(--line); border-radius:3px;
}
#q:focus { outline:2px solid var(--ui); outline-offset:1px; border-color:var(--ui); }
#q::placeholder { color:var(--muted); }
#subject {
  flex:0 0 auto; max-width:42%; padding:11px 10px; font:inherit; font-size:14px;
  color:var(--ink); background:var(--surface); border:1px solid var(--line);
  border-radius:3px; cursor:pointer;
}
#subject:focus { outline:2px solid var(--ui); outline-offset:1px; }

#tiers { display:flex; gap:6px; padding:10px 0 0; flex-wrap:wrap; }
.tier {
  font:inherit; font-size:12.5px; font-weight:500; padding:5px 12px; border-radius:999px;
  cursor:pointer; white-space:nowrap; background:transparent; border:1px solid var(--line);
  color:var(--ink-2); display:flex; align-items:center; gap:6px;
}
.tier .n { font-family:"IBM Plex Mono", monospace; font-size:10.5px; opacity:0.75; font-variant-numeric:tabular-nums; }
.tier .dot { width:7px; height:7px; border-radius:50%; background:var(--muted); flex:0 0 auto; }
.tier[data-tier=""] .dot { background:var(--ui); }
.tier[data-tier="0"] .dot { background:var(--t0); }
.tier[data-tier="1"] .dot { background:var(--t1); }
.tier[data-tier="2"] .dot { background:var(--t2); }
.tier[data-tier=""]:hover { border-color:var(--ui); }
.tier[data-tier="0"]:hover { border-color:var(--t0); }
.tier[data-tier="1"]:hover { border-color:var(--t1); }
.tier[data-tier="2"]:hover { border-color:var(--t2); }
.tier[data-tier=""][aria-pressed="true"] { background:var(--ui); border-color:var(--ui); color:var(--on-accent-light); }
.tier[data-tier="0"][aria-pressed="true"] { background:var(--t0); border-color:var(--t0); color:var(--on-accent-dark); }
.tier[data-tier="1"][aria-pressed="true"] { background:var(--t1); border-color:var(--t1); color:var(--on-accent-dark); }
.tier[data-tier="2"][aria-pressed="true"] { background:var(--t2); border-color:var(--t2); color:var(--on-accent-dark); }
.tier[aria-pressed="true"] .dot { background:currentColor; }
.tier[aria-pressed="true"] .n { opacity:0.85; }
.tier:focus-visible { outline:2px solid var(--ui); outline-offset:2px; }

#kinds { display:flex; gap:5px; overflow-x:auto; padding:8px 1px 2px; scrollbar-width:thin; }
.chip {
  font:inherit; font-size:12px; padding:4px 10px; border-radius:999px; cursor:pointer;
  color:var(--ink-2); white-space:nowrap; background:transparent;
  border:1px solid var(--line); flex:0 0 auto;
}
.chip:hover { border-color:var(--ui); color:var(--ui); }
.chip[data-tier=""][aria-pressed="true"] { background:var(--ui); border-color:var(--ui); color:var(--on-accent-light); }
.chip[data-tier="0"][aria-pressed="true"] { background:var(--t0); border-color:var(--t0); color:var(--on-accent-dark); }
.chip[data-tier="1"][aria-pressed="true"] { background:var(--t1); border-color:var(--t1); color:var(--on-accent-dark); }
.chip[data-tier="2"][aria-pressed="true"] { background:var(--t2); border-color:var(--t2); color:var(--on-accent-dark); }
.chip:focus-visible { outline:2px solid var(--ui); outline-offset:2px; }

/* ---- breadcrumb + tally ------------------------------------------------- */
.status {
  display:flex; align-items:baseline; justify-content:space-between; gap:16px;
  flex-wrap:wrap; padding:10px 0 2px;
}
#crumb { font-size:14px; color:var(--ink-2); }
#crumb button {
  font:inherit; font-size:14px; color:var(--ui); background:none; border:none;
  padding:0; cursor:pointer; text-decoration:underline; text-underline-offset:2px;
}
#crumb button:focus-visible { outline:2px solid var(--ui); outline-offset:2px; }
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
.ds:focus-visible { outline:2px solid var(--ui); outline-offset:-2px; }
.ds .name {
  font-family:"Lexend", sans-serif; font-size:16px; font-weight:600;
  line-height:1.3; letter-spacing:0; display:block; margin-bottom:1px;
}
.ds .about {
  display:block; color:var(--ink-2); font-size:13px; margin-bottom:3px;
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
}
.ds .meta {
  font-family:"IBM Plex Mono", monospace; font-size:11px; color:var(--muted);
  font-variant-numeric:tabular-nums; display:flex; align-items:center; gap:5px; flex-wrap:wrap;
}
.ds .meta .dot { opacity:0.5; padding:0 2px; }
.tb { display:inline-flex; align-items:center; gap:3px; }
.tb i { width:6px; height:6px; border-radius:50%; display:inline-block; opacity:0.72; transition:opacity .1s; }
.ds:hover .tb i, .ds:focus-visible .tb i { opacity:1; }
.tb.t0 i { background:var(--t0); } .tb.t1 i { background:var(--t1); } .tb.t2 i { background:var(--t2); }
.groupname i.t0 { background:var(--t0); } .groupname i.t1 { background:var(--t1); } .groupname i.t2 { background:var(--t2); }

/* ---- an opened dataset -------------------------------------------------- */
.head {
  margin:14px 0 4px; padding:14px 16px 16px; background:var(--surface);
  border:1px solid var(--line); border-radius:8px;
}
.head h2 {
  font-family:"Lexend", sans-serif; font-weight:600; font-size:22px;
  letter-spacing:0; margin:0 0 3px; text-wrap:balance;
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
  display:flex; align-items:center; gap:6px;
}
.groupname i { width:6px; height:6px; border-radius:50%; display:inline-block; }

/* ---- the full column reference for an opened dataset -------------------- */
.cols { margin:10px 0 0; }
.cols summary {
  cursor:pointer; font-size:12.5px; color:var(--muted); font-family:"IBM Plex Mono", monospace;
  padding:6px 0; list-style:none; display:flex; align-items:center; gap:5px;
}
.cols summary::before { content:'▸'; font-size:10px; }
.cols[open] summary::before { content:'▾'; }
.cols summary:hover { color:var(--ui); }
.cols summary::-webkit-details-marker { display:none; }
.colgrid {
  border:1px solid var(--line); border-radius:4px; background:var(--sunk);
  max-height:340px; overflow-y:auto; margin:4px 0 4px;
}
.colrow {
  display:flex; gap:12px; padding:5px 10px; border-top:1px solid var(--line);
  font-size:12.5px; align-items:baseline;
}
.colrow:first-child { border-top:none; }
.colrow code {
  font-family:"IBM Plex Mono", monospace; font-size:11.5px; color:var(--ink);
  flex:0 0 auto; min-width:180px; max-width:280px; word-break:break-all;
}
.colrow span { color:var(--ink-2); }

/* ---- one question: a single line until it is opened ---------------------- */
.item { border-top:1px solid var(--line); }
.qrow { display:flex; align-items:flex-start; gap:8px; }
.qbtn {
  flex:1 1 auto; min-width:0; text-align:left; font:inherit; cursor:pointer;
  background:none; border:none; padding:6px 0 6px 8px; color:inherit;
  font-family:"Lexend", sans-serif; font-size:14px; line-height:1.5;
  letter-spacing:0; display:flex; gap:8px; align-items:baseline;
}
.qbtn:hover { color:var(--ui); }
.qbtn:focus-visible { outline:2px solid var(--ui); outline-offset:-2px; }
.qbtn .caret {
  flex:0 0 auto; font-family:"IBM Plex Mono", monospace; font-size:11px;
  color:var(--muted); width:9px;
}
.item.open .qbtn, .item.open .qbtn .caret { color:var(--ui); }
.copy {
  flex:0 0 auto; margin:6px 8px 0 0; font:inherit; font-size:10.5px;
  font-family:"IBM Plex Mono", monospace; letter-spacing:0.04em;
  padding:2px 8px; border-radius:3px; cursor:pointer; align-self:flex-start;
  background:var(--surface); color:var(--muted); border:1px solid var(--line);
  min-width:56px; text-align:center;
}
.copy:hover { color:var(--ui); border-color:var(--ui); }
.copy:focus-visible { outline:2px solid var(--ui); outline-offset:2px; }
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
  background:var(--t2-soft); color:var(--ink);
  font-family:"IBM Plex Mono", monospace; font-size:10.5px;
}

#more {
  display:block; width:100%; margin:26px 0 0; padding:13px; cursor:pointer;
  font:inherit; font-size:14px; color:var(--ui); background:var(--surface);
  border:1px solid var(--line); border-radius:3px;
}
#more:hover { border-color:var(--ui); }
#more[hidden] { display:none; }
.empty { padding:44px 8px; color:var(--muted); font-size:15px; }
.note {
  margin-top:32px; padding:16px 20px; background:var(--surface);
  border:1px solid var(--line); border-radius:4px;
}
.note h2 { font-family:"Lexend", sans-serif; font-weight:600; margin:0 0 9px; font-size:17px; }
.note ul { margin:0; padding-left:17px; }
.note li { margin:0 0 8px; color:var(--ink-2); font-size:13.5px; line-height:1.6; max-width:68ch; }
.note li:last-child { margin-bottom:0; }
.note strong { color:var(--ink); font-weight:600; }
#top {
  position:fixed; right:20px; bottom:20px; z-index:40; display:none;
  font:inherit; font-size:12px; font-family:"IBM Plex Mono", monospace;
  padding:8px 12px; border-radius:3px; cursor:pointer;
  background:var(--surface); color:var(--ink-2); border:1px solid var(--line);
  box-shadow:0 1px 4px rgba(0,0,0,0.14);
}
#top:hover { color:var(--ui); border-color:var(--ui); }
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
  <p class="eyebrow">Every count, cross, and real join in one place</p>
  <h1>__N_TOTAL__ things you can ask the warehouse</h1>
  <p class="lede">Across <strong>__N_TABLES__ datasets</strong>, in three tiers: __N_TIER0__ plain counts,
  __N_TIER1__ cross-tabs and shares, and __N_JOINS_TOTAL__ real two-table joins. Click a tier or a kind below
  to browse the whole warehouse by that alone, or open a dataset to see everything it can answer.
  Nothing below has been run except the joins marked so. __JOIN_NOTE__</p>
</header>

<div class="bar">
  <div class="row1">
    <input id="q" type="search" placeholder="Search everything &mdash; judge, mine, opioid, per year&hellip;    press /" autocomplete="off">
    <select id="subject" aria-label="Filter by subject">
      <option value="">All subjects</option>
      __OPTIONS__
    </select>
  </div>
  <div id="tiers">
    <button class="tier" data-tier="" aria-pressed="true"><span class="dot"></span>everything</button>
    <button class="tier" data-tier="0" aria-pressed="false"><span class="dot"></span>plain counts <span class="n">__N_TIER0__</span></button>
    <button class="tier" data-tier="1" aria-pressed="false"><span class="dot"></span>cross &amp; share <span class="n">__N_TIER1__</span></button>
    <button class="tier" data-tier="2" aria-pressed="false"><span class="dot"></span>real joins <span class="n">__N_TIER2__</span></button>
  </div>
  <div id="kinds">
    <button class="chip" data-kind="" data-tier="" aria-pressed="true">every kind</button>
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
    <li><strong>Rows &ne; things.</strong> Check &ldquo;different things&rdquo; against the row count &mdash; a big gap means one thing shows up many times. The &ldquo;repeat rate&rdquo; questions say this as a percent directly.</li>
    <li><strong>Blank &ne; zero.</strong> Run the &ldquo;missing&rdquo; count first, or a breakdown quietly drops rows and still looks clean.</li>
    <li><strong>A share is one division past a count</strong> &mdash; the number and its percent of the total sit side by side, so a &ldquo;top&rdquo; result can't be mistaken for a big one just because it's first.</li>
    <li><strong>Cross-tabs stay inside one table</strong> &mdash; kind by place, place by year &mdash; no join, just two of the same table's own columns at once. A real join only runs once the key is already proven live in both tables, not a guess at a match.</li>
    <li><strong>Rising counts often mean rising coverage,</strong> not a rising world &mdash; check the per-year &ldquo;different things&rdquo; count too.</li>
    <li><strong>Three or more tables, entity resolution, and the full connection map are the next tier up</strong> &mdash; not here on purpose.</li>
  </ul>
</div>
</div>

<button id="top" type="button">&uarr; top</button>

<script id="data" type="application/json">__PAYLOAD__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
const T = DATA.t, E = DATA.e, K = DATA.k, C = DATA.c, KT = DATA.kt;
const PAGE = 150;
const TDOT = ['t0', 't1', 't2'];

const hay = E.map(e => (e[2] + ' ' + e[3] + ' ' + T[e[0]][0] + ' ' + T[e[0]][2]).toLowerCase());
const tHay = T.map(t => (t[0] + ' ' + t[2] + ' ' + t[3] + ' ' + t[1]).toLowerCase());

const byTable = T.map(() => []);
E.forEach((e, i) => byTable[e[0]].push(i));
const tOrder = T.map((t, i) => i).sort((a, b) => T[b][4] - T[a][4]);
const tRank = new Array(T.length);
tOrder.forEach((idx, rank) => { tRank[idx] = rank; });

const q = document.getElementById('q');
const subjectSel = document.getElementById('subject');
const tiersRow = document.getElementById('tiers');
const kindsRow = document.getElementById('kinds');
const results = document.getElementById('results');
const crumb = document.getElementById('crumb');
const tally = document.getElementById('tally');
const more = document.getElementById('more');
const topBtn = document.getElementById('top');

let subject = '', tier = '', kind = '', openTable = -1, shown = 0, matches = [], mode = 'index';

function esc(s) {
  return String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
}
function rowText(n) { return n < 0 ? 'row count unknown' : n.toLocaleString() + ' rows'; }
function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

function shortName(fqn) {
  const tail = fqn.split('.').pop();
  return (tail.includes('__') ? tail.split('__').slice(1).join(' ') : tail)
    .replace(/_/g, ' ').toLowerCase();
}
function title(t) { return t[5] ? cap(t[3]) : cap(shortName(t[0])); }
function about(t) { return t[7] ? t[2] : 'No description written for this one yet.'; }
function terms() { const s = q.value.trim().toLowerCase(); return s ? s.split(/\s+/) : []; }
function hit(text, ts) { for (const w of ts) if (!text.includes(w)) return false; return true; }
function backLink() { return '<button type="button" id="back">&larr; all datasets</button>'; }
function columnsBlock(t) {
  const cols = t[11] || [];
  if (!cols.length) return '';
  const rows = cols.map(c =>
    '<div class="colrow"><code>' + esc(c[0]) + '</code><span>' + esc(c[1]) + '</span></div>').join('');
  return '<details class="cols"><summary>All ' + cols.length + ' columns in this table</summary>' +
    '<div class="colgrid">' + rows + '</div></details>';
}
function tierBreakdown(t) {
  const parts = [];
  if (t[8]) parts.push('<span class="tb t0"><i></i>' + t[8] + '</span>');
  if (t[9]) parts.push('<span class="tb t1"><i></i>' + t[9] + '</span>');
  if (t[10]) parts.push('<span class="tb t2"><i></i>' + t[10] + '</span>');
  return parts.join('');
}

/* ---------- which of the three views is on screen ------------------------ */
function update() {
  const ts = terms();
  const filtered = ts.length || tier !== '' || kind !== '';
  mode = openTable >= 0 ? 'dataset' : (filtered ? 'browse' : 'index');
  shown = 0;
  results.innerHTML = '';
  more.hidden = true;
  if (mode === 'index') renderIndex(ts);
  else computeMatches(ts);
}

/* ---------- the landing view: the datasets themselves -------------------- */
function renderIndex(ts) {
  const list = tOrder.filter(i =>
    (!subject || T[i][1] === subject) && T[i][6] > 0 && (!ts.length || hit(tHay[i], ts)));
  crumb.textContent = 'Every dataset, biggest first. Click one, or pick a tier above to browse by that instead.';
  tally.textContent = list.length.toLocaleString() + ' datasets · ' +
    E.length.toLocaleString() + ' questions';
  if (!list.length) {
    results.innerHTML = '<p class="empty">No dataset matches that.</p>';
    return;
  }
  results.innerHTML = list.map(i => {
    const t = T[i];
    return '<button class="ds" data-table="' + i + '" type="button">' +
      '<span class="name">' + esc(title(t)) + '</span>' +
      '<span class="about">' + esc(about(t)) + '</span>' +
      '<span class="meta">' + tierBreakdown(t) + '<span class="dot">&middot;</span>' +
      rowText(t[4]) + '<span class="dot">&middot;</span>' + esc(t[1]) +
      (title(t).toLowerCase() !== shortName(t[0])
        ? '<span class="dot">&middot;</span>' + esc(shortName(t[0])) : '') +
      '</span></button>';
  }).join('');
}

/* ---------- questions, inside one dataset or across a browse/search ------ */
function computeMatches(ts) {
  const pool = openTable >= 0 ? byTable[openTable] : E.map((_, i) => i);
  matches = [];
  for (const i of pool) {
    const e = E[i], t = T[e[0]];
    if (openTable < 0 && subject && t[1] !== subject) continue;
    if (tier !== '' && e[6] !== +tier) continue;
    if (kind !== '' && e[1] !== +kind) continue;
    if (ts.length && !hit(hay[i], ts)) continue;
    matches.push(i);
  }
  matches.sort((a, b) =>
    (tRank[E[a][0]] - tRank[E[b][0]]) || (E[a][6] - E[b][6]) || (E[a][1] - E[b][1]) || (a - b));

  if (openTable >= 0) {
    const t = T[openTable];
    crumb.innerHTML = backLink();
    results.innerHTML =
      '<div class="head"><h2>' + esc(title(t)) + '</h2>' +
      '<p class="about">' + esc(about(t)) + '</p>' +
      '<p class="src">' + esc(t[0]) + '<span class="dot">&middot;</span>' + esc(t[1]) +
      '<span class="dot">&middot;</span>' + rowText(t[4]) + '</p>' +
      columnsBlock(t) + '</div>';
  } else {
    crumb.innerHTML = backLink() + '&nbsp; matches across every dataset';
  }
  tally.textContent = matches.length.toLocaleString() + ' question' +
    (matches.length === 1 ? '' : 's');
  if (!matches.length) {
    const msg = (tier === '2' && !ts.length)
      ? 'The 206 real joins haven&rsquo;t been run yet &mdash; nothing to show here until they are.'
      : 'Nothing matches. Try a plainer word &mdash; the questions are written in ordinary English.';
    results.insertAdjacentHTML('beforeend', '<p class="empty">' + msg + '</p>');
    return;
  }
  renderMatches();
}

function renderMatches() {
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
      out += '<p class="groupname"><i class="' + TDOT[e[6]] + '"></i>' + esc(C[e[1]] || K[e[1]]) + '</p>';
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
        (e[5] ? '<span class="needs">' + (e[6] === 2 ? 'run against the warehouse &mdash; real numbers' : 'needs two tables joined') + '</span>' : '') +
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
    openTable = +ds.dataset.table;
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
    openTable = -1; update(); scrollTo({top: 0});
  }
});

function setTierChip(val) {
  tiersRow.querySelectorAll('.tier').forEach(x =>
    x.setAttribute('aria-pressed', x.dataset.tier === val ? 'true' : 'false'));
}
function setKindChip(val) {
  kindsRow.querySelectorAll('.chip').forEach(x =>
    x.setAttribute('aria-pressed', x.dataset.kind === val ? 'true' : 'false'));
}
function rebuildKindRow() {
  kindsRow.querySelectorAll('.chip').forEach(x => {
    const t = x.dataset.tier;
    x.style.display = (tier === '' || t === '' || t === tier) ? '' : 'none';
  });
}

tiersRow.addEventListener('click', ev => {
  const b = ev.target.closest('.tier');
  if (!b) return;
  tier = b.dataset.tier;
  if (kind !== '' && (tier === '' || String(KT[+kind]) !== tier)) kind = '';
  setTierChip(tier);
  setKindChip(kind);
  rebuildKindRow();
  update();
});

kindsRow.addEventListener('click', ev => {
  const c = ev.target.closest('.chip');
  if (!c) return;
  kind = c.dataset.kind;
  if (kind !== '') { tier = String(KT[+kind]); setTierChip(tier); rebuildKindRow(); }
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
more.addEventListener('click', renderMatches);

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
    print(f"{n:,} questions across {t:,} tables -> {path} ({os.path.getsize(path)/1e6:.1f} MB)")
