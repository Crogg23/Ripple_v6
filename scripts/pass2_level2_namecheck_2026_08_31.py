"""Name-check the 'level 2 only' pass-2 edges + stress the questioned SOLIDs. 2026-08-31.

Extends scripts/pass2_precision_check_2026_08_29.py (same sampling + scoring, imported)
to the edges that shipped with overlap numbers but no matched-pair name check.

Edges that CANNOT be name-checked are listed in NAME_FREE with the reason —
that list is part of the deliverable, not an omission.

Output: reports/recon/pass2/pass2_level2_namecheck_2026-08-31.json + .log
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
spec = importlib.util.spec_from_file_location(
    "p2", os.path.join(HERE, "pass2_precision_check_2026_08_29.py"))
p2 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p2)

REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "reports", "recon", "pass2", "pass2_level2_namecheck_2026-08-31.json")
LOGP = os.path.join(REPO, "reports", "recon", "pass2", "pass2_level2_namecheck_2026-08-31.log")

# same tuple shape as the original EDGES
EDGES = [
    ("HRSA site grantee id -> health center info", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER", "SITE_NAME", "SITE_STATE_ABBREVIATION", "FED_HRSA_UDS_HEALTH_CENTER_INFO", "BHCMISID", "HEALTHCENTERNAME", None, "upper"),
    ("NRC report seq -> incident seq", "FED_USCG_NRC_INCIDENT_REPORTS", "SEQNOS", "RESPONSIBLE_COMPANY", None, "FED_USCG_NRC_INCIDENTS", "SEQNOS", "RESPONSIBLE_COMPANY", None, "digits", 20, 20),
    ("FDIC ultimate-parent cert -> cert", "FED_FDIC_BANK_DATA", "ULTCERT", "NAME", "STALP", "FED_FDIC_BANK_DATA", "CERT", "NAME", "STALP", "ltrim0"),
    ("FDIC direct-parent cert -> cert (tiny)", "FED_FDIC_BANK_DATA", "PARCERT", "NAME", "STALP", "FED_FDIC_BANK_DATA", "CERT", "NAME", "STALP", "ltrim0"),
    ("FHA sponsor # -> originating mortgagee # (same file)", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "SPONSOR_NUMBER", "SPONSOR_NAME", None, "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "ORIGINATING_MORTGAGEE_NUMBER", "ORIGINATION_MORTGAGEE_SPONSOR_ORIGINATOR", None, "digits", 20, 20),
    ("MMF series id -> SEC series registry", "FED_SEC_MONEY_MARKET_FUND_INFORMATION", "SERIES_ID", "SERIES_NAME", None, "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "SERIES_ID", "SERIES_NAME", None, "upper"),
    ("EPA crosswalk ultimate-parent LEI -> GLEIF", "XC_EPA_CORPORATE_CROSSWALK", "ULTIMATE_PARENT_LEI", "PARENT_LEGAL_NAME", None, "INTL_GLEIF", "LEI", "Entity.LegalName", None, "upper"),
    ("EPA crosswalk parent CIK -> insider issuer CIK", "XC_EPA_CORPORATE_CROSSWALK", "PARENT_CIK", "PARENT_LEGAL_NAME", None, "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "ISSUERNAME", None, "ltrim0"),
    ("FMCSA prior-revoke DOT -> DOT (reincorporation)", "FED_FMCSA_COMPANY_CENSUS", "PRIOR_REVOKE_DOT_NUMBER", "LEGAL_NAME", "PHY_STATE", "FED_FMCSA_COMPANY_CENSUS", "DOT_NUMBER", "LEGAL_NAME", "PHY_STATE", "digits"),
    ("OSHA injury log EIN -> Form 5500 sponsor EIN", "FED_OSHA_ITA_300A_SUMMARY_2024", "EIN", "COMPANY_NAME", None, "FED_DOL_FORM5500_FULL", "SPONS_DFE_EIN", "SPONSOR_DFE_NAME", None, "digits"),
    ("OSHA injury log EIN -> IRS nonprofit EIN", "FED_OSHA_ITA_300A_SUMMARY_2024", "EIN", "COMPANY_NAME", None, "FED_IRS_BMF", "EIN", "NAME", None, "digits"),
    ("OSHA establishment across years", "FED_OSHA_ITA_300A_SUMMARY_2024", "ESTABLISHMENT_ID", "ESTABLISHMENT_NAME", None, "FED_OSHA_ITA_300A_SUMMARY_2023", "ESTABLISHMENT_ID", "ESTABLISHMENT_NAME", None, "upper"),
    ("Subaward FAIN -> its grant", "FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_FAIN", "PRIME_AWARDEE_NAME", None, "FED_USASPENDING_ASSISTANCE_FULL", "award_id_fain", "recipient_name", None, "upper", 10, 10),
    ("Subawardee parent UEI -> SAM", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_PARENT_UEI", "SUBAWARDEE_PARENT_NAME", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 5, 100),
    ("Grant recipient UEI -> SAM", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_uei", "recipient_name", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 3, 100),
    ("SBIR contract # -> contract record", "FED_SBIR_STTR_AWARDS", "CONTRACT", "COMPANY", None, "FED_USASPENDING_CONTRACTS_FULL_R2", "AWARD_ID_PIID", "RECIPIENT_NAME", None, "upper", 100, 3),
    ("SBIR tracking # -> NIH project", "FED_SBIR_STTR_AWARDS", "AGENCY_TRACKING_NUMBER", "COMPANY", None, "FED_NIH_REPORTER", "CORE_PROJECT_NUM", "ORG_NAME", None, "upper", 100, 20),
    ("Hospital enrollment PAC -> PECOS master", "FED_CMS_HOSPITAL_ENROLLMENTS", "ASSOCIATE_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "ORG_NAME", "STATE_CD", "digits"),
    ("SNF enrollment PAC -> PECOS master", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "ASSOCIATE_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "ORG_NAME", "STATE_CD", "digits"),
    ("HHA enrollment PAC -> PECOS master", "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS", "ASSOCIATE_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "ORG_NAME", "STATE_CD", "digits"),
    ("FQHC enrollment PAC -> PECOS master", "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS", "ASSOCIATE_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "ORG_NAME", "STATE_CD", "digits"),
    ("RHC enrollment PAC -> PECOS master", "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS", "ASSOCIATE_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "ORG_NAME", "STATE_CD", "digits"),
    ("Hospital enrollment id -> PECOS master", "FED_CMS_HOSPITAL_ENROLLMENTS", "ENROLLMENT_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "ORG_NAME", "STATE_CD", "upper"),
    ("SNF enrollment id -> PECOS master", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "ENROLLMENT_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "ORG_NAME", "STATE_CD", "upper"),
    ("HHA enrollment id -> PECOS master", "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS", "ENROLLMENT_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "ORG_NAME", "STATE_CD", "upper"),
    ("FQHC enrollment id -> PECOS master", "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS", "ENROLLMENT_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "ORG_NAME", "STATE_CD", "upper"),
    ("RHC enrollment id -> PECOS master", "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS", "ENROLLMENT_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "ORG_NAME", "STATE_CD", "upper"),
    ("Hospice enrollment id -> PECOS master", "FED_CMS_HOSPICE_ENROLLMENTS", "ENROLLMENT_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "ENRLMT_ID", "ORG_NAME", "STATE_CD", "upper"),
    ("Subaward award key -> prime contract", "FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_UNIQUE_KEY", "PRIME_AWARDEE_NAME", None, "FED_USASPENDING_CONTRACTS_FULL_R2", "CONTRACT_AWARD_UNIQUE_KEY", "RECIPIENT_NAME", None, "upper", 10, 2),
    ("Debarred CAGE -> contract CAGE", "FED_SAM_EXCLUSIONS_FULL_R2", "CAGE", "NAME", None, "FED_USASPENDING_CONTRACTS_FULL_R2", "CAGE_CODE", "RECIPIENT_NAME", None, "upper", 100, 2),
    ("Branch cert -> bank cert", "FED_FDIC_SOD_BRANCH_DEPOSITS", "CERT", "NAMEFULL", None, "FED_FDIC_BANK_DATA", "CERT", "NAME", None, "ltrim0", 20, 100),
    ("Branch RSSD -> bank RSSD", "FED_FDIC_SOD_BRANCH_DEPOSITS", "RSSDID", "NAMEFULL", None, "FED_FDIC_BANK_DATA", "FED_RSSD", "NAME", None, "ltrim0", 20, 100),
    ("eGRID plant -> EIA plant master", "FED_EPA_EGRID_PLANT_2022", "DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE", "PLANT_NAME", None, "FED_EIA860_2_PLANT", "PLANT_CODE", "PLANT_NAME", None, "digits"),
    ("Generator -> its plant", "FED_EIA860_3_1_GENERATOR", "PLANT_CODE", "PLANT_NAME", None, "FED_EIA860_2_PLANT", "PLANT_CODE", "PLANT_NAME", None, "digits"),
    ("Plant -> its operating utility", "FED_EIA860_2_PLANT", "UTILITY_ID", "UTILITY_NAME", None, "FED_EIA860_1_UTILITY", "UTILITY_ID", "UTILITY_NAME", None, "digits"),
    ("eGRID plant -> its utility", "FED_EPA_EGRID_PLANT_2022", "UTILITY_ID", "UTILITY_NAME", None, "FED_EIA860_1_UTILITY", "UTILITY_ID", "UTILITY_NAME", None, "digits"),
    ("EIA-861 seller -> EIA-860 utility", "FED_EIA861_UTILITY_DATA", "UTILITY_NUMBER", "UTILITY_NAME", None, "FED_EIA860_1_UTILITY", "UTILITY_ID", "UTILITY_NAME", None, "digits"),
    ("CAMPD smokestack facility -> EIA plant", "FED_EPA_CAMPD_FACILITY", "FACILITY_ID", "FACILITY_NAME", None, "FED_EIA860_2_PLANT", "PLANT_CODE", "PLANT_NAME", None, "digits"),
    ("Contractor UEI -> SAM (R2 full file)", "FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_UEI", "RECIPIENT_NAME", "RECIPIENT_STATE_CODE", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", "PHYSICAL_ADDRESS_STATE", "upper", 0.5, 100),
    ("Contractor UEI -> SAM (recent copy)", "FED_USASPENDING_CONTRACTS", "RECIPIENT_UEI", "RECIPIENT_NAME", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 5, 100),
    ("Contractor UEI -> SAM (20M truncated copy)", "FED_USASPENDING_CONTRACTS_FULL", "recipient_uei", "recipient_name", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 2, 100),
]

# two-hop stress test for the worst-scoring SOLID: HRSA site NPI -> NPPES (35.6% site-vs-org).
# claim: the NPI belongs to the site's PARENT org. If true, the parent grantee's name
# (via BHCMIS join to health-center info) should match NPPES at a much higher rate.
TWO_HOP_SQL = """
WITH s AS (
  SELECT NULLIF(REGEXP_REPLACE(FQHC_SITE_NPI_NUMBER,'[^0-9]',''),'') AS npi,
         SITE_NAME, BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER AS bh
  FROM LIBRARY_RAW.LANDING.FED_HRSA_UDS_SERVICE_DELIVERY_SITES
  QUALIFY ROW_NUMBER() OVER (PARTITION BY npi ORDER BY RANDOM()) = 1
), h AS (
  SELECT NULLIF(UPPER(TRIM(BHCMISID)),'') AS bh, HEALTHCENTERNAME
  FROM LIBRARY_RAW.LANDING.FED_HRSA_UDS_HEALTH_CENTER_INFO
  QUALIFY ROW_NUMBER() OVER (PARTITION BY bh ORDER BY RANDOM()) = 1
), n AS (
  SELECT NULLIF(REGEXP_REPLACE(NPI,'[^0-9]',''),'') AS npi,
         PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME AS org
  FROM LIBRARY_RAW.LANDING.FED_CMS_NPPES
  QUALIFY ROW_NUMBER() OVER (PARTITION BY npi ORDER BY RANDOM()) = 1
)
SELECT s.npi, s.SITE_NAME, h.HEALTHCENTERNAME, n.org
FROM s JOIN n USING (npi) LEFT JOIN h ON NULLIF(UPPER(TRIM(s.bh)),'') = h.bh
WHERE s.npi IS NOT NULL ORDER BY RANDOM() LIMIT 60"""

NAME_FREE = [
    ("GUDID DEVICE -> IDENTIFIERS", "same publisher, same DI, join is by construction"),
    ("FDIC/SOD RSSDHCR both sides", "holding-company pointers; the Fed NIC master is not held, no name resolves"),
    ("GLEIF relationships start/end node", "relationship rows carry no name; both ends resolve only through GLEIF itself"),
    ("CourtListener predecessor/supervisor/parent-court", "pointer's own name not stored on the left row; tiny edges"),
    ("EIA owner row -> its plant", "owner name vs plant name differ by design"),
    ("CMS facility-affiliation IND_PAC_ID", "person-grain: clinician names vs org master; needs a person-name spec"),
    ("PECOS_PROVIDER_ENROLLMENT dup", "same file loaded twice, by construction"),
    ("HMDA HUD rows -> IRS BMF", "HMDA historic carries no lender name; 19 matched keys anyway"),
    ("GLEIF successor LEI -> LEI", "successor NAME column is 100% empty where a successor LEI exists; 0 of 34,181 scoreable (live full-table count 2026-08-31)"),
]


def main():
    log = open(LOGP, "a", encoding="utf-8")
    def L(m):
        line = f"{time.strftime('%H:%M:%S')} {m}"; print(line, flush=True); log.write(line + "\n"); log.flush()
    conn = p2.sf.connect(); cur = conn.cursor()
    cur.execute("ALTER SESSION SET QUERY_TAG='pass2_level2_namecheck_2026_08_31'")
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 900")
    out = {"edges": [], "name_free": [dict(label=a, reason=b) for a, b in NAME_FREE]}
    L(f"{len(EDGES)} edges, {p2.N} pairs each")
    for i, e in enumerate(EDGES, 1):
        label = e[0]
        try:
            cur.execute(p2.sample_sql(e)); rows = cur.fetchall()
            nm = [p2.name_match(r[1], r[3]) for r in rows]
            scored = [x for x in nm if x is not None]
            st = [(r[2] or "").strip().upper() == (r[4] or "").strip().upper() for r in rows if r[2] and r[4]]
            miss = [(r[0], str(r[1])[:40], str(r[3])[:40]) for r, m in zip(rows, nm) if m is False][:3]
            # sample matched pairs too, so false POSITIVES are auditable (skeptic 2026-08-31)
            hits = [(r[0], str(r[1])[:40], str(r[3])[:40]) for r, m in zip(rows, nm) if m is True][:3]
            res = dict(label=label, pairs=len(rows), name_scored=len(scored),
                       name_match_pct=round(100 * sum(scored) / len(scored), 1) if scored else None,
                       state_scored=len(st), state_match_pct=round(100 * sum(st) / len(st), 1) if st else None,
                       mismatches=miss, matched_samples=hits)
            out["edges"].append(res)
            L(f"[{i}] {label}: names {res['name_match_pct']}% of {len(scored)} | states {res['state_match_pct']}% of {len(st)}")
        except Exception as ex:  # noqa: BLE001
            out["edges"].append(dict(label=label, error=str(ex)[:300])); L(f"[{i}] ERR {label}: {str(ex)[:200]}")
        json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)

    L("two-hop HRSA->NPPES stress test")
    try:
        cur.execute(TWO_HOP_SQL); rows = cur.fetchall()
        site = [p2.name_match(r[1], r[3]) for r in rows]
        parent = [p2.name_match(r[2], r[3]) for r in rows if r[2]]
        either = [p2.name_match(r[1], r[3]) or (r[2] and p2.name_match(r[2], r[3])) for r in rows]
        def pct(xs):
            xs = [x for x in xs if x is not None]
            return round(100 * sum(bool(x) for x in xs) / len(xs), 1) if xs else None
        out["hrsa_two_hop"] = dict(pairs=len(rows), site_vs_nppes=pct(site),
                                   parent_vs_nppes=pct(parent), either=pct(either),
                                   parent_scored=len([x for x in parent if x is not None]))
        L(f"two-hop: site {pct(site)}% | parent {pct(parent)}% | either {pct(either)}%")
    except Exception as ex:  # noqa: BLE001
        out["hrsa_two_hop"] = dict(error=str(ex)[:300]); L(f"ERR two-hop: {str(ex)[:200]}")
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    L("DONE")


if __name__ == "__main__":
    main()
