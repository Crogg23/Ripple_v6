"""Verification scan over every mart table: ID-key reality, date sanity, exact-dup check.

Aggregate-only queries (no row dumps). Checkpoints per table so it survives restarts.
Writes scratchpad/scan_results.jsonl (one JSON object per table).
"""
import json, os, re, sys, time

sys.path.insert(0, r"c:\Code\Ripple_v6\scripts")
from _snowflake_conn import connect  # noqa: E402

_REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(_REPO, "outputs", "_mart_key_date_dup_scan_rerun.jsonl")
CKPT = os.path.join(_REPO, "outputs", "_scan_rerun_done.json")

# Optional: pass table keys (SCHEMA.TABLE) as argv to scan only those.
ONLY = set(a.upper() for a in sys.argv[1:])

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
    done = set()
    if os.path.exists(CKPT):
        done = set(json.load(open(CKPT)))
    conn = connect(database="LIBRARY_MARTS")
    cur = conn.cursor()
    cur.execute(
        "select table_schema, table_name, row_count from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
        "where table_type='BASE TABLE' and table_schema<>'INFORMATION_SCHEMA' order by row_count"
    )
    tables = cur.fetchall()
    print(f"{len(tables)} tables, {len(done)} already done", flush=True)
    cols_by_table = {}
    cur.execute(
        "select table_schema, table_name, column_name, data_type from "
        "LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS"
    )
    for sch, tab, col, typ in cur.fetchall():
        cols_by_table.setdefault((sch, tab), []).append((col, typ))

    out = open(OUT, "a", encoding="utf-8")
    for i, (sch, tab, rc) in enumerate(tables):
        fqn = f'LIBRARY_MARTS."{sch}"."{tab}"'
        key = f"{sch}.{tab}"
        if key in done:
            continue
        if ONLY and key.upper() not in ONLY:
            continue
        cols = cols_by_table.get((sch, tab), [])
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
            # to_varchar server-side: extreme years (0001, 10000+) overflow the
            # Python client's date/int decoding -- the cause of the 16 scan
            # errors on 2026-08-11 ("ordinal must be >= 1", "int too large").
            exprs += [f"to_varchar(min({q}))", f"to_varchar(max({q}))",
                      f"count_if(year({q})=1970)", f"count_if({q} > current_date + 365*5)"]
        # exact duplicate check: full-row hash distinct (cheap-ish aggregate)
        exprs.append("count(distinct hash(*))")
        sql = f"select {', '.join(exprs)} from {fqn}"
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
            (nn, dn, mnl, mxl, mnv, mxv, sent) = vals[p:p+7]; p += 7
            rec["ids"][c] = {"nonnull": nn, "distinct": dn, "minlen": mnl, "maxlen": mxl,
                             "minval": (str(mnv)[:60] if mnv is not None else None),
                             "maxval": (str(mxv)[:60] if mxv is not None else None),
                             "sentinels": sent}
        for c in datec:
            (mn, mx, y1970, far) = vals[p:p+4]; p += 4
            rec["dates"][c] = {"min": str(mn), "max": str(mx), "y1970": y1970, "future5y": far}
        rec["distinct_row_hashes"] = vals[p]
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add(key)
        if i % 20 == 0:
            json.dump(sorted(done), open(CKPT, "w"))
            print(f"[{i}/{len(tables)}] {key} rows={rc}", flush=True)
    json.dump(sorted(done), open(CKPT, "w"))
    print("DONE", len(done), flush=True)

if __name__ == "__main__":
    main()
