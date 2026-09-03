"""Derivation rules for the three date/time shapes a plain cast can't fix:
range-in-one-field, format-code-as-data, and time-of-day with no date attached.

Reads reports/recon/date_cast_inventory_2026-09-03.csv (from date_cast_inventory.py)
and the gen-1 recon JSON for column context, then emits ready SQL per column:

  range        two new columns, <COL>_START / <COL>_END, split on the detected
               separator and cast per side. Only emitted for the two verified
               formats below — anything else stays flagged, not guessed.
  granularity  a CASE translating the strftime code to a plain label.
  time_pair    a combined TIMESTAMP built from this TIME column plus a sibling
               DATE column found by exact name match (TIME token -> DATE token
               in the same table). No sibling found -> stays unresolved, not
               guessed.

Every format string below was validated against Snowflake with a zero-table
constant SELECT before being written here (see session transcript). Read-only:
this script only reads local JSON/CSV and writes a CSV. No warehouse write.

Output: reports/recon/date_derive_rules_2026-09-03.csv
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
JSON_DIR = REPO / "reports" / "recon" / "content" / "json"
INV_CSV = REPO / "reports" / "recon" / "date_cast_inventory_2026-09-03.csv"
OUT_CSV = REPO / "reports" / "recon" / "date_derive_rules_2026-09-03.csv"

TIME_TOKEN = re.compile(r"(?<![A-Z])TIME(?![A-Z])")

GRANULARITY_CODES = {"%Y-%m-%d": "day", "%Y-%m": "month", "%Y": "year"}

TIME_COMBINE = (
    "COALESCE("
    "TRY_TO_TIMESTAMP_NTZ({date_str} || ' ' || TRIM({time_col}), 'YYYY-MM-DD HH24:MI:SS'), "
    "TRY_TO_TIMESTAMP_NTZ({date_str} || ' ' || TRIM({time_col}), 'YYYY-MM-DD HH12:MI:SS AM'), "
    "TRY_TO_TIMESTAMP_NTZ({date_str} || ' ' || TRIM({time_col}), 'YYYY-MM-DD HH24:MI'), "
    "TRY_TO_TIMESTAMP_NTZ({date_str} || ' ' || TRIM({time_col}), 'YYYY-MM-DD HH12:MI AM'))"
)


def q(name: str) -> str:
    return '"' + name.replace('"', '""') + '"'


def classify_unresolved(col: str, sample: str) -> str:
    s = (sample or "").strip()
    if re.fullmatch(r"\d{2}[A-Za-z]{3}\d{4}-\d{2}[A-Za-z]{3}\d{4}", s):
        return "range_ddmonyyyy"
    if re.fullmatch(r"[A-Za-z]+,? \d{4} to [A-Za-z]+,? \d{4}", s):
        return "range_month_yyyy"
    if s in GRANULARITY_CODES:
        return "granularity"
    if TIME_TOKEN.search(col) and re.fullmatch(r"\s*\d{1,2}:\d{2}(:\d{2})?\s*(AM|PM)?\s*", s, re.I):
        return "time_pair"
    return "other"


def main():
    inv = list(csv.DictReader(open(INV_CSV, encoding="utf-8")))
    by_table_col = {(r["table"], r["column"]): r for r in inv}
    unresolved = [r for r in inv if r["bucket"] == "unclassified_needs_eyeball"]

    out_rows = []
    range_n = granularity_n = paired_n = still_manual_n = 0

    for r in unresolved:
        table, col, sample = r["table"], r["column"], r["sample"]
        kind = classify_unresolved(col, sample)
        qc = q(col)

        if kind == "range_ddmonyyyy":
            start = f"TRY_TO_DATE(SPLIT_PART({qc}, '-', 1), 'DDMONYYYY')"
            end = f"TRY_TO_DATE(SPLIT_PART({qc}, '-', 2), 'DDMONYYYY')"
            out_rows.append(dict(table=table, column=col, rule="range", pattern="ddmonyyyy", sibling="",
                                  new_columns=f"{col}_START, {col}_END",
                                  expr=f"{col}_START: {start}  |  {col}_END: {end}"))
            range_n += 1
            continue

        if kind == "range_month_yyyy":
            start = f"TRY_TO_DATE(SPLIT_PART({qc}, ' to ', 1), 'MMMM, YYYY')"
            end = f"TRY_TO_DATE(SPLIT_PART({qc}, ' to ', 2), 'MMMM, YYYY')"
            out_rows.append(dict(table=table, column=col, rule="range", pattern="monthyyyy", sibling="",
                                  new_columns=f"{col}_START, {col}_END",
                                  expr=f"{col}_START: {start}  |  {col}_END: {end}"))
            range_n += 1
            continue

        if kind == "granularity":
            cases = " ".join(f"WHEN {code!r} THEN '{label}'" for code, label in GRANULARITY_CODES.items())
            expr = f"CASE {qc} {cases} ELSE NULL END"
            out_rows.append(dict(table=table, column=col, rule="granularity", pattern="", sibling="",
                                  new_columns=f"{col}_LABEL", expr=expr))
            granularity_n += 1
            continue

        if kind == "time_pair":
            date_col = TIME_TOKEN.sub("DATE", col)
            sibling = by_table_col.get((table, date_col))
            if sibling and sibling["bucket"] in ("native", "content_date"):
                date_expr = sibling["cast_expr"] or q(date_col)
                if sibling["bucket"] == "native":
                    date_str = f"TO_VARCHAR({date_expr}, 'YYYY-MM-DD')"
                else:
                    date_str = f"TO_VARCHAR(({date_expr}), 'YYYY-MM-DD')"
                combine = TIME_COMBINE.format(date_str=date_str, time_col=qc)
                out_rows.append(dict(table=table, column=col, rule="time_pair", pattern=sibling["bucket"],
                                      sibling=date_col, new_columns=f"{col}_FULL paired with {date_col}",
                                      expr=combine))
                paired_n += 1
                continue

        out_rows.append(dict(table=table, column=col, rule="still_manual", pattern="", sibling="",
                              new_columns="", expr=""))
        still_manual_n += 1

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["table", "column", "rule", "pattern", "sibling", "new_columns", "expr"])
        w.writeheader()
        w.writerows(out_rows)

    print(f"range columns resolved: {range_n}")
    print(f"granularity columns resolved: {granularity_n}")
    print(f"time/date pairs resolved: {paired_n}")
    print(f"still manual: {still_manual_n}")
    print(f"csv={OUT_CSV}")


if __name__ == "__main__":
    main()
