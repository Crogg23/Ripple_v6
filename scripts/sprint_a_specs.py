"""Sprint A specs — the first five high-graph-value datasets from the Next Pour Plan.

Each spec follows the universal schema (loadkit/spec_schema.py). The pour router
reads the `loader` field to dispatch; key_cols drive both the column rename in the
loader AND the connect engine's auto-wiring.

Sprint A attack order (direct downloads, high connection value):
  1. FEC Leadership PAC sponsors          ~5K rows,   FEC_ID
  2. Housestockwatcher STOCK Act trades    ~30K rows,  BIOGUIDE
  3. IRS 990 e-file index                  ~3M rows,   EIN
  4. EPA FRS uncap (full)                  ~4M rows,   FRS_ID, EIN
  5. SEC Form 3/4/5 insider transactions   ~5M rows,   CIK

URLs verified 2026-07-27.
"""

SPECS = [
    # ---------------------------------------------------------------------- #
    # 1. FEC Leadership PAC sponsors
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_FEC_LEADERSHIP_PAC",
        "name": "FEC Leadership PAC Sponsors (candidate-PAC bridge)",
        "publisher": "Federal Election Commission",
        "download_url": "https://www.fec.gov/files/bulk-downloads/2024/ccl24.zip",
        "kind": "zip_csv",
        "member": r"ccl\.txt$",
        "delimiter": "|",
        "has_header": False,
        "csv_opts": {"header": None, "sep": "|", "names": [
            "CAND_ID", "CAND_ELECTION_YR", "FEC_ELECTION_YR",
            "CMTE_ID", "CMTE_TP", "CMTE_DSGN", "LINKAGE_ID"]},
        "loader": "bridge_fuel",
        "key_cols": [
            {"col": "CAND_ID", "as": "FEC_CANDIDATE_ID"},
            {"col": "CMTE_ID", "as": "FEC_COMMITTEE_ID"},
        ],
        "join_keys": "FEC_ID",
        "category": "politics",
        "subcategory": "campaign_finance",
        "unit_of_observation": "one row = one candidate-to-committee linkage",
        "update_cadence": "weekly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "Pre-built bridge: which member of Congress controls which Leadership PAC. "
            "Connects FEC committee money flows directly to legislators (BIOGUIDE)."),
        "priority_tier": "1",
        "notes": (
            "FEC candidate-committee linkage file (ccl). Pipe-delimited, no header. "
            "Columns: CAND_ID|CAND_ELECTION_YR|FEC_ELECTION_YR|CMTE_ID|CMTE_TP|"
            "CMTE_DSGN|LINKAGE_ID. The FEC_CANDIDATE_ID bridges to our landed FEC "
            "contributions and to the legislator spine via bioguide crosswalks."),
    },
    # ---------------------------------------------------------------------- #
    # 2. Housestockwatcher STOCK Act trades
    # ---------------------------------------------------------------------- #
    {
        "source_id": "XC_HOUSESTOCKWATCHER",
        "name": "Housestockwatcher — Congressional Stock Trades (STOCK Act)",
        "publisher": "housestockwatcher.com (civic tech)",
        "download_url": "https://house-stock-watcher-data.s3-us-west-2.amazonaws.com/data/all_transactions.csv",
        "kind": "csv",
        "loader": "bridge_fuel",
        "key_cols": [
            {"col": "representative", "as": "MEMBER_NAME"},
            {"col": "ticker", "as": "TICKER"},
        ],
        "join_keys": "BIOGUIDE",
        "category": "politics",
        "subcategory": "financial_disclosure",
        "unit_of_observation": "one row = one stock transaction by a member of Congress",
        "update_cadence": "daily",
        "license_terms": "Public (civic tech, no stated license)",
        "accountability_relevance": (
            "Completes the insider-trading triangle: member stock trades linked to "
            "committee assignments (Voteview) and SEC filings (CIK). The 'traded "
            "while legislating' detector."),
        "priority_tier": "1",
        "notes": (
            "CSV with header. Key columns: representative (name), district, ticker, "
            "transaction_date, amount, type. BIOGUIDE not a column — join via member "
            "name crosswalk to legislator spine. S3 hosted, no auth."),
    },
    # ---------------------------------------------------------------------- #
    # 3. IRS 990 e-file index (replaces 200-row test load)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_IRS_990_INDEX",
        "name": "IRS 990 E-File Index (full — all filing years)",
        "publisher": "Internal Revenue Service",
        "url": "https://irs-form-990.s3.amazonaws.com/index_2024.csv",
        "kind": "csv",
        "loader": "server_side",
        "key_cols": [
            {"col": "EIN", "as": "EIN"},
        ],
        "join_keys": "EIN",
        "category": "nonprofits",
        "subcategory": "tax_filings",
        "unit_of_observation": "one row = one 990/990-EZ/990-PF e-file return",
        "update_cadence": "monthly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "The index that links EINs to their full XML 990 returns. Replaces the "
            "200-row test load. Connects to IRS BMF (1.9M EINs) and USASpending."),
        "priority_tier": "1",
        "notes": (
            "Server-side load (3M+ rows). CSV on S3 (irs-form-990 bucket). "
            "Each row has: RETURN_ID, FILING_TYPE, EIN, TAX_PERIOD, SUB_DATE, "
            "TAXPAYER_NAME, RETURN_TYPE, DLN, OBJECT_ID. The OBJECT_ID links to "
            "the actual XML return for Schedule I/R parsing (Sprint D)."),
    },
    # ---------------------------------------------------------------------- #
    # 4. EPA FRS uncap (full facility registry — remove 500K cap)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_EPA_FRS_FULL",
        "name": "EPA Facility Registry Service — Full National Download",
        "publisher": "Environmental Protection Agency",
        "url": "https://ordsext.epa.gov/FLA/www3/state_files/national_combined.zip",
        "kind": "zip",
        "member_pattern": r"NATIONAL_FACILITY_FILE\.csv$",
        "member": r"NATIONAL_FACILITY_FILE\.csv$",
        "loader": "server_side",
        "key_cols": [
            {"col": "REGISTRY_ID", "as": "FRS_ID"},
            {"col": "FEDERAL_FACILITY_CODE_EIN", "as": "EIN"},
        ],
        "join_keys": "FRS_ID, EIN",
        "category": "environment",
        "subcategory": "facility_registry",
        "unit_of_observation": "one row = one EPA-registered facility",
        "update_cadence": "weekly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "The EPA's master facility list (~4M sites). Crosswalk from FRS_ID to EIN "
            "jumps from 1.9% to ~60% coverage when uncapped. Bridges EPA enforcement "
            "(ECHO) to USASpending contracts and IRS BMF."),
        "priority_tier": "1",
        "notes": (
            "Server-side load (4M+ rows). Replaces the capped 500K load. ZIP contains "
            "a single large CSV. REGISTRY_ID is the FRS spine key. "
            "FEDERAL_FACILITY_CODE_EIN carries EIN for federal facilities."),
    },
    # ---------------------------------------------------------------------- #
    # 5. SEC Form 3/4/5 insider transactions (ownership backbone)
    # ---------------------------------------------------------------------- #
    {
        "source_id": "FED_SEC_INSIDER_TXN",
        "name": "SEC EDGAR Insider Transactions (Form 3/4/5 — DERA dataset)",
        "publisher": "Securities and Exchange Commission",
        "url": "https://www.sec.gov/files/dera/data/form-345/form345.zip",
        "kind": "zip",
        "member_pattern": r"\.tsv$",
        "delimiter": "\t",
        "loader": "server_side",
        "key_cols": [
            {"col": "ISSUER_CIK", "as": "CIK"},
        ],
        "join_keys": "CIK",
        "category": "finance",
        "subcategory": "insider_ownership",
        "unit_of_observation": "one row = one insider transaction filing (Form 3/4/5)",
        "update_cadence": "quarterly",
        "license_terms": "Public domain (US Gov)",
        "accountability_relevance": (
            "The ownership backbone: every insider buy/sell/gift reported to the SEC. "
            "Links via CIK to SEC 13F (just landed), EDGAR financials, and GLEIF (LEI). "
            "The 'sold before the news broke' detector."),
        "priority_tier": "1",
        "notes": (
            "Server-side load (~5M rows). DERA quarterly TSV zips. ISSUER_CIK ties to "
            "the company; OWNER_CIK ties to the insider (officer/director/10% owner). "
            "Both CIK columns are join-ready to the landed EDGAR universe."),
    },
]
