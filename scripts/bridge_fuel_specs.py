"""Source specs for scripts/bridge_fuel_load.py — verified bridge-fuel sources.

Each dict is a known-shape bulk source whose exact URL + key columns were verified
live by the 2026-06-24 bridge-fuel research workflow. The loader (bridge_fuel_load)
renames the VERIFIED id columns (`key_cols`) to canonical names the connect tagger
detects (CCN/NPI are STEEL tokens) — this is per-source, so it never risks false
positives in the existing 638-table graph (unlike broadening the global tagger).

CROSSWALK (lights the bridge):
  fed_cms_facility_affiliation — CMS Doctors&Clinicians Facility Affiliation:
    ~2.24M rows co-carrying NPI + CCN, 0 masked. THE flagship CCN<->NPI hop.

CCN ENDPOINTS (reachable to NPPES/LEIE the instant the crosswalk lands):
  fed_cms_pos_other, fed_cms_hospital_general, fed_cms_hospice,
  fed_cms_home_health, fed_cms_irf, fed_cms_ltch, fed_cms_dialysis

DEFERRED: NBER npi_medicarexw (2nd CCN<->NPI crosswalk) — NBER hard-blocks bot
  downloads (403, IP-reputation); frozen at 2017 anyway. Facility Affiliation is the
  current, larger, primary crosswalk and stands alone.
"""

SPECS = [
    # ---- THE CROSSWALK (CCN <-> NPI) ---------------------------------------
    {
        "source_id": "fed_cms_facility_affiliation",
        "name": "CMS Doctors & Clinicians — Facility Affiliation (NPI↔CCN crosswalk)",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/27ea-46a8",
        "provider_data_id": "27ea-46a8",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/b7c4080ae144663e43353a9c35cd3f53_1780085743/Facility_Affiliation.csv",
        "kind": "csv",
        "chunked": True,
        "chunk_rows": 250_000,
        "key_cols": [
            {"col": "Facility Affiliations Certification Number", "as": "CCN"},
            {"col": "NPI", "as": "NPI"},
        ],
        "join_keys": "CCN, NPI",
        "category": "Health",
        "subcategory": "Provider Crosswalk",
        "unit_of_observation": "one row = one clinician-to-facility affiliation",
        "update_cadence": "monthly",
        "accountability_relevance": "Bridges Medicare facility CCNs to provider NPIs — connects facility tables to NPPES and the OIG-LEIE banned-provider list ('banned but still operating').",
        "priority_tier": "1",
        "notes": "CCN<->NPI crosswalk that activates the connect bridge layer. CCN col = 'Facility Affiliations Certification Number' aliased to CCN. Loaded LLM-free (bridge_fuel_load).",
    },
    # ---- CCN ENDPOINTS ------------------------------------------------------
    {
        "source_id": "fed_cms_pos_other",
        "name": "CMS Provider of Services — Hospital & Non-Hospital Facilities",
        "publisher": "CMS",
        "url": "https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/provider-of-services-file-hospital-non-hospital-facilities",
        "download_url": "https://data.cms.gov/sites/default/files/2026-04/8ff9bcf4-032e-4a6f-b1c1-d8f1c2e96885/Hospital_and_other.DATA.Q1_2026.csv",
        "kind": "csv",
        "key_cols": [{"col": "PRVDR_NUM", "as": "CCN"}],
        "csv_opts": {"encoding": "latin-1"},
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one Medicare-certified facility (CCN)",
        "update_cadence": "quarterly",
        "accountability_relevance": "~44k facility CCNs across hospitals/ASC/ESRD/FQHC/RHC/hospice/home-health — broad CCN endpoint reachable to NPPES/LEIE via the facility-affiliation crosswalk.",
        "priority_tier": "2",
        "notes": "CCN-only endpoint; PRVDR_NUM aliased to CCN. data.cms.gov dated URL (verified 2026-06-24).",
    },
    {
        "source_id": "fed_cms_hospital_general",
        "name": "CMS Care Compare — Hospital General Information",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/xubh-q36u",
        "provider_data_id": "xubh-q36u",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/893c372430d9d71a1c52737d01239d47_1777413958/Hospital_General_Information.csv",
        "kind": "csv",
        "key_cols": [{"col": "Facility ID", "as": "CCN"}],
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one hospital (CCN)",
        "update_cadence": "monthly",
        "priority_tier": "2",
        "notes": "CCN-only endpoint; 'Facility ID' (=CCN) aliased to CCN.",
    },
    {
        "source_id": "fed_cms_hospice",
        "name": "CMS Care Compare — Hospice General Information",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/yc9t-dgbk",
        "provider_data_id": "yc9t-dgbk",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/1671415a6c26789acf1569fa5dd49ba0_1777658734/Hospice_General-Information_May2026.csv",
        "kind": "csv",
        "key_cols": [{"col": "CMS Certification Number (CCN)", "as": "CCN"}],
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one hospice (CCN)",
        "update_cadence": "monthly",
        "priority_tier": "2",
        "notes": "CCN-only endpoint.",
    },
    {
        "source_id": "fed_cms_home_health",
        "name": "CMS Care Compare — Home Health Agencies",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/6jpm-sxkc",
        "provider_data_id": "6jpm-sxkc",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/f9a309e9463cdf0a7d7828f8d8d0e653_1775505949/HH_Provider_Apr2026.csv",
        "kind": "csv",
        "key_cols": [{"col": "CMS Certification Number (CCN)", "as": "CCN"}],
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one home health agency (CCN)",
        "update_cadence": "monthly",
        "priority_tier": "2",
        "notes": "CCN-only endpoint.",
    },
    {
        "source_id": "fed_cms_irf",
        "name": "CMS Care Compare — Inpatient Rehabilitation Facility General Information",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/7t8x-u3ir",
        "provider_data_id": "7t8x-u3ir",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/5ebf2040f6f206a89a6354611e7856a6_1781623440/Inpatient_Rehabilitation_Facility-General_Information_Jun2026_b.csv",
        "kind": "csv",
        "key_cols": [{"col": "CMS Certification Number (CCN)", "as": "CCN"}],
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one inpatient rehab facility (CCN)",
        "update_cadence": "quarterly",
        "priority_tier": "2",
        "notes": "CCN-only endpoint.",
    },
    {
        "source_id": "fed_cms_ltch",
        "name": "CMS Care Compare — Long-Term Care Hospital General Information",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/azum-44iv",
        "provider_data_id": "azum-44iv",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/c3ce320ddf464b5df1bceae3f55da0d5_1781037952/Long-Term_Care_Hospital-General_Information_Jun2026.csv",
        "kind": "csv",
        "key_cols": [{"col": "CMS Certification Number (CCN)", "as": "CCN"}],
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one long-term care hospital (CCN)",
        "update_cadence": "quarterly",
        "priority_tier": "2",
        "notes": "CCN-only endpoint.",
    },
    {
        "source_id": "fed_cms_dialysis",
        "name": "CMS Care Compare — Dialysis Facility Listing",
        "publisher": "CMS — Provider Data Catalog",
        "url": "https://data.cms.gov/provider-data/dataset/23ew-n7w9",
        "provider_data_id": "23ew-n7w9",
        "download_url": "https://data.cms.gov/provider-data/sites/default/files/resources/c04d84bc5c641284494bee4f20f17f9c_1774454758/DFC_FACILITY.csv",
        "kind": "csv",
        "key_cols": [{"col": "CMS Certification Number (CCN)", "as": "CCN"}],
        "join_keys": "CCN",
        "category": "Health",
        "subcategory": "Facility Roster",
        "unit_of_observation": "one row = one dialysis facility (CCN)",
        "update_cadence": "quarterly",
        "priority_tier": "2",
        "notes": "CCN-only endpoint.",
    },
]
