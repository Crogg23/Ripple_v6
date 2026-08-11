"""Compare each mart model's own header row-count claim against the live table.

WHY THIS EXISTS (2026-08-11): 199 mart models carry a sentence like
"-- 5,544,626 rows as of ..." in their header. Nothing ever re-checked those
numbers after a re-ingest, so a source can advertise itself as far bigger (or
smaller) than the table actually is -- which is how a stale claim ends up in a
chart caption or a published figure.

Read-only. Uses INFORMATION_SCHEMA only, so it costs no warehouse compute.

  python scripts/check_mart_row_claims.py            # report to stdout + CSV
"""
from __future__ import annotations

import csv
import glob
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARTS = os.path.join(REPO, "library-onboarding", "ripple_dbt", "models", "marts")
OUT = os.path.join(REPO, "outputs", "_mart_row_claims_2026-08-11.csv")

# "5,544,626 rows" / "500000 rows" / "~1.9M rows" is NOT matched on purpose --
# only an exact digit claim is checkable, and only those are worth rewriting.
CLAIM_RE = re.compile(r"([0-9][0-9,]{3,})\s+rows", re.IGNORECASE)
TOLERANCE = 0.01


def claims_in(path):
    """Every exact row claim in a model's LEADING comment block, with line numbers."""
    out = []
    with open(path, encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, 1):
            s = line.strip()
            if not (s.startswith("--") or s.startswith("{#") or s.startswith("#")):
                # Claims below the header are inside SQL; leave those alone.
                if s and not s.startswith("/*") and i > 1:
                    break
                continue
            for m in CLAIM_RE.finditer(line):
                out.append((i, m.group(1), int(m.group(1).replace(",", ""))))
    return out


def live_counts():
    sys.path.insert(0, os.path.join(REPO, "library-onboarding"))
    try:
        from dotenv import load_dotenv
        load_dotenv(os.path.join(REPO, "library-onboarding", ".env"), override=True)
    except Exception:
        pass
    import snow
    cur = snow.connect().cursor()
    cur.execute("""
        SELECT TABLE_NAME, ROW_COUNT
        FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES
        WHERE TABLE_SCHEMA <> 'INFORMATION_SCHEMA'
    """)
    return {r[0].upper(): r[1] for r in cur.fetchall()}


def main():
    live = live_counts()
    rows = []
    for path in sorted(glob.glob(os.path.join(MARTS, "*", "*.sql"))):
        model = os.path.basename(path)[:-4]
        actual = live.get(model.upper())
        for line_no, raw, claimed in claims_in(path):
            if actual is None:
                verdict = "NO_LIVE_TABLE"
            elif actual == 0:
                verdict = "LIVE_EMPTY"
            elif abs(claimed - actual) / max(actual, 1) <= TOLERANCE:
                verdict = "OK"
            else:
                verdict = "DISAGREES"
            rows.append({
                "model": model,
                "folder": os.path.basename(os.path.dirname(path)),
                "line": line_no,
                "claimed_raw": raw,
                "claimed": claimed,
                "actual": actual,
                "verdict": verdict,
            })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    tally = Counter(r["verdict"] for r in rows)
    print(f"{len(rows)} row claims across "
          f"{len({r['model'] for r in rows})} models")
    for k, v in tally.most_common():
        print(f"  {k:14s} {v}")
    bad = [r for r in rows if r["verdict"] == "DISAGREES"]
    bad.sort(key=lambda r: -abs(r["claimed"] - (r["actual"] or 0)))
    print("\nworst 20 disagreements:")
    for r in bad[:20]:
        print(f"  {r['model'][:52]:52s} claims {r['claimed']:>12,}  actual {r['actual']:>12,}")
    print(f"\nwrote {OUT}")


if __name__ == "__main__":
    main()
