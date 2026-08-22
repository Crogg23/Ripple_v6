"""Derive per-column typing rulings from the value-check evidence.

Phase 2 of the canonical typing layer. Pure local — no warehouse. Reads
reports/typing_index/value_checks.csv, writes reports/typing_index/
typing_rulings.csv with one ruling per column:

  cast_double   -- >=99% of non-empty values parse as numbers, dates don't fit
  cast_date     -- >=99% parse as dates/timestamps, numbers don't fit
  keep_text     -- with a reason:
      id_smell        fixed-width values with leading zeros (ZIP/FIPS class —
                      casting these is the exact 2026-08-10 bug)
      empty           column has no non-empty values to verify against
      partial_cast    50-99% castable — unknown sentinels, needs a human look
      low_cast        <50% castable — the name lied, it's not a measure
      query_error     the check query failed
  ambiguous_number / ambiguous_date -- BOTH parse >=99% (e.g. '20120101').
      Ruled by the worklist's name heuristic but flagged — these are exactly
      the epoch-trap class (TRY_TO_DATE on year numbers collapses to 1970),
      so the guard test must range-check every cast_date/ambiguous_date.

    python scripts/typing/derive_rulings.py
"""
from __future__ import annotations

import csv
import sys
from collections import Counter
from pathlib import Path

_REPO = Path(__file__).resolve().parents[2]
CHECKS = _REPO / "reports" / "typing_index" / "value_checks.csv"
OUT = _REPO / "reports" / "typing_index" / "typing_rulings.csv"

FIELDS = ["schema", "table", "column", "ruling", "reason",
          "n_nonempty", "pct_double", "pct_date"]


def main() -> int:
    rows = list(csv.DictReader(open(CHECKS, newline="", encoding="utf-8")))
    out = []
    for r in rows:
        if r["error"]:
            out.append((r, "keep_text", "query_error", "", ""))
            continue
        ne = int(r["n_nonempty"] or 0)
        if ne == 0:
            out.append((r, "keep_text", "empty", "", ""))
            continue
        pd_ = int(r["n_double"] or 0) / ne
        # timestamp_tz parses everything a date parse does and more
        pt = max(int(r["n_date"] or 0), int(r["n_ts_tz"] or 0)) / ne
        pd_s, pt_s = f"{pd_:.3f}", f"{pt:.3f}"
        if r["fixed_width"] == "1" and int(r["has_leading_zero"] or 0) > 0:
            out.append((r, "keep_text", "id_smell", pd_s, pt_s))
        elif pd_ >= 0.99 and pt >= 0.99:
            want = "date" if r["should_be"] == "date" else "number"
            out.append((r, f"ambiguous_{want}", "both_parse", pd_s, pt_s))
        elif pd_ >= 0.99:
            out.append((r, "cast_double", "clean", pd_s, pt_s))
        elif pt >= 0.99:
            out.append((r, "cast_date", "clean", pd_s, pt_s))
        elif max(pd_, pt) >= 0.50:
            out.append((r, "keep_text", "partial_cast", pd_s, pt_s))
        else:
            out.append((r, "keep_text", "low_cast", pd_s, pt_s))

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r, ruling, reason, pd_s, pt_s in out:
            w.writerow({"schema": r["schema"], "table": r["table"],
                        "column": r["column"], "ruling": ruling,
                        "reason": reason, "n_nonempty": r["n_nonempty"],
                        "pct_double": pd_s, "pct_date": pt_s})

    tally = Counter(f"{ruling}/{reason}" for _, ruling, reason, _, _ in out)
    for k, v in tally.most_common():
        print(f"{v:5d}  {k}")
    print(f"total {len(out)} -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
