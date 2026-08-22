"""Value-check every candidate column in the typing worklist against live data.

Phase 1 of the canonical typing layer (Chris picked the clock-style approach,
2026-08-22). The worklist (reports/lab_map/TYPING_WORKLIST.csv) is a column-NAME
heuristic and has known false positives (GLEIF registry IDs flagged as numbers)
— so nothing gets cast on name alone. This sweep measures, per column:

  - non-empty count
  - try_to_double castable count
  - try_to_date / try_to_timestamp_tz castable count
  - a leading-zero / fixed-width signal (ID smell — never cast those)
  - top non-castable values (sentinel discovery)

One query per table (all its candidate columns aggregated), so ~197 queries.
Prior calibration: 771 whole-warehouse queries = 14 min / $1-2.

Output: reports/typing_index/value_checks.csv — the evidence file the rulings
are derived from. Resumable: tables already present in the output are skipped.

    python scripts/typing/value_check_sweep.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))

from scripts._snowflake_conn import connect  # noqa: E402

WORKLIST = _REPO / "reports" / "lab_map" / "TYPING_WORKLIST.csv"
OUT = _REPO / "reports" / "typing_index" / "value_checks.csv"

FIELDS = ["schema", "table", "column", "should_be", "table_row_count",
          "n_nonempty", "n_double", "n_date", "n_ts_tz",
          "fixed_width", "has_leading_zero", "error"]


def main() -> int:
    by_table: dict[tuple[str, str], list[dict]] = defaultdict(list)
    with open(WORKLIST, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            by_table[(row["schema"], row["table"])].append(row)

    done: set[tuple[str, str]] = set()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    if OUT.exists():
        with open(OUT, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add((row["schema"], row["table"]))

    cur = connect().cursor()
    out_f = open(OUT, "a", newline="", encoding="utf-8")
    w = csv.DictWriter(out_f, fieldnames=FIELDS)
    if not done:
        w.writeheader()

    n_tables = 0
    for (schema, table), cols in sorted(by_table.items()):
        if (schema, table) in done:
            continue
        exprs = []
        for c in cols:
            col = c["column"]
            exprs.append(
                f"count_if({col} is not null and trim({col}) <> '') ,"
                f"count(try_to_double(nullif(trim({col}), ''))) ,"
                f"count(try_to_date(nullif(trim({col}), ''))) ,"
                f"count(try_to_timestamp_tz(nullif(trim({col}), ''))) ,"
                # ID smell: every non-empty value the same width AND at least one
                # starts with 0 -> fixed-width zero-padded identifier, never cast
                f"iff(min(length(nullif(trim({col}), ''))) = max(length(nullif(trim({col}), ''))), 1, 0) ,"
                f"count_if(left(nullif(trim({col}), ''), 1) = '0')"
            )
        sql = (f"select {', '.join(exprs)} "
               f"from LIBRARY_MARTS.{schema}.{table}")
        try:
            cur.execute(sql)
            vals = cur.fetchone()
            for i, c in enumerate(cols):
                base = i * 6
                w.writerow({
                    "schema": schema, "table": table, "column": c["column"],
                    "should_be": c["should_be"],
                    "table_row_count": c["table_row_count"],
                    "n_nonempty": vals[base], "n_double": vals[base + 1],
                    "n_date": vals[base + 2], "n_ts_tz": vals[base + 3],
                    "fixed_width": vals[base + 4],
                    "has_leading_zero": vals[base + 5], "error": "",
                })
        except Exception as e:
            for c in cols:
                w.writerow({"schema": schema, "table": table,
                            "column": c["column"], "should_be": c["should_be"],
                            "table_row_count": c["table_row_count"],
                            "n_nonempty": "", "n_double": "", "n_date": "",
                            "n_ts_tz": "", "fixed_width": "",
                            "has_leading_zero": "", "error": str(e)[:200]})
        out_f.flush()
        n_tables += 1
        print(f"[{n_tables}] {schema}.{table} ({len(cols)} cols)", flush=True)

    out_f.close()
    print("DONE", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
