"""The ledger: every table, pair, place, name and event in the marts, with a status.

One row per thing to check. Six layers, shaved from the bottom:
  singles  one table alone          what stands out inside it
  pairs    two tables on one ID     does it join, is there a gap
  hops     two tables, two IDs      linked through a crosswalk that carries both
  rollups  one ID, many tables      the same actor across every harm table, and harm against money
  place    one table rolled to geo  where is it worst, what moves with it
  names    one table with names     who is it, which ID table do they bridge to
  time     one table with an event  what happened after the event
  chains   three or more tables     grown by hand from live rows below
Plus findings: what was actually found, with a pointer back to the rows.

Reads outputs/catalog/er.json and plain.json. No warehouse calls.
Rebuilding keeps every status, note and finding already written.

  python scripts/ledger.py build              regenerate rows, keep statuses, write the page
  python scripts/ledger.py status             coverage per layer
  python scripts/ledger.py next pairs 20      the next 20 untouched rows, best first; 'all' ranks every layer
  python scripts/ledger.py next all 20 --tag MAP --claim agent1   reserve rows for one parallel agent
  python scripts/ledger.py release agent1 | release --stale 2   hand claimed rows back
  python scripts/ledger.py mark ID STATUS "note" [--finding F-001] [--by name]
  python scripts/ledger.py found LAYER TIER "headline" --rows ID,ID [--sql path] [--chart "decile staircase"]
  python scripts/ledger.py chain "A -> B -> C" "what to look for" [--from ID]
"""
import contextlib
import csv
import datetime as dt
import os
import time
import itertools
import json
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "ledger"
ER = ROOT / "outputs" / "catalog" / "er.json"
PLAIN = ROOT / "outputs" / "catalog" / "plain.json"

STATUSES = ["untouched", "claimed", "probed", "dead", "live", "finding", "skip"]
TRACK = ["status", "found", "finding_ids", "by", "date"]  # hand-kept columns, never regenerated

# ---------------------------------------------------------------- key families

ENTITY_KEYS = {
    "EIN": "nonprofit or company tax ID", "NPI": "doctor or clinic", "CCN": "Medicare facility",
    "CIK": "SEC company or person", "FRS_ID": "EPA facility", "BIOGUIDE": "member of Congress",
    "FEC_CMTE_ID": "campaign committee", "FEC_CAND_ID": "candidate", "UEI": "federal contractor",
    "DUNS": "company, old contractor ID", "LEI": "legal entity, global", "EIA_UTILITY_ID": "power utility",
    "EIA_PLANT_ID": "power plant", "NPDES_ID": "water discharge permit", "CL_PERSON_ID": "judge",
    "CL_COURT_ID": "court", "PWSID": "drinking water system", "PECOS_PAC_ID": "Medicare enrollee",
    "PECOS_ENRLMT_ID": "Medicare enrollment", "NCUA_CHARTER": "credit union", "IMO": "ship",
    "MMSI": "ship radio ID", "MINE_ID": "mine", "MSHA_CONTROLLER_ID": "mine owner",
    "MSHA_OPERATOR_ID": "mine operator", "FDIC_CERT": "bank", "RSSD": "bank, Fed ID",
    "CUSIP": "security", "COMPANY_NO": "UK company", "DEA_NO": "DEA registrant",
    "ICE_FACILITY": "detention facility", "AWARD_KEY": "federal award", "CAGE": "defense contractor",
    "NDC": "drug package", "PATENT": "patent", "FDA_510K_NO": "device clearance",
    "FDA_PMA_NO": "device approval", "ACCESSION": "SEC filing", "DOCKET": "case or rule docket",
}
CATEGORY_KEYS = {"SIC", "NAICS", "DRUG", "CFDA", "HCPCS", "ICPSR", "CAS"}  # group-by codes, not things
GEO_ORDER = ["TRACT_FIPS", "COUNTY_FIPS", "ZIP", "STATE_FIPS", "STATE", "LATLON", "GEOM", "COUNTRY"]
GEO_WORD = {"TRACT_FIPS": "census tract", "COUNTY_FIPS": "county", "ZIP": "ZIP code",
            "STATE_FIPS": "state", "STATE": "state", "LATLON": "map point", "GEOM": "map shape",
            "COUNTRY": "country"}

# Column words, matched on whole underscore-split tokens so SOLICITATION never reads as CITATION.
MONEY_STEMS = ("AMOUNT", "AMT", "PAYMENT", "PAID", "PENALT", "FINE", "COST", "DOLLAR", "OBLIG", "REVENUE",
               "SALAR", "COMPENS", "LOAN", "GRANT", "PRICE", "SPEND", "CHARGE", "DEPOSIT", "ASSET", "INCOME",
               "FEE", "CONTRIB", "RECEIPT", "DISBURS", "USD", "VALUE", "EXPEND", "FUNDING", "DEBT", "PROFIT", "SALES")
MONEY_TEXT_OK = ("AMOUNT", "AMT", "PAYMENT", "PENALT", "FINE", "COST", "SALAR", "COMPENS", "OBLIG", "DOLLAR")
HARM_STEMS = ("DEATH", "FATAL", "INJUR", "KILL", "OVERDOSE", "VIOLAT", "DEFICIEN", "RECALL", "ACCIDENT",
              "COMPLAINT", "CITATION", "ENFORCE", "SANCTION", "EXCLUSION", "DEBAR", "REVOK", "SUSPEN", "ARREST",
              "OFFENSE", "CRIME", "SHOOT", "ABUSE", "POLLUT", "SPILL", "EXPOSURE", "DENIAL", "DENIED",
              "FAILURE", "DISCIPLIN", "CONVICT", "MISCONDUCT", "HOMICIDE", "SUICIDE", "HAZARD")
PERSON_STEMS = ("FIRST", "LAST", "FULLNAME", "PERSON", "INDIVIDUAL", "DONOR", "CONTRIBUTOR", "PHYSICIAN",
                "PRESCRIBER", "OFFICER", "JUDGE", "SENATOR", "REPRESENTATIVE", "AUTHOR", "OWNER", "EMPLOYEE",
                "DEFENDANT", "INSIDER", "LOBBYIST", "DOCTOR", "PATIENT", "INMATE", "DECEDENT", "VICTIM")
OFFICIAL_STEMS = ("JUDGE", "JUDGES", "SENATOR", "SENATE", "HOUSE", "CONGRESS", "CONGRESSIONAL", "BIOGUIDE",
                  "LEGISLATOR", "LEGISLATIVE", "LOBBY", "LDA", "MEMBER", "MEMBERS", "COURTLISTENER")
EVENT_STEMS = ("EXCLUSION", "EXCLUDED", "DEBAR", "SANCTION", "ENFORCE", "PENALT", "VIOLAT", "RECALL", "RETRACT",
               "REVOK", "SUSPEN", "CLOSURE", "CLOSED", "FAIL", "DEATH", "ACCIDENT", "INSPECT", "CITATION",
               "BANKRUPT", "INDICT", "CONVICT", "TERMINAT", "WARNING", "LAWSUIT", "DISCIPLIN", "CHOW",
               "MERGER", "ACQUI", "DISCLOSURE", "TRADE", "TRADES", "COMPLAINT", "SHOOTING",
               "ARREST", "DETENTION", "DEPORT", "REMOVAL", "STRIKE", "LAYOFF", "WARN", "INCIDENT", "EVENT",
               "SEIZURE", "OUTAGE", "BREACH", "DISASTER", "EVICTION", "FORECLOS")
NOT_METRIC_TOKENS = {"ID", "CODE", "CD", "YEAR", "YR", "FIPS", "ZIP", "LAT", "LATITUDE", "LON", "LONG",
                     "LONGITUDE", "NO", "NUM", "NUMBER", "NBR", "KEY", "PHONE", "SEQ", "RANK", "MONTH",
                     "QUARTER", "QTR", "DAY", "VERSION", "FLAG", "COUNTRY", "CERT", "NPI", "EIN", "CIK", "UEI",
                     "DUNS", "FRS", "CCN", "INGESTED", "SOURCE", "RUN", "FY", "DATE", "SIC", "NAICS",
                     "IA", "UPLOAD", "RUCA", "RANGE", "BAND", "PRESIDENT", "TIER", "CLASS", "GRADE"}
EVENT_EXACT = {"ORDER", "ORDERS"}  # whole word only: ORDERING_PERIOD_END_DATE is not an order
# Which date says when the thing happened. Start-type words first, end-type words last.
DATE_FIRST = {"START", "ACTIVATION", "ACTIVE", "EFFECTIVE", "FILED", "FILING", "ISSUED", "ISSUE", "INCIDENT",
              "EVENT", "OCCUR", "OCCURRENCE", "VIOLATION", "ACCIDENT", "DEATH", "TRADE", "TRANSACTION", "EXCLUSION",
              "DEBARMENT", "SANCTION", "RECALL", "RETRACTION", "INSPECTION", "CITATION", "ORDER", "DECISION",
              "RECEIVED", "SIGNED", "ACTION", "INITIATION", "BEGIN", "OPEN", "OPENED"}
DATE_LAST = {"END", "TERMINATION", "TERMINATED", "EXPIRATION", "EXPIRY", "EXPIRES", "UPDATED", "UPDATE",
             "MODIFIED", "LAST", "CLOSED", "CLOSE", "DEACTIVATION", "TERM", "LOAD", "LOADED", "EXTRACT", "REFRESH"}
FEDERAL_MONEY = ("USASPENDING", "CONTRACT", "GRANT", "AWARD", "ASSISTANCE", "SBA", "PPP", "FPDS", "NIH", "SPENDING",
                 "PROCUREMENT", "SAM")
REFERENCE_SCHEMAS = {"CORE", "REFERENCE"}
NOT_MONEY_TOKENS = {"MEDIAN", "ACS", "CENSUS", "HOUSEHOLD", "RANGE", "BAND", "RATIO",  # neighborhood context, not money that moved
                    "NAME", "TYPE", "DESCRIPTION", "DESC", "STATE", "COUNTRY", "INDICATOR", "FORM", "NATURE",
                    "CATEGORY", "METHOD", "STATUS", "TEXT", "UNIT", "UNITS"}
# Harm text must be the harm itself, not a date part, record number or code for it.
NOT_HARM_TOKENS = {"MONTH", "DAY", "YEAR", "YR", "DATE", "NUMBER", "NO", "NBR", "NUM", "ID", "CODE", "CD", "KEY",
                   "CITY", "STATE", "COUNTY", "COUNTRY", "PLACE", "LOCATION"}
NOT_HARM_COLS = {"CITATION_COUNT"}  # court opinions citing each other, not a citation for a violation
DEMO_TOKENS = {"RACE", "ETHNICITY", "HISPANIC", "SEX", "GENDER", "AGE", "VETERAN", "DISABILITY", "CITIZENSHIP",
               "NATIONALITY", "LANGUAGE", "INCOME"}
OUTCOME_TOKENS = {"STATUS", "OUTCOME", "DISPOSITION", "DECISION", "RESULT", "RESOLUTION", "RESPONSE", "ACTION",
                  "VERDICT", "SENTENCE", "JUDGMENT", "RULING", "DENIAL"}
TEXT_TOKENS = {"NARRATIVE", "DESCRIPTION", "SUMMARY", "REMARKS", "COMMENT", "COMMENTS", "NOTES", "ABSTRACT",
               "SYNOPSIS", "COMPLAINT", "ALLEGATION", "ALLEGATIONS", "FINDINGS", "EXPLANATION", "PURPOSE"}
NOT_PERSON_TOKENS = {"OCCUPANCY", "AUTHORITY", "PLAN", "SYSTEM", "ORG", "BALANCING"}
# Record numbers identify a document, not an actor. Time rows built on them ask about timing, not repeat actors.
RECORD_KEYS = {"DOCKET", "ACCESSION", "AWARD_KEY", "PATENT", "FDA_510K_NO", "FDA_PMA_NO", "NDC", "CUSIP"}


def toks(c):
    return [t for t in re.split(r"[_\W]+", c.upper()) if t]


def has(c, stems):
    return any(t.startswith(stems) for t in toks(c))


def is_metric(c):
    return not c.startswith("_") and not (set(toks(c)) & NOT_METRIC_TOKENS)


# A key label is a word match. These guards keep pairs to one real ID system.
# Pairs that cross groups stay in the ledger, auto-marked skip with the reason.
KEY_GROUPS = {
    # Supreme Court numbers like 19-123 are national. District numbers repeat across courts, so they
    # only join with the court alongside. CourtListener DOCKET_IDs are its own row ids.
    "DOCKET": [("Supreme Court docket", ("OYEZ", "SCDB")),
               ("district docket number, needs the court too", ("FJC_IDB", "COURTLISTENER_DOCKETS",
                                                               "ORIGINATING_COURT_INFO")),
               ("CourtListener row id", ("COURTLISTENER",)),
               ("FDIC enforcement case", ("FDIC_ENFORCEMENT",)), ("bank charter", ("FDIC",)), ("FERC filing", ("EIA860",)),
               ("rulemaking", ("FEDERAL_REGISTER", "FDA_DEVICE_PMA"))],
    "CL_PERSON_ID": [("CourtListener judge", ("COURTLISTENER",))],
    "CL_COURT_ID": [("CourtListener court", ("COURTLISTENER",))],
}
BAD_LABELS = {("NPI", "NPI_DEACTIVATION_REASON_CODE")}
# A labeled key column that a known trap proves unusable. Its pairs stay, auto-skipped with the trap.
KEY_DEAD = {
    ("EIN", "HEALTH__FED_CMS_NPPES"): "NPPES EIN is an empty string on every row, trap nppes-ein-column-is-empty",
    ("EIN", "ECONOMICS__FED_US_USASPENDING_API"): "USASPENDING_API IDs are blank on all 300 rows, sweep 2026-09-24",
    ("UEI", "ECONOMICS__FED_US_USASPENDING_API"): "USASPENDING_API IDs are blank on all 300 rows, sweep 2026-09-24",
    ("DUNS", "ECONOMICS__FED_US_USASPENDING_API"): "USASPENDING_API IDs are blank on all 300 rows, sweep 2026-09-24",
    ("NPI", "HEALTH__SAM_EXCLUDED_PROVIDERS"): "its NPI is a name guess, cities disagree on all 24 top matches, trap guessed-and-circular-ids",
}
# A CCN's digits code the facility type, so a hospice CCN never matches a nursing-home one.
# Tables that hold one type are listed; mixed or unknown tables match anything.
CCN_FAMILY = [
    ("NURSING_HOME", "nursing home"), ("NURSINGHOME411", "nursing home"), ("SKILLED_NURSING", "nursing home"),
    ("MINIMUM_DATA_SET", "nursing home"), ("HOME_HEALTH", "home health"), ("HOSPICE", "hospice"),
    ("DIALYSIS", "dialysis"), ("FEDERALLY_QUALIFIED_HEALTH_CENTER", "health center"),
    ("RURAL_HEALTH_CLINIC", "rural clinic"), ("XWALK_HOSPITAL", "hospital"), ("HOSPITAL_CLOSURE", "hospital"),
    ("HOSPITAL_ENROLLMENTS", "hospital"), ("HOSPITAL_GENERAL", "hospital"), ("INPATIENT_HOSPITALS", "hospital"),
    ("OUTPATIENT_HOSPITALS", "hospital"), ("LTCH", "hospital"), ("OPEN_PAYMENTS", "hospital"),
]
# Tables loaded twice. Rows on the copy are auto-skipped; the original carries the work.
DUPLICATE_OF = {
    "HOUSING__FED_CFPB_HMDA_DC_ONLY": "HOUSING__FED_CFPB_HMDA",
    "POLITICS__FED_FJC_JUDGES": "JUSTICE__FED_FJC_ARTICLE_III_JUDGES",
    "ECONOMICS__FED_IRS_BMF": "CORPORATE_REGISTRY__FED_IRS_EO_BMF",
    "HEALTH__FED_CMS_MEDICARE_PROVIDER": "HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER",
    "POLITICS__BILL_COSPONSORS": "POLITICS__FED_GOVINFO_BILL_COSPONSORS",
}


def ccn_family(table):
    for frag, fam in CCN_FAMILY:
        if frag in table:
            return fam
    return None


def ccn_clash(k, a, b):
    """Both tables hold one known facility type each, and the types differ."""
    if k != "CCN":
        return ""
    fa, fb = ccn_family(a), ccn_family(b)
    return f"{fa} vs {fb}" if fa and fb and fa != fb else ""


# One labeled column in one table that is empty, while the table's other ID columns are fine.
BAD_COLS = {("ECONOMICS__FED_DOL_FORM5500", "EIN")}  # 100% empty; the employer is SPONS_DFE_EIN


def key_group(key, table):
    for label, frags in KEY_GROUPS.get(key, []):
        if any(f in table for f in frags):
            return label
    return None if key in KEY_GROUPS else "any"


# Known traps, by the table-name fragment they touch. Slugs match the memory folder.
TRAP_BY_FRAGMENT = [
    ("ATF", "atf-zips-lost-leading-zeros"),
    ("CDC_INJURY", "cdc-injury-count-sup-is-the-count"),
    ("CDC_INJURY", "cdc-injury-county-has-overdose-2019-2024"),
    ("DURABLE_MEDICAL_EQUIPMENT", "dme-referrer-columns-lie"), ("DURABLE_MEDICAL_EQUIPMENT", "bene-cc-pct-two-scales"),
    ("FACILITY_AFFILIATION", "facility-affiliation-underreports"),
    ("HMDA_HISTORIC", "hmda-historic-originations-only"),
    ("NPPES", "nppes-ein-column-is-empty"),
    ("NURSING_HOME", "nursing-home-chow-flag-constant"), ("NURSING_HOME", "owner-flag-columns-exist-but-empty"),
    ("EPA_TRI", "nursing-home-chow-flag-constant"), ("SKILLED_NURSING", "owner-flag-columns-exist-but-empty"),
    ("PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERV", "partb-service-table-is-suppressed-subset"),
    ("PARTD", "partd-is-dy2022"), ("PART_D", "partd-is-dy2022"),
    ("INSIDER_DERIV_TRANS", "sec-deriv-table-renames-everything"),
    ("FAERS", "three-tables-not-what-they-look-like"), ("EOIR", "three-tables-not-what-they-look-like"),
    ("NHTSA", "three-tables-not-what-they-look-like"), ("MSHA", "three-tables-not-what-they-look-like"),
    ("NPDB", "three-tables-not-what-they-look-like"),
    ("USASPENDING_ASSIST", "usaspending-assistance-1m-per-year-cap"),
    ("PECOS", "no-org-to-person-enrollment-bridge"), ("ENROLLMENTS", "no-org-to-person-enrollment-bridge"),
]
TRAP_BY_KEY = {"EIN": "ein-and-cik-width-mismatch", "CIK": "ein-and-cik-width-mismatch",
               "ZIP": "reach-is-not-a-usable-join"}
# Traps found by the 2026-09-23 hunt, not yet in memory. Plain text, shown on the row.
HUNT_TRAPS = {
    "JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES": "YEAR_COL junk under 2000 and over 2030; PERSON_ID null on 56%",
    "JUSTICE__FED_COURTLISTENER_DOCKETS": "DATE_FILED runs 1871 to 2079",
    "ENVIRONMENT__FED_EPA_GHGRP_EMISSION": "CO2E_EMISSION null on about a third of 2023 rows",
    "HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF": "ARID_2017 is agency code plus respondent id, zeros stripped",
    "ECONOMICS__FED_USASPENDING_CONTRACTS": "2024-2025 only; full history is _FULL_R2",
    "ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2": "93M rows, ACTION_DATE is text, 150 s per full scan",
    "POLITICS__SENATE_TRADES": "ends 2020-12",
    "FINANCE__FED_FEC_INDIV_CONTRIBUTIONS": "DONOR_NAME has a space after the comma; split then trim",
    # found by the 2026-09-24 sweep
    "HEALTH__FED_HRSA_NPDB": "TOTAL_PAYMENT is null on all 1.91M rows; dollars sit in PAYMENT_FLAG as '$' text",
    "LABOR__FED_OSHA_ITA_CASE_DETAIL_2024": "DATE_OF_DEATH is blank on every row; deaths are INCIDENT_OUTCOME = '1'",
    "HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS": "GROSS_INCOME is 0 or blank on all 26.25M rows",
    "JUSTICE__XC_WAPO_FATAL_FORCE": "MENTAL_ILLNESS_RELATED and BODY_CAMERA_PRESENT are 'false' on every row; at least 3 people entered twice",
    "HOUSING__FED_CFPB_HMDA_DC_ONLY": "a row-for-row copy of HOUSING__FED_CFPB_HMDA",
    "POLITICS__FED_FJC_JUDGES": "an older copy of JUSTICE__FED_FJC_ARTICLE_III_JUDGES",
    "HEALTH__FED_CMS_NURSING_HOME": "DATE_OF_MOST_RECENT_HEALTH_INSPECTION is null on all 14,700 rows",
    "ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK": "PARENT_UEI is the recipient's own UEI, name-matched from CONTRACTS_FULL; land rates against it are circular",
    "ECONOMICS__FED_DOL_FORM5500": "EIN and the asset totals are 100% empty; the employer is SPONS_DFE_EIN",
    "HEALTH__SAM_EXCLUDED_PROVIDERS": "not health providers; every row is already in SAM_EXCLUSIONS, NPI guessed by name",
    "ECONOMICS__FED_USASPENDING_CONTRACTS_FULL": "capped at 1M rows per FY, 43-120 days, mostly Jul-Sep; use _FULL_R2",
    "CORE__DIM_COUNTY": "Connecticut uses 2022 planning regions; old CT county codes match nothing",
    "DIM_COUNTY": "Connecticut uses 2022 planning regions; old CT county codes match nothing",
    # found by sweep two
    "HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE": "ALLOWED_CHARGES is the group's total on every clinician row, sums to $17.3T; use PARTICIPATION_OPTION = 'Individual'",
    "JUSTICE__FED_COURTLISTENER_DISCLOSURE_NON_INVESTMENT_INCOME": "INCOME_AMOUNT blank on 99.3% of rows",
    "POLITICS__FED_CONGRESS_LEGISLATORS": "N_TERMS is text, MAX gives 9 not 30; LEGISLATOR_SET blank on every row",
    "POLITICS__ST_NYC_CFB_CAMPAIGN_2001_CONTRIBUTION": "CONTRIBUTION_DATE null on every row",
    "HEALTH__FED_CMS_OPEN_PAYMENTS": "teaching-hospital rows carry NPI as an empty string; COALESCE on NPI makes one fake $0.7-1.1B recipient",
    "EDUCATION__FED_SENATE_LDA_FILINGS": "amendments repeat the original's total; sums double count",
    "FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS": "BRANCH_STATE_COUNTY_FIPS lost its leading zero in states 01-09; pad before joining",
    "JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS": "CMP_AMOUNT_TOTAL repeats within a docket; one penalty can read twice",
    "HEALTH__FED_HRSA_HPSA_PRIMARY_CARE": "70% of rows are withdrawn or proposed for withdrawal; filter status first",
    "HEALTH__FED_DEA_ARCOS": "VA mail-order pharmacies make Charleston SC and Leavenworth KS look like pill mills; 5 junk rows with codes 9143/9193 hold 2.14B units, keep code 'S'",
    "JUSTICE__COUNTY_DOUBLE_BURDEN": "JAIL_RATE_YEAR runs 1970-2024; pick a year",
    "ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS": "ACHIEVED_DATE runs 0001 to 8202; filter 1990 to today",
    "JUSTICE__FED_COURTLISTENER_FJC_IDB_CL_LINKED": "mostly 2010-19 cases, none after 2020; civil and criminal share docket numbers, filter DATASET_SOURCE",
    # found by sweep three
    "FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS": "EIN is the 527 group's own; 10,443 lump rows like 'Aggregate below threshold' hold $1.47B, drop them before ranking donors",
    "HEALTH__FED_FDA_FAERS_DEMO": "DEATH_DT blank on all 5.81M rows; country spelled 'UNITED STATES' and 'US'",
    "LABOR__FED_OSHA_ITA_300A_SUMMARY_2023": "ANNUAL_AVERAGE_EMPLOYEES has typos up to 172M; EINs typed by employers, USPS differs by year",
    "LABOR__FED_OSHA_ITA_300A_SUMMARY_2024": "ANNUAL_AVERAGE_EMPLOYEES has typos up to 172M; EINs typed by employers, USPS differs by year",
    "LABOR__FED_OSHA_ITA_CASE_DETAIL_2025": "a partial load: each month holds about half of 2024's cases",
    "HEALTH__HOSPITAL_OFFICER_PAY": "one person's TOTAL_COMPENSATION repeats on every related return; dedupe by person before summing",
    "HEALTH__FQHC_SITE_PEOPLE": "an address match against NPPES, not a staff list; a third of rows sit on 142 hospital campus sites",
    "HEALTH__FED_CMS_PARTD_PRESCRIBERS": "standing-order NPIs top vaccine counts, one ER doctor on 37,902 Shingrix patients; drop vaccines before ranking",
    "ENVIRONMENT__FED_EPA_ECHO": "TOTAL_PENALTIES repeats shared-case penalties per facility, reads 0 on 100,701 penalized sites, and national settlements sit on one HQ; formal-action counts cover recent years only",
    "JUSTICE__INTL_HUDOC": "JUDGMENT_DATE and JUDGMENT_YEAR blank on all 211,778 rows; each judgment stored in English and French",
    "HOUSING__FED_HUD_PUBLIC_HOUSING_AUTHORITIES": "statewide authorities booked to one county; CT uses old county codes, $97.7M lands nowhere",
    "TRANSPORT__FED_FRA_CASUALTIES": "DATE blank before 1997",
    "POLITICS__FED_GOVINFO_BILL_COSPONSORS": "Chip Roy listed as original cosponsor on 521 consecutive bills from HR1844, all withdrawn 2023-05-18; a clerk artifact",
}

# ---------------------------------------------------------------- io


def read_tsv(name):
    p = LEDGER / f"{name}.tsv"
    if not p.exists():
        return []
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(name, rows, cols):
    LEDGER.mkdir(exist_ok=True)
    with (LEDGER / f"{name}.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({c: ("" if r.get(c) is None else str(r.get(c)).replace("\t", " ").replace("\n", " ")) for c in cols})


def today():
    return dt.date.today().isoformat()

# ---------------------------------------------------------------- catalog read


def load_catalog():
    er = json.loads(ER.read_text(encoding="utf-8"))
    plain = json.loads(PLAIN.read_text(encoding="utf-8"))
    tables = {}
    for schema, name, rows, cols, grain in er["t"]:
        p = plain.get(name, {})
        t = dict(schema=schema, table=name, rows=rows or 0, grain=grain, cols=cols,
                 summary=p.get("summary", ""), row_is=p.get("row", ""))
        t["keys"] = defaultdict(list)
        for c, typ, label in cols:
            if label and (label, c) not in BAD_LABELS and (name, c) not in BAD_COLS:
                t["keys"][label].append(c)
        num = ("NUMBER", "FLOAT")
        isdate = lambda typ: typ.startswith(("DATE", "TIMESTAMP"))
        t["money"] = [c for c, typ, _ in cols if is_metric(c) and not isdate(typ) and
                      ((typ in num and has(c, MONEY_STEMS)) or (typ == "TEXT" and has(c, MONEY_TEXT_OK)))
                      and not set(toks(c)) & NOT_MONEY_TOKENS]
        t["harm"] = [c for c, typ, _ in cols if not isdate(typ) and has(c, HARM_STEMS) and not c.startswith("_")
                     and c not in NOT_HARM_COLS and not set(toks(c)) & NOT_HARM_TOKENS
                     and ((typ in num and is_metric(c)) or typ in ("TEXT", "BOOLEAN"))]
        t["person"] = [c for c, typ, lab in cols if typ == "TEXT" and has(c, PERSON_STEMS)
                       and (lab == "NAME" or "NAME" in toks(c)) and not set(toks(c)) & NOT_PERSON_TOKENS]
        t["dates"] = [c for c, typ, _ in cols if isdate(typ) and not c.startswith("_")]
        t["metrics"] = [c for c, typ, _ in cols if typ in num and is_metric(c) and not set(toks(c)) & DEMO_TOKENS]
        t["harm_num"] = [c for c, typ, _ in cols if c in t["harm"] and typ in num]
        t["flags"] = [c for c, typ, _ in cols if typ == "BOOLEAN" or c.startswith(("IS_", "HAS_")) or c.endswith("_FLAG")]
        t["entity"] = [k for k in t["keys"] if k in ENTITY_KEYS]
        t["geo"] = [k for k in GEO_ORDER if k in t["keys"]]
        t["names"] = t["keys"].get("NAME", [])
        t["address"] = t["keys"].get("ADDRESS", [])
        t["demo"] = [c for c, typ, _ in cols if not c.startswith("_") and set(toks(c)) & DEMO_TOKENS
                     and not set(toks(c)) & {"PCT", "PERCENT", "RATE", "ADJUSTED", "CNT", "COUNT", "TOT", "TOTAL",
                                             "NUM", "AVG", "MEAN"} and not isdate(typ)]
        t["outcome"] = [c for c, typ, _ in cols if typ == "TEXT" and set(toks(c)) & OUTCOME_TOKENS
                        and not set(toks(c)) & {"DATE", "ID", "NAME", "DESCRIPTION"}]
        t["text"] = [c for c, typ, _ in cols if typ == "TEXT" and set(toks(c)) & TEXT_TOKENS]
        tags = []
        if t["money"]:
            tags.append("MONEY")
        if t["harm"] or has(name, HARM_STEMS) or "EXCLUDED" in toks(name):
            tags.append("HARM")
        if t["person"] or {"NPI", "BIOGUIDE", "CL_PERSON_ID"} & set(t["entity"]):
            tags.append("PEOPLE")
        if has(name, OFFICIAL_STEMS) or {"BIOGUIDE", "CL_PERSON_ID"} & set(t["entity"]):
            tags.append("OFFICIALS")
        if t["geo"]:
            tags.append("MAP")
        if t["demo"]:
            tags.append("DEMOGRAPHIC")
        if t["outcome"]:
            tags.append("OUTCOME")
        if t["text"]:
            tags.append("TEXT")
        if not t["rows"]:
            tags.append("EMPTY")
        t["tags"] = tags
        traps = [slug for frag, slug in TRAP_BY_FRAGMENT if re.search(rf"(^|_){frag}(_|$)", name)]
        traps += [TRAP_BY_KEY[k] for k in t["keys"] if k in TRAP_BY_KEY]
        t["traps"] = sorted(set(traps))
        t["hunt_trap"] = HUNT_TRAPS.get(name, "")
        t["reference"] = schema in REFERENCE_SCHEMAS or name.startswith("DIM_")
        if t["reference"]:
            t["tags"].append("REFERENCE")
        t["derived"] = schema == "FINDINGS"  # a prior hunt's output, built from tables already in the ledger
        if t["derived"]:
            t["tags"].append("DERIVED")
        tables[name] = t
    return tables


def is_event_col(c):
    return has(c, EVENT_STEMS) or bool(set(toks(c)) & EVENT_EXACT)


def date_rank(c):
    tk = set(toks(c))
    return 2 if tk & DATE_LAST else 0 if tk & DATE_FIRST else 1


def score(tags, rows):
    """Sort order only. Never a filter: every row stays in the ledger."""
    w = {"MONEY": 3, "HARM": 3, "PEOPLE": 2, "OFFICIALS": 3, "MAP": 1, "DEMOGRAPHIC": 2, "OUTCOME": 1,
         "TEXT": 1, "EMPTY": -10}
    return round(sum(w.get(x, 0) for x in tags) + math.log10(max(rows, 1)) / 2, 1)


def short(cols, n=4):
    return ", ".join(cols[:n]) + (f" +{len(cols) - n}" if len(cols) > n else "")


def q(question, chart):
    """One thing to look for, and the chart that would show it. Stored as 'question :: chart'."""
    return f"{question} :: {chart}"


def pack(look):
    return " | ".join(look), " ".join(sorted({x.split(" :: ")[1].replace(" ", "_") for x in look if " :: " in x}))

# ---------------------------------------------------------------- layer builders


def build_singles(T):
    out = []
    for t in T.values():
        look = []
        m, h, d = t["money"], t["harm"], t["dates"]
        actors = [k for k in t["entity"] if k not in RECORD_KEYS]
        if m:
            look.append(q(f"who gets the most: top 20 by {m[0]}", "ranked bar"))
            look.append(q(f"concentration: what share of all {m[0]} goes to the top 1%", "share curve"))
            look.append(q(f"bunching: {m[0]} piling up just under round lines like $10K or $150K", "histogram"))
        if len(m) >= 2:
            look.append(q(f"the gap on one row: {m[0]} against {m[1]}; who pays or gets least of what's due", "scatter with a diagonal"))
        if h:
            look.append(q(f"worst actors: who racks up the most {h[0]}", "ranked bar"))
            if actors:
                look.append(q(f"repeat offenders: {actors[0]} values with three or more {h[0]} rows", "dot strip"))
        if t["metrics"]:
            look.append(q(f"outliers: rows over 10x the median {t['metrics'][0]} of their peers", "dot strip"))
        if t["demo"]:
            target = (h or m or t["outcome"] or ["row count"])[0]
            look.append(q(f"disparity: {target} by {', '.join(t['demo'][:2])}; the raw gap first, then the boring reason", "dot plot by group"))
        if t["outcome"]:
            look.append(q(f"outcomes: share of each {t['outcome'][0]} value by entity, place or year; who loses most", "stacked bars"))
        if d:
            look.append(q(f"trend: spikes and step changes by year in {d[0]}", "line over time"))
            fed = m and has(short_name(t), FEDERAL_MONEY) and not short_name(t).startswith("INTL_")
            look.append(q(f"rhythm: month of year and day of week in {d[0]}"
                          + ("; the September end-of-fiscal-year rush" if fed else ""), "calendar heatmap"))
            if actors:
                look.append(q(f"newcomers and vanishers: {actors[0]} values that appear from nowhere big, or drop out", "slope chart"))
        if actors and not m:
            look.append(q(f"concentration: does a handful of {actors[0]} values hold most rows; name them", "share curve"))
        if t["flags"]:
            look.append(q(f"flag rates by group: {t['flags'][0]}; count its values first", "grouped bars"))
        if t["text"]:
            look.append(q(f"read the words: search {t['text'][0]} for named products, firms or phrases", "word bars"))
        if t["geo"]:
            lvl = t["geo"][0]
            look.append(q(f"where: rank by {GEO_WORD[lvl]}", "point map" if lvl in ("LATLON", "GEOM") else "choropleth map"))
        if not look:
            look.append(q("read 20 rows and the plain summary; decide if it has a number worth ranking", "table"))
        where = []
        for lab, cols in (("money", m), ("harm", h), ("metrics", t["metrics"]), ("dates", d), ("flags", t["flags"]),
                          ("people", t["person"]), ("groups", t["demo"]), ("outcomes", t["outcome"]), ("text", t["text"])):
            if cols:
                where.append(f"{lab}: {short(cols)}")
        lf, charts = pack(look)
        out.append(dict(
            id=f"S:{t['table']}", schema=t["schema"], table=t["table"], rows=t["rows"],
            tags=" ".join(t["tags"]), score=score(t["tags"], t["rows"]), summary=t["summary"],
            look_for=lf, charts=charts, where="; ".join(where),
            keys=", ".join(sorted(t["entity"])), traps=" ".join(t["traps"]), hunt_trap=t["hunt_trap"]))
    return out


def family(name):
    """Tables from one source family, like OPEN_PAYMENTS and OPEN_PAYMENTS_2022, share a family."""
    base = name.split("__", 1)[-1]
    return re.sub(r"(_FULL|_R\d|_\d{4}|_HISTORIC|_DIM|_DETAIL|_SUMMARY)+$", "", base)


def siblings(a, b):
    fa, fb = family(a["table"]), family(b["table"])
    return fa == fb or fa.startswith(fb) or fb.startswith(fa)


def gap_one(t):
    """The number to compare for matched vs unmatched. Text harm becomes a rate, never an average."""
    m = t["money"] or t["harm_num"] or t["metrics"]
    if m:
        return q(f"gap: {m[0]} in {short_name(t)} for matched vs unmatched", "paired bars")
    if t["harm"]:
        return q(f"gap: share of {short_name(t)} rows with a {t['harm'][0]}, matched vs unmatched", "paired bars")
    return None


def gap_looks(a, b):
    look = [x for x in (gap_one(a), gap_one(b)) if x]
    if a["money"] and b["money"]:
        look.append(q(f"big on both sides: {a['money'][0]} against {b['money'][0]}, one dot per match", "scatter"))
    ea = is_event_col(short_name(a)) and a["dates"]
    eb = is_event_col(short_name(b)) and b["dates"]
    if ea or eb:
        ev, other = (a, b) if ea else (b, a)
        dcol = min(ev["dates"], key=lambda c: (date_rank(c), ev["dates"].index(c)))
        look.append(q(f"after: does {short_name(other)} keep going after {dcol} in {short_name(ev)}", "before-after line"))
    return look


def pair_tags(a, b):
    tags = sorted((set(a["tags"]) | set(b["tags"])) - {"MAP", "EMPTY", "TEXT", "DEMOGRAPHIC", "OUTCOME"})
    if "EMPTY" in a["tags"] or "EMPTY" in b["tags"]:
        tags.append("EMPTY")
    if a["schema"] != b["schema"]:
        tags.append("CROSS")
    return tags


def build_pairs(T):
    by_key = defaultdict(list)
    for t in T.values():
        for k in t["entity"]:
            by_key[k].append(t)
    out = []
    for k, ts in by_key.items():
        for a, b in itertools.combinations(sorted(ts, key=lambda x: x["table"]), 2):
            cross = a["schema"] != b["schema"]
            sib = siblings(a, b)
            tags = pair_tags(a, b)
            look = [q(f"land rate: how many {k} values, each a {ENTITY_KEYS[k]}, sit on both sides; check a name or state agrees", "overlap bar")]
            if sib:
                tags.append("SIBLING")
                look.append(q("same source, another year or cut: who is new, who left, who grew most", "slope chart"))
            look += gap_looks(a, b)
            ga, gb = key_group(k, a["table"]), key_group(k, b["table"])
            auto = KEY_DEAD.get((k, a["table"])) or KEY_DEAD.get((k, b["table"])) or ""
            clash = ccn_clash(k, a["table"], b["table"])
            if auto:
                auto = f"auto-skip at build: {auto}"
                tags.append("TRAP")
            elif clash:
                auto = f"auto-skip at build: a CCN's digits code the facility type, {clash} never match"
                tags.append("MISMATCH")
            elif ga != gb or ga is None:
                auto = (f"auto-skip at build: the {k} label means {ga or 'something unchecked'} on one side "
                        f"and {gb or 'something unchecked'} on the other; label fired on a word")
                tags.append("MISMATCH")
            if ga and ga.startswith("district"):
                look[0] = q("land rate: join on court plus docket number, never the number alone; district numbers repeat", "overlap bar")
            s = score(tags, min(a["rows"], b["rows"])) + (2 if cross else 0) - (1 if sib else 0) - (20 if auto else 0)
            s -= 3 if k in RECORD_KEYS else 0  # a shared record number is plumbing until it proves otherwise
            lf, charts = pack(look)
            out.append(dict(
                id=f"P:{k}:{a['table']}~{b['table']}", key=k, key_is=ENTITY_KEYS[k],
                a=a["table"], b=b["table"], a_schema=a["schema"], b_schema=b["schema"],
                a_col=", ".join(a["keys"][k]), b_col=", ".join(b["keys"][k]),
                a_rows=a["rows"], b_rows=b["rows"], tags=" ".join(tags), score=round(s, 1),
                look_for=lf, charts=charts, auto_skip=auto,
                traps=" ".join(sorted(set(a["traps"]) | set(b["traps"])))))
    return out


def actors_of(t):
    return sorted({k for k in t["entity"] if k not in RECORD_KEYS})


def usable(k, t, other):
    """Can table t's k column meet other's k column? Same ID system, and no trap says it's empty."""
    g1, g2 = key_group(k, t["table"]), key_group(k, other["table"])
    return (g1 is not None and g1 == g2 and (k, t["table"]) not in KEY_DEAD and (k, other["table"]) not in KEY_DEAD
            and not ccn_clash(k, t["table"], other["table"]))


def build_hops(T, pairs):
    """A and C share no usable ID, but a crosswalk table B carries both of theirs: A -k1- B -k2- C.
    One row per A and C, with every route listed. Where A and C already join directly, the pair row covers it."""
    direct = set()
    for p in pairs:
        if not p.get("auto_skip"):
            direct |= {(p["a"], p["b"]), (p["b"], p["a"])}
    by_key = defaultdict(set)
    for t in T.values():
        for k in actors_of(t):
            by_key[k].add(t["table"])
    routes = defaultdict(lambda: defaultdict(lambda: {"ok": set(), "all": set()}))
    for b in T.values():
        ks = actors_of(b)
        if len(ks) < 2:
            continue
        for k1, k2 in itertools.permutations(ks, 2):
            for an in by_key[k1]:
                a = T[an]
                if an == b["table"] or k2 in actors_of(a):
                    continue
                for cn in by_key[k2]:
                    c = T[cn]
                    if cn in (an, b["table"]) or k1 in actors_of(c):
                        continue
                    (x, kx), (y, ky) = sorted([(an, k1), (cn, k2)])
                    h = routes[(x, y)][(kx, ky)]
                    h["all"].add(b["table"])
                    if usable(k1, a, b) and usable(k2, c, b):
                        h["ok"].add(b["table"])
    out, covered = [], 0
    for (an, cn), rs in routes.items():
        if (an, cn) in direct:
            covered += 1
            continue
        a, c = T[an], T[cn]
        ok = [(k, v["ok"]) for k, v in rs.items() if v["ok"]]
        use = ok or [(k, v["all"]) for k, v in rs.items()]
        use.sort(key=lambda kv: (-max(T[x]["rows"] for x in kv[1]), kv[0]))
        (k1, k2), via = use[0]
        route_txt = "; ".join(f"{ka} to {kc} via {short([short_name(T[x]) for x in sorted(v, key=lambda x: -T[x]['rows'])], 2)}"
                              for (ka, kc), v in use)
        tags = pair_tags(a, c) + ["HOP"]
        look = [q(f"does it land: share of {short_name(a)} {k1} values that reach a {k2} through the crosswalk, "
                  f"and on to {short_name(c)}", "flow diagram")]
        look += gap_looks(a, c)
        auto = ""
        if not ok:
            auto = ("auto-skip at build: every crosswalk here is unusable, a known-empty key or a label "
                    "that means different things on each side")
            tags.append("TRAP")
        s = score(tags, min(a["rows"], c["rows"])) + (2 if a["schema"] != c["schema"] else 0) - 1 - (20 if auto else 0)
        lf, charts = pack(look)
        out.append(dict(
            id=f"H:{an}~{cn}", a=an, a_key=k1, c=cn, c_key=k2, a_schema=a["schema"], c_schema=c["schema"],
            a_rows=a["rows"], c_rows=c["rows"], via=route_txt, via_count=len(use),
            tags=" ".join(tags), score=round(s, 1), look_for=lf, charts=charts, auto_skip=auto,
            traps=" ".join(sorted(set(a["traps"]) | set(c["traps"])))))
    CUTS["hops_covered_by_pairs"] = covered
    return out


def source_of(t):
    """INTL_UK_SANCTIONS and XC_UK_SANCTIONS are one list loaded twice. Strip the loader prefix and year."""
    return re.sub(r"^(FED_|INTL_|XC_|US_)+", "", family(t["table"]))


def one_per_source(ts):
    best = {}
    for t in sorted(ts, key=lambda t: -t["rows"]):
        best.setdefault(source_of(t), t)
    return sorted(best.values(), key=lambda t: -t["rows"])


def build_rollups(T):
    """One row per ID: the same doctor, firm or facility across every harm table, and harm against money."""
    out = []
    for k in sorted(ENTITY_KEYS):
        if k in RECORD_KEYS:
            continue
        ts = [t for t in T.values() if k in actors_of(t) and (k, t["table"]) not in KEY_DEAD
              and key_group(k, t["table"]) is not None and not t["reference"] and not t["derived"]
              and t["table"] not in DUPLICATE_OF]
        harm = one_per_source([t for t in ts if "HARM" in t["tags"]])
        money = one_per_source([t for t in ts if "MONEY" in t["tags"] and "HARM" not in t["tags"]])
        rows = []
        if len(harm) >= 2:
            rows.append(("worst", f"worst lists: the same {k} across its {len(harm)} harm tables", [
                q(f"count each {k} across {len(harm)} harm tables; who shows up in three or more", "ranked bar"),
                q("which harm tables overlap most, and on whom", "overlap matrix"),
                q("the top ten repeat names: walk each one across the tables", "timeline")]))
        if harm and money:
            rows.append(("harm-money", f"harm meets money: {k} on {len(harm)} harm and {len(money)} money tables", [
                q(f"{k} values on any harm table that also draw money from the {len(money)} money tables", "paired bars"),
                q("dollars to flagged vs unflagged, by year", "line over time"),
                q("the biggest earners among the flagged: name them", "ranked bar")]))
        for kind, label, look in rows:
            both = harm + (money if kind == "harm-money" else [])
            tags = sorted({"HARM", "MONEY"} if kind == "harm-money" else {"HARM"}) + ["ROLLUP"]
            if len({t["schema"] for t in both}) > 1:
                tags.append("CROSS")
            if {"PEOPLE"} & {x for t in both for x in t["tags"]}:
                tags.append("PEOPLE")
            lf, charts = pack(look)
            out.append(dict(
                id=f"R:{k}:{kind}", key=k, key_is=ENTITY_KEYS[k], kind=label, n_harm=len(harm), n_money=len(money),
                harm_tables=short([short_name(t) for t in harm], 8),
                money_tables=short([short_name(t) for t in money], 8) if kind == "harm-money" else "",
                tags=" ".join(tags), score=round(score(tags, 10 ** 6) + min(len(both), 12) / 2, 1),
                look_for=lf, charts=charts,
                traps=" ".join(sorted({x for t in both for x in t["traps"]}))))
    return out


CUTS = {}


def short_name(t):
    return t["table"].split("__", 1)[-1]


def place_metric(t):
    """Numbers first. A text harm column still counts: it rolls up as a count of rows."""
    num = t["money"] + t["harm_num"] + [c for c in t["metrics"] if c not in t["money"] + t["harm_num"]]
    return num + [f"rows with {c}" for c in t["harm"] if c not in t["harm_num"]]


def build_place(T):
    out = []
    for t in T.values():
        if not t["geo"]:
            continue
        lvl = t["geo"][0]
        m = place_metric(t)
        per = " per person, using CORE.DIM_COUNTY population" if lvl == "COUNTY_FIPS" else " per person"
        mapchart = {"LATLON": "point map", "GEOM": "point map", "COUNTRY": "world map"}.get(lvl, "choropleth map")
        look = [q(f"rank every {GEO_WORD[lvl]} by {m[0] if m else 'row count'}{per}", mapchart)]
        if lvl in ("LATLON", "GEOM"):
            look.append(q("clusters: where the points bunch; then what they sit near, see the proximity rows", "point map"))
        elif lvl == "COUNTRY":
            look.append(q("offshore and sanctions hot spots: which countries carry the money or the harm", "world map"))
        else:
            look.append(q(f"correlate against every other {GEO_WORD[lvl]} number; see the county panel rows", "scatter"))
        if t["dates"]:
            look.append(q(f"which places moved most over {t['dates'][0]}", "slope chart"))
        look.append(q("top and bottom tenth: name them, then name the boring reason", "decile staircase"))
        lf, charts = pack(look)
        out.append(dict(
            id=f"G:{t['table']}", schema=t["schema"], table=t["table"], rows=t["rows"],
            level=GEO_WORD[lvl], geo_col=", ".join(t["keys"][lvl]), all_levels=", ".join(GEO_WORD[g] for g in t["geo"]),
            metrics=short(m, 6) if m else "row count only", tags=" ".join(t["tags"]),
            score=score(t["tags"], t["rows"]) + (2 if lvl in ("COUNTY_FIPS", "TRACT_FIPS") else 0),
            look_for=lf, charts=charts, traps=" ".join(t["traps"]), hunt_trap=t["hunt_trap"]))
    # Panel rows: two county tables side by side is how pills met deaths. Two point tables is how a plant meets a school.
    for lvl, kind in (("COUNTY_FIPS", "county"), ("LATLON", "near")):
        ts = sorted([t for t in T.values() if lvl in t["keys"]], key=lambda x: x["table"])
        for a, b in itertools.combinations(ts, 2):
            tags = pair_tags(a, b) + ["PANEL"]
            ref = a if a["reference"] else b if b["reference"] else None
            if kind == "county":
                ma, mb = (place_metric(a) or ["row count"])[0], (place_metric(b) or ["row count"])[0]
                look = [q(f"roll both to county: {ma} against {mb}, per person", "scatter"),
                        q(f"top tenth of counties by {ma}: where do they sit on {mb}", "decile staircase"),
                        q("counties high on both: name them, then the boring reason", "two-color map")]
            else:
                look = [q(f"what sits near what: {short_name(a)} points within a mile of {short_name(b)} points", "point map"),
                        q("count of near neighbors per point; the ones with the most", "ranked bar")]
            lf, charts = pack(look)
            s = score(tags, min(a["rows"], b["rows"])) + (2 if a["schema"] != b["schema"] else 0) - (0 if kind == "county" else 2)
            auto = ""
            if ref:
                auto = (f"auto-skip at build: {short_name(ref)} is a reference or sample table; "
                        "divide by it or read it, don't pair it")
                tags.append("REFERENCE")
                s -= 20
            elif siblings(a, b):
                auto = "auto-skip at build: the same source twice; its year-over-year lives in the pair and single rows"
                tags.append("SIBLING")
                s -= 20
            out.append(dict(
                id=f"G2:{kind}:{a['table']}~{b['table']}", schema=f"{a['schema']} ↔ {b['schema']}",
                table=f"{short_name(a)} ↔ {short_name(b)}", a=a["table"], b=b["table"], rows=min(a["rows"], b["rows"]),
                level="county pair" if kind == "county" else "proximity pair",
                geo_col=f"{', '.join(a['keys'][lvl])} / {', '.join(b['keys'][lvl])}", all_levels="",
                metrics=f"{short(place_metric(a), 2)} / {short(place_metric(b), 2)}", tags=" ".join(tags),
                score=round(s, 1), look_for=lf, charts=charts, auto_skip=auto,
                traps=" ".join(sorted(set(a["traps"]) | set(b["traps"]))), hunt_trap=""))
    return out


def build_names(T):
    idx = [t for t in T.values() if t["names"] and actors_of(t)]
    out = []
    for t in T.values():
        if not t["names"] and not t["address"]:
            continue
        kind = "people" if t["person"] else "organizations"
        has_state = "STATE" in t["keys"]
        look = []
        if t["names"]:
            look.append(q(f"who repeats: the {kind} named most often, and how many rows each", "ranked bar"))
            if actors_of(t):
                look.append(q(f"already has an ID ({', '.join(actors_of(t))}); use it, names only to check the join", "table"))
            else:
                look.append(q(f"no ID: bridge to an ID table of {kind} on name{' + state' if has_state else ''}, two words minimum", "overlap bar"))
                look.append(q("report the agreement rate on a second field before trusting any match", "table"))
            look.append(q("the web: one name across many tables, and who sits next to whom", "network"))
        if t["address"]:
            look.append(q(f"shared addresses: many different names or IDs at one {t['address'][0]}, like a P.O. box", "ranked bar"))
            look.append(q("same address in another table: match on street plus ZIP, never street alone", "network"))
        same = [x for x in idx if x["table"] != t["table"] and bool(x["person"]) == bool(t["person"])]
        same.sort(key=lambda x: (x["schema"] != t["schema"], "STATE" not in x["keys"], -x["rows"], x["table"]))
        lf, charts = pack(look)
        out.append(dict(
            id=f"N:{t['table']}", schema=t["schema"], table=t["table"], rows=t["rows"],
            name_cols=short(t["names"] + t["address"], 5), kind=kind, has_id="yes" if actors_of(t) else "no",
            has_state="yes" if has_state else "no",
            bridge_to="" if actors_of(t) else short([short_name(x) for x in same], 5),
            tags=" ".join(t["tags"]), score=score(t["tags"], t["rows"]) + (1 if not actors_of(t) else 0),
            look_for=lf, charts=charts,
            traps=" ".join(sorted(set(t["traps"]) | {"crosstable-single-word-name-collision"})), hunt_trap=t["hunt_trap"]))
    return out


def build_time(T, pairs):
    partners = defaultdict(set)
    for p in pairs:
        if not p.get("auto_skip"):
            partners[p["a"]].add(p["b"])
            partners[p["b"]].add(p["a"])
    out = []
    for t in T.values():
        ev_cols = [c for c in t["dates"] if is_event_col(c)]
        if not t["dates"] or not (is_event_col(short_name(t)) or ev_cols):
            continue
        # Every date competes: when it happened beats when it ended, and an event-named date wins a tie.
        pool = t["dates"]
        dcol = min(pool, key=lambda c: (date_rank(c), c not in ev_cols, pool.index(c)))
        actors = actors_of(t)
        if actors:
            who = ", ".join(actors)
            look = [q(f"after {dcol}: does the same {who} keep getting money, licenses or contracts elsewhere", "before-after line"),
                    q(f"before {dcol}: what did that {who} look like the year before; any warning sign", "before-after line"),
                    q(f"lag: days from {dcol} to the next event for the same {who}", "histogram")]
        elif t["names"]:
            who = "names only"
            look = [q(f"after {dcol}: do the named {', '.join(t['names'][:2])} show up again in money tables", "before-after line"),
                    q("bridge the names to an ID table first; see the names layer", "table")]
        else:
            who = "no actor column"
            look = [q(f"timeline: count by month in {dcol}; find the spikes and what sits under them", "line over time")]
        look.append(q(f"clusters: many events on one day or in one place in {dcol}", "timeline"))
        pt = sorted(partners[t["table"]], key=lambda x: (-T[x]["rows"], x))
        lf, charts = pack(look)
        out.append(dict(
            id=f"T:{t['table']}", schema=t["schema"], table=t["table"], rows=t["rows"],
            event_date=dcol, entity=who, partners=len(pt), partner_tables=short([short_name(T[x]) for x in pt], 5),
            tags=" ".join(t["tags"]), score=score(t["tags"], t["rows"]) + min(len(pt), 10) / 5,
            look_for=lf, charts=charts, traps=" ".join(t["traps"]), hunt_trap=t["hunt_trap"]))
    return out


COLS = {
    "singles": ["id", "status", "score", "schema", "table", "rows", "tags", "summary", "look_for", "charts", "where",
                "keys", "traps", "hunt_trap"] + TRACK[1:],
    "pairs": ["id", "status", "score", "key", "key_is", "a", "b", "a_schema", "b_schema", "a_col", "b_col",
              "a_rows", "b_rows", "tags", "look_for", "charts", "traps"] + TRACK[1:],
    "hops": ["id", "status", "score", "a", "a_key", "c", "c_key", "a_schema", "c_schema", "a_rows", "c_rows",
             "via", "via_count", "tags", "look_for", "charts", "traps"] + TRACK[1:],
    "place": ["id", "status", "score", "schema", "table", "rows", "level", "geo_col", "all_levels", "metrics",
              "a", "b", "tags", "look_for", "charts", "traps", "hunt_trap"] + TRACK[1:],
    "names": ["id", "status", "score", "schema", "table", "rows", "name_cols", "kind", "has_id", "has_state",
              "bridge_to", "tags", "look_for", "charts", "traps", "hunt_trap"] + TRACK[1:],
    "time": ["id", "status", "score", "schema", "table", "rows", "event_date", "entity", "partners",
             "partner_tables", "tags", "look_for", "charts", "traps", "hunt_trap"] + TRACK[1:],
    "rollups": ["id", "status", "score", "key", "key_is", "kind", "n_harm", "n_money", "harm_tables", "money_tables",
                "tags", "look_for", "charts", "traps"] + TRACK[1:],
    "chains": ["id", "status", "path", "look_for", "charts", "grown_from"] + TRACK[1:],
    "findings": ["id", "date", "layer", "tier", "headline", "chart", "ledger_rows", "tables", "skeptic", "sql", "notes"],
}
LAYERS = ["singles", "pairs", "hops", "rollups", "place", "names", "time", "chains"]
LAYER_WHAT = {
    "singles": "one table alone: who gets the most, worst actors, outliers, gaps, disparities, spikes",
    "pairs": "two tables sharing an ID: does it land, is there a gap, and year-over-year for siblings",
    "hops": "two tables with different IDs, linked through a crosswalk that carries both",
    "rollups": "one row per ID: the same doctor, firm or facility across every harm table, and harm against money",
    "place": "one table by county, ZIP, state, country or map point; plus county pairs and what sits near what",
    "names": "tables that name people, firms or addresses: who repeats, and which ID table they bridge to",
    "time": "tables with an event date: what happened before and after the ban, fine, crash or sale",
    "chains": "four or more tables, grown by hand from live rows in the layers below",
}


def merge(name, fresh):
    """Fresh rows carry what and where. Old rows carry status and notes. Old wins on TRACK columns."""
    old = {r["id"]: r for r in read_tsv(name)}
    seen = set()
    for r in fresh:
        o = old.get(r["id"])
        if o and o.get("by") == "build":  # build's own verdict is redone every time, so a fixed guard clears it
            o = None
        for c in TRACK:
            r[c] = o.get(c, "") if o else ""
        r["status"] = r["status"] or "untouched"
        if r.get("auto_skip") and r["status"] == "untouched":
            r["status"], r["found"], r["by"], r["date"] = "skip", r["auto_skip"], "build", today()
        seen.add(r["id"])
    for i, o in old.items():  # a table left the catalog: keep its history, mark it
        if i not in seen and o.get("status") not in ("", "untouched"):
            o["tags"] = (o.get("tags", "") + " GONE").strip()
            fresh.append(o)
    fresh.sort(key=lambda r: (-float(r.get("score") or 0), r["id"]))
    return fresh


def build():
    T = load_catalog()
    pairs = build_pairs(T)
    layers = {"singles": build_singles(T), "pairs": pairs, "hops": build_hops(T, pairs), "rollups": build_rollups(T),
              "place": build_place(T), "names": build_names(T), "time": build_time(T, pairs)}
    derived = {n for n, t in T.items() if t["derived"]}
    for rows in layers.values():
        for r in rows:
            touched = {r.get(k) for k in ("table", "a", "b", "c")}
            if r.get("auto_skip"):
                continue
            if touched & derived:
                r["auto_skip"] = ("auto-skip at build: built on a prior hunt's output table in FINDINGS; "
                                  "shave its source tables instead")
            elif touched & set(DUPLICATE_OF):
                dup = sorted(touched & set(DUPLICATE_OF))[0]
                r["auto_skip"] = f"auto-skip at build: {dup} is a copy of {DUPLICATE_OF[dup]}; the original's rows carry the work"
    (LEDGER / "_cuts.json").write_text(json.dumps(CUTS), encoding="utf-8")
    for name, rows in layers.items():
        write_tsv(name, merge(name, rows), COLS[name])
    for name in ("chains", "findings"):
        write_tsv(name, read_tsv(name), COLS[name])
    render()
    status()

# ---------------------------------------------------------------- updates


def find_rows(q):
    """Exact id first, then a unique substring across every layer."""
    hits = []
    for name in LAYERS:
        for r in read_tsv(name):
            if r["id"] == q:
                return [(name, r["id"])]
            if q.upper() in r["id"].upper():
                hits.append((name, r["id"]))
    return hits


def mark(q, st, note="", finding="", by="claude", keep_finding=False):
    if st not in STATUSES:
        sys.exit(f"status must be one of {STATUSES}")
    hits = find_rows(q)
    if not hits:
        sys.exit(f"no row matches {q}")
    if len(hits) > 1:
        print(f"{len(hits)} rows match {q}; use a full id:")
        for n, i in hits[:15]:
            print(f"  {n:8} {i}")
        sys.exit(1)
    name, rid = hits[0]
    rows = read_tsv(name)
    for r in rows:
        if r["id"] == rid:
            if not (keep_finding and r.get("status") == "finding"):
                r["status"] = st
            if note:
                r["found"] = f"{r['found']} // {note}".strip(" /") if r.get("found") else note
            if finding:
                ids = [x for x in (r.get("finding_ids") or "").split() if x]
                r["finding_ids"] = " ".join(sorted(set(ids + finding.split(","))))
            r["by"], r["date"] = by, today()
    write_tsv(name, rows, COLS[name])
    print(f"{name}: {rid} -> {st}")


def release(who="", stale_days=0):
    """Hand claimed rows back. By agent name, or every claim older than N days, like after a crash."""
    cutoff = (dt.date.today() - dt.timedelta(days=stale_days)).isoformat() if stale_days else ""
    n = 0
    for name in LAYERS:
        rows = read_tsv(name)
        hit = False
        for r in rows:
            if r.get("status") != "claimed":
                continue
            if (who and r.get("by") == who) or (cutoff and r.get("date", "") < cutoff):
                r["status"], r["by"], r["date"] = "untouched", "", ""
                n += 1
                hit = True
        if hit:
            write_tsv(name, rows, COLS[name])
    print(f"released {n} claimed rows")


def next_id(name, prefix):
    n = [int(r["id"].split("-")[1]) for r in read_tsv(name) if r["id"].startswith(prefix)]
    return f"{prefix}{max(n, default=0) + 1:03d}"


def found(layer, tier, headline, rows="", sql="", tables="", skeptic="not sent", notes="", chart=""):
    fs = read_tsv("findings")
    fid = next_id("findings", "F-")
    fs.append(dict(id=fid, date=today(), layer=layer, tier=tier, headline=headline, chart=chart, ledger_rows=rows,
                   tables=tables, skeptic=skeptic, sql=sql, notes=notes))
    write_tsv("findings", fs, COLS["findings"])
    for q in [x.strip() for x in rows.split(",") if x.strip()]:
        # A clean miss answers one question; the row may hold others, so it stays open as probed.
        # A row that already holds a finding never drops back.
        st = "finding" if tier in ("A", "B") else "probed"
        mark(q, st, finding=fid, note=f"{fid} {tier}: {headline}", keep_finding=True)
    print(f"findings: {fid} {tier} {headline}")
    return fid


def chain(path, look, grown_from="", st="untouched", note="", chart="flow diagram"):
    cs = read_tsv("chains")
    cid = next_id("chains", "C-")
    look = look if " :: " in look else q(look, chart)
    cs.append(dict(id=cid, status=st, path=path, look_for=look, charts=chart.replace(" ", "_"),
                   grown_from=grown_from, found=note,
                   by="claude", date=today()))
    write_tsv("chains", cs, COLS["chains"])
    print(f"chains: {cid} {path}")
    return cid

# ---------------------------------------------------------------- views


def coverage():
    out = {}
    for name in LAYERS:
        rows = read_tsv(name)
        c = {s: 0 for s in STATUSES}
        for r in rows:
            c[r.get("status") or "untouched"] = c.get(r.get("status") or "untouched", 0) + 1
        out[name] = dict(total=len(rows), **c)
    return out


def status():
    """Worked means a person or agent touched it. Build's own auto-skips are shown apart, never as progress."""
    cov = coverage()
    cols = [s for s in STATUSES if s != "untouched"]
    print(f"\n{'layer':8} {'open':>6} {'worked':>7} {'%':>6}  {'untouched':>9} "
          + " ".join(f"{s:>8}" for s in cols) + f"  {'auto-skip':>9}")
    for name, c in cov.items():
        auto = sum(1 for r in read_tsv(name) if r.get("status") == "skip" and r.get("by") == "build")
        open_ = c["total"] - auto
        worked = open_ - c["untouched"]
        pct = 100 * worked / open_ if open_ else 0
        vals = [c[s] - (auto if s == "skip" else 0) for s in cols]
        print(f"{name:8} {open_:6} {worked:7} {pct:5.1f}%  {c['untouched']:9} "
              + " ".join(f"{v:8}" for v in vals) + f"  {auto:9}")
    print(f"\nfindings: {len(read_tsv('findings'))}   page: ledger/ledger.html\n")


def show_next(name, n=20, tag="", claim=""):
    """Best untouched rows. 'all' ranks across every layer. --claim NAME reserves them for one agent."""
    names = [x for x in LAYERS if x != "chains"] if name == "all" else [name]
    rows = [(ln, r) for ln in names for r in read_tsv(ln)
            if r["status"] == "untouched" and tag.upper() in r.get("tags", "") + " " + r.get("charts", "").upper()]
    rows.sort(key=lambda x: -float(x[1].get("score") or 0))
    for ln, r in rows[:n]:
        print(f"{r.get('score', ''):>5}  {r['id']}")
        for item in r.get("look_for", "").split(" | "):
            print(f"       - {item.replace(' :: ', '   [') + (']' if ' :: ' in item else '')}")
        print()
    if claim:
        for ln, r in rows[:n]:
            mark(r["id"], "claimed", by=claim)


def excluded():
    """What the pairs layer leaves out on purpose, counted, so the cut is visible."""
    er = json.loads(ER.read_text(encoding="utf-8"))["t"]
    by = defaultdict(set)
    for _, name, _, cols, _ in er:
        for c, _, lab in cols:
            if lab in CATEGORY_KEYS:
                by[lab].add(name)
    return [dict(key=k, tables=len(v), pairs=len(v) * (len(v) - 1) // 2) for k, v in sorted(by.items())]


def render():
    data = {}
    for n in LAYERS + ["findings"]:
        rows = read_tsv(n)
        cols = COLS[n]
        data[n] = {"cols": cols, "rows": [[r.get(c, "") for c in cols] for r in rows]}
    data["_what"] = LAYER_WHAT
    data["_excluded"] = excluded()
    cp = LEDGER / "_cuts.json"
    data["_cuts"] = json.loads(cp.read_text(encoding="utf-8")) if cp.exists() else {}
    data["_built"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    tpl = (ROOT / "scripts" / "ledger_page.html").read_text(encoding="utf-8")
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    out, tmp = LEDGER / "ledger.html", LEDGER / f".ledger.{os.getpid()}.html"
    tmp.write_text(tpl.replace("/*DATA*/null", blob), encoding="utf-8")
    for attempt in range(20):  # Windows refuses the swap while an editor or browser holds the file
        try:
            os.replace(tmp, out)
            return
        except OSError:
            time.sleep(0.25)
    tmp.unlink(missing_ok=True)
    print("page not refreshed: ledger.html is held open elsewhere; the TSVs are saved, run `ledger.py render` later")

@contextlib.contextmanager
def locked(wait=60):
    """One writer at a time. Parallel shavers share these files."""
    LEDGER.mkdir(exist_ok=True)
    lock = LEDGER / ".lock"
    t0 = time.time()
    while True:
        try:
            fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            if time.time() - t0 > wait:
                sys.exit(f"ledger is locked by another writer for {wait}s; if nobody is running, delete {lock}")
            time.sleep(0.2)
    try:
        yield
    finally:
        os.close(fd)
        os.remove(lock)

# ---------------------------------------------------------------- cli


def opt(args, flag, default=""):
    if flag in args:
        i = args.index(flag)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def main(argv):
    if not argv:
        print(__doc__)
        return
    cmd, args = argv[0], argv[1:]
    if cmd == "status":
        status()
        return
    if cmd == "next" and "--claim" not in args:
        tag = opt(args, "--tag")
        show_next(args[0] if args else "all", int(args[1]) if len(args) > 1 else 20, tag)
        return
    with locked():
        if cmd == "build":
            build()
        elif cmd == "render":
            render()
        elif cmd == "next":
            tag, who = opt(args, "--tag"), opt(args, "--claim")
            show_next(args[0] if args else "all", int(args[1]) if len(args) > 1 else 20, tag, who)
            render()
        elif cmd == "mark":
            fid, by = opt(args, "--finding"), opt(args, "--by", "claude")
            mark(args[0], args[1], args[2] if len(args) > 2 else "", fid, by)
            render()
        elif cmd == "found":
            rows, sql, tables = opt(args, "--rows"), opt(args, "--sql"), opt(args, "--tables")
            sk, notes, chart = opt(args, "--skeptic", "not sent"), opt(args, "--notes"), opt(args, "--chart")
            found(args[0], args[1], args[2], rows, sql, tables, sk, notes, chart)
            render()
        elif cmd == "release":
            days = opt(args, "--stale")
            release(args[0] if args else "", int(days) if days else 0)
            render()
        elif cmd == "chain":
            gf, st, note = opt(args, "--from"), opt(args, "--status", "untouched"), opt(args, "--found")
            chart = opt(args, "--chart", "flow diagram")
            chain(args[0], args[1] if len(args) > 1 else "", gf, st, note, chart)
            render()
        else:
            print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
