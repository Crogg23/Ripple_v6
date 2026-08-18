"""Pre-rebuild batch verification: every un-wired candidate key column, measured.

For each candidate (existing key axis, landing table, column):
  - fill: rows / nonnull / distinct after the axis's OWN normalization
    (connect.keys.normalize_sql -- the exact SQL the spine would run)
  - spine overlap: how many distinct normalized values already exist in the
    live entity map under that key type (proves same value space, not just
    same column name)
New internal families (water permits, credit unions, ICE facilities) are
verified referentially against their authority table, court-keys style.

Read-only aggregates, checkpointed per candidate. Output:
reports/census_grid_2026-08-12/fill/spine_batch_verification.jsonl
"""
import json
import os
import sys

sys.path.insert(0, r"c:\Code\Ripple_v6")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _snowflake_conn import connect  # noqa: E402
from connect.keys import normalize_sql  # noqa: E402

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "reports", "census_grid_2026-08-12", "fill",
                   "spine_batch_verification.jsonl")
CKPT = OUT + ".done.json"
L = 'LIBRARY_RAW."LANDING"'
EMAP = 'LIBRARY_META."CONNECT"."ENTITY_MAP"'

# (key_axis, table, column) -- existing axes, un-spec'd tables, curated from the
# 2026-08-17 column sweep. Known-dead excluded up front: FED_FOREIGNASSISTANCE.EIN
# (single repeated value, fill census), FED_SAM_EXCLUSIONS (9k round-cap sample,
# FULL_R2 already spec'd), FED_USASPENDING_BULK (50k sample), FED_CFPB_HMDA_LAR
# (17k sample of a redlining dataset -- reload first).
CANDIDATES = [
    ("EIN", "FED_IRS_EO_BMF", "EIN"),
    ("EIN", "FED_IRS_527_ORGS", "EIN"),
    ("EIN", "IRS527_8871_ORGS", "EIN"),
    ("EIN", "IRS527_8872_REPORTS", "EIN"),
    ("EIN", "IRS527_DIRECTORS_OFFICERS", "EIN"),
    ("EIN", "IRS527_RELATED_ENTITIES", "EIN"),
    ("EIN", "FED_US_SEC_EDGAR", "EIN"),
    ("EIN", "FED_DOL_EBSA_FORM5500_SCHEDULE_SB", "SB_EIN"),
    ("EIN", "FED_PBGC_TRUSTEED_PENSION_PLANS", "EIN"),
    ("EIN", "FED_PBGC_TRUSTEED_PLANS", "EIN"),
    ("EIN", "FED_COURTLISTENER_SCHOOLS", "EIN"),
    ("EIN", "FED_FCC_LICENSING", "EIN"),          # expect masked (memory trap) - verify to kill
    ("EIN", "FED_IRS_990_EFILER_INDEX_2022", "EIN"),
    ("EIN", "FED_IRS_990_EFILER_INDEX_2023", "EIN"),
    ("NPI", "FED_CMS_OPEN_PAYMENTS_GNRL", "Covered_Recipient_NPI"),
    ("NPI", "FED_CMS_PECOS_PROVIDER_ENROLLMENT", "NPI"),
    ("NPI", "FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT", "COVERED_RECIPIENT_NPI"),
    ("NPI", "FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL", "SUPLR_NPI"),
    ("NPI", "FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER", "RFRG_NPI"),
    ("NPI", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_NPI_NUMBER"),
    ("CCN", "FED_CMS_OPEN_PAYMENTS_GNRL", "Teaching_Hospital_CCN"),
    ("CCN", "FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE", "RNDRNG_PRVDR_CCN"),
    ("CCN", "FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE", "RNDRNG_PRVDR_CCN"),
    ("UEI", "FED_NIH_REPORTER", "ORG_UEI"),
    ("UEI", "FED_SBIR_STTR_AWARDS", "UEI"),
    ("DUNS", "FED_NIH_REPORTER", "ORG_DUNS"),
    ("DUNS", "FED_SBIR_STTR_AWARDS", "DUNS"),
    ("CIK", "FED_US_SEC_EDGAR", "CIK"),
    ("CIK", "FED_PCAOB_FORM_AP_FILINGS", "ISSUER_CIK"),
    ("CIK", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "CIK_NUMBER"),
    ("CIK", "FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE", "CIK"),
    ("LEI", "FED_FDIC_BANK_DATA", "LEI"),
    ("LEI", "INTL_ISO_MIC_REGISTRY", "LEI"),
    ("IMO", "INTL_UK_SANCTIONS_LIST", "IMO_NUMBER"),
    ("FRS_ID", "FED_EPA_FRS_FRS_FACILITIES", "REGISTRY_ID"),
    ("FRS_ID", "FED_EPA_ICIS_ICIS_AIR_FACILITIES", "REGISTRY_ID"),
    ("FRS_ID", "FED_EPA_GHGRP_FACILITY", "FRS_ID"),
    ("FRS_ID", "FED_EPA_TRI_FACILITY", "FRS_ID"),
    ("FRS_ID", "FED_EPA_TRI_BASIC_2023", "C_3_FRS_ID"),
    # the in-house EPA corporate crosswalk: measured here for the record, but its
    # matched columns are probabilistic (MATCH_METHOD/MATCH_CONFIDENCE) -- spine
    # admission is decided by the method distribution, not just overlap.
    ("LEI", "XC_EPA_CORPORATE_CROSSWALK", "MATCHED_LEI"),
    ("FRS_ID", "XC_EPA_CORPORATE_CROSSWALK", "EPA_REGISTRY_ID"),
]

# new internal families: (family, carrier, col, authority table, authority col)
INTERNAL = [
    ("NPDES", "FED_EPA_NPDES_NPDES_CS_VIOLATIONS", "NPDES_ID"),
    ("NPDES", "FED_EPA_NPDES_NPDES_PS_VIOLATIONS", "NPDES_ID"),
    ("NPDES", "FED_EPA_NPDES_NPDES_SE_VIOLATIONS", "NPDES_ID"),
    ("NPDES", "FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS", "NPDES_ID"),
    ("NPDES", "FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS", "NPDES_ID"),
    ("NPDES", "FED_EPA_NPDES_NPDES_INSPECTIONS", "NPDES_ID"),
    ("NPDES", "FED_EPA_NPDES_NPDES_QNCR_HISTORY", "NPDES_ID"),
    ("NCUA", "FED_NCUA_CALL_REPORTS_FOICU", "CU_NUMBER"),
    ("NCUA", "FED_NCUA_CALL_REPORTS_FS220", "CU_NUMBER"),
    ("NCUA", "FED_NCUA_CHARTER_MERGER_EVENTS", "CONTINUING_CREDIT_UNION_CHARTER"),
    ("NCUA", "FED_NCUA_CHARTER_MERGER_EVENTS", "MERGING_CREDIT_UNION_CHARTER"),
    ("ICE", "FED_ICE_DETENTION_STINTS", "DETENTION_FACILITY_CODE"),
]
INTERNAL_AUTH = {
    "NPDES": ("FED_EPA_NPDES_ICIS_FACILITIES", "NPDES_ID"),
    "NCUA": ("FED_NCUA_FEDERALLY_INSURED_CU_LIST", "CHARTER_NUMBER"),
    "ICE": ("FED_ICE_DETENTION_FACILITY_CODES", "DETENTION_FACILITY_CODE"),
}


def done_set():
    return set(json.load(open(CKPT))) if os.path.exists(CKPT) else set()


def save(done):
    json.dump(sorted(done), open(CKPT, "w"))


def main():
    conn = connect(database="LIBRARY_RAW")
    cur = conn.cursor()
    out = open(OUT, "a", encoding="utf-8")
    done = done_set()

    for axis, tbl, col in CANDIDATES:
        key = f"{axis}|{tbl}|{col}"
        if key in done:
            continue
        norm = normalize_sql(axis, f'"{col}"')
        try:
            cur.execute(f"""
                with s as (select distinct {norm} as v from {L}."{tbl}" where {norm} is not null)
                select (select count(*) from {L}."{tbl}"),
                       (select count({norm}) from {L}."{tbl}"),
                       (select count(*) from s),
                       (select count(*) from s join {EMAP} e
                          on e.KEY_TYPE = '{axis}' and e.KEY_VALUE = s.v)""")
            n, nn, dn, overlap = cur.fetchone()
            cur.execute(f"select {norm} from {L}.\"{tbl}\" where {norm} is not null limit 5")
            sample = [r[0] for r in cur.fetchall()]
            rec = {"kind": "axis", "axis": axis, "table": tbl, "column": col,
                   "rows": n, "nonnull_norm": nn, "distinct_norm": dn,
                   "spine_overlap": overlap,
                   "overlap_pct": round(100 * overlap / dn, 2) if dn else None,
                   "sample": sample}
        except Exception as e:
            rec = {"kind": "axis", "axis": axis, "table": tbl, "column": col,
                   "error": str(e)[:250]}
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add(key)
        save(done)
        print(json.dumps(rec, default=str)[:220], flush=True)

    for fam, tbl, col in INTERNAL:
        key = f"{fam}|{tbl}|{col}"
        if key in done:
            continue
        auth_t, auth_c = INTERNAL_AUTH[fam]
        try:
            cur.execute(f"""
                select count(*), count(c."{col}"), approx_count_distinct(c."{col}"),
                       count_if(a."{auth_c}" is not null)
                from {L}."{tbl}" c
                left join {L}."{auth_t}" a
                  on upper(trim(to_varchar(a."{auth_c}"))) = upper(trim(to_varchar(c."{col}")))""")
            n, nn, dn, matched = cur.fetchone()
            rec = {"kind": "internal", "family": fam, "table": tbl, "column": col,
                   "rows": n, "nonnull": nn, "distinct": dn, "matched": matched,
                   "match_pct": round(100 * matched / nn, 2) if nn else None}
        except Exception as e:
            rec = {"kind": "internal", "family": fam, "table": tbl, "column": col,
                   "error": str(e)[:250]}
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add(key)
        save(done)
        print(json.dumps(rec, default=str)[:220], flush=True)

    # one-off shape checks
    if "oneoffs" not in done:
        cur.execute(f'select "FEC_IDS" from {L}."FED_CONGRESS_LEGISLATORS" '
                    f'where "FEC_IDS" is not null limit 8')
        fec = [r[0] for r in cur.fetchall()]
        cur.execute(f'select "MATCH_METHOD", "MATCH_CONFIDENCE", count(*) '
                    f'from {L}."XC_EPA_CORPORATE_CROSSWALK" group by 1,2 order by 3 desc limit 12')
        xc = [list(r) for r in cur.fetchall()]
        cur.execute(f'select count(*), approx_count_distinct("CHARTER_NUMBER") '
                    f'from {L}."FED_NCUA_FEDERALLY_INSURED_CU_LIST"')
        ncua = list(cur.fetchone())
        cur.execute(f'select count(*), approx_count_distinct("DETENTION_FACILITY_CODE") '
                    f'from {L}."FED_ICE_DETENTION_FACILITY_CODES"')
        ice = list(cur.fetchone())
        cur.execute(f'select count(*), approx_count_distinct("NPDES_ID"), '
                    f'count_if(nullif(trim("FACILITY_NAME"), \'\') is not null) '
                    f'from {L}."FED_EPA_NPDES_ICIS_FACILITIES"')
        npdes = list(cur.fetchone())
        rec = {"kind": "oneoffs", "legislator_fec_ids_sample": fec,
               "xc_crosswalk_method_dist": xc, "ncua_authority": ncua,
               "ice_authority": ice, "npdes_authority": npdes}
        out.write(json.dumps(rec, default=str) + "\n")
        out.flush()
        done.add("oneoffs")
        save(done)
        print("oneoffs done", flush=True)

    conn.close()
    print("BATCH VERIFICATION DONE", flush=True)


if __name__ == "__main__":
    main()
