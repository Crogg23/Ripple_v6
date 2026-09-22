#!/usr/bin/env python3
"""Probe every enabled mart that has no dbt test, live, and pick a test it can pass.

For each mart: count rows, then for every business column count distinct and count nulls.
A column with distinct == rows and 0 nulls is a real row key -> unique + not_null.
If none, try pairs of the best near-keys -> unique_combination.
If nothing is unique, the most-filled column gets not_null.
Writes reports/untested_marts_probe_<date>.tsv. Read-only.
"""
from __future__ import annotations
import csv, datetime as dt, itertools, json, sys
from pathlib import Path
REPO = Path(__file__).resolve().parents[1]
DBT = REPO / "library-onboarding" / "ripple_dbt"
sys.path.insert(0, str(REPO))
from connect import db

SKIP_PREFIX = ("_",)
def main():
    m = json.loads((DBT / "target" / "manifest.json").read_text(encoding="utf-8"))
    n = m["nodes"]
    marts = {k: v for k, v in n.items() if v["resource_type"] == "model" and "/marts/" in v["original_file_path"].replace("\\", "/") and v.get("config", {}).get("enabled", True)}
    tested = {d for v in n.values() if v["resource_type"] == "test" for d in v.get("depends_on", {}).get("nodes", [])}
    bare = sorted(set(marts) - tested)
    conn = db.connect()
    out = []
    prev = {}
    import glob
    for f in sorted(glob.glob(str(REPO / "reports" / "untested_marts_probe_*.tsv"))):
        for r in csv.DictReader(open(f, encoding="utf-8"), delimiter="	"):
            if r["verdict"] not in ("MISSING", "ERROR"): prev[r["model"]] = r
    for k in bare:
        v = marts[k]; rel = v["relation_name"]
        if v["name"] in prev:
            r = prev[v["name"]]; out.append((r["model"], r["relation"], r["verdict"], r["column"], r["rows"])); print(v["name"], "kept"); continue
        try:
            cols = [r[0] for r in db.rows(conn, f"select column_name from {v['database']}.information_schema.columns where table_schema='{v['schema']}' and table_name='{v['alias'].upper()}' order by ordinal_position")]
        except Exception as e:
            out.append((v["name"], rel, "ERROR", str(e)[:120], "")); print(v["name"], "ERROR", e); continue
        if not cols:
            out.append((v["name"], rel, "MISSING", "no such table", "")); print(v["name"], "MISSING"); continue
        biz = [c for c in cols if not c.startswith(SKIP_PREFIX)]
        sel = ", ".join(f'count(distinct "{c}") , count_if("{c}" is null)' for c in biz)
        r = db.rows(conn, f'select count(*), {sel} from {rel}')[0]
        total = r[0]
        stats = {c: (r[1 + 2 * i], r[2 + 2 * i]) for i, c in enumerate(biz)}
        keys = [c for c, (d, nl) in stats.items() if total > 0 and d == total and nl == 0]
        verdict, detail = "", ""
        if total == 0:
            verdict, detail = "EMPTY", "0 rows"
        elif keys:
            verdict, detail = "UNIQUE", keys[0]
        else:
            near = [] if total > 20_000_000 else sorted(((d, c) for c, (d, nl) in stats.items() if nl == 0 and d > 1), reverse=True)[:6]
            for a, b in itertools.combinations([c for _, c in near], 2):
                d = db.rows(conn, f'select count(*) from (select distinct "{a}", "{b}" from {rel})')[0][0]
                if d == total:
                    verdict, detail = "PAIR", f"{a}|{b}"; break
            if not verdict:
                filled = sorted(((nl, c) for c, (d, nl) in stats.items()))
                verdict, detail = "NOTNULL", filled[0][1] if filled[0][0] == 0 else f"{filled[0][1]}:{filled[0][0]}nulls"
        out.append((v["name"], rel, verdict, detail, total))
        print(v["name"], total, verdict, detail, flush=True)
    p = REPO / "reports" / f"untested_marts_probe_{dt.date.today()}.tsv"
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t"); w.writerow(["model", "relation", "verdict", "column", "rows"]); w.writerows(out)
    print("wrote", p)

if __name__ == "__main__":
    main()
