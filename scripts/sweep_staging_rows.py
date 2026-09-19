#!/usr/bin/env python3
"""Count every staging view against its landing table. Read-only.

Why this exists (2026-09-19): 289 staging views were hiding 9.2M rows while
every dbt test on them was green. A view that dedupes on a key and then tests
that same key for uniqueness can never fail -- the test asks "are there
duplicates left after I removed duplicates". The only check that catches a key
that does not identify a row is the dumb one: count the view, count the file.

What is checked, per model file under models/staging:
  - the landing table it reads (source('ripple_raw', X), honoring a schema.yml
    `identifier:` alias -- FED_SEC_13F_POSITIONS is really FED_SEC_13F_HOLDINGS)
  - its QUALIFY partition key
  - count(*) of the view in LIBRARY_STAGING.<schema>, against landing row_count
  - for a short view: distinct load run ids in landing, and the biggest load

What a hit means: view short of landing AND landing holds one load -> rows that
arrived together in one file were collapsed by the dedupe key. Not checked:
whether those rows are exact copies (a deliberate WHERE filter also reads as
"short" -- fed_osha_ita_300a_summary_2025 drops 3 malformed rows on purpose).
What a miss means: view equals landing -> the key holds for THIS load. It cannot
see a landing table that is itself a double load.

    python scripts/sweep_staging_rows.py                  # DBT_CROGERS
    python scripts/sweep_staging_rows.py --schema DBT_CROGERS_RIPPLE

Writes reports/staging_row_sweep_<date>.tsv. Four connections, ~4 minutes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import queue
import re
import sys
import threading
from pathlib import Path

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO))
from connect import db  # noqa: E402

STAGING = _REPO / "library-onboarding" / "ripple_dbt" / "models" / "staging"


def identifier_aliases() -> dict[str, str]:
    """source name -> real landing table, where a schema.yml says `identifier:`."""
    out: dict[str, str] = {}
    for yml in STAGING.rglob("*.yml"):
        lines = yml.read_text(encoding="utf-8", errors="replace").splitlines()
        for i, ln in enumerate(lines):
            m = re.match(r"\s*identifier:\s*(\S+)", ln)
            if not m:
                continue
            for back in range(i - 1, max(i - 6, -1), -1):
                n = re.match(r"\s*-\s*name:\s*(\S+)", lines[back])
                if n:
                    out[n.group(1)] = m.group(1)
                    break
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--schema", default="DBT_CROGERS")
    args = ap.parse_args()
    schema = args.schema.upper()

    c0 = db.connect()
    landing = {r[0]: r[1] for r in db.rows(
        c0, "select table_name, row_count from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_schema='LANDING'")}
    have = {r[0] for r in db.rows(
        c0, f"select table_name from LIBRARY_STAGING.INFORMATION_SCHEMA.TABLES where table_schema='{schema}'")}
    run_col: dict[str, str] = {}
    for t, col in db.rows(
            c0, "select table_name, column_name from LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
                "where table_schema='LANDING' and column_name in ('_SOURCE_RUN_ID','SOURCE_RUN_ID')"):
        run_col.setdefault(t, col)
    alias = identifier_aliases()

    jobs: queue.Queue = queue.Queue()
    for f in sorted(STAGING.rglob("*.sql")):
        txt = f.read_text(encoding="utf-8", errors="replace")
        srcs = [alias.get(s, s) for s in re.findall(r"source\(\s*'ripple_raw'\s*,\s*'([^']+)'\s*\)", txt)]
        part = re.search(r"partition\s+by\s+([^\n]+)", txt, flags=re.I)
        jobs.put((f.stem.upper(), srcs, part.group(1).strip()[:80] if part else "(no dedupe)"))
    total = jobs.qsize()

    out_path = _REPO / "reports" / f"staging_row_sweep_{dt.date.today().isoformat()}.tsv"
    lock = threading.Lock()
    results: list[tuple] = []

    def work() -> None:
        c = db.connect()
        while True:
            try:
                view, srcs, key = jobs.get_nowait()
            except queue.Empty:
                return
            src = srcs[0] if len(srcs) == 1 else ("+".join(srcs) or None)
            n_land = landing.get(src) if len(srcs) == 1 else None
            n_view = runs = biggest = None
            if len(srcs) != 1:
                verdict = "not comparable: zero or several landing sources"
            elif n_land is None:
                verdict = "landing table not found"
            elif view not in have:
                verdict = f"view not built in {schema}"
            else:
                try:
                    n_view = db.rows(c, f'select count(*) from LIBRARY_STAGING.{schema}."{view}"')[0][0]
                    if n_view == n_land:
                        verdict = "exact"
                    elif n_view > n_land:
                        verdict = "view larger than landing"
                    elif src in run_col:
                        runs, biggest = db.rows(
                            c, f'select count(*), max(n) from (select "{run_col[src]}" k, count(*) n '
                               f'from LIBRARY_RAW.LANDING."{src}" group by 1)')[0]
                        # DATA TRAP: on some tables the run id is a per-ROW uuid
                        # (FED_CMS_OPT_OUT_AFFIDAVITS: 57,209 rows, 57,209 run ids),
                        # so "biggest load" is 1 row and any short view looked fine.
                        # Under 100 rows per run id, it is not a load id: one load.
                        if runs and n_land / runs < 100:
                            runs, biggest = 1, n_land
                        verdict = ("ONE LOAD: key hides rows" if runs <= 1 else
                                   "many loads: dedupe plausibly right" if n_view >= biggest else
                                   "many loads AND short of biggest load: key hides rows")
                    else:
                        verdict = "short, no run-id column to separate reloads"
                except Exception as e:  # a broken view is a finding, not a crash
                    verdict = "count failed: " + " ".join(str(e).split())[:160]
            with lock:
                results.append((view, src, n_land, n_view, runs, biggest, verdict, key))
                if len(results) % 200 == 0:
                    print(f"{len(results)} of {total}", flush=True)

    threads = [threading.Thread(target=work) for _ in range(4)]
    [t.start() for t in threads]
    [t.join() for t in threads]

    # A renamed model leaves its OLD view behind in the warehouse, still on the
    # old key, and this sweep walks files so it never saw them
    # (STG_FED_EPA_ECHO__RECORDS sat beside the new __FACILITIES view).
    modelled = {r[0] for r in results}
    for orphan in sorted(v for v in have if v.startswith("STG_") and v not in modelled):
        results.append((orphan, None, None, None, None, None, "view in warehouse, no model file", ""))

    results.sort()
    with out_path.open("w", encoding="utf-8") as fh:
        fh.write("view\tsource\tlanding_rows\tview_rows\truns\tbiggest_run_rows\tverdict\tkey\n")
        for r in results:
            fh.write("\t".join("" if x is None else str(x) for x in r) + "\n")

    counts: dict[str, int] = {}
    for r in results:
        k = r[6].split(":")[0] if r[6].startswith("count failed") else r[6]
        counts[k] = counts.get(k, 0) + 1
    hidden = sum((r[2] - r[3]) for r in results if "key hides rows" in r[6] and r[6].startswith("ONE"))
    print(f"\n{total} models, schema {schema}")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{v:>6}  {k}")
    print(f"rows hidden behind a one-load key: {hidden:,}")
    print(f"wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
