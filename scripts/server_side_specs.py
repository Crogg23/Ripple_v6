"""Server-side bulk-load specs (consumed by scripts/server_side_load.py).

The GB-scale sources that stall when pulled through the laptop, so Snowflake
fetches them directly (see infra/ddl/08_bulk_ingest.sql). A plain list `SPECS`
of dicts -- no import of the loader (avoids a cycle).

Required per spec: source_id, url. Optional:
    kind            'csv' (default) | 'zip'
    member_pattern  regex to pick the zip member; '' => largest member
    delimiter       field delimiter (default ',')
    has_header      True (default) | False -> synthesize C1..CN column names
    resolver        {'url','type':'json'|'regex','path'} -> resolve the real, rotating
                    download link first (e.g. GLEIF's metadata API). The RESOLVED
                    host must also be on RIPPLE_BULK_EGRESS.
    plus any SOURCE_REGISTRY facet fields consumed by bridge_fuel_load._register
    (name, publisher, description, join_keys, accountability_relevance, ...).

Host must be listed in the RIPPLE_BULK_EGRESS network rule, and the URL must be
served DIRECTLY (a cross-host 302 -- e.g. FEC -> S3 -- is blocked by egress scope).
"""

SPECS = [
    {
        "source_id": "FED_CFPB_COMPLAINTS",
        "name": "CFPB Consumer Complaint Database (full bulk)",
        "url": "https://files.consumerfinance.gov/ccdb/complaints.csv.zip",
        "kind": "zip",
        "member_pattern": r"complaints\.csv$",
        "delimiter": ",",
        "publisher": "Consumer Financial Protection Bureau",
        "description": (
            "Every consumer complaint the CFPB sent to a company for response, "
            "published after the company responds or after 15 days. One row per complaint."),
        "jurisdiction": "US",
        "category": "consumer_finance",
        "subcategory": "complaints",
        "unit_of_observation": "one row = one consumer complaint",
        "geographic_scope": "United States",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "daily",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "Company; State; ZIP code",
        "accountability_relevance": (
            "Direct record of consumer financial harm by company/product -- the "
            "who-got-hurt receipts for banks, debt collectors, credit bureaus."),
        "priority_tier": "2",
        "notes": "Server-side bulk load (scripts/server_side_load.py); 1.4 GB zip fetched cloud-to-cloud.",
    },
    {
        "source_id": "INTL_GLEIF",
        "name": "GLEIF LEI2 Golden Copy (full CSV)",
        # The download link rotates each publish, so resolve it from the metadata API.
        # 'url' is a human-facing fallback; the resolver returns the real .csv.zip link.
        "url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/lei2/latest",
        "resolver": {
            "url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/lei2/latest",
            "type": "json",
            "path": "data.full_file.csv.url",
        },
        "kind": "zip",
        "member_pattern": r"\.csv$",
        "delimiter": ",",
        "publisher": "Global Legal Entity Identifier Foundation (GLEIF)",
        "description": (
            "The LEI golden copy: every Legal Entity Identifier and its registration + "
            "entity reference data. The global company-identity spine. One row per LEI."),
        "jurisdiction": "GLOBAL",
        "category": "entity_registry",
        "subcategory": "legal_entity_identifier",
        "unit_of_observation": "one row = one LEI",
        "geographic_scope": "Global",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "daily",
        "license_terms": "CC0 (GLEIF public)",
        "join_keys": "LEI; (entity name/address)",
        "accountability_relevance": (
            "The cross-border company-identity backbone -- links entities across "
            "jurisdictions and to their parents (the ownership graph)."),
        "priority_tier": "1",
        "notes": "Server-side bulk load; resolver hop (metadata API -> rotating .csv.zip link).",
    },
    {
        "source_id": "FED_IRS_EO_PR",
        "name": "IRS Exempt Organizations BMF - Puerto Rico",
        "url": "https://www.irs.gov/pub/irs-soi/eo_pr.csv",
        "kind": "csv",
        "delimiter": ",",
        "publisher": "Internal Revenue Service",
        "description": "IRS Exempt Organizations Business Master File extract, Puerto Rico region. One row per exempt org.",
        "jurisdiction": "US",
        "category": "nonprofits",
        "subcategory": "exempt_organizations",
        "unit_of_observation": "one row = one exempt organization",
        "geographic_scope": "Puerto Rico",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "monthly",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "EIN",
        "accountability_relevance": "Tax-exempt org registry (EIN spine) for Puerto Rico.",
        "priority_tier": "3",
        "notes": "Small plain-CSV source; also the server-side refresh test fixture.",
    },
    {
        "source_id": "FED_CMS_OPEN_PAYMENTS_GNRL",
        "name": "CMS Open Payments - General Payments (full program year)",
        # Direct CSV on download.cms.gov (already on RIPPLE_BULK_EGRESS). The fetch proc
        # gzips on the fly (raw General file is ~10GB and overflows the /tmp sandbox; its
        # .gz ~2GB fits). Publication suffix (PGYR<year>_P<pubdate>_<refresh>) rotates.
        "url": "https://download.cms.gov/openpayments/PGYR2024_P06302025_06162025/OP_DTL_GNRL_PGYR2024_P06302025_06162025.csv",
        "kind": "csv",
        "delimiter": ",",
        "publisher": "Centers for Medicare & Medicaid Services",
        "description": (
            "Every industry general payment or transfer of value to physicians, "
            "non-physician practitioners, and teaching hospitals reported under the "
            "Sunshine Act. One row per reported payment."),
        "jurisdiction": "US",
        "category": "healthcare",
        "subcategory": "industry_payments",
        "unit_of_observation": "one row = one reported general payment",
        "geographic_scope": "United States",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "annual",
        "license_terms": "Public domain (US Gov)",
        "join_keys": (
            "Covered_Recipient_NPI; Covered_Recipient_Profile_ID; "
            "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID; Record_ID"),
        "accountability_relevance": (
            "The who-paid-whom receipts for medical conflicts of interest -- links "
            "drug/device makers to the doctors and hospitals they pay."),
        "priority_tier": "1",
        "notes": (
            "Server-side bulk load; direct General-Payments CSV (PY2024), gzipped on the "
            "fly by the fetch proc (raw ~10GB overflows /tmp; .gz fits). Research/Ownership "
            "files publish as sibling OP_DTL_RSRCH_/OP_DTL_OWNRSHP_ CSVs -- add later."),
    },
    {
        "source_id": "FED_CMS_PARTD_PRESCRIBER_DRUG",
        "name": "CMS Medicare Part D Prescribers - by Provider and Drug (DY2022)",
        # Direct CSV on data.cms.gov (already on RIPPLE_BULK_EGRESS). The hashed path +
        # data year rotate per release; a newer data year (e.g. RY25/DY23,
        # MUP_DPR_RY25_P04_V10_DY23_NPIBN.csv) exists -- bump the URL at run time
        # (confirm the current download link with scripts/intake.py first).
        "url": "https://data.cms.gov/sites/default/files/2024-05/18f82097-61a6-4889-9941-9a0b6ad7523c/MUP_DPR_RY24_P04_V10_DY22_NPIBN.csv",
        "kind": "csv",
        "delimiter": ",",
        "publisher": "Centers for Medicare & Medicaid Services",
        "description": (
            "Prescription drugs prescribed to Medicare Part D beneficiaries, aggregated "
            "by prescriber (NPI) and drug (brand + generic). One row per prescriber-drug."),
        "jurisdiction": "US",
        "category": "healthcare",
        "subcategory": "prescribing",
        "unit_of_observation": "one row = one prescriber x drug",
        "geographic_scope": "United States",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "annual",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "Prscrbr_NPI; Brnd_Name; Gnrc_Name",
        "accountability_relevance": (
            "Prescribing volume + drug cost per provider -- pairs with Open Payments to "
            "test whether industry money tracks prescribing behavior."),
        "priority_tier": "1",
        "notes": (
            "Server-side bulk load; direct CSV on data.cms.gov (~25M rows). Rotating "
            "hashed path -- confirm/bump the data year with intake.py before --run."),
    },
    {
        "source_id": "FED_NHTSA_COMPLAINTS",
        "name": "NHTSA ODI Consumer Complaints (flat file)",
        "url": "https://static.nhtsa.gov/odi/ffdd/cmpl/FLAT_CMPL.zip",
        "kind": "zip",
        "member_pattern": r"CMPL\.txt$",
        "delimiter": "\t",
        "enclosure": None,     # NHTSA TAB flat files use NO enclosure; narratives carry stray "
        "has_header": False,   # CMPL.txt is data-only (TAB, ~49 fields); dbt maps C1..CN via the ODI field spec
        "publisher": "National Highway Traffic Safety Administration",
        "description": (
            "Every safety-related defect complaint NHTSA received since 1995 -- crash, fire, "
            "injury and death reports on vehicles/equipment. One row per complaint record."),
        "jurisdiction": "US",
        "category": "Health",
        "subcategory": "vehicle_safety",
        "unit_of_observation": "one row = one consumer complaint",
        "geographic_scope": "United States",
        "access_method": "bulk",
        "format": "tsv",
        "update_cadence": "daily",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "MFR_NAME; MAKETXT; MODELTXT; YEARTXT; ODINO",
        "accountability_relevance": (
            "Direct who-got-hurt receipts for auto defects -- injuries/deaths tied to make/"
            "model/manufacturer; pairs with recalls to test whether defects were acted on."),
        "priority_tier": "1",
        "notes": "Headerless TAB flat file (CMPL.txt) inside FLAT_CMPL.zip; ~49 fields per ODI spec.",
    },
    {
        "source_id": "FED_NHTSA_RECALLS",
        "name": "NHTSA ODI Recalls (flat file)",
        "url": "https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip",
        "kind": "zip",
        "member_pattern": r"RCL.*\.txt$",
        "delimiter": "\t",
        "enclosure": None,
        "has_header": False,
        "publisher": "National Highway Traffic Safety Administration",
        "description": (
            "Every safety recall campaign NHTSA holds -- defect/noncompliance, affected "
            "make/model/year, remedy. One row per campaign x product combination."),
        "jurisdiction": "US",
        "category": "Health",
        "subcategory": "vehicle_safety",
        "unit_of_observation": "one row = one recall campaign x product",
        "geographic_scope": "United States",
        "access_method": "bulk",
        "format": "tsv",
        "update_cadence": "daily",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "CAMPNO; MFGNAME; MAKETXT; MODELTXT; YEARTXT",
        "accountability_relevance": (
            "What defects got officially recalled -- the action side to pair with complaints "
            "(harm) and manufacturer identity."),
        "priority_tier": "1",
        "notes": "Headerless TAB flat file (RCL.txt) inside FLAT_RCL.zip; ~27 fields per ODI spec.",
    },
    {
        "source_id": "FED_NHTSA_INVESTIGATIONS",
        "name": "NHTSA ODI Investigations (flat file)",
        "url": "https://static.nhtsa.gov/odi/ffdd/inv/FLAT_INV.zip",
        "kind": "zip",
        "member_pattern": r"INV\.txt$",
        "delimiter": "\t",
        "enclosure": None,
        "has_header": False,
        "publisher": "National Highway Traffic Safety Administration",
        "description": (
            "NHTSA defect investigations -- the formal probes opened from complaint trends. "
            "One row per investigation record."),
        "jurisdiction": "US",
        "category": "Health",
        "subcategory": "vehicle_safety",
        "unit_of_observation": "one row = one investigation",
        "geographic_scope": "United States",
        "access_method": "bulk",
        "format": "tsv",
        "update_cadence": "daily",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "MFR_NAME; MAKETXT; MODELTXT; YEARTXT",
        "accountability_relevance": "Which harms NHTSA actually investigated -- regulator attention signal.",
        "priority_tier": "2",
        "notes": "Headerless TAB flat file (INV.txt) inside FLAT_INV.zip.",
    },
    {
        "source_id": "FED_OSHA_INSPECTIONS",
        "name": "OSHA Inspections (enforcement)",
        "url": "https://enforcedata.dol.gov/data_catalogs/osha/osha_inspection.csv.zip",
        "kind": "zip", "member_pattern": r"\.csv$", "delimiter": ",",
        "publisher": "Occupational Safety and Health Administration (DOL)",
        "description": "Every OSHA workplace safety inspection since 1972 -- impetus, scope, establishment. One row per inspection.",
        "jurisdiction": "US", "category": "Health", "subcategory": "workplace_safety",
        "unit_of_observation": "one row = one OSHA inspection", "geographic_scope": "United States",
        "access_method": "bulk", "format": "csv", "update_cadence": "daily", "license_terms": "Public domain (US Gov)",
        "join_keys": "activity_nr; estab_name; ein; state; naics_code",
        "accountability_relevance": "Where workers get hurt and who was inspected -- the workplace-harm surface; joins to employer identity.",
        "priority_tier": "1",
        "notes": "DOL enforcedata bulk CSV zip. If 404, confirm current path at enforcedata.dol.gov catalog.",
    },
    {
        "source_id": "FED_OSHA_VIOLATIONS",
        "name": "OSHA Violations (enforcement)",
        "url": "https://enforcedata.dol.gov/data_catalogs/osha/osha_violation.csv.zip",
        "kind": "zip", "member_pattern": r"\.csv$", "delimiter": ",",
        "publisher": "Occupational Safety and Health Administration (DOL)",
        "description": "Citations issued from OSHA inspections -- standard cited, penalty, gravity. One row per violation.",
        "jurisdiction": "US", "category": "Health", "subcategory": "workplace_safety",
        "unit_of_observation": "one row = one OSHA violation", "geographic_scope": "United States",
        "access_method": "bulk", "format": "csv", "update_cadence": "daily", "license_terms": "Public domain (US Gov)",
        "join_keys": "activity_nr; citation_id; standard; ein",
        "accountability_relevance": "What specifically the employer did wrong + the penalty -- the harm detail behind an inspection.",
        "priority_tier": "1",
        "notes": "DOL enforcedata bulk CSV zip; joins to OSHA inspections on activity_nr.",
    },
    {
        "source_id": "FED_DOL_WHD_WHISARD",
        "name": "DOL Wage & Hour compliance actions (WHISARD)",
        "url": "https://enforcedata.dol.gov/data_catalogs/whd/whd_whisard.csv.zip",
        "kind": "zip", "member_pattern": r"\.csv$", "delimiter": ",",
        "publisher": "Wage and Hour Division (DOL)",
        "description": "Every concluded WHD compliance action since FY2005 -- violations found, back wages, employees due, civil penalties. One row per case.",
        "jurisdiction": "US", "category": "Labor & Employment", "subcategory": "wage_theft",
        "unit_of_observation": "one row = one WHD compliance action", "geographic_scope": "United States",
        "access_method": "bulk", "format": "csv", "update_cadence": "quarterly", "license_terms": "Public domain (US Gov)",
        "join_keys": "case_id; trade_nm; legal_name; ein; naic_cd",
        "accountability_relevance": "Wage theft receipts -- who stiffed workers, how much back pay owed, how many employees hurt.",
        "priority_tier": "1",
        "notes": "DOL enforcedata bulk CSV zip. If 404, confirm current path at enforcedata.dol.gov catalog.",
    },
    {
        "source_id": "FED_MSHA_VIOLATIONS",
        "name": "MSHA Mine Safety Violations",
        "url": "https://arlweb.msha.gov/opengovernmentdata/DataSets/Violations.zip",
        "kind": "zip", "member_pattern": r"\.txt$", "delimiter": "|", "enclosure": None,
        "publisher": "Mine Safety and Health Administration (DOL)",
        "description": "Violations issued from MSHA mine inspections -- standard, penalty, persons affected. One row per violation.",
        "jurisdiction": "US", "category": "Health", "subcategory": "mine_safety",
        "unit_of_observation": "one row = one MSHA violation", "geographic_scope": "United States",
        "access_method": "bulk", "format": "psv", "update_cadence": "daily", "license_terms": "Public domain (US Gov)",
        "join_keys": "MINE_ID; EVENT_NO; CONTRACTOR_ID",
        "accountability_relevance": "Mine safety harm -- persons affected by hazardous conditions, tied to mine operator identity.",
        "priority_tier": "2",
        "notes": "MSHA open-data pipe-delimited .txt inside Violations.zip; header row present.",
    },
    {
        "source_id": "FED_MSHA_ACCIDENTS",
        "name": "MSHA Mine Accidents & Injuries",
        "url": "https://arlweb.msha.gov/opengovernmentdata/DataSets/Accidents.zip",
        "kind": "zip", "member_pattern": r"\.txt$", "delimiter": "|", "enclosure": None,
        "publisher": "Mine Safety and Health Administration (DOL)",
        "description": "Reported mine accidents, injuries and fatalities (30 CFR Part 50). One row per accident/injury record.",
        "jurisdiction": "US", "category": "Health", "subcategory": "mine_safety",
        "unit_of_observation": "one row = one accident/injury", "geographic_scope": "United States",
        "access_method": "bulk", "format": "psv", "update_cadence": "quarterly", "license_terms": "Public domain (US Gov)",
        "join_keys": "MINE_ID; CONTRACTOR_ID; DOCUMENT_NO",
        "accountability_relevance": "The bodies: mine injuries and deaths, tied to operator -- direct who-got-hurt.",
        "priority_tier": "2",
        "notes": "MSHA open-data pipe-delimited .txt inside Accidents.zip.",
    },
    {
        "source_id": "FED_MSHA_MINES",
        "name": "MSHA Mines (operator directory)",
        "url": "https://arlweb.msha.gov/opengovernmentdata/DataSets/Mines.zip",
        "kind": "zip", "member_pattern": r"\.txt$", "delimiter": "|", "enclosure": None,
        "publisher": "Mine Safety and Health Administration (DOL)",
        "description": "All coal and metal/non-metal mines under MSHA jurisdiction -- status, current owner/operator, commodity. One row per mine.",
        "jurisdiction": "US", "category": "Health", "subcategory": "mine_safety",
        "unit_of_observation": "one row = one mine", "geographic_scope": "United States",
        "access_method": "bulk", "format": "psv", "update_cadence": "monthly", "license_terms": "Public domain (US Gov)",
        "join_keys": "MINE_ID; CURRENT_CONTROLLER_ID; OPERATOR_ID",
        "accountability_relevance": "The mine->operator spine that turns violations/accidents into named-owner accountability.",
        "priority_tier": "2",
        "notes": "MSHA open-data pipe-delimited .txt inside Mines.zip.",
    },
    {
        "source_id": "FED_IRS_990_EFILE_INDEX",
        "name": "IRS 990 e-file Index (filer + XML URL, by year)",
        # UPGRADE 1 manifest: per-year index CSVs appended into one table.
        # apps.irs.gov serves 2017-2026 (earlier years 404; pre-2017 on AWS bucket, now dead).
        "manifest": [
            "https://apps.irs.gov/pub/epostcard/990/xml/2017/index_2017.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2018/index_2018.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2019/index_2019.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2020/index_2020.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2021/index_2021.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2022/index_2022.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2023/index_2023.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2024/index_2024.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2025/index_2025.csv",
            "https://apps.irs.gov/pub/epostcard/990/xml/2026/index_2026.csv",
        ],
        "kind": "csv", "delimiter": ",", "has_header": True,
        "publisher": "Internal Revenue Service (via AWS Open Data)",
        "description": (
            "Index of every electronically-filed Form 990/990-EZ/990-PF -- EIN, org name, "
            "form type, tax period, and the URL of the return's XML. One row per filing."),
        "jurisdiction": "US", "category": "Corporate / Nonprofit", "subcategory": "nonprofit_filings",
        "unit_of_observation": "one row = one e-filed 990 return", "geographic_scope": "United States",
        "access_method": "bulk", "format": "csv", "update_cadence": "static", "license_terms": "Public domain (US Gov)",
        "join_keys": "EIN; OBJECT_ID (-> XML return); TAXPAYER_NAME",
        "accountability_relevance": (
            "The map into the dark-money graph -- points at each nonprofit's XML return "
            "(Schedule I grants, Schedule R related orgs); the index to parse next."),
        "priority_tier": "1",
        "notes": "Manifest of AWS index_YYYY.csv. 2022+ need IRS.gov/GivingTuesday lake. Full XML parse is a separate build.",
    },
    {
        "source_id": "FED_SEC_INSIDER",
        "name": "SEC EDGAR Insider Transactions (Form 3/4/5, full history 2016Q3-2025Q1)",
        # UPGRADE 4 manifest+members: iterate all quarterly zips, extract per-member,
        # append across all quarters into per-member tables.
        "manifest": [
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2016q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2016q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2017q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2017q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2017q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2017q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2018q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2018q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2018q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2018q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2019q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2019q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2019q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2019q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2020q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2020q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2020q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2020q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2021q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2021q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2021q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2021q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2022q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2022q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2022q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2022q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2023q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2023q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2023q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2023q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2024q1_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2024q2_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2024q3_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2024q4_form345.zip",
            "https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/2025q1_form345.zip",
        ],
        "kind": "zip", "delimiter": "\t", "has_header": True, "enclosure": None,
        "members": [
            {"pattern": r"SUBMISSION\.tsv$", "suffix": "SUBMISSION"},
            {"pattern": r"REPORTINGOWNER\.tsv$", "suffix": "REPORTINGOWNER"},
            {"pattern": r"NONDERIV_TRANS\.tsv$", "suffix": "NONDERIV_TRANS"},
            {"pattern": r"(?<!NON)DERIV_TRANS\.tsv$", "suffix": "DERIV_TRANS"},
        ],
        "publisher": "U.S. Securities and Exchange Commission",
        "description": (
            "Section 16 insider filings (Form 3/4/5) as flat tables: submissions, reporting "
            "owners, and non-derivative/derivative transactions. Who bought/sold their own "
            "company's stock. Full history 2016Q3-2025Q1 (~35 quarters)."),
        "jurisdiction": "US", "category": "Corporate & Business Registries", "subcategory": "insider_ownership",
        "unit_of_observation": "one row per filing/owner/transaction", "geographic_scope": "United States",
        "access_method": "bulk", "format": "tsv", "update_cadence": "quarterly", "license_terms": "Public domain (US Gov)",
        "join_keys": "ACCESSION_NUMBER; CIK; ISSUERCIK; RPTOWNERCIK",
        "accountability_relevance": (
            "The ownership/control graph -- links named insiders (CIK) to the companies "
            "they control and trade; the who-profits backbone. Full history enables "
            "correlation with events (recalls, enforcement, earnings)."),
        "priority_tier": "1",
        "notes": "Manifest+members combo: 35 quarterly zips x 4 TSV members each -> 4 tables appended across all quarters.",
    },
    {
        "source_id": "FED_FDA_DRUG_ENFORCEMENT",
        "name": "openFDA Drug Enforcement (recalls)",
        # UPGRADE 3 json: .json.zip -> single-column RAW VARIANT table (dbt flattens results).
        "url": "https://download.open.fda.gov/drug/enforcement/drug-enforcement-0001-of-0001.json.zip",
        "kind": "json",
        "publisher": "U.S. Food and Drug Administration (openFDA)",
        "description": (
            "FDA drug recall/enforcement actions -- recalling firm, product, reason, "
            "classification, status. openFDA JSON (one doc with a results array)."),
        "jurisdiction": "US", "category": "Health", "subcategory": "drug_safety",
        "unit_of_observation": "recall events (in RAW:results)", "geographic_scope": "United States",
        "access_method": "bulk", "format": "json", "update_cadence": "quarterly", "license_terms": "Public domain (US Gov)",
        "join_keys": "recalling_firm; product_description; recall_number",
        "accountability_relevance": (
            "Drug harm receipts -- which firms recalled which products and why; pairs with "
            "Open Payments/Part D to connect industry money to product safety."),
        "priority_tier": "2",
        "notes": "openFDA zipped JSON -> VARIANT. Upgrades the prior 5000-row stub. Adverse events (huge) deferred (RED).",
    },
    {
        "source_id": "FED_FDA_DEVICE_CLASSIFICATION",
        "name": "openFDA Device Classification",
        "url": "https://download.open.fda.gov/device/classification/device-classification-0001-of-0001.json.zip",
        "kind": "json",
        "publisher": "U.S. Food and Drug Administration (openFDA)",
        "description": (
            "FDA medical-device classification database -- device name, class (I/II/III), "
            "regulation number, medical specialty, submission type. openFDA JSON "
            "(one doc with a results array)."),
        "jurisdiction": "US", "category": "Health", "subcategory": "device_safety",
        "unit_of_observation": "device classifications (in RAW:results)", "geographic_scope": "United States",
        "access_method": "bulk", "format": "json", "update_cadence": "monthly", "license_terms": "Public domain (US Gov)",
        "join_keys": "product_code; regulation_number",
        "accountability_relevance": (
            "Reference layer for device-harm work: maps product codes to risk class and "
            "regulation, so recalls and clearances can be read by risk tier."),
        "priority_tier": "2",
        "notes": "Re-ingest: prior API loader failed at first page and landed 1 junk row. Adverse events (MAUDE/FAERS/CAERS) stay deferred (RED).",
    },
    {
        "source_id": "FED_FDA_MAUDE_FULL",
        "name": "openFDA Device Adverse Events (MAUDE, full bulk)",
        # Loaded via scripts/fda_bulk_split_load.py (parts exceed the 128MB
        # whole-doc VARIANT parse limit). Manifest: openFDA download.json,
        # device.event partitions (~365 quarterly part files, ~25.7M records).
        "url": "https://download.open.fda.gov/device/event/",
        "kind": "json",
        "manifest": {"type": "json", "url": "https://api.fda.gov/download.json",
                     "path": "results.device.event.partitions", "item": "file"},
        "publisher": "U.S. Food and Drug Administration (openFDA)",
        "description": (
            "FDA MAUDE medical-device adverse-event reports (malfunctions, injuries, "
            "deaths) -- full openFDA bulk export, all quarters. openFDA JSON parts "
            "(each a doc with a results array; rows are chunks, use ARRAY_SIZE)."),
        "jurisdiction": "US", "category": "Health", "subcategory": "device_safety",
        "unit_of_observation": "device adverse-event reports (in RAW:results)",
        "geographic_scope": "United States",
        "access_method": "bulk", "format": "json", "update_cadence": "quarterly",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "mdr_report_key; device.device_report_product_code",
        "accountability_relevance": (
            "The device-harm event layer itself: who was hurt by which device, "
            "pairs with GUDID/classification/enforcement for the full device map."),
        "priority_tier": "1",
        "notes": "Full replacement for the 1,386-row FED_FDA_MAUDE stub (left untouched). Authorized 2026-08-27.",
    },
    {
        "source_id": "FED_FDA_DEVICE_ENFORCEMENT",
        "name": "openFDA Device Enforcement (recalls)",
        "url": "https://download.open.fda.gov/device/enforcement/device-enforcement-0001-of-0001.json.zip",
        "kind": "json",
        "publisher": "U.S. Food and Drug Administration (openFDA)",
        "description": (
            "FDA device recall/enforcement actions -- recalling firm, product, reason, "
            "classification, status. openFDA JSON (one doc with a results array)."),
        "jurisdiction": "US", "category": "Health", "subcategory": "device_safety",
        "unit_of_observation": "recall events (in RAW:results)", "geographic_scope": "United States",
        "access_method": "bulk", "format": "json", "update_cadence": "quarterly", "license_terms": "Public domain (US Gov)",
        "join_keys": "recalling_firm; product_description; recall_number",
        "accountability_relevance": (
            "Device harm receipts -- which firms recalled which devices and why; mirrors "
            "the drug-enforcement table on the device side."),
        "priority_tier": "2",
        "notes": "Re-ingest: prior API loader failed at first page and landed 1 junk row. Adverse events (MAUDE/FAERS/CAERS) stay deferred (RED).",
    },
    {
        "source_id": "FED_FEC_INDEPENDENT_EXPENDITURES",
        "name": "FEC Independent Expenditures (bulk, multi-cycle)",
        # UPGRADE 1 manifest: per-cycle IE CSVs on www.fec.gov (direct, no S3 redirect),
        # appended into one table. Upgrades the prior 83k stub.
        "manifest": [
            "https://www.fec.gov/files/bulk-downloads/2018/independent_expenditure_2018.csv",
            "https://www.fec.gov/files/bulk-downloads/2020/independent_expenditure_2020.csv",
            "https://www.fec.gov/files/bulk-downloads/2022/independent_expenditure_2022.csv",
            "https://www.fec.gov/files/bulk-downloads/2024/independent_expenditure_2024.csv",
        ],
        "kind": "csv", "delimiter": ",", "has_header": True,
        "publisher": "Federal Election Commission",
        "description": (
            "Independent expenditures -- spending by super PACs and outside groups for/against "
            "federal candidates, not coordinated with campaigns. One row per expenditure."),
        "jurisdiction": "US", "category": "Politics", "subcategory": "independent_expenditures",
        "unit_of_observation": "one row = one independent expenditure", "geographic_scope": "United States",
        "access_method": "bulk", "format": "csv", "update_cadence": "cycle", "license_terms": "Public domain (US Gov)",
        "join_keys": "cmte_id; cand_id; payee_name",
        "accountability_relevance": (
            "The dark/outside money OUT of politics -- who spent to elect/defeat whom; the "
            "counterpart to the 84M individual contributions (money IN)."),
        "priority_tier": "1",
        "notes": "Manifest of FEC bulk IE CSVs (2018-2024). If a cycle 404s or lacks a header, adjust.",
    },
    {
        "source_id": "FED_USASPENDING_CONTRACTS_FULL",
        "name": "USASpending Federal Contract Awards (FY2007-FY2026, all agencies)",
        "manifest": {
            # USAspending deletes last month's archive, so a literal list of dated
            # URLs 404s on their schedule. Read the bucket listing instead and take
            # whichever snapshot is live today.
            "type": "regex",
            "url": "https://files.usaspending.gov/award_data_archive/",
            "path": r"<Key>(FY\d{4}_All_Contracts_Full_\d{8}\.zip)</Key>",
            "base": "https://files.usaspending.gov/award_data_archive/",
            "paginate": "s3",
            "latest_re": r"_(\d{8})\.zip$",
            "expect_files": 20,          # FY2007-FY2026; a short resolve is a sweep
        },
        "kind": "zip",
        "member_pattern": r"\.csv$",
        "delimiter": ",",
        "publisher": "U.S. Department of the Treasury / USASpending.gov",
        "description": (
            "Every federal prime contract award (FY2007-present). One row per contract action (transaction). "
            "Carries recipient UEI, DUNS, NAICS, awarding/funding agency, place of performance, dollar amounts."),
        "jurisdiction": "US",
        "category": "Spending",
        "subcategory": "federal_contracts",
        "unit_of_observation": "one row = one contract transaction/action",
        "geographic_scope": "United States + international",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "monthly",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "recipient_uei; awarding_agency_code; funding_agency_code; naics_code; recipient_name",
        "accountability_relevance": (
            "Where ALL federal contract money goes. Links debarred parties (SAM UEI) to contracts they "
            "still received; tracks which companies get repeat sole-source awards; geographic concentration."),
        "priority_tier": "1",
        "notes": (
            "Manifest of per-FY all-agency zips from files.usaspending.gov. Each zip ~1-2 GB; "
            "unzipped CSV ~8-12 GB per FY. Total ~30 GB compressed. Expect 100M+ rows across all FYs."),
    },
    {
        "source_id": "FED_USASPENDING_ASSISTANCE_FULL",
        "name": "USASpending Federal Assistance Awards (FY2007-FY2026, all agencies)",
        "manifest": {
            # USAspending deletes last month's archive, so a literal list of dated
            # URLs 404s on their schedule. Read the bucket listing instead and take
            # whichever snapshot is live today.
            "type": "regex",
            "url": "https://files.usaspending.gov/award_data_archive/",
            "path": r"<Key>(FY\d{4}_All_Assistance_Full_\d{8}\.zip)</Key>",
            "base": "https://files.usaspending.gov/award_data_archive/",
            "paginate": "s3",
            "latest_re": r"_(\d{8})\.zip$",
            "expect_files": 20,          # FY2007-FY2026; a short resolve is a sweep
        },
        "kind": "zip",
        "member_pattern": r"\.csv$",
        "delimiter": ",",
        "publisher": "U.S. Department of the Treasury / USASpending.gov",
        "description": (
            "Every federal assistance award -- grants, loans, direct payments, insurance (FY2007-present). "
            "One row per transaction. Carries recipient UEI, CFDA/Assistance Listing, agency, amounts."),
        "jurisdiction": "US",
        "category": "Spending",
        "subcategory": "federal_assistance",
        "unit_of_observation": "one row = one assistance transaction/action",
        "geographic_scope": "United States + international",
        "access_method": "bulk",
        "format": "csv",
        "update_cadence": "monthly",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "recipient_uei; awarding_agency_code; cfda_number; recipient_name",
        "accountability_relevance": (
            "Where ALL federal grants/loans/aid goes. Links to SAM (UEI), connects debarred orgs to "
            "assistance they received, tracks geographic distribution of federal aid."),
        "priority_tier": "1",
        "notes": (
            "Manifest of per-FY all-agency zips from files.usaspending.gov. Each zip 0.2-3 GB; "
            "total ~20 GB compressed. Expect 50-100M+ rows across all FYs."),
    },
    {
        "source_id": "FED_FEC_COMMITTEES",
        "name": "FEC Committee Master (bulk, multi-cycle)",
        # Direct S3 URLs (fec.gov redirects cross-host to this GovCloud bucket).
        # Pipe-delimited, no header, zipped.
        "manifest": [
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2018/cm18.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2020/cm20.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2022/cm22.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2024/cm24.zip",
        ],
        "kind": "zip", "delimiter": "|", "has_header": False, "enclosure": None,
        "publisher": "Federal Election Commission",
        "description": (
            "FEC committee master file -- every registered political committee (PACs, party committees, "
            "candidate committees). ID, name, type, party, treasurer, address, filing frequency."),
        "jurisdiction": "US", "category": "Politics", "subcategory": "committees",
        "unit_of_observation": "one row = one committee registration", "geographic_scope": "United States",
        "access_method": "bulk", "format": "pipe-delimited", "update_cadence": "cycle",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "C1 (CMTE_ID); C11 (CONNECTED_ORG_ID)",
        "accountability_relevance": (
            "The registry of all PACs, party committees, and candidate committees -- "
            "links committee IDs in contribution/expenditure data to real names and connected orgs."),
        "priority_tier": "1",
        "notes": "Pipe-delimited, headerless, zip. Uses direct GovCloud S3 URL (fec.gov 302s).",
    },
    {
        "source_id": "FED_FEC_CANDIDATES",
        "name": "FEC Candidate Master (bulk, multi-cycle)",
        "manifest": [
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2018/cn18.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2020/cn20.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2022/cn22.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2024/cn24.zip",
        ],
        "kind": "zip", "delimiter": "|", "has_header": False, "enclosure": None,
        "publisher": "Federal Election Commission",
        "description": (
            "FEC candidate master file -- every registered federal candidate. "
            "ID, name, party, office, state, district, incumbent status."),
        "jurisdiction": "US", "category": "Politics", "subcategory": "candidates",
        "unit_of_observation": "one row = one candidate registration", "geographic_scope": "United States",
        "access_method": "bulk", "format": "pipe-delimited", "update_cadence": "cycle",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "C1 (CAND_ID); C6 (CAND_PCC, principal campaign committee)",
        "accountability_relevance": (
            "Registry of all federal candidates -- links candidate IDs in expenditure/contribution "
            "data to real names, parties, and offices sought."),
        "priority_tier": "1",
        "notes": "Pipe-delimited, headerless, zip. Uses direct GovCloud S3 URL.",
    },
    {
        "source_id": "FED_FEC_CAND_CMTE_LINKAGE",
        "name": "FEC Candidate-Committee Linkage (bulk, multi-cycle)",
        "manifest": [
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2018/ccl18.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2020/ccl20.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2022/ccl22.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2024/ccl24.zip",
        ],
        "kind": "zip", "delimiter": "|", "has_header": False, "enclosure": None,
        "publisher": "Federal Election Commission",
        "description": (
            "Links candidates to their authorized committees (PACs that can accept "
            "contributions on their behalf). The bridge between candidate IDs and committee IDs."),
        "jurisdiction": "US", "category": "Politics", "subcategory": "candidate_committee_linkage",
        "unit_of_observation": "one row = one candidate-committee link", "geographic_scope": "United States",
        "access_method": "bulk", "format": "pipe-delimited", "update_cadence": "cycle",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "C1 (CAND_ID); C2 (CAND_ELECTION_YR); C3 (FEC_ELECTION_YR); C4 (CMTE_ID)",
        "accountability_relevance": (
            "The bridge table that connects candidates to the committees raising money for them."),
        "priority_tier": "1",
        "notes": "Pipe-delimited, headerless, zip. Uses direct GovCloud S3 URL.",
    },
    {
        "source_id": "FED_FEC_PAC_SUMMARY",
        "name": "FEC PAC/Party Committee Summary (bulk, multi-cycle)",
        "manifest": [
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2018/webk18.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2020/webk20.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2022/webk22.zip",
            "https://cg-519a459a-0ea3-42c2-b7bc-fa1143481f74.s3-us-gov-west-1.amazonaws.com/bulk-downloads/2024/webk24.zip",
        ],
        "kind": "zip", "delimiter": "|", "has_header": False, "enclosure": None,
        "publisher": "Federal Election Commission",
        "description": (
            "Financial summary for PACs and party committees -- total receipts, disbursements, "
            "cash on hand, debts, contributions to/from candidates."),
        "jurisdiction": "US", "category": "Politics", "subcategory": "pac_financials",
        "unit_of_observation": "one row = one committee financial summary per cycle", "geographic_scope": "United States",
        "access_method": "bulk", "format": "pipe-delimited", "update_cadence": "cycle",
        "license_terms": "Public domain (US Gov)",
        "join_keys": "C1 (CMTE_ID); C2 (CMTE_NM)",
        "accountability_relevance": (
            "The money totals -- how much each PAC/party committee raised and spent. "
            "Connects to committees and expenditures for the full political money flow."),
        "priority_tier": "1",
        "notes": "Pipe-delimited, headerless, zip. Uses direct GovCloud S3 URL.",
    },
]
