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
    survivorship, since it's the same underlying row.
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
    # FED_CMS_FACILITY_AFFILIATION removed 2026-07-20: the landing table was
    # dropped (verified live — zero columns in INFORMATION_SCHEMA). Its NPIs
    # stay on the spine via NPPES/LEIE; the banned_but_operating detector's
    # frozen evidence is unaffected (documented caveat in lead_queue.sql).
    "FED_HHS_OIG_LEIE": {
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

    # --- money / maritime / corporate (2026-06-26: unhealth the spine) ---
    # keys.py already normalizes UEI/CIK/IMO; ENTITY_TYPE_BY_KEY maps them to
    # organization/vessel. Adding these makes a debarred-and-funded UEI, a
    # sanctioned-and-broadcasting IMO, and a SEC CIK first-class multi-source entities.
    "FED_USASPENDING_CONTRACTS": {            # UEI organization (the money anchor, 6.3M rows)
        "key": "UEI", "key_col": "RECIPIENT_UEI", "org": "RECIPIENT_NAME",
        "city": "RECIPIENT_CITY_NAME", "state": "RECIPIENT_STATE_CODE",
        "zip": "RECIPIENT_ZIP_4_CODE", "authority": 4,
    },
    "FED_SAM_EXCLUSIONS": {                   # UEI organization (the federal debarment flag)
        "key": "UEI", "key_col": "UEI", "org": "ENTITY_NAME",
        "city": "CITY", "state": "STATE", "zip": "ZIP", "authority": 5,
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
}

# spine scope = every table with a nameable hard key (health + money/maritime/corporate).
SPINE_TABLES = list(DISPLAY_SPECS)

# entity type from its hard key
ENTITY_TYPE_BY_KEY = {
    "NPI": "provider", "CCN": "facility",
    "EIN": "organization", "CIK": "organization", "DUNS": "organization",
    "LEI": "organization", "UEI": "organization",
    "IMO": "vessel", "MMSI": "vessel",
    "BIOGUIDE": "person", "ICPSR": "person",   # politicians (Step-K politics)
}
