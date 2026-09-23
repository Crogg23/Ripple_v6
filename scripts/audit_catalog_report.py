"""Analyze stage of scripts/audit_catalog.py. Local only, reads the cache.

Writes audit/catalog_audit_<date>.md (the walk-through) and
audit/catalog_audit_<date>.tsv (one row per finding, the shape
LIBRARY_META.AUDIT.CATALOG_AUDIT would take).
"""

from __future__ import annotations

import collections
import csv
import glob
import gzip
import json
import re
from pathlib import Path

import yaml

from audit_catalog import (CACHE, HARD_KEYS, NAME_OK, OUT, REPO, TODAY, column_rows, load_inventory)

GEO_KEYS = {"FIPS", "ZIP", "COUNTRY", "LATLON", "GEOM"}
BACKUP = re.compile(r"__PREV|_PREV_|_BAK|^ZZ_|_OLD$|_TMP$|_COPY$|_BACKUP|_RESTORE", re.I)
MATCH_MIN_PCT = 5.0      # share of A's distinct IDs found in B for a link to count
MATCH_MIN_N = 50         # and at least this many shared IDs


def _dbt_words():
    """Table and column descriptions from every mart YAML, keyed by upper table name."""
    tdesc, cdesc, has_yml = {}, collections.defaultdict(dict), set()
    for f in glob.glob(str(REPO / "library-onboarding/ripple_dbt/models/marts/**/*.yml"), recursive=True):
        y = yaml.safe_load(open(f, encoding="utf-8")) or {}
        for m in y.get("models", []) or []:
            t = str(m.get("name", "")).upper()
            has_yml.add(t)
            if m.get("description"):
                tdesc[t] = m["description"]
            for c in m.get("columns", []) or []:
                if c.get("description"):
                    cdesc[t][str(c["name"]).upper()] = c["description"]
    return tdesc, cdesc, has_yml


def _time_registry():
    p = REPO / "library-onboarding/ripple_dbt/seeds/ripple_time_registry.csv"
    return {r["table_name"]: r for r in csv.DictReader(open(p, encoding="utf-8"))}


def cmd_analyze():
    OUT.mkdir(exist_ok=True)
    inv = load_inventory()
    tabs = {f"{t['S']}.{t['T']}": t for t in inv["tabs"]}
    vcounts = json.load(open(CACHE / "view_counts.json")) if (CACHE / "view_counts.json").exists() else {}
    rows = column_rows()
    F = []  # findings

    def find(table, column, check, result, severity, fix):
        F.append({"table": table, "column": column or "", "check": check, "result": result,
                  "severity": severity, "proposed_fix": fix})

    # ---------------- C1 inventory ----------------
    n_base = sum(1 for t in tabs.values() if t["TY"] == "BASE TABLE")
    n_view = sum(1 for t in tabs.values() if t["TY"] == "VIEW")
    for k, t in tabs.items():
        if t["TY"] == "VIEW":
            c = vcounts.get(k, "not counted")
            find(k, None, "C1 view counted as a table", f"view; real rows {c}", "minor",
                 "catalog reads table_type and counts views with COUNT(*)")
    backups = {k: t for k, t in tabs.items() if BACKUP.search(t["T"])}
    for k, t in backups.items():
        find(k, None, "C1 backup copy in catalog", f"{t['R'] or 0:,} rows", "moderate",
             "leave the catalog now; drop only on greenlight destroy after reader check")
    sig = collections.defaultdict(list)
    colsets = collections.defaultdict(list)
    for c in inv["cols"]:
        colsets[f"{c['S']}.{c['T']}"].append(c["C"])
    for k, t in tabs.items():
        if t["TY"] == "BASE TABLE" and not backups.get(k):
            sig[(tuple(colsets[k]), t["R"])].append(k)
    dupes = [v for v in sig.values() if len(v) > 1]
    for grp in dupes:
        for k in grp:
            find(k, None, "C1 exact duplicate", "same columns and row count as " + ", ".join(x for x in grp if x != k),
                 "moderate", "keep one, drop the rest on greenlight destroy")
    sample_err = {}
    for k in tabs:
        p = CACHE / "samples" / f"{k}.json.gz"
        if p.exists():
            with gzip.open(p, "rt", encoding="utf-8") as f:
                e = json.load(f)["error"]
            if e:
                sample_err[k] = e
                find(k, None, "C1 object will not open", e[:160], "severe", "repair or retire the view")
    schema_n = collections.Counter(t["S"] for t in tabs.values())

    # ---------------- C2 tag truth ----------------
    def verdict(pct, filled):
        if filled == 0:
            return "EMPTY"
        if pct is None:
            return "NO SHAPE TEST"
        return "PASS" if pct >= 90 else "WEAK" if pct >= 50 else "FAIL"

    tag_stats = {"regex": collections.defaultdict(collections.Counter), "real": collections.defaultdict(collections.Counter)}
    for r in rows:
        for label in ("regex", "real"):
            tag = r[f"{label}_tag"]
            if not tag:
                continue
            if tag in ("NAME", "ORG_NAME"):
                v = r.get("names_holds", "empty")
                v = "PASS" if v in NAME_OK else ("EMPTY" if v == "empty" else "FAIL")
            else:
                v = verdict(r[f"{label}_shape_pct"], r["filled"])
            r[f"{label}_verdict"] = v
            tag_stats[label][tag][v] += 1
        if r["real_tag"] and r.get("real_verdict") in ("FAIL", "EMPTY") and r["real_tag"] != "NAME":
            find(f"{r['schema']}.{r['table']}", r["column"], "C2 tag fails its format",
                 f"{r['real_tag']}: {r['real_shape_pct']}% of {r['filled']} sampled values fit; e.g. {r['examples'][:3]}"
                 if r["filled"] else f"{r['real_tag']}: 0 of {r['sampled']} sampled rows filled",
                 "severe" if r["real_tag"] in HARD_KEYS else "moderate",
                 "fix the rule in connect/keys.py or portal_recon/tag_portal_index.py, then re-tag")
        if r["regex_tag"] and r.get("regex_verdict") == "FAIL" and r["regex_tag"] != "ORG_NAME":
            find(f"{r['schema']}.{r['table']}", r["column"], "C2 catalog regex tag wrong",
                 f"{r['regex_tag']}: {r['regex_shape_pct']}% fit; e.g. {r['examples'][:3]}", "moderate",
                 "retire the regex catalog; tag with the platform tagger")
        if (r["regex_tag"] == "ORG_NAME" or r["real_tag"] == "NAME") and r.get("names_holds") not in NAME_OK | {"empty", None}:
            find(f"{r['schema']}.{r['table']}", r["column"], "C2 name tag holds something else",
                 f"{r.get('names_holds')}; org words {r.get('names_org_pct')}%, people {r.get('names_person_pct')}%; e.g. {r['examples'][:3]}",
                 "minor", "name keys only on columns holding organizations or people, graded PROBABILISTIC")

    # ---------------- C3 missing tags ----------------
    for r in rows:
        if r["real_tag"]:
            continue
        if r["value_looks_like"]:
            find(f"{r['schema']}.{r['table']}", r["column"], "C3 untagged key, by value",
                 f"{r['value_looks_like']} of distinct sampled values; e.g. {r['examples'][:3]}", "moderate",
                 "add a table-scoped rule or token rule, then re-tag")
        elif r["name_hint"] and r["filled"]:
            find(f"{r['schema']}.{r['table']}", r["column"], "C3 untagged key, by name",
                 f"name says {r['name_hint']}; e.g. {r['examples'][:3]}", "minor",
                 "decide if this key family joins the vocabulary")

    # ---------------- C4 links ----------------
    link_vals = {}
    for p in glob.glob(str(CACHE / "links" / "*.txt.gz")):
        k = Path(p).name[:-7]
        with gzip.open(p, "rt", encoding="utf-8") as f:
            link_vals[k] = set(x for x in f.read().split("\n") if x)
    col_key = {f"{r['schema']}.{r['table']}.{r['column']}": r["real_tag"] for r in rows}
    by_key = collections.defaultdict(list)
    for k, vals in link_vals.items():
        if BACKUP.search(k.split(".")[1]):
            continue  # a table matching its own backup is not a link
        by_key[col_key.get(k)].append((k, vals))
    pairs = []
    for key, cols in by_key.items():
        for a, av in cols:
            for b, bv in cols:
                ta, tb = a.rsplit(".", 1)[0], b.rsplit(".", 1)[0]
                if ta == tb or not av:
                    continue
                n = len(av & bv)
                pairs.append({"key": key, "a": a, "b": b, "a_ids": len(av), "shared": n,
                              "pct_of_a": round(100 * n / len(av), 2)})
    # small tables: a 20-ID table matching 20 of 20 works; the floor is min(50, A's size)
    works = lambda p: p["shared"] >= min(MATCH_MIN_N, p["a_ids"]) and p["pct_of_a"] >= MATCH_MIN_PCT
    table_link = collections.defaultdict(lambda: {"pairs": 0, "working": 0})
    for p in pairs:
        ta = p["a"].rsplit(".", 1)[0]
        table_link[ta]["pairs"] += 1
        table_link[ta]["working"] += works(p)
    hard_tables = {f"{r['schema']}.{r['table']}" for r in rows if r["real_tag"] in HARD_KEYS
                   and not BACKUP.search(r["table"])}
    for t in sorted(hard_tables):
        tl = table_link.get(t)
        if not tl or tl["pairs"] == 0:
            find(t, None, "C4 hard ID with no partner", "no other catalog table carries the same ID",
                 "minor", "a dead end until a partner table lands")
        elif tl["working"] == 0:
            find(t, None, "C4 hard ID matches nothing", f"{tl['pairs']} partner columns, none share "
                 f"{MATCH_MIN_PCT}% and {MATCH_MIN_N} IDs", "moderate", "check cleaning rule and vintage")

    # ---------------- C5 time ----------------
    treg = _time_registry()
    tl_views = {t["T"] for t in inv["timeline"] if t["TY"] == "VIEW"}
    time_rows = []
    date_cols = collections.defaultdict(list)
    for c in inv["cols"]:
        if c["D"] in ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_TZ", "TIMESTAMP_LTZ") and not c["C"].startswith("_"):
            date_cols[f"{c['S']}.{c['T']}"].append(c["C"])
    for k, t in tabs.items():
        reg = treg.get(t["T"], {})
        has_view = t["T"] in tl_views
        time_rows.append({"table": k, "timeline_view": has_view, "grain": reg.get("grain", ""),
                          "clock": reg.get("clock", ""), "date_columns": len(date_cols.get(k, []))})
        if not has_view and date_cols.get(k) and not backups.get(k):
            find(k, None, "C5 dates but no timeline view", f"{len(date_cols[k])} date columns, e.g. {date_cols[k][:3]}",
                 "minor", "add a row to ripple_time_registry and regenerate time views")

    # ---------------- C6 words ----------------
    tdesc, cdesc, has_yml = _dbt_words()
    friendly = {r["OBJECT_FQN"].split(".", 1)[1]: r for r in inv["friendly"]}
    colcat = collections.defaultdict(dict)
    for r in inv["colcat"]:
        colcat[r["FQN"].split(".", 1)[1]][r["COLUMN_NAME"]] = r["PLAIN_GLOSS"]
    words = []
    for k, t in tabs.items():
        cs = colsets[k]
        described = sum(1 for c in cs if cdesc.get(t["T"], {}).get(c) or colcat.get(k, {}).get(c))
        summary = bool(t.get("CM")) or bool(tdesc.get(t["T"])) or k in friendly
        words.append({"table": k, "summary": summary, "cols": len(cs), "cols_described": described,
                      "has_yml": t["T"] in has_yml})
    n_cols = sum(w["cols"] for w in words)
    n_desc = sum(w["cols_described"] for w in words)

    # ---------------- MAP parts ----------------
    real_hard = [r for r in rows if r["real_tag"] in HARD_KEYS | GEO_KEYS and r["real_tag"] not in ("LATLON", "GEOM")]
    empty_keys = sum(1 for r in real_hard if r.get("real_verdict") == "EMPTY")
    real_hard = [r for r in real_hard if r.get("real_verdict") not in ("NO SHAPE TEST", "EMPTY", None)]
    tags_true = sum(1 for r in real_hard if r.get("real_verdict") == "PASS")
    ht_linked = sum(1 for t in hard_tables if table_link.get(t, {}).get("working"))
    clean = len(tabs) - len(backups) - sum(len(g) - 1 for g in dupes) - len(sample_err)
    parts = {
        "Tags true": (tags_true, len(real_hard)),
        "  (labeled key columns empty in sample, not graded)": (empty_keys, empty_keys),
        "Hard links work": (ht_linked, len(hard_tables)),
        "Tables with a summary": (sum(w["summary"] for w in words), len(words)),
        "Columns described": (n_desc, n_cols),
        "Inventory clean": (clean, len(tabs)),
    }

    graded = {k: v for k, v in parts.items() if not k.startswith(" ")}
    map_score = round(sum(100 * a / b for a, b in graded.values() if b) / len(graded), 1)
    json.dump({"date": TODAY, "map": map_score,
               "parts": {k: {"passed": a, "of": b, "pct": round(100 * a / b, 1) if b else 0}
                         for k, (a, b) in graded.items()},
               "source": "scripts/audit_catalog.py analyze"},
              open(OUT / f"catalog_map_{TODAY}.json", "w", encoding="utf-8"), indent=1)

    # ---------------- write ----------------
    tsv = OUT / f"catalog_audit_{TODAY}.tsv"
    with open(tsv, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(F[0].keys()), delimiter="\t")
        w.writeheader()
        w.writerows(F)
    with open(OUT / f"catalog_audit_columns_{TODAY}.tsv", "w", newline="", encoding="utf-8") as f:
        keys_ = ["schema", "table", "column", "type", "regex_tag", "regex_verdict", "real_tag", "real_tier",
                 "real_verdict", "sampled", "filled", "distinct", "regex_shape_pct", "real_shape_pct",
                 "value_looks_like", "name_hint", "names_holds", "fips_level", "examples"]
        w = csv.DictWriter(f, fieldnames=keys_, delimiter="\t", extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "examples": json.dumps(r["examples"][:3])})
    with open(OUT / f"catalog_audit_links_{TODAY}.tsv", "w", newline="", encoding="utf-8") as f:
        if pairs:
            w = csv.DictWriter(f, fieldnames=list(pairs[0].keys()) + ["works"], delimiter="\t")
            w.writeheader()
            for p in sorted(pairs, key=lambda x: (x["key"] or "", -x["pct_of_a"])):
                w.writerow({**p, "works": works(p)})

    sev = collections.Counter(x["severity"] for x in F)
    chk = collections.Counter(x["check"] for x in F)
    L = [f"# Catalog audit — {TODAY}", "",
         "Read-only. Grades the MAP of LIBRARY_MARTS: is each table what the catalog says,",
         "is each key tag true, do links match, is there plain English. Script: scripts/audit_catalog.py.", "",
         "## MAP parts", "", "```"]
    for name, (a, b) in parts.items():
        L.append(f"{name:28} {a:>7,} of {b:>7,}   {100 * a / b if b else 0:5.1f}%")
    L += ["```", "", "## Inventory", "", "```",
          f"objects in catalog      {len(tabs):>6}", f"  base tables           {n_base:>6}", f"  views                 {n_view:>6}",
          f"backup copies           {len(backups):>6}", f"exact duplicate groups  {len(dupes):>6}",
          f"objects that error      {len(sample_err):>6}", f"schemas                 {len(schema_n):>6}",
          f"  with 4 or fewer       {sum(1 for v in schema_n.values() if v <= 4):>6}", "```", "",
          "Views and their real row counts:", ""]
    for k, t in sorted(tabs.items()):
        if t["TY"] == "VIEW":
            L.append(f"- {k}: {vcounts.get(k, 'not counted')}")
    L += ["", "Backup copies:", ""] + [f"- {k}: {t['R'] or 0:,} rows" for k, t in sorted(backups.items())]
    L += ["", "Schemas by size:", "", "```"] + [f"{s:32} {n:>4}" for s, n in schema_n.most_common()] + ["```", ""]
    L += ["## Tag truth", "", "Verdict per tag. PASS = 90%+ of sampled values fit the key's shape.",
          "Name tags PASS only when the values read as organizations.", ""]
    for label, title in (("real", "Platform tagger, connect/keys.py"), ("regex", "Catalog regex, catalog.json")):
        L += [f"### {title}", "", "```", f"{'tag':14} {'cols':>5} {'PASS':>5} {'WEAK':>5} {'FAIL':>5} {'EMPTY':>5} {'NOTEST':>6}"]
        for tag, c in sorted(tag_stats[label].items(), key=lambda x: -sum(x[1].values())):
            L.append(f"{tag:14} {sum(c.values()):>5} {c['PASS']:>5} {c['WEAK']:>5} {c['FAIL']:>5} {c['EMPTY']:>5} {c['NO SHAPE TEST']:>6}")
        L += ["```", ""]
    fails = [r for r in rows if r.get("real_verdict") == "FAIL" and r["real_tag"] != "NAME"]
    extra = collections.Counter()
    for r in fails:
        toks = set(r["column"].split("_"))
        hit = next((w for w in ("FLAG", "DATE", "NAME", "TYPE", "IND", "COUNT", "REPORTS", "NONE", "TICKER",
                                "EXT", "LAST", "4", "PCT", "STATUS", "DESC") if w in toks), "no extra word")
        extra[hit] += 1
    L += ["### Why platform tags fail, by the extra word in the column name", "",
          "The tagger fires on one word, like NPI, and ignores what else the name says.", "", "```"] +          [f"{w:16} {n:>4}" for w, n in extra.most_common()] + ["```", ""]
    holds = collections.Counter(r.get("names_holds") for r in rows if r["real_tag"] == "NAME")
    L += ["### What NAME-tagged columns hold", "", "```"] + [f"{str(h):32} {n:>5}" for h, n in holds.most_common()] + ["```", ""]
    fl = collections.Counter(r.get("fips_level") for r in rows if r["real_tag"] == "FIPS")
    L += ["### FIPS columns by level", "", "```"] + [f"{str(h):16} {n:>5}" for h, n in fl.most_common()] + ["```", ""]
    L += ["## Links", "", f"A link works when {MATCH_MIN_PCT}%+ of table A's distinct IDs, and {MATCH_MIN_N}+ IDs, appear in B.", "", "```",
          f"{'key':16} {'columns':>7} {'pairs':>6} {'working':>7}"]
    for key, cols in sorted(by_key.items(), key=lambda x: -len(x[1])):
        ps = [p for p in pairs if p["key"] == key]
        L.append(f"{str(key):16} {len(cols):>7} {len(ps):>6} {sum(works(p) for p in ps):>7}")
    L += ["```", "", "## Time", "", "```",
          f"catalog tables with a timeline view   {sum(1 for t in time_rows if t['timeline_view']):>5}",
          f"with date columns, no timeline view   {sum(1 for t in time_rows if not t['timeline_view'] and t['date_columns']):>5}",
          f"no date columns at all                {sum(1 for t in time_rows if not t['date_columns']):>5}", "```", "",
          "Grain of timeline views: " + ", ".join(f"{g or 'unknown'} {n}" for g, n in collections.Counter(
              t["grain"] for t in time_rows if t["timeline_view"]).most_common()), "",
          "## Findings", "", "```"] + [f"{c:40} {n:>5}" for c, n in chk.most_common()] + ["```", "",
          "By severity: " + ", ".join(f"{s} {n}" for s, n in sev.most_common()), "",
          f"Every finding: audit/catalog_audit_{TODAY}.tsv. Every column: audit/catalog_audit_columns_{TODAY}.tsv.",
          f"Every link pair: audit/catalog_audit_links_{TODAY}.tsv."]
    (OUT / f"catalog_audit_{TODAY}.md").write_text("\n".join(L), encoding="utf-8")
    print("\n".join(L[:60]))


# =========================================================================== #
# catalog: the verified catalog. Name rules propose a key; sampled values decide.
# Writes outputs/catalog/catalog.json (Patch Panel) and outputs/catalog/er.json
# (Warehouse Compass). Backups are left out; views carry their real COUNT(*).
# =========================================================================== #
from audit_catalog import SHAPES, fips_level, is_state, nonempty  # noqa: E402

# key -> the Patch Panel's coarser family and grade
FAMILY = {
    "NPI": "NPI", "CCN": "CCN", "EIN": "EIN", "CIK": "CIK", "LEI": "LEI", "UEI": "UEI/DUNS",
    "DUNS": "UEI/DUNS", "ACCESSION": "ACCESSION", "FDIC_CERT": "FDIC_CERT",
    "FEC_CMTE_ID": "FEC_ID", "FEC_CAND_ID": "FEC_ID", "BIOGUIDE": "BIOGUIDE", "ICPSR": "BIOGUIDE",
    "IMO": "IMO", "MMSI": "IMO", "FRS_ID": "FRS/EPA", "NPDES_ID": "FRS/EPA", "PWSID": "FRS/EPA",
    "MINE_ID": "MINE_ID", "MSHA_CONTROLLER_ID": "MINE_ID", "MSHA_OPERATOR_ID": "MINE_ID",
    "DEA_NO": "DEA_NO", "COUNTY_FIPS": "COUNTY_FIPS", "TRACT_FIPS": "TRACT", "STATE_FIPS": "STATE",
    "STATE": "STATE", "ZIP": "ZIP", "NAME": "ORG_NAME",
    "NDC": "WHAT", "DRUG": "WHAT", "HCPCS": "WHAT", "CFDA": "WHAT", "CAS": "WHAT", "ICD": "WHAT", "NAICS": "WHAT", "SIC": "WHAT",
}
GRADE = {"COUNTY_FIPS": "medium", "TRACT": "medium", "ZIP": "weak", "STATE": "weak", "ORG_NAME": "weak",
         "WHAT": "medium"}


def final_tag(r: dict) -> tuple[str | None, str]:
    """(verified key or None, why). One row of column_rows()."""
    tag, ne = r["real_tag"], r["filled"]
    if not tag:
        return None, ""
    if not ne and r["real_tier"] not in ("STEEL", "STRONG"):
        # nothing to confirm a place or name label with; hard IDs keep theirs, since
        # a first-rows sample can miss a column filled further down
        return None, f"{tag} label, empty in sample"
    pct = r.get("real_shape_pct")
    if tag == "NAME":
        holds = r.get("names_holds")
        if holds == "places":
            return (("STATE", "state codes") if r["examples"] and all(is_state(x) for x in r["examples"])
                    else (None, "place names, not a name link"))
        if holds == "things, not names" and re.search(r"DRUG|INGREDIENT|GENERIC|BRAND|MEDICATION|PRODUCT", r["column"]):
            return "DRUG", "drug or product names"
        if holds in NAME_OK or holds == "empty":
            return "NAME", holds or ""
        return None, f"name label holds {holds}"
    if tag == "FIPS":
        lv = r.get("fips_level")
        if not ne:
            return None, "FIPS label, empty in sample, level unknown"
        if pct is not None and pct < 50:
            return None, f"FIPS label, {pct}% fit"
        return {"state": ("STATE_FIPS", "2-digit state"), "county": ("COUNTY_FIPS", "5-digit county"),
                "tract": ("TRACT_FIPS", "11-digit tract"), "block group": ("TRACT_FIPS", "block group")
                }.get(lv, (None, f"FIPS level {lv}"))
    if tag == "ZIP":
        if ne and pct is not None and pct < 50:
            return None, f"not US zips, {pct}% fit"
        return "ZIP", ""
    if tag == "STATE":
        if ne and pct is not None and pct < 90:
            return None, f"not state codes, {pct}% fit"
        return "STATE", ""
    if tag in SHAPES and ne and pct is not None and pct < 50:
        return None, f"{tag} label, {pct}% fit"
    return tag, ""


def cmd_catalog():
    import datetime as _dt
    inv = load_inventory()
    vcounts = json.load(open(CACHE / "view_counts.json")) if (CACHE / "view_counts.json").exists() else {}
    rows = column_rows()
    by_t = collections.defaultdict(list)
    for r in rows:
        by_t[(r["schema"], r["table"])].append(r)
    ttype = {(t["S"], t["T"]): t for t in inv["tabs"]}
    cat = {"generated": _dt.date.today().isoformat(), "source": "scripts/audit_catalog.py catalog",
           "keys": collections.defaultdict(list), "tables": []}
    er = {"g": cat["generated"], "t": []}
    treg = _time_registry()
    tl_views = {x["T"] for x in inv["timeline"] if x["TY"] == "VIEW"}
    dropped = collections.Counter()
    for (s, t), rs in sorted(by_t.items()):
        if BACKUP.search(t):
            dropped["backup"] += 1
            continue
        meta = ttype[(s, t)]
        n = meta["R"] if meta["TY"] == "BASE TABLE" else vcounts.get(f"{s}.{t}")
        n = n if isinstance(n, int) else 0
        cols, ercols, fams = [], [], set()
        for r in rs:
            k, why = final_tag(r)
            fam = FAMILY.get(k) if k else None
            if k and not fam and r["real_tier"] in ("STEEL", "STRONG"):
                fam = "OTHER_ID"
            g = (GRADE.get(fam, "strong") if fam else None)
            cols.append({"c": r["column"], "d": r["type"], "k": fam, "g": g, "key": k, "why": why})
            ercols.append([r["column"], r["type"], k or ""])
            if fam:
                fams.add(fam)
        for f in fams:
            cat["keys"][f].append(f"{s}.{t}")
        cat["tables"].append({"s": s, "t": t, "type": meta["TY"].lower(), "r": n, "n": len(cols),
                              "keys": sorted(fams), "cols": cols})
        grain = treg.get(t, {}).get("grain", "") if t in tl_views else ""
        er["t"].append([s, t, n, ercols, grain])   # [4]: the TIMELINE view's grain, '' if none
    cat["keys"] = {k: sorted(v) for k, v in cat["keys"].items()}
    out = REPO / "outputs" / "catalog"
    json.dump(cat, open(out / "catalog.json", "w", encoding="utf-8"), separators=(",", ":"))
    json.dump(er, open(out / "er.json", "w", encoding="utf-8"), separators=(",", ":"))
    print(f"catalog: {len(cat['tables'])} tables, {dropped['backup']} backups left out")
    for k, v in sorted(cat["keys"].items(), key=lambda x: -len(x[1])):
        print(f"  {k:14} {len(v):>4} tables")
