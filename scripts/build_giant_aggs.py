"""Giant pre-agg mart generator -- collapse the >1M-row giants into <100k-row rollup
marts so evidence.dev can extract them (its page query wants <=100k rows).

Spec-driven. For each giant we build, in LIBRARY_MARTS.PUBLIC, a rollup:

    CREATE OR REPLACE TABLE LIBRARY_MARTS.PUBLIC.<DOMAIN>__<SOURCE>_<GRAIN>_AGG AS
      SELECT <grain cols>, COUNT(*) AS N_RECORDS, SUM(<NULLIF-before-cast measure>) ...
      FROM <landing table or the 3-year OpenPay UNION>
      [WHERE <junk-year guard>]
      GROUP BY <grain>

...then a plain-English reading-room view over it:

    CREATE OR REPLACE VIEW THE_LIBRARY.<schema>.<NAME> COPY GRANTS AS SELECT * FROM <mart>

Every grain below was verified live to land < 100,000 rows (the preview re-proves each with
COUNT(*) FROM (the agg) and refuses to claim OK if any is >= 100k). Every dollar/number measure
is NULLIF-before-cast (dodges literal 'nan', blank, and sentinel text). Dates use EXPLICIT
formats -- never a bare 8-digit cast (TRY_TO_DATE('10042024') would misread as a 1970 epoch).

GRANTS (audit bug D04): the THE_LIBRARY views are SELECT-granted to RIPPLE_READER and
CLAUDE_MCP_READONLY (the evidence read lane). A plain CREATE OR REPLACE VIEW strips those.
We add COPY GRANTS *and* explicitly re-GRANT to both roles after --apply (COPY GRANTS has
nothing to copy on first creation), then verify with SHOW GRANTS. The marts + views are owned
by ACCOUNTADMIN, so the views read their base marts via ownership chaining -- readers need
SELECT on the view only, not the mart.

    python3 scripts/build_giant_aggs.py            # PREVIEW: prove every rowcount + print DDL
    python3 scripts/build_giant_aggs.py --apply    # create marts + views, grant, verify

Idempotent + re-runnable (CREATE OR REPLACE). --apply snapshots rollback DDL for every object
it will replace to outputs/ before touching anything.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

L = "LIBRARY_RAW.LANDING."
MART_DB = "LIBRARY_MARTS"
MART_SCHEMA = "PUBLIC"          # dbt-free (0 base tables) -> a selector-less dbt build can't clobber it
LIB_DB = "THE_LIBRARY"
READ_ROLES = ("RIPPLE_READER", "CLAUDE_MCP_READONLY")
CAP = 100_000


# ---- reusable, trap-aware SQL fragments -------------------------------------
def money(col: str) -> str:
    """Dollar text -> DOUBLE, NULLIF-before-cast (literal 'nan' -> NULL, not NaN)."""
    return f"TRY_TO_DOUBLE(NULLIF({col},'nan'))"


def num0(col: str) -> str:
    """Integer text -> NUMBER, NULLIF 'nan', COALESCE 0 so it never NULL-poisons a SUM of parts."""
    return f"COALESCE(TRY_TO_NUMBER(NULLIF({col},'nan')),0)"


def damage(col: str) -> str:
    """NOAA storm damage text ('1.00K' / '2.5M' / '3B' / plain / '') -> DOUBLE dollars."""
    return (
        f"CASE WHEN {col} IS NULL OR {col}='' THEN NULL "
        f"WHEN UPPER(RIGHT({col},1))='K' THEN TRY_TO_DOUBLE(NULLIF(LEFT({col},LENGTH({col})-1),''))*1e3 "
        f"WHEN UPPER(RIGHT({col},1))='M' THEN TRY_TO_DOUBLE(NULLIF(LEFT({col},LENGTH({col})-1),''))*1e6 "
        f"WHEN UPPER(RIGHT({col},1))='B' THEN TRY_TO_DOUBLE(NULLIF(LEFT({col},LENGTH({col})-1),''))*1e9 "
        f"WHEN UPPER(RIGHT({col},1))='T' THEN TRY_TO_DOUBLE(NULLIF(LEFT({col},LENGTH({col})-1),''))*1e12 "
        f"ELSE TRY_TO_DOUBLE(NULLIF({col},'')) END"
    )


def esc(s: str) -> str:
    return (s or "").replace("'", "''")


# explicit date-year expressions (never a bare 8-digit cast)
FEC_YEAR = "YEAR(TRY_TO_DATE(TRANSACTION_DT,'MMDDYYYY'))"          # source is MMDDYYYY text
USASP_YEAR = "YEAR(TRY_TO_DATE(ACTION_DATE,'YYYY-MM-DD'))"         # ISO
FCC_YEAR = "YEAR(TRY_TO_DATE(GRANT_DATE,'MM/DD/YYYY'))"            # US slashes
REVOC_YEAR = "YEAR(TRY_TO_DATE(REVOCATION_DATE,'DD-MON-YYYY'))"    # 15-NOV-2017

# The OpenPay giant is three landing tables (2024 + 2023 + 2022) -- same 94 cols, same order.
# INT_OPEN_PAYMENTS_ALL_YEARS is exactly this UNION but lives in a personal dbt dev schema;
# we inline it so the marts carry no fragile cross-schema dependency.
OP_SRC = (
    f"(SELECT * FROM {L}FED_CMS_OPEN_PAYMENTS "
    f"UNION ALL SELECT * FROM {L}FED_CMS_OPEN_PAYMENTS_2023 "
    f"UNION ALL SELECT * FROM {L}FED_CMS_OPEN_PAYMENTS_2022) op"
)


# ---- the spec -- one entry per rollup mart -----------------------------------
# each: mart name, reading-room schema+view, FROM source, grain cols, optional WHERE,
# measures, and the spec's proven target (preview re-proves the live number).
SPEC = [
    {   # 84.2M -> 419
        "raw": "FED_FEC_INDIV_CONTRIBUTIONS (84.2M)",
        "domain": "money_in_politics", "lib_schema": "CAMPAIGN_FINANCE",
        "mart": "MONEY_IN_POLITICS__FEC_INDIV_BY_STATE_CYCLE_AGG",
        "view": "FEC_CONTRIBUTIONS_BY_STATE_AND_CYCLE",
        "src": f"{L}FED_FEC_INDIV_CONTRIBUTIONS",
        "grain": [("CONTRIBUTOR_STATE", "STATE"), ("CYCLE_YEAR", FEC_YEAR)],
        "where": f"{FEC_YEAR} BETWEEN 1979 AND 2026",
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_AMOUNT", f"SUM({money('TRANSACTION_AMT')})")],
        "target": 419,
        "comment": "FEC individual contributions rolled to contributor STATE x CYCLE_YEAR (calendar "
                   "year of the transaction). N_RECORDS = number of contributions; TOTAL_AMOUNT = total "
                   "dollars. Junk transaction years (<1979 or >2026 in the raw) dropped. Pre-aggregated "
                   "from 84.2M raw rows so it extracts under the 100k cap.",
    },
    {   # 84.2M -> 29,878
        "raw": "FED_FEC_INDIV_CONTRIBUTIONS (84.2M)",
        "domain": "money_in_politics", "lib_schema": "CAMPAIGN_FINANCE",
        "mart": "MONEY_IN_POLITICS__FEC_INDIV_BY_CMTE_CYCLE_AGG",
        "view": "FEC_CONTRIBUTIONS_BY_COMMITTEE_AND_CYCLE",
        "src": f"{L}FED_FEC_INDIV_CONTRIBUTIONS",
        "grain": [("CMTE_ID", "CMTE_ID"), ("CYCLE_YEAR", FEC_YEAR)],
        "where": f"{FEC_YEAR} BETWEEN 1979 AND 2026",
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_AMOUNT", f"SUM({money('TRANSACTION_AMT')})")],
        "target": 29878,
        "comment": "FEC individual contributions rolled to recipient COMMITTEE (CMTE_ID) x CYCLE_YEAR. "
                   "N_RECORDS = number of contributions; TOTAL_AMOUNT = total dollars raised. Join CMTE_ID "
                   "to the FEC committee master for names. Junk years dropped. From 84.2M raw rows.",
    },
    {   # ~43.3M (2024+2023+2022 union) -> 19,377
        "raw": "FED_CMS_OPEN_PAYMENTS x3yr (~43.3M)",
        "domain": "health_medicine", "lib_schema": "HEALTH",
        "mart": "HEALTH_MEDICINE__OPEN_PAYMENTS_BY_MFR_NATURE_AGG",
        "view": "OPEN_PAYMENTS_BY_MANUFACTURER_AND_NATURE",
        "src": OP_SRC,
        "grain": [("MANUFACTURER_GPO", "APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME"),
                  ("PROGRAM_YEAR", "PROGRAM_YEAR"),
                  ("PAYMENT_NATURE", "NATURE_OF_PAYMENT_OR_TRANSFER_OF_VALUE")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_AMOUNT", f"SUM({money('TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS')})")],
        "target": 19377,
        "comment": "CMS Open Payments (industry payments to physicians/hospitals), 2022-2024 combined, "
                   "rolled to paying MANUFACTURER/GPO x PROGRAM_YEAR x nature of payment. TOTAL_AMOUNT = "
                   "total USD transferred. From ~43.3M raw payment rows.",
    },
    {   # ~43.3M -> 34,993
        "raw": "FED_CMS_OPEN_PAYMENTS x3yr (~43.3M)",
        "domain": "health_medicine", "lib_schema": "HEALTH",
        "mart": "HEALTH_MEDICINE__OPEN_PAYMENTS_BY_SPECIALTY_STATE_AGG",
        "view": "OPEN_PAYMENTS_BY_SPECIALTY_AND_STATE",
        "src": OP_SRC,
        "grain": [("RECIPIENT_SPECIALTY", "COVERED_RECIPIENT_SPECIALTY_1"),
                  ("PROGRAM_YEAR", "PROGRAM_YEAR"),
                  ("RECIPIENT_STATE", "RECIPIENT_STATE")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_AMOUNT", f"SUM({money('TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS')})")],
        "target": 34993,
        "comment": "CMS Open Payments 2022-2024 rolled to recipient SPECIALTY x PROGRAM_YEAR x recipient "
                   "STATE. TOTAL_AMOUNT = total USD received. From ~43.3M raw payment rows.",
    },
    {   # 9.6M -> 62,927
        "raw": "FED_CMS_NPPES (9.6M)",
        "domain": "health_medicine", "lib_schema": "HEALTH",
        "mart": "HEALTH_MEDICINE__NPPES_BY_TAXONOMY_STATE_AGG",
        "view": "PROVIDERS_BY_TAXONOMY_AND_STATE",
        "src": f"{L}FED_CMS_NPPES",
        "grain": [("TAXONOMY_CODE", "HEALTHCARE_PROVIDER_TAXONOMY_CODE_1"),
                  ("PRACTICE_STATE", "PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_STATE_NAME"),
                  ("ENTITY_TYPE_CODE", "ENTITY_TYPE_CODE")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)")],
        "target": 62927,
        "comment": "NPPES national provider registry rolled to primary TAXONOMY_CODE x practice STATE x "
                   "ENTITY_TYPE_CODE (1=individual, 2=organization). N_RECORDS = number of NPIs. Join "
                   "TAXONOMY_CODE to the NUCC taxonomy for specialty names. From 9.6M providers.",
    },
    {   # 6.3M -> 17,490
        "raw": "FED_USASPENDING_CONTRACTS (6.3M)",
        "domain": "spending_budget", "lib_schema": "GOVERNMENT_SPENDING",
        "mart": "SPENDING_BUDGET__USASPENDING_BY_AGENCY_NAICS_AGG",
        "view": "CONTRACTS_BY_AGENCY_AND_NAICS",
        "src": f"{L}FED_USASPENDING_CONTRACTS",
        "grain": [("AWARDING_AGENCY", "AWARDING_AGENCY_NAME"),
                  ("NAICS_CODE", "NAICS_CODE"),
                  ("ACTION_YEAR", USASP_YEAR)],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_OBLIGATION", f"SUM({money('FEDERAL_ACTION_OBLIGATION')})")],
        "target": 17490,
        "comment": "USASpending federal contract transactions rolled to AWARDING_AGENCY x NAICS_CODE "
                   "(industry) x ACTION_YEAR. TOTAL_OBLIGATION = summed federal action obligation dollars "
                   "(can be negative -- de-obligations). From 6.3M transactions.",
    },
    {   # 6.3M -> 3,925
        "raw": "FED_USASPENDING_CONTRACTS (6.3M)",
        "domain": "spending_budget", "lib_schema": "GOVERNMENT_SPENDING",
        "mart": "SPENDING_BUDGET__USASPENDING_BY_AGENCY_STATE_AGG",
        "view": "CONTRACTS_BY_AGENCY_AND_STATE",
        "src": f"{L}FED_USASPENDING_CONTRACTS",
        "grain": [("AWARDING_AGENCY", "AWARDING_AGENCY_NAME"),
                  ("RECIPIENT_STATE", "RECIPIENT_STATE_CODE"),
                  ("ACTION_YEAR", USASP_YEAR)],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_OBLIGATION", f"SUM({money('FEDERAL_ACTION_OBLIGATION')})")],
        "target": 3925,
        "comment": "USASpending federal contracts rolled to AWARDING_AGENCY x recipient STATE x "
                   "ACTION_YEAR. TOTAL_OBLIGATION = summed federal obligation dollars. From 6.3M transactions.",
    },
    {   # 2.17M -> 3,893
        "raw": "FED_SBA_LOANS (2.17M)",
        "domain": "spending_budget", "lib_schema": "GOVERNMENT_SPENDING",
        "mart": "SPENDING_BUDGET__SBA_LOANS_BY_STATE_PROGRAM_AGG",
        "view": "SBA_LOANS_BY_STATE_AND_PROGRAM",
        "src": f"{L}FED_SBA_LOANS",
        "grain": [("BORROWER_STATE", "BORRSTATE"),
                  ("PROGRAM", "PROGRAM"),
                  ("APPROVAL_FY", "APPROVALFY")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_GROSS_APPROVAL", f"SUM({money('GROSSAPPROVAL')})")],
        "target": 3893,
        "comment": "SBA 7(a)/504 loan approvals rolled to borrower STATE x PROGRAM x approval fiscal year. "
                   "TOTAL_GROSS_APPROVAL = summed gross approved loan dollars. From 2.17M loans.",
    },
    {   # 1.97M -> 7,677
        "raw": "FED_IRS_BMF (1.97M)",
        "domain": "corporate_entities", "lib_schema": "COMPANIES",
        "mart": "CORPORATE_ENTITIES__IRS_BMF_BY_STATE_NTEE_AGG",
        "view": "NONPROFITS_BY_STATE_AND_NTEE",
        "src": f"{L}FED_IRS_BMF",
        "grain": [("STATE", "STATE"),
                  ("SUBSECTION", "SUBSECTION"),
                  ("NTEE_MAJOR", "LEFT(NTEE_CD,1)")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_REVENUE", f"SUM({money('REVENUE_AMT')})")],
        "target": 7677,
        "comment": "IRS Business Master File (tax-exempt orgs) rolled to STATE x 501(c) SUBSECTION x "
                   "NTEE_MAJOR (first letter of the NTEE code = broad nonprofit category). N_RECORDS = "
                   "number of orgs; TOTAL_REVENUE = summed reported revenue. From 1.97M orgs.",
    },
    {   # 1.78M -> 28,343
        "raw": "FED_NOAA_STORM_EVENTS (1.78M)",
        "domain": "energy_environment", "lib_schema": "ENERGY_ENVIRONMENT",
        "mart": "ENERGY_ENVIRONMENT__NOAA_STORMS_BY_STATE_EVENT_AGG",
        "view": "STORM_EVENTS_BY_STATE_AND_TYPE",
        "src": f"{L}FED_NOAA_STORM_EVENTS",
        "grain": [("STATE", "STATE"),
                  ("EVENT_YEAR", "TRY_TO_NUMBER(NULLIF(YEAR,'nan'))"),
                  ("EVENT_TYPE", "EVENT_TYPE")],
        "where": None,
        "measures": [
            ("N_RECORDS", "COUNT(*)"),
            ("TOTAL_DEATHS", f"SUM({num0('DEATHS_DIRECT')}+{num0('DEATHS_INDIRECT')})"),
            ("TOTAL_INJURIES", f"SUM({num0('INJURIES_DIRECT')}+{num0('INJURIES_INDIRECT')})"),
            ("TOTAL_PROPERTY_DAMAGE", f"SUM({damage('DAMAGE_PROPERTY')})"),
            ("TOTAL_CROP_DAMAGE", f"SUM({damage('DAMAGE_CROPS')})"),
        ],
        "target": 28343,
        "comment": "NOAA Storm Events rolled to STATE x EVENT_YEAR x EVENT_TYPE. TOTAL_DEATHS/INJURIES = "
                   "direct+indirect; DAMAGE columns parse the raw K/M/B/T suffix text into USD. From 1.78M events.",
    },
    {   # 1.69M -> 8,765
        "raw": "FED_FCC_LICENSING (1.69M)",
        "domain": "government_power", "lib_schema": "GOVERNMENT",
        "mart": "GOVERNMENT_POWER__FCC_LICENSES_BY_STATE_SERVICE_AGG",
        "view": "FCC_LICENSES_BY_STATE_AND_SERVICE",
        "src": f"{L}FED_FCC_LICENSING",
        "grain": [("STATE", "STATE"),
                  ("RADIO_SERVICE_CODE", "RADIO_SERVICE_CODE"),
                  ("LICENSE_STATUS", "LICENSE_STATUS"),
                  ("GRANT_YEAR", FCC_YEAR)],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)")],
        "target": 8765,
        "comment": "FCC ULS license records rolled to STATE x RADIO_SERVICE_CODE x LICENSE_STATUS x "
                   "GRANT_YEAR. N_RECORDS = number of licenses. From 1.69M license records.",
    },
    {   # 1.42M -> 5,321
        "raw": "FED_CMS_PART_D_PRESCRIBERS (1.42M)",
        "domain": "health_medicine", "lib_schema": "HEALTH",
        "mart": "HEALTH_MEDICINE__PART_D_BY_STATE_TYPE_AGG",
        "view": "PART_D_PRESCRIBING_BY_STATE_AND_TYPE",
        "src": f"{L}FED_CMS_PART_D_PRESCRIBERS",
        "grain": [("PRESCRIBER_STATE", "PRSCRBR_STATE_ABRVTN"),
                  ("PRESCRIBER_TYPE", "PRSCRBR_TYPE")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_CLAIMS", f"SUM({money('TOT_CLMS')})"),
                     ("TOTAL_DRUG_COST", f"SUM({money('TOT_DRUG_CST')})")],
        "target": 5321,
        "comment": "CMS Medicare Part D prescribers rolled to prescriber STATE x prescriber TYPE (specialty). "
                   "TOTAL_CLAIMS = total claims; TOTAL_DRUG_COST = total drug cost USD. From 1.42M prescribers.",
    },
    {   # 1.3M -> 4,976
        "raw": "FED_CMS_MEDICARE_PROVIDER (1.3M)",
        "domain": "health_medicine", "lib_schema": "HEALTH",
        "mart": "HEALTH_MEDICINE__MEDICARE_PROVIDER_BY_STATE_TYPE_AGG",
        "view": "MEDICARE_PROVIDERS_BY_STATE_AND_TYPE",
        "src": f"{L}FED_CMS_MEDICARE_PROVIDER",
        "grain": [("PROVIDER_STATE", "RNDRNG_PRVDR_STATE_ABRVTN"),
                  ("PROVIDER_TYPE", "RNDRNG_PRVDR_TYPE")],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)"),
                     ("TOTAL_SERVICES", f"SUM({money('TOT_SRVCS')})"),
                     ("TOTAL_MEDICARE_PAYMENT", f"SUM({money('TOT_MDCR_PYMT_AMT')})")],
        "target": 4976,
        "comment": "CMS Medicare provider utilization rolled to rendering-provider STATE x provider TYPE. "
                   "TOTAL_SERVICES = total services; TOTAL_MEDICARE_PAYMENT = total Medicare paid USD. From 1.3M providers.",
    },
    {   # 1.2M -> 1,011
        "raw": "FED_IRS_REVOCATION (1.2M)",
        "domain": "corporate_entities", "lib_schema": "COMPANIES",
        "mart": "CORPORATE_ENTITIES__IRS_REVOCATION_BY_STATE_YEAR_AGG",
        "view": "NONPROFIT_REVOCATIONS_BY_STATE_AND_YEAR",
        "src": f"{L}FED_IRS_REVOCATION",
        "grain": [("STATE", "STATE"),
                  ("REVOCATION_YEAR", REVOC_YEAR)],
        "where": None,
        "measures": [("N_RECORDS", "COUNT(*)")],
        "target": 1011,
        "comment": "IRS automatic revocations of tax-exempt status rolled to org STATE x REVOCATION_YEAR. "
                   "N_RECORDS = number of revoked orgs. Revocation date parsed as DD-MON-YYYY. From 1.2M revocations.",
    },
]

# Baked-in exclusions: giants we deliberately DON'T aggregate, with the reason.
EXCLUDED = [
    ("FED_FOREIGNASSISTANCE (3.97M)",
     "BROKEN LOAD -- OBLIGATION_AMOUNT, DISBURSEMENT_AMOUNT, USG_SECTOR, DAC_CATEGORY are 100% empty "
     "(0 non-blank of 3.97M, verified live); COUNTRY/agency hold bare numeric codes. No measure to sum. "
     "Flag for reload, then agg country x agency x sector x FY."),
    ("FED_FHFA_NMDB (19M)",
     "BROKEN LOAD -- STATISTIC_VALUE 100% empty. Flag for reload."),
    ("FED_EOIR_CASE_DATA",
     "1-column TSV wreck -- no parseable grain."),
    ("FED_IRS_EO_BMF",
     "Exact 2x duplicate of FED_IRS_BMF -- would double-count. Use the IRS_BMF agg."),
    ("FED_FJC_IDB",
     "All-blank load."),
    ("FED_NOAA_AIS",
     "Stale 8-day Jan-2024 snapshot, not aggregation-shaped (and a reverse-causality trap)."),
    ("XC_WAYBACK_DOJ_EPSTEIN / INTL_VOETEN_UNGA_VOTES / FED_USGS_WATER",
     "Text/niche -- not rollup-shaped."),
]


# ---- DDL builders ------------------------------------------------------------
def agg_select(e: dict) -> str:
    grain = ",\n         ".join(f"{expr} AS {name}" for name, expr in e["grain"])
    meas = ",\n         ".join(f"{expr} AS {name}" for name, expr in e["measures"])
    where = f"\n  WHERE {e['where']}" if e.get("where") else ""
    gb = ", ".join(str(i + 1) for i in range(len(e["grain"])))
    return (f"SELECT {grain},\n         {meas}\n"
            f"  FROM {e['src']}{where}\n"
            f"  GROUP BY {gb}")


def mart_fqn(e: dict) -> str:
    return f"{MART_DB}.{MART_SCHEMA}.{e['mart']}"


def view_fqn(e: dict) -> str:
    return f"{LIB_DB}.{e['lib_schema']}.{e['view']}"


def mart_ddl(e: dict) -> str:
    return f"CREATE OR REPLACE TABLE {mart_fqn(e)} AS\n{agg_select(e)}"


def view_ddl(e: dict) -> str:
    return (f"CREATE OR REPLACE VIEW {view_fqn(e)} COPY GRANTS\n"
            f"  COMMENT='{esc(e['comment'])}' AS\n"
            f"  SELECT * FROM {mart_fqn(e)}")


# ---- rollback snapshot (destructive --apply only) ----------------------------
def snapshot_rollback(cur) -> Path:
    ts = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    out = REPO / "outputs" / f"_rollback_giant_aggs_{ts}.sql"
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"-- Rollback snapshot for build_giant_aggs.py --apply ({ts})",
             "-- Prior DDL of every object this run will CREATE OR REPLACE. New objects show a DROP.",
             ""]
    for e in SPEC:
        for kind, fqn in (("TABLE", mart_fqn(e)), ("VIEW", view_fqn(e))):
            try:
                cur.execute(f"SELECT GET_DDL('{kind}','{fqn}')")
                lines.append(f"-- prior {kind} {fqn}:")
                lines.append(cur.fetchone()[0].rstrip() + ";")
            except Exception:
                lines.append(f"-- {fqn} did not exist before this run; to roll back:")
                lines.append(f"DROP {kind} IF EXISTS {fqn};")
            lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---- reading-room durability: register the agg views as FRIENDLY_LAYER extras ----
EXTRAS_FQN = "LIBRARY_META.REGISTRY.FRIENDLY_LAYER_EXTRAS"


def register_extras(cur, results) -> int:
    """Persist these agg views as FRIENDLY_LAYER 'extras' so thelibrary_build merges them
    into FRIENDLY_LAYER on every reconcile: they keep their nice friendly names, appear in
    START_HERE, and are NEVER pruned (the prune only drops views absent from FRIENDLY_LAYER).
    Idempotent -- replaces only the rows this script manages (MANAGED_BY='build_giant_aggs')."""
    cur.execute(f"""CREATE TABLE IF NOT EXISTS {EXTRAS_FQN}(
        OBJECT_FQN STRING, LANDING_FQN STRING, SOURCE_ID STRING, LAYER STRING,
        FRIENDLY_SCHEMA STRING, FRIENDLY_NAME STRING, FRIENDLY_DOMAIN STRING,
        ONE_LINER STRING, COMMENT STRING, IS_SAMPLE BOOLEAN, ROW_COUNT NUMBER,
        THE_LIBRARY_FQN STRING, MANAGED_BY STRING, GENERATED_AT TIMESTAMP_NTZ)""")
    cur.execute(f"DELETE FROM {EXTRAS_FQN} WHERE MANAGED_BY='build_giant_aggs'")
    rows = []
    for e, n in results:
        raw = e["src"]
        sid = raw.split(".")[-1].lower() if raw.startswith(L) else "fed_cms_open_payments"
        one_liner = e["comment"].split(". ")[0].rstrip(".") + "."
        rows.append((mart_fqn(e), None, sid, "mart", e["lib_schema"], e["view"], e["domain"],
                     one_liner, e["comment"], False, int(n), view_fqn(e), "build_giant_aggs"))
    cur.executemany(
        f"""INSERT INTO {EXTRAS_FQN}
            (OBJECT_FQN,LANDING_FQN,SOURCE_ID,LAYER,FRIENDLY_SCHEMA,FRIENDLY_NAME,FRIENDLY_DOMAIN,
             ONE_LINER,COMMENT,IS_SAMPLE,ROW_COUNT,THE_LIBRARY_FQN,MANAGED_BY,GENERATED_AT)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP())""", rows)
    return len(rows)


# ---- main --------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Build the giant pre-agg rollup marts (<100k rows).")
    ap.add_argument("--apply", action="store_true", help="create marts + views (default: preview)")
    args = ap.parse_args()

    from connect import db
    conn = db.connect()
    cur = conn.cursor()

    print(f"[{'APPLY' if args.apply else 'PREVIEW'}] giant pre-agg marts -> "
          f"{MART_DB}.{MART_SCHEMA}.*  +  {LIB_DB}.<shelf>.* (COPY GRANTS)\n")

    # PREVIEW: prove every rowcount live, print the DDL it would run.
    results = []
    all_ok = True
    for e in SPEC:
        sel = agg_select(e)
        try:
            n = db.scalar(conn, f"SELECT COUNT(*) FROM (\n{sel}\n)")
        except Exception as ex:
            print(f"  !! {e['mart']} COUNT failed: {str(ex)[:140]}")
            all_ok = False
            results.append((e, None))
            continue
        ok = n < CAP
        all_ok = all_ok and ok
        results.append((e, n))
        flag = "OK  " if ok else "OVER"
        print(f"  [{flag}] {mart_fqn(e)}")
        print(f"         rows={n:,}  (cap {CAP:,}; spec target {e['target']:,})  "
              f"grain={' x '.join(name for name, _ in e['grain'])}")
        print(f"         -> {view_fqn(e)}")
        if not args.apply:
            print("         --- mart DDL ---")
            for ln in mart_ddl(e).splitlines():
                print("         " + ln)
            print("         --- view DDL ---")
            for ln in view_ddl(e).splitlines():
                print("         " + ln)
        print()

    print("  EXCLUDED (not aggregated):")
    for name, reason in EXCLUDED:
        print(f"    - {name}: {reason}")

    sized = [n for _, n in results if n is not None]
    print(f"\n  SUMMARY: {len(SPEC)} marts | "
          f"max rows={max(sized):,} | all <100k={all_ok} | "
          f"total rollup rows={sum(sized):,}")

    if not args.apply:
        print("\n  PREVIEW only -- nothing created. Re-run with --apply.")
        conn.close()
        return 0 if all_ok else 1

    if not all_ok:
        print("\n  ABORT: at least one grain is >= 100k or failed to count. Fix the spec before --apply.")
        conn.close()
        return 1

    # APPLY -------------------------------------------------------------------
    roll = snapshot_rollback(cur)
    print(f"\n  rollback DDL snapshotted -> {roll}")

    # schemas exist already, but keep idempotent + safe.
    cur.execute(f"CREATE SCHEMA IF NOT EXISTS {MART_DB}.{MART_SCHEMA}")
    for sch in sorted({e["lib_schema"] for e in SPEC}):
        cur.execute(f"CREATE SCHEMA IF NOT EXISTS {LIB_DB}.{sch}")

    for e, n in results:
        cur.execute(mart_ddl(e))
        cur.execute(view_ddl(e))                              # COPY GRANTS (preserves on re-run)
        for role in READ_ROLES:                               # explicit re-grant (first-run has nothing to copy)
            cur.execute(f"GRANT SELECT ON VIEW {view_fqn(e)} TO ROLE {role}")
        live = db.scalar(conn, f"SELECT COUNT(*) FROM {mart_fqn(e)}")
        grants = {str(g[5]).upper() for g in cur.execute(f"SHOW GRANTS ON VIEW {view_fqn(e)}").fetchall()}
        have_both = all(r in grants for r in READ_ROLES)
        print(f"   built {e['mart']:52} rows={live:>7,}  grants[RIPPLE_READER+CLAUDE_MCP]={have_both}")
        if not have_both:
            print(f"     [!] {view_fqn(e)} is missing a read grant -- re-grant before shipping.")

    nx = register_extras(cur, results)
    print(f"\n  registered {nx} agg views in {EXTRAS_FQN} "
          f"(so thelibrary_build keeps them on reconcile, never prunes them).")

    print("\n  DONE.")
    conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
