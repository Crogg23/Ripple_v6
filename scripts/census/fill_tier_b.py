"""Tier B of the census-grid fill: per-table scans for mart models the
2026-08-11 verification scan did not cover (new CourtListener tables + the
mart-layer views over large raw tables).

Same aggregate battery as scripts/scan_keys_dates.py (ID-key reality, date
sanity, exact-dup hash) so results merge cleanly with the 8/11 scan output.
Read-only, aggregate-only, checkpointed per table. Tables are passed one per
line in a file given as argv[1]; smallest-first ordering is the caller's job.

Writes reports/census_grid_2026-08-12/fill/tier_b_new_scans.jsonl.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _snowflake_conn import connect  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FILL = os.path.join(REPO, "reports", "census_grid_2026-08-12", "fill")
OUT = os.path.join(FILL, "tier_b_new_scans.jsonl")
CKPT = os.path.join(FILL, "tier_b_done.json")

ID_RE = re.compile(
    r"(?:^|_)(id|ids|key|number|num|no|code|npi|ein|cik|lei|cusip|duns|uei|fips|"
    r"zip|ssn|vin|imo|mmsi|cert|license|permit|docket|case|accession|registration|"
    r"identifier|bioguide|crd|rssd|abi|isin|ticker|facility|station)(?:$|_)",
    re.I,
)
SKIP_ID = re.compile(r"(name|desc|text|note|title|url|address|city|county_name)", re.I)


def id_like(col):
    return bool(ID_RE.search(col)) and not SKIP_ID.search(col)


def main():
    tables = [t.strip() for t in open(sys.argv[1], encoding="utf-8") if t.strip()]
    done = set(json.load(open(CKPT))) if os.path.exists(CKPT) else set()
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    out = open(OUT, "a", encoding="utf-8")
    print(f"{len(tables)} tables, {len(done)} already done", flush=True)
    for key in tables:
        if key in done:
            continue
        sch, tab = key.split(".", 1)
        cur.execute(
            "select column_name, data_type from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS "
            "where table_schema=%s and table_name=%s order by ordinal_position",
            (sch, tab),
        )
        cols = cur.fetchall()
        idc = [c for c, t in cols if id_like(c)][:12]
        datec = [c for c, t in cols if t in ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ")][:8]
        exprs = ["count(*) as n_rows"]
        for c in idc:
            q = f'"{c}"'
            exprs += [
                f"count({q})",
                f"approx_count_distinct({q})",
                f"min(length(to_varchar({q})))",
                f"max(length(to_varchar({q})))",
                f"min(to_varchar({q}))",
                f"max(to_varchar({q}))",
                f"count_if(lower(to_varchar({q})) in ('nan','none','null','n/a','na','unknown',''))",
            ]
        for c in datec:
            q = f'"{c}"'
            exprs += [f"to_varchar(min({q}))", f"to_varchar(max({q}))",
                      f"count_if(year({q})=1970)", f"count_if({q} > current_date + 365*5)"]
        exprs.append("count(distinct hash(*))")
        sql = f'select {", ".join(exprs)} from LIBRARY_MARTS."{sch}"."{tab}"'
        print(f"scanning {key} ({len(idc)} ids, {len(datec)} dates)", flush=True)
        try:
            cur.execute(sql)
            vals = list(cur.fetchone())
        except Exception as e:
            out.write(json.dumps({"table": key, "error": str(e)[:300]}) + "\n")
            out.flush()
            done.add(key)
            json.dump(sorted(done), open(CKPT, "w"))
            continue
        rec = {"table": key, "n_rows": vals[0], "ids": {}, "dates": {}}
        p = 1
        for c in idc:
            nn, dn, mnl, mxl, mnv, mxv, sent = vals[p:p + 7]
            p += 7
            rec["ids"][c] = {"nonnull": nn, "distinct": dn, "minlen": mnl, "maxlen": mxl,
                             "minval": (str(mnv)[:60] if mnv is not None else None),
                             "maxval": (str(mxv)[:60] if mxv is not None else None),
                             "sentinels": sent}
        for c in datec:
            mn, mx, y1970, far = vals[p:p + 4]
            p += 4
            rec["dates"][c] = {"min": str(mn), "max": str(mx), "y1970": y1970, "future5y": far}
        rec["distinct_row_hashes"] = vals[p]
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add(key)
        json.dump(sorted(done), open(CKPT, "w"))
        print(f"done {key} rows={vals[0]:,}", flush=True)
    print("TIER B DONE", len(done), flush=True)


if __name__ == "__main__":
    main()
