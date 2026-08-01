"""Referee for the Senate trades leg — must pass before the data is used.

Checks (against LIVE warehouse tables):
  1. Landing table exists with a sane row count (>= 5,000 trades).
  2. Named-member check: Sheldon Whitehouse / Ron Wyden class of frequent
     filers resolve — specifically, trades matching 'Wyden' map to exactly
     ONE bioguide, and that bioguide's spine row is a senator.
  3. Match-through: >= 90% of TRADES carry a bioguide (the source is
     name-only — see build_senate_trades.py header — so a perfect rate is
     impossible; the quarantine list is printed, not hidden).
  4. Amount bands are bands (contain '$' and '-'), never bare numbers.
  5. Freshness: the max transaction date is PRINTED (volunteer-maintained
     source — staleness is reported, never asserted).
"""
from __future__ import annotations

import sys
from pathlib import Path as _RepoPath

_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
import snow  # noqa: E402

LANDING = "LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER"
MART = "LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES"


def main() -> int:
    conn = snow.connect()
    cur = conn.cursor()
    failures = []

    def q1(sql):
        cur.execute(sql)
        return cur.fetchone()

    n_land = q1(f"SELECT COUNT(*) FROM {LANDING}")[0]
    print(f"landing rows: {n_land:,}")
    if n_land < 5_000:
        failures.append(f"landing count {n_land} < 5,000")

    n, m = q1(f"SELECT COUNT(*), SUM(IFF(bioguide IS NOT NULL, 1, 0)) "
              f"FROM {MART}")
    rate = 100 * (m or 0) / max(n, 1)
    print(f"mart rows: {n:,}; bioguide matched: {m:,} ({rate:.1f}%)")
    if rate < 90:
        failures.append(f"bioguide match-through {rate:.1f}% < 90%")

    wyden = q1(f"""SELECT COUNT(DISTINCT bioguide) FROM {MART}
                   WHERE senator ILIKE '%wyden%'
                     AND bioguide IS NOT NULL""")[0]
    print(f"named-member check (Wyden): {wyden} distinct bioguide(s)")
    if wyden != 1:
        failures.append(f"Wyden resolves to {wyden} bioguides, expected 1")
    else:
        row = q1(f"""SELECT s.bioguide, x.full_name, x.last_term_type
                     FROM {MART} s
                     JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x
                       ON x.bioguide = s.bioguide
                     WHERE s.senator ILIKE '%wyden%' LIMIT 1""")
        print(f"  -> {row[0]} {row[1]} ({row[2]})")
        if row[2] != "sen":
            failures.append("Wyden's matched spine row is not a senator")

    # A band is a range ('$15,001 - $50,000'), open-ended ('$1,000,001 +'),
    # or the source's literal 'Unknown' (463 rows in the live file — the
    # filing didn't yield a band; kept verbatim, never invented). The only
    # forbidden shape is a bare exact number pretending to be precise.
    bad_amt = q1(f"""SELECT COUNT(*) FROM {MART}
                     WHERE amount_band IS NOT NULL
                       AND amount_band NOT LIKE '%$%'
                       AND UPPER(amount_band) <> 'UNKNOWN'""")[0]
    print(f"amount values that are neither a band nor 'Unknown': {bad_amt}")
    if bad_amt > 0:
        failures.append(f"{bad_amt} amount values are not disclosure bands")

    # mart must carry EVERY landed row (no silent dedup)
    n_mart_vs_land = q1(f"""SELECT (SELECT COUNT(*) FROM {MART})
                          - (SELECT COUNT(*) FROM {LANDING})""")[0]
    print(f"mart minus landing rows: {n_mart_vs_land}")
    if n_mart_vs_land != 0:
        failures.append(f"mart row count differs from landing by "
                        f"{n_mart_vs_land} — rows were dropped or fanned out")

    mx, mn = q1(f"SELECT MAX(transaction_date), MIN(transaction_date) "
                f"FROM {MART}")
    print(f"transaction dates span {mn} .. {mx} (freshness REPORTED, not "
          f"asserted - volunteer-maintained source)")

    print("\ntop unmatched (quarantine, informational):")
    cur.execute(f"""SELECT senator, COUNT(*) FROM {MART}
                    WHERE bioguide IS NULL GROUP BY 1
                    ORDER BY 2 DESC LIMIT 5""")
    for s, c in cur.fetchall():
        print(f"  {s}: {c}")

    if failures:
        print("\nSMOKE FAILED:")
        for f in failures:
            print(f"  FAIL {f}")
        return 1
    print("\nSMOKE PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
