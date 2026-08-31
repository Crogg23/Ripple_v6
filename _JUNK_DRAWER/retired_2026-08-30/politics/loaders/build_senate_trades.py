"""Senate stock trades — the STOCK Act disclosure leg (Senate only).

Lands the Senate Stock Watcher aggregate (a volunteer-maintained re-parse of
the Senate's official eFD periodic transaction reports) and builds one mart
with an HONEST member match.

  LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER   one row per disclosed trade
  LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES trades + bioguide match

SCHEMA REALITY (verified live 2026-08-01): the source carries NO bioguide and
NO disclosure date — fields are transaction_date, owner, ticker,
asset_description, asset_type, type, amount, comment, senator (display name),
ptr_link. The prior scouting note claiming "bioguide-keyed" was WRONG. The
member link is therefore a NAME MATCH against the member crosswalk
(surname + senate chamber + term-span, the exact rule build_who_won.py uses),
recorded per row in MATCH_METHOD so a name-only identity never silently
reads as a hard fact. AMOUNT is the disclosure BAND text and is kept
verbatim — never midpointed.

LEGAL: journalism use only. 5 USC 13107(c)(1) forbids commercial, credit,
or solicitation use of financial-disclosure data. The registry row carries
this in LICENSE_TERMS; any commercial release gate must exclude this table
and everything derived from it.

Usage:
  python politics/loaders/build_senate_trades.py              # fetch + land + mart
  python politics/loaders/build_senate_trades.py --skip-fetch # rebuild mart only
Referee: politics/loaders/smoke_senate_trades.py
"""
from __future__ import annotations

import sys
from pathlib import Path as _RepoPath

import pandas as pd
import requests

_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))
import snow  # noqa: E402
from build_skeleton import land  # noqa: E402

SOURCE_ID = "fed_senate_stock_watcher"
URL = ("https://raw.githubusercontent.com/timothycarambat/"
       "senate-stock-watcher-data/master/aggregate/all_transactions.json")
UA = {"User-Agent": "Mozilla/5.0 (Ripple Library onboarding; senate trades)"}

COLS = ["TRANSACTION_DATE", "OWNER", "TICKER", "ASSET_DESCRIPTION",
        "ASSET_TYPE", "TYPE", "AMOUNT", "COMMENT", "SENATOR", "PTR_LINK"]

MART = "LIBRARY_MARTS.POLITICS.POLITICS__SENATE_TRADES"

# The member match mirrors build_who_won.py: normalized surname tail +
# senate term type + trade-year within the term span; suffixes stripped;
# one row per trade, unmatched stays NULL with match_method='unmatched'.
MART_DDL = f"""
CREATE OR REPLACE TABLE {MART} AS
WITH t AS (
  SELECT
    TRY_TO_DATE(TRANSACTION_DATE, 'MM/DD/YYYY')            AS transaction_date,
    OWNER, TICKER, ASSET_DESCRIPTION, ASSET_TYPE, TYPE,
    AMOUNT,                                        -- the disclosure BAND, verbatim
    COMMENT, SENATOR, PTR_LINK,
    -- every LANDED row keeps exactly one mart row: identical duplicate
    -- filings are real filings, never collapsed (live lesson 2026-08-01:
    -- a content-keyed dedup silently dropped 398 rows)
    ROW_NUMBER() OVER (ORDER BY PTR_LINK, TRANSACTION_DATE) AS row_seq,
    -- name cleanup: trailing commas/periods first ('Jerry Moran,' is in the
    -- live file), then generational suffixes
    REGEXP_REPLACE(
        REGEXP_REPLACE(UPPER(TRIM(SENATOR)), '[,.]+$', ''),
        '[ ,]+(JR|SR|II|III|IV|2ND|3RD)\\\\.?$', '')        AS name_clean
  FROM LIBRARY_RAW.LANDING.FED_SENATE_STOCK_WATCHER
),
matched AS (
  SELECT t.*,
         x.bioguide, x.full_name AS spine_name,
         CASE WHEN x.bioguide IS NULL THEN 'unmatched'
              ELSE 'surname+senate+term-span' END AS match_method
  FROM t
  LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x
    ON x.last_term_type = 'sen'
   AND (t.name_clean = UPPER(x.name_last)
        OR ENDSWITH(t.name_clean, ' ' || UPPER(x.name_last)))
   AND COALESCE(YEAR(t.transaction_date), 2020)
       BETWEEN YEAR(TRY_TO_DATE(x.first_term_start)) - 1
           AND COALESCE(YEAR(TRY_TO_DATE(x.last_term_end)), 2030) + 1
  QUALIFY ROW_NUMBER() OVER (
      PARTITION BY t.row_seq
      ORDER BY (x.bioguide IS NOT NULL) DESC, x.full_name) = 1
)
SELECT transaction_date, owner, ticker, asset_description, asset_type,
       type AS transaction_type, amount AS amount_band, comment, senator,
       ptr_link, bioguide, spine_name, match_method
FROM matched
"""


def to_frame(recs: list[dict]) -> pd.DataFrame:
    """Source JSON records -> the landing frame: columns upper-cased and
    ordered, missing fields NULL, values untouched (AMOUNT stays the band
    text, SENATOR stays the display name). Pure — unit-tested offline."""
    df = pd.DataFrame.from_records(recs)
    df.columns = [c.upper() for c in df.columns]
    for c in COLS:
        if c not in df.columns:
            df[c] = None
    return df[COLS]


def fetch_and_land():
    print(f"fetching {URL}")
    r = requests.get(URL, timeout=120, headers=UA)
    r.raise_for_status()
    df = to_frame(r.json())
    print(f"parsed {len(df):,} trades")
    land(df, SOURCE_ID, URL,
         "Senate Stock Watcher aggregate (volunteer re-parse of Senate eFD "
         "PTRs). JOURNALISM USE ONLY - 5 USC 13107(c)(1).",
         min_rows=5_000)


def build_mart():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        cur.execute(MART_DDL)
        conn.commit()
        print(f"  built {MART}")
        cur.execute(f"""SELECT COUNT(*),
                               SUM(IFF(bioguide IS NOT NULL, 1, 0)),
                               COUNT(DISTINCT senator),
                               COUNT(DISTINCT IFF(bioguide IS NOT NULL,
                                                  senator, NULL))
                        FROM {MART}""")
        n, m, sen, sen_m = cur.fetchone()
        print(f"INTEGRITY: {n:,} trades; {m:,} matched to a bioguide "
              f"({100 * m / max(n, 1):.1f}%); senators {sen_m}/{sen} matched")
        cur.execute(f"""SELECT senator, COUNT(*) FROM {MART}
                        WHERE bioguide IS NULL GROUP BY 1 ORDER BY 2 DESC
                        LIMIT 10""")
        misses = cur.fetchall()
        if misses:
            print("  top unmatched senators (name-match quarantine):")
            for s, c in misses:
                print(f"    {s}: {c}")
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    if "--skip-fetch" not in sys.argv:
        fetch_and_land()
    build_mart()
    print("\nDONE. Referee: politics/loaders/smoke_senate_trades.py")
