"""Phase 5 specs, 2026-09-10: the four depth-plan sources from the wonder ledger.

Probe receipts: reports/phase5_probe_2026-09-10.md. Every URL below was fetched
that day with a Range request and the header read before the spec was written.

  B  FED_CMS_SNF_OWNERSHIP     SNF All Owners, 295,083 rows, bridge_fuel (under 5M)
  C  FED_EOIR_PROCEEDING       B_TblProceeding, 16.8M rows, phase5 loader (ranged zip + fast PUT/COPY)
  C  FED_EOIR_JUDGE            tblLookupJudge, 1,785 rows, phase5 loader (same zip member trick)
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
        "key_cols": [{"col": "ENROLLMENT ID", "as": "ENROLLMENT_ID"},
                     {"col": "ASSOCIATE ID - OWNER", "as": "ASSOCIATE_ID_OWNER"},
                     {"col": "ROLE CODE - OWNER", "as": "ROLE_CODE_OWNER"}],
        "join_keys": "ENROLLMENT_ID -> FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.ENROLLMENT_ID -> CCN; ASSOCIATE_ID_OWNER",
        "category": "Health",
        "subcategory": "Provider Ownership",
        "unit_of_observation": "one row = one SNF enrollment x one owner x one role; key is the triple, ENROLLMENT_ID alone repeats 20x",
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
        "notes": "Landed 2026-09-10, phase 5. 1,785 rows; the zip Count.txt says 1,786. Includes the placeholder All Judges code AAA. Tab-delimited.",
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
        "join_keys": "LEGAL_NAME + ZIP_CD (no EIN; 3,612 blank names, 19 blank zips); NAIC_CD",
        "category": "Labor",
        "subcategory": "Wage Enforcement",
        "unit_of_observation": "one row = one concluded WHD compliance action",
        "update_cadence": "quarterly",
        "temporal_coverage": "concluded cases since FY2005",
        "accountability_relevance": "Employer, address, back wages, workers owed, violations by statute, findings dates. The wage-theft table.",
        "priority_tier": "1",
        "notes": ("Phase 5, 2026-09-10. Landed 2026-09-10 11:11, 367,890 rows, the API's whole set. enforcedata.dol.gov flat files are gone; every path redirects to data.dol.gov. "
                  "Pulled through the v4 API, 10,000 rows a page, X-API-KEY as a query parameter, sorted by case_id. "
                  "Rate limited, 429 after a burst; the loader backs off. 110 columns."),
    },
    {
        "source_id": "FED_SEC_13F_SECURITIES_LIST",
        "name": "SEC Official List of Section 13(f) Securities, 2026 Q2",
        "publisher": "SEC",
        "url": "https://www.sec.gov/divisions/investment/13flists.htm",
        "download_url": "https://www.sec.gov/files/investment/13flist2026q2-txt.txt",
        "kind": "fixed_width",
        "encoding": "latin-1",
        "widths": [("CUSIP", 0, 9), ("HAS_LISTED_OPTIONS", 9, 10), ("ISSUER_NAME", 10, 40),
                   ("ISSUER_DESCRIPTION", 40, 67), ("STATUS", 67, 70)],
        "constants": {"LIST_QUARTER": "2026Q2"},
        "loader": "phase5",
        "key_cols": [{"col": "CUSIP", "as": "CUSIP"}],
        "join_keys": "CUSIP -> FED_SEC_FTD_CUSIP_BRIDGE.CUSIP -> SYMBOL -> company_tickers CIK; no CIK in this file",
        "category": "Economics",
        "subcategory": "Securities Reference",
        "unit_of_observation": "one row = one line of the quarterly list; 25,333 lines, 23,277 distinct CUSIPs, ~2,000 verbatim repeats",
        "update_cadence": "quarterly",
        "temporal_coverage": "2026 Q2 list; text form exists 2020q1 onward, PDF back to 1996",
        "accountability_relevance": "Every security a 13F filer must report: CUSIP, issuer name, class. The name side of the CUSIP-to-CIK bridge.",
        "priority_tier": "2",
        "notes": ("Homestretch 2026-09-11, ledger row 13. Fixed-width 80-char text, no header, no CIK. "
                  "Col 10 '*' = has listed options, 6,110 rows. STATUS *A* added 1,351, *D* deleted 844, blank 23,138. "
                  "LINE_NO is the row key; CUSIP repeats on ~2,000 verbatim duplicate lines, dedupe on CUSIP before joining."),
    },
]

# Census 2020 ZCTA-to-county relationship file. Landed 2026-09-11 to close the ZIP-to-county hole:
# six or more county wonders were blocked on it. One row per ZCTA x county overlap, with land area of the
# overlap, so a ZCTA split across counties can be assigned to its largest-area county. ZCTA is not USPS ZIP:
# P.O.-box-only ZIPs have no ZCTA. The HUD USPS crosswalk is the better file but needs an API token we lack.
SPECS.append({
    "source_id": "FED_CENSUS_ZCTA_COUNTY_2020",
    "name": "Census 2020 ZCTA to county relationship file",
    "publisher": "Census Bureau",
    "url": "https://www.census.gov/geographies/reference-files/time-series/geo/relationship-files.2020.html",
    "download_url": "https://www2.census.gov/geo/docs/maps-data/data/rel2020/zcta520/tab20_zcta520_county20_natl.txt",
    "kind": "url_csv",
    "delimiter": "|",
    "loader": "phase5",
    "key_cols": [{"col": "GEOID_ZCTA5_20", "as": "GEOID_ZCTA5_20"}, {"col": "GEOID_COUNTY_20", "as": "GEOID_COUNTY_20"}],
    "join_keys": "GEOID_ZCTA5_20 = 5-digit ZCTA, joins any ZIP5 column; GEOID_COUNTY_20 = 5-digit county FIPS -> FED_CENSUS_COUNTY_2020",
    "category": "Reference",
    "subcategory": "Geography",
    "unit_of_observation": "one row = one ZCTA x county overlap; key is the pair, ZCTA alone repeats where a ZCTA crosses a county line",
    "update_cadence": "decennial",
    "temporal_coverage": "2020 vintage",
    "accountability_relevance": "The ZIP to county bridge every ZIP-only table needs to land on a county map.",
    "priority_tier": "1",
    "notes": ("Landed 2026-09-11. Pipe-delimited. Rows with a blank GEOID_ZCTA5_20 are county land with no ZCTA; drop them. "
              "AREALAND_PART is the overlap area: pick the max per ZCTA for a one-to-one map."),
})

# HUD Multifamily properties with assistance and Section 8 contracts, property level, with the OWNER and the
# MANAGEMENT AGENT named. Landed 2026-09-11 to close the landlord hole: no other public national file names who
# owns a rental building. Scope is HUD-assisted or HUD-insured multifamily only, not the private rental market.
_HUD_HDR = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.hud.gov/"}
SPECS.append({
    "source_id": "FED_HUD_MF_PROPERTIES_OWNERS",
    "name": "HUD multifamily properties with assistance and Section 8 contracts, owner and management agent",
    "publisher": "HUD Office of Multifamily Housing",
    "url": "https://www.hud.gov/hud-partners/multifamily-assist-section8-database",
    "download_url": "https://www.hud.gov/sites/dfiles/Housing/documents/MF-Properties-with-Assistance-Sec8-Contracts1.xlsx",
    "kind": "url_xlsx",
    "headers": _HUD_HDR,
    "loader": "phase5",
    "key_cols": [{"col": "property_id", "as": "PROPERTY_ID"}],
    "join_keys": ("PROPERTY_ID -> FED_HUD_MF_SECTION8_CONTRACTS.PROPERTY_ID; OWNER_PARTICIPANT_ID groups buildings by owner; "
                  "STATE_CODE||COUNTY_CODE = county FIPS; ZIP_CODE -> FED_CENSUS_ZCTA_COUNTY_2020"),
    "category": "Housing",
    "subcategory": "Multifamily Ownership",
    "unit_of_observation": "one row = one HUD multifamily property, 23,612 rows, PROPERTY_ID unique",
    "update_cadence": "monthly",
    "temporal_coverage": "snapshot 2026-08-07",
    "accountability_relevance": "Who owns and who manages every HUD-assisted apartment building: org name, participant id, address, type.",
    "priority_tier": "1",
    "notes": ("Landed 2026-09-11. Cells come space-padded to fixed width; TRIM everything. Blanks are a single space, "
              "not NULL. COUNTY_CODE is the 3-digit county FIPS without the state. Owner is either an org or an individual: "
              "OWNER_ORGANIZATION_NAME or the OWNER_INDIVIDUAL_* columns, never both. hud.gov needs a Referer header."),
})

# HUD LIHTC property database, placed in service 1987-2024. Landed 2026-09-11. No owner in it: this is the
# PLACE side of subsidized housing, tract and county FIPS on every row, 2020 vintage. Owner lives only in
# FED_HUD_MF_PROPERTIES_OWNERS, and the two do not share a key; address+ZIP is the only bridge.
SPECS.append({
    "source_id": "FED_HUD_LIHTC_PROPERTIES",
    "name": "HUD Low-Income Housing Tax Credit property database, 1987-2024",
    "publisher": "HUD PD&R",
    "url": "https://www.huduser.gov/portal/datasets/lihtc.html",
    "download_url": "https://www.huduser.gov/lihtc/lihtcpub.zip",
    "kind": "zip_xlsx",
    "member": r"^LIHTCPUB\.xlsx$",
    "xlsx_strip_synch": True,
    "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36",
                "Referer": "https://www.huduser.gov/portal/datasets/lihtc/property.html"},
    "loader": "phase5",
    "key_cols": [{"col": "hud_id", "as": "HUD_ID"}],
    "join_keys": "FIPS2020 = 11-digit tract; ST2020||CNTY2020 = county FIPS -> FED_CENSUS_COUNTY_2020; PROJ_ZIP -> FED_CENSUS_ZCTA_COUNTY_2020",
    "category": "Housing",
    "subcategory": "Subsidized Housing",
    "unit_of_observation": "one row = one LIHTC project, HUD_ID unique",
    "update_cadence": "annual",
    "temporal_coverage": "placed in service 1987-2024",
    "accountability_relevance": "Where every tax-credit apartment project sits, how many units, what year, what other federal money.",
    "priority_tier": "2",
    "notes": ("Landed 2026-09-11. YR_PIS and YR_ALLOC use 9999 for unknown and 8888 for not yet placed; NULLIF both. "
              "No owner, no developer, no syndicator in the public file. ST2020 and CNTY2020 come with leading zeros stripped; lpad before joining. huduser.gov 202s a non-browser User-Agent."),
})
