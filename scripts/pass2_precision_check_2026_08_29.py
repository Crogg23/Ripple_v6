"""Level-3 precision check for the pass-2 (and a few pass-1) edges, 2026-08-29.

For each edge: sample up to N matched key pairs (random), pull a name (and where available a state)
from BOTH sides, and score whether the two sides describe the same real-world thing.

Name score: normalize (upper, strip punctuation, drop corporate suffixes/stopwords), then match if
token-Jaccard >= 0.5 OR one normalized name contains the other OR first 12 chars equal.
State score: equal 2-letter codes where both sides have one.

Output: reports/recon/pass2/pass2_precision_2026-08-29.json + .log
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _snowflake_conn as sf  # noqa: E402

REPO = os.path.dirname(HERE)
OUT = os.path.join(REPO, "reports", "recon", "pass2", "pass2_precision_2026-08-29.json")
LOGP = os.path.join(REPO, "reports", "recon", "pass2", "pass2_precision_2026-08-29.log")
DB = "LIBRARY_RAW.LANDING"
N = 60

STOP = set("INC LLC CORP CORPORATION CO COMPANY LTD LIMITED THE OF AND & LP LLP PLC PC NA DBA GROUP HOLDINGS "
           "INCORPORATED L L C TRUST BANK NATIONAL ASSOCIATION FSB SA NV AG GMBH".split())


def norm(s):
    if s is None:
        return ""
    s = re.sub(r"[^A-Z0-9 ]", " ", str(s).upper())
    toks = [t for t in s.split() if t and t not in STOP]
    return " ".join(toks)


def name_match(a, b):
    na, nb = norm(a), norm(b)
    if not na or not nb:
        return None
    if na == nb or na in nb or nb in na:
        return True
    ta, tb = set(na.split()), set(nb.split())
    if ta and tb and len(ta & tb) / len(ta | tb) >= 0.5:
        return True
    if na[:12] == nb[:12]:
        return True
    return False


def q(col):
    return col if re.fullmatch(r"[A-Z_][A-Z0-9_]*", col) else '"' + col + '"'


def K(col, how):
    c = q(col)
    return {
        None: f"NULLIF(TRIM({c}),'')",
        "upper": f"NULLIF(UPPER(TRIM({c})),'')",
        "digits": f"NULLIF(REGEXP_REPLACE({c},'[^0-9]',''),'')",
        "ltrim0": f"NULLIF(LTRIM(REGEXP_REPLACE({c},'[^0-9]',''),'0'),'')",
        "nnum": f"NULLIF(REGEXP_REPLACE(UPPER(TRIM({c})),'^N',''),'')",
        "ndc9l": f"LEFT(NULLIF(REGEXP_REPLACE({c},'[^0-9]',''),''),9)",
        "ndc9r": f"LPAD(SPLIT_PART({c},'-',1),5,'0')||LPAD(SPLIT_PART({c},'-',2),4,'0')",
        "aridstrip": f"NULLIF(LTRIM(SUBSTR(REGEXP_REPLACE({c},'[^0-9]',''),2),'0'),'')",
        "ukch": f"LPAD(NULLIF(TRIM({c}),''),8,'0')",
    }[how]


# (label, left table, left key, left name, left state, right table, right key, right name, right state, norm[, sample_pct_left, sample_pct_right, left_where])
EDGES = [
    ("Drug price NDC -> drug label NDC", "FED_CMS_NADAC", "NDC", "NDC_DESCRIPTION", None, "FED_FDA_NDC_DIRECTORY", "PRODUCTNDC", "PROPRIETARYNAME", None, "ndc9"),
    ("Clinic NPI -> provider registry", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_NPI_NUMBER", "SITE_NAME", "SITE_STATE_ABBREVIATION", "FED_CMS_NPPES", "NPI", "PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME", None, "digits"),
    ("Clinic Medicare billing # -> provider-of-services CCN", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_MEDICARE_BILLING_NUMBER", "SITE_NAME", "SITE_STATE_ABBREVIATION", "FED_CMS_POS_OTHER", "CCN", "FAC_NAME", "STATE_CD", "upper"),
    ("Hospice associate id -> PECOS PAC id", "FED_CMS_HOSPICE_ENROLLMENTS", "ASSOCIATE_ID", "ORGANIZATION_NAME", "STATE", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "ORG_NAME", "STATE_CD", "digits"),
    ("Predecessor CCN -> CCN (lineage; names may differ)", "FED_CMS_POS_OTHER", "CROSS_REF_PROVIDER_NUMBER", "FAC_NAME", "STATE_CD", "FED_CMS_POS_OTHER", "CCN", "FAC_NAME", "STATE_CD", "upper"),
    ("Nursing-home chain id CMS -> 411", "FED_CMS_NURSING_HOME", "CHAIN_ID", "CHAIN_NAME", None, "FED_NURSINGHOME411", "CHAIN_ID", "CHAIN_NAME", None, "digits"),
    ("TRI EPA registry id -> FRS registry", "FED_EPA_TRI_FACILITY", "EPA_REGISTRY_ID", "FACILITY_NAME", "STATE_ABBR", "FED_EPA_FRS_FRS_FACILITIES", "REGISTRY_ID", "FAC_NAME", "FAC_STATE", "digits"),
    ("TRI parent DUNS -> contract recipient DUNS", "FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM", "PARENT_CO_NAME", None, "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "recipient_name", None, "digits", 100, 2),
    ("FDIC successor cert -> cert (lineage; state)", "FED_FDIC_BANK_DATA", "NEWCERT", "NAME", "STALP", "FED_FDIC_BANK_DATA", "CERT", "NAME", "STALP", "ltrim0"),
    ("FHLB member cert -> FDIC cert", "FED_FHFA_FHLB_MEMBERSHIP", "CERT", "MEMBER_NAME", "STATE", "FED_FDIC_BANK_DATA", "CERT", "NAME", "STALP", "ltrim0"),
    ("FHLB member Fed id -> FDIC Fed RSSD", "FED_FHFA_FHLB_MEMBERSHIP", "FED_ID", "MEMBER_NAME", "STATE", "FED_FDIC_BANK_DATA", "FED_RSSD", "NAME", "STALP", "ltrim0"),
    ("FHLB member NCUA id -> credit-union charter", "FED_FHFA_FHLB_MEMBERSHIP", "NCUA_ID", "MEMBER_NAME", "STATE", "FED_NCUA_CALL_REPORTS_FOICU", "CU_NUMBER", "CU_NAME", "STATE", "ltrim0"),
    ("SBA lender FDIC # -> FDIC cert", "FED_SBA_LOANS", "BANKFDICNUMBER", "BANKNAME", "BANKSTATE", "FED_FDIC_BANK_DATA", "CERT", "NAME", "STALP", "ltrim0", 5, 100),
    ("SBA lender NCUA # -> credit-union charter", "FED_SBA_LOANS", "BANKNCUANUMBER", "BANKNAME", "BANKSTATE", "FED_NCUA_CALL_REPORTS_FOICU", "CU_NUMBER", "CU_NAME", "STATE", "ltrim0", 5, 100),
    ("HMDA legacy id (agency-stripped) -> FDIC cert", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "ARID_2017", "RESPONDENT_NAME", None, "FED_FDIC_BANK_DATA", "CERT", "NAME", None, "aridcert"),
    ("HMDA xref LEI -> global LEI registry", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "LEI_2018", "RESPONDENT_NAME", None, "INTL_GLEIF", "LEI", "Entity.LegalName", None, "upper"),
    ("Market-venue LEI -> global LEI registry", "INTL_ISO_MIC_REGISTRY", "LEI", "LEGAL_ENTITY_NAME", None, "INTL_GLEIF", "LEI", "Entity.LegalName", None, "upper"),
    ("LEI national company # (UK) -> Companies House", "INTL_GLEIF", "Entity.RegistrationAuthority.RegistrationAuthorityEntityID", "Entity.LegalName", None, "INT_UK_COMPANIES_HOUSE", "CompanyNumber", "CompanyName", None, "ukch", 100, 100, "WHERE \"Entity.RegistrationAuthority.RegistrationAuthorityID\"='RA000585'"),
    ("Screening-list entity # -> OFAC SDN #", "FED_CONSOLIDATED_SCREENING_LIST", "ENTITY_NUMBER", "NAME", None, "FED_OFAC_SDN", "ENT_NUM", "SDN_NAME", None, "digits"),
    ("UK-sanctioned ship IMO -> OFAC IMO", "INTL_UK_SANCTIONS_LIST", "IMO_NUMBER", "NAME_6", None, "FED_OFAC_SDN", "IMO", "SDN_NAME", None, "digits"),
    ("SAM exclusion NPI -> provider registry (people)", "FED_SAM_EXCLUSIONS_FULL_R2", "NPI", "LAST", "STATE_PROVINCE", "FED_CMS_NPPES", "NPI", "PROVIDER_LAST_NAME_LEGAL_NAME", None, "digits"),
    ("SAM exclusion NPI -> health exclusion list", "FED_SAM_EXCLUSIONS_FULL_R2", "NPI", "LAST", "STATE_PROVINCE", "FED_HHS_OIG_LEIE", "NPI", "LASTNAME", "STATE", "digits"),
    ("ICE stint facility code -> facility codes", "FED_ICE_DETENTION_STINTS", "DETENTION_FACILITY_CODE", "DETENTION_FACILITY", "STATE", "FED_ICE_DETENTION_FACILITY_CODES", "DETENTION_FACILITY_CODE", "DETENTION_FACILITY_NAME", "STATE", "upper", 2, 100),
    ("Crash N-number -> FAA registry (serial #)", "FED_NTSB_AVIATION_AIRCRAFT", "REGIS_NO", "ACFT_SERIAL_NO", None, "FED_FAA_AIRCRAFT_REGISTRY", "N_NUMBER", "SERIAL_NUMBER", None, "nnum"),
    ("Rail parent code -> reporting railroad code", "FED_FRA_CASUALTIES", "REPORTING_PARENT_RAILROAD_CODE", "REPORTING_PARENT_RAILROAD_NAME", None, "FED_FRA_EQUIPMENT_ACCIDENTS", "REPORTING_RAILROAD_CODE", "REPORTING_RAILROAD_NAME", None, "upper", 5, 20),
    ("Subawardee UEI -> SAM registrant", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_UEI", "SUBAWARDEE_NAME", "SUBAWARDEE_STATE_CODE", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", "PHYSICAL_ADDRESS_STATE", "upper", 3, 100),
    ("Grant recipient parent UEI -> SAM registrant", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_parent_uei", "recipient_parent_name", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 2, 100),
    ("Contract recipient parent UEI -> SAM registrant", "FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_PARENT_UEI", "RECIPIENT_PARENT_NAME", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 0.5, 100),
    ("Contract CAGE -> SAM CAGE (pass-1 edge)", "FED_USASPENDING_CONTRACTS_FULL_R2", "CAGE_CODE", "RECIPIENT_NAME", "RECIPIENT_STATE_CODE", "FED_SAM_ENTITY_PUBLIC", "CAGE_CODE", "LEGAL_BUSINESS_NAME", "PHYSICAL_ADDRESS_STATE", "upper", 0.5, 100),
    ("NIH org UEI -> SAM registrant", "FED_NIH_REPORTER", "ORG_UEI", "ORG_NAME", "ORG_STATE", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", "PHYSICAL_ADDRESS_STATE", "upper", 10, 100),
    ("SBIR UEI -> SAM registrant", "FED_SBIR_STTR_AWARDS", "UEI", "COMPANY", "STATE", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", "PHYSICAL_ADDRESS_STATE", "upper"),
    ("Device-maker DUNS -> contract recipient DUNS", "FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER", "COMPANYNAME", None, "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "recipient_name", None, "digits", 5, 2),
    ("Trucker DUNS -> contract recipient DUNS", "FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO", "LEGAL_NAME", "PHY_STATE", "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "recipient_name", "recipient_state_code", "digits", 5, 2),
    ("Transmission owner id -> EIA utility id", "FED_EIA860_2_PLANT", "TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID", "TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER", None, "FED_EIA860_1_UTILITY", "UTILITY_ID", "UTILITY_NAME", None, "digits"),
    ("Plant owner id -> EIA utility id", "FED_EIA860_4_OWNER", "OWNERSHIP_ID", "OWNER_NAME", "OWNER_STATE", "FED_EIA860_1_UTILITY", "UTILITY_ID", "UTILITY_NAME", None, "digits"),
    ("Bill sponsor bioguide -> member roster", "FED_GOVINFO_BILLSTATUS", "SPONSOR_BIOGUIDE", "SPONSOR_NAME", None, "FED_VOTEVIEW_MEMBERS", "BIOGUIDE_ID", "BIONAME", None, "upper"),
    ("Audit issuer CIK -> insider-filing issuer CIK", "FED_PCAOB_FORM_AP_FILINGS", "ISSUER_CIK", "ISSUER_NAME", None, "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "ISSUERNAME", None, "ltrim0", 20, 10),
    ("EPA crosswalk parent UEI -> SAM registrant", "XC_EPA_CORPORATE_CROSSWALK", "PARENT_UEI", "PARENT_LEGAL_NAME", None, "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "LEGAL_BUSINESS_NAME", None, "upper", 5, 100),
    ("US-documented vessel IMO -> AIS IMO (pass-1 edge)", "FED_USCG_VESSEL_DOCUMENTATION", "IMO_NUMBER", "VESSEL_NAME", None, "FED_NOAA_AIS", "IMO", "VESSELNAME", None, "digits", 100, 0.2),
    ("US-documented call sign -> AIS call sign (pass-1 edge)", "FED_USCG_VESSEL_DOCUMENTATION", "CALL_SIGN", "VESSEL_NAME", None, "FED_NOAA_AIS", "CALLSIGN", "VESSELNAME", None, "upper", 100, 0.2),
    ("Committee's candidate id -> FEC candidate (office state)", "FED_FEC_BULK_COMMITTEES", "FEC_CAND_ID", "CMTE_NM", "CMTE_ST", "FED_FEC_BULK_CANDIDATES", "CAND_ID", "CAND_NAME", "CAND_OFFICE_ST", "upper"),
]


def keyexpr(col, how, side):
    if how == "ndc9":
        return K(col, "ndc9l" if side == "l" else "ndc9r")
    if how == "aridcert":
        return K(col, "aridstrip" if side == "l" else "ltrim0")
    if how == "ukch":
        return K(col, "ukch")
    return K(col, how)


def sample_sql(e):
    label, lt, lk, ln, ls, rt, rk, rn, rs, how = e[:10]
    lp = e[10] if len(e) > 10 else 100
    rp = e[11] if len(e) > 11 else 100
    lw = e[12] if len(e) > 12 else ""
    def side(t, k, n, s, pct, how_side, where):
        samp = f" SAMPLE ({pct})" if pct < 100 else ""
        scol = q(s) if s else "NULL"
        return (f"SELECT {keyexpr(k, how, how_side)} AS v, {q(n)} AS nm, {scol} AS st FROM {DB}.{t}{samp} {where} "
                f"QUALIFY ROW_NUMBER() OVER (PARTITION BY v ORDER BY RANDOM()) = 1")
    return f"""
    WITH l AS ({side(lt, lk, ln, ls, lp, 'l', lw)}), r AS ({side(rt, rk, rn, rs, rp, 'r', '')})
    SELECT l.v, l.nm, l.st, r.nm, r.st FROM l JOIN r USING (v)
    WHERE l.v IS NOT NULL AND l.v <> '0' ORDER BY RANDOM() LIMIT {N}"""


def main():
    log = open(LOGP, "a", encoding="utf-8")
    def L(m):
        line = f"{time.strftime('%H:%M:%S')} {m}"; print(line, flush=True); log.write(line + "\n"); log.flush()
    conn = sf.connect(); cur = conn.cursor()
    cur.execute("ALTER SESSION SET QUERY_TAG='pass2_precision_2026_08_29'")
    cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 600")
    out = []
    L(f"{len(EDGES)} edges, {N} pairs each")
    for i, e in enumerate(EDGES, 1):
        label = e[0]
        try:
            cur.execute(sample_sql(e)); rows = cur.fetchall()
            nm = [name_match(r[1], r[3]) for r in rows]
            scored = [x for x in nm if x is not None]
            st = [(r[2] or "").strip().upper() == (r[4] or "").strip().upper() for r in rows if r[2] and r[4]]
            miss = [(r[0], str(r[1])[:40], str(r[3])[:40]) for r, m in zip(rows, nm) if m is False][:3]
            res = dict(label=label, pairs=len(rows), name_scored=len(scored),
                       name_match_pct=round(100 * sum(scored) / len(scored), 1) if scored else None,
                       state_scored=len(st), state_match_pct=round(100 * sum(st) / len(st), 1) if st else None,
                       mismatches=miss)
            out.append(res)
            L(f"[{i}] {label}: names {res['name_match_pct']}% of {len(scored)} | states {res['state_match_pct']}% of {len(st)} | e.g. {miss[:1]}")
        except Exception as ex:  # noqa: BLE001
            out.append(dict(label=label, error=str(ex)[:300])); L(f"[{i}] ERR {label}: {str(ex)[:200]}")
        json.dump(out, open(OUT, "w", encoding="utf-8"), indent=1, default=str)
    L("DONE")


if __name__ == "__main__":
    main()
