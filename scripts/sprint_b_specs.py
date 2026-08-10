"""Sprint B specs — the 6 gap-list datasets with verified direct download URLs.

Sprint B attack order (direct downloads + resolver, high connection value):
  1. GLEIF Level 2 (RR)        — who-owns-whom globally       LEI (resolver)
  2. SEC 13F Submission        — filer metadata                CIK
  3. SEC 13F Positions         — institutional holdings        CUSIP
  4. DOL OSHA Inspections      — workplace safety enforcement  activity_nr
  5. PHMSA Flagged Incidents   — pipeline failures/explosions  operator
  6. UK Companies House        — 6M UK companies              CompanyNumber
  7. DOL OLMS (LM-2 filings)  — union financial reports       EIN

URLs verified 2026-07-27.

Deferred to Sprint C (API-gated / need custom loaders):
  - LDA lobbying (lda.gov REST API, needs key + pagination)
  - USASpending subawards (bulk_download API, needs POST + poll)
  - DOL WHD wage theft (old URL dead, new portal API-gated)
  - ATF FFL listings (form-gated, no static URL)
"""

SPECS = [
    # ---------------------------------------------------------------------- #
    # 1. GLEIF Level 2 — Relationship Records (who-owns-whom)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "INT_GLEIF_RR",
        "name": "GLEIF Level 2 — Relationship Records (parent-child ownership)",
        "publisher": "Global Legal Entity Identifier Foundation",
        "url": "",  # resolved dynamically
        "kind": "zip",
        "member_pattern": r"\.csv$",
        "loader": "server_side",
        "resolver": {
            "url": "https://goldencopy.gleif.org/api/v2/golden-copies/publishes/latest",
            "type": "json",
            "path": "data.rr.full_file.csv.url",
        },
        "key_cols": [
            {"col": "Relationship.StartNode.NodeID", "as": "LEI"},
            {"col": "Relationship.EndNode.NodeID", "as": "PARENT_LEI"},
        ],
        "join_keys": "LEI",
        "category": "corporate_structure",
        "subcategory": "ownership",
        "unit_of_observation": "one row = one LEI-to-parent-LEI relationship",
        "update_cadence": "daily",
        "license_terms": "CC0 (GLEIF Golden Copy)",
        "accountability_relevance": (
            "Lights up the entire 3.4M LEI spine with who-owns-whom chains. "
            "Every corporate subsidiary → ultimate parent traversal starts here. "
            "Bridges SEC filers (CIK→LEI crosswalk) to their global parent entities."),
        "priority_tier": "1",
        "notes": (
            "Server-side load. GLEIF Golden Copy API resolves a daily-rotating URL. "
            "ZIP contains one large CSV with dotted column names "
            "(Relationship.StartNode.NodeID, Relationship.EndNode.NodeID, "
            "Relationship.RelationshipType, Registration.RegistrationStatus, etc). "
            "~2M rows. The resolver extracts data.rr.full_file.csv.url from the "
            "publishes/latest JSON endpoint."),
    },
    # ---------------------------------------------------------------------- #
    # 2. SEC 13F — Submission metadata (filer identity)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_SEC_13F_SUBMISSION",
        "name": "SEC Form 13F — Submission Metadata (filer identity)",
        "publisher": "Securities and Exchange Commission",
        "url": "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/01mar2026-31may2026_form13f.zip",
        "kind": "zip",
        "member": r"SUBMISSION\.tsv$",
        "delimiter": "\t",
        "loader": "server_side",
        "key_cols": [
            {"col": "CIK", "as": "CIK"},
        ],
        "join_keys": "CIK",
        "category": "finance",
        "subcategory": "institutional_ownership",
        "unit_of_observation": "one row = one 13F filing (one filer, one quarter)",
        "update_cadence": "quarterly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "The filer identity table for 13F institutional holdings. ~5K filers per "
            "quarter (hedge funds, mutual funds, insurance companies). CIK key connects "
            "to SEC EDGAR universe, insider transactions, and GLEIF (via CIK→LEI crosswalk)."),
        "priority_tier": "1",
        "notes": (
            "Server-side load. ZIP contains 7 TSV files — this targets SUBMISSION.tsv "
            "only. Columns: ACCESSION_NUMBER, CIK, COMPANY_CONFORMED_NAME, "
            "FILING_DATE, REPORT_CALENDAR_OR_QUARTER, others. "
            "ACCESSION_NUMBER bridges to the 13F positions table (INFOTABLE). "
            "URL pattern: 01mon{YYYY}-{end}mon{YYYY}_form13f.zip (changed 2024)."),
    },
    # ---------------------------------------------------------------------- #
    # 3. SEC 13F — Positions (institutional holdings)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_SEC_13F_POSITIONS",
        "name": "SEC Form 13F — Institutional Holdings (positions)",
        "publisher": "Securities and Exchange Commission",
        "url": "https://www.sec.gov/files/structureddata/data/form-13f-data-sets/01mar2026-31may2026_form13f.zip",
        "kind": "zip",
        "member": r"INFOTABLE\.tsv$",
        "delimiter": "\t",
        "loader": "server_side",
        "key_cols": [
            {"col": "CUSIP", "as": "CUSIP"},
            {"col": "ACCESSION_NUMBER", "as": "SEC_ACCESSION_NUMBER"},
        ],
        "join_keys": "CUSIP, SEC_ACCESSION_NUMBER",
        "category": "finance",
        "subcategory": "institutional_ownership",
        "unit_of_observation": "one row = one security position held by one filer in one quarter",
        "update_cadence": "quarterly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "Millions of fund→company ownership positions per quarter. CUSIP identifies "
            "the held security; ACCESSION_NUMBER joins to SUBMISSION for filer CIK. "
            "The 'who owns what' backbone: which hedge fund loaded up before the merger, "
            "which insurer dumped stock before the recall."),
        "priority_tier": "1",
        "notes": (
            "Server-side load (~2-3M rows per quarter). ZIP targets INFOTABLE.tsv. "
            "Columns: ACCESSION_NUMBER, INFOTABLE_SK, NAMEOFISSUER, TITLEOFCLASS, "
            "CUSIP, VALUE (in $1000s), SSHPRNAMT, SSHPRNAMTTYPE, "
            "INVESTMENTDISCRETION, VOTING_AUTH_SOLE/SHARED/NONE, PUTCALL. "
            "Join via ACCESSION_NUMBER → FED_SEC_13F_SUBMISSION for filer CIK."),
    },
    # ---------------------------------------------------------------------- #
    # 4. DOL OSHA — Inspections (workplace safety enforcement)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_DOL_OSHA_INSPECTION",
        "name": "DOL OSHA — Workplace Safety Inspections",
        "publisher": "Occupational Safety and Health Administration",
        "url": "https://data.dol.gov/data-catalog/OSHA/inspection/OSHA_inspection.zip",
        "kind": "zip_csv",
        "loader": "server_side",
        "key_cols": [
            {"col": "activity_nr", "as": "OSHA_ACTIVITY_NR"},
        ],
        "join_keys": "OSHA_ACTIVITY_NR",
        "category": "labor",
        "subcategory": "workplace_safety",
        "unit_of_observation": "one row = one OSHA inspection of a worksite",
        "update_cadence": "monthly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "~4-5M inspections back to 1970s. Identifies repeat-violator establishments "
            "by name and address. SIC/NAICS codes enable industry-wide pattern detection. "
            "Bridges to other enforcement datasets via establishment name/address matching. "
            "The 'how many times were they warned before someone died' detector."),
        "priority_tier": "1",
        "notes": (
            "Server-side load (~4-5M rows). New URL at data.dol.gov (old enforcedata.dol.gov "
            "is dead, 301 → generic page). CSV inside ZIP. 36 columns including: "
            "activity_nr (PK), estab_name, site_address/city/state/zip, owner_type, "
            "sic_code, naics_code, insp_type, open_date, close_case_date, "
            "nr_in_estab (employee count), union_status. "
            "NOTE: No direct EIN column — entity linkage is via name/address or "
            "SIC/NAICS + geography. The connect engine may match via establishment name."),
    },
    # ---------------------------------------------------------------------- #
    # 5. PHMSA — Flagged Pipeline Incidents
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_PHMSA_FLAGGED_INCIDENTS",
        "name": "PHMSA — Flagged Pipeline Safety Incidents (significant events)",
        "publisher": "Pipeline and Hazardous Materials Safety Administration",
        "download_url": "https://www.phmsa.dot.gov/sites/phmsa.dot.gov/files/data_statistics/pipeline/incident_gas_transmission_gathering_jan2010_present.zip",
        "kind": "zip_csv",
        "member": r"\.(csv|txt)$",
        "encoding": "latin-1",
        # the .txt member is tab-delimited; ragged trailing tabs on some rows,
        # so use the python engine and skip malformed lines loudly
        "csv_opts": {"sep": "\t", "engine": "python", "on_bad_lines": "warn"},
        "loader": "bridge_fuel",
        "key_cols": [
            {"col": "OPERATOR_ID", "as": "PHMSA_OPERATOR_ID"},
        ],
        "join_keys": "PHMSA_OPERATOR_ID",
        "category": "environment",
        "subcategory": "pipeline_safety",
        "unit_of_observation": "one row = one flagged pipeline incident (failure, explosion, leak)",
        "update_cadence": "quarterly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "Curated significant pipeline incidents — failures, explosions, fatalities. "
            "OPERATOR_ID identifies the pipeline company; repeat-violator patterns are "
            "immediately visible. Connects to EPA FRS (facility) and FERC filings "
            "via operator identity. The 'they kept exploding and nobody shut them down' "
            "detector."),
        "priority_tier": "1",
        "notes": (
            "Bridge_fuel load (smaller curated dataset). Direct stable ZIP URL at "
            "phmsa.dot.gov — not rotating. Contains flagged/significant incidents across "
            "all pipeline types (gas distribution, gas transmission, hazardous liquid, LNG). "
            "Columns include: OPERATOR_ID, OPERATOR_NAME, REPORT_NUMBER, INCIDENT_DATE, "
            "CITY/STATE/COUNTY/FIPS, FATALITIES, INJURIES, PROPERTY_DAMAGE_COSTS, "
            "COMMODITY, CAUSE. "
            "Follow-up: load full incident datasets per type for completeness."),
    },
    # ---------------------------------------------------------------------- #
    # 6. UK Companies House — Full company register
    # ---------------------------------------------------------------------- #
    {
        "source_id": "INT_UK_COMPANIES_HOUSE",
        "name": "UK Companies House — Basic Company Data (full register)",
        "publisher": "UK Companies House",
        "url": "https://download.companieshouse.gov.uk/BasicCompanyDataAsOneFile-2026-07-01.zip",
        "kind": "zip",
        "member_pattern": r"\.csv$",
        "loader": "server_side",
        "key_cols": [
            {"col": "CompanyNumber", "as": "UK_COMPANY_NUMBER"},
        ],
        "join_keys": "UK_COMPANY_NUMBER",
        "category": "corporate_structure",
        "subcategory": "company_registry",
        "unit_of_observation": "one row = one UK registered company",
        "update_cadence": "monthly",
        "license_terms": "Open Government Licence v3.0",
        "accountability_relevance": (
            "6M UK companies with registered address, SIC codes, incorporation date, "
            "and company status. Some carry LEI cross-references. Bridges to GLEIF L1/L2 "
            "for UK entities in global ownership chains. Essential for tracing UK "
            "subsidiaries of US-listed parent companies."),
        "priority_tier": "2",
        "notes": (
            "Server-side load (~6M rows). Monthly snapshot ZIP — URL rotates predictably: "
            "BasicCompanyDataAsOneFile-{YYYY}-{MM}-01.zip. CSV inside ZIP. "
            "Columns: CompanyName, CompanyNumber, RegAddress.*, CompanyCategory, "
            "CompanyStatus, CountryOfOrigin, DissolutionDate, IncorporationDate, "
            "Accounts.*, Returns.*, SICCode.SicText_1-4, URI. "
            "NOTE: Column names use dots (like GLEIF L1). CompanyNumber is the UK "
            "equivalent of EIN — 8 chars, sometimes with letter prefix."),
    },
    # ---------------------------------------------------------------------- #
    # 7. DOL OLMS — Union Financial Reports (LM-2/3/4)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_DOL_OLMS",
        "name": "DOL OLMS — Union Financial Reports (LM-2/3/4 filings)",
        "publisher": "Office of Labor-Management Standards",
        "download_url": "https://olmsapps.dol.gov/olpdr/GetYearlyFileServlet?report=LVLk",
        "kind": "zip_csv",
        "member": r"lm_data",
        "delimiter": "|",
        "has_header": False,
        "loader": "bridge_fuel",
        "csv_opts": {"header": None, "sep": "|", "names": [
            "RPT_ID", "UNION_NAME", "ABBR", "FILE_NUMBER", "DESIGNATION_DATE",
            "FISCAL_YEAR_END", "UNIT_NAME", "FORM_TYPE", "TOTAL_ASSETS",
            "TOTAL_LIABILITIES", "TOTAL_RECEIPTS", "TOTAL_DISBURSEMENTS",
            "TOTAL_MEMBERS", "RECEIVE_DATE", "CITY", "STATE", "ZIP",
            "EIN", "AMENDED", "COVERAGE_START", "COVERAGE_END",
        ]},
        "key_cols": [
            {"col": "EIN", "as": "EIN"},
            {"col": "FILE_NUMBER", "as": "OLMS_FILE_NUMBER"},
        ],
        "join_keys": "EIN",
        "category": "labor",
        "subcategory": "union_finances",
        "unit_of_observation": "one row = one union financial report (LM-2, LM-3, or LM-4)",
        "update_cadence": "yearly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "Union financial disclosure: total assets, liabilities, receipts, "
            "disbursements, and membership counts. EIN-keyed so it connects directly "
            "to IRS BMF (1.9M nonprofits) and USASpending contracts. "
            "The 'where did the union dues go' detector — tracks officer compensation, "
            "general disbursements, and payer/payee relationships."),
        "priority_tier": "1",
        "notes": (
            "Bridge_fuel load (2026 fiscal year). OLMS OLPDR yearly download: "
            "ZIP contains 25 pipe-delimited text files with NO headers. "
            "This spec loads only the `lm_data` file (core filing table). "
            "Column names inferred from the OLMS data guide. "
            "Each yearly ZIP has ~30K-50K filings. "
            "Follow-up: load ar_disbursements_emp_off (officer comp) and "
            "ar_payer_payee (who got paid) as separate sources. "
            "Host: olmsapps.dol.gov (new to egress). "
            "Report code for 2026 is 'LVLk' — codes are opaque, not predictable."),
    },
]
