# Data traps — columns that look real but aren't, counts that lie. One line each, dated. Added by /wrap or by hand.

2026-08-30 — the scripts door logs in as ACCOUNTADMIN; a wrong command has no safety net.
2026-08-30 — the warehouse query log stores SQL text, not shell commands; price by table/statement pattern, not by script name. 500 rows = the cap, not a count.
2026-08-31 — zip loads keep only the LARGEST member per zip (08_bulk_ingest.sql:179); a count that's a multiple of the publisher's split size is the smell, but partial last chunks make totals non-round. 18 zip specs ride this path.
2026-08-31 — landing table name = UPPER(SOURCE_ID) is broken warehouse-wide; name-only registry↔landing joins fabricate hundreds of false orphans both ways.
2026-08-31 — SOURCE_REGISTRY.INCLUDE is a 'Y'/'N' STRING; Python truthiness counts 'N' as true.
2026-08-31 — LEIE UPIN column holds empty strings, not NULLs; count() without nullif(trim()) overcounts 14x.
2026-08-31 — checkpoint-sum = landing-count proves nothing about never-attempted files: both sides are zero. 13F missed 7 of 53 zips while summing exactly.
2026-08-31 — FDA_DT is the receipt date; it smears quarter-file boundaries. Reconcile FAERS by run id, never by event-date histogram.
2026-08-31 — the name-matcher's first-12-chars rule passes UNIVERSITY OF MICHIGAN = UNIVERSITY OF MISSOURI; ~12% false-positive on generic org names.
2026-08-31 — dbt test warn ≠ small: this run's 246 warns hide 99.4M failing rows.
2026-08-31 — Part D prescriber-drug has NO year column; one load run = one data year (DY22), not a series.
2026-08-31 — some loaders write audit columns UNPREFIXED (LEIE: INGESTED_AT not _INGESTED_AT); check before referencing.
2026-08-31 — USAspending landing tables carry case-sensitive lowercase and digit-leading column names; unquoted SQL resolves uppercase and misses.
2026-08-31 — the timeline rollup tables freeze the planned/actual tag at build time; it ages past current_date. Guard green also ≠ TIMELINE schema clean — nothing walks warehouse→registry.
2026-08-31 — identical row counts ≠ identical tables: hash before dropping, always. But raw HASH_AGG lies the other way too: the 8 ICIJ "different vintage" copies were the SAME snapshot with different blank spellings ('', NULL, 'NA', 'None', 'N/A', 'n/a') — blank-normalize before hashing or every loader pair "differs". Verdict: reports/row1/icij_vintage_verdict_2026-08-31.md.
2026-08-30 — portal_recon/ looks dead by import scan; connect/keys.py sys.path-imports its tagger by bare file name. Grep file names before retiring a folder.
2026-08-30 — "1,121" is the hard-ID edge count in lab_map facts, NOT the test count. The two got copy-crossed once already.
2026-08-30 — typing-layer tests query live marts but carried no snowflake marker until today; unmarked tests can burn credits from a plain pytest run.
- 2026-08-31 — CONNECT_WATERMARK content-key survives things it shouldn't: a table can be pinned "current" while SPINE_KEYSET_LIVE holds zero rows for it. connect-one then silently no-ops. Check keyset count, never the watermark, to know if a table is wired.
- 2026-08-31 — KEY_TYPE columns were CTAS-inferred VARCHAR(12)/(8); any key name over the width crashes MERGEs mid-run, leaving keyset-without-index half-states. All widened to 32; regression test in tests/test_keys_normalize.py.
- 2026-08-31 — reslice_discover's pair query has no size cap: a non-spec table with millions of keys blows Snowflake's 128MB LOB limit and kills the whole run BEFORE config pinning, so the next run redoes everything. FED_USASPENDING_CONTRACTS was the trigger; its graph keys are removed, the class remains.
- 2026-08-31 — registry SOURCE_ID is mixed-case and the index's SOURCE_TABLE is upper: name joins silently drop every lowercase registry row. Map via SOURCE_FRESHNESS.LANDING_FQN first, case-blind name second.
2026-09-01 — "never landed" by registry-vs-watermark SOURCE_ID join lied twice (FEC contributions, OpenSanctions): registry doubles and missing watermark credit both fake absence. LIKE-search LANDING table names before queuing any load.
2026-09-01 — the watermark lies BOTH ways: fed_cms_tic_mrf and fed_cms_hpt_enforcement have watermark rows and zero landed data. Watermark membership proves nothing in either direction.
2026-09-01 — FED_FEC_COMMITTEE_TO_COMMITTEE is 93% 15J earmark memos with MEMO_CD='X'; summing with itcont double-counts the same dollar under different CMTE_ID and SUB_ID. Filter MEMO_CD <> 'X' first.
2026-09-01 — FED_FCC_LICENSING.EIN is 100% empty string, 1.69M rows; detect_key fires on names. Count distinct before calling any column a key.
2026-09-01 — count parity is not coverage when the source prunes: GLEIF drops ended relationships, so a BIGGER new vintage still lost July's dead links. Rescued to RAW.RETIRED.INTL_GLEIF_RR_VINTAGE_20260731.
2026-09-01 — FED_USASPENDING_CONTRACTS_FULL is exactly 20,000,000 rows — a cap, superseded by _R2 (93M, wired); ASSISTANCE_FULL 19.9M unverified either way.
2026-09-01 — FED_HOUSE_DISBURSEMENTS ships SUBTOTAL ROWS INLINE: 371K rows (7.6%) with DESCRIPTION LIKE '%TOTALS%' hold $48.4B of the $64.5B naive sum. Filter them out or every dollar total is ~4x reality; detail-only ≈ $1.5B/yr matches the House appropriation.
2026-09-01 — FED_HOUSE_FD_PTR_INDEX.DOCID is NOT unique: the Clerk re-lists amendments in every year's zip (41,883 rows, 41,860 distinct). NO natural key exists: DOCID+INDEX_YEAR also fans out (18 exact-dupe row groups); dedup on hash(*). Only DOCID 9110829 legitimately spans years.
2026-09-01 — FED_HOUSE_DISBURSEMENTS.AMOUNT is TEXT and 6 rows hold column-shifted junk from embedded commas; bare sum() throws — always try_to_number. SOD_QUARTER has 42 spellings in 6 styles; parse with care.
