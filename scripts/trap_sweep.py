"""Five mechanical trap sweeps across every table in the warehouse.

Read-only. One profiling pass per table, sampled by default.
Finds the five trap shapes a machine can find; the judgment-class traps
still need a hunt. Written 2026-09-08 after the Tool Box hunt scored
5 of its 7 traps as machine-findable.

  S1  copy-paste rows      identical numeric tuple repeated across rows
  S2  blank-vs-null lie    a column blank as '' where a NULL test passes
  S3  sentinel domination  one value swallowing a column that looks like an id
  S4  name-vs-content      column named like a date/amount/id and isn't
  S5  twin tables          two tables sharing a key, neither a superset

Usage:
  python3 scripts/trap_sweep.py --limit 8              # smoke test
  python3 scripts/trap_sweep.py --schema LABOR
  python3 scripts/trap_sweep.py --all --sample 100000  # the real run
  python3 scripts/trap_sweep.py --all --full           # no sampling, expensive
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from connect import db  # noqa: E402

MARTS_DB = "LIBRARY_MARTS"
RAW_DB = "LIBRARY_RAW"

# columns whose NAME promises a shape; S4 checks the content against the promise
NAME_PROMISES = [
    ("date", re.compile(r"(^|_)(DATE|DT|DAY|YEAR|YR|TIMESTAMP|TS)($|_)")),
    ("amount", re.compile(r"(^|_)(AMOUNT|AMT|PAYMENT|COST|PRICE|FEE|DOLLARS|USD|REVENUE|SPEND|PENALTY|FINE)($|_)")),
    ("id", re.compile(r"(^|_)(ID|EIN|NPI|CCN|CIK|LEI|UEI|DUNS|NUMBER|NUM|KEY|CODE)($|_)")),
    ("count", re.compile(r"(^|_)(COUNT|CNT|TOTAL|QTY|QUANTITY|N)($|_)")),
    ("flag", re.compile(r"(^|_)(FLAG|IS|HAS|SW|IND|INDICATOR)($|_)")),
]

TEXTY = ("TEXT", "VARCHAR", "STRING", "CHAR")
NUMERIC = ("NUMBER", "FLOAT", "DECIMAL", "INT", "INTEGER", "BIGINT", "DOUBLE", "REAL")
TEMPORAL = ("DATE", "TIMESTAMP_NTZ", "TIMESTAMP_LTZ", "TIMESTAMP_TZ", "DATETIME")


def promise_for(col: str) -> str | None:
    up = col.upper()
    for label, rx in NAME_PROMISES:
        if rx.search(up):
            return label
    return None


def q(conn, sql):
    cur = conn.cursor()
    try:
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        cur.close()


def list_tables(conn, schema=None, include_landing=True, limit=None):
    rows = q(conn, f"""
        select table_catalog db, table_schema sch, table_name tbl, row_count rc
        from {MARTS_DB}.information_schema.tables
        where table_type='BASE TABLE' and row_count > 0
        union all
        select table_catalog, table_schema, table_name, row_count
        from {RAW_DB}.information_schema.tables
        where table_type='BASE TABLE' and row_count > 0
          and table_schema = 'LANDING' and {'true' if include_landing else 'false'}
        order by rc desc
    """)
    # backup/restore schemas lead with an underscore; skip them in Python,
    # Snowflake's LIKE escape zeroed the whole marts half when this was SQL.
    rows = [r for r in rows if not r["SCH"].startswith("_")]
    if schema:
        rows = [r for r in rows if r["SCH"].upper() == schema.upper()]
    if limit:
        rows = rows[:limit]
    return rows


def columns_for(conn, dbname, sch, tbl):
    return q(conn, f"""
        select column_name nm, data_type dt, ordinal_position op
        from {dbname}.information_schema.columns
        where table_schema='{sch}' and table_name='{tbl}'
        order by ordinal_position
    """)


def profile_table(conn, dbname, sch, tbl, rc, sample_rows, batch=30, cols=None):
    """S2, S3, S4 in one pass per column batch. Returns a list of findings."""
    if cols is None:
        cols = columns_for(conn, dbname, sch, tbl)
    if not cols:
        return []
    fq = f'"{dbname}"."{sch}"."{tbl}"'
    src = fq
    sampled = False
    if sample_rows and rc and rc > sample_rows:
        src = f"{fq} sample row ({sample_rows} rows)"
        sampled = True

    findings = []
    for i in range(0, len(cols), batch):
        chunk = cols[i:i + batch]
        sel = ["count(*) __n"]
        for j, c in enumerate(chunk):
            nm, dt = c["NM"], (c["DT"] or "").upper()
            ref = f'"{nm}"'
            sel.append(f"count_if({ref} is null) n{j}_null")
            sel.append(f"approx_count_distinct({ref}) n{j}_dist")
            if dt.startswith(TEXTY):
                sel.append(f"count_if(trim({ref})='') n{j}_blank")
                sel.append(f"to_json(approx_top_k({ref},1)) n{j}_top")
                sel.append(f"count_if(try_to_date({ref}) is not null) n{j}_asdate")
                sel.append(f"count_if(try_to_number({ref}) is not null) n{j}_asnum")
            else:
                sel.append(f"0 n{j}_blank")
                sel.append(f"to_json(approx_top_k(to_varchar({ref}),1)) n{j}_top")
                sel.append(f"0 n{j}_asdate")
                sel.append(f"0 n{j}_asnum")
        sql = "select " + ", ".join(sel) + f" from {src}"
        try:
            row = q(conn, sql)[0]
        except Exception as e:
            findings.append(dict(db=dbname, sch=sch, tbl=tbl, col="*", sweep="ERROR",
                                 detail=str(e)[:200], n=rc, sampled=sampled))
            continue

        n = row["__N"] or 0
        if not n:
            continue
        for j, c in enumerate(chunk):
            nm, dt = c["NM"], (c["DT"] or "").upper()
            nulls = row[f"N{j}_NULL"] or 0
            blanks = row[f"N{j}_BLANK"] or 0
            dist = row[f"N{j}_DIST"] or 0
            asdate = row[f"N{j}_ASDATE"] or 0
            asnum = row[f"N{j}_ASNUM"] or 0
            # approx_top_k returns [[value, count]] — a list of PAIRS. Reading
            # it as [{"value":..,"count":..}] throws, and a bare except turns
            # that into a silent None on every column. Found 2026-09-08 after
            # a full 2,916-table run in which S3 raised exactly zero flags.
            top_val, top_cnt = None, 0
            try:
                top = json.loads(row[f"N{j}_TOP"] or "[]")
                if top and isinstance(top[0], (list, tuple)) and len(top[0]) >= 2:
                    top_val, top_cnt = str(top[0][0]), int(top[0][1])
                elif top and isinstance(top[0], dict):
                    top_val, top_cnt = str(top[0]["value"]), int(top[0]["count"])
            except Exception:
                pass
            filled = n - nulls - blanks

            def add(sweep, detail):
                findings.append(dict(db=dbname, sch=sch, tbl=tbl, col=nm, sweep=sweep,
                                     detail=detail, n=n, sampled=sampled))

            # S2 — blank-vs-null lie. Only on columns whose NAME promises
            # a value; a blank EMPLOYER or MEMO_TEXT is normal in raw filings.
            promise_early = promise_for(nm)
            if promise_early in ("id", "amount", "date", "count"):
                if blanks and nulls == 0 and blanks / n >= 0.05:
                    add("S2_blank_not_null",
                        f"named like a {promise_early}; {blanks}/{n} = {blanks/n:.1%} "
                        f"empty string with zero NULL, so `is not null` passes on all")
                if nulls and blanks and nulls / n >= 0.05 and blanks / n >= 0.05:
                    add("S2_both_blank_kinds",
                        f"named like a {promise_early}; {nulls} NULL and {blanks} "
                        f"empty string in one column, two ways to be missing")

            # S3 — sentinel domination
            if top_val is not None and filled > 0 and top_cnt / n >= 0.90 and dist <= 5:
                add("S3_sentinel",
                    f"one value '{top_val[:40]}' on {top_cnt}/{n} = {top_cnt/n:.1%}, "
                    f"{dist} distinct values total")
            elif top_val is not None and top_cnt / n >= 0.50 and promise_for(nm) == "id":
                add("S3_id_not_unique",
                    f"named like an id but '{top_val[:40]}' covers {top_cnt/n:.1%}, "
                    f"{dist} distinct on {n} rows")

            # S4 — name promises a shape the content does not keep
            promise = promise_for(nm)
            if promise and filled >= 50:
                # only judge TEXT: a FLOAT column named NAICS_YEAR holding 2022
                # is a year, and try_to_date has nothing to say about it.
                if promise == "date" and dt.startswith(TEXTY):
                    bare_year = bool(top_val and re.fullmatch(r"(19|20)\d\d(\.0)?", top_val))
                    if asdate / filled < 0.5 and not bare_year:
                        add("S4_date_name_not_date",
                            f"named like a date, {asdate}/{filled} = {asdate/filled:.1%} parse; "
                            f"top value '{(top_val or '')[:30]}'")
                if promise == "amount" and dt.startswith(TEXTY) and asnum / filled < 0.9:
                    add("S4_amount_name_not_number",
                        f"named like money, {asnum}/{filled} = {asnum/filled:.1%} numeric")
                if promise == "id" and dist <= 1 and filled >= 100:
                    add("S4_id_one_value",
                        f"named like an id, exactly {dist} distinct value on {filled} filled rows")
    return findings


def sweep_copy_paste(conn, dbname, sch, tbl, rc, sample_rows, min_block=20, cols=None):
    """S1 — the Caltrans shape: an identical numeric tuple repeated across rows."""
    if cols is None:
        cols = columns_for(conn, dbname, sch, tbl)
    cand = [c["NM"] for c in cols if (c["DT"] or "").upper().startswith(NUMERIC)]
    cand = [c for c in cand if not c.upper().startswith("_")][:25]
    if len(cand) < 2:
        return []
    fq = f'"{dbname}"."{sch}"."{tbl}"'
    src = fq
    sampled = False
    if sample_rows and rc and rc > sample_rows:
        src = f"{fq} sample row ({sample_rows} rows)"
        sampled = True

    # Pick the widest-spread numeric columns. A YEAR column has 20 distinct
    # values and repeats by design; TOTAL_HOURS_WORKED has thousands, so a
    # block of rows sharing one value there is a filer copying its own page.
    try:
        d = q(conn, "select " + ", ".join(
            f'approx_count_distinct("{c}") d{i}' for i, c in enumerate(cand)
        ) + f" from {src}")[0]
    except Exception:
        return []
    spread = sorted(((d.get(f"D{i}") or 0, c) for i, c in enumerate(cand)), reverse=True)
    nums = [c for cnt, c in spread if cnt >= 100][:3]
    if len(nums) < 2:
        return []
    keys = ", ".join(f'"{c}"' for c in nums)
    notnull = " and ".join(f'"{c}" is not null' for c in nums)
    mag = " + ".join(f'abs("{c}")' for c in nums)
    # Tail gate. MSHA hands out thousands of identical $100 fines and that is
    # the system working. Caltrans stamping 10,580,031 hours on 41 rows is not.
    # So the repeated value must sit in the top 1% of its own column, not the
    # bottom, before a repeated block counts as a copy-paste.
    sql = f"""
      with r as (select {keys}, {mag} mag from {src} where {notnull}),
           cut as (select percentile_cont(0.99) within group (order by mag) p99 from r),
           g as (select {keys}, count(*) c, max(mag) mag from r group by {keys}),
           b as (select * from g where c >= {min_block} and mag >= (select p99 from cut)),
           w as (select object_construct('rows', c, 'tuple', array_construct({keys})) worst
                 from b order by c * mag desc limit 1)
      select (select count(*) from b) big_blocks,
             (select coalesce(sum(c),0) from b) rows_in_big_blocks,
             (select coalesce(max(c),0) from b) biggest,
             (select to_json(worst) from w) worst
    """
    try:
        r = q(conn, sql)[0]
    except Exception as e:
        return [dict(db=dbname, sch=sch, tbl=tbl, col=",".join(nums), sweep="ERROR",
                     detail=str(e)[:200], n=rc, sampled=sampled)]
    big = r["ROWS_IN_BIG_BLOCKS"] or 0
    biggest = r["BIGGEST"] or 0
    if big and biggest >= min_block:
        worst = (r.get("WORST") or "")
        return [dict(db=dbname, sch=sch, tbl=tbl, col=",".join(nums), sweep="S1_copy_paste",
                     detail=f"{big} rows in blocks of {min_block}+ sharing one "
                            f"({', '.join(nums)}) tuple; biggest block {biggest}; "
                            f"worst block {str(worst)[:160]}",
                     n=rc, sampled=sampled)]
    return []


def sweep_twin_tables(conn):
    """S5 — two tables carrying the same near-unique key, neither a superset.

    Structure only here. It names the pairs worth set-comparing; the
    comparison itself is one query per pair and is left to the caller.
    """
    rows = q(conn, f"""
        with c as (
          select table_schema sch, table_name tbl, column_name col
          from {MARTS_DB}.information_schema.columns
          where column_name in ('REGISTRY_ID','NPI','CCN','EIN','CIK','LEI','UEI',
                                'DUNS','FRS_ID','PWSID','NPDES_ID','IMO','MMSI',
                                'CMTE_ID','CAND_ID','BIOGUIDE_ID','OBJECT_ID')
        ),
        t as (
          select table_schema sch, table_name tbl, row_count rc
          from {MARTS_DB}.information_schema.tables
          where table_type='BASE TABLE' and row_count > 1000
        )
        select c.col, count(*) tables_, sum(t.rc) rows_,
               listagg(c.sch||'.'||c.tbl, ' | ') within group (order by t.rc desc) members
        from c join t on t.sch=c.sch and t.tbl=c.tbl
        group by c.col having count(*) between 2 and 40
        order by tables_ desc
    """)
    out = []
    for r in rows:
        out.append(dict(db=MARTS_DB, sch="*", tbl="*", col=r["COL"], sweep="S5_twin_candidates",
                        detail=f"{r['TABLES_']} tables carry {r['COL']}; set-compare each pair. "
                               f"members: {(r['MEMBERS'] or '')[:400]}",
                        n=r["ROWS_"], sampled=False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--schema", help="one schema only")
    ap.add_argument("--limit", type=int, help="first N tables by row count")
    ap.add_argument("--all", action="store_true", help="every table")
    ap.add_argument("--sample", type=int, default=200000, help="rows to sample per table")
    ap.add_argument("--full", action="store_true", help="no sampling, full scan")
    ap.add_argument("--no-landing", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--threads", type=int, default=6,
                    help="parallel table workers, one connection each")
    args = ap.parse_args()

    if not (args.schema or args.limit or args.all):
        ap.error("pick one of --schema, --limit or --all")

    sample = None if args.full else args.sample
    out = Path(args.out) if args.out else _REPO / "reports" / f"trap_sweep_{time.strftime('%Y-%m-%d')}.csv"

    conn = db.connect()
    t0 = time.time()
    try:
        tables = list_tables(conn, args.schema, not args.no_landing, args.limit)
        print(f"[sweep] {len(tables)} tables, "
              f"{'full scan' if args.full else f'sampled to {sample:,} rows'}")

        findings = sweep_twin_tables(conn)
        print(f"[S5] {len(findings)} key columns spanning 2+ tables")

        # one connection per worker; Snowflake is happy with a handful at once
        local = threading.local()
        lock = threading.Lock()
        done = [0]

        def conn_for():
            if not getattr(local, "conn", None):
                local.conn = db.connect()
            return local.conn

        def one(t):
            dbn, sch, tbl, rc = t["DB"], t["SCH"], t["TBL"], t["RC"]
            try:
                c = conn_for()
                cols = columns_for(c, dbn, sch, tbl)   # once per table, not twice
                f = profile_table(c, dbn, sch, tbl, rc, sample, cols=cols)
                f += sweep_copy_paste(c, dbn, sch, tbl, rc, sample, cols=cols)
            except Exception as e:
                f = [dict(db=dbn, sch=sch, tbl=tbl, col="*", sweep="ERROR",
                          detail=str(e)[:200], n=rc, sampled=False)]
            with lock:
                findings.extend(f)
                done[0] += 1
                if done[0] % 25 == 0 or done[0] == len(tables):
                    print(f"[sweep] {done[0]}/{len(tables)} tables, {len(findings)} flags, "
                          f"{time.time()-t0:.0f}s elapsed", flush=True)
            return None

        with ThreadPoolExecutor(max_workers=max(1, args.threads)) as ex:
            list(ex.map(one, tables))

        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["db", "sch", "tbl", "col", "sweep",
                                               "detail", "n", "sampled"])
            w.writeheader()
            w.writerows(findings)

        by = {}
        for f in findings:
            by[f["sweep"]] = by.get(f["sweep"], 0) + 1
        print(f"\n[done] {len(findings)} flags in {time.time()-t0:.0f}s -> {out}")
        for k in sorted(by, key=lambda x: -by[x]):
            print(f"  {by[k]:>6}  {k}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
