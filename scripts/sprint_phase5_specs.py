"""Phase 5 specs, 2026-09-10: the four depth-plan sources from the wonder ledger.

Probe receipts: reports/phase5_probe_2026-09-10.md. Every URL below was fetched
that day with a Range request and the header read before the spec was written.

  B  FED_CMS_SNF_OWNERSHIP     SNF All Owners, 295,083 rows, bridge_fuel (under 5M)
  C  FED_EOIR_PROCEEDING       B_TblProceeding, 16.8M rows, phase5 loader (ranged zip + fast PUT/COPY)
  C  FED_EOIR_JUDGE            tblLookupJudge, 1,786 rows, phase5 loader (same zip member trick)
  D  FED_DOL_WHD_ENFORCEMENT   DOL v4 API, 10k rows a page, phase5 loader (page to csv, fast PUT/COPY)

A, SAM entity registration, is NOT here: LIBRARY_RAW.LANDING.FED_SAM_ENTITY_PUBLIC
already holds the August 2026 public extract (895,429 rows). The public layout
carries no EIN and no parent UEI. A refresh is a separate call.

loader values:
  bridge_fuel  scripts/bridge_fuel_load.py picks these up by itself (sprint_*_specs glob)
  phase5       scripts/phase5_load.py, which fetches then calls cms_years_fast_load.land()
"""

EOIR_ZIP = "https://fileshare.eoir.justice.gov/EOIR Case Data.zip"

SPECS = [
    {
        "source_id": "FED_CMS_SNF_OWNERSHIP",
        "name": "CMS Skilled Nursing Facility All Owners",
        "publisher": "CMS",
        "url": "https://data.cms.gov/provider-characteristics/hospitals-and-other-facilities/skilled-nursing-facility-all-owners",
        "download_url": "https://data.cms.gov/sites/default/files/2026-08/1d804c1b-cefd-4438-852d-a267890bb144/SNF_All_Owners_2026.07.31.csv",
        "kind": "csv",
        "encoding": "cp1252",
        "loader": "bridge_fuel",
        "key_cols": [{"col": "ENROLLMENT ID", "as": "ENROLLMENT_ID"}],
        "join_keys": "ENROLLMENT_ID -> FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID -> CCN; ASSOCIATE_ID_OWNER",
        "category": "Health",
        "subcategory": "Provider Ownership",
        "unit_of_observation": "one row = one SNF enrollment x one owner x one role",
        "update_cadence": "quarterly",
        "temporal_coverage": "snapshot 2026-07-31; 46 quarterly vintages exist back to 2015",
        "accountability_relevance": "Who owns every nursing home: person or org, role, percent, date. Chains, PE, REITs, holding companies by flag.",
        "priority_tier": "1",
        "notes": ("Landed 2026-09-10, phase 5. No CCN in the file; join ENROLLMENT_ID to the SNF enrollments table. "
                  "Source is cp1252, not UTF-8. Grain is enrollment x owner x role, 198,299 distinct enrollment+owner pairs. "
                  "Sibling: FED_CMS_HOME_HEALTH_OWNERS, same layout."),
    },
    {
        "source_id": "FED_EOIR_PROCEEDING",
        "name": "EOIR Immigration Court Proceedings with decision and judge",
        "publisher": "DOJ EOIR",
        "url": "https://www.justice.gov/eoir/foia-library-0",
        "download_url": EOIR_ZIP,
        "member": "EOIR Case Data/B_TblProceeding.csv",
        "kind": "zip_member_ranged",
        "repair_rows": True,
        "delimiter": "\t",
        "quote_none": True,
        "encoding": "utf-8",
        "loader": "phase5",
        "key_cols": [{"col": "IDNPROCEEDING", "as": "IDNPROCEEDING"}],
        "join_keys": "IDNCASE -> FED_EOIR_CASE_DATA / FED_EOIR_CASES; IJ_CODE -> FED_EOIR_JUDGE.JUDGE_CODE",
        "category": "Immigration",
        "subcategory": "Court Proceedings",
        "unit_of_observation": "one row = one proceeding in one case",
        "update_cadence": "monthly",
        "temporal_coverage": "all proceedings on file, zip dated 2026-09-01",
        "accountability_relevance": "Judge code, decision code and type, completion date, absentia, custody per proceeding. The grant-rate-by-judge table.",
        "priority_tier": "1",
        "notes": ("Landed 2026-09-10, phase 5. There is no tblDecision in the EOIR zip; decisions are DEC_CODE, DEC_TYPE, "
                  "COMP_DATE on this table. Tab-delimited despite the .csv name. Pulled by ranged zip read, "
                  "not the whole 4.56 GB. Count.txt in the zip says 16,817,336 rows."),
    },
    {
        "source_id": "FED_EOIR_JUDGE",
        "name": "EOIR Immigration Judge lookup",
        "publisher": "DOJ EOIR",
        "url": "https://www.justice.gov/eoir/foia-library-0",
        "download_url": EOIR_ZIP,
        "member": "Lookup/tblLookupJudge.csv",
        "kind": "zip_member_ranged",
        "delimiter": "\t",
        "quote_none": True,
        "encoding": "utf-8",
        "loader": "phase5",
        "key_cols": [{"col": "JUDGE_CODE", "as": "JUDGE_CODE"}],
        "join_keys": "JUDGE_CODE -> FED_EOIR_PROCEEDING.IJ_CODE",
        "category": "Immigration",
        "subcategory": "Court Proceedings",
        "unit_of_observation": "one row = one judge code",
        "update_cadence": "monthly",
        "temporal_coverage": "all judge codes ever issued, active flag",
        "accountability_relevance": "Judge code to name. The only public list of immigration judges with an active flag.",
        "priority_tier": "1",
        "notes": "Landed 2026-09-10, phase 5. 1,786 rows. Includes the placeholder All Judges code AAA. Tab-delimited.",
    },
    {
        "source_id": "FED_DOL_WHD_ENFORCEMENT",
        "name": "DOL Wage and Hour Division compliance actions",
        "publisher": "DOL WHD",
        "url": "https://data.dol.gov/",
        "download_url": "https://apiprod.dol.gov/v4/get/whd/enforcement/csv",
        "kind": "dol_api_paged",
        "page_rows": 10_000,
        "sort_by": "case_id",
        "loader": "phase5",
        "key_cols": [{"col": "case_id", "as": "CASE_ID"}],
        "join_keys": "LEGAL_NAME + ZIP_CD (no EIN); NAIC_CD",
        "category": "Labor",
        "subcategory": "Wage Enforcement",
        "unit_of_observation": "one row = one concluded WHD compliance action",
        "update_cadence": "quarterly",
        "temporal_coverage": "concluded cases since FY2005",
        "accountability_relevance": "Employer, address, back wages, workers owed, violations by statute, findings dates. The wage-theft table.",
        "priority_tier": "1",
        "notes": ("Landed 2026-09-10, phase 5. enforcedata.dol.gov flat files are gone; every path redirects to data.dol.gov. "
                  "Pulled through the v4 API, 10,000 rows a page, X-API-KEY as a query parameter, sorted by case_id. "
                  "Rate limited, 429 after a burst; the loader backs off. 110 columns."),
    },
]
