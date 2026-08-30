"""Handbook follow-up overlaps, 2026-08-30.

Re-measures (and logs, for the first time) the 2026-08-29 connections that were quoted in the
pass-1 / pass-2 reports but never written to a JSON receipt, plus the PECOS pointer edges the
bucket-B verification skipped. Read-only; ~a dozen small queries.

Output: reports/recon/pass2/handbook_followups_2026-08-30.json + .log
"""
from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _snowflake_conn as sf  # noqa: E402

REPO = os.path.dirname(HERE)
OUTDIR = os.path.join(REPO, "reports", "recon", "pass2")
OUT = os.path.join(OUTDIR, "handbook_followups_2026-08-30.json")
LOGP = os.path.join(OUTDIR, "handbook_followups_2026-08-30.log")
DB = "LIBRARY_RAW.LANDING"


def q(col):
    import re
    return col if re.fullmatch(r"[A-Z_][A-Z0-9_]*", col) else '"' + col + '"'


def K(col, how):
    c = q(col)
    return {
        "upper": f"NULLIF(UPPER(TRIM({c})),'')",
        "digits": f"NULLIF(REGEXP_REPLACE({c},'[^0-9]',''),'')",
        "ltrim0": f"NULLIF(LTRIM(REGEXP_REPLACE({c},'[^0-9]',''),'0'),'')",
        "int": f"NULLIF(LTRIM(REGEXP_REPLACE(SPLIT_PART({c},'.',1),'[^0-9]',''),'0'),'')",
    }[how]


# (label, left table, left col, right table, right col, norm, left_where)
EDGES = [
    ("CAMPD facility id (ORISPL) -> EIA-860 plant code", "FED_EPA_CAMPD_FACILITY", "FACILITY_ID",
     "FED_EIA860_2_PLANT", "PLANT_CODE", "int", ""),
    ("Contracts (R2) recipient UEI -> SAM registrant UEI", "FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_UEI",
     "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper", ""),
    ("Old-HMDA respondent id, bank-regulator rows (agency 1-3) -> FDIC cert", "FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID",
     "FED_FDIC_BANK_DATA", "CERT", "ltrim0", "WHERE TRIM(AGENCY_CODE) IN ('1','2','3')"),
    ("Old-HMDA respondent id, HUD rows (agency 7) -> IRS BMF EIN", "FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID",
     "FED_IRS_BMF", "EIN", "digits", "WHERE TRIM(AGENCY_CODE) = '7'"),
    ("Old-HMDA respondent id, HUD rows (agency 7) -> Form 5500 sponsor EIN", "FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID",
     "FED_DOL_FORM5500_FULL", "SPONS_DFE_EIN", "digits", "WHERE TRIM(AGENCY_CODE) = '7'"),
    ("Home-health agency associate id -> PECOS PAC id", "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS", "ASSOCIATE_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "digits", ""),
    ("FQHC associate id -> PECOS PAC id", "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS", "ASSOCIATE_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "digits", ""),
    ("Rural health clinic associate id -> PECOS PAC id", "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS", "ASSOCIATE_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "digits", ""),
    ("SNF enrollment id -> PECOS enrollment id", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "ENROLLMENT_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "upper", ""),
    ("Home-health enrollment id -> PECOS enrollment id", "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS", "ENROLLMENT_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "upper", ""),
    ("Hospice enrollment id -> PECOS enrollment id", "FED_CMS_HOSPICE_ENROLLMENTS", "ENROLLMENT_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "upper", ""),
    ("FQHC enrollment id -> PECOS enrollment id", "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS", "ENROLLMENT_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "upper", ""),
    ("Rural health clinic enrollment id -> PECOS enrollment id", "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS", "ENROLLMENT_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "upper", ""),
    ("PECOS enrollment twin: PAC id -> FFS enrollment PAC id", "FED_CMS_PECOS_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID",
     "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "digits", ""),
]


def overlap_sql(lt, lc, rt, rc, how, lw):
    return f"""
    WITH l AS (SELECT DISTINCT {K(lc, how)} AS v FROM {DB}.{lt} {lw}),
         r AS (SELECT DISTINCT {K(rc, how)} AS v FROM {DB}.{rt})
    SELECT (SELECT COUNT(*) FROM l WHERE v IS NOT NULL),
           (SELECT COUNT(*) FROM r WHERE v IS NOT NULL),
           (SELECT COUNT(*) FROM l JOIN r USING (v) WHERE v IS NOT NULL)"""


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    log = open(LOGP, "a", encoding="utf-8")

    def L(m):
        line = f"{time.strftime('%H:%M:%S')} {m}"
        print(line, flush=True)
        log.write(line + "\n")
        log.flush()

    conn = sf.connect()
    cur = conn.cursor()
    cur.execute("ALTER SESSION SET QUERY_TAG='handbook_followups_2026_08_30'")
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 600")

    # column sanity for the two tables whose column names were never written down
    cols = {}
    for t in ("FED_EPA_CAMPD_FACILITY", "FED_CFPB_HMDA_HISTORIC"):
        cur.execute(f"SELECT COLUMN_NAME FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS "
                    f"WHERE TABLE_SCHEMA='LANDING' AND TABLE_NAME='{t}' ORDER BY ORDINAL_POSITION")
        cols[t] = [r[0] for r in cur.fetchall()]
        L(f"columns {t}: {cols[t][:40]}")

    out = dict(measured_on="2026-08-30", columns=cols, overlaps=[])
    for label, lt, lc, rt, rc, how, lw in EDGES:
        try:
            cur.execute(overlap_sql(lt, lc, rt, rc, how, lw))
            ld, rd, both = cur.fetchone()
            share = round(100.0 * both / ld, 1) if ld else None
            rec = dict(label=label, left=f"{lt}.{lc}", right=f"{rt}.{rc}", norm=how, left_where=lw,
                       left_distinct=ld, right_distinct=rd, matched=both, share=share)
            L(f"{label}: {both:,} of {ld:,} ({share}%) | right distinct {rd:,}")
        except Exception as ex:  # noqa: BLE001
            rec = dict(label=label, left=f"{lt}.{lc}", right=f"{rt}.{rc}", error=str(ex)[:300])
            L(f"ERR {label}: {str(ex)[:200]}")
        out["overlaps"].append(rec)
        json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    L("DONE")


if __name__ == "__main__":
    main()
