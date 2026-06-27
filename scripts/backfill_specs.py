"""AUTO-GENERATED backfill specs (2026-06-26) from the verify-backfill-specs workflow
(wf_b5553854). Each URL + key columns were live-verified (HTTP 200 + header read) by a
per-source agent. Consumed by scripts/bridge_fuel_load.py alongside bridge_fuel_specs.py.
NOTE: opensanctions/epa/fec carry keys the connect tagger does not yet know (FRS_ID/FEC_*/
buried IMO) -- they LAND fine; auto-connect on those keys needs the Step-K tagger work.
"""

SPECS = [{'source_id': 'fed_cms_part_d_prescribers',
  'name': 'Medicare Part D Prescribers - by Provider',
  'publisher': 'Centers for Medicare & Medicaid Services (CMS)',
  'url': 'https://data.cms.gov/provider-summary-by-type-of-service/medicare-part-d-prescribers/medicare-part-d-prescribers-by-provider',
  'download_url': 'https://data.cms.gov/sites/default/files/2026-05/e9cd7dfb-9c27-4b3f-8f5d-2454091303ee/MUP_DPR_RY26_P04_V10_DY24_NPI.csv',
  'kind': 'csv',
  'csv_opts': {'dtype': 'str'},
  'chunked': True,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'PRSCRBR_NPI', 'as': 'NPI'}],
  'join_keys': 'NPI',
  'category': 'health_medicine',
  'subcategory': 'medicare_part_d',
  'jurisdiction': 'fed',
  'unit_of_observation': 'one row = one Part D prescriber (NPI) summarized across all drugs for '
                         'the data year',
  'update_cadence': 'annual',
  'volume': '~1.1M rows (one per prescriber), ~1+ GB CSV',
  'accountability_relevance': 'Prescriber-level Part D drug prescribing: opioid prescribing rates, '
                              'brand vs generic, total drug cost, beneficiary demographics. Joins '
                              'on NPI to NPPES (provider identity) and LEIE (OIG exclusions) to '
                              'flag debarred-but-prescribing providers and opioid overprescribers.',
  'priority_tier': 'high',
  'notes': 'Data year 2024 (12/2024), release RY26, modified 2026-05-21 -- latest available. '
           'Standard comma-delimited CSV, real header row, UTF-8, no quirks. NPI col is '
           'PRSCRBR_NPI (first column, fully populated 10-digit NPIs). dtype:str keeps NPIs as '
           "strings so leading-zero / scientific-notation corruption can't happen. Suppressed "
           "cells use *_Sprsn_Flag columns. Sibling 'by Provider and Drug' dataset (NPIBN, ~25M "
           'rows) is a separate source; this is the by-Provider rollup. downloadURL resolved from '
           "https://data.cms.gov/data.json (dataset 'Medicare Part D Prescribers - by Provider', "
           '2024-12-01 CSV distribution); verified HTTP 200 text/csv via curl. URLs are dated-path '
           'and rotate each annual release -- re-resolve from data.json when refreshing.'},
 {'source_id': 'fed_cms_medicare_provider',
  'name': 'Medicare Physician & Other Practitioners - by Provider',
  'publisher': 'Centers for Medicare & Medicaid Services (CMS)',
  'url': 'https://data.cms.gov/provider-summary-by-type-of-service/medicare-physician-other-practitioners/medicare-physician-other-practitioners-by-provider',
  'download_url': 'https://data.cms.gov/sites/default/files/2026-05/7323ba02-52e7-4a86-b2ce-ad210c25d9aa/MUP_PHY_R26_P05_V10_D24_Prov.csv',
  'kind': 'csv',
  'csv_opts': {'encoding': 'latin-1', 'dtype': 'str'},
  'chunked': True,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'Rndrng_NPI', 'as': 'NPI'}],
  'join_keys': 'NPI',
  'category': 'health_medicine',
  'subcategory': 'medicare_provider_payments',
  'jurisdiction': 'fed',
  'unit_of_observation': 'one row = one rendering provider (NPI) for a given calendar year',
  'update_cadence': 'annual',
  'volume': '~1.1M rows per year (~600MB CSV); chunked streaming load',
  'accountability_relevance': 'What Medicare Part B paid each individual provider (NPI): total '
                              'submitted charges, allowed amounts, payments, standardized amounts, '
                              'plus drug vs medical breakdown and beneficiary demographics. Ties '
                              'provider identity to federal payment flows -- joins to NPPES, Open '
                              'Payments, exclusions (LEIE), and the by-Provider-and-Service '
                              'detail.',
  'priority_tier': '1',
  'notes': 'Latest release = R26 P05 V10 D24 (data year 2023, published 2026-05-11). Clean '
           "comma-separated CSV with header row. NPI column is exactly 'Rndrng_NPI' "
           '(case-sensitive), populated with 10-digit NPIs (sample: 1003000126). No content-length '
           '(chunked transfer-encoding) so row count not from header, but CMS by-Provider files '
           'run ~1.1M rows -> chunked:true required. dtype:str forces all-TEXT mirror; '
           'encoding:latin-1 guards against accented provider names breaking mid-stream chunk '
           "decode. Resolved via https://data.cms.gov/data.json (dataset 'Medicare Physician & "
           "Other Practitioners - by Provider', first/newest CSV distribution). URL verified live: "
           'HTTP 200, content-type text/csv, last-modified Mon 11 May 2026.'},
 {'source_id': 'fed_irs_eo_bmf',
  'name': 'IRS Exempt Organizations Business Master File (EO BMF) - Region 3 (Gulf Coast & Pacific '
          'Coast)',
  'publisher': 'Internal Revenue Service (IRS), Statistics of Income (SOI)',
  'url': 'https://www.irs.gov/charities-non-profits/exempt-organizations-business-master-file-extract-eo-bmf',
  'download_url': 'https://www.irs.gov/pub/irs-soi/eo3.csv',
  'kind': 'csv',
  'csv_opts': {'dtype': 'str'},
  'chunked': True,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'EIN', 'as': 'EIN'}],
  'join_keys': 'EIN',
  'category': 'money_finance',
  'subcategory': 'nonprofits_exempt_orgs',
  'jurisdiction': 'fed',
  'unit_of_observation': 'one row = one IRS-recognized tax-exempt organization (EIN)',
  'update_cadence': 'monthly',
  'volume': 'eo3.csv ~964K rows / ~166MB (largest single regional file); full BMF ~1.97M records '
            'is split across eo1-eo4 + eo_xx + eo_pr + per-state files',
  'accountability_relevance': 'high',
  'priority_tier': '1',
  'notes': 'EO BMF is the master registry of every active IRS-recognized tax-exempt org. Bulk '
           'extract is split into REGIONAL files, NOT a single combined file: eo1.csv (Northeast, '
           '~280K rows), eo2.csv (Mid-Atlantic & Great Lakes, ~725K rows), eo3.csv (Gulf Coast & '
           'Pacific Coast, ~964K rows -- LARGEST), eo4.csv (all other areas, ~5K rows), plus '
           'eo_xx.csv (International) and eo_pr.csv (Puerto Rico). The loader does ONE file per '
           'spec, so this spec loads eo3 (the largest); full coverage requires 4-6 separate loads '
           'under variant source_ids or sequential download_url swaps. All files share an '
           "IDENTICAL 28-column header. First column is exactly 'EIN' (case-sensitive), "
           'zero-padded to 9 digits and stored as TEXT (e.g. 000260049) -- verified 0 empty in '
           '1000-row sample. Standard comma sep, default UTF-8, minimal quoting. csv_opts forces '
           'dtype=str to preserve EIN/ZIP/code leading zeros. EIN is a STEEL join key (links to '
           'IRS 990 e-file, Form 990 financials, GuideStar/Candid, FEC, USAspending recipients). '
           'Files updated monthly (last-modified 2026-06-08).'},
 {'source_id': 'fed_irs_revocation',
  'name': 'IRS Automatic Revocation of Exemption List (Auto-Revocation)',
  'publisher': 'Internal Revenue Service (IRS) - Tax Exempt Organization Search (TEOS)',
  'url': 'https://www.irs.gov/charities-non-profits/tax-exempt-organization-search-bulk-data-downloads',
  'download_url': 'https://apps.irs.gov/pub/epostcard/data-download-revocation.zip',
  'kind': 'zip_csv',
  'member': 'data-download-revocation\\.txt',
  'csv_opts': {'sep': '|',
               'header': None,
               'names': ['EIN',
                         'LEGAL_NAME',
                         'DBA_NAME',
                         'ORG_ADDRESS',
                         'CITY',
                         'STATE',
                         'ZIP_CODE',
                         'COUNTRY',
                         'EXEMPTION_TYPE',
                         'REVOCATION_DATE',
                         'REVOCATION_POSTING_DATE',
                         'EXEMPTION_REINSTATEMENT_DATE'],
               'skip_blank_lines': True},
  'chunked': True,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'EIN', 'as': 'EIN'}],
  'join_keys': 'EIN',
  'category': 'nonprofits',
  'subcategory': 'tax_exempt_status',
  'jurisdiction': 'US',
  'unit_of_observation': 'one row = one organization whose 501(c) tax-exempt status was '
                         'automatically revoked (for failing to file Form 990/990-EZ/990-PF/990-N '
                         'for 3 consecutive years)',
  'update_cadence': 'monthly',
  'volume': '~1.2M rows (1,206,628 data rows; ~46MB zip / ~144MB uncompressed pipe-delimited .txt)',
  'accountability_relevance': 'FLAG list. Powers the revoked-but-funded detector: an org that lost '
                              'tax-exempt status but still appears as a grantee/recipient in '
                              'funding data (federal grants, foundation 990 grant tables, '
                              'contracts) is a red flag. Joins on EIN to the nonprofit/funding '
                              'spine (IRS EO BMF, Form 990, USASpending, grants).',
  'priority_tier': '1',
  'notes': 'VERIFIED 2026-06-26 (file last updated 2026-06-16). Zip has ONE member '
           'data-download-revocation.txt. HEADERLESS, pipe-delimited (|), ASCII/CRLF. File begins '
           'with 2 BLANK CRLF lines + a trailing blank line -> skip_blank_lines:true drops them '
           "(loader default keep_default_na=False keeps empty fields as ''). 12 columns, "
           'consistent across all 1,206,628 data rows. EIN is field 1: zero-padded 9-digit string '
           '(e.g. 000003154) -> dtype=str (loader default) preserves leading zeros, essential for '
           'the EIN join. Dates are DD-MMM-YYYY (e.g. 15-NOV-2017); cast in staging. '
           'EXEMPTION_REINSTATEMENT_DATE often blank (org never reinstated). chunked:true required '
           'for 1.2M rows; low_memory(default) is ignored under chunksize - no conflict (tested). '
           'EIN is a tagger-known canonical -> no new key infra. New spec (not yet in '
           'bridge_fuel_specs.py).'},
 {'source_id': 'fed_sec_edgar_insiders',
  'name': 'SEC Form 3/4/5 Insider Transactions Data Sets (SUBMISSION master table)',
  'publisher': 'U.S. Securities and Exchange Commission (SEC)',
  'url': 'https://www.sec.gov/data-research/sec-markets-data/insider-transactions-data-sets',
  'download_url': 'https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2026q1_form345.zip',
  'kind': 'zip_csv',
  'member': '^SUBMISSION\\.tsv$',
  'csv_opts': {'sep': '\t', 'dtype': 'str', 'keep_default_na': False},
  'chunked': False,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'ISSUERCIK', 'as': 'CIK'}],
  'join_keys': 'CIK (issuer, ISSUERCIK), ACCESSION_NUMBER, ticker (ISSUERTRADINGSYMBOL)',
  'category': 'money_finance',
  'subcategory': 'securities_insider_transactions',
  'jurisdiction': 'fed',
  'unit_of_observation': 'one Form 3/4/5 ownership filing (keyed on ACCESSION_NUMBER)',
  'update_cadence': 'quarterly',
  'volume': '~69K filings per quarter (SUBMISSION.tsv ~7.5MB uncompressed); full ZIP ~14MB / ~91MB '
            'unzipped across 8 TSVs',
  'accountability_relevance': 'Insider buying/selling by corporate officers, directors, and 10% '
                              'owners (Section 16). Joins to SEC company universe via issuer CIK; '
                              'surfaces self-dealing, timed trades, and ownership concentration.',
  'priority_tier': 'high',
  'notes': 'Live URL pattern verified via curl (HTTP 200): '
           'https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/<YYYY>q<N>_form345.zip '
           '(NOT the /dera/ path, which 404s). Latest available quarter as of 2026-06-26 is 2026q1 '
           '(13.9MB). ZIP holds 8 TSVs; we land SUBMISSION.tsv (the filing master, one row per '
           'filing) because it carries the issuer CIK (ISSUERCIK, 10-digit zero-padded, 100% '
           'populated). member regex pinned to ^SUBMISSION\\.tsv$ so the loader does NOT grab the '
           '44MB FOOTNOTES.tsv via largest-CSV fallback. Tab-separated, standard UTF-8. ~69K rows '
           '-> no chunking. SEC requires a real User-Agent (loader sets one). Note: SEC re-posts '
           "each quarter's ZIP as late filings accrue, so the SHA-256 can change between runs -> "
           'the SHA-skip will correctly reload. Related members in the same ZIP that could become '
           'separate sources: REPORTINGOWNER.tsv (insider CIK = RPTOWNERCIK), NONDERIV_TRANS.tsv / '
           'DERIV_TRANS.tsv (actual transactions, join back on ACCESSION_NUMBER).'},
 {'source_id': 'fed_sec_edgar_financials',
  'name': 'SEC Financial Statement Data Sets',
  'publisher': 'U.S. Securities and Exchange Commission (DERA)',
  'url': 'https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets',
  'download_url': 'https://www.sec.gov/files/dera/data/financial-statement-data-sets/2024q4.zip',
  'kind': 'zip_csv',
  'member': '^sub\\.txt$',
  'csv_opts': {'sep': '\t', 'dtype': 'str', 'keep_default_na': False},
  'chunked': False,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'cik', 'as': 'CIK'},
               {'col': 'ein', 'as': 'EIN'},
               {'col': 'sic', 'as': 'SIC'}],
  'join_keys': 'CIK, EIN, SIC, adsh (accession number)',
  'category': 'money_finance',
  'subcategory': 'corporate_financial_reporting',
  'jurisdiction': 'federal',
  'unit_of_observation': 'One row = one XBRL financial-report submission (filing) by a registrant '
                         'in the quarter; PK = adsh (EDGAR accession number).',
  'update_cadence': 'quarterly',
  'volume': '~6,500 filings per quarterly sub.txt member (this 2024q4 ZIP is ~123 MB total; '
            'sub.txt itself is ~2 MB / 6,491 rows). Full ZIP also holds num.txt ~527MB, pre.txt '
            '~90MB, tag.txt ~18MB which are NOT loaded by this spec.',
  'accountability_relevance': 'Structured financial-statement line items from every public company '
                              '10-K/10-Q. CIK joins to the rest of the SEC EDGAR universe; EIN '
                              'bridges to IRS/nonprofit/business-entity data; SIC classifies '
                              'industry. Core spine for following corporate money.',
  'priority_tier': '1',
  'notes': 'VERIFIED LIVE: curl HTTP 200, 122,932,548 bytes, last-modified 2025-01-16. Member '
           'sub.txt = tab-separated, 36 cols, header row 1, 6,491 data rows -> chunked:false. '
           'Exact key columns (lowercase, case-sensitive): cik, ein, sic; adsh is the unique PK '
           "per SEC readme. ein sometimes carries placeholder '000000000' for filers without a "
           'published EIN -- keep_default_na:false preserves it as text rather than NaN. *** '
           "LOADER BLOCKER: SEC's Akamai/nginx edge returns HTTP 403 for the loader's hardcoded UA "
           "'Mozilla/5.0 (ripple-bridge-fuel-loader)'. SEC fair-access policy REQUIRES a "
           "User-Agent containing a real contact (name + email), e.g. 'Ripple Library "
           "admin@example.com'. Confirmed: Mozilla UA -> 403, contact-email UA -> 200. The "
           "loader's UA constant in scripts/bridge_fuel_load.py (line 64) must be changed to an "
           'SEC-compliant contact string before this source will load, OR add per-spec header '
           'override. *** MULTI-TABLE SHAPE: the quarterly ZIP is a 4-table relational set -- '
           'sub.txt (submissions/filers, carries CIK+EIN+SIC), num.txt (numeric facts, keyed '
           'adsh+tag+version), pre.txt (presentation), tag.txt (tag dictionary). This spec loads '
           "sub.txt only (the entity spine). num/pre/tag don't carry CIK/EIN directly; they join "
           'back via adsh. To onboard the financial line items, add separate source_ids per '
           'member. *** HISTORICAL: same URL pattern back to 2009q1 '
           '(https://www.sec.gov/files/dera/data/financial-statement-data-sets/<YYYY>q<N>.zip) for '
           'backfill.'},
 {'source_id': 'intl_opensanctions',
  'name': 'OpenSanctions Consolidated Sanctions (Targets, Simplified CSV)',
  'publisher': 'OpenSanctions',
  'url': 'https://www.opensanctions.org/datasets/sanctions/',
  'download_url': 'https://data.opensanctions.org/datasets/latest/sanctions/targets.simple.csv',
  'kind': 'csv',
  'csv_opts': {'dtype': 'str', 'keep_default_na': False},
  'chunked': False,
  'chunk_rows': 200000,
  'join_keys': 'NAME + COUNTRY (clean columns: name, countries[ISO2]); IMO/MMSI for vessels exist '
               'but are buried unlabeled in the semicolon-joined `identifiers` blob -> NOT '
               'directly aliasable',
  'category': 'sanctions_enforcement',
  'subcategory': 'consolidated_sanctions_lists',
  'jurisdiction': 'intl',
  'unit_of_observation': 'one row = one sanctioned/listed target (Person, Organization, Company, '
                         'Vessel, etc.) consolidated across all source sanctions lists',
  'update_cadence': 'daily',
  'volume': '~66 MB, ~80k target rows (full FtM entity_count incl. sub-entities is 287,144; simple '
            'targets export is the deduped target subset)',
  'accountability_relevance': 'Core sanctions/PEP screening spine. Consolidates OFAC SDN, EU, UK, '
                              'UN, Ukraine NSDC and ~270 source lists into one entity set. Joins '
                              'to maritime (vessel IMO/MMSI, once extracted), corporate, and '
                              'money-finance entities by name+country.',
  'priority_tier': '1',
  'notes': 'VERIFIED LIVE: curl -sI returned HTTP 200, content-type text/csv, content-length '
           '66,250,177 (~66 MB), last-modified daily. Stable alias path '
           '/datasets/latest/sanctions/targets.simple.csv is the always-current export (index.json '
           'also exposes a versioned artifact URL under /artifacts/sanctions/<ts>-onf/ but the '
           'latest alias is correct for a recurring loader). Standard comma-separated, UTF-8, has '
           'header row, RFC4180 quoting (fields contain Cyrillic, embedded commas/semicolons, '
           'doubled-quote escaping) -> default pandas read_csv handles it; passing dtype=str + '
           'keep_default_na=false preserves the all-TEXT mirror and stops pandas turning '
           "blank/'NA' into NaN. ~80k rows -> chunking NOT needed (set chunked=false; chunk_rows "
           'kept as a safe default if flipped on). KEY-INFRA GAP: clean join columns are `name` '
           'and `countries`(ISO2), but NAME and COUNTRY are NOT canonicals the tagger knows (it '
           'only knows NPI EIN CIK UEI DUNS LEI CCN IMO MMSI NAICS SIC), so key_cols is empty and '
           'needs_key_infra=true. IMO/MMSI vessel IDs DO exist for Vessel-schema rows but live '
           'unlabeled inside the semicolon-joined `identifiers` column (e.g. '
           "'1187746408761;7725491052') -> cannot be aliased as a clean IMO/MMSI column without a "
           'downstream parse/extract step. Recommend: land as-is now; add NAME+COUNTRY join infra '
           '+ an identifiers-blob IMO/MMSI extractor in staging later.'},
 {'source_id': 'fed_epa_echo',
  'name': 'EPA ECHO Exporter (Facility-level Enforcement & Compliance)',
  'publisher': 'U.S. Environmental Protection Agency',
  'url': 'https://echo.epa.gov/tools/data-downloads',
  'download_url': 'https://echo.epa.gov/files/echodownloads/echo_exporter.zip',
  'kind': 'zip_csv',
  'member': 'ECHO_EXPORTER\\.csv',
  'csv_opts': {'encoding': 'latin-1', 'dtype': 'str'},
  'chunked': True,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'REGISTRY_ID', 'as': 'FRS_ID'}],
  'join_keys': 'FRS_ID (REGISTRY_ID, FRS facility registry id), FAC_FIPS_CODE (state+county FIPS), '
               'FAC_LAT/FAC_LONG (lat/lon), FAC_NAICS_CODES (multi-valued NAICS, not a clean '
               'single key)',
  'category': 'environment',
  'subcategory': 'pollution_enforcement_compliance',
  'jurisdiction': 'fed',
  'unit_of_observation': 'one EPA-regulated facility (FRS REGISTRY_ID)',
  'update_cadence': 'weekly',
  'volume': '~1.5M facilities, 133 columns, ~425MB zip (~445,905,683 bytes), last-modified '
            '2026-06-20',
  'accountability_relevance': 'Core polluter-accountability spine: aggregates 5 years of '
                              'compliance + enforcement (inspections, formal actions, penalties, '
                              'significant-noncompliance flags) and pollutant releases (TRI/GHG) '
                              'to the facility level across CAA/CWA/RCRA/SDWA programs. '
                              'REGISTRY_ID (FRS_ID) links to all other ECHO/FRS program files; '
                              'FIPS + lat/lon enable geographic/environmental-justice joins.',
  'priority_tier': '1',
  'notes': 'VERIFIED LIVE: curl -sI returned HTTP 200, content-type application/zip, '
           'content-length 445905683, last-modified Sat 20 Jun 2026. Zip local file header member '
           '= ECHO_EXPORTER.csv (single CSV, deflate). Decompressed + pandas-parsed the start of '
           'the real file: 133 columns, comma-separated, all fields double-quoted in source '
           '(pandas default quotechar handles it -> clean unquoted column names). REGISTRY_ID '
           'populated (~0.4% null in sample), 12-digit FRS IDs e.g. 110070259655. KEY INFRA: '
           'REGISTRY_ID = FRS_ID (Facility Registry Service id) -> tagger does NOT know FRS_ID, so '
           'needs_key_infra=true; column still mapped. NO EIN COLUMN EXISTS in this file (task '
           "hint 'EIN' was wrong). NAICS present as FAC_NAICS_CODES but SPACE-DELIMITED "
           "MULTI-VALUED (e.g. '211130 211120') -> deliberately NOT mapped as a key_col (would "
           'mislead the single-value join tagger); CAA_NAICS/CWA_NAICS/RCRA_NAICS are also '
           'multi-valued. encoding latin-1 set defensively for EPA bulk files. chunked at 200k due '
           'to ~1.5M rows. Column names confirmed against official metadata: '
           'https://echo.epa.gov/system/files/echo_exporter_columns_7-16-2025_0.xlsx (last updated '
           '07/16/2025).'},
 {'source_id': 'fed_fec_bulk',
  'name': 'FEC Bulk Data - Committee Master (2024)',
  'publisher': 'Federal Election Commission (FEC)',
  'url': 'https://www.fec.gov/data/browse-data/?tab=bulk-data',
  'download_url': 'https://www.fec.gov/files/bulk-downloads/2024/cm24.zip',
  'kind': 'zip_csv',
  'member': 'cm\\.txt',
  'csv_opts': {'sep': '|',
               'header': None,
               'dtype': 'str',
               'names': ['CMTE_ID',
                         'CMTE_NM',
                         'TRES_NM',
                         'CMTE_ST1',
                         'CMTE_ST2',
                         'CMTE_CITY',
                         'CMTE_ST',
                         'CMTE_ZIP',
                         'CMTE_DSGN',
                         'CMTE_TP',
                         'CMTE_PTY_AFFILIATION',
                         'CMTE_FILING_FREQ',
                         'ORG_TP',
                         'CONNECTED_ORG_NM',
                         'CAND_ID']},
  'chunked': False,
  'chunk_rows': 0,
  'key_cols': [{'col': 'CMTE_ID', 'as': 'FEC_CMTE_ID'}, {'col': 'CAND_ID', 'as': 'FEC_CAND_ID'}],
  'join_keys': 'FEC_CMTE_ID, FEC_CAND_ID, NAME (CMTE_NM)',
  'category': 'money_finance',
  'subcategory': 'campaign_finance',
  'jurisdiction': 'fed',
  'unit_of_observation': 'one registered political committee (PAC/party/candidate committee)',
  'update_cadence': 'daily (FEC refreshes bulk files nightly during the cycle)',
  'volume': '~20,938 rows; ~2.5MB uncompressed',
  'accountability_relevance': 'Campaign finance entity spine: maps every registered federal '
                              'political committee (PACs, party committees, candidate committees) '
                              'to its treasurer, connected organization, and the candidate it '
                              'supports. Core for tracing money-in-politics networks and following '
                              'dark-money/PAC flows.',
  'priority_tier': 'high',
  'notes': 'HEADERLESS pipe-delimited file - csv_opts MUST include header:null + names from FEC '
           'committee master file description. Column 0 (CMTE_ID) is the FEC_CMTE_ID; column 14 '
           '(CAND_ID) carries FEC_CAND_ID (sparse - only candidate committees populate it). Both '
           'keys need new key infra (not in tagger canonical list). zip member is cm.txt (regex '
           'cm\\.txt avoids matching cn.txt). SIBLING FILE: candidate master at '
           'https://www.fec.gov/files/bulk-downloads/2024/cn24.zip (member cn.txt, ~9,799 rows, '
           'headerless pipe, cols: '
           'CAND_ID|CAND_NAME|CAND_PTY_AFFILIATION|CAND_ELECTION_YR|CAND_OFFICE_ST|CAND_OFFICE|CAND_OFFICE_DISTRICT|CAND_ICI|CAND_STATUS|CAND_PCC|CAND_ST1|CAND_ST2|CAND_CITY|CAND_ST|CAND_ZIP) '
           '- needs its OWN source_id (e.g. fed_fec_candidates) since it has a different schema '
           'and cannot share the FED_FEC_BULK landing table. URL is for 2024 cycle; FEC publishes '
           'per-cycle zips (pattern: /bulk-downloads/<YYYY>/cm<YY>.zip).'},
 {'source_id': 'fed_cms_open_payments_2023',
  'name': 'CMS Open Payments PY2023 - General Payments (Detailed)',
  'publisher': 'Centers for Medicare & Medicaid Services (CMS)',
  'url': 'https://openpaymentsdata.cms.gov/dataset/fb3a65aa-c901-4a38-a813-b04b00dfa2a9',
  'download_url': 'https://download.cms.gov/openpayments/PGYR2023_P01232026_01102026/OP_DTL_GNRL_PGYR2023_P01232026_01102026.csv',
  'kind': 'csv',
  'csv_opts': {'dtype': 'str'},
  'chunked': True,
  'chunk_rows': 200000,
  'key_cols': [{'col': 'Covered_Recipient_NPI', 'as': 'NPI'},
               {'col': 'Teaching_Hospital_CCN', 'as': 'CCN'}],
  'join_keys': 'NPI, CCN',
  'category': 'health_medicine',
  'subcategory': 'industry_payments',
  'jurisdiction': 'fed',
  'unit_of_observation': 'One row = one general (non-research) payment / transfer of value from a '
                         'drug/device manufacturer or GPO to a covered recipient (physician, '
                         'non-physician practitioner, or teaching hospital) in reporting year 2023',
  'update_cadence': 'annual',
  'volume': '~15M rows (full-year general payments detail; current publication P01232026_01102026)',
  'accountability_relevance': 'Core industry-to-prescriber money trail; adds PY2023 to the '
                              'NPI-money spine (joins to NPPES providers, Medicare Part D '
                              'prescribing, etc.). Maps pharma/device financial influence on '
                              'individual clinicians and teaching hospitals.',
  'priority_tier': '1',
  'notes': 'Resolved via openpaymentsdata.cms.gov DKAN metastore '
           '(api/1/metastore/schemas/dataset/items?show-reference-ids), dataset identifier '
           "fb3a65aa-c901-4a38-a813-b04b00dfa2a9, title '2023 General Payment Data'. download_url "
           'verified live HTTP 200 (Akamai NetStorage, last-modified 2026-01-10, '
           'content-disposition attachment). Standard comma CSV with quoted fields - parses with '
           'pandas defaults; dtype=str keeps the all-TEXT mirror. Key cols verified case-sensitive '
           'against the live header: Covered_Recipient_NPI (well-populated for '
           'physician/non-physician recipient rows) and Teaching_Hospital_CCN (populated only on '
           'teaching-hospital recipient rows, blank when NPI is present - each row carries one or '
           'the other). ~15M rows so chunked:true. Both NPI and CCN are tagger-known canonicals '
           '(no new key infra needed). NDC drug codes also present '
           '(Associated_Drug_or_Biological_NDC_1..5) but not in the canonical key set. URL embeds '
           'a publication-date stamp (PGYR2023_P01232026_01102026) - if CMS re-publishes PY2023, '
           're-resolve via the metastore before reload.'}]
