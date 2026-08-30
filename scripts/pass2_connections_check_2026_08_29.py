"""Pass 2 of the master connections list (2026-08-29).

Three jobs, all read-only, all against LIBRARY_RAW.LANDING:
  A. Value-check candidate ID columns that pass 1 skipped or mis-matched (bucket-B leftovers,
     the 08-05 catalog's "already have?" rows, tables landed after the 08-20 snapshot).
  B. Profile parent / owner / successor pointer columns and measure whether their values resolve
     into a target key column (self or another table).
  C. Cross-table overlaps for candidates that have a second side.

Every column gets: rows, filled, distinct non-blank, junk share, 3-value sample.
Output: reports/recon/pass2/pass2_live_check_2026-08-29.json  (+ a .log alongside).
"""
from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import _snowflake_conn as sf  # noqa: E402

OUT_DIR = os.path.join(REPO, "reports", "recon", "pass2")
OUT_JSON = os.path.join(OUT_DIR, "pass2_live_check_2026-08-29.json")
OUT_LOG = os.path.join(OUT_DIR, "pass2_live_check_2026-08-29.log")
COLS_CSV = os.path.join(OUT_DIR, "live_columns_2026-08-29.csv")

DB = "LIBRARY_RAW.LANDING"
JUNK = "('', '0', 'N/A', 'NA', 'NONE', 'NULL', 'UNKNOWN', 'UNAVAIL', '-', 'NAN', 'NOT APPLICABLE', '.', '00000000')"

# ---------------------------------------------------------------------------------------------
# live column inventory (local CSV pulled earlier this session)
# ---------------------------------------------------------------------------------------------
COLS: dict[str, list[str]] = defaultdict(list)
ROWS: dict[str, int] = {}
with open(COLS_CSV, encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r["schema"] != "LANDING":
            continue
        COLS[r["table"]].append(r["column"])
        try:
            ROWS[r["table"]] = int(r["row_count"] or 0)
        except ValueError:
            ROWS[r["table"]] = 0


def has(table: str, col: str) -> bool:
    return col in COLS.get(table, [])


def find_col(table_pat: str, col_pat: str):
    t = re.compile(table_pat)
    c = re.compile(col_pat)
    for tb, cs in COLS.items():
        if t.search(tb):
            for cc in cs:
                if c.search(cc):
                    return tb, cc
    return None


def q(col: str) -> str:
    """Quote a column name (dotted GLEIF names and lower-case names need it)."""
    if re.fullmatch(r"[A-Z_][A-Z0-9_]*", col):
        return col
    return '"' + col.replace('"', '""') + '"'


# ---------------------------------------------------------------------------------------------
# A. candidate ID columns  (cand label, table, column)
# ---------------------------------------------------------------------------------------------
A_CANDS = [
    # --- devices / drugs / FDA
    ("GUDID primary DI (UDI-DI)", "FED_FDA_GUDID_FULL_DEVICE", "PRIMARYDI"),
    ("GUDID primary DI (UDI-DI)", "FED_FDA_GUDID_FULL_IDENTIFIERS", "PRIMARYDI"),
    ("GUDID device id (all pkg levels)", "FED_FDA_GUDID_FULL_IDENTIFIERS", "DEVICEID"),
    ("GUDID labeler DUNS", "FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER"),
    ("GUDID device record key", "FED_FDA_GUDID_FULL_DEVICE", "PUBLICDEVICERECORDKEY"),
    ("NDC directory product NDC", "FED_FDA_NDC_DIRECTORY", "PRODUCTNDC"),
    ("NDC directory product id (NDC+SPL set)", "FED_FDA_NDC_DIRECTORY", "PRODUCTID"),
    ("FDA application # (NDA/ANDA/BLA)", "FED_FDA_NDC_DIRECTORY", "APPLICATIONNUMBER"),
    ("FDA drug master file #", "FED_FDA_DRUG_MASTER_FILES", "DMF"),
    ("NADAC NDC (11-digit)", "FED_CMS_NADAC", "NDC"),
    # --- health plans / providers
    ("HIOS issuer id", "FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF", "ISSUERID"),
    ("HIOS standard component id", "FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF", "STANDARDCOMPONENTID"),
    ("HIOS plan id (variant)", "FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF", "PLANID"),
    ("HIOS product id", "FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF", "HIOSPRODUCTID"),
    ("HRSA health center #", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "HEALTH_CENTER_NUMBER"),
    ("HRSA BHCMIS org id", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER"),
    ("HRSA BPHC site #", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "BPHC_ASSIGNED_NUMBER"),
    ("HRSA site NPI", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_NPI_NUMBER"),
    ("HRSA site Medicare billing # (CCN?)", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_MEDICARE_BILLING_NUMBER"),
    ("HRSA BHCMIS id (center info)", "FED_HRSA_UDS_HEALTH_CENTER_INFO", "BHCMISID"),
    ("HRSA grant #", "FED_HRSA_UDS_HEALTH_CENTER_INFO", "GRANTNUMBER"),
    ("HRSA HPSA id", "FED_HRSA_SHORTAGE_AREAS", "HPSA_ID"),
    ("NPDB practitioner #", "FED_HRSA_NPDB", "PRACTNUM"),
    ("CMS POS Medicaid vendor #", "FED_CMS_POS_OTHER", "MDCD_VNDR_NUM"),
    ("CMS POS cross-ref provider #", "FED_CMS_POS_OTHER", "CROSS_REF_PROVIDER_NUMBER"),
    ("PECOS associate id (hospice)", "FED_CMS_HOSPICE_ENROLLMENTS", "ASSOCIATE_ID"),
    ("Nursing-home chain id", "FED_CMS_NURSING_HOME", "CHAIN_ID"),
    ("Nursing-home chain id (411)", "FED_NURSINGHOME411", "CHAIN_ID"),
    ("SNF affiliation entity id", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "AFFILIATION_ENTITY_ID"),
    # --- environment
    ("EPA AQS site # (needs state+county)", "FED_EPA_AQS_SITES", "SITE_NUMBER"),
    ("NRC incident seq # (incidents)", "FED_USCG_NRC_INCIDENTS", "SEQNOS"),
    ("NRC incident seq # (reports)", "FED_USCG_NRC_INCIDENT_REPORTS", "SEQNOS"),
    ("NFIP community id", "FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK", "COMMUNITYIDNUMBER"),
    ("NFIP community id (R2)", "FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK_FULL_R2", "COMMUNITYIDNUMBER"),
    ("WQP monitoring location id", "FED_WQP_MONITORING_STATIONS", "MONITORINGLOCATIONIDENTIFIER"),
    ("TRI parent DUNS", "FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM"),
    ("TRI foreign parent DUNS", "FED_EPA_TRI_FACILITY", "FOREIGN_PARENT_CO_DB_NUM"),
    ("TRI parent DUNS (basic 2023)", "FED_EPA_TRI_BASIC_2023", "C_16_PARENT_CO_DB_NUM"),
    ("TRI EPA registry id", "FED_EPA_TRI_FACILITY", "EPA_REGISTRY_ID"),
    ("CAMPD owner/operator (text)", "FED_EPA_CAMPD_FACILITY", "OWNER_OPERATOR"),
    ("GHGRP parent company (text)", "FED_EPA_GHGRP_FACILITY", "PARENT_COMPANY"),
    # --- banking
    ("FDIC UNINUM", "FED_FDIC_BANK_DATA", "UNINUM"),
    ("FDIC NEWCERT (successor cert)", "FED_FDIC_BANK_DATA", "NEWCERT"),
    ("FDIC PARCERT (parent cert)", "FED_FDIC_BANK_DATA", "PARCERT"),
    ("FDIC ULTCERT (ultimate cert)", "FED_FDIC_BANK_DATA", "ULTCERT"),
    ("FDIC RSSDHCR (holding co RSSD)", "FED_FDIC_BANK_DATA", "RSSDHCR"),
    ("FDIC OTS docket", "FED_FDIC_BANK_DATA", "DOCKET"),
    ("FDIC SOD RSSDID", "FED_FDIC_SOD_BRANCH_DEPOSITS", "RSSDID"),
    ("FDIC SOD RSSDHCR", "FED_FDIC_SOD_BRANCH_DEPOSITS", "RSSDHCR"),
    ("FHLB member FHFA id", "FED_FHFA_FHLB_MEMBERSHIP", "FHFA_ID"),
    ("FHLB member FDIC cert", "FED_FHFA_FHLB_MEMBERSHIP", "CERT"),
    ("FHLB member Fed RSSD", "FED_FHFA_FHLB_MEMBERSHIP", "FED_ID"),
    ("FHLB member NCUA id", "FED_FHFA_FHLB_MEMBERSHIP", "NCUA_ID"),
    ("FHLB member NAIC id (insurers!)", "FED_FHFA_FHLB_MEMBERSHIP", "NAIC_ID"),
    ("SBA lender FDIC #", "FED_SBA_LOANS", "BANKFDICNUMBER"),
    ("SBA lender NCUA #", "FED_SBA_LOANS", "BANKNCUANUMBER"),
    ("SBA location id", "FED_SBA_LOANS", "LOCATIONID"),
    ("SBA franchise code", "FED_SBA_LOANS", "FRANCHISECODE"),
    ("PPP originating lender location id", "FED_SBA_PPP", "ORIGINATINGLENDERLOCATIONID"),
    ("PPP servicing lender location id", "FED_SBA_PPP", "SERVICINGLENDERLOCATIONID"),
    ("HMDA legacy respondent id", "FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID"),
    ("HMDA legacy agency code", "FED_CFPB_HMDA_HISTORIC", "AGENCY_CODE"),
    ("HMDA ARID 2017 (xref)", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "ARID_2017"),
    ("HMDA LEI 2018 (xref)", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "LEI_2018"),
    ("FHA originating mortgagee #", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "ORIGINATING_MORTGAGEE_NUMBER"),
    ("FHA sponsor #", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "SPONSOR_NUMBER"),
    ("FHA non-profit #", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "NON_PROFIT_NUMBER"),
    ("HUD Section 8 contract #", "FED_HUD_MF_SECTION8_CONTRACTS", "CONTRACT_NUMBER"),
    ("HUD Section 8 property id", "FED_HUD_MF_SECTION8_CONTRACTS", "PROPERTY_ID"),
    ("HUD assisted-housing code", "FED_HUD_ASSISTED_HOUSING_PROJECTS", "CODE"),
    ("USDA RD borrower id", "FED_USDA_RD_MFH_ACTIVE_PROJECTS", "BORROWER_ID"),
    # --- securities
    ("SEC series id", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "SERIES_ID"),
    ("SEC class id", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "CLASS_ID"),
    ("SEC 1940-Act file # (series/class)", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "REPORTING_FILE_NUMBER"),
    ("SEC class ticker", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "CLASS_TICKER"),
    ("SEC MMF series id", "FED_SEC_MONEY_MARKET_FUND_INFORMATION", "SERIES_ID"),
    ("SEC MMF class id", "FED_SEC_MONEY_MARKET_FUND_INFORMATION", "CLASS_ID"),
    ("FINRA CRD # (13F filers)", "FED_SEC_13F_FILERS", "CRDNUMBER"),
    ("SEC file # (13F filers)", "FED_SEC_13F_FILERS", "SECFILENUMBER"),
    ("13F file #", "FED_SEC_13F_FILERS", "FORM13FFILENUMBER"),
    ("PCAOB firm id", "FED_PCAOB_FORM_AP_FILINGS", "FIRM_ID"),
    ("PCAOB issuer id", "FED_PCAOB_FORM_AP_FILINGS", "ISSUER_ID"),
    ("PCAOB issuer CIK", "FED_PCAOB_FORM_AP_FILINGS", "ISSUER_CIK"),
    ("PCAOB engagement partner id", "FED_PCAOB_FORM_AP_FILINGS", "ENGAGEMENT_PARTNER_ID"),
    ("ISO MIC", "INTL_ISO_MIC_REGISTRY", "MIC"),
    ("ISO MIC operating MIC", "INTL_ISO_MIC_REGISTRY", "OPERATING_MIC"),
    ("ISIN (US SEC EDGAR table)", "FED_US_SEC_EDGAR", "ISIN"),
    ("SEC insider file #", "FED_SEC_INSIDER_REPORTINGOWNER", "FILE_NUMBER"),
    # --- sanctions
    ("OFAC SDN entity #", "FED_OFAC_SDN", "ENT_NUM"),
    ("CSL entity #", "FED_CONSOLIDATED_SCREENING_LIST", "ENTITY_NUMBER"),
    ("CSL ids blob", "FED_CONSOLIDATED_SCREENING_LIST", "IDS"),
    ("EU sanctions ref #", "INTL_EU_SANCTIONS", "EU_REF_NUM"),
    ("EU sanctions id-doc #", "INTL_EU_SANCTIONS", "IDEN_NUMBER"),
    ("UK OFSI group id", "INTL_UK_SANCTIONS_LIST", "OFSI_GROUP_ID"),
    ("UK sanctions UN ref #", "INTL_UK_SANCTIONS_LIST", "UN_REFERENCE_NUMBER"),
    ("UK sanctions business reg # (text)", "INTL_UK_SANCTIONS_LIST", "BUSINESS_REGISTRATION_NUMBER_S"),
    ("UK sanctions IMO", "INTL_UK_SANCTIONS_LIST", "IMO_NUMBER"),
    ("UK sanctions national id #", "INTL_UK_SANCTIONS_LIST", "NATIONAL_IDENTIFIER_NUMBER"),
    ("UK sanctions passport #", "INTL_UK_SANCTIONS_LIST", "PASSPORT_NUMBER"),
    ("UK sanctions HIN", "INTL_UK_SANCTIONS_LIST", "HULL_IDENTIFICATION_NUMBER_HIN"),
    ("OpenSanctions id", "INTL_OPENSANCTIONS_DEFAULT", "ID"),
    ("OpenSanctions identifiers blob", "INTL_OPENSANCTIONS_DEFAULT", "IDENTIFIERS"),
    # --- corporate registries
    ("GLEIF RA entity id (national co #)", "INTL_GLEIF", "Entity.RegistrationAuthority.RegistrationAuthorityEntityID"),
    ("GLEIF RA id", "INTL_GLEIF", "Entity.RegistrationAuthority.RegistrationAuthorityID"),
    ("GLEIF successor LEI", "INTL_GLEIF", "Entity.SuccessorEntity.1.SuccessorLEI"),
    ("GLEIF L2 start node LEI", "INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_STARTNODE_NODEID"),
    ("GLEIF L2 end node LEI", "INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_ENDNODE_NODEID"),
    ("GLEIF L2 relationship type", "INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_RELATIONSHIPTYPE"),
    ("FARA registration #", "FED_FARA_BULK", "REGISTRATION_NUMBER"),
    ("IRS group exemption #", "FED_IRS_BMF", "C_GROUP"),
    ("IRS affiliation code", "FED_IRS_BMF", "AFFILIATION"),
    ("FMCSA USDOT #", "FED_FMCSA_COMPANY_CENSUS", "DOT_NUMBER"),
    ("FMCSA MC docket 1", "FED_FMCSA_COMPANY_CENSUS", "DOCKET1"),
    ("FMCSA docket 1 prefix", "FED_FMCSA_COMPANY_CENSUS", "DOCKET1PREFIX"),
    ("FMCSA prior revoked USDOT #", "FED_FMCSA_COMPANY_CENSUS", "PRIOR_REVOKE_DOT_NUMBER"),
    ("FMCSA DUNS", "FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO"),
    ("FMCSA business org id", "FED_FMCSA_COMPANY_CENSUS", "BUSINESS_ORG_ID"),
    ("SAM DoDAAC", "FED_SAM_ENTITY_PUBLIC", "DODAAC"),
    ("SAM exclusions SAM #", "FED_SAM_EXCLUSIONS_FULL_R2", "SAM_NUMBER"),
    ("SAM exclusions UEI", "FED_SAM_EXCLUSIONS_FULL_R2", "UNIQUE_ENTITY_ID"),
    ("SAM exclusions NPI", "FED_SAM_EXCLUSIONS_FULL_R2", "NPI"),
    ("SAM exclusions cross-reference", "FED_SAM_EXCLUSIONS_FULL_R2", "CROSS_REFERENCE"),
    ("USCG vessel id", "FED_USCG_VESSEL_DOCUMENTATION", "VESSEL_ID"),
    ("USCG party id (owner)", "FED_USCG_VESSEL_DOCUMENTATION", "PARTY_ID"),
    ("USCG HIN", "FED_USCG_VESSEL_DOCUMENTATION", "HIN"),
    ("USCG hull #", "FED_USCG_VESSEL_DOCUMENTATION", "HULL_NUMBER"),
    # --- labor
    ("OSHA ITA establishment id 2023", "FED_OSHA_ITA_300A_SUMMARY_2023", "ESTABLISHMENT_ID"),
    ("OSHA ITA establishment id 2024", "FED_OSHA_ITA_300A_SUMMARY_2024", "ESTABLISHMENT_ID"),
    ("OSHA ITA EIN 2024", "FED_OSHA_ITA_300A_SUMMARY_2024", "EIN"),
    ("OSHA inspections host est key", "FED_DOL_OSHA_INSPECTIONS", "HOST_EST_KEY"),
    ("OSHA inspections reporting id", "FED_DOL_OSHA_INSPECTIONS", "REPORTING_ID"),
    ("OFLC prevailing-wage tracking #", "FED_DOL_OFLC", "PW_TRACKING_NUMBER_1"),
    ("OLMS subsidiary (text)", "FED_DOL_OLMS", "SUBSIDIARY"),
    # --- justice / immigration
    ("ICE detention facility code (codes)", "FED_ICE_DETENTION_FACILITY_CODES", "DETENTION_FACILITY_CODE"),
    ("ICE detention facility code (stints)", "FED_ICE_DETENTION_STINTS", "DETENTION_FACILITY_CODE"),
    ("ICE stint unique identifier (person)", "FED_ICE_DETENTION_STINTS", "UNIQUE_IDENTIFIER"),
    ("ICE stay id", "FED_ICE_DETENTION_STINTS", "STAY_ID"),
    ("MPV ORI agency id", "XC_MAPPING_POLICE_VIOLENCE", "ORI_AGENCY_IDENTIFIER_IF_AVAILABLE"),
    ("MPV WaPo id", "XC_MAPPING_POLICE_VIOLENCE", "WAPO_ID_IF_INCLUDED_IN_WAPO_DATABASE"),
    ("MPV fatal encounters id", "XC_MAPPING_POLICE_VIOLENCE", "FATAL_ENCOUNTERS_ID"),
    ("CL positions predecessor id", "FED_COURTLISTENER_POSITIONS", "PREDECESSOR_ID"),
    ("CL positions supervisor id", "FED_COURTLISTENER_POSITIONS", "SUPERVISOR_ID"),
    ("CL positions school id", "FED_COURTLISTENER_POSITIONS", "SCHOOL_ID"),
    ("CL courts parent court id", "FED_COURTLISTENER_COURTS", "PARENT_COURT_ID"),
    ("CL dockets parent docket id", "FED_COURTLISTENER_DOCKETS", "PARENT_DOCKET_ID"),
    ("ECHR application #", "INTL_HUDOC", "APPNO"),
    ("ECLI", "INTL_HUDOC", "ECLI"),
    # --- transport
    ("FAA N-number", "FED_FAA_AIRCRAFT_REGISTRY", "N_NUMBER"),
    ("FAA Mode S code", "FED_FAA_AIRCRAFT_REGISTRY", "MODE_S_CODE"),
    ("FAA registry unique id", "FED_FAA_AIRCRAFT_REGISTRY", "UNIQUE_ID"),
    ("NTSB registration # (N-number)", "FED_NTSB_AVIATION_AIRCRAFT", "REGIS_NO"),
    ("NTSB operator cert #", "FED_NTSB_AVIATION_AIRCRAFT", "OPER_CERT_NUM"),
    ("NTSB operator code", "FED_NTSB_AVIATION_AIRCRAFT", "OPER_CODE"),
    ("NTSB departure airport id", "FED_NTSB_AVIATION_AIRCRAFT", "DPRT_APT_ID"),
    ("FRA accident #", "FED_FRA_EQUIPMENT_ACCIDENTS", "ACCIDENT_NUMBER"),
    ("FRA parent railroad code (casualties)", "FED_FRA_CASUALTIES", "REPORTING_PARENT_RAILROAD_CODE"),
    ("FRA holding company (text)", "FED_FRA_CASUALTIES", "REPORTING_RAILROAD_HOLDING_COMPANY"),
    ("AIS MMSI", "FED_NOAA_AIS", "MMSI"),
    ("PHMSA operator id", "FED_PHMSA_FLAGGED_INCIDENTS", "PHMSA_OPERATOR_ID"),
    # --- consumer
    ("CPSC NEISS case #", "FED_CPSC_NEISS", "CPSC_CASE_NUMBER"),
    ("CFPB complaint id", "FED_CFPB_COMPLAINTS", "Complaint ID"),
    # --- procurement / grants
    ("Subaward number", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARD_NUMBER"),
    ("Subaward SAM report id", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARD_SAM_REPORT_ID"),
    ("Subaward prime FAIN", "FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_FAIN"),
    ("Subaward prime parent PIID", "FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_PARENT_PIID"),
    ("Subawardee UEI", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_UEI"),
    ("Subawardee parent UEI", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_PARENT_UEI"),
    ("Subawardee DUNS", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_DUNS"),
    ("Contracts parent award PIID (20M copy)", "FED_USASPENDING_CONTRACTS_FULL", "parent_award_id_piid"),
    ("Contracts recipient parent UEI (R2)", "FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_PARENT_UEI"),
    ("Contracts recipient parent UEI (20M copy)", "FED_USASPENDING_CONTRACTS_FULL", "recipient_parent_uei"),
    ("Contracts recipient parent DUNS (20M copy)", "FED_USASPENDING_CONTRACTS_FULL", "recipient_parent_duns"),
    ("Assistance recipient parent UEI", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_parent_uei"),
    ("Assistance recipient parent DUNS", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_parent_duns"),
    ("Solicitation id (bulk sample)", "FED_USASPENDING_BULK", "SOLICITATION_IDENTIFIER"),
    ("NIH org IPF code", "FED_NIH_REPORTER", "ORG_IPF_CODE"),
    ("NIH PI profile ids", "FED_NIH_REPORTER", "PI_PROFILE_IDS"),
    ("NIH org UEI", "FED_NIH_REPORTER", "ORG_UEI"),
    ("NIH org DUNS", "FED_NIH_REPORTER", "ORG_DUNS"),
    ("NIH subproject id", "FED_NIH_REPORTER", "SUBPROJECT_ID"),
    ("SBIR agency tracking #", "FED_SBIR_STTR_AWARDS", "AGENCY_TRACKING_NUMBER"),
    ("SBIR contract #", "FED_SBIR_STTR_AWARDS", "CONTRACT"),
    ("SBIR solicitation #", "FED_SBIR_STTR_AWARDS", "SOLICITATION_NUMBER"),
    ("SBIR UEI", "FED_SBIR_STTR_AWARDS", "UEI"),
    ("SBIR DUNS", "FED_SBIR_STTR_AWARDS", "DUNS"),
    ("NSF EIN (stub)", "FED_NSF_AWARDS", "EIN"),
    # --- energy
    ("EIA FERC cogeneration docket", "FED_EIA860_2_PLANT", "FERC_COGENERATION_DOCKET_NUMBER"),
    ("EIA FERC small-power docket", "FED_EIA860_2_PLANT", "FERC_SMALL_POWER_PRODUCER_DOCKET_NUMBER"),
    ("EIA FERC EWG docket", "FED_EIA860_2_PLANT", "FERC_EXEMPT_WHOLESALE_GENERATOR_DOCKET_NUMBER"),
    ("EIA transmission owner id", "FED_EIA860_2_PLANT", "TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID"),
    ("EIA ownership id", "FED_EIA860_4_OWNER", "OWNERSHIP_ID"),
    # --- politics
    ("Committee's candidate id", "FED_FEC_BULK_COMMITTEES", "FEC_CAND_ID"),
    ("Bill sponsor bioguide", "FED_GOVINFO_BILLSTATUS", "SPONSOR_BIOGUIDE"),
    ("Cosponsor bioguide", "FED_GOVINFO_BILL_COSPONSORS", "COSPONSOR_BIOGUIDE"),
    # --- misc pointers
    ("Treasury MTS parent id", "FED_TREASURY_MTS_RECEIPTS", "PARENT_ID"),
    ("NPPES parent org TIN (known masked)", "FED_CMS_NPPES", "PARENT_ORGANIZATION_TIN"),
    ("NPPES parent org LBN", "FED_CMS_NPPES", "PARENT_ORGANIZATION_LBN"),
    ("EPA crosswalk ultimate parent LEI", "XC_EPA_CORPORATE_CROSSWALK", "ULTIMATE_PARENT_LEI"),
    ("EPA crosswalk parent CIK", "XC_EPA_CORPORATE_CROSSWALK", "PARENT_CIK"),
    ("EPA crosswalk parent UEI", "XC_EPA_CORPORATE_CROSSWALK", "PARENT_UEI"),
]

# ---------------------------------------------------------------------------------------------
# B/C. overlap / resolution tests: (label, left table, left col, right table, right col, norm)
#   share = distinct left values found in right
#   norm: None | 'digits' (strip non-digits) | 'ltrim0' | 'upper' | 'nnum' (strip leading N) |
#         'ndc9' (left NADAC 11-digit -> first 9; right PRODUCTNDC 'LLLLL-PPPP' -> 9)
# ---------------------------------------------------------------------------------------------
OVERLAPS = [
    # devices / drugs
    ("NADAC NDC -> NDC directory (9-digit labeler+product)", "FED_CMS_NADAC", "NDC", "FED_FDA_NDC_DIRECTORY", "PRODUCTNDC", "ndc9"),
    ("GUDID DI -> GUDID identifiers DI", "FED_FDA_GUDID_FULL_DEVICE", "PRIMARYDI", "FED_FDA_GUDID_FULL_IDENTIFIERS", "PRIMARYDI", None),
    ("GUDID labeler DUNS -> contracts recipient DUNS (20M)", "FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER", "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "digits"),
    ("GUDID labeler DUNS -> FMCSA DUNS", "FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER", "FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO", "digits"),
    ("GUDID labeler DUNS -> NIH org DUNS", "FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER", "FED_NIH_REPORTER", "ORG_DUNS", "digits"),
    # health
    ("HRSA site NPI -> NPPES NPI", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "FQHC_SITE_NPI_NUMBER", "FED_CMS_NPPES", "NPI", "digits"),
    ("HRSA BHCMIS (sites) -> BHCMIS (center info)", "FED_HRSA_UDS_SERVICE_DELIVERY_SITES", "BHCMIS_ORGANIZATION_IDENTIFICATION_NUMBER", "FED_HRSA_UDS_HEALTH_CENTER_INFO", "BHCMISID", "upper"),
    ("Hospice associate id -> PECOS PAC id", "FED_CMS_HOSPICE_ENROLLMENTS", "ASSOCIATE_ID", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "digits"),
    ("SNF affiliation entity id -> PECOS PAC id", "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS", "AFFILIATION_ENTITY_ID", "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT", "PECOS_ASCT_CNTL_ID", "digits"),
    ("POS cross-ref provider # -> POS CCN", "FED_CMS_POS_OTHER", "CROSS_REF_PROVIDER_NUMBER", "FED_CMS_POS_OTHER", "CCN", "upper"),
    ("Nursing-home chain id -> 411 chain id", "FED_CMS_NURSING_HOME", "CHAIN_ID", "FED_NURSINGHOME411", "CHAIN_ID", "digits"),
    # environment
    ("NRC seq # incidents -> reports", "FED_USCG_NRC_INCIDENTS", "SEQNOS", "FED_USCG_NRC_INCIDENT_REPORTS", "SEQNOS", "digits"),
    ("TRI parent DUNS -> contracts recipient DUNS (20M)", "FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM", "FED_USASPENDING_CONTRACTS_FULL", "recipient_duns", "digits"),
    ("TRI parent DUNS -> FMCSA DUNS", "FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM", "FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO", "digits"),
    ("TRI parent DUNS -> GUDID labeler DUNS", "FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM", "FED_FDA_GUDID_FULL_DEVICE", "DUNSNUMBER", "digits"),
    ("TRI parent DUNS -> subaward prime DUNS", "FED_EPA_TRI_FACILITY", "PARENT_CO_DB_NUM", "FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARDEE_DUNS", "digits"),
    ("TRI EPA registry id -> TRI FRS_ID (same table)", "FED_EPA_TRI_FACILITY", "EPA_REGISTRY_ID", "FED_EPA_TRI_FACILITY", "FRS_ID", "digits"),
    # banking
    ("FDIC PARCERT -> FDIC CERT", "FED_FDIC_BANK_DATA", "PARCERT", "FED_FDIC_BANK_DATA", "CERT", "ltrim0"),
    ("FDIC ULTCERT -> FDIC CERT", "FED_FDIC_BANK_DATA", "ULTCERT", "FED_FDIC_BANK_DATA", "CERT", "ltrim0"),
    ("FDIC NEWCERT -> FDIC CERT", "FED_FDIC_BANK_DATA", "NEWCERT", "FED_FDIC_BANK_DATA", "CERT", "ltrim0"),
    ("FDIC RSSDHCR -> FDIC FED_RSSD (bank RSSDs)", "FED_FDIC_BANK_DATA", "RSSDHCR", "FED_FDIC_BANK_DATA", "FED_RSSD", "ltrim0"),
    ("FDIC RSSDHCR -> SOD RSSDHCR", "FED_FDIC_BANK_DATA", "RSSDHCR", "FED_FDIC_SOD_BRANCH_DEPOSITS", "RSSDHCR", "ltrim0"),
    ("FHLB CERT -> FDIC CERT", "FED_FHFA_FHLB_MEMBERSHIP", "CERT", "FED_FDIC_BANK_DATA", "CERT", "ltrim0"),
    ("FHLB FED_ID -> FDIC FED_RSSD", "FED_FHFA_FHLB_MEMBERSHIP", "FED_ID", "FED_FDIC_BANK_DATA", "FED_RSSD", "ltrim0"),
    ("SBA lender FDIC # -> FDIC CERT", "FED_SBA_LOANS", "BANKFDICNUMBER", "FED_FDIC_BANK_DATA", "CERT", "ltrim0"),
    ("HMDA legacy respondent id -> ARID 2017 xref", "FED_CFPB_HMDA_HISTORIC", "RESPONDENT_ID", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "ARID_2017", "upper"),
    ("HMDA xref LEI 2018 -> GLEIF LEI", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "LEI_2018", "INTL_GLEIF", "LEI", "upper"),
    ("HMDA xref LEI 2018 -> HMDA LEI", "FED_CFPB_HMDA_ARID2017_LEI_XREF", "LEI_2018", "FED_CFPB_HMDA", "LEI", "upper"),
    ("FHA sponsor # -> FHA originating mortgagee #", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "SPONSOR_NUMBER", "FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT", "ORIGINATING_MORTGAGEE_NUMBER", "digits"),
    # securities
    ("SEC MMF series id -> series/class table", "FED_SEC_MONEY_MARKET_FUND_INFORMATION", "SERIES_ID", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "SERIES_ID", "upper"),
    ("SEC series/class CIK -> insider issuer CIK", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "CIK_NUMBER", "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "ltrim0"),
    ("PCAOB issuer CIK -> insider issuer CIK", "FED_PCAOB_FORM_AP_FILINGS", "ISSUER_CIK", "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "ltrim0"),
    ("PCAOB issuer CIK -> DERA sub CIK 2025Q4", "FED_PCAOB_FORM_AP_FILINGS", "ISSUER_CIK", "FED_SEC_DERA_SUB_2025Q4", "CIK", "ltrim0"),
    ("Insider reporting-owner CIK -> insider issuer CIK", "FED_SEC_INSIDER_REPORTINGOWNER", "RPTOWNERCIK", "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "ltrim0"),
    ("MIC registry LEI -> GLEIF LEI", "INTL_ISO_MIC_REGISTRY", "LEI", "INTL_GLEIF", "LEI", "upper"),
    ("SEC class ticker -> company-tickers ticker", "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS", "CLASS_TICKER", "FED_SEC_EDGAR_COMPANY_TICKERS", "TICKER", "upper"),
    # sanctions
    ("CSL entity # -> OFAC SDN ent #", "FED_CONSOLIDATED_SCREENING_LIST", "ENTITY_NUMBER", "FED_OFAC_SDN", "ENT_NUM", "digits"),
    ("UK sanctions IMO -> OFAC SDN IMO", "INTL_UK_SANCTIONS_LIST", "IMO_NUMBER", "FED_OFAC_SDN", "IMO", "digits"),
    ("UK sanctions IMO -> USCG IMO", "INTL_UK_SANCTIONS_LIST", "IMO_NUMBER", "FED_USCG_VESSEL_DOCUMENTATION", "IMO_NUMBER", "digits"),
    ("UK sanctions IMO -> AIS IMO", "INTL_UK_SANCTIONS_LIST", "IMO_NUMBER", "FED_NOAA_AIS", "IMO", "digits"),
    ("UK sanctions HIN -> USCG HIN", "INTL_UK_SANCTIONS_LIST", "HULL_IDENTIFICATION_NUMBER_HIN", "FED_USCG_VESSEL_DOCUMENTATION", "HIN", "upper"),
    ("OFAC SDN IMO -> AIS IMO", "FED_OFAC_SDN", "IMO", "FED_NOAA_AIS", "IMO", "digits"),
    ("AIS MMSI -> OFAC SDN call sign? (no) / skip", None, None, None, None, None),
    # corporate
    ("GLEIF successor LEI -> GLEIF LEI", "INTL_GLEIF", "Entity.SuccessorEntity.1.SuccessorLEI", "INTL_GLEIF", "LEI", "upper"),
    ("GLEIF L2 start node -> GLEIF LEI", "INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_STARTNODE_NODEID", "INTL_GLEIF", "LEI", "upper"),
    ("GLEIF L2 end node -> GLEIF LEI", "INTL_GLEIF_RELATIONSHIPS", "RELATIONSHIP_ENDNODE_NODEID", "INTL_GLEIF", "LEI", "upper"),
    ("GLEIF RA entity id (UK RA000585) -> UK Companies House #", "INTL_GLEIF", "Entity.RegistrationAuthority.RegistrationAuthorityEntityID", "INT_UK_COMPANIES_HOUSE", "CompanyNumber", "ukch"),
    ("EPA crosswalk ultimate parent LEI -> GLEIF LEI", "XC_EPA_CORPORATE_CROSSWALK", "ULTIMATE_PARENT_LEI", "INTL_GLEIF", "LEI", "upper"),
    ("EPA crosswalk parent CIK -> insider issuer CIK", "XC_EPA_CORPORATE_CROSSWALK", "PARENT_CIK", "FED_SEC_INSIDER_SUBMISSION", "ISSUERCIK", "ltrim0"),
    ("EPA crosswalk parent UEI -> SAM UEI", "XC_EPA_CORPORATE_CROSSWALK", "PARENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("FMCSA prior revoked USDOT -> FMCSA USDOT", "FED_FMCSA_COMPANY_CENSUS", "PRIOR_REVOKE_DOT_NUMBER", "FED_FMCSA_COMPANY_CENSUS", "DOT_NUMBER", "digits"),
    ("SAM exclusions UEI -> SAM entity UEI", "FED_SAM_EXCLUSIONS_FULL_R2", "UNIQUE_ENTITY_ID", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("SAM exclusions NPI -> NPPES NPI", "FED_SAM_EXCLUSIONS_FULL_R2", "NPI", "FED_CMS_NPPES", "NPI", "digits"),
    ("SAM exclusions NPI -> LEIE NPI", "FED_SAM_EXCLUSIONS_FULL_R2", "NPI", "FED_HHS_OIG_LEIE", "NPI", "digits"),
    ("SAM DoDAAC -> contracts awarding office code (20M copy)", "FED_SAM_ENTITY_PUBLIC", "DODAAC", "FED_USASPENDING_CONTRACTS_FULL", "awarding_office_code", "upper"),
    # labor
    ("OSHA ITA establishment id 2024 -> 2023", "FED_OSHA_ITA_300A_SUMMARY_2024", "ESTABLISHMENT_ID", "FED_OSHA_ITA_300A_SUMMARY_2023", "ESTABLISHMENT_ID", "digits"),
    ("OSHA ITA EIN 2024 -> IRS BMF EIN", "FED_OSHA_ITA_300A_SUMMARY_2024", "EIN", "FED_IRS_BMF", "EIN", "digits"),
    ("OSHA ITA EIN 2024 -> Form 5500 sponsor EIN", "FED_OSHA_ITA_300A_SUMMARY_2024", "EIN", "FED_DOL_FORM5500_FULL", "SPONS_DFE_EIN", "digits"),
    ("Form 5500 sponsor EIN -> IRS BMF EIN", "FED_DOL_FORM5500", "SPONSOR_DFE_EIN", "FED_IRS_BMF", "EIN", "digits"),
    # justice
    ("ICE stints facility code -> ICE facility codes", "FED_ICE_DETENTION_STINTS", "DETENTION_FACILITY_CODE", "FED_ICE_DETENTION_FACILITY_CODES", "DETENTION_FACILITY_CODE", "upper"),
    ("CL positions predecessor -> CL people id", "FED_COURTLISTENER_POSITIONS", "PREDECESSOR_ID", "FED_COURTLISTENER_JUDGES", "ID", "digits"),
    ("CL positions supervisor -> CL people id", "FED_COURTLISTENER_POSITIONS", "SUPERVISOR_ID", "FED_COURTLISTENER_JUDGES", "ID", "digits"),
    ("CL courts parent court -> CL courts id", "FED_COURTLISTENER_COURTS", "PARENT_COURT_ID", "FED_COURTLISTENER_COURTS", "ID", "upper"),
    ("CL dockets parent docket -> CL dockets id", "FED_COURTLISTENER_DOCKETS", "PARENT_DOCKET_ID", "FED_COURTLISTENER_DOCKETS", "ID", "digits"),
    # transport
    ("NTSB N-number -> FAA N-number", "FED_NTSB_AVIATION_AIRCRAFT", "REGIS_NO", "FED_FAA_AIRCRAFT_REGISTRY", "N_NUMBER", "nnum"),
    ("FRA parent railroad code -> FRA reporting railroad code", "FED_FRA_CASUALTIES", "REPORTING_PARENT_RAILROAD_CODE", "FED_FRA_EQUIPMENT_ACCIDENTS", "REPORTING_RAILROAD_CODE", "upper"),
    ("AIS MMSI -> USCG? (no MMSI col) skip", None, None, None, None, None),
    # procurement / grants
    ("Subaward prime FAIN -> assistance FAIN", "FED_USASPENDING_SUBAWARDS_FULL", "PRIME_AWARD_FAIN", "FED_USASPENDING_ASSISTANCE_FULL", "award_id_fain", "upper"),
    ("Subawardee UEI -> SAM UEI", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("Subawardee parent UEI -> SAM UEI", "FED_USASPENDING_SUBAWARDS_FULL", "SUBAWARDEE_PARENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("Contracts recipient parent UEI (R2) -> SAM UEI", "FED_USASPENDING_CONTRACTS_FULL_R2", "RECIPIENT_PARENT_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("Assistance recipient parent UEI -> SAM UEI", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_parent_uei", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("Assistance recipient UEI -> SAM UEI", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_uei", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("Assistance recipient parent DUNS -> FMCSA DUNS", "FED_USASPENDING_ASSISTANCE_FULL", "recipient_parent_duns", "FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO", "digits"),
    ("Contracts parent PIID (20M) -> contracts PIID (R2)", "FED_USASPENDING_CONTRACTS_FULL", "parent_award_id_piid", "FED_USASPENDING_CONTRACTS_FULL_R2", "AWARD_ID_PIID", "upper"),
    ("NIH org UEI -> SAM UEI", "FED_NIH_REPORTER", "ORG_UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("NIH org DUNS -> FMCSA DUNS", "FED_NIH_REPORTER", "ORG_DUNS", "FED_FMCSA_COMPANY_CENSUS", "DUN_BRADSTREET_NO", "digits"),
    ("SBIR UEI -> SAM UEI", "FED_SBIR_STTR_AWARDS", "UEI", "FED_SAM_ENTITY_PUBLIC", "UEI_SAM", "upper"),
    ("SBIR contract # -> contracts PIID (R2)", "FED_SBIR_STTR_AWARDS", "CONTRACT", "FED_USASPENDING_CONTRACTS_FULL_R2", "AWARD_ID_PIID", "upper"),
    ("SBIR agency tracking # -> NIH project #", "FED_SBIR_STTR_AWARDS", "AGENCY_TRACKING_NUMBER", "FED_NIH_REPORTER", "CORE_PROJECT_NUM", "upper"),
    # energy
    ("EIA transmission owner id -> EIA utility id", "FED_EIA860_2_PLANT", "TRANSMISSION_OR_DISTRIBUTION_SYSTEM_OWNER_ID", "FED_EIA860_1_UTILITY", "UTILITY_ID", "digits"),
    ("EIA ownership id -> EIA utility id", "FED_EIA860_4_OWNER", "OWNERSHIP_ID", "FED_EIA860_1_UTILITY", "UTILITY_ID", "digits"),
    # politics
    ("Committee's candidate id -> FEC candidates", "FED_FEC_BULK_COMMITTEES", "FEC_CAND_ID", "FED_FEC_BULK_CANDIDATES", "FEC_CAND_ID", "upper"),
    ("Bill sponsor bioguide -> VoteView bioguide", "FED_GOVINFO_BILLSTATUS", "SPONSOR_BIOGUIDE", "FED_VOTEVIEW_MEMBERS", "BIOGUIDE_ID", "upper"),
    # misc
    ("Treasury MTS parent id -> classification id", "FED_TREASURY_MTS_RECEIPTS", "PARENT_ID", "FED_TREASURY_MTS_RECEIPTS", "CLASSIFICATION_ID", "digits"),
]


def norm_expr(col: str, how):
    c = q(col)
    if how is None:
        return f"NULLIF(TRIM({c}), '')"
    if how == "digits":
        return f"NULLIF(REGEXP_REPLACE({c}, '[^0-9]', ''), '')"
    if how == "ltrim0":
        return f"NULLIF(LTRIM(REGEXP_REPLACE({c}, '[^0-9]', ''), '0'), '')"
    if how == "upper":
        return f"NULLIF(UPPER(TRIM({c})), '')"
    if how == "nnum":
        return f"NULLIF(REGEXP_REPLACE(UPPER(TRIM({c})), '^N', ''), '')"
    raise ValueError(how)


def ndc9_left(col):
    return f"LEFT(NULLIF(REGEXP_REPLACE({q(col)}, '[^0-9]', ''), ''), 9)"


def ndc9_right(col):
    c = q(col)
    return (f"LPAD(SPLIT_PART({c}, '-', 1), 5, '0') || LPAD(SPLIT_PART({c}, '-', 2), 4, '0')")


def ukch_left(col):
    # only rows where the RA is UK Companies House; zero-pad to 8
    return f"LPAD(NULLIF(TRIM({q(col)}), ''), 8, '0')"


LOG = open(OUT_LOG, "a", encoding="utf-8")


def log(msg):
    line = f"{time.strftime('%H:%M:%S')} {msg}"
    print(line, flush=True)
    LOG.write(line + "\n")
    LOG.flush()


def run(cur, sql, timeout=600):
    cur.execute(f"ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = {timeout}")
    cur.execute(sql)
    return cur.fetchall()


def profile(cur, table, col):
    c = q(col)
    sql = f"""
    SELECT COUNT(*) AS rows_,
           COUNT({c}) AS filled,
           COUNT(DISTINCT NULLIF(TRIM({c}), '')) AS distinct_nonblank,
           COUNT_IF(UPPER(TRIM({c})) IN {JUNK}) AS junk,
           MIN(LENGTH(TRIM({c}))) AS minlen, MAX(LENGTH(TRIM({c}))) AS maxlen
    FROM {DB}.{table}
    """
    rows_, filled, dist, junk, minlen, maxlen = run(cur, sql)[0]
    sample = [r[0] for r in run(cur, f"""
        SELECT {c} FROM {DB}.{table}
        WHERE NULLIF(TRIM({c}), '') IS NOT NULL AND UPPER(TRIM({c})) NOT IN {JUNK}
        LIMIT 3""")]
    return dict(rows=rows_, filled=filled, distinct_nonblank=dist, junk=junk,
                minlen=minlen, maxlen=maxlen, sample=[str(s)[:60] for s in sample])


def overlap(cur, lt, lc, rt, rc, how):
    if how == "ndc9":
        le, re_ = ndc9_left(lc), ndc9_right(rc)
        lwhere = ""
    elif how == "ukch":
        le, re_ = ukch_left(lc), f"LPAD(NULLIF(TRIM({q(rc)}), ''), 8, '0')"
        lwhere = f" WHERE \"Entity.RegistrationAuthority.RegistrationAuthorityID\" = 'RA000585'"
    else:
        le, re_ = norm_expr(lc, how), norm_expr(rc, how)
        lwhere = ""
    sql = f"""
    WITH l AS (SELECT DISTINCT {le} AS v FROM {DB}.{lt}{lwhere}),
         r AS (SELECT DISTINCT {re_} AS v FROM {DB}.{rt})
    SELECT (SELECT COUNT(*) FROM l WHERE v IS NOT NULL AND UPPER(v) NOT IN {JUNK}) AS left_distinct,
           (SELECT COUNT(*) FROM r WHERE v IS NOT NULL) AS right_distinct,
           (SELECT COUNT(*) FROM l JOIN r USING (v) WHERE UPPER(v) NOT IN {JUNK}) AS matched
    """
    ld, rd, m = run(cur, sql, timeout=900)[0]
    return dict(left_distinct=ld, right_distinct=rd, matched=m,
                share=round(100.0 * m / ld, 1) if ld else None)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    conn = sf.connect()
    cur = conn.cursor()
    cur.execute("ALTER SESSION SET QUERY_TAG = 'pass2_connections_check_2026_08_29'")
    out = {"profiles": [], "overlaps": [], "errors": [], "extras": {}}
    t0 = time.time()

    # ---- A. profiles
    log(f"A. profiling {len(A_CANDS)} candidate columns")
    for i, (cand, table, col) in enumerate(A_CANDS, 1):
        if not has(table, col):
            out["errors"].append({"step": "profile", "cand": cand, "table": table, "col": col, "err": "column not in live inventory"})
            log(f"  [{i}] SKIP {table}.{col} (not in inventory)")
            continue
        try:
            p = profile(cur, table, col)
            p.update(cand=cand, table=table, col=col)
            out["profiles"].append(p)
            log(f"  [{i}] {cand}: {table}.{col} rows={p['rows']} filled={p['filled']} distinct={p['distinct_nonblank']} junk={p['junk']} {p['sample'][:2]}")
        except Exception as e:  # noqa: BLE001
            out["errors"].append({"step": "profile", "cand": cand, "table": table, "col": col, "err": str(e)[:300]})
            log(f"  [{i}] ERR {table}.{col}: {str(e)[:200]}")
        if i % 10 == 0:
            json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), indent=1, default=str)

    # ---- extras: composite AQS id, GLEIF L2 type breakdown, GLEIF RA id breakdown, FMCSA docket prefix breakdown
    extras = {
        "aqs_site_composite_distinct": f"SELECT COUNT(DISTINCT STATE_CODE||'-'||COUNTY_CODE||'-'||SITE_NUMBER) FROM {DB}.FED_EPA_AQS_SITES",
        "gleif_l2_relationship_types": f"SELECT RELATIONSHIP_RELATIONSHIPTYPE, RELATIONSHIP_RELATIONSHIPSTATUS, COUNT(*) FROM {DB}.INTL_GLEIF_RELATIONSHIPS GROUP BY 1,2 ORDER BY 3 DESC LIMIT 12",
        "gleif_ra_top": f"SELECT \"Entity.RegistrationAuthority.RegistrationAuthorityID\" AS ra, COUNT(*) FROM {DB}.INTL_GLEIF GROUP BY 1 ORDER BY 2 DESC LIMIT 15",
        "gleif_us_ra_count": f"SELECT \"Entity.LegalJurisdiction\" AS j, COUNT(*), COUNT(DISTINCT \"Entity.RegistrationAuthority.RegistrationAuthorityEntityID\") FROM {DB}.INTL_GLEIF WHERE \"Entity.LegalJurisdiction\" LIKE 'US%' GROUP BY 1 ORDER BY 2 DESC LIMIT 12",
        "fmcsa_docket_prefix": f"SELECT DOCKET1PREFIX, COUNT(*), COUNT(DISTINCT DOCKET1) FROM {DB}.FED_FMCSA_COMPANY_CENSUS GROUP BY 1 ORDER BY 2 DESC LIMIT 8",
        "fhlb_member_types": f"SELECT MEM_TYPE, CHAR_TYPE, COUNT(*), COUNT_IF(NULLIF(TRIM(NAIC_ID),'') IS NOT NULL) AS with_naic FROM {DB}.FED_FHFA_FHLB_MEMBERSHIP GROUP BY 1,2 ORDER BY 3 DESC LIMIT 12",
        "hmda_historic_agency_x_respondent": f"SELECT AGENCY_CODE, COUNT(*), COUNT(DISTINCT RESPONDENT_ID) FROM {DB}.FED_CFPB_HMDA_HISTORIC GROUP BY 1 ORDER BY 2 DESC",
        "sam_exclusion_classification": f"SELECT CLASSIFICATION, COUNT(*), COUNT_IF(NULLIF(TRIM(UNIQUE_ENTITY_ID),'') IS NOT NULL) AS with_uei, COUNT_IF(NULLIF(TRIM(NPI),'') IS NOT NULL) AS with_npi, COUNT_IF(NULLIF(TRIM(CAGE),'') IS NOT NULL) AS with_cage FROM {DB}.FED_SAM_EXCLUSIONS_FULL_R2 GROUP BY 1 ORDER BY 2 DESC",
        "ndc_dir_marketing_category": f"SELECT MARKETINGCATEGORYNAME, COUNT(*), COUNT(DISTINCT APPLICATIONNUMBER) FROM {DB}.FED_FDA_NDC_DIRECTORY GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "ice_stints_person_reuse": f"SELECT COUNT(*) AS rows_, COUNT(DISTINCT UNIQUE_IDENTIFIER) AS people, COUNT(DISTINCT STAY_ID) AS stays FROM {DB}.FED_ICE_DETENTION_STINTS",
        "opensanctions_schema": f"SELECT C_SCHEMA, COUNT(*) FROM {DB}.INTL_OPENSANCTIONS_DEFAULT GROUP BY 1 ORDER BY 2 DESC LIMIT 10",
        "opensanctions_identifier_kinds": f"SELECT REGEXP_SUBSTR(IDENTIFIERS, '[A-Za-z]+') AS kind, COUNT(*) FROM {DB}.INTL_OPENSANCTIONS_DEFAULT WHERE NULLIF(TRIM(IDENTIFIERS),'') IS NOT NULL GROUP BY 1 ORDER BY 2 DESC LIMIT 12",
        "fdic_docket_nonzero": f"SELECT COUNT(*) , COUNT_IF(NULLIF(LTRIM(TRIM(DOCKET),'0'),'') IS NOT NULL) FROM {DB}.FED_FDIC_BANK_DATA",
        "cl_positions_types_with_predecessor": f"SELECT POSITION_TYPE, COUNT(*), COUNT_IF(NULLIF(TRIM(PREDECESSOR_ID),'') IS NOT NULL) FROM {DB}.FED_COURTLISTENER_POSITIONS GROUP BY 1 ORDER BY 2 DESC LIMIT 8",
    }
    log("A2. extras")
    for k, sql in extras.items():
        try:
            out["extras"][k] = [list(map(str, r)) for r in run(cur, sql)]
            log(f"  {k}: {out['extras'][k][:4]}")
        except Exception as e:  # noqa: BLE001
            out["errors"].append({"step": "extra", "key": k, "err": str(e)[:300]})
            log(f"  ERR {k}: {str(e)[:200]}")
    json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), indent=1, default=str)

    # ---- B/C. overlaps
    real = [o for o in OVERLAPS if o[1]]
    log(f"B/C. {len(real)} overlap / resolution tests")
    for i, (label, lt, lc, rt, rc, how) in enumerate(real, 1):
        missing = [f"{t}.{c}" for t, c in ((lt, lc), (rt, rc)) if not has(t, c)]
        if missing:
            out["errors"].append({"step": "overlap", "label": label, "err": f"missing {missing}"})
            log(f"  [{i}] SKIP {label}: missing {missing}")
            continue
        try:
            r = overlap(cur, lt, lc, rt, rc, how)
            r.update(label=label, left=f"{lt}.{lc}", right=f"{rt}.{rc}", norm=how)
            out["overlaps"].append(r)
            log(f"  [{i}] {label}: {r['matched']}/{r['left_distinct']} = {r['share']}%  (right {r['right_distinct']})")
        except Exception as e:  # noqa: BLE001
            out["errors"].append({"step": "overlap", "label": label, "err": str(e)[:300]})
            log(f"  [{i}] ERR {label}: {str(e)[:200]}")
        if i % 5 == 0:
            json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), indent=1, default=str)

    out["elapsed_s"] = round(time.time() - t0)
    json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), indent=1, default=str)
    log(f"DONE in {out['elapsed_s']}s -> {OUT_JSON}")
    conn.close()


if __name__ == "__main__":
    main()
