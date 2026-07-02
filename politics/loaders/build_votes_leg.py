"""Phase 3 -- the VOTES leg: votes cast / missed votes / party unity.

Lands the Voteview per-congress files for the 118th + 119th ONLY (NOT all 700MB of
history) and builds 3 additive marts in LIBRARY_MARTS.POLITICS:

  POLITICS__VOTEVIEW_VOTES       (congress, chamber, rollnumber, icpsr)  the cast matrix
  POLITICS__VOTEVIEW_ROLLCALLS   (congress, chamber, rollnumber)         roll-call metadata
  POLITICS__MEMBER_VOTING_RECORD (bioguide, congress)                    the stat group

Landing tables (per the existing registry source_ids):
  fed_voteview_rollcalls      -> FED_VOTEVIEW_ROLLCALLS       (the VOTES MATRIX; its URL=HSall_votes.csv)
  fed_voteview_rollcall_meta  -> FED_VOTEVIEW_ROLLCALL_META   (roll-call METADATA)

STAT DEFINITIONS (documented, definition-bound -- NOT penny-exact like FEC $):
  votes_eligible  = roll-calls where the member was in the chamber (cast_code <> 0).
                    Per-congress files are already member-scoped, so this is every row;
                    the cast_code<>0 filter is the mandated denominator guard.
  votes_cast      = recorded a position: yea/nay/present (cast_code 1-8).
  missed_votes    = cast_code = 9 (Not Voting / absent).
  missed_vote_pct = 100 * missed_votes / votes_eligible.
  party_unity     = on "party-unity roll-calls" (a majority of Democrats opposed a majority
                    of Republicans -- the standard CQ definition), the share of the member's
                    yea/nay votes that sided with their OWN party's majority. Computed only
                    for the two major parties (100=D, 200=R); independents excluded from the
                    party-unity stat (they still get votes/missed). DEFINITION-BOUND.

Cast codes confirmed live from H118_votes.csv: 1=Yea, 6=Nay, 9=Not Voting, 7=Present
(2/3 paired/announced yea, 4/5 paired/announced nay, 8 present, 0 not-a-member -- handled).

Usage:
  python politics/loaders/build_votes_leg.py              # fetch + land + build
  python politics/loaders/build_votes_leg.py --skip-fetch # rebuild marts only
"""
from __future__ import annotations
import io
import sys

import pandas as pd
import requests

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))
import snow  # noqa: E402
from build_skeleton import land  # noqa: E402

BASE = "https://voteview.com/static/data/out"
CONGRESSES = ["118", "119"]
CHAMBERS = ["H", "S"]


def fetch_csv(kind: str, ch: str, cc: str) -> pd.DataFrame:
    url = f"{BASE}/{kind}/{ch}{cc}_{kind}.csv"
    r = requests.get(url, timeout=300)
    r.raise_for_status()
    df = pd.read_csv(io.BytesIO(r.content), dtype=str, keep_default_na=False)
    df.columns = [c.upper() for c in df.columns]
    print(f"    {ch}{cc}_{kind}: {len(df):,} rows")
    return df


def fetch_and_land():
    # votes matrix -> fed_voteview_rollcalls -> FED_VOTEVIEW_ROLLCALLS
    votes = pd.concat([fetch_csv("votes", ch, cc) for cc in CONGRESSES for ch in CHAMBERS],
                      ignore_index=True)
    land(votes, "fed_voteview_rollcalls", f"{BASE}/votes/",
         "Voteview member-by-member votes matrix, 118th+119th congresses; one row = one member-rollcall.")
    # roll-call metadata -> fed_voteview_rollcall_meta -> FED_VOTEVIEW_ROLLCALL_META
    rolls = pd.concat([fetch_csv("rollcalls", ch, cc) for cc in CONGRESSES for ch in CHAMBERS],
                      ignore_index=True)
    land(rolls, "fed_voteview_rollcall_meta", f"{BASE}/rollcalls/",
         "Voteview roll-call metadata, 118th+119th congresses; one row = one roll-call.")


DDL = [
("mart voteview_votes", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES AS
SELECT
  TRY_TO_NUMBER(CONGRESS)   AS congress,
  CHAMBER                   AS chamber,
  TRY_TO_NUMBER(ROLLNUMBER) AS rollnumber,
  TRY_TO_NUMBER(ICPSR)      AS icpsr,
  TRY_TO_NUMBER(CAST_CODE)  AS cast_code,
  CASE
    WHEN TRY_TO_NUMBER(CAST_CODE) IN (1,2,3) THEN 'yea'
    WHEN TRY_TO_NUMBER(CAST_CODE) IN (4,5,6) THEN 'nay'
    WHEN TRY_TO_NUMBER(CAST_CODE) IN (7,8)   THEN 'present'
    WHEN TRY_TO_NUMBER(CAST_CODE) = 9        THEN 'not_voting'
    WHEN TRY_TO_NUMBER(CAST_CODE) = 0        THEN 'not_member'
    ELSE 'other'
  END                       AS vote_position,
  TRY_TO_DOUBLE(PROB)       AS prob
FROM LIBRARY_RAW.LANDING.FED_VOTEVIEW_ROLLCALLS
WHERE TRY_TO_NUMBER(ICPSR) IS NOT NULL AND TRY_TO_NUMBER(ROLLNUMBER) IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY congress, chamber, rollnumber, icpsr
                           ORDER BY prob DESC NULLS LAST) = 1
"""),

("mart voteview_rollcalls", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS AS
SELECT
  TRY_TO_NUMBER(CONGRESS)   AS congress,
  CHAMBER                   AS chamber,
  TRY_TO_NUMBER(ROLLNUMBER) AS rollnumber,
  TRY_TO_DATE(NULLIF(TRIM(DATE),'')) AS vote_date,
  TRY_TO_NUMBER(SESSION)    AS session,
  TRY_TO_NUMBER(YEA_COUNT)  AS yea_count,
  TRY_TO_NUMBER(NAY_COUNT)  AS nay_count,
  NULLIF(TRIM(VOTE_RESULT),'')   AS vote_result,
  NULLIF(TRIM(VOTE_QUESTION),'') AS vote_question,
  NULLIF(TRIM(BILL_NUMBER),'')   AS bill_number,
  NULLIF(TRIM(VOTE_DESC),'')     AS vote_desc
FROM LIBRARY_RAW.LANDING.FED_VOTEVIEW_ROLLCALL_META
WHERE TRY_TO_NUMBER(ROLLNUMBER) IS NOT NULL
QUALIFY ROW_NUMBER() OVER (PARTITION BY congress, chamber, rollnumber
                           ORDER BY vote_date NULLS LAST) = 1
"""),

("mart member_voting_record", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD AS
WITH v AS (
  SELECT * FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES WHERE cast_code <> 0
),
mem AS (  -- icpsr -> bioguide + party, from Voteview's OWN members file (same icpsr space = full coverage)
  SELECT TRY_TO_NUMBER(ICPSR) AS icpsr, TRY_TO_NUMBER(CONGRESS) AS congress, CHAMBER AS chamber,
         TRY_TO_NUMBER(PARTY_CODE) AS party_code, NULLIF(TRIM(BIOGUIDE_ID),'') AS bioguide,
         NULLIF(TRIM(BIONAME),'') AS bioname, NULLIF(TRIM(STATE_ABBREV),'') AS state
  FROM LIBRARY_RAW.LANDING.FED_VOTEVIEW_MEMBERS
  WHERE CONGRESS IN ('118','119') AND CHAMBER IN ('House','Senate')
  QUALIFY ROW_NUMBER() OVER (PARTITION BY icpsr, congress, chamber ORDER BY PARTY_CODE) = 1
),
-- eligibility counts straight from the matrix (no member join -> complete even if unmatched)
elig AS (
  SELECT icpsr, congress, chamber,
         COUNT(*)                                          AS votes_eligible,
         SUM(IFF(vote_position IN ('yea','nay','present'),1,0)) AS votes_cast,
         SUM(IFF(vote_position = 'not_voting',1,0))        AS missed_votes
  FROM v GROUP BY icpsr, congress, chamber
),
-- party majority per roll-call (major parties only)
party_maj AS (
  SELECT congress, chamber, rollnumber, m.party_code,
         CASE WHEN SUM(IFF(v.vote_position='yea',1,0)) > SUM(IFF(v.vote_position='nay',1,0)) THEN 'yea'
              WHEN SUM(IFF(v.vote_position='nay',1,0)) > SUM(IFF(v.vote_position='yea',1,0)) THEN 'nay'
              END AS maj
  FROM v JOIN mem m USING (icpsr, congress, chamber)
  WHERE m.party_code IN (100,200) AND v.vote_position IN ('yea','nay')
  GROUP BY congress, chamber, rollnumber, m.party_code
),
-- party-unity roll-calls: D majority opposes R majority
pu AS (
  SELECT d.congress, d.chamber, d.rollnumber, d.maj AS d_maj, r.maj AS r_maj
  FROM (SELECT * FROM party_maj WHERE party_code=100) d
  JOIN (SELECT * FROM party_maj WHERE party_code=200) r USING (congress, chamber, rollnumber)
  WHERE d.maj IS NOT NULL AND r.maj IS NOT NULL AND d.maj <> r.maj
),
member_pu AS (
  SELECT v.icpsr, v.congress, v.chamber,
         COUNT(*) AS party_unity_votes,
         SUM(IFF((m.party_code=100 AND v.vote_position=pu.d_maj)
              OR (m.party_code=200 AND v.vote_position=pu.r_maj),1,0)) AS party_unity_with
  FROM v
  JOIN mem m USING (icpsr, congress, chamber)
  JOIN pu  USING (congress, chamber, rollnumber)
  WHERE v.vote_position IN ('yea','nay') AND m.party_code IN (100,200)
  GROUP BY v.icpsr, v.congress, v.chamber
),
joined AS (
  SELECT e.icpsr, e.congress, e.chamber, e.votes_eligible, e.votes_cast, e.missed_votes,
         m.bioguide, m.bioname, m.state, m.party_code,
         mp.party_unity_votes, mp.party_unity_with
  FROM elig e
  LEFT JOIN mem m       USING (icpsr, congress, chamber)
  LEFT JOIN member_pu mp USING (icpsr, congress, chamber)
)
SELECT
  bioguide,
  congress,
  ANY_VALUE(chamber)                          AS chamber,
  ARRAY_AGG(DISTINCT icpsr) WITHIN GROUP (ORDER BY icpsr) AS icpsrs,
  ANY_VALUE(bioname)                          AS bioname,
  ANY_VALUE(state)                            AS state,
  CASE ANY_VALUE(party_code) WHEN 100 THEN 'Democrat' WHEN 200 THEN 'Republican'
       ELSE 'Other/Independent' END           AS party,
  SUM(votes_eligible)                         AS votes_eligible,
  SUM(votes_cast)                             AS votes_cast,
  SUM(missed_votes)                           AS missed_votes,
  ROUND(100.0 * SUM(missed_votes) / NULLIF(SUM(votes_eligible),0), 2) AS missed_vote_pct,
  SUM(party_unity_votes)                      AS party_unity_votes,
  SUM(party_unity_with)                       AS party_unity_with,
  ROUND(100.0 * SUM(party_unity_with) / NULLIF(SUM(party_unity_votes),0), 2) AS party_unity_pct,
  (congress = 119)                            AS congress_partial
FROM joined
WHERE bioguide IS NOT NULL
GROUP BY bioguide, congress
"""),
]


def build_models():
    conn = snow.connect()
    cur = conn.cursor()
    try:
        for label, sql in DDL:
            cur.execute(sql)
            print(f"  built {label}")
        conn.commit()
        checks = {
            "votes_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES",
            "votes_dupe_key": "SELECT COUNT(*) FROM (SELECT congress,chamber,rollnumber,icpsr FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES GROUP BY 1,2,3,4 HAVING COUNT(*)>1)",
            "votes_cast_dist": "SELECT vote_position, COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES GROUP BY 1 ORDER BY 2 DESC",
            "rollcalls_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS",
            "rollcalls_dupe_key": "SELECT COUNT(*) FROM (SELECT congress,chamber,rollnumber FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_ROLLCALLS GROUP BY 1,2,3 HAVING COUNT(*)>1)",
            "voting_record_rows": "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD",
            "voting_record_members": "SELECT COUNT(DISTINCT bioguide) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD",
            "voting_record_dupe_key": "SELECT COUNT(*) FROM (SELECT bioguide,congress FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD GROUP BY 1,2 HAVING COUNT(*)>1)",
            "by_congress": "SELECT congress, COUNT(*), ROUND(AVG(missed_vote_pct),2), ROUND(AVG(party_unity_pct),2) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_VOTING_RECORD GROUP BY 1 ORDER BY 1",
            "unmatched_icpsr_votes": "SELECT COUNT(*) FROM (SELECT DISTINCT v.icpsr, v.congress FROM LIBRARY_MARTS.POLITICS.POLITICS__VOTEVIEW_VOTES v LEFT JOIN LIBRARY_RAW.LANDING.FED_VOTEVIEW_MEMBERS m ON TRY_TO_NUMBER(m.ICPSR)=v.icpsr AND TRY_TO_NUMBER(m.CONGRESS)=v.congress AND m.CHAMBER=v.chamber WHERE m.ICPSR IS NULL)",
        }
        print("\nINTEGRITY:")
        for k, q in checks.items():
            cur.execute(q)
            print(f"  {k:<24} {cur.fetchall()}")
    finally:
        cur.close()
        conn.close()


def main(skip_fetch: bool):
    if not skip_fetch:
        print("FETCH + LAND (votes matrix + rollcall metadata, 118th+119th):")
        fetch_and_land()
    print("\nBUILD MARTS:")
    build_models()
    print("\nDONE.")


if __name__ == "__main__":
    main(skip_fetch="--skip-fetch" in sys.argv)
