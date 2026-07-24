# Box 1 Acquisition Wave — Make the Library Impressive

## Context

The warehouse currently holds **1,800 tables / 358M rows / 15GB** in LIBRARY_RAW.LANDING. The heavy-harm sources are full-depth, but Box 1 ("find all public data available — healthcare, finance, politics, YOU NAME IT") demands broader coverage. Chris's instruction: keep building the library wide before connecting it.

Key unlocks this session:
- **SAM API key provided** (`SAM-2d889032-278e-4d2b-9819-69ad86a0293d`) — SAM exclusions were parked, now unblocked
- **Loader capabilities proven:** manifest (multi-URL append), members (one-zip-to-many-tables), gzip-on-fly, headerless, JSON/VARIANT
- **Missing capability:** manifest+members combo (many zips, each with named members, append per member across all) — needed for SEC full history

## Priority Order and Rationale

| # | Source | Why Now | Expected Rows | Loader Path |
|---|--------|---------|---------------|-------------|
| 1 | SAM Exclusions | Key just provided; ~100K records; fast win; links to entity spine via UEI/NPI/name | ~100K | Paginated JSON API (existing script, un-cap) |
| 2 | USASpending Contracts | Where ALL federal contract money goes; massive; on egress already; plain manifest | 50-100M+ | Manifest (enumerate S3 bucket) |
| 3 | USASpending Assistance | Grants/loans/aid — the other half of federal awards | 50-100M+ | Manifest (same approach) |
| 4 | SEC Insider Full History | Only have 1 quarter (271K rows); full = 35 quarters | 2-5M | NEW: manifest+members combo |
| 5 | FEC Remaining Bulk | Committees, candidates, PAC summaries — completes the political money picture | 1-5M | Manifest (existing capability) |
| 6 | IRS 990 Index Expansion | Have 3 years (2.2M rows); full = 12+ years | 5-10M | Manifest (extend existing spec) |

## Implementation Steps

### Task 1: SAM Exclusions (~100K rows)

**What exists:** `scripts/sam_exclusions_load.py` — a paginated JSON loader that caps at 1 page. The API at `https://api.sam.gov/entity-information/v4/exclusions` returns pages of 1,000 records (nested JSON flattened to ~20 columns).

**Work needed:**
1. Add `api.sam.gov` to the `RIPPLE_BULK_EGRESS` network rule (ALTER NETWORK RULE ... ADD)
2. Store the API key: update `library-onboarding/.env` with `SAM_API_KEY=SAM-2d889032-...`
3. Un-cap the page limit in `sam_exclusions_load.py` (remove the early-stop after page 1)
4. Run the full pull — ~100 pages at 3s sleep = ~5 min wall clock
5. Validate: row count should be ~100K, density check passes, atomic swap lands

**Alternative (server-side):** The SAM API needs pagination (100 requests) with 3s throttle. Running client-side from this shell is actually simpler than building a server-side paging proc in Snowflake. The existing script already has backoff/retry logic. Stick with client-side.

**Join keys for later (Box 2):** UEI, CAGE code, NPI (some exclusions are healthcare providers), name fields.

---

### Task 2-3: USASpending Full Award History

**Structure:** `files.usaspending.gov/award_data_archive/` is an S3 bucket listing. Files named `FY{YEAR}_{AGENCY_CODE}_{TYPE}_Full_{DATE}.zip`. Each zip contains one CSV. Two types: `Contracts_Full` and `Assistance_Full`.

**Work needed:**
1. Parse the S3 XML listing to enumerate all `Contracts_Full` zip URLs (likely 500+ files across FY2007-FY2026 x ~30 agencies)
2. Build a manifest spec with those URLs — but the manifest will be huge. Consider: group by FY or process in batches to avoid staging 500 files simultaneously.
3. Each zip contains one CSV; the loader's manifest path already handles `kind='zip'` with a single member. Verify column consistency across years (USASpending format may change between FYs).
4. Load Contracts first (already have 6.3M rows in `FED_USASPENDING_CONTRACTS` — the existing rows may be from one agency/FY only). Strategy: build the new full table alongside, then swap.
5. Repeat for Assistance.

**Size concern:** At 245MB per zip for large agencies and hundreds of zips, total raw data could be 50-100GB. The gzip-on-fly /tmp cap (~9GB) means we need to process zip-by-zip (each zip is individually small enough). Manifest loader already iterates — this should work.

**Egress:** `files.usaspending.gov` already on the rule. No change needed.

---

### Task 4: Build manifest+members Combo Loader

**Why:** SEC insider data publishes quarterly zips, each containing 4 TSV files (SUBMISSION, REPORTINGOWNER, NONDERIV_TRANS, DERIV_TRANS). To get the full back-catalog, we need to iterate 35 quarterly zips and append each member type across all zips.

**Design:**
```
New spec shape:
{
  "source_id": "FED_SEC_INSIDER",
  "manifest": [list of quarterly zip URLs],
  "members": [{pattern, suffix, delimiter, has_header}...],
  "kind": "zip"
}
```

When BOTH `manifest` AND `members` are present, the new code path:
1. Iterate each URL in the manifest (the zip files)
2. For each zip: fetch to stage, then for each member pattern: unzip member to .gz
3. On FIRST zip: derive columns for each member (from first file's header)
4. COPY each member's .gz into its corresponding staging table (appending across zips)
5. After ALL zips processed: finalize each member table (stamp, density, swap)

This is essentially `_load_manifest` logic (iterate URLs) wrapping `_load_members` logic (per-zip member extraction), with the key difference that member tables ACCUMULATE across all zips rather than being finalized per-zip.

**Location:** New function `_load_manifest_members(s, ...)` in [scripts/server_side_load.py](scripts/server_side_load.py), dispatched from `load_spec()` when both `manifest` and `members` keys are present.

---

### Task 5: SEC Full Insider History

**Source:** `https://www.sec.gov/files/structureddata/data/insider-transactions-data-sets/{YYYY}q{Q}_form345.zip`
Available from 2016q3 through 2025q1 = ~35 files.

**Work needed:**
1. Build the manifest list (35 URLs)
2. Use the new manifest+members combo with existing member patterns from the `FED_SEC_INSIDER` spec
3. Load — expect 2-5M total across all 4 tables
4. The current single-quarter data (271K rows) gets replaced by the full history

**Egress:** `www.sec.gov` already on the rule.

---

### Task 6: FEC Remaining Bulk

**What's missing:** FEC bulk downloads include committee master (`cm`), candidate master (`cn`), candidate-committee linkage (`ccl`), PAC summary (`webk`), and individual contributions (already have 84M). The committee/candidate/PAC files are small CSVs on fec.gov/files/bulk-downloads that 302 to the GovCloud S3 bucket (already on egress).

**Work needed:**
1. Add manifest specs for: committee master (multi-cycle), candidate master (multi-cycle), PAC summaries (multi-cycle)
2. Handle headerless format (FEC bulk files have no header row — known pattern, `has_header: false`)
3. Load each as a manifest into its own table

---

### Task 7: IRS 990 Index Expansion

**Current:** 3 years (2023-2025) covering 2.2M filings.
**Full:** `apps.irs.gov/pub/epostcard/990/xml/{YEAR}/index_{YEAR}.csv` from 2014 onward.

**Work needed:**
1. Expand the manifest in the existing `FED_IRS_990_EFILE_INDEX` spec to include 2014-2022
2. Re-run the load (manifest appends all years into one table)

---

## Verification

For each source after loading:
- Row count matches expected magnitude (query INFORMATION_SCHEMA)
- Density check passes (via `ingest.assess_density`)
- Key join columns are populated (spot-check NULLs on UEI/NPI/EIN/CIK as applicable)
- Registration in SOURCE_REGISTRY + INGEST_RUNS log entry

## Critical Files

- [scripts/server_side_load.py](scripts/server_side_load.py) — Main loader; add manifest+members combo here
- [scripts/server_side_specs.py](scripts/server_side_specs.py) — All source specs; add USASpending, expand SEC, add FEC bulk
- [scripts/sam_exclusions_load.py](scripts/sam_exclusions_load.py) — SAM exclusions; un-cap page limit
- [infra/ddl/08_bulk_ingest.sql](infra/ddl/08_bulk_ingest.sql) — DDL for egress rule (add api.sam.gov)
- [library-onboarding/.env](library-onboarding/.env) — Store SAM_API_KEY
