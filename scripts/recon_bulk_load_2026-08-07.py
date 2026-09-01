"""Batch loader for the 2026-08-07 recon sweep of Tier-1 bulk sources.

Follows the exact structure/conventions of scripts/tier1_bulk_batch_load.py
(same helper functions, same FORMAT_LOADERS pattern, same CLI). Targets 73
verified datasets across HRSA/IHS/FDA/EPA/USGS/FEMA/OCC/NCUA/CFPB/FHFA/PCAOB/
IRS/FINRA/ISO/UK+UN sanctions/PBGC/FJC/ATF/deportation-data/state lobbying &
campaign finance/NTSB/FAA/FMC/JPML/CA OEHHA/Education/HUD/USDA/USASpending/
SBIR/EIA-860+861/BOEM/OSFI/ROR/Crossref/NSF/Grants.gov/OSF.

NOTE: five tables appear twice in the source manifest (two independently
verified entries pointed at the same table -- FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK,
FED_OCC_NATIONAL_BANKS_BY_NAME, INTL_ISO_MIC_REGISTRY, INTL_UK_FCDO_SANCTIONS_LIST,
INTL_UN_SC_CONSOLIDATED_SANCTIONS). Both rows are kept (nothing in the source
list was dropped), but the loader skips the second occurrence of a table
within a single run so it doesn't fetch + quality-gate the same table twice
in one pass.

Several entries carry formats with no loader yet (pdf, fixed_width, zip_xml)
-- these print a clean "no loader for format" skip at run time, same as the
template's existing behavior for an unregistered format. (xml and mdb *do*
have dedicated loaders now -- see the 2026-08-07 diagnostic-fix pass below.)

    python scripts/recon_bulk_load_2026-08-07.py              # preview
    python scripts/recon_bulk_load_2026-08-07.py --run        # load all
    python scripts/recon_bulk_load_2026-08-07.py --run --group hrsa
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import datetime as dt
import sys
import uuid
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import pandas as pd
import requests

_REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_REPO / "scripts"))
sys.path.insert(0, str(_REPO / "library-onboarding"))
try:
    from dotenv import load_dotenv
    load_dotenv(_REPO / "library-onboarding/.env", override=True)
except Exception:
    pass

import snow  # noqa: E402
sys.path.insert(0, str(_REPO))
import _bulk_load_utils as bulk  # noqa: E402
from loadkit.archive import pick_member  # noqa: E402

USER_AGENT = {"User-Agent": "Ripple-Library/1.0 (data research; w.rogers9999@gmail.com)"}

# ---------------------------------------------------------------------------
# MANIFEST -- grouped by publisher cluster (verified 2026-08-07 recon sweep)
# ---------------------------------------------------------------------------

MANIFEST = [
    # --- HRSA ---
    {
        "group": 'hrsa',
        "table": 'FED_HRSA_NPDB',
        "url": 'https://www.npdb.hrsa.gov/resources/NpdbPublicUseDataCsv.zip',
        "format": 'zip_csv',
        "description": 'NPDB Public Use Data File (de-identified malpractice payment / adverse licensure / DEA action reports). Confirmed: direct zip download (38MB), contains NPDB2601.CSV (~235MB, real header row) plus format-spec PDF and a research-proposal DOCX -- zip_csv loader will pick the CSV as the largest file, which is correct. The site shows a Data Use Agreement click-through form (name/city/state/email + terms checkbox) before offering this link, but the zip URL itself works with a cold, cookie-less request -- no login or account needed. NOTE: repo already has a raw FED_HRSA_NPDB table wired to a mart (marts/health/health__fed_hrsa_npdb.sql) -- this is very likely already loaded; verify before reloading.',
        "fallback_url": 'https://www.npdb.hrsa.gov/resources/publicData.jsp',
    },
    {
        "group": 'hrsa',
        "table": 'FED_HRSA_UDS_SERVICE_DELIVERY_SITES',
        "url": 'https://data.hrsa.gov/DataDownload/DD_Files/Health_Center_Service_Delivery_and_LookAlike_Sites.csv',
        "format": 'csv',
        "description": 'HRSA Health Center Program site-level list (site name/address/city/state/zip, telephone, operating hours, location setting) -- one row per funded service-delivery site. Confirmed real CSV, ~13.8MB, real header row. This is site-level data, distinct from the already-loaded FED_HRSA_UDS_HEALTH_CENTER_INFO table (that one is grantee/awardee-level, one row per funded health center org) -- not a duplicate of it.',
        "fallback_url": 'https://data.hrsa.gov/data/download',
    },
    {
        "group": 'hrsa',
        "table": 'FED_HRSA_HPSA_PRIMARY_CARE',
        "url": 'https://data.hrsa.gov/DataDownload/DD_Files/BCD_HPSA_FCT_DET_PC.csv',
        "format": 'csv',
        "description": "HRSA HPSA Primary Care designation detail (HPSA Name, HPSA ID, Designation Type, HPSA Score, State, Status, Designation Date, Degree of Shortage, geography ID). Confirmed real CSV, ~48MB, real header row. Companion MUA/P file also confirmed live and real at https://data.hrsa.gov/DataDownload/DD_Files/MUA_DET.csv (~8.6MB, header includes 'MUA/P ID') -- a separate table, not pulled into this single entry; give it its own manifest row (e.g. FED_HRSA_MUA_DESIGNATIONS) if MUA coverage is wanted too. NOTE: repo already has a raw FED_HRSA_SHORTAGE_AREAS table (schema.yml says 'grain not yet determined') that may already cover HPSA -- check its actual contents before loading this as a duplicate; the MUA_DET.csv file looks unloaded either way.",
        "fallback_url": 'https://data.hrsa.gov/data/download',
    },
    # --- IHS ---
    {
        "group": 'ihs',
        "table": 'FED_IHS_SCB_FACILITY',
        "url": 'https://www.ihs.gov/scb/download-tablesall/?file=txt',
        "format": 'csv',
        "description": "IHS facility reference table (ASUFAC code, Area, Service Unit, Facility name/type, Location Type, Bed Count, Status, APC Flag, ITU Code), confirmed real -- 8733-row comma-delimited .txt export matching the site's stated match count. IMPORTANT: this export URL only returns data if a ColdFusion session cookie was first established by GETting the facility page (fallback_url below) in the same session/cookie jar -- hit cold with no prior request, it returns an HTML page instead of data. Not a login, just a two-step session flow the loader needs to replicate (requests.Session(): GET fallback_url, then GET url).",
        "fallback_url": 'https://www.ihs.gov/scb/standard-code-book-tables/facility/',
        # 2026-08-07 fix: load_csv does the warmup GET (in the same
        # requests.Session) before the real GET when this key is present.
        # Re-verified today: two-step flow returns real CSV, 8,733 rows.
        "session_warmup_url": 'https://www.ihs.gov/scb/standard-code-book-tables/facility/',
    },
    {
        "group": 'ihs',
        "table": 'FED_IHS_FACILITIES',
        "url": 'https://www.ihs.gov/sites/locations/themes/responsive2017/display_objects/documents/ihs_facilities.xlsx',
        "format": 'xlsx',
        "description": 'Complete listing of Indian Health Service facilities by area/service unit; verified live 200 OK, real xlsx content-type, 296,217 bytes -- matches census evidence exactly (296 KB, updated June 15 2023).',
    },
    # --- FDA Device ---
    {
        "group": 'fda_device',
        "table": 'FED_FDA_ESTABLISHMENT_REG',
        "url": 'https://api.fda.gov/device/registrationlisting.json',
        "format": 'json_api',
        "description": 'openFDA device establishment registration & listing API -- confirmed live JSON, 330,251 total records (fei_number, establishment_name, owner_operator, k_number/pma_number ties, product codes). Paginate with ?limit=1000&skip=N (max limit 1000/request, no key needed for low-volume use). DUPLICATE: repo already has a raw FED_FDA_ESTABLISHMENT_REG table pulling this exact endpoint (staging/fed_fda_establishment_reg) -- do not reload, this is almost certainly already sitting in the warehouse.',
        "fallback_url": 'https://open.fda.gov/apis/device/registrationlisting/',
    },
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_510K',
        "url": 'https://api.fda.gov/device/510k.json',
        "format": 'json_api',
        "description": 'openFDA 510(k) clearance API -- confirmed live JSON response, records from 1976-present, monthly updates. Paginate with ?limit=1000&skip=N. DUPLICATE: repo already has a raw FED_FDA_DEVICE_510K table pulling this exact endpoint (staging/fed_fda_device_510k) -- do not reload.',
        "fallback_url": 'https://open.fda.gov/apis/device/510k/',
    },
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_PMA',
        "url": 'https://api.fda.gov/device/pma.json',
        "format": 'json_api',
        "description": 'openFDA PMA (premarket approval) API -- confirmed live JSON response, 1976-present, monthly updates. Paginate with ?limit=1000&skip=N. DUPLICATE: repo already has a raw FED_FDA_DEVICE_PMA table pulling this exact endpoint (staging/fed_fda_device_pma) -- do not reload.',
        "fallback_url": 'https://open.fda.gov/apis/device/pma/',
    },
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_ENFORCEMENT',
        "url": 'https://api.fda.gov/device/enforcement.json',
        "format": 'json_api',
        "description": "openFDA device enforcement reports API (device recalls from FDA's Recall Enterprise System) -- confirmed live JSON response, coverage 2004-present, weekly updates. Paginate with ?limit=1000&skip=N. Not currently in the repo's dbt models (checked -- no match).",
        "fallback_url": 'https://open.fda.gov/apis/device/enforcement/',
    },
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_CLASSIFICATION',
        "url": 'https://api.fda.gov/device/classification.json',
        "format": 'json_api',
        "description": "openFDA device product classification database (product codes under 21 CFR 862-892, device class, regulation number) -- confirmed live JSON response. Paginate with ?limit=1000&skip=N. Not currently in the repo's dbt models (checked -- no match).",
        "fallback_url": 'https://open.fda.gov/apis/device/classification/',
    },
    # --- DailyMed ---
    {
        "group": 'dailymed',
        "table": 'FED_NLM_DAILYMED_SPL_SETID_MAP',
        "url": 'https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_zip_files_meta_data.zip',
        "format": 'zip_csv',
        "description": "DailyMed SPL Set ID mapping file -- one row per SPL document mapping SETID to zip filename, upload date, SPL version, and drug title. Confirmed real zip (7.6MB) containing a 29MB pipe-delimited txt plus README (verified: 'SETID|ZIP_FILE_NAME|UPLOAD_DATE|SPL_VERSION|TITLE', real sample rows). NOTE: pipe-delimited, not comma -- a plain zip_csv loader using pd.read_csv defaults will need sep='|' for this file specifically. This is the small mapping table, not the full multi-GB XML label-document dump (dm_spl_release_human_rx_part*.zip) -- those exist too but are XML SPL documents, not tabular, and would need a different loader entirely.",
        "fallback_url": 'https://dailymed.nlm.nih.gov/dailymed/spl-resources-all-mapping-files.cfm',
        "sep": '|',  # 2026-08-07 fix: pipe-delimited, not comma.
    },
    # --- Health Canada ---
    {
        "group": 'health_canada',
        "table": 'INTL_HEALTHCANADA_DPD_DRUG',
        "url": 'https://www.canada.ca/content/dam/hc-sc/documents/services/drug-product-database/drug.zip',
        "format": 'zip_csv',
        "description": "Health Canada Drug Product Database main 'drug' extract -- one row per drug product, includes the Drug Identification Number (DIN). Confirmed real zip (311KB) containing drug.txt, a 1.6MB quoted-CSV with real DIN values (e.g. '00015741','TAPAZOLE',...,'00135'). NO header row in the file -- column names come from HC's separate DPD data-extract documentation page, not the file itself, so the loader will need to hardcode column names. This is one of ~9 related extract files (drug/ingred/form/route/schedule/pharm/comp/package/inactive.zip, each with _ia/_ap/_dr variants for active/dormant/human-vs-vet splits) all confirmed live at the same path -- only the core 'drug' file was pulled into this entry.",
        "fallback_url": 'https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/drug-product-database/what-data-extract-drug-product-database.html',
    },
    # --- EPA ---
    {
        "group": 'epa',
        "table": 'FED_EPA_AQS_SITES',
        "url": 'https://aqs.epa.gov/aqsweb/airdata/aqs_sites.zip',
        "format": 'zip_csv',
        "description": 'EPA AQS AirData pre-generated national site metadata file (one row per monitoring Site ID, with location and program info); confirmed live, zip contains a single aqs_sites.csv (~6MB).',
    },
    {
        "group": 'epa',
        "table": 'FED_EPA_TRI_FACILITY',
        "url": 'https://data.epa.gov/efservice/tri_facility/rows/0:70000/CSV',
        "format": 'csv',
        "description": "EPA TRI facility registry (TRI Facility ID, name, address, lat/long, parent company) pulled via the Envirofacts efservice table API; the documented 'downloads/tri/mv_tri_basic_download' bulk shortcut on the EPA landing page returns HTTP 500 (confirmed dead on repeat tries), but this table-query endpoint works and was verified end-to-end -- 64,990 total rows, full pull succeeded in ~50s returning 19.6MB of real facility records.",
    },
    {
        "group": 'epa',
        "table": 'FED_EPA_SUPERFUND_SITE_BOUNDARIES',
        "url": 'https://services.arcgis.com/cJ9YHowT8TU7DUyn/arcgis/rest/services/FAC_Superfund_Site_Boundaries_EPA_Public/FeatureServer/0/query?where=1%3D1&outFields=*&f=json',
        "format": 'json_api',
        "description": "EPA public ArcGIS FeatureServer for Superfund site boundaries with EPA_ID (CERCLIS-style site ID), region, and program fields, queryable with no auth (verified: 2,114 records, real JSON returned); note this is EPA's current live NPL-boundary layer, narrower than the full historic CERCLIS archive the census evidence described -- the EPA landing page itself has no working bulk CSV/dBASE link anymore, only this FeatureServer and a geospatial NPL_Boundaries.zip. Not one of the six standard loader formats -- needs a new paginated ArcGIS-JSON loader.",
    },
    {
        "group": 'epa',
        "table": 'FED_EPA_GHGRP_FACILITY',
        "url": 'https://www.epa.gov/system/files/other-files/2024-10/2023_data_summary_spreadsheets.zip',
        "format": 'zip_xlsx',
        "description": 'EPA GHGRP facility-level emissions data summary spreadsheets ZIP, confirmed live and 28.4MB; contains 15 Excel files by year plus a combined ghgp_data_by_year_2023.xlsx (facility ID + emissions), which the zip_xlsx loader will pick up as the largest file.',
    },
    # --- USACE ---
    {
        "group": 'usace',
        "table": 'FED_USACE_NID_DAMS',
        "url": 'https://nid.sec.usace.army.mil/api/nation/csv',
        "format": 'csv',
        "description": "USACE National Inventory of Dams full national CSV export (NID ID, owner, location, purpose, hazard class etc.) via the site's own public data API; landing page at nid.sec.usace.army.mil is a JS app with no static download link, but this endpoint returns real data with no auth (verified: 67MB CSV, real dam records, 'Data Last Updated: 2026-8-5').",
    },
    # --- USGS ---
    {
        "group": 'usgs',
        "table": 'FED_USGS_WBD_HUC8',
        "url": 'https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer/4/query?where=1%3D1&outFields=*&f=json&returnGeometry=false',
        "format": 'arcgis_paginated_json',
        "description": 'USGS National Map Hydrologic Unit boundaries ArcGIS MapServer, layer 4 = 8-digit Hydrologic Unit Code (HUC8) polygons with huc8/name/states fields, queryable with no auth (verified: 2,456 records, real JSON); the 2.7GB national WBD geodatabase ZIP also exists and works but is too large/wrong shape for this pipeline, and the plain-text USGS huc_name.txt is an unstructured 1987 narrative document, not tabular data, so this REST layer is the best real fit. 2026-08-07 fix: the unbounded/with-geometry request 500s server-side -- added returnGeometry=false and paginated via resultOffset/resultRecordCount (service maxRecordCount=2000); re-verified today, 2 pages (2000 + 456 = 2,456 records).',
        "page_size": 2000,
    },
    # --- FEMA ---
    {
        "group": 'fema',
        "table": 'FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK',
        "url": 'https://www.fema.gov/api/open/v1/NfipCommunityStatusBook.csv',
        "format": 'csv',
        "description": 'FEMA OpenFEMA API CSV export of the NFIP Community Status Book (Community ID Number, participation status, CRS status), confirmed live with real text/csv content-type and attachment headers.',
    },
    {
        "group": 'fema',
        "table": 'FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK',
        "url": 'https://www.fema.gov/api/open/v1/NfipCommunityStatusBook',
        "format": 'json_api',
        "description": "FEMA OpenFEMA NFIP Community Status Book -- confirmed live JSON API (no auth) returning one record per NFIP-participating community with communityIdNumber, community/county/state, flood map effective dates, and participation status. It's paginated (default page size 1000 via skip/top query params, no total count given), so the assembly step needs a new paging loader function, not one of the existing FORMAT_LOADERS.",
    },
    # --- OCC ---
    {
        "group": 'occ',
        "table": 'FED_OCC_NATIONAL_BANKS_BY_NAME',
        "url": 'https://www.occ.treas.gov/topics/charters-and-licensing/financial-institution-lists/national-by-name.xlsx',
        "format": 'xlsx',
        "description": 'OCC list of active national banks and federal savings associations by charter number, confirmed live Excel file (78KB, real spreadsheetml content-type).',
    },
    {
        "group": 'occ',
        "table": 'FED_OCC_NATIONAL_BANKS_BY_NAME',
        "url": 'https://www.occ.treas.gov/topics/charters-and-licensing/financial-institution-lists/national-by-name.xlsx',
        "format": 'xlsx',
        "description": "OCC's active National Banks & Federal Branches/Agencies list sorted by name (as of 06/30/2026), confirmed as a real 78KB Excel file; column contents (including CHARTER NO) weren't opened/verified beyond confirming the file itself is genuine.",
        "fallback_url": 'https://www.occ.treas.gov/topics/charters-and-licensing/financial-institution-lists/index-financial-institution-lists.html',
    },
    # --- NCUA ---
    {
        "group": 'ncua',
        "table": 'FED_NCUA_FEDERALLY_INSURED_CU_LIST',
        "url": 'https://ncua.gov/files/publications/analysis/federally-insured-credit-union-list-march-2026.zip',
        "format": 'zip_xlsx',
        "description": 'NCUA list of all active federally insured credit unions as of the latest quarter, including charter number and core metrics; confirmed live, zip contains a single FederallyInsuredCreditUnions_2026q1.xlsx (1.1MB). Note: this is the roster/charter list, not the full quarterly Call Report financial-detail dataset the census description implied -- the roster is what resolves to a plain auth-free bulk file.',
    },
    {
        "group": 'ncua',
        "table": 'FED_NCUA_CHARTER_MERGER_EVENTS',
        "url": 'https://ncua.gov/files/publications/analysis/insurance-report-activity-mar-2026.zip',
        "format": 'zip_xlsx',
        "sheet": 'Mergers',  # 2026-08-07 fix: sheet 0 ('Applications_Approved') is empty this quarter.
        "description": 'NCUA quarterly ZIP of credit union chartering/merger event reports (charter number, credit union name, event date, event type, surviving charter number); verified ZIP contains 5 xlsx reports, the largest being insurance-report-activity-detail which matches the census evidence text. 2026-08-07 fix: the workbook has 9 sheets, sheet index 0 (\'Applications_Approved\') is empty this quarter -- loads the \'Mergers\' sheet (8 rows) instead.',
        "fallback_url": 'https://ncua.gov/analysis/chartering-mergers/merger-activity-insurance-report',
    },
    # --- CFPB HMDA ---
    {
        "group": 'cfpb_hmda',
        "table": 'FED_CFPB_HMDA_ARID2017_LEI_XREF',
        "url": 'https://files.ffiec.cfpb.gov/static-data/snapshot/2017/arid2017tolei/arid2017_to_lei_xref_csv.zip',
        "format": 'zip_csv',
        "description": "CFPB/FFIEC crosswalk mapping the legacy HMDA identifier (Agency Code + Respondent ID, concatenated as ARID_2017) to modern LEI codes for 2018-2020; confirmed live, zip contains one CSV (respondent_name, arid_2017, lei_2018, lei_2019, lei_2020). Note: this is the ID crosswalk only -- the FAQ page it was found on does not itself link the full legacy loan-level LAR dataset, which lives on a separate FFIEC 'Snapshot National Loan Level Dataset' page not checked in this batch.",
        "fallback_url": 'https://ffiec.cfpb.gov/documentation/faq/identifiers-faq',
    },
    # --- FHFA ---
    {
        "group": 'fhfa',
        "table": 'FED_FHFA_FHLB_MEMBERSHIP',
        "url": 'https://www.fhfa.gov/document/d/fhlb-m/fhlb_members_q12026.xlsx',
        "format": 'xlsx',
        "description": "FHFA's latest quarterly Federal Home Loan Bank membership listing (Q1 2026), confirmed live as a 754KB Excel file; the landing page links a full quarterly archive back to 2009 if a longer history is wanted later.",
        "fallback_url": 'https://www.fhfa.gov/data/fhlb-membership',
    },
    {
        "group": 'fhfa',
        "table": 'FED_FHFA_SUSPENDED_COUNTERPARTIES',
        "url": 'https://www.fhfa.gov/document/d/scp/download/csv',
        "format": 'csv',
        "description": 'FHFA Suspended Counterparty Program list of individuals/entities barred from doing business with Fannie Mae, Freddie Mac, and the Federal Home Loan Banks.',
    },
    # --- PCAOB ---
    {
        "group": 'pcaob',
        "table": 'FED_PCAOB_FORM_AP_FILINGS',
        "url": 'https://assets.pcaobus.org/firm-filings/FirmFilings.zip',
        "format": 'zip_csv',
        "description": "PCAOB's daily-updated AuditorSearch bulk export -- confirmed live, zip contains one CSV (FirmFilings.csv, ~93MB uncompressed) with one row per Form AP filing, including both Firm ID/Firm Name and Engagement Partner ID/Name/Issuer columns. This single file covers both the PCAOB Firm ID identifier and the PCAOB Form AP Engagement Partner ID identifier (see that candidate's skip note).",
        "fallback_url": 'https://pcaobus.org/resources/auditorsearch',
    },
    # --- IRS ---
    {
        "group": 'irs',
        "table": 'FED_IRS_FATCA_FFI_LIST',
        "url": 'https://apps.irs.gov/app/fatcaFfiList/data/FFIListFull.csv',
        "format": 'csv',
        "description": "IRS's full FATCA FFI list with GIIN numbers; the census URL is an interactive search/download tool page (apps.irs.gov/app/fatcaFfiList/), but its underlying full-list export at this URL is a real, confirmed-live plain CSV (served as octet-stream, no login needed).",
        "fallback_url": 'https://www.irs.gov/businesses/corporations/fatca-foreign-financial-institution-list-search-and-download-tool',
    },
    {
        "group": 'irs',
        "table": 'FED_IRS_527_POLITICAL_ORG_FILINGS',
        "url": 'https://forms.irs.gov/app/pod/dataDownload/fullData',
        "format": 'zip_csv',
        "description": 'IRS Political Organization Filing and Disclosure bulk download -- full database of electronically submitted Forms 8871/8872 (Section 527 political org notifications/reports) as a zipped text file; verified working, ~106MB ZIP, application/zip.',
        "fallback_url": 'https://www.irs.gov/charities-non-profits/political-organizations/political-organization-filing-and-disclosure',
    },
    # --- FINRA ---
    {
        "group": 'finra',
        "table": 'FED_FINRA_MPID_LIST',
        "url": 'https://www.nasdaqtrader.com/dynamic/Symdir/mpidlist.txt',
        "format": 'csv',
        "description": "Nasdaq's live MPID directory (~220KB), confirmed via the header row matching the census evidence exactly. Note: this is PIPE-delimited, not comma-delimited -- the loader for this table needs pd.read_csv(sep='|') instead of the default comma separator.",
        "sep": '|',  # 2026-08-07 fix: confirmed clean parse to 4,215 rows x 9 cols with sep='|'.
    },
    # --- ISO MIC ---
    {
        "group": 'iso_mic',
        "table": 'INTL_ISO_MIC_REGISTRY',
        "url": 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv',
        "format": 'csv',
        "description": "The live ISO 10383 Market Identifier Code registry as CSV; header row (MIC, OPERATING MIC, MARKET NAME, LEGAL ENTITY NAME, LEI, ...) confirmed by fetching real content. Caveat: the server's HEAD response returns HTTP 500 (an Akamai quirk) even though a real GET returns 200 with valid data -- a loader must issue a GET, not rely on a HEAD/HTTP-status precheck.",
        "fallback_url": 'https://www.iso20022.org/market-identifier-codes',
    },
    # --- UK Sanctions ---
    {
        "group": 'uk_sanctions',
        "table": 'INTL_UK_FCDO_SANCTIONS_LIST',
        "url": 'https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.csv',
        "format": 'csv',
        "description": "FCDO's live UK Sanctions List, confirmed as a real ~49.6MB CSV (served as octet-stream); this is the current successor to the retired OFSI Consolidated List that the census description referenced.",
        "fallback_url": 'https://www.gov.uk/government/publications/the-uk-sanctions-list',
    },
    {
        "group": 'uk_sanctions',
        "table": 'INTL_UK_FCDO_SANCTIONS_LIST',
        "url": 'https://sanctionslist.fcdo.gov.uk/docs/UK-Sanctions-List.csv',
        "format": 'csv',
        "description": 'Full UK Sanctions List (designated persons/entities/ships) in CSV; verified live 200 OK, 49.6MB, attachment content-disposition, real file (also available as .ods/.xml at the same path pattern).',
    },
    # --- Trade.gov ---
    {
        "group": 'trade_gov',
        "table": 'FED_TRADE_CONSOLIDATED_SCREENING_LIST',
        "url": 'https://data.trade.gov/downloadable_consolidated_screening_list/v1/consolidated.csv',
        "format": 'csv',
        "description": 'Consolidated Screening List combining BIS Entity List, Denied Persons List, Unverified List and other US export-control/sanctions party lists in one CSV; verified 16.6MB CSV with a source/programs field confirming BIS lists are included (e.g. Non-SDN Chinese Military-Industrial Complex entries observed in sample).',
        "fallback_url": 'https://www.trade.gov/consolidated-screening-list',
    },
    # --- UN Sanctions ---
    # 2026-08-07 fix: there were two manifest entries for this same underlying
    # data (one 'json_api' pointed at the dead scsanctions.un.org redirect
    # chain, one 'xml' pointed at the direct Azure blob URL). Kept only the
    # corrected xml one and removed the broken json_api duplicate; a real xml
    # loader is now registered in FORMAT_LOADERS (parses <INDIVIDUALS>/
    # <INDIVIDUAL> and <ENTITIES>/<ENTITY> via xml.etree). Re-verified today:
    # 736 individuals + 275 entities = 1,011 records.
    {
        "group": 'un_sanctions',
        "table": 'INTL_UN_SC_CONSOLIDATED_SANCTIONS',
        "url": 'https://unsolprodfiles.blob.core.windows.net/publiclegacyxmlfiles/EN/consolidated.xml',
        "format": 'xml',
        "description": 'UN Security Council Consolidated Sanctions List (individuals + entities), raw XML hosted on Azure Blob Storage; the scsanctions.un.org domain cited in the census is fully dead (404 on every path), the working host was found via web search and verified live 200 OK, 2.5MB, real XML content, last-modified Aug 6 2026. 2026-08-07: real xml loader implemented (parses <INDIVIDUALS>/<INDIVIDUAL> and <ENTITIES>/<ENTITY>, tags RECORD_TYPE).',
    },
    # --- PBGC ---
    {
        "group": 'pbgc',
        "table": 'FED_PBGC_TRUSTEED_PENSION_PLANS',
        "url": 'https://www.pbgc.gov/sites/default/files/singleemployerlist.xlsx',
        "format": 'xlsx',
        "description": 'PBGC list of single-employer pension plans currently trusteed by PBGC (8-digit case number, plan name, company); verified working xlsx download. A companion multiemployer list also verified working at https://www.pbgc.gov/sites/default/files/multiemployerlist.xlsx.',
        "fallback_url": 'https://www.pbgc.gov/workers-retirees/trusteed-plans',
    },
    # --- FJC ---
    {
        "group": 'fjc',
        "table": 'FED_FJC_ARTICLE_III_JUDGES',
        "url": 'https://www.fjc.gov/sites/default/files/history/judges.csv',
        "format": 'csv',
        "description": 'FJC Biographical Directory of Article III Federal Judges flat-file export; verified 5.4MB CSV with a leading nid column (the unique judge identifier) plus biographical/appointment fields.',
        "fallback_url": 'https://www.fjc.gov/history/judges/biographical-directory-article-iii-federal-judges-export',
    },
    # --- ATF ---
    {
        "group": 'atf',
        "table": 'FED_ATF_FFL_LOCATIONS',
        "url": 'https://services6.arcgis.com/PrP5ZtrES07DmVmv/arcgis/rest/services/Federal_Firearm_Licensees_locations/FeatureServer/0/query?where=1%3D1&outFields=*&f=json',
        "format": 'json_api',
        "description": 'ATF Federal Firearms Licensee locations. The atf.gov listing page itself is blocked by Akamai bot protection (403 on direct fetch), but the data.gov catalog page links to a public ArcGIS item that resolves (via the ArcGIS sharing REST API) to an open FeatureServer; verified query endpoint returns a count of 77,514 records with no auth required. JSON API, not a flat file -- needs a new loader that pages through results (ArcGIS caps rows per query, typically via resultOffset).',
        "fallback_url": 'https://catalog.data.gov/dataset/federal-firearms-licensees',
    },
    # --- Deportation Data Project ---
    {
        "group": 'deportation_data_project',
        "table": 'FED_ICE_DETENTIONS_DDP',
        "url": 'https://ucla.box.com/shared/static/csnihndb826omzizlps90szm60q39jxd.zip',
        "format": 'zip_csv',
        "description": "ICE detention records (individual-level, includes the Detention Facility Code/DETLOC field) compiled from FOIA releases by the Deportation Data Project (UCLA). Verified real: HTTP 200, application/zip, but far bigger than the census's 'small' size guess -- Content-Length ~2.6GB. The assembly step should NOT reuse the in-memory read-whole-response pattern from the existing loaders unmodified; it needs streaming/chunked handling, and the zip should be inspected for whether it holds one CSV (zip_csv) or several (zip_multi) before finalizing the loader.",
        "fallback_url": 'https://deportationdata.org/data/ice.html',
    },
    # --- CA CAL-ACCESS ---
    {
        "group": 'ca_calaccess',
        "table": 'ST_CA_CALACCESS_RAW',
        "url": 'https://campaignfinance.cdn.sos.ca.gov/dbwebexport.zip',
        "format": 'zip_multi',
        "description": 'Full raw CAL-ACCESS relational database export (California campaign finance AND lobbyist registration/activity tables together) as a ~1.5GB ZIP of tab-delimited text files, refreshed daily; assembly should pull out just the lobbyist-related tables if a narrower scope is wanted.',
        "fallback_url": 'https://www.sos.ca.gov/campaign-lobbying/helpful-resources/raw-data-campaign-finance-and-lobbying-activity',
    },
    # --- Elections Canada ---
    {
        "group": 'elections_canada',
        "table": 'INTL_ELECTIONS_CANADA_CONTRIBUTIONS',
        "url": 'https://www.elections.ca/fin/oda/od_cntrbtn_de_e.zip',
        "format": 'zip_csv',
        "description": 'Elections Canada Open Data - detailed contributions to registered federal political parties, candidates, and other entities. The landing page URL in the census was a nav page, not a file; real download links live on the Open Data sub-page. Companion files at the same path (contribution audits, 1993-2004 historical candidate/party archives) are also real and could be added later. 2026-08-07 fix: source hits exactly 5,000,001 rows against the default 5,000,000 max_rows cap (truncated-and-rejected, not actually broken) -- per-entry max_rows override raises the cap for this source only.',
        "fallback_url": 'https://www.elections.ca/content.aspx?section=fin&dir=oda&document=index&lang=e',
        "max_rows": 30_000_000,  # 2026-08-07 fix: per-entry override, doesn't touch the --max-rows default.
    },
    # --- NYC CFB ---
    {
        "group": 'nyc_cfb',
        "table": 'ST_NYC_CFB_CAMPAIGN_FINANCE',
        "url": 'https://www.nyccfb.info/DataLibrary/CFB-Data.zip',
        "format": 'zip_multi',
        "description": 'NYC Campaign Finance Board full data library bundle (~102MB ZIP) - contributions, expenditures, intermediaries, and public funds payments for all candidates across election cycles 2001-2025.',
        "fallback_url": 'https://www.nyccfb.info/follow-the-money/data-library/',
    },
    # --- NTSB ---
    {
        "group": 'ntsb',
        "table": 'FED_NTSB_AVIATION_ACCIDENTS',
        "url": 'https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip',
        "format": 'mdb',
        "mdb_tables": ['events', 'aircraft', 'injury'],
        "description": "NTSB aviation accident/incident database bulk export (avall.zip, ~95MB) with normalized tables for events, aircraft, and injuries. The census's app.ntsb.gov/avdata host has been retired and now redirects to data.ntsb.gov/avdata - use the new host. 2026-08-07 fix: the zip's real content is avall.mdb (a Microsoft Access database, 555MB uncompressed, 19 tables), not CSVs -- the old zip_csv/zip_multi loaders found zero CSVs and silently did nothing. Confirmed this environment has pyodbc + the 'Microsoft Access Driver (*.mdb, *.accdb)' ODBC driver installed, so a real mdb loader was implemented (extracts to a temp file, connects via pyodbc, pulls the named mdb_tables into separate landing tables) rather than leaving this as a documented skip. Re-verified today: events=30,968 rows, aircraft and injury tables also read cleanly.",
        "fallback_url": 'https://www.ntsb.gov/safety/data/Pages/Data_Stats.aspx',
    },
    # --- FAA ADIP ---
    {
        "group": 'faa_adip',
        "table": 'FED_FAA_ADIP_PRIVATE_AIRPORTS',
        "url": 'https://adip.faa.gov/publishedAirports/PrivateAirportReport.xlsx',
        "format": 'xlsx',
        "description": "FAA ADIP's published Private Airport Report (Excel, confirmed working) covering private-use airport location identifiers and facility details. Scope caveat: this is the private-airport subset only - adip.faa.gov itself is a JS single-page app (map/search UI) with no public-use/all-airports bulk export found, and the fuller 5010 master record lives in FAA's separate NASR subscription product, which needs its own check before relying on it.",
    },
    # --- FMC ---
    {
        "group": 'fmc',
        "table": 'FED_FMC_OTI_NVOCC_LIST',
        "url": 'https://www2.fmc.gov/oti/NVOCC.aspx',
        "format": 'xlsx',
        "description": "FMC list of active licensed/registered Ocean Transportation Intermediaries (NVOCCs and Ocean Freight Forwarders), delivered as an Excel export. Confirmed real by actually triggering the page's 'OTI List Download' button: it's an ASP.NET webforms postback (POST with __VIEWSTATE/__EVENTVALIDATION), not a plain GET link, and returned a genuine 1.8MB .xlsx file. The assembly step needs a loader that simulates that form postback rather than a simple GET.",
    },
    # --- JPML ---
    {
        "group": 'jpml',
        "table": 'FED_JPML_PENDING_MDLS',
        "url": 'https://www.jpml.uscourts.gov/sites/jpml/files/Pending_MDL_Dockets_By_MDL_Number-August-3-2026.pdf',
        "format": 'pdf',
        "description": "JPML's monthly pending-MDL docket report sorted by MDL number, confirmed real and downloadable (refreshed monthly; By District/By Type/By Actions Pending variants and a Recently Terminated report also exist at the same page). It is PDF-only - no CSV/Excel version exists - so this needs a new PDF-table-extraction loader, not one of the existing formats. Also note: the site's WAF 404s a bare curl request without an Accept-Language header, but resolves fine with normal browser-like headers.",
        "fallback_url": 'https://www.jpml.uscourts.gov/pending-mdls-0',
    },
    # --- FDA ---
    {
        "group": 'fda',
        "table": 'FED_FDA_CAERS_FOOD_EVENTS',
        "url": 'https://api.fda.gov/food/event.json',
        "format": 'json_api',
        "description": "openFDA Food Event API (CAERS) - confirmed live JSON API, no key required for basic use (151,589 total records at check time); the census's open.fda.gov/apis/food/event/ URL is documentation, this is the real API endpoint, paginated via skip/limit query params.",
    },
    # --- CA OEHHA ---
    {
        "group": 'ca_oehha',
        "table": 'ST_CA_OEHHA_PROP65_CHEMICALS',
        "url": 'https://oehha.ca.gov/sites/default/files/media/2025-01/p65chemicalslist.csv',
        "format": 'csv',
        "description": 'OEHHA Proposition 65 list of chemicals known to California to cause cancer or reproductive harm, as CSV (~70KB). The site runs Incapsula bot protection, so a bare curl request to the file alone gets a JS-challenge page; a normal client that first loads the listing page (picking up the Incapsula session cookie) then gets the real CSV, which is what happened here - this is a genuine no-login block, not an auth wall.',
    },
    # --- Education (ED/NCES) ---
    {
        "group": 'education',
        "table": 'FED_ED_SCORECARD_INSTITUTION',
        "url": 'https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_06102026.zip',
        "format": 'zip_csv',
        "description": 'US Dept of Education College Scorecard institution-level file (confirmed real ZIP/CSV, 3308 columns); every row carries OPEID and OPEID6 alongside the IPEDS UNITID, so this file itself is the OPEID-to-UNITID crosswalk the census was pointing at -- the landing page URL is JS-rendered so I pulled the real download link straight out of its payload.',
        "fallback_url": 'https://collegescorecard.ed.gov/data/',
    },
    {
        "group": 'education',
        "table": 'FED_ED_NCES_CIP_CODES',
        "url": 'https://nces.ed.gov/ipeds/cipcode/Files/CIPCode2010.csv',
        "format": 'csv',
        "description": 'NCES Classification of Instructional Programs code table -- confirmed real CSV (2,319 rows) with CIPFamily/CIPCode/CIPTitle/CIPDefinition columns; this is the CIP2010 vintage (the 2020 revision only ships as an Excel CIP-to-SOC crosswalk, not a standalone code list, on the same page).',
        "fallback_url": 'https://nces.ed.gov/ipeds/cipcode/',
    },
    # --- HUD ---
    {
        "group": 'hud',
        "table": 'FED_HUD_MF_FIRM_COMMITMENTS',
        "url": 'https://www.hud.gov/sites/default/files/Housing/documents/FHA-MF-Firm-Commitments-and-Endorsements-Database-FY01-FY26-Q3.xlsx',
        "format": 'xlsx',
        "sheet": 'Firm Commitments',
        "description": "HUD FHA Multifamily Firm Commitments and Initial Endorsements database, FY2001 through FY2026 Q3 (confirmed real xlsx, 8.2MB, 3 sheets: Firm Commitments / Initial Endorsements / HFA FFB Usage); keyed on FHA Number, which is the Multifamily Project Number -- note the real column header row is row 10 (there's a title/cover block above it), so the existing xlsx loader needs a header-row-offset option, it can't just read row 0.",
        "fallback_url": 'https://www.hud.gov/hud-partners/multifamily-data',
    },
    {
        "group": 'hud',
        "table": 'FED_HUD_FHA_SF_PORTFOLIO_SNAPSHOT',
        "url": 'https://www.hud.gov/sites/default/files/Housing/documents/FHA_SF_Forward_Snapshot_JUN2026.xlsx',
        "format": 'xlsx',
        "sheet": 'Purchase Data June 2026',
        "description": "HUD FHA Single Family Forward Portfolio Snapshot for June 2026 (confirmed real xlsx, 10.6MB); the 'Purchase Data June 2026' sheet has a clean header row 0 with Originating Mortgagee Number, Sponsor Number, and property location fields exactly as the census evidence described. This is a monthly-refreshed file (new filename and sheet name each month), so the loader will need to be pointed at the latest month going forward.",
        "fallback_url": 'https://www.hud.gov/stat/sfh/fha-sf-portfolio-snapshot',
    },
    {
        "group": 'hud',
        "table": 'FED_HUD_PUBLIC_HOUSING_AUTHORITIES',
        "url": 'https://opendata.arcgis.com/api/v3/datasets/3d6ef39026b94eb59ddb7ce28eb0b692_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1',
        "format": 'csv',
        "description": "HUD Public Housing Authorities dataset via HUD's ArcGIS Open Data hub (confirmed real CSV, 3,788 rows) with PARTICIPANT_CODE (the PHA code), formal name, contact info, occupancy and funding fields; the data.gov page only advertises Shapefile/geodatabase downloads but the same underlying ArcGIS dataset also serves a flat CSV via its API, which is the link recorded here.",
        "fallback_url": 'https://catalog.data.gov/dataset/public-housing-authorities',
    },
    {
        "group": 'hud',
        "table": 'FED_HUD_MF_SECTION8_CONTRACTS',
        "url": 'https://www.hud.gov/sites/dfiles/Housing/documents/MF-Assistance-Sec8-Contracts1.xlsx',
        "format": 'xlsx',
        "description": "HUD Multifamily Assistance & Section 8 Contracts database (confirmed real xlsx, 4.7MB, single sheet, clean header row 0) -- one row per contract_number (the HAP Contract Number) with property_id, TRACS effective/expiration dates, contract status, and assisted-unit counts. Census evidence described an old MS Access 7.0 format; the live download has since moved to a clean XLSX, which is what's recorded here. A companion properties-level file also exists at the same URL pattern (MF-Properties-with-Assistance-Sec8-Contracts1.xlsx, 10.7MB, also confirmed real) if that grain is wanted too.",
        "fallback_url": 'https://www.hud.gov/hud-partners/multifamily-assist-section8-database',
    },
    # --- USDA Rural Development ---
    {
        "group": 'usda_rd',
        "table": 'FED_USDA_RD_MFH_ACTIVE_PROJECTS',
        "url": 'https://www.sc.egov.usda.gov/data/files/MFH_Section_515/ActiveProjects/mfhd_active_projects.csv',
        "format": 'csv',
        "description": 'USDA Rural Development active Section 515/514 multifamily housing projects, one row per project with location, loan/program IDs, LIHTC ID, and unit counts.',
    },
    # --- USASpending ---
    {
        "group": 'usaspending',
        "table": 'FED_USASPENDING_TAS_FILTER_TREE',
        "url": 'https://api.usaspending.gov/api/v2/references/filter_tree/tas/',
        "format": 'json_api',
        "description": 'USASpending.gov reference API returning the full CGAC agency-code tree with TAS counts per agency (confirmed live JSON, ~100 agencies with codes/descriptions/counts); it is a hierarchical drill-down API (agency -> federal account -> TAS list via /tas/<AGENCY>/<FEDERAL_ACCOUNT>/), not a single bulk file, so format is json_api and the assembly step needs a loader that walks the tree rather than a one-shot fetch.',
    },
    # --- SBIR ---
    {
        "group": 'sbir',
        "table": 'FED_SBIR_STTR_AWARDS',
        "url": 'https://data.www.sbir.gov/mod_awarddatapublic_no_abstract/award_data_no_abstract.csv',
        "format": 'csv',
        "description": 'SBIR.gov full award-level database of all SBIR/STTR awards without abstracts, confirmed live (200 OK, 91MB CSV via CloudFront/S3); the with-abstracts variant is also available at https://data.www.sbir.gov/mod_awarddatapublic/award_data.csv but is larger (~290MB).',
    },
    # --- EIA-860 ---
    {
        "group": 'eia_860',
        "table": 'FED_EIA_860_PLANT',
        "url": 'https://www.eia.gov/electricity/data/eia860/xls/eia8602024.zip',
        "format": 'zip_xlsx',
        "member": '2___Plant_Y2024.xlsx',
        "sheet": 'Plant',
        "description": "EIA-860 2024 plant-level data, confirmed inside the live zip as member file '2___Plant_Y2024.xlsx' (sheet 'Plant'); the zip bundles 13 files for different EIA-860 sub-schedules (utility, plant, generator, wind, solar, storage, owner, environmental), so the existing zip_xlsx loader's largest-file heuristic will pick the wrong file -- assembly needs a variant that extracts by exact member filename.",
    },
    {
        "group": 'eia_860',
        "table": 'FED_EIA_860_UTILITY',
        "url": 'https://www.eia.gov/electricity/data/eia860/xls/eia8602024.zip',
        "format": 'zip_xlsx',
        "member": '1___Utility_Y2024.xlsx',
        "sheet": 'Utility',
        "description": "EIA-860 2024 utility-level data, confirmed inside the live zip as member file '1___Utility_Y2024.xlsx' (sheet 'Utility'); same zip as the Plant and Generator entries in this batch -- assembly needs a loader variant that extracts by exact member filename rather than largest-file-in-zip.",
    },
    {
        "group": 'eia_860',
        "table": 'FED_EIA_860_GENERATOR',
        "url": 'https://www.eia.gov/electricity/data/eia860/xls/eia8602024.zip',
        "format": 'zip_xlsx',
        "member": '3_1_Generator_Y2024.xlsx',
        "sheet": 'Operable',
        "description": "EIA-860 2024 generator-level data, confirmed inside the live zip as member file '3_1_Generator_Y2024.xlsx' with three tabs (Operable, Proposed, Retired and Canceled); same zip as the Plant and Utility entries in this batch -- assembly needs a loader variant that extracts by exact member filename and likely needs to union or pick a specific tab.",
    },
    # --- BOEM ---
    {
        "group": 'boem',
        "table": 'FED_BOEM_LEASE_REGISTER',
        "url": 'https://www.data.boem.gov/Leasing/Files/lstleasefixed.zip',
        "format": 'fixed_width',
        "description": "BOEM offshore lease register (lease number, status, effective/expiration/relinquish dates, owning company code), confirmed live -- but the zip's single member (LSTLEASE.DAT) is genuinely fixed-width ASCII, not comma/tab delimited (verified by inspecting raw content), so it fits none of the standard CSV/Excel formats; assembly needs a new fixed-width parser (BOEM publishes the column-position layout as a companion PDF in the same /Leasing/Files/ directory).",
    },
    # --- EIA-861 ---
    {
        "group": 'eia_861',
        "table": 'FED_EIA_861_BALANCING_AUTHORITY',
        "url": 'https://www.eia.gov/electricity/data/eia861/zip/f8612024.zip',
        "format": 'zip_xlsx',
        "member": 'Balancing_Authority_2024.xlsx',
        "sheet": 'Balancing Authority',
        "description": "EIA-861 2024 balancing authority list with the states each one operates in, confirmed inside the live zip as member file 'Balancing_Authority_2024.xlsx' (sheet 'Balancing Authority'); the zip bundles 20 EIA-861 sub-files, so assembly needs a loader variant that extracts this specific member by filename rather than the largest file in the zip.",
    },
    # --- OSFI ---
    {
        "group": 'osfi',
        "table": 'INTL_OSFI_REGULATED_FI',
        "url": 'https://open.canada.ca/data/dataset/b27ec3ef-7338-4e76-a6fd-128339a92df5/resource/945045fa-2de0-47d4-aad2-144d69467824/download/who_we_regulate_fi_eng.csv',
        "format": 'csv',
        "description": 'OSFI list of ~350 federally regulated Canadian financial institutions with company name, FI type/group/industry, and representative contact info, confirmed live (200 OK, 116KB CSV after following the open.canada.ca redirect to the Azure blob host); the raw open.canada.ca host blocks bare curl requests without a Referer header/full browser UA, so the loader needs those headers set.',
    },
    # --- Education (ED) ---
    {
        "group": 'ed',
        "table": 'FED_ED_COLLEGE_SCORECARD_INSTITUTION',
        "url": 'https://ed-public-download.scorecard.network/downloads/Most-Recent-Cohorts-Institution_06102026.zip',
        "format": 'zip_csv',
        "description": 'Most recent institution-level College Scorecard data (ZIP containing CSV), OPE ID to IPEDS UNITID crosswalk included; verified live 200 OK, 23.5MB zip, application/zip -- confirmed real download host is ed-public-download.scorecard.network, not the collegescorecard.ed.gov landing page.',
    },
    # --- ROR ---
    {
        "group": 'ror',
        "table": 'XC_ROR_RESEARCH_ORGANIZATIONS',
        "url": 'https://zenodo.org/api/records/21773148/files/v2.11-2026-08-03-ror-data.zip/content',
        "format": 'zip_csv',
        "description": "ROR registry dump, current release v2.11 (Aug 3 2026, 135,710 orgs, 35.6MB ZIP) containing schema-v2 JSON (primary) plus CSV; direct curl was blocked by Zenodo's bot-detection WAF (403 'unusual traffic from your network') but WebFetch independently confirmed the live record twice with matching real filename/size/DOI/checksum, so treated as verified live -- assembly step should extract the CSV via zip_csv loader logic but note the JSON is the authoritative format.",
    },
    # --- Crossref ---
    {
        "group": 'crossref',
        "table": 'XC_RETRACTION_WATCH_DATABASE',
        "url": 'https://gitlab.com/crossref/retraction-watch-data/-/raw/main/retraction_watch.csv',
        "format": 'csv',
        "description": 'Combined Retraction Watch + Crossref retraction records CSV, raw file confirmed at the GitLab repo (found via repository tree API); verified live 200 OK, 65.6MB, real CSV content.',
    },
    {
        "group": 'crossref',
        "table": 'XC_CROSSREF_FUNDER_REGISTRY',
        "url": 'https://doi.crossref.org/funderNames?mode=list',
        "format": 'csv',
        "description": 'CC0-licensed CSV of the latest Crossref Open Funder Registry (funder IDs mapped to https://doi.org/10.13039/[ID]); verified live 200 OK, real CSV content returned (content-type text/comma-separated-values).',
    },
    # --- NSF ---
    {
        "group": 'nsf',
        "table": 'FED_NSF_AWARDS',
        "url": 'http://api.nsf.gov/services/v1/awards.json',
        "format": 'json_api',
        "description": 'NSF Award Search API, no authentication required; verified live 200 OK with real JSON award records returned for a test keyword query, output formats XML/JSON/JSONP as claimed -- needs a new JSON-API loader (paginated keyword/date queries, not a single bulk file).',
    },
    # --- Grants.gov ---
    {
        "group": 'grants_gov',
        "table": 'FED_GRANTSGOV_EXTRACT',
        "url": 'https://prod-grants-gov-chatbot.s3.amazonaws.com/extracts/GrantsDBExtract20260807v2.zip',
        "format": 'zip_xml',
        "description": "Daily full export of the Grants.gov database as a ZIP containing a single large XML file (not CSV, not JSON); verified live 200 OK, 77.9MB zip, real S3-hosted file matching the day's date (Aug 7 2026) -- does not fit any of the six standard formats or the JSON-API case, needs a new zip_xml loader (unzip, parse XML elements).",
    },
    # --- OSF ---
    {
        "group": 'osf',
        "table": 'XC_OSF_REGISTRATIONS',
        "url": 'https://api.osf.io/v2/registrations/',
        "format": 'json_api',
        "description": 'OSF API v2 registrations endpoint, no authentication required; verified live 200 OK with real registration records returned (titles, descriptions, ids) -- needs a new JSON-API loader with pagination, not a single bulk file. 2026-08-07 fix: pd.json_normalize does not fully flatten nested list/dict-valued columns from this API -- load_json_api now json.dumps()\'s any object-dtype column containing non-scalar values before write, as a general safety step (not just this entry).',
    },
    # --- ISO ---
    {
        "group": 'iso',
        "table": 'INTL_ISO_MIC_REGISTRY',
        "url": 'https://www.iso20022.org/sites/default/files/ISO10383_MIC/ISO10383_MIC.csv',
        "format": 'csv',
        "description": 'Latest ISO 10383 Market Identifier Codes list (exchanges/venues), CSV format; HEAD requests return HTTP 500 from the Akamai-fronted host (a known quirk) but a real GET returns valid CSV data with header row and real MIC records -- loader must use GET (the reference script already does), not HEAD.',
    },
]

# ---------------------------------------------------------------------------
# Loaders by format
# ---------------------------------------------------------------------------

# This batch is scoped to confirmed small/medium-size sources -- every loader
# below reads the whole response into memory (io.BytesIO), which is fine up
# to ~100MB (the largest legitimate entry in this manifest, IRS 527, is
# ~106MB) but is the wrong pattern for the two outsized entries that slipped
# into the manifest: FED_ICE_DETENTIONS_DDP (~2.6GB) and ST_CA_CALACCESS_RAW
# (~1.5GB) -- both explicitly flagged in their own descriptions as needing a
# streaming/chunked loader instead. Rather than silently attempt a multi-GB
# in-memory download (which could exhaust memory or hang the run for a very
# long time), every fetch below is capped: it aborts cleanly with a clear
# RuntimeError the moment the response exceeds this size, so an oversized
# entry lands in the normal failure summary instead of stalling the batch.
MAX_DOWNLOAD_BYTES = 500_000_000  # 500MB


def _get(url: str, timeout: int, max_bytes: int = MAX_DOWNLOAD_BYTES,
         session_warmup_url: str | None = None) -> bytes:
    """Streaming GET with a hard cap on total response size.

    session_warmup_url (2026-08-07 fix, FED_IHS_SCB_FACILITY): if given,
    GET that URL first in the same requests.Session to establish a session
    cookie the real download needs, then GET the real url in that same
    session. A plain requests.get(url) with no prior request returns an
    HTML page instead of data for that source. Entries that don't set this
    key behave exactly as before (a fresh, cookie-less GET).
    """
    session = requests.Session()
    if session_warmup_url:
        warmup = session.get(session_warmup_url, timeout=timeout, headers=USER_AGENT)
        warmup.raise_for_status()
    resp = session.get(url, timeout=timeout, headers=USER_AGENT, stream=True)
    resp.raise_for_status()
    chunks = []
    total = 0
    try:
        for chunk in resp.iter_content(chunk_size=1024 * 1024):
            total += len(chunk)
            if total > max_bytes:
                raise RuntimeError(
                    f"response exceeded {max_bytes:,} byte cap (aborted at "
                    f"{total:,} bytes) -- this source needs a dedicated "
                    f"streaming loader, not the standard in-memory one")
            chunks.append(chunk)
    finally:
        resp.close()
    return b"".join(chunks)


def _provenance(content: bytes) -> tuple[str, str, dt.datetime]:
    sha = hashlib.sha256(content).hexdigest()
    run_id = str(uuid.uuid4())
    started = dt.datetime.now(dt.timezone.utc)
    return sha, run_id, started


def _stamp(df: pd.DataFrame, sha: str, run_id: str, started: dt.datetime) -> pd.DataFrame:
    df[bulk.META_INGESTED_AT] = started.replace(tzinfo=None)
    df[bulk.META_SOURCE_RUN_ID] = run_id
    df[bulk.META_SRC_SHA256] = sha
    return df


def _sf_col(name: str) -> str:
    """Sanitize a source column name for Snowflake (2026-08-07 fix, scoped to
    this script only -- does NOT touch the shared library-onboarding/ingest.py
    sanitizer other loaders depend on).

    FED_PCAOB_FORM_AP_FILINGS crashed write_pandas with a duplicate-column
    error because 'Amendment Participants > 5%' and 'Amendment Participants
    < 5%' both sanitize to the same identifier under the shared sanitizer
    (both '>' and '<' collapse to '_'). Map '>' -> '_GT_' and '<' -> '_LT_'
    first so those two stay distinct, then fall through to bulk.sf_col for
    everything else -- columns without '>'/'<' sanitize identically to
    before.
    """
    name = str(name).replace(">", "_GT_").replace("<", "_LT_")
    return bulk.sf_col(name)


def _dedupe_cols(cols: list[str]) -> list[str]:
    """Defensive safety net: disambiguate any exact-duplicate sanitized
    column names with a numeric suffix instead of crashing write_pandas.
    The >/< mapping in _sf_col should prevent the PCAOB-style collision,
    but this catches any other unforeseen collision too."""
    seen: dict[str, int] = {}
    out = []
    for c in cols:
        if c not in seen:
            seen[c] = 1
            out.append(c)
        else:
            seen[c] += 1
            out.append(f"{c}_{seen[c]}")
    return out


def _write(conn, df: pd.DataFrame, tbl: str, *,
           sha: str = "", run_id: str = "", source_url: str = "") -> int:
    from snowflake.connector.pandas_tools import write_pandas
    df.columns = _dedupe_cols([_sf_col(c) for c in df.columns])
    ok, _c, _n, _ = write_pandas(
        conn, df, table_name=tbl,
        database=bulk.LANDING_DB, schema=bulk.LANDING_SCHEMA,
        auto_create_table=True, overwrite=True, quote_identifiers=False,
    )
    if not ok:
        raise RuntimeError(f"write_pandas failed for {tbl}")
    # Quality gate + INGEST_RUNS row (same gate-bypass fix as the tier1 batch
    # loader). A dq_failed load raises so it lands in the failure summary and
    # the exit code, never a silent "success".
    passed, report = bulk.run_quality_gate(
        conn, tbl, tbl, run_id or str(uuid.uuid4()),
        sha256=sha, source_url=source_url)
    if not passed:
        raise RuntimeError(f"{tbl}: quality gate failed -- {report}")
    return len(df)


def load_csv(conn, entry: dict, max_rows: int) -> int:
    content = _get(entry["url"], timeout=300,
                   session_warmup_url=entry.get("session_warmup_url"))
    sha, run_id, started = _provenance(content)
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace",
                     sep=entry.get("sep", ","))
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_zip_csv(conn, entry: dict, max_rows: int) -> int:
    content = _get(entry["url"], timeout=600)
    sha, run_id, started = _provenance(content)
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        # ONE member or entry["member"] pattern -- never largest-wins
        # (the EIA-860 multi-file truncation trap this file documented).
        chosen = pick_member(zf, pattern=entry.get("member"),
                             suffixes=(".csv", ".txt"))
        with zf.open(chosen) as f:
            content = f.read()
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace",
                     sep=entry.get("sep", ","))
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_zip_multi(conn, entry: dict, max_rows: int) -> int:
    """Load multiple CSVs from a ZIP (e.g., multi-table bundles)."""
    content = _get(entry["url"], timeout=900)
    sha, run_id, started = _provenance(content)
    total = 0
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        csv_files = [n for n in zf.namelist()
                     if n.lower().endswith('.csv') and not n.startswith('__MACOSX')]
        # Deliberate multi-file load: top-5 by size, every pick printed.
        csv_files.sort(key=lambda n: zf.getinfo(n).file_size, reverse=True)  # archive-gate: allow
        for name in csv_files[:5]:
            tbl = bulk.table_name(entry["table"].rsplit("_", 1)[0], Path(name).stem)
            try:
                with zf.open(name) as f:
                    content = f.read()
                df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                                 low_memory=False, encoding_errors="replace")
                if len(df) > max_rows:
                    raise RuntimeError(
                        f"{tbl}: source has more than max_rows={max_rows:,} rows -- "
                        f"refusing to silently truncate. Pass a higher max_rows explicitly.")
                if df.empty:
                    continue
                df = _stamp(df, sha, run_id, started)
                n = _write(conn, df, tbl, sha=sha, run_id=run_id,
                           source_url=entry["url"])
                print(f"      {tbl}: {n:,} rows")
                total += n
            except Exception as e:
                print(f"      FAILED {tbl}: {str(e)[:100]}")
    return total


def load_zip_xlsx(conn, entry: dict, max_rows: int) -> int:
    """Load Excel from inside a ZIP.

    Some zips bundle many Excel files (EIA-860/861 sub-schedules) and the
    "largest file in the zip" heuristic silently grabs the wrong one when
    that happens -- if the manifest entry names an exact "member" filename,
    honor it instead of guessing by size.
    """
    content = _get(entry["url"], timeout=600)
    sha, run_id, started = _provenance(content)
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        member = entry.get("member")
        if member:
            matches = [n for n in zf.namelist() if Path(n).name == member]
            if not matches:
                raise RuntimeError(
                    f"member '{member}' not found in ZIP for {entry['table']} "
                    f"(zip contains: {zf.namelist()[:10]})")
            chosen = matches[0]
        else:
            # ONE Excel member or entry["member"] -- never largest-wins.
            chosen = pick_member(zf, suffixes=(".xlsx", ".xls"))
        with zf.open(chosen) as f:
            xlsx_content = f.read()
    sheet = entry.get("sheet", 0)
    df = pd.read_excel(io.BytesIO(xlsx_content), dtype=str, nrows=max_rows + 1, sheet_name=sheet)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_xlsx(conn, entry: dict, max_rows: int) -> int:
    content = _get(entry["url"], timeout=300)
    sha, run_id, started = _provenance(content)
    sheet = entry.get("sheet", 0)
    df = pd.read_excel(io.BytesIO(content), dtype=str, nrows=max_rows + 1, sheet_name=sheet)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_bz2_csv(conn, entry: dict, max_rows: int) -> int:
    import bz2
    content = _get(entry["url"], timeout=600)
    sha, run_id, started = _provenance(content)
    decompressed = bz2.decompress(content)
    df = pd.read_csv(io.BytesIO(decompressed), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace")
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_mdb(conn, entry: dict, max_rows: int) -> int:
    """Extract tables out of a zipped MS Access (.mdb) database.

    2026-08-07 fix, FED_NTSB_AVIATION_ACCIDENTS: the zip's real content is
    avall.mdb, not CSVs -- the zip_csv/zip_multi loaders find zero CSV files
    and silently do nothing. pyodbc + the "Microsoft Access Driver (*.mdb,
    *.accdb)" ODBC driver are confirmed present in this environment
    (2026-08-07 diagnostic: real connection, table list, and row reads all
    verified against the live NTSB file), so this is a genuine loader, not a
    stub. pyodbc's Access driver needs a real file on disk (no in-memory
    DSN-less option), so the .mdb member is extracted to a temp file and
    cleaned up after. Loads each table named in entry["mdb_tables"] (or, if
    that key is absent, every non-system table in the database) into its own
    landing table, the same one-table-in/many-tables-out shape as
    load_zip_multi.
    """
    import tempfile
    import pyodbc

    content = _get(entry["url"], timeout=600)
    sha, run_id, started = _provenance(content)
    total = 0
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        # ONE Access db or entry["member"] -- never largest-wins.
        mdb_name = pick_member(zf, pattern=entry.get("member"),
                               suffixes=(".mdb", ".accdb"))

        with tempfile.TemporaryDirectory() as tmpdir:
            mdb_path = Path(tmpdir) / "extracted.mdb"
            with zf.open(mdb_name) as src, open(mdb_path, "wb") as dst:
                dst.write(src.read())

            conn_str = (r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                        f"DBQ={mdb_path};")
            mdb_conn = pyodbc.connect(conn_str, autocommit=True)
            try:
                cur = mdb_conn.cursor()
                all_tables = [r.table_name for r in cur.tables(tableType='TABLE')]
                wanted = entry.get("mdb_tables") or [
                    t for t in all_tables
                    if not t.lower().startswith(('msys', 'eadmspub'))]
                for tname in wanted:
                    if tname not in all_tables:
                        print(f"      SKIP {tname}: not found in mdb "
                              f"(has: {all_tables})")
                        continue
                    tbl = bulk.table_name(entry["table"].rsplit("_", 1)[0], tname)
                    try:
                        sub_cur = mdb_conn.cursor()
                        sub_cur.execute(f"SELECT * FROM [{tname}]")
                        cols = [d[0] for d in sub_cur.description]
                        rows = [list(r) for r in sub_cur.fetchmany(max_rows + 1)]
                        sub_cur.close()
                        if len(rows) > max_rows:
                            raise RuntimeError(
                                f"{tbl}: source has more than max_rows={max_rows:,} "
                                f"rows -- refusing to silently truncate. Pass a "
                                f"higher max_rows explicitly.")
                        if not rows:
                            continue
                        df = pd.DataFrame(rows, columns=cols).astype(str)
                        df = _stamp(df, sha, run_id, started)
                        n = _write(conn, df, tbl, sha=sha, run_id=run_id,
                                   source_url=entry["url"])
                        print(f"      {tbl}: {n:,} rows")
                        total += n
                    except Exception as e:
                        print(f"      FAILED {tbl}: {str(e)[:100]}")
            finally:
                mdb_conn.close()
    return total


def load_xml(conn, entry: dict, max_rows: int) -> int:
    """Parse a flat XML document into a table.

    2026-08-07 fix, INTL_UN_SC_CONSOLIDATED_SANCTIONS: the real data is XML,
    not JSON. Walks <INDIVIDUALS>/<INDIVIDUAL> and <ENTITIES>/<ENTITY>
    elements (the UN Security Council consolidated list's actual shape,
    confirmed against the live file), flattening each record one level deep
    (nested elements become TAG_SUBTAG columns; repeated tags -- e.g. an
    entity with several ENTITY_ALIAS blocks -- get their text values joined
    with '; ' so no data is silently dropped) and tagging each row
    RECORD_TYPE = INDIVIDUAL or ENTITY so both shapes can share one table.
    """
    def _elem_to_dict(elem: ET.Element) -> dict:
        d: dict[str, str] = {}
        for child in elem:
            tag = child.tag
            if list(child):
                for grandchild in child:
                    key = f"{tag}_{grandchild.tag}"
                    text = (grandchild.text or "").strip()
                    if not text:
                        continue
                    d[key] = f"{d[key]}; {text}" if key in d else text
            else:
                text = (child.text or "").strip()
                if not text:
                    continue
                d[tag] = f"{d[tag]}; {text}" if tag in d else text
        return d

    content = _get(entry["url"], timeout=300)
    sha, run_id, started = _provenance(content)
    root = ET.fromstring(content)

    records = []
    individuals = root.find("INDIVIDUALS")
    if individuals is not None:
        for ind in individuals.findall("INDIVIDUAL"):
            rec = _elem_to_dict(ind)
            rec["RECORD_TYPE"] = "INDIVIDUAL"
            records.append(rec)
    entities = root.find("ENTITIES")
    if entities is not None:
        for ent in entities.findall("ENTITY"):
            rec = _elem_to_dict(ent)
            rec["RECORD_TYPE"] = "ENTITY"
            records.append(rec)
    if not records:
        raise RuntimeError(
            f"{entry['table']}: no INDIVIDUAL/ENTITY records found in XML "
            f"(root tag was <{root.tag}>) -- source shape may have changed")

    df = pd.json_normalize(records)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


# Per-table record-path overrides for load_json_api, keyed by table name.
# Each value is the sequence of dict keys to walk from the parsed JSON
# payload down to the list of record dicts. Tables not listed here fall
# back to the auto-detect heuristic in load_json_api (checks "results" /
# "data" / "value" / ArcGIS-style "features", then gives up and flattens
# the whole payload as a single row).
JSON_API_RECORD_PATH = {
    # openFDA endpoints: {"meta": {...}, "results": [...]}
    "FED_FDA_ESTABLISHMENT_REG": ("results",),
    "FED_FDA_DEVICE_510K": ("results",),
    "FED_FDA_DEVICE_PMA": ("results",),
    "FED_FDA_DEVICE_ENFORCEMENT": ("results",),
    "FED_FDA_DEVICE_CLASSIFICATION": ("results",),
    "FED_FDA_CAERS_FOOD_EVENTS": ("results",),
    # ArcGIS FeatureServer/MapServer "?f=json" query responses:
    # {"features": [{"attributes": {...}, "geometry": {...}}, ...]}
    # NOTE: FED_USGS_WBD_HUC8 used to be here too, but the 2026-08-07 fix
    # moved it to format 'arcgis_paginated_json' (load_arcgis_paginated_json
    # below) since the unbounded single-request fetch 500s server-side --
    # it no longer goes through load_json_api at all.
    "FED_EPA_SUPERFUND_SITE_BOUNDARIES": ("features",),
    "FED_ATF_FFL_LOCATIONS": ("features",),
    # OpenFEMA convention: payload wraps records under a key matching the
    # dataset name, alongside a "metadata" key.
    "FED_FEMA_NFIP_COMMUNITY_STATUS_BOOK": ("NfipCommunityStatusBook",),
    # NSF Award Search API: {"response": {"award": [...]}}
    "FED_NSF_AWARDS": ("response", "award"),
    # OSF API v2 is JSON:API shaped: {"data": [...], "links": {...}}
    "XC_OSF_REGISTRATIONS": ("data",),
    # FED_USASPENDING_TAS_FILTER_TREE (nested agency->account->TAS tree)
    # deliberately has no entry here -- see its manifest description. It
    # falls through to the heuristic below and, if that still doesn't
    # produce a usable table, fails loudly rather than silently writing
    # garbage; a real fix needs its own dedicated loader later.
    # (INTL_UN_SC_CONSOLIDATED_SANCTIONS used to be listed here too, marked
    # deliberately absent because it redirected to XML -- 2026-08-07 fix
    # replaced that manifest entry with the real xml-format one, see
    # load_xml above, so it no longer touches load_json_api either.)
}


def _flatten_object_columns(df: pd.DataFrame) -> pd.DataFrame:
    """json.dumps() any column still holding list/dict values after
    pd.json_normalize (2026-08-07 fix, XC_OSF_REGISTRATIONS: nested arrays
    that json_normalize doesn't fully flatten land as Python list/dict
    objects in an object-dtype column, which Snowflake's write_pandas
    chokes on). Applied generally in load_json_api (and the ArcGIS
    paginated loader below), not just for the one entry that surfaced it,
    since any json_api source could hit the same shape. Columns that never
    held non-scalar values pass through untouched.
    """
    for col in df.columns:
        if df[col].dtype == object:
            if df[col].apply(lambda v: isinstance(v, (list, dict))).any():
                df[col] = df[col].apply(
                    lambda v: json.dumps(v) if isinstance(v, (list, dict)) else v)
    return df


def load_json_api(conn, entry: dict, max_rows: int) -> int:
    """Fetch a JSON API endpoint and flatten it into a table.

    Single GET per entry -- no built-in pagination. Several sources in this
    manifest are naturally paginated (skip/limit, resultOffset, page[number]);
    this loader deliberately stays a one-shot fetch-and-flatten, matching the
    other loaders' shape. A follow-up paginating loader can replace this one
    per-table later if a fuller pull is wanted.
    """
    content = _get(entry["url"], timeout=300)
    sha, run_id, started = _provenance(content)
    payload = json.loads(content)

    records = None
    path = JSON_API_RECORD_PATH.get(entry["table"])
    if path:
        node = payload
        for key in path:
            node = node[key]
        records = node
    elif isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict):
        for key in ("results", "data", "value"):
            if isinstance(payload.get(key), list):
                records = payload[key]
                break
        if records is None and isinstance(payload.get("features"), list):
            records = [f.get("attributes", f) for f in payload["features"]]
    if records is None:
        records = [payload]  # unrecognized shape -- flatten the whole payload as one row

    df = pd.json_normalize(records)
    df = _flatten_object_columns(df)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_arcgis_paginated_json(conn, entry: dict, max_rows: int) -> int:
    """Page through an ArcGIS FeatureServer/MapServer query endpoint.

    2026-08-07 fix, FED_USGS_WBD_HUC8: the plain load_json_api loader does
    one unbounded GET, which reliably 500s server-side on this service when
    geometry is included and/or the result set is unbounded. Pages
    resultOffset by page_size (default 2000, matching the service's
    advertised maxRecordCount) until a page comes back with fewer than
    page_size features. entry["url"] is expected to already include
    returnGeometry=false (attribute-only) -- this loader just adds paging on
    top of whatever query string is already there.
    """
    page_size = entry.get("page_size", 2000)
    all_records: list[dict] = []
    contents: list[bytes] = []
    offset = 0
    while True:
        sep = '&' if '?' in entry["url"] else '?'
        page_url = f"{entry['url']}{sep}resultOffset={offset}&resultRecordCount={page_size}"
        content = _get(page_url, timeout=300)
        contents.append(content)
        payload = json.loads(content)
        features = payload.get("features", [])
        all_records.extend(f.get("attributes", f) for f in features)
        if len(features) < page_size:
            break
        offset += page_size
        if offset > max_rows:
            raise RuntimeError(
                f"{entry['table']}: paged past max_rows={max_rows:,} without "
                f"the source running out -- refusing to keep paging unbounded.")

    sha, run_id, started = _provenance(b"".join(contents))
    df = pd.json_normalize(all_records)
    df = _flatten_object_columns(df)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


FORMAT_LOADERS = {
    "csv": load_csv,
    "zip_csv": load_zip_csv,
    "zip_multi": load_zip_multi,
    "zip_xlsx": load_zip_xlsx,
    "xlsx": load_xlsx,
    "bz2_csv": load_bz2_csv,
    "json_api": load_json_api,
    "arcgis_paginated_json": load_arcgis_paginated_json,  # 2026-08-07 fix
    "xml": load_xml,  # 2026-08-07 fix
    "mdb": load_mdb,  # 2026-08-07 fix
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Batch loader for the 2026-08-07 recon sweep")
    ap.add_argument("--run", action="store_true", help="Actually load (default: preview)")
    ap.add_argument("--group", type=str, default=None, help="Only load a specific group")
    ap.add_argument("--max-rows", type=int, default=5_000_000, help="Row cap per dataset")
    args = ap.parse_args()

    entries = MANIFEST
    if args.group:
        entries = [e for e in entries if e["group"] == args.group]
        if not entries:
            print(f"No entries for group '{args.group}'")
            groups = sorted(set(e["group"] for e in MANIFEST))
            print(f"Available groups: {', '.join(groups)}")
            return 1

    conn = snow.connect()
    loaded = bulk.get_loaded_tables(conn)
    print(f"Already loaded: {len(loaded)} tables in LANDING\n")

    to_load = []
    seen_this_run = set()
    seen_source = set()
    for entry in entries:
        # (url, sheet) fingerprints the actual source being fetched. Two
        # entries can share a URL for a legitimate reason (EIA-860's zip
        # bundles Plant/Utility/Generator as separate sheets/members of the
        # same download) so sheet is part of the key -- only entries that
        # would fetch and load the exact same content under a different
        # table name get caught here (e.g. FED_ED_SCORECARD_INSTITUTION vs
        # FED_ED_COLLEGE_SCORECARD_INSTITUTION, same zip, no sheet).
        source_key = (entry["url"], entry.get("sheet"))
        if entry["table"] in loaded:
            print(f"  SKIP {entry['table']} (exists)")
        elif entry["table"] in seen_this_run:
            # Source manifest has a few tables verified twice (two independent
            # entries pointing at the same table) -- only queue it once per run.
            print(f"  SKIP {entry['table']} (duplicate manifest row, already queued this run)")
        elif source_key in seen_source:
            print(f"  SKIP {entry['table']} (duplicate source -- same URL/sheet as an already-queued table)")
        else:
            seen_this_run.add(entry["table"])
            seen_source.add(source_key)
            to_load.append(entry)

    print(f"\n{'='*60}")
    print(f"{len(to_load)} datasets to load")
    print(f"{'='*60}")

    if not args.run:
        print("\n(preview only -- add --run to execute)\n")
        for i, e in enumerate(to_load, 1):
            print(f"  {i:2d}. [{e['group']:25s}] {e['table']:45s}")
            print(f"      {e['description']}")
            print(f"      {e['url'][:90]}")
            print()
        return 0

    # Execute loads sequentially (many are large ZIPs)
    results = []
    for i, entry in enumerate(to_load, 1):
        print(f"\n[{i}/{len(to_load)}] {entry['table']}")
        print(f"  {entry['description']}")
        loader = FORMAT_LOADERS.get(entry["format"])
        if not loader:
            print(f"  SKIP: no loader for format '{entry['format']}'")
            results.append({"name": entry["table"], "error": f"no loader for {entry['format']}"})
            continue
        try:
            # 2026-08-07 fix: entry["max_rows"] lets one source (e.g.
            # INTL_ELECTIONS_CANADA_CONTRIBUTIONS, which genuinely has more
            # rows than the global default) override the cap without
            # touching args.max_rows for everything else.
            n = loader(conn, entry, entry.get("max_rows", args.max_rows))
            print(f"  -> {n:,} rows loaded")
            results.append({"name": entry["table"], "rows": n})
        except Exception as e:
            msg = str(e)[:200]
            print(f"  FAILED: {msg}")
            if entry.get("fallback_url"):
                print(f"  Check: {entry['fallback_url']}")
            results.append({"name": entry["table"], "error": msg})

    # Summary
    ok = sum(1 for r in results if "rows" in r and r["rows"] > 0)
    total_rows = sum(r.get("rows", 0) for r in results)
    failed = [r for r in results if "error" in r]

    print(f"\n{'='*60}")
    print(f"DONE: {ok}/{len(to_load)} loaded, {total_rows:,} total rows")
    if failed:
        print(f"\nFailed ({len(failed)}):")
        for r in failed:
            print(f"  - {r['name']}: {r['error'][:80]}")
    print(f"{'='*60}")

    conn.close()
    # Non-zero exit when anything failed (same convention as the template --
    # main() should never silently return 0 while hiding failures).
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
