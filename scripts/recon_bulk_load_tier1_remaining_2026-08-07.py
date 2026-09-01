"""Batch loader for the 2026-08-07 Tier-1 REMAINING sources sweep.

Follows the exact structure/conventions of scripts/recon_bulk_load_2026-08-07.py
(same _provenance/_stamp/_write helpers, same FORMAT_LOADERS pattern, same
--run/--group/--max-rows CLI, same already-loaded skip check, same per-item
try/except with a clean summary). That file is the template and is NOT
modified by this one.

Targets a verified 120-entry recon list (spanning FDA/CMS/EPA/USGS/IRS/SEC/
FINRA/DOL-EBSA/DOL-OFLC/USSC/ICE-deportation-data/HUD/DOT/PHMSA/FERC/EIA/FCC/
USAC/CFPB/FEMA/ORCID/OpenAlex/PubMed/PMC/Crossref/NIH/USASpending/arXiv/OSTI/
GLEIF/France-Sirene/Japan-NTA/Brazil-Receita-Federal and more). One census row
("openFDA Device 510(k) Clearances API & PMA (Premarket Approval) API") bundled
two distinct URLs/tables into a single line -- that row was split into two real
manifest entries (FED_FDA_DEVICE_510K, FED_FDA_DEVICE_PMA) since a single entry
can only carry one url/format, so this file's MANIFEST has 121 rows for the
120 verified datasets. Several tables appear more than once in the source list
(the census verified them independently more than once, or two different
census rows resolve to the identical underlying file) -- FED_FDA_GUDID_FULL_RELEASE,
FED_CMS_PECOS_PROVIDER_ENROLLMENT, FED_IRS_FATCA_FFI_LIST, XC_ICIJ_OFFSHORE_LEAKS,
FED_USSC_INDIVIDUAL_OFFENDER_DATAFILES, FED_ICE_DETENTIONS_DDP, plus several more
that share a URL under a different table name (e.g. FED_CMS_HIOS_PLAN_ATTRIBUTES
vs FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF). Nothing was dropped from the source
list -- every row is kept, and the existing dedup logic in main() (duplicate
table name -> skip, duplicate (url, sheet) source -> skip, already-loaded table
-> skip) handles all of these cleanly at run time, exactly like the template.

FORMAT NOTES (2026-08-07):
  Reused as-is from the template: csv, zip_csv, zip_multi, zip_xlsx, xlsx,
  bz2_csv, json_api, arcgis_paginated_json, xml, mdb.
  Three new, low-risk loaders were added below, each a close sibling of an
  existing one:
    - csv_gz    (gzip.decompress + read_csv -- same shape as load_bz2_csv)
    - parquet   (pd.read_parquet -- same shape as load_csv, needs pyarrow)
    - zip_sqlite (extract to temp file + sqlite3 stdlib -- same shape as
                  load_mdb, but no external ODBC driver dependency)
  Every other unsupported format in this batch (pdf, rdb, fixed-width-ish
  government flat files behind a per-state API, web-form report builders,
  POST-only mapping/search APIs, async job-based bulk-download APIs, OAI-PMH
  harvesting, zip-of-DBF, zip-of-shapefile, zip-of-many-small-XML-docs,
  multi-GB manifest-driven multi-file snapshots) is left as an unregistered
  format string (pdf, rdb, xml_generic, web_form_export, json_api_post,
  post_zip_multi, csrf_post_zip, async_job_api, oai_pmh_xml, zip_dbf,
  zip_shapefile, zip_multi_xml, tar_gz, jsonl_gz, xml_gz) -- these hit the
  existing "no loader for format" skip path at run time, same discipline the
  template already uses for pdf/fixed_width/zip_xml. None of these were
  forced into a fragile one-off loader.

  load_csv and load_zip_csv also grew one small, generic, opt-in extra: an
  entry can set "header": None (matching pandas' own header= kwarg) for
  sources confirmed to have no header row; when it does, and no explicit
  "names" list is given, columns are renamed COL_0, COL_1, ... after the
  read so a bare numeric column name never reaches Snowflake table creation
  unquoted. Entries that don't set "header" behave exactly as before
  (header="infer", pandas' own default).

SIZE CAP -- unchanged from the template, per instruction: MAX_DOWNLOAD_BYTES
stays 500MB and the default --max-rows stays 5,000,000. Many entries in this
batch are individually flagged as multi-GB (openFDA bulk partitions, PubMed,
OpenAlex, ORCID, ICE detention data, DOT NAD, CFPB complaints, HMDA nationwide,
Companies House PSC, France Sirene, etc.) -- these will hit MAX_DOWNLOAD_BYTES
during _get() and fail with a clear "needs a dedicated streaming loader"
message rather than attempt an in-memory pull. That is the correct, safe
behavior this run is meant to demonstrate, not a bug to fix here.

    python scripts/recon_bulk_load_tier1_remaining_2026-08-07.py              # preview
    python scripts/recon_bulk_load_tier1_remaining_2026-08-07.py --run        # load all
    python scripts/recon_bulk_load_tier1_remaining_2026-08-07.py --run --group fda_openfda
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
# MANIFEST -- 121 rows for the 120 verified 2026-08-07 "tier1 remaining" datasets
# ---------------------------------------------------------------------------

MANIFEST = [
    # --- fda_gudid ---
    {
        "group": 'fda_gudid',
        "table": 'FED_FDA_GUDID_FULL_RELEASE',
        "url": 'https://accessgudid.nlm.nih.gov/release_files/download/gudid_full_release_20260803.zip',
        "format": 'zip_multi',
        "description": "FDA/NLM Global UDI Database full release zip -- confirmed live via HEAD, 541,460,684 bytes (~516MB), no login. Exceeds the 500MB download cap so will fail cleanly at _get() time, not be parsed. Likely a set of pipe-delimited relational .TXT files (device/identifiers/GMDN/contacts), not one flat CSV -- zip_multi is the closer structural fit than zip_csv even though it can't be confirmed without exceeding the size cap. Verified twice independently in the source census under two dataset names pointed at this same URL -- second row kept in this manifest too, will skip as a duplicate manifest row at run time.",
    },
    # --- cms_marketplace ---
    {
        "group": 'cms_marketplace',
        "table": 'FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF',
        "url": 'https://download.cms.gov/marketplace-puf/2026/plan-attributes-puf.zip',
        "format": 'zip_csv',
        "description": "CMS Health Insurance Marketplace Plan Attributes PUF, plan year 2026 (StandardComponentId/IssuerId/HIOSProductId + ~146 more columns). Confirmed real: HEAD 200 OK, application/zip, 1,001,042 bytes (~1.0MB) zipped / ~32MB uncompressed CSV. Same underlying file/URL as FED_CMS_HIOS_PLAN_ATTRIBUTES later in this manifest -- the later row will skip as a duplicate source at run time.",
    },
    # --- cms_open_payments ---
    {
        "group": 'cms_open_payments',
        "table": 'FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT',
        "url": 'https://download.cms.gov/openpayments/PHPRFL_P06302026_06032026/OP_CVRD_RCPNT_PRFL_SPLMTL_P06302026_06032026.csv',
        "format": 'csv',
        "description": "CMS Open Payments Covered Recipient Profile Supplement -- one row per covered recipient (physician/NPP) with Covered_Recipient_Profile_ID, NPI, name/address, specialty/taxonomy, license state. Confirmed via ranged GET: HTTP 206, Content-Range total 404,839,303 bytes (~386MB), real header row and sample rows. Under the 500MB cap but large -- will be slow. NOTE: URL is period-stamped (refreshes on CMS's release cycle) -- re-derive from openpaymentsdata.cms.gov/data.json rather than hardcoding long-term.",
    },
    # --- cms_pecos ---
    {
        "group": 'cms_pecos',
        "table": 'FED_CMS_PECOS_PROVIDER_ENROLLMENT',
        "url": 'https://data.cms.gov/sites/default/files/2026-07/9c89bdde-66b6-4fb9-8c2f-a96cbb3859ba/PPEF_Enrollment_Extract_2026.07.17.csv',
        "format": 'csv',
        "description": "CMS PECOS Public Provider Enrollment extract -- NPI, PECOS_ASCT_CNTL_ID (PAC ID), ENRLMT_ID, provider type, state, name fields. Confirmed via ranged GET: HTTP 206, Content-Range total 320,536,185 bytes (~306MB), real header/sample rows. NOTE: URL embeds a date-stamped path + UUID that changes on each CMS refresh -- re-derive from data.cms.gov/data.json rather than hardcoding long-term. Verified twice independently in the source census under this same table/URL -- second row kept, will skip as a duplicate manifest row at run time.",
    },
    # --- nber_npi_upin ---
    {
        "group": 'nber_npi_upin',
        "table": 'FED_CMS_NPI_UPIN_CROSSWALK',
        "url": 'https://data.nber.org/npi/2017/npi2upinxw.csv',
        "format": 'csv',
        "description": "CMS-built NPI-to-UPIN crosswalk, mirrored by NBER as a plain static file. Confirmed via full GET: HTTP 200, 34,692,914 bytes (~33.1MB), 850,200 rows, real header (npi, seq, upin, othpidty, ...). CAVEAT: static December 2017 snapshot -- a one-time historical crosswalk, will not reflect anything assigned/retired after 2017.",
    },
    # --- fda_gudid (duplicate manifest row -- same table/url as above) ---
    {
        "group": 'fda_gudid',
        "table": 'FED_FDA_GUDID_FULL_RELEASE',
        "url": 'https://accessgudid.nlm.nih.gov/release_files/download/gudid_full_release_20260803.zip',
        "format": 'zip_multi',
        "description": "Same underlying file as the FED_FDA_GUDID_FULL_RELEASE row above (census verified it twice, once via the /download subpage, once via the bare domain). Kept as a separate manifest row per source data; the dedup logic in main() will skip this one as a duplicate manifest row at run time.",
    },
    # --- fda_unii ---
    {
        "group": 'fda_unii',
        "table": 'FED_FDA_UNII_GSRS_SUBSTANCES',
        "url": 'https://precision.fda.gov/uniisearch/archive/latest/UNII_Data.zip',
        "format": 'zip_csv',
        "sep": '\t',
        "description": "FDA Global Substance Registration System (GSRS) full UNII list export. Confirmed by full download: HTTP 200, 16,947,343 bytes (~16.2MB) zip, containing UNII_Records_*.txt (~38.1MB uncompressed, TAB-delimited, real header UNII/Display Name/RN/EC/NCIT/RXCUI/.../SUBSTANCE_TYPE/UUID) plus a small Legacy_UNIIs.txt and a README. zip_csv's largest-file heuristic correctly grabs the records file; needs sep='\\t', not comma.",
    },
    # --- fda_openfda ---
    {
        "group": 'fda_openfda',
        "table": 'FED_FDA_MAUDE_DEVICE_EVENTS',
        "url": 'https://api.fda.gov/device/event.json',
        "format": 'json_api',
        "description": "openFDA MAUDE device adverse-event reports API. Confirmed live: HTTP 200, real JSON, meta.results.total=2,536,816 records, no key required for low-volume use. Not currently in this repo's manifest under this table name. This one-shot loader pulls only the default page (openFDA's own bulk manifest lists ~18GB across 362 partition zips for the full corpus) -- a real full pull needs a dedicated partitioned loader, not this single-GET one.",
    },
    {
        "group": 'fda_openfda',
        "table": 'FED_FDA_FAERS_DRUG_EVENTS',
        "url": 'https://api.fda.gov/drug/event.json',
        "format": 'json_api',
        "description": "openFDA FAERS drug adverse-event reports API. Confirmed live: HTTP 200, real JSON, meta.results.total=2,069,269 records, no key required. This one-shot loader pulls only the default page (openFDA's bulk manifest lists ~113.5GB across 1,767 partitions for the full corpus, the single largest source in this whole batch) -- do not attempt a full pull with this loader.",
    },
    # --- fda_purple_book ---
    {
        "group": 'fda_purple_book',
        "table": 'FED_FDA_PURPLE_BOOK',
        "url": 'https://www.accessdata.fda.gov/drugsatfda_docs/PurpleBook/2026/purplebook-search-June-data-download.csv',
        "format": 'csv',
        "description": "FDA Purple Book of licensed biological products (BLA number, product name, applicant, licensure date, marketing status, exclusivity flags). Confirmed real and live, 200 OK, real CSV, no login. Monthly snapshot, ~457KB.",
    },
    # --- fda_dmf ---
    {
        "group": 'fda_dmf',
        "table": 'FED_FDA_DRUG_MASTER_FILES',
        "url": 'https://www.fda.gov/media/192069/download?attachment',
        "format": 'xlsx',
        "description": "FDA's quarterly List of Drug Master Files (DMF number, holder, subject, type, status). Confirmed real: 200 OK, real spreadsheetml content-type, ~3.85MB. NOTE: the numeric FDA media ID changes every quarter when a new file posts -- a real loader needs to re-resolve the link from the DMF listing page each run, not hardcode this ID long-term.",
    },
    # --- dea_schedules ---
    {
        "group": 'dea_schedules',
        "table": 'FED_DEA_CONTROLLED_SUBSTANCES_ACSCN',
        "url": 'https://www.deadiversion.usdoj.gov/schedules/orangebook/c_cs_alpha.pdf',
        "format": 'pdf',
        "description": "DEA Diversion Control's 'Orange Book' -- alphabetical listing of controlled substances by DEA number (ACSCN). Confirmed real and live, 200 OK, real PDF, ~421.8KB. Every list on the DEA schedules page is PDF-only, no CSV/Excel alternative exists. Format left unregistered (no loader) -- needs a PDF-table-extraction loader this batch deliberately does not build, same discipline as the template's own pdf entries.",
    },
    # --- epa_rcra ---
    {
        "group": 'epa_rcra',
        "table": 'FED_EPA_RCRAINFO',
        "url": 'https://echo.epa.gov/files/echodownloads/rcra_downloads.zip',
        "format": 'zip_multi',
        "description": "EPA RCRAInfo national hazardous waste handler database bulk export via ECHO. Confirmed real: 200 OK, zip contains six CSVs (RCRA_FACILITIES the handler universe, plus ENFORCEMENTS/EVALUATIONS/NAICS/VIOLATIONS/VIOSNC_HISTORY). zip is 119.06MB compressed; zip_multi's 5-largest-CSV cap means one of the six tables won't get pulled in a single pass.",
    },
    # --- usgs_wells ---
    {
        "group": 'usgs_wells',
        "table": 'FED_USGS_ORPHANED_OIL_GAS_WELLS',
        "url": 'https://www.sciencebase.gov/catalog/file/get/62ebd67bd34eacf539724c56?f=__disk__11%2Fe9%2F27%2F11e927c652d995f46129f282b400063b5d262369',
        "format": 'csv',
        "description": "USGS Documented Unplugged Orphaned Oil and Gas Well Dataset (117,672 orphaned wells across 27 states per USGS). Confirmed real: 200 OK, real CSV, no login, ~22.19MB. Covers orphaned wells only, not the full national universe of API-numbered wells (that's scattered across state oil & gas commission databases, not aggregated federally).",
    },
    # --- usgs_nwis ---
    {
        "group": 'usgs_nwis',
        "table": 'FED_USGS_NWIS_SITES',
        "url": 'https://waterservices.usgs.gov/nwis/site/?format=rdb&siteStatus=all&stateCd=RI',
        "format": 'rdb',
        "description": "USGS NWIS Site Service REST API, confirmed live and auth-free -- a Rhode Island test pull (this URL) returned real station rows (agency, site number, name, type, lat/long, HUC code). RDB is NOT plain CSV: '#'-prefixed comment lines, then a real header row, then a field-width-code row that must be skipped before data -- and the service is used state-by-state (a national pull needs a 50+ state loop, not one URL). Format left unregistered (no loader) rather than forcing a one-state-only parser to stand in for the real per-state-looping design this needs.",
    },
    # --- nrc ---
    {
        "group": 'nrc',
        "table": 'FED_USCG_NRC_INCIDENT_REPORTS',
        "url": 'https://nrc.uscg.mil/FOIAFiles/CYDECADE2020.zip',
        "format": 'zip_xlsx',
        "description": "National Response Center oil/chemical spill and incident reports (USCG), 2020-2024 decade bundle. Confirmed real: 66.95MB zip containing a single CY2020-2024.xlsx member (~69.1MB uncompressed, confirmed via zip central-directory read). Single-year files (e.g. CY26.xlsx, ~7.76MB) also exist at the same path pattern for more current coverage. NOTE: nrc.uscg.mil DNS was flaky on first attempt in the source check -- a production loader should retry on connection failure.",
    },
    # --- wqp ---
    {
        "group": 'wqp',
        "table": 'FED_WQP_MONITORING_STATIONS',
        "url": 'https://www.waterqualitydata.us/data/Station/search?mimeType=csv&statecode=US%3A44',
        "format": 'csv',
        "description": "Water Quality Portal aggregated monitoring-station metadata (Rhode Island test slice, statecode=US:44). Confirmed real and auth-free: 5,818 real station rows, 1.62MB, real Total-Site-Count header. SCOPE CAVEAT: this is the Station (site inventory) endpoint only -- the much larger Result (measurement) dataset behind the same portal is likely multi-GB nationally and not covered here. Full national coverage of even just Station needs a per-state loop (~100-300MB combined, rough extrapolation), not one URL.",
    },
    # --- usgs_gnis ---
    {
        "group": 'usgs_gnis',
        "table": 'FED_USGS_GNIS_ALL_NAMES',
        "url": 'https://prd-tnm.s3.amazonaws.com/StagedProducts/GeographicNames/Topical/AllNames_National_Text.zip',
        "format": 'zip_csv',
        "sep": '|',
        "description": "USGS Geographic Names Information System (GNIS) full national names extract (feature name, type, state, county, coordinates, elevation). Confirmed real: 200 OK, S3-hosted zip, ~15.55MB, no login. Per USGS's own GNIS documentation the text file inside is pipe-delimited, not comma -- needs sep='|'.",
    },
    # --- itis ---
    {
        "group": 'itis',
        "table": 'FED_ITIS_TAXONOMY',
        "url": 'https://www.itis.gov/downloads/itisSqlite.zip',
        "format": 'zip_sqlite',
        "description": "Integrated Taxonomic Information System full taxonomic database dump (plants, animals, fungi, microbes -- taxonomic serial numbers, names, ranks, hierarchy). Confirmed real: 200 OK, ~223.17MB zip. No plain CSV/flat-file export exists, only full SQL dumps (MSSQL/MySQL/PostgreSQL/SQLite) -- SQLite is the only one loadable without a real DB server, so this uses the new load_zip_sqlite loader added in this file (extracts the .sqlite member to a temp file via Python's stdlib sqlite3, loads every non-internal table).",
    },
    # --- epa_icis ---
    {
        "group": 'epa_icis',
        "table": 'FED_EPA_ICIS_AIR',
        "url": 'https://echo.epa.gov/files/echodownloads/ICIS-AIR_downloads.zip',
        "format": 'zip_multi',
        "description": "EPA ICIS-Air (Clean Air Act stationary sources) bulk download via ECHO. Confirmed real: 68.65MB zip, 10 CSVs verified via central-directory read (FACILITIES, PROGRAMS, PROGRAM_SUBPARTS, POLLUTANTS, FCES_PCES, STACK_TESTS, TITLEV_CERTS, FORMAL_ACTIONS, INFORMAL_ACTIONS, VIOLATION_HISTORY) -- zip_multi's 5-largest-CSV cap means five of the ten tables won't get pulled in a single pass. A much larger companion ICIS-NPDES file (~348MB zip) exists at the same path if wanted separately.",
    },
    # --- fdic_sod ---
    {
        "group": 'fdic_sod',
        "table": 'FED_FDIC_SOD_BRANCH_DEPOSITS',
        "url": 'https://api.fdic.gov/banks/sod?filters=YEAR:2025&limit=10000',
        "format": 'json_api',
        "description": "FDIC Summary of Deposits (SOD) branch-level deposit data (cert number, branch name/address, deposits, county/state) via FDIC's own public API, no auth required. Confirmed live: a filters=YEAR:2025 test query returned 76,120 branch records. This URL is a narrow single-year, capped-limit slice -- a full multi-decade pull needs a real offset-paginated loader, not this one-shot GET.",
    },
    # --- sba_ppp ---
    {
        "group": 'sba_ppp',
        "table": 'FED_SBA_PPP_LOANS_150K_PLUS',
        "url": 'https://data.sba.gov/sites/default/files/distribution/SBA-OCA-2022-07-001/public_150k_plus_240930.csv',
        "format": 'csv',
        "description": "SBA PPP FOIA loan-level data for loans of $150,000+ (borrower name/address, lender, loan amount, jobs reported, NAICS code, forgiveness amount). Confirmed live: real CSV, 313,067,386 bytes (~313MB). One of 13 sibling files at the same distribution (a 12-part 'under $150k' series runs ~400-450MB each, ~5-6GB aggregate) -- each part needs its own manifest row, not pulled into this one.",
    },
    # --- irs ---
    {
        "group": 'irs',
        "table": 'FED_IRS_FATCA_FFI_LIST',
        "url": 'https://apps.irs.gov/app/fatcaFfiList/data/FFIListFull.csv',
        "format": 'csv',
        "description": "IRS FATCA FFI list with GIIN numbers, full national list. Confirmed real, live, plain CSV (octet-stream), no login. ~38.85MB, 516,299 rows. LIKELY ALREADY LOADED: this exact table + URL is already in scripts/recon_bulk_load_2026-08-07.py's manifest -- verify before assuming this run adds it. Verified twice independently in the source census under this same table/URL -- the later duplicate row in this manifest will skip at run time.",
    },
    # --- cfpb_hmda ---
    {
        "group": 'cfpb_hmda',
        "table": 'FED_CFPB_HMDA_LAR',
        "url": 'https://ffiec.cfpb.gov/v2/data-browser-api/view/csv?years=2023&states=DC',
        "format": 'csv',
        "description": "CFPB/FFIEC HMDA Data Browser bulk CSV export API. Confirmed real and auth-free: years=2023&states=DC (this URL) returns a real 6.75MB CSV via a 301 to an S3-hosted file; a CA equivalent returned 367.8MB for one year. Requesting nationwide with no state filter 400s -- a full pull needs a loop over all states x years (2018-present), not one URL. This entry is deliberately the smallest single state/year slice so a single GET stays well under the caps.",
    },
    # --- sec_iapd ---
    {
        "group": 'sec_iapd',
        "table": 'FED_SEC_FORM_ADV_FILINGS',
        "url": 'https://www.sec.gov/files/adv-filing-data-20111105-20241231-part1.zip',
        "format": 'zip_csv',
        "description": "SEC's official Form ADV Part 1 + ADV-W historical filing-data CSV bulk export (firm CRD/SEC number, filing dates, registration status). Confirmed real: needs SEC's required descriptive User-Agent header (this repo's USER_AGENT already sets one) or it rate-limits/blocks. This part is 701,619,239 bytes (~702MB) -- exceeds the 500MB cap and will fail cleanly at _get() time; a companion part2 (~429MB) and a 2000-2011 file (~250MB) are each individually under the cap if wanted as separate rows.",
    },
    # --- sec_edgar ---
    {
        "group": 'sec_edgar',
        "table": 'FED_SEC_INVESTMENT_COMPANY_SERIES_CLASS',
        "url": 'https://www.sec.gov/files/investment/data/other/investment-company-series-class-information/investment-company-series-class-2026.csv',
        "format": 'csv',
        "description": "SEC's official Series ID / Class ID reference file (Series ID = 'S'+9 digits, Class ID = 'C'+9 digits, tied to fund CIK). Confirmed live with SEC's required descriptive User-Agent header: 200 OK, real octet-stream CSV, 8,051,163 bytes (~8.05MB).",
    },
    # --- msrb ---
    {
        "group": 'msrb',
        "table": 'FED_MSRB_REGISTRANTS',
        "url": 'https://www.msrb.org/exportregistrant?page&_format=csv',
        "format": 'csv',
        "description": "MSRB's live CSV export of all registered brokers/dealers/municipal securities dealers/municipal advisors. Confirmed live: real CSV, Content-Disposition filename dated to the day fetched (confirms a live daily-generated export, not stale). ~51KB.",
    },
    # --- dtcc ---
    {
        "group": 'dtcc',
        "table": 'FED_DTCC_DTC_PARTICIPANTS',
        "url": 'https://www.dtcc.com/-/media/Files/Downloads/client-center/DTC/DTC-Participant-in-Alphabetical-Listing.xlsx',
        "format": 'xlsx',
        "description": "DTC Participant Directory (participant name + participant number, alphabetical listing). Confirmed live and auth-free, ~46.77KB. Sibling files at the same path (numerical listing, pledgees, settling banks, DRS report) also confirmed present.",
    },
    # --- sec_edgar (CIK lookup) ---
    {
        "group": 'sec_edgar',
        "table": 'FED_SEC_EDGAR_CIK_LOOKUP',
        "url": 'https://www.sec.gov/Archives/edgar/cik-lookup-data.txt',
        "format": 'csv',
        "sep": ':',
        "description": "SEC's full CIK-to-entity-name lookup covering every CIK ever assigned (companies, individuals, filing agents, foreign governments). Confirmed live with SEC's required descriptive User-Agent: 200 OK, real plain-text colon-delimited content ('NAME:CIK:' pairs per line, e.g. 'APPLE INC:0000320193:'), ~39.9MB. Not real comma-CSV -- uses sep=':' so each line splits into name/CIK columns instead of one blob column. A narrower ticker-only JSON alternative (company_tickers.json, ~796KB) also exists if a smaller subset is preferred.",
    },
    # --- occ ---
    {
        "group": 'occ',
        "table": 'FED_OCC_CLEARING_MEMBERS',
        "url": 'https://www.theocc.com/api/memberdirectory/xls',
        "format": 'xlsx',
        "description": "OCC's live clearing-member directory export (~115 clearing members: broker-dealers, FCMs, non-US securities firms). Site runs Akamai bot protection that 403s a bare request without browser-like headers/Referer -- confirmed real and working with those headers set. ~15.7KB. A CSV variant exists at /api/memberdirectory/csv if preferred.",
    },
    # --- uk_companieshouse ---
    {
        "group": 'uk_companieshouse',
        "table": 'INTL_UK_COMPANIESHOUSE_PSC',
        "url": 'https://download.companieshouse.gov.uk/persons-with-significant-control-snapshot-2026-08-07.zip',
        "format": 'zip_multi',
        "description": "UK Companies House full PSC (beneficial ownership) daily snapshot. Confirmed live via HEAD, 2,189,753,727 bytes (~2.19GB) -- exceeds the 500MB cap by a wide margin, will fail cleanly at _get() time. Actually newline-delimited JSON inside the zip, not CSV (source census mislabeled this row's format as 'json_api'; corrected here to zip_multi since that's the closer registered shape and the size cap makes the distinction moot -- it never gets far enough to parse either way). A 32-part chunked split (~72MB/part) exists at the same page and is the realistic path to actually load this later.",
    },
    # --- icij ---
    {
        "group": 'icij',
        "table": 'XC_ICIJ_OFFSHORE_LEAKS',
        "url": 'https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip',
        "format": 'zip_multi',
        "description": "ICIJ's official combined Offshore Leaks CSV package (entities, officers, addresses, intermediaries, relationships across Panama/Paradise/Pandora/Bahamas/Offshore Leaks). Confirmed live and auth-free, 71,934,796 bytes (~68.6MB). Open Database License / CC BY-SA -- cite ICIJ when used.",
    },
    # --- cms_pecos (duplicate manifest row) ---
    {
        "group": 'cms_pecos',
        "table": 'FED_CMS_PECOS_PROVIDER_ENROLLMENT',
        "url": 'https://data.cms.gov/sites/default/files/2026-07/9c89bdde-66b6-4fb9-8c2f-a96cbb3859ba/PPEF_Enrollment_Extract_2026.07.17.csv',
        "format": 'csv',
        "description": "Same table/URL as the FED_CMS_PECOS_PROVIDER_ENROLLMENT row earlier in this manifest. Kept as a separate row per source data; will skip as a duplicate manifest row at run time.",
    },
    # --- openfigi ---
    {
        "group": 'openfigi',
        "table": 'XC_OPENFIGI_MAPPING',
        "url": 'https://api.openfigi.com/v3/mapping',
        "format": 'json_api_post',
        "description": "OpenFIGI's free mapping API -- POST a batch of identifiers (ISIN/CUSIP/ticker/SEDOL) and get back FIGI + issuer + exchange + security type. Confirmed free and open, no key required for low-volume use (25 req/min unauthenticated). Not a bulk file -- there's no 'download everything' endpoint; using it means feeding it identifiers Ripple already has, not a one-shot ingest. Format left unregistered (no loader) -- a POST-batch mapping shape doesn't fit this script's GET-and-parse loaders.",
    },
    # --- sec_edgar (submissions bulk) ---
    {
        "group": 'sec_edgar',
        "table": 'FED_SEC_EDGAR_SUBMISSIONS_BULK',
        "url": 'https://www.sec.gov/Archives/edgar/daily-index/bulkdata/submissions.zip',
        "format": 'zip_multi',
        "description": "SEC EDGAR's own daily full bulk export: one JSON file per company (CIK-keyed) inside a zip, each with filings.recent.fileNumber (the real SEC/Commission File Number), plus CIK/EIN/LEI/name/address/SIC/formerNames. Confirmed live with SEC's required descriptive User-Agent (prior 403s in earlier sessions were a UA problem, not a dead endpoint). Confirmed via HEAD: 1,556,242,184 bytes (~1.45GB) -- exceeds the 500MB cap, will fail cleanly at _get() time; a real loader needs streaming, and the zip holds thousands of individual JSON files, not one CSV/table.",
    },
    # --- irs_eobmf ---
    {
        "group": 'irs_eobmf',
        "table": 'FED_IRS_EO_BMF',
        "url": 'https://www.irs.gov/pub/irs-soi/eo1.csv',
        "format": 'csv',
        "description": "IRS Exempt Organizations Business Master File, region 1 of 4 (eo1.csv; the full national extract is eo1-eo4.csv unioned, ~1.98M orgs total). Confirmed live and real, text/csv, 200 OK. eo1.csv alone confirmed 49,109,162 bytes (~46.8MB) via Range request; eo2-4 exist at the same path pattern and would need their own rows to get the other 3 regions.",
    },
    # --- companies_house (snapshot, correctly-labeled zip_multi) ---
    {
        "group": 'companies_house',
        "table": 'INTL_UK_COMPANIESHOUSE_PSC_SNAPSHOT',
        "url": 'https://download.companieshouse.gov.uk/persons-with-significant-control-snapshot-2026-08-07.zip',
        "format": 'zip_multi',
        "description": "Same underlying UK Companies House PSC daily snapshot as INTL_UK_COMPANIESHOUSE_PSC above, under a different table name in the source census (correctly labeled zip_multi here). Confirmed live via HEAD, 2,189,753,727 bytes (~2.19GB) -- exceeds the 500MB cap, will fail cleanly. Will skip as a duplicate source (same URL) at run time since the earlier row claims this URL first.",
    },
    # --- icij (entities variant, same URL) ---
    {
        "group": 'icij',
        "table": 'XC_ICIJ_OFFSHORELEAKS_ENTITIES',
        "url": 'https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip',
        "format": 'zip_multi',
        "description": "Same underlying ICIJ Offshore Leaks package as XC_ICIJ_OFFSHORE_LEAKS above, under a different table name. Will skip as a duplicate source (same URL) at run time.",
    },
    # --- opensanctions --- EXCLUDED 2026-08-07: CC BY-NC 4.0 (non-commercial only),
    # licensing decision deferred to Chris, not approved for this run. Entry removed
    # rather than left commented with a live URL, so a future --run can't load it by
    # accident. Re-add explicitly once the licensing question is actually resolved.
    # --- nlrb ---
    {
        "group": 'nlrb',
        "table": 'FED_NLRB_CASE_SEARCH_EXPORT',
        "url": 'https://www.nlrb.gov/advanced-search',
        "format": 'web_form_export',
        "description": "NLRB case-handling data (unfair labor practice and representation cases) via a real, working, no-login report-builder that emits CSV, capped at 100,000 records per export request. Confirmed genuine (real Drupal export module backing the page), but there's no single static bulk file URL -- building this out means replicating the report-builder's form parameters (case type/date range/columns), not a one-shot fetch. Format left unregistered (no loader).",
    },
    # --- cms_hios ---
    {
        "group": 'cms_hios',
        "table": 'FED_CMS_HIOS_PLAN_ATTRIBUTES',
        "url": 'https://download.cms.gov/marketplace-puf/2026/plan-attributes-puf.zip',
        "format": 'zip_csv',
        "description": "Same file as FED_CMS_MARKETPLACE_PLAN_ATTRIBUTES_PUF earlier in this manifest -- one row per plan with StandardComponentId/IssuerId/HIOSProductId/NetworkId/ServiceAreaId + 146 more columns, confirmed by actually opening the zip's Plan_Attributes_PUF.csv. Will skip as a duplicate source (same URL) at run time.",
    },
    # --- ebsa_form5500 ---
    {
        "group": 'ebsa_form5500',
        "table": 'FED_DOL_EBSA_FORM5500_SCHEDULE_SB',
        "url": 'https://askebsa.dol.gov/FOIA%20Files/2024/All/F_SCH_SB_2024_All.zip',
        "format": 'zip_csv',
        "description": "Form 5500 Schedule SB (single-employer defined-benefit actuarial certifications, carries the Enrolled Actuary number as a field), 2024 all-filers zip. Confirmed live and real: 7,090,660 bytes (~6.8MB), single-CSV zip, no auth. A much smaller companion Schedule MB (multiemployer) file (~302KB) exists at the same path pattern if that population is wanted too.",
    },
    # --- ofccp ---
    {
        "group": 'ofccp',
        "table": 'FED_DOL_OFCCP_CSAL',
        "url": 'https://www.dol.gov/sites/dolgov/files/OFCCP/scheduling/files/FY2025-CSAL-SupplyAndService-SchedulingList-Release1.xlsx',
        "format": 'xlsx',
        "description": "OFCCP Corporate Scheduling Announcement List (establishments selected for a compliance evaluation), FY2025 Supply & Service Release 1. Confirmed live and real via HEAD, 154,218 bytes (~151KB). A plain curl with a normal User-Agent works; this page 403s some fetchers, not a real auth wall.",
    },
    # --- ussc ---
    {
        "group": 'ussc',
        "table": 'FED_USSC_INDIVIDUAL_OFFENDER_DATAFILES',
        "url": 'https://www.ussc.gov/sites/default/files/zip/opafy25nid_csv.zip',
        "format": 'zip_csv',
        "description": "USSC Individual Offender Datafiles, FY2025 CSV zip (sentencing/demographic/offense fields, one row per offender). Confirmed live via HEAD: 21,314,665 bytes (~20.3MB). CSV and SAS/SPSS variants exist per fiscal year back to FY2002 -- loading the full FY2002-2025 series would run several hundred MB combined. Verified twice independently in the source census under this same table/URL -- the later duplicate row will skip at run time.",
    },
    # --- ussc (duplicate manifest row) ---
    {
        "group": 'ussc',
        "table": 'FED_USSC_INDIVIDUAL_OFFENDER_DATAFILES',
        "url": 'https://www.ussc.gov/sites/default/files/zip/opafy25nid_csv.zip',
        "format": 'zip_csv',
        "description": "Same table/URL as the FED_USSC_INDIVIDUAL_OFFENDER_DATAFILES row above. Will skip as a duplicate manifest row at run time.",
    },
    # --- oflc ---
    {
        "group": 'oflc',
        "table": 'FED_DOL_OFLC_LCA_DISCLOSURE',
        "url": 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/LCA_Disclosure_Data_FY2025_Q4.xlsx',
        "format": 'xlsx',
        "description": "OFLC LCA Program disclosure data (Form ETA-9035, H-1B/H-1B1/E-3), FY2025 Q4 cumulative -- the latest complete-fiscal-year file. Confirmed live via HEAD, 79,134,156 bytes (~75.5MB).",
    },
    {
        "group": 'oflc',
        "table": 'FED_DOL_OFLC_PERM_DISCLOSURE',
        "url": 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/PERM_Disclosure_Data_FY2025_Q4.xlsx',
        "format": 'xlsx',
        "description": "OFLC PERM Program disclosure data (Form ETA-9089), FY2025 Q4 cumulative. Confirmed live via HEAD, 87,007,731 bytes (~83.0MB). A revised-form 'New Form FY2024 Q4' variant also exists at the same page.",
    },
    {
        "group": 'oflc',
        "table": 'FED_DOL_OFLC_H2A_DISCLOSURE',
        "url": 'https://www.dol.gov/sites/dolgov/files/ETA/oflc/pdfs/H-2A_Disclosure_Data_FY2025_Q4.xlsx',
        "format": 'xlsx',
        "description": "OFLC H-2A Program disclosure data (Form ETA-9142A, agricultural workers), FY2025 Q4 cumulative. Confirmed live via HEAD, 80,636,352 bytes (~76.9MB). A separate H-2B file (Form ETA-9142B, non-agricultural, ~67.6MB) exists at the equivalent path and needs its own row (different schema -- H-2A includes housing/employment addenda).",
    },
    # --- deportation_data_project ---
    {
        "group": 'deportation_data_project',
        "table": 'FED_ICE_DETENTIONS_DDP',
        "url": 'https://ucla.box.com/shared/static/csnihndb826omzizlps90szm60q39jxd.zip',
        "format": 'zip_multi',
        "description": "ICE detention/detainer records bundle (2012-2023 raw releases from the Deportation Data Project / CILP v. ICE FOIA litigation) -- detainers, detention stays, and detention stints as separate raw files inside one zip. Confirmed real via a 1-byte Range GET: Content-Range total 2,604,829,726 bytes (~2.6GB) -- exceeds the 500MB cap, will fail cleanly. Same table already exists in scripts/recon_bulk_load_2026-08-07.py's manifest with the same streaming-needed caveat. Verified twice independently in the source census (once framed as 'detention stints/stays', once as 'detainers') under the same table/URL -- the later duplicate row will skip at run time.",
    },
    # --- deportation_data_project (duplicate manifest row) ---
    {
        "group": 'deportation_data_project',
        "table": 'FED_ICE_DETENTIONS_DDP',
        "url": 'https://ucla.box.com/shared/static/csnihndb826omzizlps90szm60q39jxd.zip',
        "format": 'zip_multi',
        "description": "Same table/URL as the FED_ICE_DETENTIONS_DDP row above ('detainers' framing vs. 'detention stints/stays' framing in the source census -- identical underlying zip). Will skip as a duplicate manifest row at run time.",
    },
    # --- ice_offices ---
    {
        "group": 'ice_offices',
        "table": 'FED_ICE_OFFICES_AOR',
        "url": 'https://github.com/deportationdata/ice-offices/raw/refs/heads/main/data/ice-offices.xlsx',
        "format": 'xlsx',
        "description": "ICE ERO field offices and check-in sub-offices list (Deportation Data Project). Confirmed live, ~40.6KB. Companion shapefiles (field/sub-office points, ERO area-of-responsibility polygons, county-level AOR polygons) exist at the same repo path if a geospatial grain is wanted.",
    },
    # --- house_clerk_fd ---
    {
        "group": 'house_clerk_fd',
        "table": 'FED_HOUSE_CLERK_FD_INDEX',
        "url": 'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/2025FD.ZIP',
        "format": 'zip_csv',
        "description": "House Clerk Financial Disclosure Reports annual index (filer name, doc ID, filing date/type) -- 2025 vintage. Confirmed live, ~100KB zip containing both a .txt and .xml index; zip_csv's largest-file pick grabs the .txt. CAVEAT: this is an index of who filed and when with a doc ID pointing at individually-hosted scanned PDF filings -- not the underlying financial figures themselves.",
    },
    # --- eu_transparency_register ---
    {
        "group": 'eu_transparency_register',
        "table": 'INTL_EU_TRANSPARENCY_REGISTER',
        "url": 'https://ec.europa.eu/transparencyregister/public/files/ODP/download/XML/latest',
        "format": 'xml_generic',
        "description": "EU Transparency Register (Joint Transparency Register Secretariat) open dataset -- one row per registered lobbying organisation. Confirmed live: the 'latest' XML endpoint returns a dated file (~109MB), no login. NOTE: this repo's load_xml loader is hardcoded to the UN Security Council sanctions list's specific <INDIVIDUALS>/<ENTITIES> tag shape -- reusing it here would just raise 'no INDIVIDUAL/ENTITY records found', so this is tagged with a distinct unregistered format (xml_generic) instead of pretending it's a match. A real loader for this shape doesn't exist yet.",
    },
    # --- fcc_publicfiles ---
    {
        "group": 'fcc_publicfiles',
        "table": 'FED_FCC_PUBLICFILES_POLITICAL',
        "url": 'https://publicfiles.fcc.gov/api/manager',
        "format": 'json_api',
        "description": "FCC Online Public Inspection File -- Political File (broadcast station political ad disclosures) via a real, live, no-auth Swagger-documented file-manager API. There's no single bulk-download URL -- it's a hierarchical folder/file browsing API (enumerate by facility, tens of thousands of stations). Deliberately left with no JSON_API_RECORD_PATH override (same treatment as FED_USASPENDING_TAS_FILTER_TREE in the template) so it falls through to the generic heuristic rather than pretending a one-shot GET produces a real records table; needs its own recursive loader later.",
    },
    # --- ocd_id ---
    {
        "group": 'ocd_id',
        "table": 'XC_OCD_DIVISION_IDS',
        "url": 'https://raw.githubusercontent.com/opencivicdata/ocd-division-ids/master/identifiers/country-us.csv',
        "format": 'csv',
        "description": "Open Civic Data Division Identifiers (OCD-ID) -- one row per US state/county/place/school-district identifier. Confirmed live via the raw GitHub URL (the repo page itself 403s bot fetchers, the raw file doesn't), ~21MB.",
    },
    # --- faa_airmen ---
    {
        "group": 'faa_airmen',
        "table": 'FED_FAA_AIRMEN_CERTIFICATION',
        "url": 'https://registry.faa.gov/database/CS082026.zip',
        "format": 'zip_csv',
        "description": "FAA Airmen Certification Database (Releasable Airman File), comma-delimited monthly export. Confirmed real via HTTP Range request (plain GET/HEAD intermittently 503s from Akamai throttling -- a real loader needs retry/backoff), ~54.6MB, Last-Modified 2026-08-01.",
    },
    # --- accessgudid (third GUDID variant, same URL, different declared format) ---
    {
        "group": 'accessgudid',
        "table": 'FED_FDA_ACCESSGUDID_FULL_RELEASE',
        "url": 'https://accessgudid.nlm.nih.gov/release_files/download/gudid_full_release_20260803.zip',
        "format": 'zip_csv',
        "description": "Same underlying AccessGUDID full-release zip as FED_FDA_GUDID_FULL_RELEASE earlier in this manifest, under a third table name in the source census. Confirmed via HEAD, 541,460,684 bytes (~516MB) -- exceeds the 500MB cap. Will skip as a duplicate source (same URL) at run time.",
    },
    # --- nhtsa_recalls ---
    {
        "group": 'nhtsa_recalls',
        "table": 'FED_NHTSA_RECALLS_FLAT',
        "url": 'https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip',
        "format": 'zip_csv',
        "sep": '\t',
        "header": None,
        "description": "NHTSA Recalls bulk flat file, post-2010 (the api.nhtsa.gov campaignNumber lookup is single-campaign only, not bulk -- this static.nhtsa.gov S3 path is the real bulk source). Confirmed live, ~14.7MB. Tab-delimited with NO header row (29 fields incl. CAMPNO/MAKETXT/MODELTXT per NHTSA's own companion schema doc) -- loaded with header=None, so columns land as COL_0.. rather than a real schema; a companion PRE_2010 file (~7.3MB) exists at the same path.",
    },
    # --- fda_device (MAUDE, dup URL) ---
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_EVENT_MAUDE',
        "url": 'https://api.fda.gov/device/event.json',
        "format": 'json_api',
        "description": "Same endpoint as FED_FDA_MAUDE_DEVICE_EVENTS earlier in this manifest, under a different table name -- openFDA's own bulk manifest lists ~18.0GB across 362 partitions for the full corpus (this one-shot loader only pulls the default page). Will skip as a duplicate source (same URL) at run time.",
    },
    # --- fda_drug (FAERS, dup URL) ---
    {
        "group": 'fda_drug',
        "table": 'FED_FDA_DRUG_EVENT_FAERS',
        "url": 'https://api.fda.gov/drug/event.json',
        "format": 'json_api',
        "description": "Same endpoint as FED_FDA_FAERS_DRUG_EVENTS earlier in this manifest, under a different table name -- openFDA's own bulk manifest lists ~113.5GB across 1,767 partitions for the full corpus (this one-shot loader only pulls the default page). Will skip as a duplicate source (same URL) at run time.",
    },
    # --- fda (food enforcement) ---
    {
        "group": 'fda',
        "table": 'FED_FDA_FOOD_ENFORCEMENT',
        "url": 'https://api.fda.gov/food/enforcement.json',
        "format": 'json_api',
        "description": "openFDA Food Enforcement Reports (Recall Enterprise System). Confirmed live: real JSON, meta.results.total=29,275. openFDA's own bulk manifest confirms 29,275 records / 5.5MB, single partition, weekly refresh -- small and easy despite looking like a big-agency source.",
    },
    # --- epa (TRI basic) ---
    {
        "group": 'epa',
        "table": 'FED_EPA_TRI_BASIC',
        "url": 'https://data.epa.gov/efservice/downloads/tri/mv_tri_basic_download/2023_US/csv',
        "format": 'csv',
        "description": "EPA TRI (Toxics Release Inventory) Basic Data Files, 2023 national extract (~100 Form R/Form A fields incl. YEAR, TRIFD, FRS ID, FACILITY NAME). Confirmed real: HEAD 500s on this Akamai-fronted host (must use GET, not HEAD -- same quirk as the ISO MIC entry already in this repo). Server streams slowly (~180KB/s observed) -- a 280s test fetch only got 52MB/66,845 rows before timing out, true size plausibly 70-150MB; a real load needs a longer timeout. Only 2023 is in this URL -- the full 1987-2024 series needs 38 separate per-year fetches at the same path pattern.",
    },
    # --- fda_device (510k / PMA -- split from one combined census row) ---
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_510K',
        "url": 'https://api.fda.gov/device/510k.json',
        "format": 'json_api',
        "description": "openFDA 510(k) clearance API. Confirmed live: meta.results.total=175,686 (openFDA's own bulk manifest: 233.9MB / 175,686 records -- not actually large despite the census's grouped 'large' framing). LIKELY DUPLICATE: this exact endpoint is already in scripts/recon_bulk_load_2026-08-07.py's manifest as FED_FDA_DEVICE_510K. Source census bundled this and PMA into a single row with two URLs under one table name (\"FED_FDA_DEVICE_510K / FED_FDA_DEVICE_PMA\") -- split here into two real manifest entries since one row can only carry one url/format.",
    },
    {
        "group": 'fda_device',
        "table": 'FED_FDA_DEVICE_PMA',
        "url": 'https://api.fda.gov/device/pma.json',
        "format": 'json_api',
        "description": "openFDA PMA (premarket approval) API. Confirmed live: meta.results.total=56,853 (openFDA's own bulk manifest: 20.9MB / 56,853 records). LIKELY DUPLICATE: this exact endpoint is already in scripts/recon_bulk_load_2026-08-07.py's manifest as FED_FDA_DEVICE_PMA. See FED_FDA_DEVICE_510K above for the split-row note.",
    },
    # --- nhtsa (ODI complaints) ---
    {
        "group": 'nhtsa',
        "table": 'FED_NHTSA_ODI_COMPLAINTS',
        "url": 'https://static.nhtsa.gov/odi/ffdd/cmpl/FLAT_CMPL.zip',
        "format": 'zip_csv',
        "sep": '\t',
        "header": None,
        "description": "NHTSA ODI Vehicle Owner Complaints Database, full flat file back to 1987. Confirmed by full download: zip = 368,800,360 bytes (~369MB, under the download cap), but the single member FLAT_CMPL.txt uncompresses to ~1.5GB -- zip_csv reads the uncompressed content into memory with no size check of its own (only the compressed _get() download is capped), so this can genuinely spike memory at --run time even though the zip itself passes the cap; flagging as a real risk, not just a theoretical one. TAB-delimited with NO header row (~50-column layout documented separately by NHTSA) -- loaded with header=None, columns land as COL_0...",
    },
    # --- dailymed (SPL full dump) ---
    {
        "group": 'dailymed',
        "table": 'FED_NLM_DAILYMED_SPL_DOCUMENTS',
        "url": 'https://dailymed-data.nlm.nih.gov/public-release-files/dm_spl_release_remainder.zip',
        "format": 'zip_multi_xml',
        "description": "DailyMed's full multi-GB per-drug SPL XML label-document dump -- 19 separate category zips (6 human-Rx parts, 11 human-OTC parts, 1 homeopathic, 1 animal, 1 remainder, ~55-60GB combined), each holding thousands of individual XML documents, not one flat file. This is exactly the dump scripts/recon_bulk_load_2026-08-07.py already looked at and explicitly declined to bulk-load (loading only the small SETID mapping table instead). Format left unregistered (no loader) -- needs a dedicated 'unzip thousands of small XML docs, parse each' loader this batch does not build.",
    },
    # --- education (DAPIP) ---
    {
        "group": 'education',
        "table": 'FED_ED_DAPIP_ACCREDITATION',
        "url": 'https://ope.ed.gov/dapip/api/downloadFiles/accreditationDataFiles',
        "format": 'post_zip_multi',
        "description": "DAPIP (Database of Accredited Postsecondary Institutions and Programs) full export -- InstitutionCampus/AccreditationRecords/AccreditationActions CSVs inside a zip. DAPIP is an Angular SPA with no static download link; the real download is a POST (not GET) to this URL with a JSON body ({\"CSVChecked\":true,\"ExcelChecked\":false}), confirmed real end-to-end (200 OK, application/zip, 3,615,703 bytes). Format left unregistered (no loader) -- this script's shared _get() helper is GET-only; a POST-with-JSON-body fetch needs its own small loader rather than bending the shared helper for one entry.",
    },
    # --- usac (Form 470) ---
    {
        "group": 'usac',
        "table": 'FED_USAC_ERATE_FORM470_BIDDING',
        "url": 'https://opendata.usac.org/resource/jp7a-89nd.csv?$limit=500000',
        "format": 'csv',
        "description": "USAC E-Rate Open Competitive Bidding: Basic Information (FCC Form 470), Billed Entity Number (ben) + ~66 other columns. Confirmed real via the SODA API: 284,034 total rows (confirmed via $select=count(*)); a plain GET with no $limit only returns Socrata's default ~800-1,000 row page, so $limit=500000 is added here to grab the real dataset in one shot (well under the 5,000,000-row and 500MB caps either way, since the full table is 284,034 rows).",
    },
    # --- education (NCES CCD) ---
    {
        "group": 'education',
        "table": 'FED_ED_NCES_CCD_SCHOOL_DIRECTORY',
        "url": 'https://nces.ed.gov/sites/default/files/data-asset/ccd-common-core-data/2025/08/2024-25-common-core-data-ccd-preliminary-directory-files/2025046%20Preliminary%20Data%20Release%20CCD%20Nonfiscal_0.zip',
        "format": 'zip_csv',
        "description": "NCES Common Core of Data (CCD) SY2024-25 preliminary directory files -- school-level CSV (ST_LEAID/ST_SCHID state-assigned IDs alongside NCES LEAID/NCESSCH) plus a district-level CSV. Confirmed real: 200 OK, ~15.6MB zip; zip_csv's largest-file heuristic correctly grabs the school-level CSV (~40.7MB uncompressed) over the smaller district-level one.",
    },
    # --- aba ---
    {
        "group": 'aba',
        "table": 'FED_ABA_JD_APPLICANT_ENROLLEE_DATA',
        "url": 'https://www.americanbar.org/content/dam/aba/administrative/legal_education_and_admissions_to_the_bar/statistics/2025/2025-fall-jd-applicant-and-enrollee-class-data.xlsx',
        "format": 'xlsx',
        "description": "ABA 2025 Fall JD Applicant and Enrollee Class Data by law school (LSAT/UGPA percentiles per school). Confirmed real: 200 OK, ~109KB, one row per ABA-approved law school. NOTE: this is NOT the literal Standard 509 disclosure report (that's per-school only via a POST API, no single-file compilation found) -- this is a genuine multi-school bulk substitute sourced from the same Annual Questionnaire.",
    },
    # --- education (EADA athletics) ---
    {
        "group": 'education',
        "table": 'FED_ED_EADA_ATHLETICS',
        "url": 'https://ope.ed.gov/athletics/api/dataFiles/file?fileName=EADA_All_Data_Combined_2024-2025_SAS_SPSS_EXCEL.zip',
        "format": 'zip_xlsx',
        "member": 'EADA_2025.xlsx',
        "sheet": 'eada_2025',
        "description": "Equity in Athletics Data Analysis (EADA), 2024-25 combined data -- unitid (IPEDS UnitID) + OPEID + institution/sport rows. Confirmed by fully downloading: zip real, 17.0MB, containing EADA_2025.xlsx (11.1MB) plus larger SAS/SPSS/codebook siblings. zip_xlsx's largest-file heuristic would wrongly grab the 70.9MB SPSS .sav file, so an explicit member override points at the real xlsx.",
    },
    # --- cfpb_hmda (nationwide) ---
    {
        "group": 'cfpb_hmda',
        "table": 'FED_CFPB_HMDA_NATIONWIDE_LAR',
        "url": 'https://ffiec.cfpb.gov/v2/data-browser-api/view/nationwide/csv?years=2023',
        "format": 'csv',
        "description": "True nationwide HMDA LAR export (no state filter) via FFIEC's real nationwide/csv endpoint. Confirmed live: GET (not HEAD -- HEAD 405s) 301-redirects to a static file HEAD-confirmed at Content-Length 4,399,684,763 bytes (~4.4GB) for 2023 alone -- exceeds the 500MB cap by a wide margin, will fail cleanly at _get() time. This directly targets the known gap where this repo's current FED_CFPB_HMDA table was found to be 100% STATE_CODE='DC' (a load-scope bug) -- this is the real nationwide source, but needs a genuine streaming loader, not this one.",
    },
    # --- cfpb ---
    {
        "group": 'cfpb',
        "table": 'FED_CFPB_CONSUMER_COMPLAINTS',
        "url": 'https://files.consumerfinance.gov/ccdb/complaints.csv',
        "format": 'csv',
        "description": "CFPB Consumer Complaint Database, full history since 2011, one row per complaint across all financial products/companies. Confirmed live via HEAD: Content-Length 8,905,555,191 bytes (~8.9GB) -- by far the largest single flat-file entry in this batch, will fail cleanly at _get() time. No key/login needed for the flat-file download (a separate, smaller Open Data API also exists).",
    },
    # --- hud (subsidized households, project) ---
    {
        "group": 'hud',
        "table": 'FED_HUD_PICTURE_SUBSIDIZED_HOUSEHOLDS_PROJECT',
        "url": 'https://www.huduser.gov/portal/datasets/pictures/files/PROJECT_2025_2020census.xlsx',
        "format": 'xlsx',
        "description": "HUD Picture of Subsidized Households, project/development grain, SY2025 (2020-census geography). Confirmed live with a normal browser User-Agent (huduser.gov runs an AWS WAF that 202/0-byte-challenges a bare curl -- a UA issue, not a real auth wall), ~17.5MB.",
    },
    # --- cfpb_hmda (historic) ---
    {
        "group": 'cfpb_hmda',
        "table": 'FED_CFPB_HMDA_HISTORIC',
        "url": 'https://files.consumerfinance.gov/hmda-historic-loan-data/hmda_2007_nationwide_first-lien-owner-occupied-1-4-family-records_labels.zip',
        "format": 'zip_csv',
        "description": "HMDA historic (pre-2018) nationwide first-lien-owner-occupied LAR flat files, 2007 vintage. Confirmed live via HEAD: 453,036,077 bytes (~432MB) -- under the 500MB cap but close. This repo's scripts/hmda_historic_lar_load.py already loads this same file family for 2015-2017 only (a scoped 3-year slice) -- this URL pattern (swap the year) closes the gap for 2007-2014, each year individually ~350-455MB, multi-GB in aggregate across all 8 missing years.",
    },
    # --- la_county ---
    {
        "group": 'la_county',
        "table": 'ST_LACOUNTY_ASSESSOR_PARCELS',
        "url": 'https://apps.gis.lacounty.gov/hubfiles/LACounty_Parcels_Shapefile.zip',
        "format": 'zip_shapefile',
        "description": "LA County Assessor parcel data (~2.4M parcels), shapefile export via the county's ArcGIS Hub sharing API. Confirmed live via HEAD, ~336.8MB. SCOPE CAVEAT (matches the source's own framing): this is one county, not a national parcel-ID system -- county assessor parcel numbering is fragmented nationally, no federal aggregator exists. Format left unregistered (no loader) -- needs geopandas/fiona, not confirmed available in this environment, so not forced in.",
    },
    # --- hud (LIHTC BIN) ---
    {
        "group": 'hud',
        "table": 'FED_HUD_LIHTC_PROPERTY_BIN',
        "url": 'https://www.huduser.gov/lihtc/lihtcpub.zip',
        "format": 'zip_xlsx',
        "member": 'LIHTCPUB_BIN.xlsx',
        "description": "HUD LIHTC Database, Building Identification Number (BIN) extract. Confirmed by fully downloading: zip real, 29,421,665 bytes (~29.4MB), containing LIHTCPUB.accdb (source DB), LIHTCPUB.xlsx (fuller property-level export, ~13.0MB), and LIHTCPUB_BIN.xlsx (~6.2MB, the BIN-specific extract) -- an explicit member override picks the BIN file since zip_xlsx's largest-file heuristic would otherwise grab the bigger property-level workbook instead.",
    },
    # --- dot ---
    {
        "group": 'dot',
        "table": 'FED_DOT_NAD_ADDRESSES',
        "url": 'https://data.transportation.gov/download/fc2s-wawr/application/x-zip-compressed',
        "format": 'zip_csv',
        "description": "DOT National Address Database (NAD) -- nationwide address points with jurisdiction/coordinate/OID metadata. Confirmed real via a 1-byte Range GET (HEAD timed out): Content-Range total 7,601,412,707 bytes (~7.6GB) -- the single largest entry in this batch, exceeds the 500MB cap by ~15x, will fail cleanly at _get() time. Needs a dedicated streaming loader; not remotely viable in-memory.",
    },
    # --- richmond_dsl ---
    {
        "group": 'richmond_dsl',
        "table": 'XC_RICHMOND_DSL_REDLINING_ZONES',
        "url": 'https://data.source.coop/cboettig/mappinginequality/mappinginequality.parquet',
        "format": 'parquet',
        "description": "Mapping Inequality (University of Richmond Digital Scholarship Lab) HOLC redlining-zone dataset, nationwide, mirrored on source.coop as Parquet (the census's original dsl.richmond.edu fullDownload.geojson URL is stale -- it now just serves the site's generic SPA shell, not real data). Confirmed by fully downloading and reading with pandas: 2,777,622 bytes (~2.78MB), 10,154 rows x 15 columns (area_id, city, state, grade, label, residential/commercial/industrial flags, geom, geom_bbox). Uses the new load_parquet loader added in this file -- needs pyarrow (or another pandas parquet engine) installed to actually run.",
    },
    # --- fac ---
    {
        "group": 'fac',
        "table": 'FED_FAC_AUDIT_GENERAL',
        "url": 'https://app.fac.gov/dissemination/public-data/gsa/full/general.csv',
        "format": 'csv',
        "description": "Federal Audit Clearinghouse (FAC) Single Audit Report Database, 'general' table -- one row per submitted single-audit report (UEI, auditee name, fiscal year end, audit year). Confirmed via Range request against the app.fac.gov -> signed-S3 redirect: 265,406,777 bytes (~253MB). Eight companion tables (federal_awards, findings, findings_text, corrective_action_plans, passthrough, additional_eins, additional_ueis, notes_to_sefa, secondary_auditors) exist at the same path pattern; federal_awards.csv alone is ~1.27GB and would need its own row.",
    },
    # --- phmsa (gas distribution) ---
    {
        "group": 'phmsa',
        "table": 'FED_PHMSA_GAS_DISTRIBUTION_ANNUAL',
        "url": 'https://zenodo.org/api/records/18524048/files/phmsagas_gas_distribution_2010_present.zip/content',
        "format": 'zip_csv',
        "description": "PHMSA Gas Distribution annual report data, 2010-present, keyed by OPERATOR_ID. www.phmsa.dot.gov itself is fully Akamai-blocked (403 on every path) -- this uses Catalyst Cooperative's PUDL project mirror of PHMSA's own raw zips on Zenodo, confirmed real via the Zenodo API record, ~30MB compressed. Companion Gas Transmission & Gathering (~100MB) and Hazardous Liquid (~34MB) files exist at the same record.",
    },
    # --- ferc ---
    {
        "group": 'ferc',
        "table": 'FED_FERC_FORM1_ANNUAL',
        "url": 'https://cms.ferc.gov/sites/default/files/2022-01/form1_-_2021.zip',
        "format": 'zip_dbf',
        "description": "FERC Form 1 Electric Utility financial filings, FY2021 (legacy DBF/Visual FoxPro era, RESPONDENT_ID-keyed). Confirmed live via Range GET: 47,697,257 bytes (~45.5MB). This is the last DBF-era year (2011-2021 vintages exist at the same pattern) -- FERC switched to per-filer XBRL for 2021-present with no found single bulk-download file. Format left unregistered (no loader) -- DBF parsing needs a library (e.g. dbfread) not confirmed available in this environment.",
    },
    # --- fracfocus ---
    {
        "group": 'fracfocus',
        "table": 'FED_FRACFOCUS_REGISTRY',
        "url": 'https://www.fracfocusdata.org/digitaldownload/FracFocusCSV.zip',
        "format": 'zip_multi',
        "description": "FracFocus Chemical Disclosure Registry well data (state-assigned API Well Number). Confirmed live and auth-free: compressed zip is 439,402,224 bytes (~419MB, under the download cap), but its central directory (read via Range request, not a full download) shows 18 member files totaling ~3.49GB uncompressed -- 16 chunked FracFocusRegistry_N.csv files plus DisclosureList.csv and WaterSource.csv. zip_multi (5-largest-CSV cap) is a closer fit than zip_csv (which would silently keep only one ~245MB chunk of the 3.49GB total) but still won't get full coverage in one pass.",
    },
    # --- eia_176 ---
    {
        "group": 'eia_176',
        "table": 'FED_EIA176_NATURAL_GAS_RESPONDENTS',
        "url": 'https://zenodo.org/api/records/18909200/files/eia176-bulk.zip/content',
        "format": 'zip_csv',
        "description": "EIA-176 Natural Gas Annual Respondent Query System bulk export (Company ID / respondent-level), via Catalyst Cooperative's PUDL Zenodo mirror since eia.gov/naturalgas/ngqs/ is a JS query-builder with no bulk link. Confirmed real filename/URL via the Zenodo API record, ~10.0MB.",
    },
    # --- phmsa (enforcement) ---
    {
        "group": 'phmsa',
        "table": 'FED_PHMSA_ENFORCEMENT_ACTIONS',
        "url": 'https://primis.phmsa.dot.gov/enforcement-documents/PHMSA%20Pipeline%20Enforcement%20Raw%20Data.txt',
        "format": 'csv',
        "sep": '\t',
        "description": "PHMSA Pipeline Safety Enforcement Actions (CPF case numbers), via the reachable primis.phmsa.dot.gov subdomain (www.phmsa.dot.gov itself is Akamai-blocked). Confirmed via direct fetch of the first 500 bytes: real tab-delimited header (CPF_Number, Operator_ID, Operator_Name, Region, Pipeline_Type, Case_Type, penalties, Case_Status, ...). Despite the .txt extension it's tab-delimited, not comma -- sep='\\t'. ~1.97MB, updated monthly.",
    },
    # --- phmsa (underground gas storage) ---
    {
        "group": 'phmsa',
        "table": 'FED_PHMSA_UNDERGROUND_GAS_STORAGE',
        "url": 'https://zenodo.org/api/records/18524048/files/phmsagas_underground_natural_gas_storage_2017_present.zip/content',
        "format": 'zip_csv',
        "description": "PHMSA post-Aliso Canyon Underground Natural Gas Storage Facility annual reporting, 2017-present, via the same PUDL Zenodo mirror as the Gas Distribution entry above. Confirmed real filename/URL via the Zenodo API record, ~2.3-2.6MB.",
    },
    # --- fda (IMS list) ---
    {
        "group": 'fda',
        "table": 'FED_FDA_IMS_LIST',
        "url": 'https://www.fda.gov/media/193497/download?attachment',
        "format": 'pdf',
        "description": "FDA Interstate Milk Shippers (IMS) List -- quarterly roster of NCIMS-certified state-regulated milk shippers/processors/haulers/labs with sanitation compliance ratings. Confirmed real: HTTP 200, application/pdf, 2,529,083 bytes (~2.4MB). PDF-only, no CSV/Excel -- format left unregistered (no loader), same open gap already noted for the JPML entry in the template.",
    },
    # --- fcc (EAS grantee) ---
    {
        "group": 'fcc',
        "table": 'FED_FCC_EAS_GRANTEE_REGISTRATIONS',
        "url": 'https://opendata.fcc.gov/resource/3b3k-34jp.csv',
        "format": 'csv',
        "description": "FCC Equipment Authorization System (EAS) Grantee Registrations -- maps each Grantee Code (the fixed prefix of every FCC ID) to registered company name/address/registration date. Confirmed real: the legacy apps.fcc.gov/oetcf/eas ColdFusion search tool 403s and looks retired; this Socrata mirror confirmed live via a full real GET, 8,241,406 bytes (~8.0MB), 50,153 rows. STALENESS: catalog metadata shows last update 2021-03-22. SCOPE: grantee-code registry only, not the fuller per-product equipment-authorization grant records.",
    },
    # --- fcc (911 PSAP) ---
    {
        "group": 'fcc',
        "table": 'FED_FCC_911_PSAP_REGISTRY',
        "url": 'https://opendata.fcc.gov/resource/dpq5-ta9j.csv',
        "format": 'csv',
        "description": "FCC 911 Master PSAP Registry -- one row per Public Safety Answering Point (FCC-assigned PSAP ID, name, county, city, state). Confirmed real: fcc.gov's own page 403s, this Socrata mirror confirmed via a full real GET, 1,576,594 bytes (~1.5MB), 8,557 rows. STALENESS: catalog metadata shows last update 2017-10-10 -- fcc.gov itself reportedly has a fresher xlsx (~April 2025) behind the blocked page.",
    },
    # --- usac (recipients of service) ---
    {
        "group": 'usac',
        "table": 'FED_USAC_ERATE_RECIPIENTS_OF_SERVICE',
        "url": 'https://opendata.usac.org/resource/tuem-agyq.csv?$limit=500000',
        "format": 'csv',
        "description": "USAC E-Rate FCC Form 471 Recipients of Service -- ben (Billed Entity Number), application_number, funding_request_number, organization_name. Confirmed real via the SODA API, row count confirmed live at 41,377,397. Full export would be ~8.8GB (212 bytes/row extrapolated) -- $limit=500000 caps this single GET to a representative slice well under the 500MB/5,000,000-row caps; a real full pull needs offset-paginated looping, not this one-shot loader.",
    },
    # --- education (NCES CIP -- wait, not in this batch, placeholder removed) ---
    # --- usac (high cost) ---
    {
        "group": 'usac',
        "table": 'FED_USAC_HIGH_COST_DISBURSEMENTS',
        "url": 'https://opendata.usac.org/resource/w6qn-gx72.csv?$limit=2000000',
        "format": 'csv',
        "description": "USAC High Cost Universal Service Fund disbursements by Study Area Code (SAC) -- study_area_code, study_area_name, state, year, month, fund_type, amount_disbursed. Confirmed real via the SODA API, row count confirmed live at 1,041,193 (~87MB full extrapolated). $limit=2000000 exceeds the real row count, so this single GET grabs the entire table in one shot, safely under the 500MB/5,000,000-row caps.",
    },
    # --- celestrak ---
    {
        "group": 'celestrak',
        "table": 'XC_CELESTRAK_SATCAT',
        "url": 'https://celestrak.org/pub/satcat.csv',
        "format": 'csv',
        "description": "CelesTrak Satellite Catalog (SATCAT) -- NORAD Catalog Number + object name, international designator, launch/decay dates, orbital class. Confirmed live via direct GET, real CSV, no auth. Content-Length 6,696,674 bytes (~6.7MB).",
    },
    # --- fcc (consumer complaints) ---
    {
        "group": 'fcc',
        "table": 'FED_FCC_CONSUMER_COMPLAINTS',
        "url": 'https://opendata.fcc.gov/api/views/3xyp-aqkj/rows.csv?accessType=DOWNLOAD',
        "format": 'csv',
        "description": "FCC Consumer Complaints Data Center -- individual informal complaints filed with the FCC Consumer Help Center since Oct 2014, updated nightly. Confirmed real: www.fcc.gov/consumer-help-center-data 403s (Akamai), this opendata.fcc.gov Socrata mirror confirmed live, real text/csv. Row count confirmed live at 3,606,141 -- this classic 'accessType=DOWNLOAD' view endpoint serves the whole dataset in one response (no $limit param applies), extrapolated to ~833MB, which exceeds the 500MB cap and will fail cleanly at _get() time rather than silently truncate.",
    },
    # --- usac (FRN line items) ---
    {
        "group": 'usac',
        "table": 'FED_USAC_ERATE_FRN_LINE_ITEMS',
        "url": 'https://opendata.usac.org/resource/hbj5-2bpj.csv?$limit=500000',
        "format": 'csv',
        "description": "USAC E-Rate FCC Form 471 FRN Line Items -- funding_request_number, application_number, ben, organization_name, cost/pricing, product/service description. Confirmed real via the SODA API, row count confirmed live at 4,575,123 (~1.68GB full extrapolated). $limit=500000 caps this single GET to a representative slice under the caps; a real full pull needs offset-paginated looping.",
    },
    # --- cms (plan ID crosswalk) ---
    {
        "group": 'cms',
        "table": 'FED_CMS_PLAN_ID_CROSSWALK',
        "url": 'https://data.healthcare.gov/datafile/py2026/plan_id_crosswalk_PUF.csv',
        "format": 'csv',
        "description": "CMS/CCIIO Marketplace Plan ID Crosswalk PUF, plan year 2026 -- maps prior-year QHPs/SADPs to current-year plans. Confirmed live: HTTP 200, application/octet-stream, attachment disposition. 21,053,238 bytes (~21MB). Prior-year vintages (PY2021-PY2025) exist at the same URL pattern.",
    },
    # --- cms (MA/PartD monthly by plan) ---
    {
        "group": 'cms',
        "table": 'FED_CMS_MA_PARTD_MONTHLY_ENROLLMENT_PLAN',
        "url": 'https://www.cms.gov/files/zip/monthly-enrollment-plan-september-2025.zip',
        "format": 'zip_csv',
        "description": "CMS Medicare Advantage/Part D 'Monthly Enrollment by Plan' report, September 2025 vintage. Confirmed live: HTTP 200, application/zip. ~632KB -- much smaller than its 'large' size-class guess. NOTE: monthly-refreshed with a new dated URL each month -- re-point going forward, don't hardcode this month long-term.",
    },
    # --- treasury ---
    {
        "group": 'treasury',
        "table": 'FED_TREASURY_CIRCULAR_570_SURETIES',
        "url": 'https://fiscal.treasury.gov/system/files/files/surety-bonds/list-certified-companies.xlsx',
        "format": 'xlsx',
        "description": "Treasury Circular 570 -- companies holding Certificates of Authority as acceptable sureties/reinsurers on federal bonds (always-current spreadsheet successor to the annual PDF). Confirmed live, real spreadsheetml content-type, ~154KB. A supplemental-changes.xlsx (interim changes) exists at the same path.",
    },
    # --- vt_captives ---
    {
        "group": 'vt_captives',
        "table": 'ST_VT_CAPTIVE_INSURANCE_COMPANIES',
        "url": 'https://dfr.vermont.gov/sites/finreg/files/documents/Licensed%20Captive%20Insurance%20Companies%20as%20of%2009302025.pdf',
        "format": 'pdf',
        "description": "Vermont Dept. of Financial Regulation's current list of licensed Vermont captive insurance companies (as of 09/30/2025). Confirmed live: HTTP 200, real application/pdf, ~622KB, no login. PDF table -- format left unregistered (no loader), same open gap as the other pdf entries in this batch.",
    },
    # --- hud (subsidized households, PHA) ---
    {
        "group": 'hud',
        "table": 'FED_HUD_PICTURE_SUBSIDIZED_HOUSEHOLDS_PHA',
        "url": 'https://www.huduser.gov/portal/datasets/pictures/files/PHA_2025_2020census.xlsx',
        "format": 'xlsx',
        "description": "HUD Picture of Subsidized Households, Public Housing Agency (PHA-code) grain, SY2025. Confirmed live, real spreadsheetml content-type, 7,380,733 bytes (~7.4MB).",
    },
    # --- hud (MF properties assisted) ---
    {
        "group": 'hud',
        "table": 'FED_HUD_MF_PROPERTIES_ASSISTED',
        "url": 'https://opendata.arcgis.com/api/v3/datasets/f4721da932a94b218bdb5a861fd7429e_0/downloads/data?format=csv&spatialRefId=4326&where=1%3D1',
        "format": 'csv',
        "description": "HUD 'Multifamily Properties - Assisted' dataset (project-based Section 8 / assisted multifamily properties) via HUD's ArcGIS Open Data Hub CSV export. Confirmed by full download: 200 OK, real text/csv, 23,758 rows, ~42.3MB.",
    },
    # --- cms_ma_partd ---
    {
        "group": 'cms_ma_partd',
        "table": 'FED_CMS_MA_PARTD_ENROLLMENT_CONTRACT',
        "url": 'https://www.cms.gov/files/zip/monthly-report-contract-2026-07-zip.zip',
        "format": 'zip_csv',
        "description": "CMS Medicare Advantage/Part D monthly enrollment-by-contract report, July 2026. Confirmed live: 200 OK, real application/zip, downloaded and inspected -- contains a CSV + matching xlsx + readme, zip_csv's largest-file heuristic correctly grabs the CSV. ~128KB. NOTE: month-specific URL, needs re-pointing monthly.",
    },
    # --- opm_fehb ---
    {
        "group": 'opm_fehb',
        "table": 'FED_OPM_FEHB_RATES',
        "url": 'https://www.opm.gov/healthcare-insurance/healthcare/transparency-in-healthcare/public-use-files/2026/fehb/2026-fehb-rates-10232025.xlsx',
        "format": 'xlsx',
        "description": "OPM FEHB (Federal Employees Health Benefits) plan rates PUF, plan year 2026 -- one row per plan/enrollment-code with premium and government contribution amounts. Confirmed live, real spreadsheetml content-type, ~370KB. Companion Plan Key/Benefits/Service Area/Payroll Rates files (also PSHB and FEDVIP variants) exist at the same URL pattern.",
    },
    # --- cms_marketplace_puf ---
    {
        "group": 'cms_marketplace_puf',
        "table": 'FED_CMS_MARKETPLACE_RATE_PUF',
        "url": 'https://download.cms.gov/marketplace-puf/2026/rate-puf.zip',
        "format": 'zip_csv',
        "description": "CMS Health Insurance Marketplace Rate PUF, plan year 2026 -- one row per rating-area/plan/age-band premium (the modern successor to the discontinued QHP Landscape files). Confirmed by full download and zip inspection: 16.2MB zip containing a single Rate_PUF.csv (~280.7MB uncompressed).",
    },
    # --- fema ---
    {
        "group": 'fema',
        "table": 'FED_FEMA_HOUSING_ASSISTANCE_OWNERS_V2',
        "url": 'https://www.fema.gov/api/open/v2/HousingAssistanceOwners',
        "format": 'json_api',
        "description": "FEMA OpenFEMA HousingAssistanceOwners v2 -- county/disaster-level aggregate Individual Assistance stats (validRegistrations, totalInspected, totalApprovedIhpAmount), no individual-applicant PII. Confirmed live JSON, no auth, paginated via $skip/$top. Total 159,959 records confirmed live via $inlinecount=allpages (~112MB estimated full pull) -- this one-shot loader pulls only the default page unless the URL itself carries a high $top.",
    },
    # --- orcid ---
    {
        "group": 'orcid',
        "table": 'XC_ORCID_PUBLIC_DATA_FILE',
        "url": 'https://ndownloader.figshare.com/files/58834837',
        "format": 'tar_gz',
        "description": "ORCID Public Data File 2025 annual snapshot (CC0), 'summaries' tar.gz -- one flattened XML/JSON record per ORCID iD. Confirmed live via HEAD (302 to a signed S3 URL matching the Figshare-listed size). The summaries file alone is ~46.3GB; the full release (summaries + 11 activities shards) is ~232GB. Format left unregistered (no loader) -- guaranteed to hit the size cap regardless, and tar handling + per-record XML/JSON parsing isn't a trivial sibling of the existing zip loaders.",
    },
    # --- openalex ---
    {
        "group": 'openalex',
        "table": 'XC_OPENALEX_WORKS',
        "url": 'https://openalex.s3.amazonaws.com/data/jsonl/manifest.json',
        "format": 'jsonl_gz',
        "description": "OpenAlex full snapshot (works, authors, sources, institutions, topics, publishers, funders) on a public, unauthenticated S3 bucket, updated monthly. Confirmed live via the bucket's own manifest.json -- the 'works' entity alone is 100GB+ across many gzipped JSONL part-files (Parquet also available). Total across all entities: 745.5GB / 649M records per the snapshot's own manifest. Format left unregistered (no loader) -- manifest-driven multi-file streaming is out of scope for a single-URL-per-entry loader.",
    },
    # --- pubmed ---
    {
        "group": 'pubmed',
        "table": 'FED_NLM_PUBMED_BASELINE',
        "url": 'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/',
        "format": 'xml_gz',
        "description": "NLM/NCBI's complete annual PubMed baseline snapshot in MEDLINE XML -- ~1,334 separate gzipped XML files, confirmed live via a plain directory listing (no login wall; the site's 'Terms and Conditions' text is informational, not an enforced gate). ~50.6GB total, summed directly from the real directory listing. The URL here is a directory listing, not a single fetchable file -- format left unregistered (no loader), needs a real multi-file loop-and-fetch design.",
    },
    # --- pmc ---
    {
        "group": 'pmc',
        "table": 'FED_NLM_PMC_IDS_XREF',
        "url": 'https://ftp.ncbi.nlm.nih.gov/pub/pmc/PMC-ids.csv.gz',
        "format": 'csv_gz',
        "description": "NLM/NCBI PMC-ids.csv.gz -- the PMID/PMCID/DOI/journal crosswalk covering the whole PMC corpus. Confirmed live via direct FTP-over-HTTPS directory listing, no auth, ~240MB gzip-compressed. Uses the new load_csv_gz loader added in this file (a trivial gzip sibling of the template's load_bz2_csv). NOTE: only the crosswalk is pulled here -- the much larger full-text OA XML bulk (183GB+ just for one of three buckets) is deliberately NOT included.",
    },
    # --- crossref (works API) ---
    {
        "group": 'crossref',
        "table": 'XC_CROSSREF_WORKS',
        "url": 'https://api.crossref.org/works',
        "format": 'json_api',
        "description": "Crossref's public REST API for DOI/works metadata. Confirmed live with a real GET (HEAD 405s, expected/documented). No auth required (a mailto= param is recommended for the 'polite pool' but not required). 185,277,841 total works confirmed live via a real ?rows=0 count query -- this one-shot loader pulls only the default page, not a bulk file; needs a cursor-paginated loader for a full pull.",
    },
    # --- nih_reporter ---
    {
        "group": 'nih_reporter',
        "table": 'FED_NIH_REPORTER_PROJECTS',
        "url": 'https://api.reporter.nih.gov/v2/projects/search',
        "format": 'json_api_post',
        "description": "NIH RePORTER Project Search API -- confirmed live with a real POST request (criteria/limit/offset JSON body) returning PI/org/award amount/abstract/terms/dates, no auth. Unlike this script's GET-based json_api loader, this is POST-with-JSON-body; pagination is also hard-capped at offset 14,999 by NIH's own API, so a full historical pull needs chunking by fiscal_year, not straight paging. Format left unregistered (no loader) rather than guessing a default criteria body that might silently produce a misleading partial pull.",
    },
    # --- usaspending ---
    {
        "group": 'usaspending',
        "table": 'FED_USASPENDING_ASSISTANCE_BULK',
        "url": 'https://api.usaspending.gov/api/v2/download/awards/',
        "format": 'async_job_api',
        "description": "USAspending.gov bulk assistance-award download -- a two-step async job (POST creates a job with status_url + file_url, poll status_url, then GET the zip), confirmed real with a live test job. LIKELY DUPLICATE: this repo already has a mature FED_USASPENDING_ASSISTANCE_FULL mart with extensive dbt tests, so the underlying data is probably already loaded via a different mechanism. Format left unregistered (no loader) -- an async POST-then-poll-then-GET job doesn't fit this script's single-fetch loader shape.",
    },
    # --- arxiv ---
    {
        "group": 'arxiv',
        "table": 'XC_ARXIV_METADATA',
        "url": 'https://export.arxiv.org/oai2?verb=ListRecords&metadataPrefix=arXiv',
        "format": 'oai_pmh_xml',
        "description": "arXiv bulk metadata via the standard OAI-PMH harvest endpoint. Confirmed live and auth-free: a real GET returned 1,300 records (3.07MB) with a valid resumptionToken for continued paging. Needs a new paginated-harvest loader (loop on resumptionToken, typically rate-limited over many sequential requests) -- ~6GB of raw XML for a full metadata harvest, not a single-file fetch, so left unregistered rather than reusing load_xml (which expects a different, flat, non-paginated shape).",
    },
    # --- osti ---
    {
        "group": 'osti',
        "table": 'FED_OSTI_RECORDS',
        "url": 'https://www.osti.gov/api/v1/records',
        "format": 'json_api',
        "description": "OSTI.GOV Records API (DOE technical reports) -- osti_id, title, authors, sponsor_orgs, DOI, links. Confirmed live JSON, no auth. Total corpus 4,172,008 records confirmed via the X-Total-Count response header; the payload is a top-level JSON array so load_json_api's existing list-detection handles it with no override needed. This one-shot loader pulls only the default page of a rows/page-paginated API.",
    },
    # --- gleif ---
    {
        "group": 'gleif',
        "table": 'INTL_GLEIF_RR',
        "url": 'https://goldencopy.gleif.org/storage/golden-copy-files/2026/08/08/1261145/20260808-0000-gleif-goldencopy-rr-golden-copy.csv.zip',
        "format": 'zip_csv',
        "description": "GLEIF Level 2 Relationship Data (direct/ultimate parent LEI relationships) golden-copy CSV zip. Confirmed live via HEAD, 24,200,821 bytes (~23.08MB), 483,992 relationship records confirmed via GLEIF's own /publishes/latest API. NOTE: URL is date-stamped and rotates daily -- a real loader should hit /publishes/latest first, not hardcode this path. LIKELY DUPLICATE: this repo already has scripts/gleif_relationships_load.py hitting this exact endpoint plus existing GLEIF RR marts -- probably already loaded.",
    },
    # --- sirene ---
    {
        "group": 'sirene',
        "table": 'INTL_FR_SIRENE_UNITE_LEGALE',
        "url": 'https://static.data.gouv.fr/resources/base-sirene-des-entreprises-et-de-leurs-etablissements-siren-siret/20260801-072607/stock-stockunitelegale-csv.zip',
        "format": 'zip_csv',
        "description": "France's Base Sirene legal-unit register (SIREN-level), monthly refresh. Confirmed via data.gouv.fr's own API filesize field (not downloaded): 970,595,120 bytes (~925.6MB) -- exceeds the 500MB cap by nearly 2x, will fail cleanly at _get() time. A companion establishment-level (SIRET) file is even bigger (~2.66GB).",
    },
    # --- irs (FATCA, duplicate manifest row) ---
    {
        "group": 'irs',
        "table": 'FED_IRS_FATCA_FFI_LIST',
        "url": 'https://apps.irs.gov/app/fatcaFfiList/data/FFIListFull.csv',
        "format": 'csv',
        "description": "Same table/URL as the FED_IRS_FATCA_FFI_LIST row earlier in this manifest. Will skip as a duplicate manifest row at run time.",
    },
    # --- opensanctions (duplicate source, different table name) --- EXCLUDED 2026-08-07,
    # same reason as the other OpenSanctions entry above.
    # --- companies_house (third PSC variant) ---
    {
        "group": 'companies_house',
        "table": 'CORPORATE_REGISTRY_UK_COMPANIES_HOUSE_PSC',
        "url": 'https://download.companieshouse.gov.uk/persons-with-significant-control-snapshot-2026-08-07.zip',
        "format": 'zip_multi',
        "description": "Same underlying UK Companies House PSC daily snapshot as the two INTL_UK_COMPANIESHOUSE_PSC* rows earlier in this manifest, under a third table name. LIKELY DUPLICATE OF EXISTING INFRA: this repo already has scripts/uk_ch_psc_load.py purpose-built for this exact dataset (32-chunk, JSON-lines-in-zip, checkpointed loader). Will skip as a duplicate source (same URL) at run time.",
    },
    # --- icij (third variant, same URL) ---
    {
        "group": 'icij',
        "table": 'XC_ICIJ_OFFSHORE_LEAKS',
        "url": 'https://offshoreleaks-data.icij.org/offshoreleaks/csv/full-oldb.LATEST.zip',
        "format": 'zip_multi',
        "description": "Same table/URL as the XC_ICIJ_OFFSHORE_LEAKS row earlier in this manifest. LIKELY DUPLICATE OF EXISTING INFRA: this repo already has scripts/icij_offshoreleaks_load.py for this exact dataset. Will skip as a duplicate manifest row at run time.",
    },
    # --- japan_nta ---
    {
        "group": 'japan_nta',
        "table": 'INTL_JP_NTA_CORPORATE_NUMBERS',
        "url": 'https://www.houjin-bangou.nta.go.jp/download/zenken/index.html',
        "format": 'csrf_post_zip',
        "description": "Japan National Tax Agency Corporate Number Publication Site, nationwide bulk download (Shift-JIS CSV variant). Confirmed end-to-end with curl replicating the real two-step flow: GET the page for a session cookie + CSRF token, then POST with event=download&selDlFileNo=<id> -- got a real ZIP payload (file-signature verified), ~238.8MB, dated to the latest month-end snapshot. The URL here is the index page, not the download itself -- the real fetch needs a session cookie + CSRF-token POST this script's shared GET-only _get() helper doesn't support. Format left unregistered (no loader) rather than forcing a one-off session/CSRF flow into shared infra.",
    },
    # --- receita_federal ---
    {
        "group": 'receita_federal',
        "table": 'INTL_BR_RFB_CNPJ_EMPRESAS',
        "url": 'https://dados-abertos-rf-cnpj.casadosdados.com.br/arquivos/2026-01-11/Empresas0.zip',
        "format": 'zip_csv',
        "description": "Brazil Receita Federal CNPJ register, Empresas (companies) part 0 of 10. The official dadosabertos.rfb.gov.br host was unreachable from the source census's sandbox (could be a real outage or just that sandbox's network egress -- re-test the official host before relying on this substitute long-term); this uses a well-known public mirror confirmed via a real Apache directory listing matching the official monthly cadence. Confirmed via HEAD: 488,344,875 bytes (~466MB) for this one part -- close to the 500MB cap. Full release is split into 3 table types (Empresas/Estabelecimentos/Socios) x 10 parts each plus ~9 small lookup tables; Estabelecimentos0.zip alone is already ~1.86GB. Only this one part is in this manifest row.",
    },
]

# ---------------------------------------------------------------------------
# Loaders by format
# ---------------------------------------------------------------------------

# Same discipline as the template: every loader below reads the whole
# response into memory (io.BytesIO), capped by MAX_DOWNLOAD_BYTES on the way
# in. Left at 500MB per instruction -- do not raise it here. Several entries
# in this manifest are individually flagged well past that (openFDA bulk
# partitions, PubMed, OpenAlex, ORCID, ICE detention data, DOT NAD, CFPB
# complaints, HMDA nationwide, Companies House PSC, France Sirene, SEC EDGAR
# submissions bulk, SEC ADV part1, Brazil Receita Federal) -- those abort
# cleanly with a clear RuntimeError the moment the response exceeds this
# size, landing in the normal failure summary instead of silently truncating
# or hanging. That is expected, correct behavior for this run, not a bug.
MAX_DOWNLOAD_BYTES = 500_000_000  # 500MB -- unchanged, per instruction


def _get(url: str, timeout: int, max_bytes: int = MAX_DOWNLOAD_BYTES,
         session_warmup_url: str | None = None) -> bytes:
    """Streaming GET with a hard cap on total response size.

    session_warmup_url: if given, GET that URL first in the same
    requests.Session to establish a session cookie the real download needs,
    then GET the real url in that same session. No entry in this manifest
    currently sets this key, but it's kept for parity with the template
    (some future entry in this group may need it, same as
    FED_IHS_SCB_FACILITY did in the template).
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
    """Sanitize a source column name for Snowflake (scoped to this script
    only, same pattern as the template's _sf_col -- does NOT touch the
    shared library-onboarding/ingest.py sanitizer other loaders depend on).
    Maps '>' -> '_GT_' and '<' -> '_LT_' first (both otherwise collapse to
    '_' under the shared sanitizer and can collide), then falls through to
    bulk.sf_col for everything else.
    """
    name = str(name).replace(">", "_GT_").replace("<", "_LT_")
    return bulk.sf_col(name)


def _dedupe_cols(cols: list[str]) -> list[str]:
    """Defensive safety net: disambiguate any exact-duplicate sanitized
    column names with a numeric suffix instead of crashing write_pandas."""
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
    passed, report = bulk.run_quality_gate(
        conn, tbl, tbl, run_id or str(uuid.uuid4()),
        sha256=sha, source_url=source_url)
    if not passed:
        raise RuntimeError(f"{tbl}: quality gate failed -- {report}")
    return len(df)


def _apply_no_header_fallback(df: pd.DataFrame, entry: dict) -> pd.DataFrame:
    """When entry['header'] is None (source confirmed to have no header row)
    and no explicit entry['names'] was given, pandas leaves columns as bare
    integers (0, 1, 2, ...). An unquoted numeric-only Snowflake identifier
    is invalid, so rename to COL_0, COL_1, ... before it ever reaches
    _write(). Entries that don't set "header" are untouched (df comes back
    exactly as pd.read_csv's own header="infer" default produced it)."""
    if entry.get("header", "infer") is None and not entry.get("names"):
        df.columns = [f"COL_{i}" for i in range(len(df.columns))]
    return df


def load_csv(conn, entry: dict, max_rows: int) -> int:
    content = _get(entry["url"], timeout=300,
                   session_warmup_url=entry.get("session_warmup_url"))
    sha, run_id, started = _provenance(content)
    df = pd.read_csv(io.BytesIO(content), dtype=str, nrows=max_rows + 1,
                     low_memory=False, encoding_errors="replace",
                     sep=entry.get("sep", ","),
                     header=entry.get("header", "infer"))
    df = _apply_no_header_fallback(df, entry)
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
                     sep=entry.get("sep", ","),
                     header=entry.get("header", "infer"))
    df = _apply_no_header_fallback(df, entry)
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
    """Load Excel from inside a ZIP. Honors an exact "member" filename
    override instead of guessing by size, same as the template."""
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
            # ONE Excel member -- never largest-wins.
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


def load_csv_gz(conn, entry: dict, max_rows: int) -> int:
    """Load a single gzip-compressed CSV (e.g. NCBI's PMC-ids.csv.gz).

    2026-08-07 addition, FED_NLM_PMC_IDS_XREF: a trivial gzip sibling of
    load_bz2_csv -- same shape, gzip.decompress instead of bz2.decompress.
    Like load_bz2_csv, this does NOT cap the *decompressed* size (only
    _get() caps the compressed download) -- a source whose uncompressed CSV
    balloons past what fits in memory fails at pd.read_csv time, not with
    the same clean "exceeded byte cap" message the download-side cap gives.
    Kept intentionally simple: this format is only worth a real loader
    because it's a one-line variant of an already-proven pattern, not
    because every gzip-wrapped source in this batch got one (PubMed's
    xml_gz and OpenAlex's jsonl_gz were both left unregistered instead,
    since those are multi-file/manifest-driven, not this simple shape).
    """
    import gzip
    content = _get(entry["url"], timeout=600)
    sha, run_id, started = _provenance(content)
    decompressed = gzip.decompress(content)
    df = pd.read_csv(io.BytesIO(decompressed), dtype=str, nrows=max_rows + 1,
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


def load_parquet(conn, entry: dict, max_rows: int) -> int:
    """Load a single Parquet file (e.g. the Richmond DSL redlining-zone
    export on source.coop). 2026-08-07 addition -- a trivial sibling of
    load_csv: fetch, read, cap rows, stamp, write. Needs a pandas parquet
    engine (pyarrow or fastparquet) installed -- not independently
    confirmed present in this environment, same category of dependency
    risk as pyodbc already carries for load_mdb; if it's missing this
    raises ImportError at --run time for the one entry that needs it, not
    at preview/parse time. If the source parquet carries a geometry column
    it lands as opaque bytes/text once cast to str, not real GIS geometry
    -- acceptable for a landing table, same tradeoff this script already
    makes for JSON columns via _flatten_object_columns.
    """
    content = _get(entry["url"], timeout=300)
    sha, run_id, started = _provenance(content)
    df = pd.read_parquet(io.BytesIO(content))
    df = df.astype(str)
    if len(df) > max_rows:
        raise RuntimeError(
            f"{entry['table']}: source has more than max_rows={max_rows:,} rows -- "
            f"refusing to silently truncate. Pass a higher max_rows explicitly.")
    if df.empty:
        return 0
    df = _stamp(df, sha, run_id, started)
    return _write(conn, df, entry["table"], sha=sha, run_id=run_id,
                  source_url=entry["url"])


def load_zip_sqlite(conn, entry: dict, max_rows: int) -> int:
    """Extract tables out of a zipped SQLite database (e.g. ITIS's
    itisSqlite.zip).

    2026-08-07 addition -- same one-table-in/many-tables-out shape as the
    template's load_mdb, but sqlite3 is Python stdlib (no extra ODBC
    driver/DSN dependency like load_mdb's Access driver), so this is a
    lower-risk sibling: extract the .sqlite/.db member to a temp file, open
    it with sqlite3, and load each table named in entry["sqlite_tables"]
    (or, if absent, every non-internal table) into its own landing table.
    """
    import sqlite3
    import tempfile

    content = _get(entry["url"], timeout=600)
    sha, run_id, started = _provenance(content)
    total = 0
    with zipfile.ZipFile(io.BytesIO(content)) as zf:
        # ONE sqlite db or entry["member"] -- never largest-wins.
        db_name = pick_member(zf, pattern=entry.get("member"),
                              suffixes=(".sqlite", ".sqlite3", ".db"))

        with tempfile.TemporaryDirectory() as tmpdir:
            db_path = Path(tmpdir) / "extracted.sqlite"
            with zf.open(db_name) as src, open(db_path, "wb") as dst:
                dst.write(src.read())

            sconn = sqlite3.connect(str(db_path))
            try:
                cur = sconn.cursor()
                cur.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' "
                    "AND name NOT LIKE 'sqlite_%'")
                all_tables = [r[0] for r in cur.fetchall()]
                wanted = entry.get("sqlite_tables") or all_tables
                for tname in wanted:
                    if tname not in all_tables:
                        print(f"      SKIP {tname}: not found in sqlite db "
                              f"(has: {all_tables})")
                        continue
                    tbl = bulk.table_name(entry["table"].rsplit("_", 1)[0], tname)
                    try:
                        sub_cur = sconn.cursor()
                        sub_cur.execute(f'SELECT * FROM "{tname}" LIMIT {max_rows + 1}')
                        cols = [d[0] for d in sub_cur.description]
                        rows = sub_cur.fetchall()
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
                sconn.close()
    return total


def load_mdb(conn, entry: dict, max_rows: int) -> int:
    """Extract tables out of a zipped MS Access (.mdb) database. Carried
    over unchanged from the template for structural parity (FORMAT_LOADERS
    reuse) even though no entry in this manifest currently needs it."""
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
    """Parse a flat XML document into a table. Carried over unchanged from
    the template for structural parity -- this is hardcoded to the UN
    Security Council sanctions list's specific <INDIVIDUALS>/<ENTITIES>
    tag shape. No entry in this manifest reuses it (the one candidate flat
    XML source here, EU Transparency Register, has a different tag shape
    and is deliberately tagged xml_generic/unregistered instead of being
    force-fit through this loader)."""
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
# Tables not listed here fall back to the auto-detect heuristic in
# load_json_api (checks "results" / "data" / "value" / ArcGIS-style
# "features", then gives up and flattens the whole payload as one row).
JSON_API_RECORD_PATH = {
    # openFDA endpoints: {"meta": {...}, "results": [...]}
    "FED_FDA_MAUDE_DEVICE_EVENTS": ("results",),
    "FED_FDA_FAERS_DRUG_EVENTS": ("results",),
    "FED_FDA_DEVICE_EVENT_MAUDE": ("results",),
    "FED_FDA_DRUG_EVENT_FAERS": ("results",),
    "FED_FDA_FOOD_ENFORCEMENT": ("results",),
    "FED_FDA_DEVICE_510K": ("results",),
    "FED_FDA_DEVICE_PMA": ("results",),
    # OpenFEMA convention: payload wraps records under a key matching the
    # dataset name, alongside a "metadata" key.
    "FED_FEMA_HOUSING_ASSISTANCE_OWNERS_V2": ("HousingAssistanceOwners",),
    # Crossref works API: {"status": "ok", "message": {"items": [...], ...}}
    "XC_CROSSREF_WORKS": ("message", "items"),
    # FDIC /banks/sod ({"data": [...], "meta": {...}}) and OSTI.GOV
    # (top-level JSON array) both fall through to the existing heuristic
    # cleanly -- "data" key and list-payload are both already handled, no
    # override needed for FED_FDIC_SOD_BRANCH_DEPOSITS or FED_OSTI_RECORDS.
    #
    # FED_FCC_PUBLICFILES_POLITICAL deliberately has no entry here -- it's a
    # hierarchical folder/file browsing API, not a flat records list (same
    # treatment as FED_USASPENDING_TAS_FILTER_TREE in the template). It
    # falls through to the heuristic and, if that doesn't produce a usable
    # table, fails loudly rather than silently writing garbage.
}


def _flatten_object_columns(df: pd.DataFrame) -> pd.DataFrame:
    """json.dumps() any column still holding list/dict values after
    pd.json_normalize -- Snowflake's write_pandas chokes on raw Python
    list/dict objects in an object-dtype column. Carried over unchanged
    from the template."""
    for col in df.columns:
        if df[col].dtype == object:
            if df[col].apply(lambda v: isinstance(v, (list, dict))).any():
                df[col] = df[col].apply(
                    lambda v: json.dumps(v) if isinstance(v, (list, dict)) else v)
    return df


def load_json_api(conn, entry: dict, max_rows: int) -> int:
    """Fetch a JSON API endpoint and flatten it into a table. Single GET
    per entry -- no built-in pagination, same as the template. Several
    sources in this manifest are naturally paginated or need a POST body;
    those are deliberately tagged with a different, unregistered format
    (json_api_post, async_job_api, oai_pmh_xml) instead of being routed
    through here with a guessed default body/page."""
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
    Carried over unchanged from the template for structural parity -- no
    entry in this manifest currently needs it."""
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
    "arcgis_paginated_json": load_arcgis_paginated_json,
    "xml": load_xml,
    "mdb": load_mdb,
    "csv_gz": load_csv_gz,       # new in this file
    "parquet": load_parquet,     # new in this file
    "zip_sqlite": load_zip_sqlite,  # new in this file
}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> int:
    ap = argparse.ArgumentParser(description="Batch loader for the 2026-08-07 tier1-remaining recon sweep")
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
        # (url, sheet) fingerprints the actual source being fetched -- same
        # dedup key as the template. sheet is part of the key so two
        # legitimately-different entries pulling different sheets/members
        # out of the same zip (none of those happen to collide in this
        # manifest, but the key shape is kept for parity) aren't wrongly
        # flagged as duplicates of each other.
        source_key = (entry["url"], entry.get("sheet"))
        if entry["table"] in loaded:
            print(f"  SKIP {entry['table']} (exists)")
        elif entry["table"] in seen_this_run:
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
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
