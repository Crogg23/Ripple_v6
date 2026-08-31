"""TASK B -- MEDSL "who won": land MIT Election Lab constituency returns + build the
who_won mart joined to the member spine.

REALITY CHECK (verified against the actual data 2026-06-30, both contradict the brief):
  1. The MEDSL constituency files do NOT carry FEC_candidate_id or ICPSR. The candidate
     is a NAME string only. So the spine join is NAME + state (+ district) -- a fuzzy,
     LEAD-grade match, NOT the advertised steel key. We MEASURE the match rate and never
     auto-publish a name-only identity as fact.
  2. The House + President + county-president Dataverse files are GUESTBOOK-gated (need a
     free Harvard Dataverse API token -- a human gate). Only Senate (1976-2024) and the
     GitHub constituency-returns mirror (House/President, but only through 2018) are
     ungated. Set MEDSL_DV_TOKEN in the env to unlock the clean full House/President.

So this loader lands what is cleanly available now (Senate 1976-2024, complete) and is
structured to land House/President the moment a token is present.

  python politics/loaders/build_who_won.py            # land available + build + referee
  python politics/loaders/build_who_won.py --skip-fetch
"""
from __future__ import annotations

import io
import os
import sys

import pandas as pd
import requests

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO))
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(str(_REPO / "library-onboarding" / ".env"), override=True)

import snow  # noqa: E402
from build_skeleton import land  # noqa: E402  (TEXT mirror + provenance + INGEST_RUNS)

UA = {"User-Agent": "Ripple-Library/1.0 (data onboarding; w.rogers9999@gmail.com)"}
DV = "https://dataverse.harvard.edu"
TOKEN = os.environ.get("MEDSL_DV_TOKEN", "").strip()

# MEDSL sources. 'dataverse_file' = (doi, datafile_id). Senate is ungated; House/President
# are guestbook-gated (need TOKEN) -- their ungated GitHub fallback stops at 2018/2016.
SPECS = {
    "fed_medsl_senate_returns": dict(
        office="US SENATE", gated=False,
        dataverse_file=(["10.7910/DVN/PEJ5QU"], 13887039),
        url="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/PEJ5QU",
        coverage="1976-2024 (complete)",
    ),
    "fed_medsl_house_returns": dict(
        office="US HOUSE", gated=True,
        dataverse_file=(["10.7910/DVN/IG0UN2"], 13592823),
        github="https://raw.githubusercontent.com/MEDSL/constituency-returns/master/1976-2018-house.csv",
        url="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/IG0UN2",
        coverage="1976-2024 via token; 1976-2018 via ungated GitHub fallback",
    ),
    "fed_medsl_president_returns": dict(
        office="US PRESIDENT", gated=True,
        dataverse_file=(["10.7910/DVN/42MVDX"], 13887042),
        github="https://raw.githubusercontent.com/MEDSL/constituency-returns/master/1976-2016-president.csv",
        url="https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/42MVDX",
        coverage="1976-2024 via token; 1976-2016 via ungated GitHub fallback",
    ),
}


def _read_bytes_to_df(content: bytes) -> pd.DataFrame:
    for sep in ("\t", ","):
        try:
            df = pd.read_csv(io.BytesIO(content), sep=sep, dtype=str,
                             low_memory=False, encoding_errors="replace", keep_default_na=False)
            if df.shape[1] > 3:
                return df
        except Exception:
            pass
    return pd.read_csv(io.BytesIO(content), sep=None, engine="python", dtype=str,
                       encoding_errors="replace", keep_default_na=False)


def fetch_source(sid: str, spec: dict):
    """Return (df, url, note) or (None, None, reason). Prefers the clean Dataverse file
    (with token if gated); falls back to the ungated GitHub mirror."""
    dois, fid = spec["dataverse_file"]
    headers = dict(UA)
    if TOKEN:
        headers["X-Dataverse-key"] = TOKEN
    if (not spec["gated"]) or TOKEN:
        r = requests.get(f"{DV}/api/access/datafile/{fid}?format=original", headers=headers, timeout=300)
        if r.status_code == 200:
            return _read_bytes_to_df(r.content), spec["url"], f"Dataverse ({spec['coverage'].split(';')[0]})"
        if not spec["gated"]:
            return None, None, f"Dataverse HTTP {r.status_code}"
        print(f"  [{sid}] Dataverse gated + token rejected (HTTP {r.status_code}); trying GitHub mirror")
    gh = spec.get("github")
    if gh:
        r = requests.get(gh, headers=UA, timeout=300)
        if r.status_code == 200:
            return _read_bytes_to_df(r.content), gh, "GitHub mirror (PARTIAL: ends 2018/2016 -- set MEDSL_DV_TOKEN for full)"
        return None, None, f"GitHub HTTP {r.status_code}"
    return None, None, "gated, no token, no GitHub fallback"


def fetch_and_land():
    landed = {}
    for sid, spec in SPECS.items():
        print(f"\n[{sid}] ({spec['office']})")
        df, url, note = fetch_source(sid, spec)
        if df is None:
            print(f"  SKIP -- {note}")
            continue
        yrs = sorted(set(df[[c for c in df.columns if c.lower() == 'year'][0]]))
        print(f"  fetched {len(df):,} rows, {df.shape[1]} cols, years {yrs[0]}..{yrs[-1]}  [{note}]")
        land(df, sid, url, f"MEDSL {spec['office']} constituency returns. {note}. "
                           f"NO FEC/ICPSR in source -> spine join is name+state(+district), LEAD-grade.")
        landed[sid] = spec
    return landed


# ---------------------------------------------------------------------------
# The mart: one WINNER per race, name-matched to the member spine.
# No FEC/ICPSR in source -> the bioguide match is surname(normalized)+state+chamber+
# term-span-contains-election-year. ENDSWITH handles compound surnames (BLUNT ROCHESTER);
# the suffix strip handles "KING JR.". match_method records HOW each row resolved so a
# name-only identity never silently reads as a hard fact.
# ---------------------------------------------------------------------------
MART = "LIBRARY_MARTS.POLITICS.POLITICS__WHO_WON"

MART_DDL = f"""
CREATE OR REPLACE TABLE {MART} AS
WITH base AS (
  -- unify the 3 MEDSL tables to a common grain. NB MEDSL mixes case across its old
  -- (lowercase 'gen'/'total') and new 2022+ (uppercase) files -> filter case-insensitively.
  -- Keep general + runoff rows; runoff (GA/LA/MS) is resolved as decisive below.
  SELECT 'SENATE' office, YEAR yr, STATE_PO st, 'statewide' district, SPECIAL special,
         UPPER(STAGE) stage_raw, CANDIDATE candidate,
         COALESCE(NULLIF(PARTY_SIMPLIFIED,''),PARTY_DETAILED) party,
         TRY_TO_NUMBER(CANDIDATEVOTES) cv, TRY_TO_NUMBER(TOTALVOTES) tv
  FROM LIBRARY_RAW.LANDING.FED_MEDSL_SENATE_RETURNS
  WHERE UPPER(STAGE) IN ('GEN','GEN RUNOFF','RUNOFF') AND UPPER(WRITEIN)<>'TRUE' AND UPPER(MODE)='TOTAL'
  UNION ALL
  SELECT 'HOUSE', YEAR, STATE_PO, DISTRICT, SPECIAL, UPPER(STAGE), CANDIDATE, PARTY,
         TRY_TO_NUMBER(CANDIDATEVOTES), TRY_TO_NUMBER(TOTALVOTES)
  FROM LIBRARY_RAW.LANDING.FED_MEDSL_HOUSE_RETURNS
  WHERE UPPER(STAGE) IN ('GEN','GEN RUNOFF','RUNOFF') AND UPPER(WRITEIN)<>'TRUE' AND UPPER(MODE)='TOTAL'
  UNION ALL
  SELECT 'PRESIDENT', YEAR, STATE_PO, 'statewide', 'False', 'GEN', CANDIDATE, PARTY,
         TRY_TO_NUMBER(CANDIDATEVOTES), TRY_TO_NUMBER(TOTALVOTES)
  FROM LIBRARY_RAW.LANDING.FED_MEDSL_PRESIDENT_RETURNS
  WHERE UPPER(WRITEIN)<>'TRUE'
),
decisive AS (   -- when a race has a runoff, the runoff supersedes the general
  SELECT *,
         MAX(IFF(stage_raw LIKE '%RUNOFF%',1,0)) OVER (PARTITION BY office,yr,st,district,special) has_ro,
         IFF(stage_raw LIKE '%RUNOFF%',1,0) is_ro
  FROM base
),
cand AS (   -- collapse fusion-ticket / multi-party rows: SUM votes per (race, candidate)
  SELECT office, yr, st, district, special, candidate,
         ANY_VALUE(party) party, SUM(cv) cv, MAX(tv) tv
  FROM decisive
  WHERE cv IS NOT NULL AND ((has_ro=1 AND is_ro=1) OR has_ro=0)
  GROUP BY office, yr, st, district, special, candidate
),
ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY office,yr,st,district,special ORDER BY cv DESC) rn,
         SUM(cv) OVER (PARTITION BY office,yr,st,district,special) race_total_cv
  FROM cand
),
race AS (
  SELECT w.office, w.yr, w.st, w.district, w.special,
         w.candidate winner, w.party winner_party, w.cv winner_votes, w.tv total_votes,
         ROUND(w.cv / NULLIFZERO(w.tv), 4) vote_share,
         r2.candidate runner_up, r2.party runner_up_party, r2.cv runner_up_votes,
         w.cv - COALESCE(r2.cv,0) margin_votes,
         ROUND((w.cv - COALESCE(r2.cv,0)) / NULLIFZERO(w.tv), 4) margin_pct
  FROM ranked w
  LEFT JOIN ranked r2 ON r2.office=w.office AND r2.yr=w.yr AND r2.st=w.st
       AND r2.district=w.district AND r2.special=w.special AND r2.rn=2
  WHERE w.rn=1
),
norm AS (   -- normalized winner surname tail for the ENDSWITH match
  SELECT race.*,
         REGEXP_REPLACE(UPPER(winner), '[ ,]+(JR|SR|II|III|IV|2ND|3RD)\\\\.?$', '') AS win_clean
  FROM race
),
matched AS (
  SELECT n.*,
         x.bioguide, x.full_name spine_name, x.icpsr,
         CASE WHEN n.office='PRESIDENT' THEN 'n/a (state-level office)'
              WHEN x.bioguide IS NULL THEN 'unmatched'
              ELSE 'surname+state+chamber+term-span' END match_method
  FROM norm n
  LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_CROSSWALK x
    ON n.office IN ('SENATE','HOUSE')
   AND x.last_state = n.st
   AND x.last_term_type = DECODE(n.office,'SENATE','sen','HOUSE','rep')
   AND (n.win_clean = UPPER(x.name_last) OR ENDSWITH(n.win_clean, ' '||UPPER(x.name_last)))
   AND TRY_TO_NUMBER(n.yr) BETWEEN YEAR(TRY_TO_DATE(x.first_term_start))-2
                               AND COALESCE(YEAR(TRY_TO_DATE(x.last_term_end)),2030)+1
  QUALIFY ROW_NUMBER() OVER (PARTITION BY office,yr,st,district,special
                             ORDER BY (bioguide IS NOT NULL) DESC, full_name) = 1
)
SELECT office, TRY_TO_NUMBER(yr) AS year, st AS state, district,
       (UPPER(special)='TRUE') AS is_special,
       winner, winner_party, winner_votes, total_votes, vote_share,
       margin_votes, margin_pct, runner_up, runner_up_party,
       bioguide, spine_name, icpsr, match_method
FROM matched
"""


def build_mart():
    conn = snow.connect(); cur = conn.cursor()
    try:
        cur.execute(MART_DDL); conn.commit()
        print(f"  built {MART}")

        def q1(sql):
            cur.execute(sql); return cur.fetchone()

        rows = q1(f"SELECT COUNT(*) FROM {MART}")[0]
        print(f"\nINTEGRITY:  rows (races)= {rows:,}")
        cur.execute(f"""SELECT office, MIN(year), MAX(year), COUNT(*) races,
                          SUM(IFF(bioguide IS NOT NULL,1,0)) matched,
                          ROUND(SUM(IFF(bioguide IS NOT NULL,1,0))/COUNT(*),3) match_rate
                        FROM {MART} GROUP BY 1 ORDER BY 1""")
        print("  office     yrs           races  matched  rate")
        for r in cur.fetchall():
            print(f"  {r[0]:<9} {r[1]}-{r[2]}   {r[3]:>6} {r[4]:>8}  {r[5]}")
        # match rate for the spine-relevant recent congressional cycles
        cur.execute(f"""SELECT office, COUNT(*) races, SUM(IFF(bioguide IS NOT NULL,1,0)) matched,
                          ROUND(SUM(IFF(bioguide IS NOT NULL,1,0))/COUNT(*),3) rate
                        FROM {MART} WHERE office IN ('SENATE','HOUSE') AND year>=2016 GROUP BY 1""")
        print("  -- congressional match rate, 2016+ (the spine-joinable era):")
        for r in cur.fetchall():
            print(f"     {r[0]:<7} {r[2]}/{r[1]} = {r[3]}")
        # dup-winner sanity (a race should have exactly one winner row)
        d = q1(f"SELECT COUNT(*) FROM (SELECT office,year,state,district,is_special FROM {MART} GROUP BY 1,2,3,4,5 HAVING COUNT(*)>1)")[0]
        print(f"  duplicate race keys (must be 0): {d}")
    finally:
        cur.close(); conn.close()


if __name__ == "__main__":
    if "--skip-fetch" not in sys.argv:
        fetch_and_land()
    build_mart()
    print("\nDONE. Referee: politics/loaders/smoke_who_won.py")
