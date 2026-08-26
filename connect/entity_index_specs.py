"""Per-source DISPLAY specs: how to read a human name + address for an entity.

Shared by the spine (golden-record survivorship) and the entity index (dossier
search labels). Column names confirmed live against LIBRARY_RAW.LANDING on
2026-06-25. A table not listed here still becomes part of the spine via its hard
key — it just contributes no name (the entity falls back to its key value).

Per-table spec:
  key      the hard key this table is indexed on (NPI / CCN / ...)
  key_col  the landing column carrying that key
  person   [last_col, first_col]  -> "LAST, FIRST" when present
  org      a single org/facility name column
  city/state/zip  address columns (any may be omitted)
  authority  survivorship rank, LOWER = more authoritative (NPPES=1 wins names)
  extra_keys  [{"key": ..., "key_col": ...}, ...] -- OPTIONAL. A table almost
    always carries exactly one hard key; a few carry two DIFFERENT hard IDs on
    the SAME row (e.g. Voteview's member file has both an ICPSR id and a
    BIOGUIDE id for the same legislator). Each extra key gets its own spine
    entity (spine v1 never fuses different ID *types* -- see spine.py's
    docstring) but shares this table's org/person/address/authority for name
    survivorship, since it's the same underlying row. Only use extra_keys when
    the extra ID genuinely describes THIS row's same entity (e.g. an auditee's
    UEI alongside its EIN) -- not a different entity on the row (e.g. ARCOS's
    buyer_dea_no shares reporter_name/city via this same mechanism today, a
    known, accepted mislabeling tradeoff; don't add a new instance of it
    without a good reason).

A table not in DISPLAY_SPECS is NOT part of the spine or ENTITY_INDEX today --
spine.py and entity_index.py both iterate this dict exclusively (SPINE_TABLES
below). (Corrected 2026-07-28: this docstring previously claimed an unlisted
table still joins the spine "via its hard key" -- that described a broader
design that was never built; DISPLAY_SPECS is the actual, current scope. See
the CONNECT_EDGES/ENTITY_INDEX scope-mismatch fix in discover.py for the
edge-generation side of the same gap.)
"""

from __future__ import annotations


def table_keys(spec: dict) -> list[tuple[str, str]]:
    """All (key_type, key_col) pairs a table contributes to the spine: the
    primary key, plus any extra_keys. Single source of truth so spine.py /
    entity_index.py / incremental.py never hand-roll this loop differently."""
    out = [(spec["key"], spec["key_col"])]
    out += [(e["key"], e["key_col"]) for e in spec.get("extra_keys", [])]
    return out


DISPLAY_SPECS: dict[str, dict] = {
    "FED_CMS_NPPES": {
        "key": "NPI", "key_col": "NPI",
        # Single-underscore names are the LIVE schema after the 2026-07-12
        # NPPES re-land (verified against INFORMATION_SCHEMA 2026-07-20; the
        # old double-underscore names crashed the spine — AUDIT 07-14 §B.2).
        "person": ["PROVIDER_LAST_NAME_LEGAL_NAME", "PROVIDER_FIRST_NAME"],
        "org": "PROVIDER_ORGANIZATION_NAME_LEGAL_BUSINESS_NAME",
        "city": "PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME",
        "state": "PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME",
        "zip": "PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE",
        "authority": 1,
    },
    # FED_CMS_FACILITY_AFFILIATION re-added 2026-07-25: table restored with 2.2M rows
    # (previously removed 2026-07-20 when it appeared empty; re-ingested since then).
    "FED_CMS_FACILITY_AFFILIATION": {
        "key": "NPI", "key_col": "NPI",
        "person": ["PROVIDER_LAST_NAME", "PROVIDER_FIRST_NAME"],
        "city": None, "state": None, "zip": None,
        "extra": {"ccn": "CCN", "facility_type": "FACILITY_TYPE"},
        "authority": 3,
    },
    "FED_HHS_OIG_LEIE": {
        # 2026-07-28 audit + repair pass: only 10.4% of rows carry a usable NPI
        # (89.6% unjoinable by hard ID) -- confirmed a HARD SOURCE LIMITATION, not
        # a pipeline bug. LEIE also carries UPIN and DOB, but neither is a
        # recognized key type anywhere in this codebase's key-tagging system
        # (portal_recon/tag_portal_index.py's KEY_TOKENS has no entry for either),
        # and there's no SSN/license-number column at all. UPIN was retired as a
        # CMS identifier before modern NPPES data, so wiring it would likely add
        # little match value for real build cost. Decision (Chris, this date):
        # document and accept the gap rather than build a new key axis or lean on
        # the gated fuzzy resolver for this population. Revisit if that changes.
        "key": "NPI", "key_col": "NPI",
        "person": ["LASTNAME", "FIRSTNAME"], "org": "BUSNAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "extra": {"excl_type": "EXCLTYPE", "excl_date": "EXCLDATE"},
        "authority": 4,
    },
    "FED_CMS_HOSPITAL_GENERAL": {
        "key": "CCN", "key_col": "CCN", "org": "FACILITY_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_CMS_HOSPICE": {
        "key": "CCN", "key_col": "CCN", "org": "FACILITY_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_CMS_HOME_HEALTH": {
        "key": "CCN", "key_col": "CCN", "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_CMS_IRF": {
        "key": "CCN", "key_col": "CCN", "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_CMS_LTCH": {
        "key": "CCN", "key_col": "CCN", "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_CMS_DIALYSIS": {
        "key": "CCN", "key_col": "CCN", "org": "FACILITY_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_CMS_POS_OTHER": {
        "key": "CCN", "key_col": "CCN", "org": "FAC_NAME",
        "city": "CITY_NAME", "state": "STATE_CD", "zip": "ZIP_CD", "authority": 3,
    },
    "FED_NURSINGHOME411": {           # CCN facility (Care Compare nursing homes, 8th facility type)
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN", "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "authority": 2,   # no ZIP column
    },

    # --- Spine Wiring 2026-07-22: 14 landed-but-unwired tables (RIPPLE_CONNECTION_KEYS_REFERENCE §2) ---
    # Utilization/payment NPI sources -- NPPES (authority=1) still wins names; these
    # only surface when an NPI isn't in NPPES. LAST_ORG_NAME carries either a
    # person's last name or an org's legal name depending on entity type (no
    # separate org column in the CMS utilization files) -- same tradeoff NPPES
    # itself doesn't have, unavoidable given the source schema.
    "FED_CMS_MEDICARE_PROVIDER": {    # NPI provider (Medicare Part B utilization)
        "key": "NPI", "key_col": "NPI",
        "person": ["RNDRNG_PRVDR_LAST_ORG_NAME", "RNDRNG_PRVDR_FIRST_NAME"],
        "city": "RNDRNG_PRVDR_CITY", "state": "RNDRNG_PRVDR_STATE_ABRVTN",
        "zip": "RNDRNG_PRVDR_ZIP5", "authority": 3,
    },
    "FED_CMS_OPEN_PAYMENTS": {        # NPI provider (industry payments, current year)
        "key": "NPI", "key_col": "NPI",
        "person": ["COVERED_RECIPIENT_LAST_NAME", "COVERED_RECIPIENT_FIRST_NAME"],
        "city": "RECIPIENT_CITY", "state": "RECIPIENT_STATE",
        "zip": "RECIPIENT_ZIP_CODE", "authority": 3,
    },
    "FED_CMS_OPEN_PAYMENTS_2022": {   # NPI provider (industry payments, PY2022)
        "key": "NPI", "key_col": "NPI",
        "person": ["COVERED_RECIPIENT_LAST_NAME", "COVERED_RECIPIENT_FIRST_NAME"],
        "city": "RECIPIENT_CITY", "state": "RECIPIENT_STATE",
        "zip": "RECIPIENT_ZIP_CODE", "authority": 3,
    },
    "FED_CMS_OPEN_PAYMENTS_2023": {   # NPI provider (industry payments, PY2023)
        "key": "NPI", "key_col": "NPI",
        "person": ["COVERED_RECIPIENT_LAST_NAME", "COVERED_RECIPIENT_FIRST_NAME"],
        "city": "RECIPIENT_CITY", "state": "RECIPIENT_STATE",
        "zip": "RECIPIENT_ZIP_CODE", "authority": 3,
    },
    "FED_CMS_PART_D_PRESCRIBERS": {   # NPI provider (Part D prescribing, opioid detectors)
        "key": "NPI", "key_col": "NPI",
        "person": ["PRSCRBR_LAST_ORG_NAME", "PRSCRBR_FIRST_NAME"],
        "city": "PRSCRBR_CITY", "state": "PRSCRBR_STATE_ABRVTN",
        "zip": "PRSCRBR_ZIP5", "authority": 3,
    },

    # EIN organization -- a brand-new key axis (no EIN entities existed before this
    # wiring). BMF is the IRS master registry (wins names); 990/Form5500 are
    # self-reported at filing time; REVOCATION is a flag/exclusion source, ranked
    # like LEIE.
    "FED_IRS_BMF": {                  # EIN organization (IRS Business Master File, the registry)
        "key": "EIN", "key_col": "EIN", "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP", "authority": 1,
    },
    "FED_IRS_990": {                  # EIN organization (nonprofit filings)
        "key": "EIN", "key_col": "EIN", "org": "ORGANIZATIONNAME",
        "state": "USADDRESS_STATEABBREVIATIONCD", "zip": "USADDRESS_ZIPCD",
        "authority": 2,   # no CITY column
    },
    "FED_DOL_FORM5500": {             # EIN organization (benefit-plan sponsor)
        "key": "EIN", "key_col": "SPONS_DFE_EIN", "org": "SPONSOR_DFE_NAME",
        "city": "SPONS_DFE_MAIL_US_CITY", "state": "SPONS_DFE_MAIL_US_STATE",
        "zip": "SPONS_DFE_MAIL_US_ZIP", "authority": 3,
    },
    "FED_IRS_REVOCATION": {           # EIN organization (tax-exemption revocation flag)
        "key": "EIN", "key_col": "EIN", "org": "LEGAL_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE", "authority": 4,
    },

    # LEI organization -- also a brand-new key axis. GLEIF is the LEI issuer's own
    # global registry (wins names; address fields are dot-notation XML paths).
    # HMDA carries LEI but no lender-name column at all (loan-level records only
    # identify the lender by LEI) -- it contributes membership only, never a name.
    "INTL_GLEIF": {                   # LEI organization (the authoritative global LEI registry)
        "key": "LEI", "key_col": "LEI", "org": "Entity.LegalName",
        "city": "Entity.LegalAddress.City",
        "state": "Entity.LegalAddress.Region",
        "zip": "Entity.LegalAddress.PostalCode",
        "authority": 1,
    },
    "FED_CFPB_HMDA": {                # LEI organization (mortgage lending; no lender-name column)
        "key": "LEI", "key_col": "LEI", "state": "STATE_CODE", "authority": 6,
    },

    # ICPSR person (roll-call votes; no name column -- BIONAME lives on FED_VOTEVIEW_MEMBERS)
    "FED_VOTEVIEW_ROLLCALLS": {
        "key": "ICPSR", "key_col": "ICPSR", "authority": 6,
    },

    # SEC CIK organization -- see Step 2 receipt: FED_SEC_EDGAR (20 distinct CIKs,
    # one ingest run) and FED_US_SEC_EDGAR (48,990 rows but only 25 distinct CIKs,
    # one ingest run) are stale test/sample loads, NOT wired. FINANCIALS is real:
    # 8,112 distinct CIKs (matches the handoff's ~8,160 estimate) loaded across two
    # separate ingest runs -- a broad universe on par with the already-wired ticker
    # table, same authority tier (both are SEC's own data).
    "FED_SEC_EDGAR_FINANCIALS": {     # CIK organization (SEC financial-statement datasets)
        "key": "CIK", "key_col": "CIK", "org": "NAME",
        "city": "CITYBA", "state": "STPRBA", "zip": "ZIPBA", "authority": 5,
    },
    "FED_SEC_13F_SUBMISSIONS": {      # CIK organization (13F institutional holdings filings)
        "key": "CIK", "key_col": "CIK", "authority": 6,
    },

    # --- money / maritime / corporate (2026-06-26: unhealth the spine) ---
    # keys.py already normalizes UEI/CIK/IMO; ENTITY_TYPE_BY_KEY maps them to
    # organization/vessel. Adding these makes a debarred-and-funded UEI, a
    # sanctioned-and-broadcasting IMO, and a SEC CIK first-class multi-source entities.
    "FED_USASPENDING_CONTRACTS": {            # UEI organization (the money anchor, 6.3M rows)
        "key": "UEI", "key_col": "RECIPIENT_UEI", "org": "RECIPIENT_NAME",
        "city": "RECIPIENT_CITY_NAME", "state": "RECIPIENT_STATE_CODE",
        "zip": "RECIPIENT_ZIP_4_CODE", "authority": 4,
    },
    # Repointed 2026-08-11 (spine audit): the spine was still reading the 9,000-row
    # capped sample (2,940 distinct UEIs) three weeks after the complete debarment
    # list landed as ..._FULL_R2 (167,928 rows, 38,425 distinct UEIs -- 13x the
    # linkable banned parties). The dbt lead queue had already been repointed; the
    # connection engine had not, so "banned but still operating" was scored against
    # ~5% of the exclusion list. UEI is populated on 47,684 of 167,928 rows (28%) --
    # excluded individuals mostly have no UEI, which is publisher reality, not loss.
    "FED_SAM_EXCLUSIONS_FULL_R2": {           # UEI organization (the federal debarment flag)
        "key": "UEI", "key_col": "UNIQUE_ENTITY_ID", "org": "NAME",
        "person": ["LAST", "FIRST"],
        "city": "CITY", "state": "STATE_PROVINCE", "zip": "ZIP_CODE", "authority": 5,
    },
    "FED_SEC_EDGAR_COMPANY_TICKERS": {        # CIK organization (public-company spine)
        "key": "CIK", "key_col": "CIK_STR", "org": "TITLE", "authority": 5,
    },
    "FED_OFAC_SDN": {                         # IMO vessel (sanctioned hull) — OFAC name wins
        "key": "IMO", "key_col": "IMO", "org": "SDN_NAME", "authority": 4,
    },
    "FED_NOAA_AIS": {                         # IMO vessel (broadcasting hull, 7.3M rows)
        "key": "IMO", "key_col": "IMO", "org": "VESSELNAME", "authority": 6,
    },
    "FED_DEA_ARCOS_FULL": {                   # DEA_NO organization (opioid distributor/buyer, 380M rows)
        "key": "DEA_NO", "key_col": "REPORTER_DEA_NO", "org": "REPORTER_NAME",
        "city": "REPORTER_CITY", "state": "REPORTER_STATE", "zip": "REPORTER_ZIP",
        "authority": 3,
        "extra_keys": [{"key": "DEA_NO", "key_col": "BUYER_DEA_NO"}],
    },

    # --- politics (2026-07-02: make legislators first-class spine entities) ---
    # BIOGUIDE + ICPSR are now hard keys (keys.py NORM_RULES / discover KEY_DOMAIN).
    # These specs make each member a 'person' entity the graph/dossier can see. The
    # golden source is FED_CONGRESS_LEGISLATORS (BIOGUIDE + split first/last names,
    # most authoritative). Voteview anchors the ICPSR entity with its single BIONAME.
    # The 84M-row itcont table is DELIBERATELY excluded (spine-scan cost); member↔
    # candidate routing is a follow-up via FEC bulk tables.
    "FED_CONGRESS_LEGISLATORS": {             # BIOGUIDE person (golden legislator source)
        "key": "BIOGUIDE", "key_col": "BIOGUIDE",
        "person": ["NAME_LAST", "NAME_FIRST"], "authority": 1,
    },
    "FED_CONGRESS_COMMITTEE_MEMBERSHIP": {    # BIOGUIDE person (committee seats)
        "key": "BIOGUIDE", "key_col": "BIOGUIDE", "org": "MEMBER_NAME", "authority": 3,
    },
    "FED_VOTEVIEW_MEMBERS": {                 # ICPSR person (roll-call member; BIONAME)
        "key": "ICPSR", "key_col": "ICPSR", "org": "BIONAME", "authority": 2,
        # 2026-07-22 upgrade: this row ALSO carries a BIOGUIDE_ID for the same
        # legislator (Voteview cross-walks its own ICPSR id to Congress.gov's
        # BIOGUIDE id). A second, DIFFERENT-typed entity -- spine v1 never fuses
        # ID types (see spine.py docstring) -- so this table now shows up as a
        # source on BOTH the ICPSR entity and the BIOGUIDE entity for that person.
        "extra_keys": [{"key": "BIOGUIDE", "key_col": "BIOGUIDE_ID"}],
    },

    # --- 2026-07-28 repair pass: 11 wired-but-never-spine-ized tables, confirmed
    # live (real columns + a real STEEL key checked against the warehouse) as
    # part of the CONNECT_EDGES/ENTITY_INDEX scope reconciliation. See
    # reports/priority1_table_classification_2026-07-28.md for the full 59-table
    # classification this was drawn from.
    "FED_IRS_990_EFILE_INDEX": {       # EIN organization (the REAL 990 e-file universe,
                                        # 5.5M rows -- FED_IRS_990 above is a 200-row stub)
        "key": "EIN", "key_col": "EIN", "org": "TAXPAYER_NAME", "authority": 2,
    },
    # Dropped 2026-08-11 (spine audit): FCC ULS is one of the platform's documented
    # masked-ID traps -- the EIN column is present on all 1,689,338 rows and carries a
    # usable value on ZERO of them (triage code A6). It contributed no entities, only
    # scan time, and left a dead key looking wired.
    "FED_FAC_SINGLE_AUDIT": {          # EIN organization (federal single-audit clearinghouse,
                                        # auditee only -- AUDITOR_EIN deliberately not wired as
                                        # an extra_key: it's a DIFFERENT entity (the audit firm)
                                        # and would wrongly inherit the auditee's name/address)
        "key": "EIN", "key_col": "AUDITEE_EIN", "org": "AUDITEE_NAME",
        "city": "AUDITEE_CITY", "state": "AUDITEE_STATE", "zip": "AUDITEE_ZIP",
        "authority": 5,
        "extra_keys": [{"key": "UEI", "key_col": "AUDITEE_UEI"}],  # same auditee, same row -- safe
    },
    # Dropped 2026-08-11 (spine audit): FED_NCUA_CALL_REPORTS held NCUA's account
    # DICTIONARY, not call reports (2026-08-11 repair, triage code A3) -- its EIN
    # column was 100% empty, so this spec contributed dead keys. The correct data
    # reloaded as FED_NCUA_CALL_REPORTS_FOICU / _FS220, and NEITHER carries an EIN
    # or any other hard ID in our vocabulary (CU_NUMBER is an NCUA-internal charter
    # number, not a cross-source key). Credit unions therefore have no spine entry
    # until a real bridge exists; a dead key posing as a live one is worse than none.
    "FED_CMS_HCRIS": {                 # CCN facility (hospital cost reports)
        "key": "CCN", "key_col": "PROVIDER_CCN", "org": "HOSPITAL_NAME",
        "city": "CITY", "state": "STATE_CODE", "zip": "ZIP_CODE", "authority": 3,
    },
    "FED_CMS_NURSING_HOME": {          # CCN facility -- added ALONGSIDE FED_NURSINGHOME411
                                        # above (2026-07-28: prior audit flagged these as a
                                        # possible-duplicate pair; not resolving which is more
                                        # complete this pass, so both feed the CCN axis at the
                                        # same authority tier). Its NPI column was confirmed
                                        # phantom (source has no NPI field; removed 2026-08-08).
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER__CCN", "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE", "authority": 2,
    },
    "FED_GOVINFO_BILL_COSPONSORS": {   # BIOGUIDE person (bill cosponsor listings)
        "key": "BIOGUIDE", "key_col": "COSPONSOR_BIOGUIDE", "org": "COSPONSOR_NAME",
        "state": "COSPONSOR_STATE", "authority": 6,
    },
    "FED_GOVINFO_BILLSTATUS": {        # BIOGUIDE person (bill sponsor)
        "key": "BIOGUIDE", "key_col": "SPONSOR_BIOGUIDE", "org": "SPONSOR_NAME", "authority": 6,
    },
    "FED_CMS_PARTD_PRESCRIBER_DRUG": { # NPI provider (Part D prescribing, drug-level grain --
                                        # companion to FED_CMS_PART_D_PRESCRIBERS above, same
                                        # NPI axis, adds table-membership breadth not a new axis)
        "key": "NPI", "key_col": "Prscrbr_NPI",   # source columns are mixed-case, must match exactly
        "person": ["Prscrbr_Last_Org_Name", "Prscrbr_First_Name"],
        "city": "Prscrbr_City", "state": "Prscrbr_State_Abrvtn", "authority": 3,
    },
    # Dropped 2026-08-11 (spine audit): NSF does not publish awardee EINs -- 0 of 125
    # rows carry one (triage code A6). Same reasoning as FCC ULS above.
    "FED_SEC_INSIDER_REPORTINGOWNER": {  # CIK organization/person (insider filer identity --
                                          # raw column is RPTOWNERCIK, no separator, which is why
                                          # the automated tagger missed it as a key on this table)
        "key": "CIK", "key_col": "RPTOWNERCIK", "org": "RPTOWNERNAME",
        "city": "RPTOWNER_CITY", "state": "RPTOWNER_STATE", "zip": "RPTOWNER_ZIPCODE",
        "authority": 6,
    },
    # =========================================================================
    # 2026-07-30 WAVE 1 — new populations (OSHA employers, IRS orgs, CMS enrollments)
    # Generated by scripts/gen_spine_specs.py --wave 1, verified against live data.
    # =========================================================================
    "FED_USASPENDING_ASSISTANCE_FULL": {
        # UEI -- 223,721 distinct / 7,788,545 rows (39.13% survive norm), +175,699 new to spine. len 12-12. e.g. Z9Z8L67WXJ85
        "key": "UEI", "key_col": "recipient_uei",
        "org": "recipient_name",
        "authority": 6,
    },
    "FED_OSHA_ITA_CASE_DETAIL_2024": {
        # EIN -- 15,659 distinct / 455,271 rows (91.05% survive norm), +12,243 new to spine. len 9-9. e.g. 742489930
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_IRS_AUTO_REVOCATIONS": {
        # EIN -- 488,994 distinct / 500,000 rows (100.0% survive norm), +15 new to spine. len 9-9. e.g. 002028280
        "key": "EIN", "key_col": "EIN",
        "org": "LEGAL_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_CASE_DETAIL_2023": {
        # EIN -- 24,931 distinct / 445,616 rows (89.12% survive norm), +20,908 new to spine. len 9-9. e.g. 240837325
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_IRS_PUB78_ELIGIBLE_DONEES": {
        # EIN -- 500,000 distinct / 500,000 rows (100.0% survive norm), +3,301 new to spine. len 9-9. e.g. 000587764
        "key": "EIN", "key_col": "EIN",
        "org": "LEGAL_NAME",
        "city": "CITY", "state": "STATE",
        "authority": 6,
    },
    "FED_OSHA_ITA_300A_SUMMARY_2024": {
        # EIN -- 114,605 distinct / 355,358 rows (89.15% survive norm), +101,536 new to spine. len 9-9. e.g. 823106264
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_300A_SUMMARY_2023": {
        # EIN -- 123,210 distinct / 353,304 rows (89.62% survive norm), +109,301 new to spine. len 9-9. e.g. 340892675
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_300A_SUMMARY_2025": {
        # EIN -- 106,219 distinct / 339,964 rows (88.7% survive norm), +93,993 new to spine. len 9-9. e.g. 205134864
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_OSHA_ITA_CASE_DETAIL_2025": {
        # EIN -- 13,387 distinct / 293,328 rows (88.77% survive norm), +10,322 new to spine. len 9-9. e.g. 430652671
        "key": "EIN", "key_col": "EIN",
        "org": "COMPANY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS": {
        # NPI -- 14,421 distinct / 14,425 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1477576346
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 14,251 distinct, +15 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS": {
        # NPI -- 11,467 distinct / 11,508 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1457434003
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 11,413 distinct, +197 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_FEDERALLY_QUALIFIED_HEALTH_CENTER_ENROLLMENTS": {
        # NPI -- 10,269 distinct / 11,063 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1700888542
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 9,955 distinct, +149 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_HOSPITAL_ENROLLMENTS": {
        # NPI -- 8,717 distinct / 9,175 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1114984671
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 5,966 distinct, +14 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_HOSPICE_ENROLLMENTS": {
        # NPI -- 6,056 distinct / 6,066 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1548201957
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 4,798 distinct, +43 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_CMS_RURAL_HEALTH_CLINIC_ENROLLMENTS": {
        # NPI -- 5,320 distinct / 5,530 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1497791511
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        # extra: CCN -- 5,313 distinct, +45 new to spine
        "extra_keys": [{"key": "CCN", "key_col": "CCN"}],
        "authority": 6,
    },
    "FED_IRS_SOI_CHARITIES": {
        # EIN -- 2,450 distinct / 2,450 rows (100.0% survive norm), +16 new to spine. len 9-9. e.g. 010880225
        "key": "EIN", "key_col": "EIN",
        "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    # =========================================================================
    # 2026-07-30 WAVE 2 — new key axes (MINE_ID, FRS_ID, PWSID, FEC)
    # Generated by scripts/gen_spine_specs.py --wave 2, verified against live data.
    # =========================================================================
    "FED_FEC_INDIV_CONTRIBUTIONS": {
        # FEC_CMTE_ID -- 12,291 distinct / 84,172,112 rows (100.0% survive norm), +12,291 new to spine. len 9-9. e.g. C00458000
        # NO name/address here (2026-08-11 connection audit): the entity keyed by
        # CMTE_ID is the COMMITTEE, but every column on a contribution row describes
        # the DONOR -- name, city, state, ZIP all belong to the person who gave the
        # money. Letting them survive named 3,883 committees after a donor (e.g. the
        # committee HISPANIC 100 FED PAC carrying "LUCKEY, PALMER"). The membership
        # edge is real and stays; only the labelling was wrong.
        "key": "FEC_CMTE_ID", "key_col": "CMTE_ID",
        "authority": 9,
    },
    "FED_MSHA_VIOLATIONS": {
        # MINE_ID -- 31,277 distinct / 3,087,266 rows (100.0% survive norm), +31,277 new to spine. len 7-7. e.g. 0101552
        "key": "MINE_ID", "key_col": "MINE_ID",
        "org": "MINE_NAME",
        "authority": 3,
    },
    "FED_EPA_FRS_FULL": {
        # FRS_ID -- 5,300,149 distinct / 5,300,149 rows (100.0% survive norm), +5,300,149 new to spine. len 12-12. e.g. 110006098310
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "PRIMARY_NAME",
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "POSTAL_CODE",
        "authority": 2,
    },
    "FED_EPA_ECHO": {
        # FRS_ID -- 3,135,553 distinct / 3,135,553 rows (99.29% survive norm), +3,135,553 new to spine. len 12-12. e.g. 110051925538
        "key": "FRS_ID", "key_col": "FRS_ID",
        "org": "FAC_NAME",
        "city": "FAC_CITY", "state": "FAC_STATE",
        "authority": 6,
        # SDWA_IDS (2026-08-18 sniffer batch): for drinking-water rows the ECHO
        # facility IS the public water system -- same entity, so sharing
        # FAC_NAME is correct, not the buyer_dea_no mislabeling. Proven live:
        # 430,991 of the spine's 434,040 distinct PWSIDs (99.3%) appear here.
        # Column is plural-named; rows holding several IDs fail the fixed-9
        # normalizer and drop -- the safe direction.
        "extra_keys": [{"key": "PWSID", "key_col": "SDWA_IDS"}],
    },
    "FED_FEC_COMMITTEE_TO_CANDIDATE": {
        # FEC_CMTE_ID -- 6,270 distinct / 866,730 rows (100.0% survive norm), +6,270 new to spine. len 9-9. e.g. C00325324
        # NO name/address here (2026-08-11 connection audit): the entity keyed by
        # CMTE_ID is the COMMITTEE, but every column on a contribution row describes
        # the DONOR -- name, city, state, ZIP all belong to the person who gave the
        # money. Letting them survive named 3,883 committees after a donor (e.g. the
        # committee HISPANIC 100 FED PAC carrying "LUCKEY, PALMER"). The membership
        # edge is real and stays; only the labelling was wrong.
        "key": "FEC_CMTE_ID", "key_col": "CMTE_ID",
        "authority": 9,
        # OTHER_ID (2026-08-18 sniffer batch): the transaction's counterpart
        # committee, proven a live FEC_CMTE_ID by value overlap (63.3%,
        # reports/value_shape_findings_2026-08-18.md). Same ARCOS-style
        # same-type second column; this table declares NO name/address (see
        # above), so the extra key can mislabel nothing.
        "extra_keys": [{"key": "FEC_CMTE_ID", "key_col": "OTHER_ID"}],
    },
    "FED_MSHA_ACCIDENTS": {
        # MINE_ID -- 13,489 distinct / 273,623 rows (100.0% survive norm), +13,489 new to spine. len 7-7. e.g. 1400413
        "key": "MINE_ID", "key_col": "MINE_ID",
        "authority": 4,
    },
    "FED_EPA_SDWA_SDWA_FACILITIES": {
        # PWSID -- 139,527 distinct / 500,000 rows (100.0% survive norm), +139,527 new to spine. len 9-9. e.g. 020010464
        # NO name here (2026-08-11 connection audit): PWSID identifies the water
        # SYSTEM; this table lists the wells, tanks and intakes INSIDE it, many per
        # system. With authority 2 it outranked the system register and named
        # 430,916 of 434,040 public water systems after one of their own wells
        # ("WELL #1", "LA1055063#01"). The rows still belong to the system -- they
        # are its facilities -- but a child row may never name its parent.
        "key": "PWSID", "key_col": "PWSID",
        "authority": 9,
    },
    "FED_EPA_FRS_FRS_SIC_CODES": {
        # FRS_ID -- 367,837 distinct / 500,000 rows (100.0% survive norm), +367,837 new to spine. len 12-12. e.g. 110000307739
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS": {
        # FRS_ID -- 27,372 distinct / 500,000 rows (100.0% survive norm), +27,372 new to spine. len 12-12. e.g. 110000314936
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_SITE_VISITS": {
        # PWSID -- 44,779 distinct / 500,000 rows (100.0% survive norm), +44,779 new to spine. len 9-9. e.g. 020000001
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS": {
        # FRS_ID -- 100,507 distinct / 499,984 rows (100.0% survive norm), +100,507 new to spine. len 12-12. e.g. 110006791187
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT": {
        # PWSID -- 15,282 distinct / 500,000 rows (100.0% survive norm), +15,282 new to spine. len 9-9. e.g. 010307001
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_FRS_FRS_PROGRAM_LINKS": {
        # FRS_ID -- 464,049 distinct / 500,000 rows (100.0% survive norm), +464,049 new to spine. len 12-12. e.g. 110001930386
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "PRIMARY_NAME",
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "POSTAL_CODE",
        "authority": 6,
    },
    "FED_EPA_FRS_FRS_NAICS_CODES": {
        # FRS_ID -- 356,856 distinct / 499,904 rows (99.98% survive norm), +356,856 new to spine. len 12-12. e.g. 110000460117
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_NPDES_NPDES_INSPECTIONS": {
        # FRS_ID -- 132,341 distinct / 499,970 rows (99.99% survive norm), +132,341 new to spine. len 12-12. e.g. 110020436125
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_LCR_SAMPLES": {
        # PWSID -- 47,068 distinct / 500,000 rows (100.0% survive norm), +47,068 new to spine. len 9-9. e.g. 020000012
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_FEC_BULK_COMMITTEES": {
        # FEC_CMTE_ID -- 20,007 distinct / 20,007 rows (100.0% survive norm), +20,007 new to spine. len 9-9. e.g. C00017681
        "key": "FEC_CMTE_ID", "key_col": "FEC_CMTE_ID",
        "org": "CMTE_NM",
        "city": "CMTE_CITY", "state": "CMTE_ST", "zip": "CMTE_ZIP",
        "authority": 6,
    },
    "FED_FEC_BULK_CANDIDATES": {
        # FEC_CAND_ID -- 13,240 distinct / 17,900 rows (100.0% survive norm), +13,240 new to spine. len 9-9. e.g. H0AK00105
        "key": "FEC_CAND_ID", "key_col": "CAND_ID",
        "org": "CAND_NAME",
        "authority": 6,
    },
    # =========================================================================
    # 2026-08-05 ingestion-sweep wiring -- UK beneficial ownership (COMPANY_NO axis).
    # Verified live 2026-08-05 with the spine's own normalizer before wiring:
    # both columns uniformly 8 chars, 2,335,951 distinct company numbers overlap
    # between the two tables (the PSC->company ownership bridge).
    # =========================================================================
    "INT_UK_COMPANIES_HOUSE": {
        # COMPANY_NO -- 5,734,779 distinct / 5,734,779 surviving rows (one NULL row),
        # len 8-8. e.g. '13163455', 'NI626580'. IS the UK company registry -> authority 2.
        "key": "COMPANY_NO", "key_col": "CompanyNumber",
        "org": "CompanyName",
        "city": "RegAddress.PostTown", "zip": "RegAddress.PostCode",
        "authority": 2,
    },
    "UK_COMPANIES_HOUSE_PSC": {
        # COMPANY_NO -- 5,107,915 distinct / 7,000,000 rows (100% survive norm, len 8-8).
        # e.g. '14551527', 'SC316600'. Grain = (company, controlling person); NAME here
        # is the PSC (owner), NOT the company -- deliberately NOT wired as org so the
        # golden record never labels a company with its owner's name. Membership only.
        "key": "COMPANY_NO", "key_col": "COMPANY_NUMBER",
        "authority": 6,
    },
    "FED_FEC_BULK_SUMMARY": {
        # FEC_CAND_ID -- 5,754 distinct / 7,933 rows (100.0% survive norm), +5,754 new to spine. len 9-9. e.g. H2AK01083
        "key": "FEC_CAND_ID", "key_col": "CAND_ID",
        "org": "CAND_NAME",
        "authority": 6,
    },
    # =========================================================================
    # 2026-08-05 WAVE 3 -- ingestion-sweep breadth pass. Generated by
    # scripts/gen_spine_specs.py --all, every key verified against live data
    # (evidence: outputs/spine_wiring_evidence.csv, rejects in _rejects.csv).
    # FED_SEC_EDGAR / FED_US_SEC_EDGAR excluded: 2026-07-28 ruled them stale
    # test loads, deliberately NOT wired (see FED_SEC_EDGAR_FINANCIALS note).
    # =========================================================================
    "INTL_GLEIF_REPEX": {
        # LEI -- 3,142,660 distinct / 6,259,489 rows (100.0% survive norm), +2,288 new to spine. len 20-20. e.g. 549300WO7OWX61PJ9L13
        "key": "LEI", "key_col": "LEI",
        "authority": 6,
    },
    "FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY": {
        # CCN -- 232 distinct / 495,726 rows (99.15% survive norm), +0 new to spine. len 6-6. e.g. 015015
        "key": "CCN", "key_col": "CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_CMS_ORDER_AND_REFERRING": {
        # NPI -- 2,018,350 distinct / 2,018,354 rows (100.0% survive norm), +1,439 new to spine. len 10-10. e.g. 1427676618
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS": {
        # PWSID -- 413,877 distinct / 578,198 rows (100.0% survive norm), +264,183 new to spine. len 9-9. e.g. NH1835020
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_FEE_FOR_SERVICE_PUBLIC_PROVIDER_ENROLLMENT": {
        # NPI -- 2,541,258 distinct / 2,978,925 rows (100.0% survive norm), +322 new to spine. len 10-10. e.g. 1407802119
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "org": "ORG_NAME",
        "state": "STATE_CD",
        "authority": 6,
    },
    "FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING": {
        # NPI -- 2,047,826 distinct / 2,047,828 rows (100.0% survive norm), +1,525 new to spine. len 10-10. e.g. 1639656747
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER_AND_SERVI": {
        # NPI -- 61,879 distinct / 500,000 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1003000126
        "key": "NPI", "key_col": "RNDRNG_NPI",
        "person": ["RNDRNG_PRVDR_LAST_ORG_NAME", "RNDRNG_PRVDR_FIRST_NAME"],
        "city": "RNDRNG_PRVDR_CITY", "state": "RNDRNG_PRVDR_STATE_ABRVTN", "zip": "RNDRNG_PRVDR_ZIP5",
        "authority": 6,
    },
    "FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE": {
        # NPI -- 453,202 distinct / 503,917 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1295197580
        "key": "NPI", "key_col": "NPI",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_DIALYSIS_FACILITIES": {
        # CCN -- 335 distinct / 500,000 rows (100.0% survive norm), +34 new to spine. len 6-6. e.g. 012501
        "key": "CCN", "key_col": "CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY", "state": "STATE",
        # NPI dropped as an identity key 2026-08-11 (connection audit): 69,437 rows
        # of this file carry an INDIVIDUAL's NPI (NPPES entity type 1) rather than
        # the clinic's -- the medical director, most likely -- so the clinic fused
        # with the doctor: "DCI ROCKCASTLE" became the same entity as the Part D
        # prescriber "Rahman, Khalil". A facility merged with a person is the worst
        # class of wrong merge, and CCN already identifies these clinics, so the
        # link is dropped rather than filtered (the spec layer has no row filter).
        "authority": 6,
    },
    "FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER": {
        # NPI -- 1,296,739 distinct / 1,296,739 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1003008095
        "key": "NPI", "key_col": "RNDRNG_NPI",
        "person": ["RNDRNG_PRVDR_LAST_ORG_NAME", "RNDRNG_PRVDR_FIRST_NAME"],
        "city": "RNDRNG_PRVDR_CITY", "state": "RNDRNG_PRVDR_STATE_ABRVTN", "zip": "RNDRNG_PRVDR_ZIP5",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS": {
        # PWSID -- 434,040 distinct / 434,040 rows (100.0% survive norm), +280,388 new to spine. len 9-9. e.g. MN1640004
        # PWS_NAME, not ORG_NAME (2026-08-11 connection audit): ORG_NAME on this
        # register is the contact/owner, frequently a private individual
        # ("ALLEN, FRITZ" for the water system "ARTISAN CENTER OF CORRALES"), so it
        # both mis-named systems and put private people's names into the map.
        # PWS_NAME is the system's own name. Authority raised to 2 so the register
        # names the system, not one of its wells.
        "key": "PWSID", "key_col": "PWSID",
        "org": "PWS_NAME",
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "ZIP_CODE",
        "authority": 2,
    },
    "FED_EPA_SDWA_SDWA_SERVICE_AREAS": {
        # PWSID -- 378,450 distinct / 422,464 rows (100.0% survive norm), +243,657 new to spine. len 9-9. e.g. 020011103
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_CMS_NURSING_HOME_DEFICIENCIES": {
        # CCN -- 14,384 distinct / 413,370 rows (98.78% survive norm), +0 new to spine. len 6-6. e.g. 015012
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_EVENTS_MILESTONES": {
        # PWSID -- 98,555 distinct / 394,075 rows (100.0% survive norm), +55,599 new to spine. len 9-9. e.g. MO6036128
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_SDWA_SDWA_PN_VIOLATION_ASSOC": {
        # PWSID -- 42,034 distinct / 387,627 rows (100.0% survive norm), +29,148 new to spine. len 9-9. e.g. 020000004
        "key": "PWSID", "key_col": "PWSID",
        "authority": 6,
    },
    "FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES": {
        # FRS_ID -- 266,026 distinct / 279,541 rows (99.93% survive norm), +57 new to spine. len 12-12. e.g. 110007133654
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_FEC_INDEPENDENT_EXPENDITURES": {
        # FEC_CAND_ID -- 2,014 distinct / 228,643 rows (87.59% survive norm), +607 new to spine. len 9-9. e.g. P80000722
        "key": "FEC_CAND_ID", "key_col": "cand_id",
        "org": "cand_name",
        "authority": 6,
    },
    "FED_EPA_ICIS_FEC_ICIS_FEC_EPA_INSPECTIONS": {
        # FRS_ID -- 156,326 distinct / 259,137 rows (99.46% survive norm), +2,486 new to spine. len 12-12. e.g. 110070715963
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "FACILITY_NAME",
        "authority": 6,
    },
    "FED_EPA_ICIS_FEC_CASE_FACILITIES": {
        # FRS_ID -- 113,854 distinct / 203,232 rows (99.61% survive norm), +70 new to spine. len 12-12. e.g. 110000318193
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE_CODE", "zip": "ZIP",
        "authority": 6,
    },
    "FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES": {
        # CCN -- 13,687 distinct / 197,027 rows (98.5% survive norm), +0 new to spine. len 6-6. e.g. 015009
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_MSHA_MINES": {
        # MINE_ID -- 91,906 distinct / 91,906 rows (100.0% survive norm), +60,478 new to spine. len 7-7. e.g. 0100099
        "key": "MINE_ID", "key_col": "MINE_ID",
        "state": "STATE",
        "authority": 6,
    },
    "FED_SEC_EDGAR_INSIDERS": {
        # CIK -- 5,306 distinct / 69,259 rows (100.0% survive norm), +190 new to spine. len 10-10. e.g. 0001825079
        "key": "CIK", "key_col": "CIK",
        "authority": 6,
    },
    "FED_CMS_OPT_OUT_AFFIDAVITS": {
        # NPI -- 56,455 distinct / 57,209 rows (100.0% survive norm), +19 new to spine. len 10-10. e.g. 1699854034
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "city": "CITY_NAME", "state": "STATE_CODE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_EPA_ICIS_FEC_EPA_INFORMAL_ENFORCEMENT_ACTIONS": {
        # FRS_ID -- 14,606 distinct / 21,930 rows (100.0% survive norm), +8 new to spine. len 12-12. e.g. 110000308569
        "key": "FRS_ID", "key_col": "REGISTRY_ID",
        "authority": 6,
    },
    "FED_FEC_BULK": {
        # FEC_CMTE_ID -- 20,938 distinct / 20,938 rows (100.0% survive norm), +5,166 new to spine. len 9-9. e.g. C00003764
        "key": "FEC_CMTE_ID", "key_col": "FEC_CMTE_ID",
        "org": "CMTE_NM",
        "city": "CMTE_CITY", "state": "CMTE_ST", "zip": "CMTE_ZIP",
        "authority": 6,
    },
    "FED_FEC_LEADERSHIP_PAC": {
        # FEC_CMTE_ID -- 8,338 distinct / 8,619 rows (100.0% survive norm), +3,464 new to spine. len 9-9. e.g. C00708867
        "key": "FEC_CMTE_ID", "key_col": "FEC_COMMITTEE_ID",
        "authority": 6,
        # FEC_CANDIDATE_ID (2026-08-18 sniffer batch): the leadership PAC's
        # sponsoring candidate -- name-invisible ('candidate' is not the
        # 'cand' token), proven live by 98.4% value overlap. This table
        # declares no name/address, so nothing can be mislabelled onto the
        # candidate entity; the PAC->candidate membership edge is the point.
        "extra_keys": [{"key": "FEC_CAND_ID", "key_col": "FEC_CANDIDATE_ID"}],
    },
    "FED_FEC_BULK_LINKAGES": {
        # FEC_CMTE_ID -- 11,427 distinct / 16,327 rows (100.0% survive norm), +3,493 new to spine. len 9-9. e.g. C00708867
        "key": "FEC_CMTE_ID", "key_col": "CMTE_ID",
        "authority": 6,
    },
    "FED_CMS_NURSING_HOME_PENALTIES": {
        # CCN -- 6,771 distinct / 16,032 rows (99.09% survive norm), +0 new to spine. len 6-6. e.g. 015019
        "key": "CCN", "key_col": "CMS_CERTIFICATION_NUMBER_CCN",
        "org": "PROVIDER_NAME",
        "city": "CITY_TOWN", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q2": {
        # CIK -- 6,250 distinct / 7,675 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000038725
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,745 distinct, +3,714 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS": {
        # NPI -- 7,240 distinct / 7,240 rows (100.0% survive norm), +361 new to spine. len 10-10. e.g. 1215687991
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q2": {
        # CIK -- 6,081 distinct / 7,009 rows (100.0% survive norm), +41 new to spine. len 10-10. e.g. 0001034054
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,509 distinct, +3,523 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS": {
        # NPI -- 6,880 distinct / 6,880 rows (100.0% survive norm), +453 new to spine. len 10-10. e.g. 1245159342
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q3": {
        # CIK -- 6,008 distinct / 6,699 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000002178
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,687 distinct, +3,671 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS": {
        # NPI -- 6,510 distinct / 6,637 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1003046806
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "state": "STATE",
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q3": {
        # CIK -- 5,909 distinct / 6,541 rows (100.0% survive norm), +57 new to spine. len 10-10. e.g. 0000010795
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,495 distinct, +3,511 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q4": {
        # CIK -- 5,833 distinct / 6,491 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0001315257
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,664 distinct, +3,650 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q4": {
        # CIK -- 5,786 distinct / 6,304 rows (100.0% survive norm), +88 new to spine. len 10-10. e.g. 0000002969
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,502 distinct, +3,517 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2025Q1": {
        # CIK -- 5,672 distinct / 6,231 rows (100.0% survive norm), +18 new to spine. len 10-10. e.g. 0000015615
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,306 distinct, +3,316 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2026Q1": {
        # CIK -- 5,750 distinct / 6,169 rows (100.0% survive norm), +95 new to spine. len 10-10. e.g. 0000015847
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,237 distinct, +3,281 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_DERA_SUB_2024Q1": {
        # CIK -- 5,506 distinct / 6,028 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000316888
        "key": "CIK", "key_col": "CIK",
        "org": "NAME",
        # extra: EIN -- 4,239 distinct, +3,234 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_IRS_EO_PR": {
        # EIN -- 2,587 distinct / 2,587 rows (100.0% survive norm), +29 new to spine. len 9-9. e.g. 660356920
        "key": "EIN", "key_col": "EIN",
        "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    "FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS": {
        # NPI -- 1,287 distinct / 1,502 rows (96.41% survive norm), +0 new to spine. len 10-10. e.g. 1003008301
        "key": "NPI", "key_col": "NPI",
        "org": "PROVIDER_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_DIABETES_PREVENTION_PROGRAM": {
        # NPI -- 307 distinct / 1,037 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 1619988144
        "key": "NPI", "key_col": "NPI",
        "org": "ORGANIZATION_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_CLOSED_END_FUND_INFORMATION": {
        # CIK -- 973 distinct / 973 rows (100.0% survive norm), +650 new to spine. len 10-10. e.g. 0000879361
        "key": "CIK", "key_col": "CIK",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    "FED_SEC_BUSINESS_DEVELOPMENT_COMPANY_REPORT": {
        # CIK -- 212 distinct / 212 rows (100.0% survive norm), +72 new to spine. len 10-10. e.g. 0001287032
        "key": "CIK", "key_col": "CIK",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE",
        "authority": 6,
    },
    # 2026-08-26: repointed from FED_USASPENDING_CONTRACTS_FULL (20M-row sampling
    # artifact, superseded) to the real full re-pull -- test_spine_inputs_live.py's
    # shadowed-sibling check caught the old table still being wired here. The old
    # table is flagged for a DROP TABLE (Chris's call, repo policy blocks agents
    # running raw DDL) -- see STATUS.md.
    "FED_USASPENDING_CONTRACTS_FULL_R2": {
        # UEI -- 582,656 distinct / 93,152,192 rows (100.0% survive norm). len 12-12. e.g. KB1EKZ5BXVL8
        "key": "UEI", "key_col": "recipient_uei",
        "org": "recipient_name",
        "authority": 6,
    },
    # ---- 2026-08-26 wave-3 breadth pass (scripts/gen_spine_specs.py --wave 3) ----
    "FED_SAM_EXCLUSIONS": {
        # UEI -- 3,210 distinct / 3,482 rows (34.82% survive norm), +5 new to spine. len 12-12. e.g. GRX8CJ2ZCNL5
        "key": "UEI", "key_col": "UEI",
        "person": ["LAST_NAME", "FIRST_NAME"],
        "org": "ENTITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "authority": 6,
    },
    "IRS527_8871_ORGS": {
        # EIN -- 58,915 distinct / 77,590 rows (100.0% survive norm), +0 new to spine. len 9-9. e.g. 912082049
        "key": "EIN", "key_col": "EIN",
        "org": "ORGANIZATION_NAME",
        "city": "MAILING_CITY", "state": "MAILING_STATE", "zip": "MAILING_ZIP",
        "authority": 6,
    },
    "FED_US_SEC_EDGAR": {
        # CIK -- 25 distinct / 48,990 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0000320193
        "key": "CIK", "key_col": "CIK",
        "org": "ENTITY_NAME",
        # extra: EIN -- 24 distinct, +0 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    "FED_SEC_EDGAR": {
        # CIK -- 20 distinct / 200 rows (100.0% survive norm), +0 new to spine. len 10-10. e.g. 0001318605
        "key": "CIK", "key_col": "CIK",
        # extra: EIN -- 19 distinct, +0 new to spine
        "extra_keys": [{"key": "EIN", "key_col": "EIN"}],
        "authority": 6,
    },
    # ---- 2026-08-26 wave-3b, after the join-key catalog backfill (--apply) ----
    "FED_USASPENDING_BULK": {
        # UEI -- 10,216 distinct / 50,000 rows (100.0% survive norm), +0 new to spine. len 12-12. e.g. LAD2HL1R71Z3
        "key": "UEI", "key_col": "RECIPIENT_UEI",
        "org": "RECIPIENT_NAME",
        "authority": 6,
    },
}

# =========================================================================== #
# 2026-08 SPINE BATCH -- STAGED behind keys.ENABLE_SPINE_BATCH_2026_08
#
# Why staged: adding any of these specs (or their NORM_RULES entries) changes
# the incremental-config fingerprint, which by design freezes connect-one /
# connect-changed until a FULL spine rebuild re-pins it -- and the full rebuild
# is a parked money decision (~$10-15). Flip the flag in the session that runs
# `python -m connect spine`, never before.
#
# Every entry below was VERIFIED LIVE 2026-08-17 before staging -- fill,
# distinct count after the axis's own normalization, and overlap against the
# live entity map (or, for new families, referential match against the family's
# authority table). Evidence: reports/census_grid_2026-08-12/fill/
# courtlistener_edges.json + spine_batch_verification.jsonl.
#
# Measured and REJECTED (do not re-add without new evidence):
#   FED_FCC_LICENSING.EIN            -- 0 of 1.69M rows survive normalization
#                                       (fully masked; the known FCC ULS trap).
#   FED_FDIC_BANK_DATA.LEI           -- 0 nonnull. Dead column.
#   FED_EPA_TRI_FACILITY.FRS_ID      -- 0 nonnull. Dead column (TRI_BASIC_2023
#                                       carries the live FRS values instead).
#   FED_US_SEC_EDGAR (EIN+CIK)       -- only ~25 distinct companies across 49k
#                                       rows; a capped per-company filings feed,
#                                       not a registry.
#   XC_EPA_CORPORATE_CROSSWALK       -- in-house name-match product (98.6% of
#                                       rows unmatched or fuzzy 0.80-0.85; only
#                                       59k "exact"). The spine is hard-ID
#                                       zero-false-merge; this stays an overlay.
#   FED_CMS_OPEN_PAYMENTS_GNRL + FED_IRS_990_EFILER_INDEX_2022/2023 -- live in
#                                       the RETIRED schema; retired on purpose.
#   IRS527_8871_ORGS                 -- byte-identical twin of FED_IRS_527_ORGS
#                                       (same rows/distinct/overlap); wire one.
#   FED_CONGRESS_LEGISLATORS.FEC_IDS -- real values but a JSON ARRAY per row
#                                       ('["S8WA00194","H2WA01054"]'); specs
#                                       address plain columns. Needs a tiny
#                                       flatten crosswalk build; still the
#                                       cheapest big politics unlock.
# --------------------------------------------------------------------------- #

# --- CourtListener (judge + court axes). 19 of 20 surfaces 99.2-100%. -------- #
# POSITIONS.APPOINTER_ID deliberately NOT wired: 47.17% match -- it references
# a different record type than a person; wiring it would manufacture false
# person entities. JUDGES has 394 alias rows (~2.4% thin duplicate persons,
# zero false merges -- specs have no row filter). DOCKETS/POSITIONS declare NO
# name columns on purpose: their name columns are case/org names, and declaring
# them would let a case name win survivorship for a court.
# COURTS.FJC_COURT_ID (200 rows) is a future bridge axis, not wired yet.
COURTLISTENER_DISPLAY_SPECS: dict[str, dict] = {
    "FED_COURTLISTENER_JUDGES": {
        # CL_PERSON_ID -- 16,057 distinct / 16,191 rows, all named. e.g. '370'
        "key": "CL_PERSON_ID", "key_col": "ID",
        "person": ["NAME_LAST", "NAME_FIRST"],
        "authority": 1,
    },
    "FED_COURTLISTENER_COURTS": {
        # CL_COURT_ID -- 3,361 distinct / 3,361 rows, all named. e.g. 'scotus', 'ca9'
        "key": "CL_COURT_ID", "key_col": "ID",
        "org": "FULL_NAME",
        "authority": 1,
    },
    "FED_COURTLISTENER_FINANCIAL_DISCLOSURES": {
        # judge -> disclosure measured 99.82% (29,041/29,092 nonnull person ids)
        "key": "CL_PERSON_ID", "key_col": "PERSON_ID",
        "authority": 5,
    },
    "FED_COURTLISTENER_POSITIONS": {
        # judge -> judgeship 100.0% (51,290 rows); court leg 100.0% (22,183 nonnull).
        # extra_keys carries the court on the same row (the judgeship is the link
        # between a person and a court). APPOINTER_ID deliberately excluded (47%).
        "key": "CL_PERSON_ID", "key_col": "PERSON_ID",
        "extra_keys": [{"key": "CL_COURT_ID", "key_col": "COURT_ID"}],
        "authority": 5,
    },
    "FED_COURTLISTENER_JUDGE_EDUCATIONS": {
        # 100.0% (12,746 nonnull)
        "key": "CL_PERSON_ID", "key_col": "PERSON_ID", "authority": 6,
    },
    "FED_COURTLISTENER_JUDGE_POLITICAL_AFFILIATIONS": {
        # 100.0% (8,486 rows)
        "key": "CL_PERSON_ID", "key_col": "PERSON_ID", "authority": 6,
    },
    "FED_COURTLISTENER_JUDGE_RACES": {
        # 100.0% (6,542 rows)
        "key": "CL_PERSON_ID", "key_col": "PERSON_ID", "authority": 6,
    },
    "FED_COURTLISTENER_DOCKETS": {
        # court -> docket 100.0% on ALL 71,677,647 rows; assigned judge 100.0%
        # on 32.4M nonnull. The judge/court caseload ledger.
        "key": "CL_COURT_ID", "key_col": "COURT_ID",
        "extra_keys": [{"key": "CL_PERSON_ID", "key_col": "ASSIGNED_TO_ID"}],
        "authority": 7,
    },
    "FED_COURTLISTENER_ORIGINATING_COURT_INFO": {
        # judge -> originating assignment 100.0% (32,857 nonnull)
        "key": "CL_PERSON_ID", "key_col": "ASSIGNED_TO_ID", "authority": 7,
    },
}

# --- Existing-axis additions (verified 2026-08-17, spine_batch_verification) -- #
SPINE_BATCH_2026_08_DISPLAY_SPECS: dict[str, dict] = {
    # EIN axis ---------------------------------------------------------------- #
    "FED_IRS_EO_BMF": {
        # 1,983,563 distinct EINs, 99.95% already in the spine -- the IRS
        # exempt-org master file, the golden CHARITY name/address source.
        "key": "EIN", "key_col": "EIN", "org": "NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP", "authority": 3,
    },
    "FED_IRS_527_ORGS": {
        # 58,915 distinct EINs, 0.81% spine overlap -- the 527 political-org
        # universe is NEW entities, which is the finding (dark-money orgs are
        # not the charity/employer population). Twin table IRS527_8871_ORGS
        # excluded (byte-identical stats).
        "key": "EIN", "key_col": "EIN", "org": "ORG_NAME",
        "city": "MAIL_CITY", "state": "MAIL_STATE", "zip": "MAIL_ZIP",
        "authority": 4,
    },
    "IRS527_8872_REPORTS": {
        # 4,150 distinct filer EINs (periodic money reports).
        "key": "EIN", "key_col": "EIN", "org": "ORGANIZATION_NAME",
        "city": "MAILING_CITY", "state": "MAILING_STATE", "zip": "MAILING_ZIP",
        "authority": 6,
    },
    "IRS527_DIRECTORS_OFFICERS": {
        # EIN is the ORG's tax id; ORG_NAME is its name. ENTITY_NAME (the
        # officer) deliberately not declared -- a person must not name the org.
        "key": "EIN", "key_col": "EIN", "org": "ORG_NAME", "authority": 8,
    },
    "IRS527_RELATED_ENTITIES": {
        "key": "EIN", "key_col": "EIN", "org": "ORG_NAME", "authority": 8,
    },
    "FED_DOL_EBSA_FORM5500_SCHEDULE_SB": {
        # 39,581 distinct sponsor EINs on actuarial filings (the pension
        # paper-trail leg). No name columns on the table.
        "key": "EIN", "key_col": "SB_EIN", "authority": 8,
    },
    "FED_PBGC_TRUSTEED_PENSION_PLANS": {
        # 20,835 distinct EINs -- failed-pension plans (admin detail vintage).
        "key": "EIN", "key_col": "EIN", "org": "PLAN_SPONSOR_NAME",
        "city": "ADMIN_CITY", "state": "ADMIN_STATE", "authority": 5,
    },
    "FED_PBGC_TRUSTEED_PLANS": {
        # 4,431 distinct EINs, 100% populated (verified 2026-08-17 incl.
        # leading-zero repair via pad-9 normalization). The sharpest harm
        # chain's pension leg.
        "key": "EIN", "key_col": "EIN", "org": "SPONSOR_NAME",
        "city": "CITY", "state": "STATE", "authority": 5,
    },
    "FED_COURTLISTENER_SCHOOLS": {
        # 2,569 distinct EINs (71.9% in spine): judges' schools join the tax
        # world -- the education-to-money bridge.
        "key": "EIN", "key_col": "EIN", "org": "NAME", "authority": 6,
    },
    # NPI axis ---------------------------------------------------------------- #
    "FED_CMS_PECOS_PROVIDER_ENROLLMENT": {
        # 2,541,258 distinct NPIs, 100.0% spine overlap -- Medicare enrollment.
        "key": "NPI", "key_col": "NPI",
        "person": ["LAST_NAME", "FIRST_NAME"], "org": "ORG_NAME",
        "authority": 3,
    },
    "FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT": {
        # 1,681,790 distinct NPIs, ~100% overlap -- pharma-payment recipient
        # profiles.
        "key": "NPI", "key_col": "COVERED_RECIPIENT_NPI",
        "person": ["COVERED_RECIPIENT_PROFILE_LAST_NAME",
                   "COVERED_RECIPIENT_PROFILE_FIRST_NAME"],
        "city": "COVERED_RECIPIENT_PROFILE_CITY",
        "state": "COVERED_RECIPIENT_PROFILE_STATE",
        "zip": "COVERED_RECIPIENT_PROFILE_ZIPCODE", "authority": 5,
    },
    "FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL": {
        # 55,598 distinct supplier NPIs, 100% overlap. LAST_NAME_ORG is a
        # mixed person/org surname column -- person-pattern keeps it honest.
        "key": "NPI", "key_col": "SUPLR_NPI",
        "person": ["SUPLR_PRVDR_LAST_NAME_ORG", "SUPLR_PRVDR_FIRST_NAME"],
        "city": "SUPLR_PRVDR_CITY", "state": "SUPLR_PRVDR_STATE_ABRVTN",
        "zip": "SUPLR_PRVDR_ZIP5", "authority": 7,
    },
    "FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_REFER": {
        # 381,228 distinct referring NPIs, 100% overlap.
        "key": "NPI", "key_col": "RFRG_NPI",
        "person": ["RFRG_PRVDR_LAST_NAME_ORG", "RFRG_PRVDR_FIRST_NAME"],
        "city": "RFRG_PRVDR_CITY", "state": "RFRG_PRVDR_STATE_ABRVTN",
        "zip": "RFRG_PRVDR_ZIP5", "authority": 7,
    },
    "FED_HRSA_UDS_SERVICE_DELIVERY_SITES": {
        # 6,047 distinct community-health-center site NPIs, 99.27% overlap.
        "key": "NPI", "key_col": "FQHC_SITE_NPI_NUMBER", "org": "SITE_NAME",
        "city": "SITE_CITY", "state": "SITE_STATE_ABBREVIATION",
        "zip": "SITE_POSTAL_CODE", "authority": 6,
    },
    # CCN axis ---------------------------------------------------------------- #
    "FED_CMS_MEDICARE_INPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE": {
        # 2,906 distinct hospital CCNs, 100% overlap -- inpatient price book.
        "key": "CCN", "key_col": "RNDRNG_PRVDR_CCN",
        "org": "RNDRNG_PRVDR_ORG_NAME", "city": "RNDRNG_PRVDR_CITY",
        "state": "RNDRNG_PRVDR_STATE_ABRVTN", "zip": "RNDRNG_PRVDR_ZIP5",
        "authority": 6,
    },
    "FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE": {
        # 3,126 distinct hospital CCNs, 100% overlap -- outpatient price book.
        "key": "CCN", "key_col": "RNDRNG_PRVDR_CCN",
        "org": "RNDRNG_PRVDR_ORG_NAME", "city": "RNDRNG_PRVDR_CITY",
        "state": "RNDRNG_PRVDR_STATE_ABRVTN", "zip": "RNDRNG_PRVDR_ZIP5",
        "authority": 6,
    },
    # UEI + DUNS (same row = same recipient, the legit extra_keys case; these
    # are the spine's FIRST DUNS entities -- ENTITY_MAP holds zero today, so
    # each table also becomes a UEI<->DUNS old/new-ID crosswalk for free) ----- #
    "FED_NIH_REPORTER": {
        # 11,903 distinct UEIs (87.4% in spine) / 14,919 distinct DUNS.
        "key": "UEI", "key_col": "ORG_UEI", "org": "ORG_NAME",
        "city": "ORG_CITY", "state": "ORG_STATE", "zip": "ORG_ZIP",
        "extra_keys": [{"key": "DUNS", "key_col": "ORG_DUNS"}],
        "authority": 6,
    },
    "FED_SBIR_STTR_AWARDS": {
        # 17,160 distinct UEIs (76.1% in spine) / 21,594 distinct DUNS.
        "key": "UEI", "key_col": "UEI", "org": "COMPANY",
        "city": "CITY", "state": "STATE", "zip": "ZIP",
        "extra_keys": [{"key": "DUNS", "key_col": "DUNS"}],
        "authority": 6,
    },
    # CIK axis ---------------------------------------------------------------- #
    "FED_PCAOB_FORM_AP_FILINGS": {
        # 28,773 distinct issuer CIKs (35.7% in spine; funds are new) -- the
        # auditor-engagement bridge.
        "key": "CIK", "key_col": "ISSUER_CIK", "org": "ISSUER_NAME",
        "authority": 6,
    },
    "FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS": {
        # 2,046 distinct fund-family CIKs (mostly new to the spine).
        "key": "CIK", "key_col": "CIK_NUMBER", "org": "ENTITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE", "authority": 7,
    },
    "FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE": {
        # 7,998 distinct CIKs, 98.2% overlap -- the listed-company ticker map.
        "key": "CIK", "key_col": "CIK", "org": "NAME", "authority": 6,
    },
    # LEI / IMO --------------------------------------------------------------- #
    "INTL_ISO_MIC_REGISTRY": {
        # 1,060 distinct exchange-operator LEIs, 99.91% overlap.
        "key": "LEI", "key_col": "LEI", "org": "LEGAL_ENTITY_NAME",
        "authority": 6,
    },
    "INTL_UK_SANCTIONS_LIST": {
        # 657 distinct sanctioned-vessel IMOs (45.5% seen broadcasting/OFAC).
        # Names deliberately not declared: the list splits names across six
        # columns; OFAC (authority 4) already names hulls.
        "key": "IMO", "key_col": "IMO_NUMBER", "authority": 7,
    },
    # FRS_ID axis ------------------------------------------------------------- #
    "FED_EPA_FRS_FRS_FACILITIES": {
        # 3,277,557 distinct registry IDs, 100.0% overlap -- the EPA facility
        # registry itself; second-most-authoritative name source for the axis.
        "key": "FRS_ID", "key_col": "REGISTRY_ID", "org": "FAC_NAME",
        "city": "FAC_CITY", "state": "FAC_STATE", "zip": "FAC_ZIP",
        "authority": 2,
    },
    "FED_EPA_ICIS_ICIS_AIR_FACILITIES": {
        # 266,026 distinct, 100.0% overlap -- air-program facilities.
        "key": "FRS_ID", "key_col": "REGISTRY_ID", "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE", "authority": 6,
    },
    "FED_EPA_GHGRP_FACILITY": {
        # 13,221 distinct, 83.1% overlap -- greenhouse-gas reporters.
        "key": "FRS_ID", "key_col": "FRS_ID", "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP", "authority": 6,
    },
    "FED_EPA_TRI_BASIC_2023": {
        # 21,760 distinct, 99.4% overlap -- toxics-release reporters.
        "key": "FRS_ID", "key_col": "C_3_FRS_ID", "org": "C_4_FACILITY_NAME",
        "city": "C_6_CITY", "zip": "C_9_ZIP", "authority": 7,
    },
    # NPDES_ID family (water-discharge permits; 100.0% referential on all
    # seven event tables vs the 1.21M-facility authority) --------------------- #
    "FED_EPA_NPDES_ICIS_FACILITIES": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "org": "FACILITY_NAME",
        "city": "CITY", "state": "STATE_CODE", "zip": "ZIP", "authority": 4,
    },
    "FED_EPA_NPDES_NPDES_CS_VIOLATIONS": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    "FED_EPA_NPDES_NPDES_PS_VIOLATIONS": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    "FED_EPA_NPDES_NPDES_SE_VIOLATIONS": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    "FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    "FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    "FED_EPA_NPDES_NPDES_INSPECTIONS": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    "FED_EPA_NPDES_NPDES_QNCR_HISTORY": {
        "key": "NPDES_ID", "key_col": "NPDES_ID", "authority": 8,
    },
    # NCUA_CHARTER family (credit unions) ------------------------------------- #
    "FED_NCUA_FEDERALLY_INSURED_CU_LIST": {
        # 4,212 distinct charters -- the insured-CU registry, golden names.
        "key": "NCUA_CHARTER", "key_col": "CHARTER_NUMBER",
        "org": "CREDIT_UNION_NAME", "city": "CITY_MAILING_ADDRESS",
        "state": "STATE_MAILING_ADDRESS", "zip": "ZIP_CODE_MAILING_ADDRESS",
        "authority": 4,
    },
    "FED_NCUA_CALL_REPORTS_FOICU": {
        # 4,289 distinct, 98.0% vs insured list (the gap: recently merged-away
        # charters -- expected, not error).
        "key": "NCUA_CHARTER", "key_col": "CU_NUMBER", "org": "CU_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP_CODE", "authority": 5,
    },
    "FED_NCUA_CALL_REPORTS_FS220": {
        "key": "NCUA_CHARTER", "key_col": "CU_NUMBER", "authority": 8,
    },
    "FED_NCUA_CHARTER_MERGER_EVENTS": {
        # Both sides of every merger. Names deliberately NOT declared: extra
        # keys share the table's name expression, so declaring the continuing
        # CU's name would also label the merged-away CU with it.
        "key": "NCUA_CHARTER", "key_col": "CONTINUING_CREDIT_UNION_CHARTER",
        "extra_keys": [{"key": "NCUA_CHARTER",
                        "key_col": "MERGING_CREDIT_UNION_CHARTER"}],
        "authority": 8,
    },
    # ICE_FACILITY family (detention) ----------------------------------------- #
    "FED_ICE_DETENTION_FACILITY_CODES": {
        # 1,470 distinct codes with names/addresses -- the authority table.
        "key": "ICE_FACILITY", "key_col": "DETENTION_FACILITY_CODE",
        "org": "DETENTION_FACILITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP", "authority": 4,
    },
    "FED_ICE_DETENTION_STINTS": {
        # 2.6M stints, 100.0% referential to the code list -- detention
        # outcomes by operator, per facility.
        "key": "ICE_FACILITY", "key_col": "DETENTION_FACILITY_CODE",
        "authority": 8,
    },
}


def _maybe_enable_spine_batch() -> None:
    # This module is imported BOTH as connect.entity_index_specs (package) and as
    # a top-level module (spine_entity.py path-hacks connect/ onto sys.path), so
    # the relative import needs a bare fallback. The flag is a module constant
    # read once at import; both import identities see the same source default.
    try:
        from .keys import ENABLE_SPINE_BATCH_2026_08
    except ImportError:
        from keys import ENABLE_SPINE_BATCH_2026_08
    if ENABLE_SPINE_BATCH_2026_08:
        DISPLAY_SPECS.update(COURTLISTENER_DISPLAY_SPECS)
        DISPLAY_SPECS.update(SPINE_BATCH_2026_08_DISPLAY_SPECS)

_maybe_enable_spine_batch()

# =========================================================================== #
# 2026-08-18 VALUE-SHAPE SNIFFER BATCH -- Chris approved wiring same day.
# Found by live VALUE overlap, not names (the names are exactly what detection
# could not see). Evidence: reports/value_shape_findings_2026-08-18.md.
#
# The four FEC history tables below load with POSITIONAL headers (C1..Cn) --
# the raw FEC bulk-file layouts, column meanings verified against live sample
# rows 2026-08-18. They are the MULTI-CYCLE supersets of the wired single-cycle
# twins (78,039 committees vs FED_FEC_BULK_COMMITTEES' 20,007; 33,506
# candidates vs FED_FEC_BULK_CANDIDATES' 17,900), dark since landing.
# ~52-58% of their IDs are already in the spine (current cycles); the rest are
# the new history entities this batch adds. Header repair at the load layer is
# the cleaner long-term fix (parked -- needs table DDL rights); wiring the
# positional names here is correct today and documented per column.
#
# Unconditional (no staging flag): wired in the same session that runs the
# full rebuild, per the flip-only-in-the-rebuild-session rule.
# =========================================================================== #
SNIFFER_BATCH_2026_08_18_DISPLAY_SPECS: dict[str, dict] = {
    "FED_FEC_COMMITTEES": {
        # cn.txt layout: C1=CMTE_ID (38,693 distinct norm, 54.1% in spine),
        # C2=CMTE_NM, C6/C7/C8=city/state/zip. C15 (the committee's candidate)
        # is a DIFFERENT entity on the row -> graph key only
        # (keys.TABLE_COLUMN_KEYS), NOT an extra_key -- the buyer_dea_no rule.
        "key": "FEC_CMTE_ID", "key_col": "C1", "org": "C2",
        "city": "C6", "state": "C7", "zip": "C8", "authority": 6,
    },
    "FED_FEC_CANDIDATES": {
        # candidate-master layout: C1=CAND_ID (19,142 distinct norm, 54.2% in
        # spine), C2=CAND_NAME ('ROBY, MARTHA' -- name_canon token-sort handles
        # the comma order), C13/C14/C15=city/state/zip. C10 (the candidate's
        # principal campaign committee) is a different entity -> graph key only.
        "key": "FEC_CAND_ID", "key_col": "C1", "org": "C2",
        "city": "C13", "state": "C14", "zip": "C15", "authority": 6,
    },
    "FED_FEC_CAND_CMTE_LINKAGE": {
        # ccl.txt layout: C1=CAND_ID (57.2% in spine), C4=CMTE_ID (51.6%).
        # Pure linkage rows -- no name columns exist, so the extra key can
        # mislabel nothing; the candidate<->committee edge is the point.
        "key": "FEC_CAND_ID", "key_col": "C1", "authority": 6,
        "extra_keys": [{"key": "FEC_CMTE_ID", "key_col": "C4"}],
    },
    "FED_FEC_PAC_SUMMARY": {
        # webk.txt layout: C1=CMTE_ID (22,899 distinct norm, 53.7% in spine),
        # C2=CMTE_NM. Financial summary columns only after that -- no address.
        "key": "FEC_CMTE_ID", "key_col": "C1", "org": "C2", "authority": 6,
    },
    "FED_EPA_ICIS_FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES": {
        # FACILITY_UIN is a full-population FRS ID hidden by its name --
        # 105,080 of 105,113 distinct (100.0%) live in the spine. Joins formal
        # enforcement-case CONCLUSIONS to the facility registry, same family
        # as the sibling ICIS_FEC case/inspection tables above.
        "key": "FRS_ID", "key_col": "FACILITY_UIN", "org": "FACILITY_NAME",
        "city": "FACILITY_CITY", "state": "FACILITY_STATE", "zip": "FACILITY_ZIP",
        "authority": 6,
    },
}
DISPLAY_SPECS.update(SNIFFER_BATCH_2026_08_18_DISPLAY_SPECS)

# spine scope = every table with a nameable hard key (health + money/maritime/corporate).
SPINE_TABLES = list(DISPLAY_SPECS)

# entity type from its hard key. THE single source of truth -- spine.py and
# incremental.py both generate their CASE expression from this via entity_type_sql()
# below, and spine_entity.py builds SPINE_ENTITY_BY_KEY on top of it. Before
# 2026-07-30 the same mapping was hand-copied into four files with a comment in each
# begging the next person to keep them in lockstep; a drift there silently re-types
# entities on a MERGE, so the copies are gone.
ENTITY_TYPE_BY_KEY = {
    "NPI": "provider", "CCN": "facility",
    "EIN": "organization", "CIK": "organization", "DUNS": "organization",
    "LEI": "organization", "UEI": "organization", "DEA_NO": "organization",
    "IMO": "vessel", "MMSI": "vessel",
    "BIOGUIDE": "person", "ICPSR": "person",   # politicians (Step-K politics)
    # --- 2026-07-30 spine wiring: four new key axes ---------------------------
    # All three of these identify a fixed physical site that a regulator inspects,
    # cites and can shut down -- the same grain as a CCN-keyed healthcare facility,
    # so they reuse 'facility' rather than inventing near-duplicate grains.
    "FRS_ID": "facility",     # EPA Facility Registry Service (any regulated site)
    "PWSID": "facility",      # EPA public water system
    "MINE_ID": "facility",    # MSHA mine
    # FEC: deliberately split. A committee is an org that raises and spends money;
    # a candidate is a human being who stands for office. Collapsing them (as the
    # registry's single 'FEC_ID' did) would put a PAC and a person in one entity.
    "FEC_CMTE_ID": "organization",
    "FEC_CAND_ID": "person",
    # 2026-08-05 ingestion-sweep wiring: UK Companies House company number. One
    # registrar's namespace (only the two UK CH tables carry it -- see
    # connect/keys.py EXACT_TOKEN_KEYS), identifying a registered company.
    "COMPANY_NO": "organization",
    # 2026-08-17 batch wiring (staged -- keys.ENABLE_SPINE_BATCH_2026_08).
    # A judge is a human being; a court is an institution that hires, rules and
    # can be appealed against -- organization, not facility (a courthouse is the
    # building; courts move between buildings). A water-discharge permit and a
    # detention center are fixed regulated sites (same grain as CCN/FRS/mine);
    # a credit union is an institution. Present unconditionally: entity typing
    # re-labels but never re-keys, so listing dark keys here is inert.
    "CL_PERSON_ID": "person",
    "CL_COURT_ID": "organization",
    "NPDES_ID": "facility",
    "NCUA_CHARTER": "organization",
    "ICE_FACILITY": "facility",
}

# Entity types that carry no hard-ID column of their own and are assigned from the
# registry's ENTITY_TYPES facet instead of a key (see spine_entity.SPINE_ENTITY_VOCAB).
_KEYLESS_ENTITY_TYPES = {"payment", "filing", "event", "aircraft"}


def entity_type_sql(col_ref: str = "key_type") -> str:
    """CASE expression mapping a key_type column to its entity type.

    Generated from ENTITY_TYPE_BY_KEY so spine.py (full rebuild), incremental.py
    (MERGE path) and the validate() shadow-recompute can never disagree -- a drift
    across those sites re-types entities mid-MERGE. ``col_ref`` is injected so the
    caller can qualify it ('k.KEY_TYPE', 'a.KEY_TYPE') or pass a literal.

    ELSE 'organization' is preserved from the original hand-written expression: an
    unmapped hard ID is far more often an org identifier than anything else, and a
    wrong-but-stable default beats a NULL entity type. ENTITY_TYPE never feeds
    ENTITY_ID (= hash(key_type|value)), so changing a mapping re-labels entities
    but never renumbers them.
    """
    whens = " ".join(
        f"WHEN '{key}' THEN '{etype}'"
        for key, etype in sorted(ENTITY_TYPE_BY_KEY.items()))
    return f"CASE {col_ref} {whens} ELSE 'organization' END"
