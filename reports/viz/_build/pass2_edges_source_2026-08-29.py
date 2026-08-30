"""Source of truth for the pass-2 connections (measured live 2026-08-29, not yet in the spine).

Running this file writes handbook_pass2_edges_2026-08-29.csv next to it. Numbers come from
reports/recon/pass2/pass2_live_check_2026-08-29.json, the level-3 precision check
(pass2_precision_2026-08-29.json), and seven follow-up overlap counts re-run 2026-08-29 late
(handbook session). Edit here, re-run, then rebuild the handbook:

    python reports/viz/_build/pass2_edges_source_2026-08-29.py
    python reports/viz/_build/build_join_handbook.py
    python reports/viz/_build/build_join_handbook_md.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import json

HERE = Path(__file__).resolve().parent
OUT = HERE / "handbook_pass2_edges_2026-08-29.csv"
PRECISION = HERE.parents[2] / "reports" / "recon" / "pass2" / "pass2_precision_2026-08-29.json"

L2 = "level 2 only (overlap measured live; matched pairs not name-checked)"
rows: list[dict] = []
MEASURED_ON = "2026-08-29"


def e(a, ca, b, cb, key, matched, da, db, rate, verdict, note="", tier="MEASURED", norm=""):
    rows.append(dict(table_a=a, table_b=b, key=key, tier=tier, col_a=ca, col_b=cb, matched=matched,
                     distinct_a=da, distinct_b=db, match_rate=rate, verdict=verdict, note=note, norm=norm,
                     measured_on=MEASURED_ON, pairs="", names_pct="", states_pct=""))


# Level-3 name/state spot-check (60 random matched pairs per edge, 2026-08-29 23:14): which
# precision-check label belongs to which column pair. Loaded from the JSON at write time.
PRECISION_PAIRS = {
    "Drug price NDC -> drug label NDC": ("FED_CMS_NADAC.NDC", "FED_FDA_NDC_DIRECTORY.PRODUCTNDC"),
    "Clinic NPI -> provider registry": ("FED_HRSA_UDS_SERVICE_DELIVERY_SITES.FQHC_SITE_NPI_NUMBER", "FED_CMS_NPPES.NPI"),
    "Clinic Medicare billing # -> provider-of-services CCN": ("FED_HRSA_UDS_SERVICE_DELIVERY_SITES.FQHC_SITE_MEDICARE_BILLING_NUMBER", "FED_CMS_POS_OTHER.CCN"),
    "Hospice associate id -> PECOS PAC id": ("FED_CMS_HOSPICE_ENROLLMENTS.ASSOCIATE_ID", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT.PECOS_ASCT_CNTL_ID"),
    "Predecessor CCN -> CCN (lineage; names may differ)": ("FED_CMS_POS_OTHER.CROSS_REF_PROVIDER_NUMBER", "FED_CMS_POS_OTHER.CCN"),
    "Nursing-home chain id CMS -> 411": ("FED_CMS_NURSING_HOME.CHAIN_ID", "FED_NURSINGHOME411.CHAIN_ID"),
    "TRI EPA registry id -> FRS registry": ("FED_EPA_TRI_FACILITY.EPA_REGISTRY_ID", "FED_EPA_FRS_FRS_FACILITIES.REGISTRY_ID"),
    "TRI parent DUNS -> contract recipient DUNS": ("FED_EPA_TRI_FACILITY.PARENT_CO_DB_NUM", "FED_USASPENDING_CONTRACTS_FULL.recipient_duns"),
    "FDIC successor cert -> cert (lineage; state)": ("FED_FDIC_BANK_DATA.NEWCERT", "FED_FDIC_BANK_DATA.CERT"),
    "FHLB member cert -> FDIC cert": ("FED_FHFA_FHLB_MEMBERSHIP.CERT", "FED_FDIC_BANK_DATA.CERT"),
    "FHLB member Fed id -> FDIC Fed RSSD": ("FED_FHFA_FHLB_MEMBERSHIP.FED_ID", "FED_FDIC_BANK_DATA.FED_RSSD"),
    "FHLB member NCUA id -> credit-union charter": ("FED_FHFA_FHLB_MEMBERSHIP.NCUA_ID", "FED_NCUA_CALL_REPORTS_FOICU.CU_NUMBER"),
    "SBA lender FDIC # -> FDIC cert": ("FED_SBA_LOANS.BANKFDICNUMBER", "FED_FDIC_BANK_DATA.CERT"),
    "SBA lender NCUA # -> credit-union charter": ("FED_SBA_LOANS.BANKNCUANUMBER", "FED_NCUA_CALL_REPORTS_FOICU.CU_NUMBER"),
    "HMDA legacy id (agency-stripped) -> FDIC cert": ("FED_CFPB_HMDA_ARID2017_LEI_XREF.ARID_2017", "FED_FDIC_BANK_DATA.CERT"),
    "HMDA xref LEI -> global LEI registry": ("FED_CFPB_HMDA_ARID2017_LEI_XREF.LEI_2018", "INTL_GLEIF.LEI"),
    "Market-venue LEI -> global LEI registry": ("INTL_ISO_MIC_REGISTRY.LEI", "INTL_GLEIF.LEI"),
    "LEI national company # (UK) -> Companies House": ("INTL_GLEIF.Entity.RegistrationAuthority.RegistrationAuthorityEntityID", "INT_UK_COMPANIES_HOUSE.CompanyNumber"),
    "Screening-list entity # -> OFAC SDN #": ("FED_CONSOLIDATED_SCREENING_LIST.ENTITY_NUMBER", "FED_OFAC_SDN.ENT_NUM"),
    "UK-sanctioned ship IMO -> OFAC IMO": ("INTL_UK_SANCTIONS_LIST.IMO_NUMBER", "FED_OFAC_SDN.IMO"),
    "SAM exclusion NPI -> provider registry (people)": ("FED_SAM_EXCLUSIONS_FULL_R2.NPI", "FED_CMS_NPPES.NPI"),
    "SAM exclusion NPI -> health exclusion list": ("FED_SAM_EXCLUSIONS_FULL_R2.NPI", "FED_HHS_OIG_LEIE.NPI"),
    "ICE stint facility code -> facility codes": ("FED_ICE_DETENTION_STINTS.DETENTION_FACILITY_CODE", "FED_ICE_DETENTION_FACILITY_CODES.DETENTION_FACILITY_CODE"),
    "Crash N-number -> FAA registry (serial #)": ("FED_NTSB_AVIATION_AIRCRAFT.REGIS_NO", "FED_FAA_AIRCRAFT_REGISTRY.N_NUMBER"),
    "Rail parent code -> reporting railroad code": ("FED_FRA_CASUALTIES.REPORTING_PARENT_RAILROAD_CODE", "FED_FRA_EQUIPMENT_ACCIDENTS.REPORTING_RAILROAD_CODE"),
    "Subawardee UEI -> SAM registrant": ("FED_USASPENDING_SUBAWARDS_FULL.SUBAWARDEE_UEI", "FED_SAM_ENTITY_PUBLIC.UEI_SAM"),
    "Grant recipient parent UEI -> SAM registrant": ("FED_USASPENDING_ASSISTANCE_FULL.recipient_parent_uei", "FED_SAM_ENTITY_PUBLIC.UEI_SAM"),
    "Contract recipient parent UEI -> SAM registrant": ("FED_USASPENDING_CONTRACTS_FULL_R2.RECIPIENT_PARENT_UEI", "FED_SAM_ENTITY_PUBLIC.UEI_SAM"),
    "Contract CAGE -> SAM CAGE (pass-1 edge)": ("FED_USASPENDING_CONTRACTS_FULL_R2.CAGE_CODE", "FED_SAM_ENTITY_PUBLIC.CAGE_CODE"),
    "NIH org UEI -> SAM registrant": ("FED_NIH_REPORTER.ORG_UEI", "FED_SAM_ENTITY_PUBLIC.UEI_SAM"),
    "SBIR UEI -> SAM registrant": ("FED_SBIR_STTR_AWARDS.UEI", "FED_SAM_ENTITY_PUBLIC.UEI_SAM"),
    "Device-maker DUNS -> contract recipient DUNS": ("FED_FDA_GUDID_FULL_DEVICE.DUNSNUMBER", "FED_USASPENDING_CONTRACTS_FULL.recipient_duns"),
    "Trucker DUNS -> contract recipient DUNS": ("FED_FMCSA_COMPANY_CENSUS.DUN_BRADSTREET_NO", "FED_USASPENDING_CONTRACTS_FULL.recipient_duns"),
    "Transmission owner id -> EIA utility id": ("FED_EIA860_2_PLANT.TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID", "FED_EIA860_1_UTILITY.UTILITY_ID"),
    "Plant owner id -> EIA utility id": ("FED_EIA860_4_OWNER.OWNERSHIP_ID", "FED_EIA860_1_UTILITY.UTILITY_ID"),
    "Bill sponsor bioguide -> member roster": ("FED_GOVINFO_BILLSTATUS.SPONSOR_BIOGUIDE", "FED_VOTEVIEW_MEMBERS.BIOGUIDE_ID"),
    "Audit issuer CIK -> insider-filing issuer CIK": ("FED_PCAOB_FORM_AP_FILINGS.ISSUER_CIK", "FED_SEC_INSIDER_SUBMISSION.ISSUERCIK"),
    "EPA crosswalk parent UEI -> SAM registrant": ("XC_EPA_CORPORATE_CROSSWALK.PARENT_UEI", "FED_SAM_ENTITY_PUBLIC.UEI_SAM"),
    "US-documented vessel IMO -> AIS IMO (pass-1 edge)": ("FED_USCG_VESSEL_DOCUMENTATION.IMO_NUMBER", "FED_NOAA_AIS.IMO"),
    "US-documented call sign -> AIS call sign (pass-1 edge)": ("FED_USCG_VESSEL_DOCUMENTATION.CALL_SIGN", "FED_NOAA_AIS.CALLSIGN"),
    "Committee's candidate id -> FEC candidate (office state)": ("FED_FEC_BULK_COMMITTEES.FEC_CAND_ID", "FED_FEC_BULK_CANDIDATES.CAND_ID"),
}


PRECISION_HMDA = PRECISION.parent / "hmda_split_precision_2026-08-30.json"
PRECISION_PAIRS_HMDA = {
    "Old-HMDA id, bank-regulator rows (agency 1-3) -> FDIC cert": ("FED_CFPB_HMDA_HISTORIC.RESPONDENT_ID", "FED_FDIC_BANK_DATA.CERT"),
    "Old-HMDA id, HUD rows (agency 7) -> Form 5500 sponsor EIN": ("FED_CFPB_HMDA_HISTORIC.RESPONDENT_ID", "FED_DOL_FORM5500_FULL.SPONS_DFE_EIN"),
}


def attach_precision(rows):
    """Stamp pairs / names_pct / states_pct onto the rows the level-3 checks covered."""
    res = {r["label"]: r for r in json.loads(PRECISION.read_text(encoding="utf-8")) if "error" not in r}
    pairs = dict(PRECISION_PAIRS)
    if PRECISION_HMDA.exists():
        res.update({r["label"]: r for r in json.loads(PRECISION_HMDA.read_text(encoding="utf-8"))})
        pairs.update(PRECISION_PAIRS_HMDA)
    by_pair = {}
    for label, (l, r) in pairs.items():
        if label in res:
            by_pair[frozenset((l, r))] = res[label]
    hit = 0
    for row in rows:
        k = frozenset((f"{row['table_a']}.{row['col_a']}", f"{row['table_b']}.{row['col_b']}"))
        p = by_pair.get(k)
        if p:
            row["pairs"] = p["name_scored"] or p["pairs"]
            row["names_pct"] = p["name_match_pct"] if p["name_match_pct"] is not None else ""
            row["states_pct"] = p["state_match_pct"] if p.get("state_match_pct") is not None else ""
            hit += 1
    return hit


# --- health / pharma / devices
e("FED_CMS_NADAC", "NDC", "FED_FDA_NDC_DIRECTORY", "PRODUCTNDC", "NDC9", 17958, 21866, 114649, 82.1, "SOLID",
  "only joins after both sides are padded to 5-4 digits (labeler-product); a raw string join gives 0%", "MEASURED", "ndc9")
e("FED_FDA_GUDID_FULL_DEVICE", "PRIMARYDI", "FED_FDA_GUDID_FULL_IDENTIFIERS", "PRIMARYDI", "UDI_DI", 5182695, 5182695, 5182695, 100.0, L2,
  "same publisher, two files; the partner files (MAUDE adverse events, device recalls) are not loaded yet")
e("FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER", "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "DUNS", 2096, 12272, 357876, 17.1, "SOLID",
  "device makers that are also federal contractors")
e("FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_NPI_NUMBER", "FED_CMS_NPPES", "NPI", "NPI", 6003, 6048, 9606683, 99.3, "SOLID (site -> parent org)",
  "the clinic row carries its parent organization's NPI, so names differ site vs org; only 32% of sites carry one")
e("FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_MEDICARE_BILLING_NUMBER", "FED_CMS_POS_OTHER", "CCN", "CCN", 7559, 8422, 44429, 89.8, "SOLID (site -> parent org)",
  "states agree 100%; site name vs org name")
e("FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER", "FED_HRSA_UDS_HEALTH_CENTER_INFO", "BHCMISID", "BHCMIS", 1344, 1525, 1356, 88.1, L2,
  "grantee <-> its sites")
e("FED_CMS_HOSPICE_ENROLLMENTS", "ASSOCIATE_ID", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 5003, 5372, 2456135, 93.1, "SOLID",
  "hospices join the PECOS ownership axis")
e("FED_CMS_POS_OTHER", "CROSS_REF_PROVIDER_NUMBER", "FED_CMS_POS_OTHER", "CCN", "CCN", 5405, 5557, 44429, 97.3, "SOLID (lineage)",
  "predecessor facility number -> current number; names differ by design, states agree 100%")
e("FED_CMS_NURSING_HOME", "CHAIN_ID", "FED_NURSINGHOME411", "CHAIN_ID", "CHAIN_ID", 576, 635, 617, 90.7, "SOLID",
  "chain = owner group; there is no chain master table, names only")
# --- environment
e("FED_EPA_TRI_FACILITY", "EPA_REGISTRY_ID", "FED_EPA_FRS_FRS_FACILITIES", "REGISTRY_ID", "FRS_ID", 64631, 64728, 3277557, 99.9, "SOLID (site key, name drift)",
  "use this column, NOT the dead FRS_ID column on the same table; name mismatches are ownership changes at the same site")
e("FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM", "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "DUNS", 2103, 10733, 357876, 19.6, "SOLID",
  "polluter's parent company -> federal contractor")
e("FED_USCG_NRC_INCIDENT_REPORTS", "SEQNOS", "FED_USCG_NRC_INCIDENTS", "SEQNOS", "NRC_SEQ", 116662, 116662, 1029020, 100.0, L2,
  "report detail -> the incident it describes")
# --- banking / housing
e("FED_FDIC_BANK_DATA", "NEWCERT", "FED_FDIC_BANK_DATA", "CERT", "FDIC_CERT", 7942, 7952, 27836, 99.9, "SOLID (lineage)",
  "successor bank pointer; the successor is a different bank by definition, states agree 90%")
e("FED_FDIC_BANK_DATA", "ULTCERT", "FED_FDIC_BANK_DATA", "CERT", "FDIC_CERT", 5191, 5199, 27836, 99.8, L2, "ultimate-parent bank pointer")
e("FED_FDIC_BANK_DATA", "PARCERT", "FED_FDIC_BANK_DATA", "CERT", "FDIC_CERT", 49, 49, 27836, 100.0, L2, "direct-parent bank pointer (tiny)")
e("FED_FDIC_BANK_DATA", "RSSDHCR", "FED_FDIC_SOD_BRANCH_DEPOSITS", "RSSDHCR", "RSSD_HC", 7243, 8736, 9728, 82.9, L2,
  "both sides are holding-company pointers; the holding-company master (Fed NIC file) is NOT held, so neither resolves to a name")
e("FED_FHFA_FHLB_MEMBERSHIP", "CERT", "FED_FDIC_BANK_DATA", "CERT", "FDIC_CERT", 3983, 3984, 27836, 100.0, "SOLID")
e("FED_FHFA_FHLB_MEMBERSHIP", "FED_ID", "FED_FDIC_BANK_DATA", "FED_RSSD", "RSSD", 3976, 3984, 26577, 99.8, "SOLID")
e("FED_FHFA_FHLB_MEMBERSHIP", "NCUA_ID", "FED_NCUA_CALL_REPORTS_FOICU", "CU_NUMBER", "NCUA_CHARTER", 1618, 1638, 4336, 98.8, "SOLID",
  "strip leading zeros on both sides")
e("FED_SBA_LOANS", "BANKFDICNUMBER", "FED_FDIC_BANK_DATA", "CERT", "FDIC_CERT", 3938, 3950, 27836, 99.7, "SOLID", "SBA lender -> bank")
e("FED_SBA_LOANS", "BANKNCUANUMBER", "FED_NCUA_CALL_REPORTS_FOICU", "CU_NUMBER", "NCUA_CHARTER", 570, 589, 4336, 96.8, "SOLID",
  "SBA lender -> credit union; strip leading zeros")
e("FED_CFPB_HMDA_ARID2017_LEI_XREF", "LEI_2018", "INTL_GLEIF", "LEI", "LEI", 5397, 5399, 3382301, 100.0, "SOLID",
  "the official old-HMDA-id -> LEI bridge; the safe route into pre-2018 HMDA")
e("FED_CFPB_HMDA_ARID2017_LEI_XREF", "ARID_2017", "FED_FDIC_BANK_DATA", "CERT", "HMDA_ARID", 2522, 5322, 27836, 47.4,
  "SUSPECT: about half the matched pairs are different banks",
  "the old respondent id is only a bank certificate # for some regulators (agency codes 1-3); for others it is something else. "
  "Do NOT use until split by agency; go through the LEI crosswalk instead", "SUSPECT", "aridcert")
e("FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "SPONSOR_NUMBER", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "ORIGINATING_MORTGAGEE_NUMBER", "FHA_MORTGAGEE", 120, 147, 961, 81.6, L2,
  "sponsor lender -> originating lender (same file)")
# --- securities / corporate
e("FED_SEC_MONEY_MARKET_FUND_INFORMATION", "SERIES_ID", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "SERIES_ID", "SEC_SERIES_ID", 314, 320, 19340, 98.1, L2,
  "money-market fund -> its registered series")
e("FED_PCAOB_FORM_AP_FILINGS", "ISSUER_CIK", "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "CIK", 9844, 28775, 10401, 34.2, "SOLID",
  "audit engagement -> the audited company's insider filings; misses are corporate renames under the same CIK")
e("INTL_ISO_MIC_REGISTRY", "LEI", "INTL_GLEIF", "LEI", "LEI", 1059, 1061, 3382301, 99.8, "SOLID", "trading venue -> its legal entity")
e("FED_CONSOLIDATED_SCREENING_LIST", "ENTITY_NUMBER", "FED_OFAC_SDN", "ENT_NUM", "OFAC_ENT_NUM", 18985, 19637, 19114, 96.7, "SOLID",
  "same number system; the screening list is the SDN list plus other agencies' lists")
e("INTL_UK_SANCTIONS_LIST", "IMO_NUMBER", "FED_OFAC_SDN", "IMO", "IMO", 291, 663, 2030, 43.9, "SOLID (hull key, name drift)",
  "sanctioned ships get renamed; the IMO hull number never changes")
e("INTL_GLEIF", "Entity.SuccessorEntity.1.SuccessorLEI", "INTL_GLEIF", "LEI", "LEI", 27279, 27279, 3382301, 100.0, L2,
  "entity lineage pointer (same file)")
e("INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_STARTNODE_NODEID", "INTL_GLEIF", "LEI", "LEI", 299509, 301482, 3382301, 99.3, L2,
  "child company in the corporate parent tree (Level 2): ultimate parent 132.6K, direct parent 126.4K, fund-managed 149.4K, subfund 73.2K, branch 1.9K")
e("INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_ENDNODE_NODEID", "INTL_GLEIF", "LEI", "LEI", 77108, 77251, 3382301, 99.8, L2,
  "parent company in the corporate parent tree (Level 2)")
e("INTL_GLEIF", "Entity.RegistrationAuthority.RegistrationAuthorityEntityID", "INT_UK_COMPANIES_HOUSE", "CompanyNumber", "COMPANY_NO", 94652, 110426, 5734779, 85.7, "SOLID",
  "UK-registered rows only (registration authority RA000585); pad the number to 8 digits. "
  "132,901 Delaware file numbers sit in the same column with no Delaware registry to receive them", "MEASURED", "ukch")
e("XC_EPA_CORPORATE_CROSSWALK", "ULTIMATE_PARENT_LEI", "INTL_GLEIF", "LEI", "LEI", 1174, 1174, 3382301, 100.0, L2, "0.7% of crosswalk rows carry one")
e("XC_EPA_CORPORATE_CROSSWALK", "PARENT_CIK", "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "CIK", 662, 704, 10401, 94.0, L2, "2.3% of crosswalk rows carry one")
e("XC_EPA_CORPORATE_CROSSWALK", "PARENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 17373, 31685, 887310, 54.8, "SOLID (n=6 sampled)", "8.1% of crosswalk rows carry one")
e("FED_FMCSA_COMPANY_CENSUS", "PRIOR_REVOKE_DOT_NUMBER", "FED_FMCSA_COMPANY_CENSUS", "DOT_NUMBER", "USDOT", 555, 556, 4493662, 99.8, L2,
  "reincorporation pointer; only 557 carriers carry one")
e("FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO", "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "DUNS", 13089, 372260, 357876, 3.5, "SOLID",
  "86% of carriers report DUNS 0 -- those are not junk rows, the 372K real values are fine; states agree 80% (HQ vs place of performance)")
e("FED_SAM_EXCLUSIONS_FULL_R2", "NPI", "FED_CMS_NPPES", "NPI", "NPI", 4854, 4867, 9606683, 99.7, "SOLID", "excluded people -> the provider registry")
e("FED_SAM_EXCLUSIONS_FULL_R2", "NPI", "FED_HHS_OIG_LEIE", "NPI", "NPI", 4688, 4867, 8661, 96.3, "SOLID", "the two federal exclusion lists agree on NPI")
e("FED_OSHA_ITA_300A_SUMMARY_2024", "EIN", "FED_DOL_FORM5500_FULL", "SPONS_DFE_EIN", "EIN", 31883, 114605, 466446, 27.8, L2,
  "injury logs <-> benefit plans by employer tax id; use the FULL 5500 table, the 33K sample's EIN column is empty")
e("FED_OSHA_ITA_300A_SUMMARY_2024", "EIN", "FED_IRS_BMF", "EIN", "EIN", 6414, 114605, 1974830, 5.6, L2,
  "few employers are nonprofits, so low overlap is expected")
e("FED_OSHA_ITA_300A_SUMMARY_2024", "ESTABLISHMENT_ID", "FED_OSHA_ITA_300A_SUMMARY_2023", "ESTABLISHMENT_ID", "OSHA_EST_ID", 219860, 398620, 394231, 55.2, L2,
  "the same workplace across two years of injury summaries")
# --- justice / transport / procurement / politics
e("FED_ICE_DETENTION_STINTS", "DETENTION_FACILITY_CODE", "FED_ICE_DETENTION_FACILITY_CODES", "DETENTION_FACILITY_CODE", "ICE_FACILITY", 705, 707, 1490, 99.7, "SOLID",
  "name mismatches are facility aliases; states agree 100%")
e("FED_COURTLISTENER_POSITIONS", "PREDECESSOR_ID", "FED_COURTLISTENER_JUDGES", "ID", "CL_PERSON_ID", 139, 139, 16191, 100.0, L2, "the judge this one replaced (tiny)")
e("FED_COURTLISTENER_POSITIONS", "SUPERVISOR_ID", "FED_COURTLISTENER_JUDGES", "ID", "CL_PERSON_ID", 130, 130, 16191, 100.0, L2, "supervising judge (tiny)")
e("FED_COURTLISTENER_COURTS", "PARENT_COURT_ID", "FED_COURTLISTENER_COURTS", "ID", "CL_COURT_ID", 128, 128, 3361, 100.0, L2, "parent court pointer")
e("FED_NTSB_AVIATION_AIRCRAFT", "REGIS_NO", "FED_FAA_AIRCRAFT_REGISTRY", "N_NUMBER", "N_NUMBER", 13528, 30249, 315447, 44.7, "SOLID",
  "the registry is current owners only, so old crashes miss; serial numbers agree 90%, the rest are reissued tail numbers", "MEASURED", "nnum")
e("FED_FRA_CASUALTIES", "REPORTING_PARENT_RAILROAD_CODE", "FED_FRA_EQUIPMENT_ACCIDENTS", "REPORTING_RAILROAD_CODE", "RR_CODE", 770, 1091, 1030, 70.6, "SOLID",
  "parent railroad -> reporting railroad")
e("FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_FAIN", "FED_USASPENDING_ASSISTANCE_FULL", "award_id_fain", "FAIN", 94073, 168225, 10319582, 55.9, L2,
  "subaward -> the grant it came from")
e("FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 148253, 220704, 887310, 67.2, "SOLID")
e("FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_PARENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 50415, 74245, 887310, 67.9, L2, "subrecipient's parent company")
e("FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_PARENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 178303, 563618, 887310, 31.6, "SOLID",
  "contractor's parent company; older UEIs are missing from the current SAM file, hence the low rate")
e("FED_USASPENDING_ASSISTANCE_FULL", "recipient_parent_uei", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 39436, 53380, 887310, 73.9, "SOLID", "grant recipient's parent company")
e("FED_USASPENDING_ASSISTANCE_FULL", "recipient_uei", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 123076, 223721, 887310, 55.0, L2, "grant recipient")
e("FED_USASPENDING_CONTRACTS_FULL_R2", "CAGE_CODE", "FED_SAM_ENTITY_PUBLIC", "CAGE_CODE", "CAGE", 85857, 92530, 794845, 92.8, "SOLID",
  "pass-1 edge, name-checked in pass 2; 1 in 60 is a CAGE reassigned to a new firm")
e("FED_NIH_REPORTER", "ORG_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 9643, 12050, 887310, 80.0, "SOLID",
  "misses are affiliates registered under a sibling legal name")
e("FED_SBIR_STTR_AWARDS", "UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 12144, 17161, 887310, 70.8, "SOLID",
  "names agree 98%; the SBIR 'state' column is NOT a state code (0% agreement) -- a column-meaning trap, not a key problem")
e("FED_SBIR_STTR_AWARDS", "CONTRACT", "FED_USASPENDING_CONTRACTS_FULL_R2", "AWARD_ID_PIID", "PIID", 14530, 156776, 63135848, 9.3, L2,
  "SBIR contract number -> the contract record")
e("FED_SBIR_STTR_AWARDS", "AGENCY_TRACKING_NUMBER", "FED_NIH_REPORTER", "CORE_PROJECT_NUM", "NIH_PROJECT", 16831, 171223, 439228, 9.8, L2,
  "SBIR tracking number -> NIH project")
e("FED_EIA860_2_PLANT", "TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID", "FED_EIA860_1_UTILITY", "UTILITY_ID", "EIA_UTILITY_ID", 553, 1080, 6643, 51.2, "SOLID",
  "owners are often not utilities, hence half resolve")
e("FED_EIA860_4_OWNER", "OWNERSHIP_ID", "FED_EIA860_1_UTILITY", "UTILITY_ID", "EIA_UTILITY_ID", 305, 1945, 6643, 15.7, "SOLID",
  "plant owners are mostly non-utilities; no owner master held")
e("FED_GOVINFO_BILLSTATUS", "SPONSOR_BIOGUIDE", "FED_VOTEVIEW_MEMBERS", "BIOGUIDE_ID", "BIOGUIDE", 632, 632, 12584, 100.0, "SOLID",
  "nickname vs legal first name explains the name misses")
e("FED_FEC_BULK_COMMITTEES", "FEC_CAND_ID", "FED_FEC_BULK_CANDIDATES", "CAND_ID", "FEC_CAND_ID", 6908, 6921, 13240, 99.8, "SOLID (by construction)",
  "committee -> the candidate it supports; office state agrees 90%")
e("FED_NOAA_AIS", "IMO", "FED_USCG_VESSEL_DOCUMENTATION", "IMO_NUMBER", "IMO", 2313, 6934, 6304, 33.4, "SOLID",
  "pass-1 edge, name-checked in pass 2; a third of AIS ships are US-documented vessels")
e("FED_NOAA_AIS", "CALLSIGN", "FED_USCG_VESSEL_DOCUMENTATION", "CALL_SIGN", "CALLSIGN", 5759, 17437, 75450, 33.0, "SOLID",
  "pass-1 edge, name-checked in pass 2")

# --- the 2026-08-29 bank / PECOS / power-plant / award-key batch (bucket B): measured live, staged in code, NOT in the spine
#     source: reports/recon/bucket_b_verify_2026-08-29.json + bucket_b_verify2_2026-08-29.json
FFS = "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT"
e("FED_CMS_FACILITY_AFFILIATION", "IND_PAC_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 937541, 940364, 2456135, 99.7, L2,
  "the clinician-to-facility affiliation file keys on the same PECOS owner/associate id as the enrollment file")
e("FED_CMS_HOSPITAL_ENROLLMENTS", "ASSOCIATE_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 5264, 5280, 2456135, 99.7, L2)
e("FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "ASSOCIATE_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 12042, 12218, 2456135, 98.6, L2)
e("FED_CMS_HOSPITAL_ENROLLMENTS", "ENROLLMENT_ID", FFS, "ENRLMT_ID", "PECOS_ENRLMT", 9103, 9175, 2978925, 99.2, L2,
  "enrollment record -> the same record in the master enrollment file")
e("FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_UNIQUE_KEY", "FED_USASPENDING_CONTRACTS_FULL_R2", "CONTRACT_AWARD_UNIQUE_KEY", "AWARD_KEY",
  110195, 279553, 74488536, 39.4, L2, "subaward -> the prime contract it came from; the contracts copy stops at FY2021, hence the low rate")
e("FED_SAM_EXCLUSIONS_FULL_R2", "CAGE", "FED_USASPENDING_CONTRACTS_FULL_R2", "CAGE_CODE", "CAGE", 182, 392, 246832, 46.4, L2,
  "debarred firms that also show up as contractors; only 435 of 168K exclusion rows carry a CAGE, so the exclusions side is thin")
e("FED_FDIC_SOD_BRANCH_DEPOSITS", "CERT", "FED_FDIC_BANK_DATA", "CERT", "FDIC_CERT", 15497, 15505, 27836, 99.9, L2,
  "branch -> its bank; strip leading zeros on both sides")
e("FED_FDIC_SOD_BRANCH_DEPOSITS", "RSSDID", "FED_FDIC_BANK_DATA", "FED_RSSD", "RSSD", 15304, 15544, 26578, 98.5, L2, "branch -> its bank by Fed id")
e("FED_EPA_EGRID_PLANT_2022", "DOE_EIA_ORIS_PLANT_OR_FACILITY_CODE", "FED_EIA860_2_PLANT", "PLANT_CODE", "EIA_PLANT_ID", 11802, 11974, 16132, 98.6, L2,
  "emissions plant -> the EIA plant master; the EIA plant code and the EPA ORIS code are the same number")
e("FED_EIA860_3_1_GENERATOR", "PLANT_CODE", "FED_EIA860_2_PLANT", "PLANT_CODE", "EIA_PLANT_ID", 13370, 13371, 16132, 100.0, L2, "generator -> its plant")
e("FED_EIA860_4_OWNER", "PLANT_CODE", "FED_EIA860_2_PLANT", "PLANT_CODE", "EIA_PLANT_ID", 2329, 2329, 16132, 100.0, L2, "plant owner row -> its plant")
e("FED_EIA860_2_PLANT", "UTILITY_ID", "FED_EIA860_1_UTILITY", "UTILITY_ID", "EIA_UTILITY_ID", 6640, 6640, 6643, 100.0, L2, "plant -> the utility that operates it")
e("FED_EPA_EGRID_PLANT_2022", "UTILITY_ID", "FED_EIA860_1_UTILITY", "UTILITY_ID", "EIA_UTILITY_ID", 4842, 5120, 6643, 94.6, L2, "emissions plant -> its utility")
e("FED_EIA861_UTILITY_DATA", "UTILITY_NUMBER", "FED_EIA860_1_UTILITY", "UTILITY_ID", "EIA_UTILITY_ID", 373, 1699, 6643, 22.0, L2,
  "same id system, different reporting universe (861 = retail sellers, 860 = plant operators), so low overlap is expected")

# --- follow-ups measured 2026-08-30 (numbers the 08-29 reports quoted but never logged; now in
#     reports/recon/pass2/handbook_followups_2026-08-30.json)
MEASURED_ON = "2026-08-30"
e("FED_EPA_CAMPD_FACILITY", "FACILITY_ID", "FED_EIA860_2_PLANT", "PLANT_CODE", "EIA_PLANT_ID", 1587, 1959, 16132, 81.0, L2,
  "smokestack-monitored units -> the EIA plant master; the 19% that miss are retired or non-EIA units. Emissions (16.5M unit-days) ride on the same id", "MEASURED", "int")
e("FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 192931, 582656, 887310, 33.1, L2,
  "contractor -> its SAM registration. The 92.5% quoted in the pass-1 report was measured on the small recent-years contracts copy; "
  "on the full 93M-row file two thirds of recipient UEIs are older registrations missing from the current public SAM extract")
e("FED_USASPENDING_CONTRACTS", "RECIPIENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 85832, 92833, 887310, 92.5, L2,
  "recent-years contracts copy (5.7M rows) -> SAM registrant")
e("FED_USASPENDING_CONTRACTS_FULL", "recipient_uei", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "UEI", 160157, 420990, 887310, 38.0, L2,
  "20M-row contracts copy -> SAM registrant; same older-UEI gap as the full file")
e("FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID", "FED_FDIC_BANK_DATA", "CERT", "HMDA_ARID", 2678, 3835, 27836, 69.8, "SOLID (split by agency code)",
  "BANK-REGULATOR ROWS ONLY (agency code 1, 2 or 3): there the old lender id is a bank certificate #. This is the split-by-agency fix for the "
  "suspect unsplit edge; name-checked 2026-08-30 through the crosswalk's lender names -- the misses are banks renamed under the same cert", "MEASURED", "ltrim0")
e("FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID", "FED_DOL_FORM5500_FULL", "SPONS_DFE_EIN", "EIN", 411, 1018, 466446, 40.4, "SOLID (split by agency code)",
  "HUD ROWS ONLY (agency code 7): there the old lender id is the lender's tax id, and 4 in 10 have a benefit-plan filing; name-checked 2026-08-30", "MEASURED", "digits")
e("FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID", "FED_IRS_BMF", "EIN", "EIN", 19, 1018, 1974830, 1.9, L2,
  "HUD ROWS ONLY (agency code 7); mortgage lenders are rarely nonprofits, so low overlap is expected", "MEASURED", "digits")
e("FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS", "ASSOCIATE_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 9986, 10223, 2456135, 97.7, L2)
e("FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS", "ASSOCIATE_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 1558, 1559, 2456135, 99.9, L2)
e("FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS", "ASSOCIATE_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 2490, 2500, 2456135, 99.6, L2)
e("FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "ENROLLMENT_ID", FFS, "ENRLMT_ID", "PECOS_ENRLMT", 14207, 14425, 2978925, 98.5, L2)
e("FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS", "ENROLLMENT_ID", FFS, "ENRLMT_ID", "PECOS_ENRLMT", 11220, 11508, 2978925, 97.5, L2)
e("FED_CMS_HOSPICE_ENROLLMENTS", "ENROLLMENT_ID", FFS, "ENRLMT_ID", "PECOS_ENRLMT", 5670, 6066, 2978925, 93.5, L2)
e("FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS", "ENROLLMENT_ID", FFS, "ENRLMT_ID", "PECOS_ENRLMT", 10936, 11063, 2978925, 98.9, L2)
e("FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS", "ENROLLMENT_ID", FFS, "ENRLMT_ID", "PECOS_ENRLMT", 5462, 5530, 2978925, 98.8, L2)
e("FED_CMS_PECOS_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", FFS, "PECOS_ASCT_CNTL_ID", "PECOS_PAC", 2456135, 2456135, 2456135, 100.0, "SOLID (by construction)",
  "the same enrollment file loaded twice under two names; identical id sets")


if __name__ == "__main__":
    hit = attach_precision(rows)
    with OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {OUT}  ({len(rows)} edges; {hit} carry level-3 name/state numbers)")
