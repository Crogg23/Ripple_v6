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
"""

from __future__ import annotations

DISPLAY_SPECS: dict[str, dict] = {
    "FED_CMS_NPPES": {
        "key": "NPI", "key_col": "NPI",
        "person": ["PROVIDER_LAST_NAME__LEGAL_NAME", "PROVIDER_FIRST_NAME"],
        "org": "PROVIDER_ORGANIZATION_NAME__LEGAL_BUSINESS_NAME",
        "city": "PROVIDER_BUSINESS_MAILING_ADDRESS_CITY_NAME",
        "state": "PROVIDER_BUSINESS_MAILING_ADDRESS_STATE_NAME",
        "zip": "PROVIDER_BUSINESS_MAILING_ADDRESS_POSTAL_CODE",
        "authority": 1,
    },
    "FED_CMS_FACILITY_AFFILIATION": {
        "key": "NPI", "key_col": "NPI",
        "person": ["PROVIDER_LAST_NAME", "PROVIDER_FIRST_NAME"],
        "authority": 3,
    },
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
}

# spine scope = every table with a nameable hard key (health + money/maritime/corporate).
SPINE_TABLES = list(DISPLAY_SPECS)

# entity type from its hard key
ENTITY_TYPE_BY_KEY = {
    "NPI": "provider", "CCN": "facility",
    "EIN": "organization", "CIK": "organization", "DUNS": "organization",
    "LEI": "organization", "UEI": "organization",
    "IMO": "vessel", "MMSI": "vessel",
}
