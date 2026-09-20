#!/usr/bin/env python3
"""Read a sample of every landing table and say what each column really holds. Read-only.

Why this exists (2026-09-19): 91,894 of 92,442 landing columns are TEXT. The
staging generator passes them through as TEXT, so dates, money and counts reach
the marts as strings (FDIC certs landed as '13925.0' and the literal 'nan').
A cast can only be emitted safely if something has looked at the values first.
This is the looking. It also gives the fill rate per column, which is what
catches a table whose label is wrong (NARA "records" that were 554 page titles).

What is checked, per column, over a sample of rows:
  - filled:   not NULL, not '', not a null word ('nan', 'n/a', 'null', 'none', ...)
  - number:   TRY_TO_DOUBLE parses it. 'nan' is excluded first -- Snowflake
              parses the string 'nan' to the float NaN, so it would count.
  - int / int_dot_zero / leading_zero: digits only; '13925.0'; '02134'.
              A leading zero means it is a code, not a number -- never cast it.
  - date:     TRY_TO_DATE parses it AND it has a - or / between two characters.
              A bare run of digits is read by Snowflake as seconds since 1970,
              so '2015' would "parse" to a day in January 1970, and '-7' to
              1969-12-31. (The 2026-09-19 file was written before the '-7' fix:
              in it, a column of negative numbers also counts as dates.)
  - date8:    YYYYMMDD with a 19xx/20xx year, parsed with an explicit format.
  - date8_mdy: MMDDYYYY, same idea (FEC TRANSACTION_DT is '01152024').
  - ts:       parses as a timestamp and carries a time part (has a ':').
  - bool_tf / bool_yn: true/false words; y/n/yes/no words (kept apart on purpose:
              INCLUDE is a 'Y'/'N' string here, and that is a judgment call).

What a hit means: share = parsed / filled. Near 1.0 on a decent number of filled
rows -> the column is that type in THIS sample. What a miss means: mixed or free
text; leave it TEXT. Blind spot: it is a sample. Big tables are block-sampled
(whole storage blocks, so rows that landed together), and a rare bad value in
row 40 million is not seen. That is why the casts must be TRY_ casts.

    python scripts/profile_landing_columns.py --tables FED_FDIC_FAILED_BANKS,FED_NARA_AAD
    python scripts/profile_landing_columns.py --staged-only     # tables a staging model reads
    python scripts/profile_landing_columns.py                   # every landing table
    python scripts/profile_landing_columns.py --resume          # skip tables already in today's file

Writes reports/landing_column_profile_<date>.tsv, one line per table-column.
"""
from __future__ import annotations

import argparse
import datetime as dt
import queue
import re
import sys
import threading
import time
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
from connect import db  # noqa: E402

STAGING = _REPO / "library-onboarding" / "ripple_dbt" / "models" / "staging"

SAMPLE_ROWS = 10_000
WHOLE_TABLE_UNDER = 50_000      # small enough to read all of it
BLOCK_SAMPLE_OVER = 1_000_000   # past this, a row sample scans the whole table; sample blocks instead
BLOCK_SAMPLE_TARGET = 200_000   # rows aimed for before the LIMIT, so a thin block sample still fills it
FAT_BYTES_PER_ROW = 50_000      # compressed bytes per row past which a table counts as fat
FAT_SAMPLE_ROWS = 200

NULL_WORDS = ("nan", "n/a", "na", "null", "none", "nil", "-", "--", "#n/a", "not available")

HEADER = ("table\tcolumn\tdata_type\ttable_rows\tsampled\tfilled\tblank\tnull_word\tnumber\tint\t"
          "int_dot_zero\tleading_zero\tdate\tdate8\tdate8_mdy\tts\tbool_tf\tbool_yn\tdistinct_approx\tmax_len\t"
          "min_value\tmax_value\n")


def sample_clause(n_rows: int) -> str:
    if n_rows <= WHOLE_TABLE_UNDER:
        return ""
    if n_rows <= BLOCK_SAMPLE_OVER:
        return f"sample ({SAMPLE_ROWS} rows)"
    pct = min(100.0, max(0.0001, 100.0 * BLOCK_SAMPLE_TARGET / n_rows))
    return f"sample system ({pct:.4f})"


def profile_sql(table: str, n_rows: int, force_limit: bool = False, fat: bool = False) -> str:
    words = ", ".join("'" + w + "'" for w in NULL_WORDS)
    # FED_FDA_MAUDE_FULL is 13,042 rows and 14 GB: one VARIANT column, about a
    # megabyte a row. Turning 10,000 of those into text ran 18 minutes before it
    # was cancelled (2026-09-19). A fat table gets the first 200 rows instead.
    # 2026-09-19: a table under WHOLE_TABLE_UNDER used to get `limit 10000` too, so
    # "read all of it" read the first 10,000 rows. A 22,674-row portal table that
    # was loaded twice, once with 1988-11-07 and once with 1988/11/07, profiled
    # as 100% dates off the first load alone.
    src = (f'select * from LIBRARY_RAW.LANDING."{table}" limit {FAT_SAMPLE_ROWS}' if fat else
           f'select * from LIBRARY_RAW.LANDING."{table}"' if n_rows <= WHOLE_TABLE_UNDER and not force_limit else
           f'select * from LIBRARY_RAW.LANDING."{table}" limit {SAMPLE_ROWS}' if force_limit else
           f'select * from LIBRARY_RAW.LANDING."{table}" {sample_clause(n_rows)} limit {SAMPLE_ROWS}')
    # One row per (sampled row, column), so one query fits any width -- the
    # widest landing table has 3,311 columns, too many for per-column SQL.
    return f"""
with s as ({src}),
cells as (
    select f.key as col, trim(f.value::string) as v
    from (select object_construct_keep_null(*) o from s), lateral flatten(input => o) f
),
t as (
    select col, v,
           (v is not null and v <> '' and lower(v) not in ({words})) as ok
    from cells
)
select col,
       count(*),
       count_if(ok),
       count_if(v = ''),
       count_if(lower(v) in ({words})),
       count_if(ok and try_to_double(v) is not null),
       count_if(ok and regexp_like(v, '[+-]?[0-9]+')),
       count_if(ok and regexp_like(v, '[+-]?[0-9]+[.]0+')),
       count_if(ok and regexp_like(v, '0[0-9]+')),
       count_if(ok and regexp_like(v, '.*[0-9A-Za-z][-/][0-9A-Za-z].*') and try_to_date(v) is not null),
       count_if(ok and regexp_like(v, '(19|20)[0-9]{{6}}') and try_to_date(v, 'YYYYMMDD') is not null),
       count_if(ok and regexp_like(v, '(0[1-9]|1[0-2])[0-3][0-9](19|20)[0-9]{{2}}')
                   and try_to_date(v, 'MMDDYYYY') is not null),
       count_if(ok and v like '%:%' and try_to_timestamp(v) is not null),
       count_if(ok and lower(v) in ('true', 'false')),
       count_if(ok and lower(v) in ('y', 'n', 'yes', 'no')),
       approx_count_distinct(iff(ok, v, null)),
       max(length(v)),
       left(min(iff(ok, v, null)), 60),
       left(max(iff(ok, v, null)), 60)
from t group by col
"""


def staged_tables() -> set[str]:
    out: set[str] = set()
    for f in STAGING.rglob("*.sql"):
        out.update(s.upper() for s in re.findall(
            r"source\(\s*'ripple_raw'\s*,\s*'([^']+)'\s*\)", f.read_text(encoding="utf-8", errors="replace")))
    return out


def clean(x) -> str:
    return "" if x is None else re.sub(r"[\t\r\n]+", " ", str(x))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--tables", help="comma-separated landing table names")
    ap.add_argument("--staged-only", action="store_true", help="only tables a staging model reads")
    ap.add_argument("--resume", action="store_true", help="skip tables already in today's file")
    ap.add_argument("--threads", type=int, default=4)
    ap.add_argument("--out", help="output path (default reports/landing_column_profile_<date>.tsv)")
    args = ap.parse_args()

    c0 = db.connect()
    meta = db.rows(
        c0, "select table_name, row_count, bytes from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES "
            "where table_schema='LANDING' and table_type='BASE TABLE'")
    landing = {r[0]: int(r[1] or 0) for r in meta}
    fat = {r[0] for r in meta if r[1] and int(r[2] or 0) / int(r[1]) > FAT_BYTES_PER_ROW}
    dtype = {(r[0], r[1]): r[2] for r in db.rows(
        c0, "select table_name, column_name, data_type from LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
            "where table_schema='LANDING'")}

    if args.tables:
        wanted = [t.strip().upper() for t in args.tables.split(",") if t.strip()]
        missing = [t for t in wanted if t not in landing]
        if missing:
            print("not in LANDING:", ", ".join(missing))
        todo = [t for t in wanted if t in landing]
    elif args.staged_only:
        todo = sorted(t for t in staged_tables() if t in landing)
    else:
        todo = sorted(landing)

    out_path = Path(args.out) if args.out else (
        _REPO / "reports" / f"landing_column_profile_{dt.date.today().isoformat()}.tsv")
    done: set[str] = set()
    if args.resume and out_path.exists():
        with out_path.open(encoding="utf-8") as fh:
            next(fh, None)
            done = {ln.split("\t", 1)[0] for ln in fh}
    todo = [t for t in todo if t not in done]
    # Biggest first: the slow ones start while all threads are free.
    todo.sort(key=lambda t: -landing[t])

    jobs: queue.Queue = queue.Queue()
    for t in todo:
        jobs.put(t)
    total = len(todo)
    lock = threading.Lock()
    n_done = [0]
    failed: list[tuple[str, str]] = []
    started = time.time()

    fh = out_path.open("a" if done else "w", encoding="utf-8")
    if not done:
        fh.write(HEADER)

    def work() -> None:
        c = db.connect()
        while True:
            try:
                table = jobs.get_nowait()
            except queue.Empty:
                return
            n_rows = landing[table]
            lines: list[str] = []
            try:
                got = db.rows(c, profile_sql(table, n_rows, fat=table in fat)) if n_rows else []
                if n_rows and not got:
                    # A thin block sample can come back with zero blocks.
                    got = db.rows(c, profile_sql(table, n_rows, force_limit=True))
                for r in got:
                    col = r[0]
                    if col.startswith("_"):
                        continue
                    lines.append("\t".join(
                        [table, col, dtype.get((table, col), ""), str(n_rows)] + [clean(x) for x in r[1:]]) + "\n")
                if not got:
                    lines.append(f"{table}\t(empty table)\t\t{n_rows}" + "\t" * 18 + "\n")
            except Exception as e:  # one bad table is a line in the report, not a dead run
                with lock:
                    failed.append((table, " ".join(str(e).split())[:200]))
            with lock:
                fh.writelines(lines)
                fh.flush()
                n_done[0] += 1
                if n_done[0] % 100 == 0 or n_done[0] == total:
                    print(f"{n_done[0]} of {total}  {time.time() - started:,.0f}s", flush=True)

    threads = [threading.Thread(target=work) for _ in range(args.threads)]
    [t.start() for t in threads]
    [t.join() for t in threads]
    fh.close()

    print(f"\n{total} tables profiled in {time.time() - started:,.0f}s, {len(failed)} failed")
    for t, e in failed:
        print(f"  FAILED {t}: {e}")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
