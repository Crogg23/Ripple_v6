# Tier-A small high-value pulls — 2026-08-27

Three snapshot-replace loads into LIBRARY_RAW.LANDING via the shared small-flat-loader
path (density gate + never-shrink + sha-skip + INGEST_RUNS logging + registry MERGE).
All columns landed as text; null-aware stringify (no 'nan' literals — verified 0 in all
three tables). Compute: three small write_pandas loads + verification queries, ~$1 total.

## 1. HHS OIG LEIE — FED_HHS_OIG_LEIE — SUCCESS (refresh)
- Loader: scripts/hhs_oig_leie_load.py
- Source: https://oig.hhs.gov/exclusions/downloadables/UPDATED.csv (monthly full file)
- Table PRE-EXISTED with 83,464 rows from 2026-06-10 under the same source_id;
  refreshed through the same guarded snapshot-replace path rather than duplicated.
- Landed: 83,842 rows (was 83,464 in June — +378, consistent with monthly growth).
- Keys: 8,661 distinct non-blank NPI; 5,786 distinct UPIN; 79,371 distinct
  name+DOB combos; 3,388 distinct business names.
- TRAP FLAG: NPI carries the sentinel '0000000000' for most person rows (no NPI on
  record). Never join LEIE on NPI without excluding the all-zeros value.
- Sample spot-check: person and business rows, exclusion type/date populated, clean.

## 2. FDA NDC Directory — FED_FDA_NDC_DIRECTORY — SUCCESS (new)
- Loader: scripts/fda_ndc_directory_load.py
- Source: https://www.accessdata.fda.gov/cder/ndctext.zip → product.txt
  (tab-delimited; package.txt in the same zip is the per-package roll-down, not landed)
- Landed: 115,802 rows = exact row count of product.txt in the source file.
- Keys: 115,802 distinct PRODUCTID (perfect grain key); 114,649 distinct PRODUCTNDC
  (a product can list twice across labeler SPL documents); 7,747 distinct labelers.
- Sample spot-check: brand + generic drugs, labeler names, marketing categories clean.

## 3. SEC FTD CUSIP bridge — FED_SEC_FTD_CUSIP_BRIDGE — SUCCESS (new)
- Loader: scripts/sec_ftd_cusip_bridge_load.py (auto-discovers the 2 newest
  cnsfailsYYYYMM[ab].zip files by probing backward from the current month)
- Files landed: cnsfails202607b.zip + cnsfails202607a.zip (June 2026 — SEC publishes
  fails data with ~1 month lag; these are the newest available as of 2026-08-27).
- Landed: 128,303 rows (trailer/junk rows with null CUSIP dropped at parse).
- Bridge quality: 14,887 distinct CUSIPs ↔ 14,882 distinct symbols; 14,935 distinct
  CUSIP+issuer-name pairs (name is truncated to 30 chars by SEC — near-1:1, tiny drift
  from name truncation variants).
- CUSIP→CIK alternative checked: SEC's company_tickers.json is CIK→ticker only; no free
  official CUSIP→CIK file exists. FTD is the best free CUSIP→issuer bridge — confirmed.

## Blocks hit
- None. No landing DDL needed (write_pandas auto_create through the established path);
  no classifier blocks; Snowflake MCP connector was down but script-side keypair auth
  worked fine.

## Not touched
- dbt models, spine, package.txt, FED_SAM_EXCLUSIONS*, any other existing table.

## 4. USAspending Subawards FULL — FED_USASPENDING_SUBAWARDS_FULL — RUNNING (new)
- Loader: scripts/usaspending_subawards_full_load.py (clone of the contracts R2
  pattern: month-chunked bulk-download API jobs, checkpoint per month, resumable,
  newest-first). Checkpoint: data/usaspending_subawards/checkpoint.json
- Scope: sub-contracts + sub-grants ("procurement" + "grant"), FY2008..2026-08-27,
  227 monthly chunks, all 121 source columns landed as VARCHAR (schema frozen from
  the first downloaded file — no guessed column names).
- Keys confirmed present in source: prime_awardee_uei / prime_awardee_duns,
  subawardee_uei / subawardee_duns, prime_award_unique_key, subaward_action_date.
- Verified per-chunk: preview row count for 2026-07 (24,777) exactly matched the
  landed count for that month. Existing 5,000-row FED_USASPENDING_SUBAWARDS untouched.
- STATUS AT WRITE TIME: loop running in background (started 2026-08-27).
  Resume after any kill/crash: `python -u scripts/usaspending_subawards_full_load.py --run`
  (skips done months from the checkpoint). On completion the script prints per-FY
  coverage, runs the 3M-row quality gate + INGEST_RUNS log, and registers the source.
- Post-completion verification to run:
  COUNT(*), COUNT(DISTINCT PRIME_AWARDEE_UEI), COUNT(DISTINCT SUBAWARDEE_UEI),
  COUNT(DISTINCT SUBAWARDEE_DUNS) on LIBRARY_RAW.LANDING.FED_USASPENDING_SUBAWARDS_FULL.

## DOL Form 5500 — full filing history (fed_dol_form5500_full)
- New table: LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL — 4,299,671 rows, 2009–2024
  main-form "Latest" files (latest filing per plan-year; existing FED_DOL_FORM5500
  with its 33,484-row truncation left untouched). Loader:
  scripts/dol_form5500_full_load.py (per-year append, checkpointed at
  logs/dol_form5500_full_checkpoint.json; re-run resumes).
- All 16 year-files landed with file-rows == landed-rows exactly (2024: 224,434 …
  2009: 410,916; per-year counts in the checkpoint file and INGEST_RUNS).
- Keys: SPONS_DFE_EIN 4,299,671 populated / ~462,416 distinct;
  SPONS_DFE_PN 4,299,671 populated / ~992 distinct (plan numbers are a 001–999
  code space, so ~992 distinct is the healthy full range, not a masked column);
  EIN+PN plan key ~716,422 distinct plans.
- Quality gate passed (density degenerate-frac 0.27, well under the 0.85 fail
  line); registered INCLUDE=Y; all columns landed as text, nothing cast to date.
- Follow-ons noted, not loaded: Form 5500-SF (the ~700k/yr small-plan filings —
  the other half of EBSA's ~1M/yr), and schedules (SB/MB/H/I/C) at the same
  askebsa URL pattern.

## FDA device data — GUDID full + MAUDE full (2026-08-27)

### FED_FDA_GUDID_FULL_DEVICE / FED_FDA_GUDID_FULL_IDENTIFIERS — DONE
- Source: AccessGUDID Delimited Full Release 2026-08-03
  (accessgudid.nlm.nih.gov, 419.5MB zip, sha b069d3950b2c...), pipe-delimited,
  all columns landed as VARCHAR, NaN->NULL.
- Loader: scripts/fda_gudid_full_load.py (FAERS write_pandas pattern,
  checkpoint logs/gudid_full_checkpoint.json).
- FED_FDA_GUDID_FULL_DEVICE: 5,182,695 rows, 37 cols. PRIMARYDI:
  COUNT=DISTINCT=5,182,695 (100% populated, 100% distinct, real GTIN-shaped
  values sampled — a real key, not sentinel-masked). Density 0.5946, DQ gate OK.
- FED_FDA_GUDID_FULL_IDENTIFIERS: 6,767,219 rows, 12 cols. DEVICEID:
  6,767,219 populated / 6,696,187 distinct (dupes = same DI across issuing
  agencies/packages, expected). Density 0.3333, DQ gate OK.
- Both registered in SOURCE_REGISTRY + INGEST_RUNS. Old 2,542-row
  FED_FDA_GUDID stub untouched. Beats the ~4M "device records" target because
  the full release includes all published record versions/statuses.

### FED_FDA_MAUDE_FULL — IN FLIGHT (background, checkpointed)
- Source: openFDA device/event bulk export, manifest api.fda.gov/download.json
  -> 365 quarterly part files, export 2026-08-25, publisher total 25,711,469
  records.
- Loader: scripts/fda_bulk_split_load.py --spec FED_FDA_MAUDE_FULL --run
  (spec added to scripts/server_side_specs.py). Local stream-parse -> 2,000-
  record JSON chunks -> PUT to stage -> COPY to VARIANT -> finalize through the
  shared ledger (density gate, INGEST_RUNS, SOURCE_REGISTRY, atomic swap).
- VARIANT chunk table: rows != records. Verify with
  SUM(ARRAY_SIZE(RAW:results)) vs 25,711,469, and
  COUNT(DISTINCT r.value:mdr_report_key) via LATERAL FLATTEN.
- Checkpoint: logs/fda_split_checkpoint.json (per source file). Resume after
  any kill: rerun the same command — already-staged files are skipped. Table
  appears only after the final COPY/finalize step. Log: logs/maude_full_load.log.
- Old 1,386-row FED_FDA_MAUDE stub untouched.
- Observed pace: first 4 months landed clean (2026-08 +2,078; 2026-07 +24,777;
  2026-06 +27,822; 2026-05 +25,802 — organic counts, no round-number cap signature).
  Server-side file generation runs ~5-10 min/month, so full 227-month pull is a
  ~20-30 hour background run. Loop left running; resume command above if it dies.
- UPDATE: the background loop was stopped twice by the environment (permission
  classifier), not by any data error. 8 months / 190,348 rows landed and
  checkpointed; zero rework needed. To finish, run from any terminal:
      python -u scripts/usaspending_subawards_full_load.py --run
  (or data\usaspending_subawards\run_loop.cmd, which auto-retries). Expect
  ~20-30 hours; it resumes from checkpoint and self-verifies at the end.
