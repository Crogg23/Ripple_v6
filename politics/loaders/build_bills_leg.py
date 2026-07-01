"""Phase 4 -- the BILLS leg: bills sponsored / cosponsored / enacted (the last clean leg).

Lands GovInfo BILLSTATUS (the official GPO bill-status XML) for the 118th + 119th
congresses, ALL bill types, then builds 3 additive marts in LIBRARY_MARTS.POLITICS:

  POLITICS__BILLS            (congress, bill_type, bill_number)            one row per bill
  POLITICS__BILL_COSPONSORS  (congress, bill_type, bill_number, bioguide) one row per cosponsorship
  POLITICS__MEMBER_BILL_RECORD (bioguide, congress)                       the stat group

Landing tables (UPPER(source_id), per the registry source_ids registered this phase):
  fed_govinfo_billstatus       -> FED_GOVINFO_BILLSTATUS        (one row per bill)
  fed_govinfo_bill_cosponsors  -> FED_GOVINFO_BILL_COSPONSORS   (one row per bill x cosponsor)

NEW PARSING PATTERN: BILLSTATUS is XML (not CSV/JSON like FEC/Voteview). We pull the
per-(congress, bill_type) bulk ZIP, each holding one XML file per bill, and parse with
xml.etree. The build_* loader scaffold + the shared land() helper are reused unchanged;
only the parse step is new.

DATA MODEL (confirmed live against 5,649 118th Senate bills before building):
  <billStatus><bill>
     <type>HR|S|HJRES|SJRES|HCONRES|SCONRES|HRES|SRES</type>  (UPPER)
     <number>, <congress>, <introducedDate>, <title>
     <sponsors><item><bioguideId>...                          (the sponsor)
     <cosponsors><item><bioguideId><isOriginalCosponsor>True|False
                       <sponsorshipDate><sponsorshipWithdrawnDate?>  (withdrawn date present ONLY if withdrawn)
     <actions><item><type>...    (GPO action taxonomy: IntroReferral/Committee/Calendars/
                                  Floor/President/ResolvingDifferences/BecameLaw/Veto/Discharge)
     <laws><item><type>Public Law</type><number>118-5</number>   (PRESENT ONLY when enacted)

STAT DEFINITIONS (objective counts; advanced_past_committee carries a documented rule):
  bills_sponsored             total measures sponsored (NEVER shown alone -- a raw count rewards spam).
  bills_sponsored_substantive law-eligible types HR/S/HJRES/SJRES (can become law).
  resolutions_sponsored       HRES/SRES/HCONRES/SCONRES (cannot become law -- never in the denominator).
  bills_enacted               sponsored bills with a <laws> element (became Public Law). Objective fact.
  enacted_rate                100 * bills_enacted / bills_sponsored_substantive
                              (LAW-ELIGIBLE denominator -- resolutions excluded; NULL if 0 substantive).
  advanced_past_committee     DOCUMENTED RULE: a sponsored law-eligible bill whose action history contains
                              ANY action type beyond the introduce-and-refer stage -- i.e. type in
                              {Committee, Calendars, Discharge, Floor, President, ResolvingDifferences,
                               Veto, BecameLaw}. Counts committee report/markup/hearing OR any later
                              floor/calendar/presidential/enactment action. (IntroReferral alone = died in
                              committee.) Slightly generous (includes hearings, not strictly reported-out)
                              -- stated plainly per the handoff's "document the rule" mandate.
  cosponsored_count           bills the member cosponsored, WITHDRAWN EXCLUDED (matches GovTrack /
                              congress.gov current behavior). Kept SEPARATE from sponsored (authoring != signing).

Usage:
  python politics/loaders/build_bills_leg.py              # fetch + land + build
  python politics/loaders/build_bills_leg.py --skip-fetch # rebuild marts only
"""
from __future__ import annotations
import io
import sys
import zipfile
import xml.etree.ElementTree as ET

import pandas as pd
import requests

from pathlib import Path as _RepoPath
_REPO = _RepoPath(__file__).resolve().parents[2]
sys.path.insert(0, str(_REPO / "library-onboarding"))
sys.path.insert(0, str(_REPO / "politics" / "loaders"))
import snow  # noqa: E402
from build_skeleton import land  # noqa: E402  (reuse the first-class land() helper)

BASE = "https://www.govinfo.gov/bulkdata/BILLSTATUS"
UA = {"User-Agent": "Mozilla/5.0 (Ripple Library onboarding; bills leg)"}
CONGRESSES = ["118", "119"]
# All 8 bill types. URL uses lowercase; the XML <type> is UPPER.
BILL_TYPES = ["hr", "s", "hjres", "sjres", "hconres", "sconres", "hres", "sres"]

BILL_COLS = ["CONGRESS", "BILL_TYPE", "BILL_NUMBER", "INTRODUCED_DATE", "TITLE",
             "SPONSOR_BIOGUIDE", "SPONSOR_NAME", "LAW_TYPE", "LAW_NUMBER",
             "ACTION_TYPES", "N_ACTIONS", "LATEST_ACTION_DATE", "LATEST_ACTION_TEXT", "N_COSPONSORS"]
COSP_COLS = ["CONGRESS", "BILL_TYPE", "BILL_NUMBER", "COSPONSOR_BIOGUIDE", "COSPONSOR_NAME",
             "COSPONSOR_PARTY", "COSPONSOR_STATE", "IS_ORIGINAL", "SPONSORSHIP_DATE",
             "SPONSORSHIP_WITHDRAWN_DATE"]


def _t(elem) -> str:
    """Text of an element, '' if missing/None."""
    return (elem.text or "").strip() if elem is not None else ""


def parse_bill(xml_bytes: bytes):
    """Parse one BILLSTATUS XML -> (bill_tuple, [cosponsor_tuples]). None on a non-bill doc."""
    root = ET.fromstring(xml_bytes)
    bill = root.find("bill") if root.tag != "bill" else root
    if bill is None:
        return None, []
    congress = _t(bill.find("congress"))
    btype = _t(bill.find("type")).upper()
    bnum = _t(bill.find("number"))

    # sponsor (first item; bioguide may be empty for by-request / committee sponsors)
    sp_bio = sp_name = ""
    sp = bill.find("sponsors")
    if sp is not None:
        item = sp.find("item")
        if item is not None:
            sp_bio = _t(item.find("bioguideId"))
            sp_name = _t(item.find("fullName"))

    # laws -> became-law signal (present ONLY when enacted)
    law_type = law_number = ""
    laws = bill.find("laws")
    if laws is not None:
        it = laws.find("item")
        if it is not None:
            law_type = _t(it.find("type"))
            law_number = _t(it.find("number"))

    # action types (distinct) + count + latest action
    types, n_actions = set(), 0
    ac = bill.find("actions")
    if ac is not None:
        for it in ac.findall("item"):
            n_actions += 1
            tt = _t(it.find("type"))
            if tt:
                types.add(tt)
    la = bill.find("latestAction")
    la_date = _t(la.find("actionDate")) if la is not None else ""
    la_text = _t(la.find("text")) if la is not None else ""

    # cosponsors -> child rows (count ALL incl. withdrawn for the raw n_cosponsors cross-check)
    cosp_rows = []
    cs = bill.find("cosponsors")
    if cs is not None:
        for it in cs.findall("item"):
            cosp_rows.append((
                congress, btype, bnum,
                _t(it.find("bioguideId")), _t(it.find("fullName")),
                _t(it.find("party")), _t(it.find("state")),
                _t(it.find("isOriginalCosponsor")),
                _t(it.find("sponsorshipDate")),
                _t(it.find("sponsorshipWithdrawnDate")),
            ))

    bill_tuple = (congress, btype, bnum, _t(bill.find("introducedDate")), _t(bill.find("title")),
                  sp_bio, sp_name, law_type, law_number,
                  "|".join(sorted(types)), str(n_actions), la_date, la_text, str(len(cosp_rows)))
    return bill_tuple, cosp_rows


def fetch_type(cc: str, bt: str):
    """Download + parse one (congress, bill_type) bulk ZIP. Returns (bill_tuples, cosp_tuples)."""
    url = f"{BASE}/{cc}/{bt}/BILLSTATUS-{cc}-{bt}.zip"
    r = requests.get(url, headers=UA, timeout=600)
    if r.status_code == 404:
        print(f"    {cc} {bt:<8} 404 (no measures of this type) -- skip")
        return [], []
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    names = [n for n in zf.namelist() if n.lower().endswith(".xml")]
    bills, cosps, bad = [], [], 0
    for n in names:
        try:
            bt_tuple, cr = parse_bill(zf.read(n))
            if bt_tuple is not None:
                bills.append(bt_tuple)
                cosps.extend(cr)
        except ET.ParseError:
            bad += 1
    note = f" ({bad} unparseable)" if bad else ""
    print(f"    {cc} {bt:<8} {len(names):>6} bills  {len(cosps):>8} cosponsorships{note}")
    return bills, cosps


def fetch_and_land():
    all_bills, all_cosps = [], []
    for cc in CONGRESSES:
        for bt in BILL_TYPES:
            b, c = fetch_type(cc, bt)
            all_bills.extend(b)
            all_cosps.extend(c)
    print(f"\n  TOTAL: {len(all_bills):,} bills  {len(all_cosps):,} cosponsorships")

    bills_df = pd.DataFrame(all_bills, columns=BILL_COLS, dtype=str)
    cosp_df = pd.DataFrame(all_cosps, columns=COSP_COLS, dtype=str)

    land(bills_df, "fed_govinfo_billstatus", f"{BASE}/",
         "GovInfo BILLSTATUS, 118th+119th, all bill types; one row = one bill.")
    land(cosp_df, "fed_govinfo_bill_cosponsors", f"{BASE}/",
         "GovInfo BILLSTATUS cosponsor extract, 118th+119th; one row = one (bill, cosponsor).")


# ---------------------------------------------------------------------------
# Marts (additive, POLITICS namespace). Bill grain preserved; cosponsors stay
# in their own table so the list never inflates the bills table.
# ---------------------------------------------------------------------------
# Action types that mean "got past the pure introduce-and-refer stage" (the documented
# advanced-past-committee rule). IntroReferral alone => died in committee.
_ADV = "('Committee','Calendars','Discharge','Floor','President','ResolvingDifferences','Veto','BecameLaw')"

DDL = [
("mart bills", f"""
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__BILLS AS
WITH base AS (
  SELECT
    TRY_TO_NUMBER(CONGRESS)               AS congress,
    UPPER(NULLIF(TRIM(BILL_TYPE),''))     AS bill_type,
    TRY_TO_NUMBER(BILL_NUMBER)            AS bill_number,
    NULLIF(TRIM(SPONSOR_BIOGUIDE),'')     AS sponsor_bioguide,
    NULLIF(TRIM(SPONSOR_NAME),'')         AS sponsor_name,
    NULLIF(TRIM(TITLE),'')                AS title,
    NULLIF(TRIM(LAW_TYPE),'')             AS law_type,
    NULLIF(TRIM(LAW_NUMBER),'')           AS law_number,
    SPLIT(NULLIF(TRIM(ACTION_TYPES),''), '|') AS action_types,
    TRY_TO_NUMBER(N_ACTIONS)              AS n_actions,
    TRY_TO_DATE(NULLIF(TRIM(INTRODUCED_DATE),'')) AS introduced_date,
    NULLIF(TRIM(LATEST_ACTION_DATE),'')   AS latest_action_date,
    NULLIF(TRIM(LATEST_ACTION_TEXT),'')   AS latest_action_text
  FROM LIBRARY_RAW.LANDING.FED_GOVINFO_BILLSTATUS
  WHERE TRY_TO_NUMBER(BILL_NUMBER) IS NOT NULL AND UPPER(NULLIF(TRIM(BILL_TYPE),'')) IS NOT NULL
  QUALIFY ROW_NUMBER() OVER (PARTITION BY congress, bill_type, bill_number
                             ORDER BY introduced_date NULLS LAST) = 1
),
-- DISTINCT cosponsors per bill, straight from the cosponsor landing. The raw BILLSTATUS
-- XML occasionally lists the SAME member twice as a cosponsor on a bill (a GovInfo quirk --
-- e.g. 118 HR 6116 lists 30 items / 27 distinct members), so we count DISTINCT bioguide here
-- to match POLITICS__BILL_COSPONSORS exactly (the landing N_COSPONSORS is the raw pre-dedup count).
cosp_n AS (
  SELECT TRY_TO_NUMBER(CONGRESS)           AS congress,
         UPPER(NULLIF(TRIM(BILL_TYPE),'')) AS bill_type,
         TRY_TO_NUMBER(BILL_NUMBER)        AS bill_number,
         COUNT(DISTINCT NULLIF(TRIM(COSPONSOR_BIOGUIDE),'')) AS n_cosponsors
  FROM LIBRARY_RAW.LANDING.FED_GOVINFO_BILL_COSPONSORS
  WHERE NULLIF(TRIM(COSPONSOR_BIOGUIDE),'') IS NOT NULL AND TRY_TO_NUMBER(BILL_NUMBER) IS NOT NULL
  GROUP BY 1, 2, 3
)
SELECT
  congress, bill_type, bill_number, sponsor_bioguide, sponsor_name, title,
  (bill_type IN ('HR','S','HJRES','SJRES'))                  AS is_law_eligible,
  CASE WHEN bill_type IN ('HR','S')          THEN 'bill'
       WHEN bill_type IN ('HJRES','SJRES')   THEN 'joint_resolution'
       WHEN bill_type IN ('HCONRES','SCONRES') THEN 'concurrent_resolution'
       WHEN bill_type IN ('HRES','SRES')     THEN 'simple_resolution'
       ELSE 'other' END                                       AS bill_class,
  (law_number IS NOT NULL)                                    AS became_law,
  law_number,
  -- advanced_past_committee: any action type beyond IntroReferral (documented rule)
  (ARRAY_SIZE(ARRAY_INTERSECTION(action_types,
     ARRAY_CONSTRUCT('Committee','Calendars','Discharge','Floor','President',
                     'ResolvingDifferences','Veto','BecameLaw'))) > 0)  AS advanced_past_committee,
  CASE
    WHEN law_number IS NOT NULL THEN 'became_law'
    WHEN ARRAY_CONTAINS('President'::variant, action_types)
      OR ARRAY_CONTAINS('Veto'::variant, action_types)
      OR ARRAY_CONTAINS('ResolvingDifferences'::variant, action_types) THEN 'passed_both_to_president'
    WHEN ARRAY_CONTAINS('Floor'::variant, action_types)            THEN 'reached_floor'
    WHEN ARRAY_CONTAINS('Calendars'::variant, action_types)
      OR ARRAY_CONTAINS('Discharge'::variant, action_types)
      OR ARRAY_CONTAINS('Committee'::variant, action_types)        THEN 'committee_action'
    WHEN ARRAY_CONTAINS('IntroReferral'::variant, action_types)    THEN 'introduced'
    ELSE 'unknown'
  END                                                         AS latest_stage,
  introduced_date, latest_action_date, latest_action_text,
  COALESCE(cn.n_cosponsors, 0)                                AS n_cosponsors,  -- DISTINCT cosponsors
  n_actions,
  (congress = 119)                                            AS congress_partial
FROM base
LEFT JOIN cosp_n cn USING (congress, bill_type, bill_number)
"""),

("mart bill_cosponsors", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS AS
SELECT
  TRY_TO_NUMBER(CONGRESS)               AS congress,
  UPPER(NULLIF(TRIM(BILL_TYPE),''))     AS bill_type,
  TRY_TO_NUMBER(BILL_NUMBER)            AS bill_number,
  NULLIF(TRIM(COSPONSOR_BIOGUIDE),'')   AS cosponsor_bioguide,
  NULLIF(TRIM(COSPONSOR_NAME),'')       AS cosponsor_name,
  NULLIF(TRIM(COSPONSOR_PARTY),'')      AS cosponsor_party,
  NULLIF(TRIM(COSPONSOR_STATE),'')      AS cosponsor_state,
  (UPPER(TRIM(IS_ORIGINAL)) = 'TRUE')   AS is_original,
  (NULLIF(TRIM(SPONSORSHIP_WITHDRAWN_DATE),'') IS NOT NULL) AS is_withdrawn,
  TRY_TO_DATE(NULLIF(TRIM(SPONSORSHIP_DATE),''))           AS sponsorship_date,
  TRY_TO_DATE(NULLIF(TRIM(SPONSORSHIP_WITHDRAWN_DATE),'')) AS sponsorship_withdrawn_date
FROM LIBRARY_RAW.LANDING.FED_GOVINFO_BILL_COSPONSORS
WHERE NULLIF(TRIM(COSPONSOR_BIOGUIDE),'') IS NOT NULL
  AND TRY_TO_NUMBER(BILL_NUMBER) IS NOT NULL
-- a member can withdraw then re-cosponsor: keep the row that is NOT withdrawn if any
QUALIFY ROW_NUMBER() OVER (PARTITION BY congress, bill_type, bill_number, cosponsor_bioguide
                           ORDER BY is_withdrawn ASC, sponsorship_date DESC NULLS LAST) = 1
"""),

("mart member_bill_record", """
CREATE OR REPLACE TABLE LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD AS
WITH spon AS (
  SELECT
    sponsor_bioguide                          AS bioguide,
    congress,
    COUNT(*)                                  AS bills_sponsored,
    SUM(IFF(is_law_eligible, 1, 0))           AS bills_sponsored_substantive,
    SUM(IFF(NOT is_law_eligible, 1, 0))       AS resolutions_sponsored,
    SUM(IFF(became_law, 1, 0))                AS bills_enacted,
    SUM(IFF(is_law_eligible AND advanced_past_committee, 1, 0)) AS advanced_past_committee_count
  FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS
  WHERE sponsor_bioguide IS NOT NULL
  GROUP BY 1, 2
),
cospon AS (
  SELECT
    cosponsor_bioguide                        AS bioguide,
    congress,
    COUNT(*)                                  AS cosponsored_count   -- withdrawn already excluded below
  FROM LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS
  WHERE NOT is_withdrawn AND cosponsor_bioguide IS NOT NULL
  GROUP BY 1, 2
),
keys AS (
  SELECT bioguide, congress FROM spon
  UNION
  SELECT bioguide, congress FROM cospon
)
SELECT
  k.bioguide,
  k.congress,
  s.full_name,
  s.party,
  s.state,
  s.last_term_type                            AS chamber,
  s.ideology_label,
  COALESCE(sp.bills_sponsored, 0)             AS bills_sponsored,
  COALESCE(sp.bills_sponsored_substantive, 0) AS bills_sponsored_substantive,
  COALESCE(sp.resolutions_sponsored, 0)       AS resolutions_sponsored,
  COALESCE(sp.bills_enacted, 0)               AS bills_enacted,
  ROUND(100.0 * sp.bills_enacted / NULLIF(sp.bills_sponsored_substantive, 0), 2) AS enacted_rate,
  COALESCE(sp.advanced_past_committee_count, 0) AS advanced_past_committee_count,
  ROUND(100.0 * sp.advanced_past_committee_count / NULLIF(sp.bills_sponsored_substantive, 0), 2) AS advanced_rate,
  COALESCE(cp.cosponsored_count, 0)           AS cosponsored_count,
  (k.congress = 119)                          AS congress_partial,
  (s.bioguide IS NOT NULL)                    AS has_spine_match
FROM keys k
LEFT JOIN spon   sp USING (bioguide, congress)
LEFT JOIN cospon cp USING (bioguide, congress)
LEFT JOIN LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_SPINE s ON s.bioguide = k.bioguide
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
            "bills_rows":            "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS",
            "bills_dupe_key":        "SELECT COUNT(*) FROM (SELECT congress,bill_type,bill_number FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS GROUP BY 1,2,3 HAVING COUNT(*)>1)",
            "bills_by_class":        "SELECT bill_class, COUNT(*), SUM(IFF(became_law,1,0)) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS GROUP BY 1 ORDER BY 2 DESC",
            "bills_law_eligible":    "SELECT is_law_eligible, COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS GROUP BY 1",
            "bills_enacted_by_cong": "SELECT congress, SUM(IFF(became_law,1,0)) enacted, SUM(IFF(is_law_eligible,1,0)) law_elig FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS GROUP BY 1 ORDER BY 1",
            "bills_stage_dist":      "SELECT latest_stage, COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS GROUP BY 1 ORDER BY 2 DESC",
            "cosp_rows":             "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS",
            "cosp_dupe_key":         "SELECT COUNT(*) FROM (SELECT congress,bill_type,bill_number,cosponsor_bioguide FROM LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS GROUP BY 1,2,3,4 HAVING COUNT(*)>1)",
            "cosp_withdrawn":        "SELECT is_withdrawn, COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS GROUP BY 1",
            # inflation cross-check: n_cosponsors on bills is now the DISTINCT cosponsor count, so
            # SUM(n_cosponsors) over POLITICS__BILLS must EQUAL POLITICS__BILL_COSPONSORS row count
            # (the raw landing has 7 more rows = a member double-listed as cosponsor on 7 bills; deduped here).
            "bills_sum_n_cosp":      "SELECT SUM(n_cosponsors) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS",
            "cosp_reconcile_zero":   "SELECT (SELECT SUM(n_cosponsors) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILLS) - (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS) AS should_be_zero",
            "landing_raw_vs_distinct": "SELECT (SELECT COUNT(*) FROM LIBRARY_RAW.LANDING.FED_GOVINFO_BILL_COSPONSORS) AS raw_rows, (SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__BILL_COSPONSORS) AS distinct_rows",
            "record_rows":           "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD",
            "record_members":        "SELECT COUNT(DISTINCT bioguide) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD",
            "record_dupe_key":       "SELECT COUNT(*) FROM (SELECT bioguide,congress FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD GROUP BY 1,2 HAVING COUNT(*)>1)",
            "record_no_spine":       "SELECT COUNT(*) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD WHERE NOT has_spine_match",
            "record_by_congress":    "SELECT congress, COUNT(*), ROUND(AVG(bills_sponsored),1), ROUND(AVG(enacted_rate),2), ROUND(AVG(cosponsored_count),1) FROM LIBRARY_MARTS.POLITICS.POLITICS__MEMBER_BILL_RECORD GROUP BY 1 ORDER BY 1",
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
        print("FETCH + LAND (BILLSTATUS XML, 118th+119th, all bill types):")
        fetch_and_land()
    print("\nBUILD MARTS:")
    build_models()
    print("\nDONE.")


if __name__ == "__main__":
    main(skip_fetch="--skip-fetch" in sys.argv)
