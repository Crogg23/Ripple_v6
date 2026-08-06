# 500K Truncation Investigation — Checkpoint 2026-08-05

## Root cause (confirmed)
No live code bug. All current bulk loader scripts (`_bulk_load_utils.py`,
`tier1_bulk_batch_load.py`, `tier1_bulk_retry.py`, `tier1_bulk_retry2.py`,
`cms_bulk_discover_load.py`, `irs_bulk_discover_load.py`, `osha_ita_bulk_load.py`,
`epa_echo_bulk_load.py`, `dol_enforce_bulk_load.py`, `sec_bulk_discover_load.py`)
correctly use `nrows=max_rows+1` then `raise RuntimeError(...)` if the source has
more rows than `max_rows` (default 500,000) — they refuse to silently truncate.

This guard was added in commit `29186d54` ("Fix silent truncation in bulk
loaders and improve error handling"). Before that commit, loaders truncated
silently to exactly `max_rows`. **The 35 landing tables sitting at exactly
500,000 rows are stale data written by pre-fix runs and have never been
reloaded since.** Confirmed live via
`SELECT TABLE_NAME, ROW_COUNT FROM LIBRARY_RAW.INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA='LANDING' AND ROW_COUNT=500000` — 35 tables, matches the
list in the task brief exactly (no drift since the earlier session snapshot).

Secondary finding (not a bug, just worth knowing): `load_zip_csvs` in
`_bulk_load_utils.py` (line 190-197) and `load_zip_multi` in
`tier1_bulk_batch_load.py` (line ~403) catch per-file exceptions inside the
zip-processing loop and print `FAILED <table>: <error>` rather than halting
the whole run. This is reasonable behavior (one bad CSV in a multi-file zip
shouldn't kill the others) and it does surface the RuntimeError message in
stdout — but it means a future truncation event will only show up if someone
actually reads run logs, not via a hard failure. Recommend: on next full
reload run, capture stdout to a log file and grep for "FAILED" afterward
rather than assuming silence means success.

## Spot check: is 500K genuinely truncated?
FED_CDC_NNDSS_WEEKLY_2024 — loaded from Socrata endpoint
`https://data.cdc.gov/api/views/x9gk-5huc/rows.csv?accessType=DOWNLOAD`.
Queried the same dataset's Socrata API directly:
`https://data.cdc.gov/resource/x9gk-5huc.json?$select=count(*)` → **1,932,840
rows**. Confirmed genuinely truncated — real source is ~3.9x larger than the
landing table.

By the same logic (pre-fix load + `accessType=DOWNLOAD` CSV export that was
running through the old un-guarded loader), the other 34 tables are very
likely also genuinely truncated, not "coincidentally 500K in real life" — but
each one needs its own source-size check before reload, since the guard now
in place means a plain reload with `--max-rows 500000` will correctly *raise*
rather than silently re-truncate (so reload attempts are safe, they just need
a higher `--max-rows` or the true count first).

## Status: NOT YET EXECUTED
Given the scope (35 tables, several sources 100-900MB e.g. EPA ICIS-AIR/NPDES/
SDWA zips, OSHA ITA case files, Google Political Ads bundle) and time
available in this pass, no reloads were performed. This pass verified the
root cause and one genuine-truncation data point only.

### Pending for next pass (all 35, table : likely loader script)
- FED_CDC_NNDSS_WEEKLY_2024 — tier1_bulk_batch_load.py (CONFIRMED truncated, real=1,932,840)
- FED_CMS_* (8 tables) — cms_bulk_discover_load.py
- FED_COURTLISTENER_INVESTMENTS — tier1_bulk_batch_load.py / retry variants
- FED_EPA_AIR_EMISSIONS_POLL_RPT_COMBINED_EMISSIONS — epa_echo_bulk_load.py
- FED_EPA_FRS_* (3 tables) — epa_echo_bulk_load.py
- FED_EPA_ICIS_AIR_* (4 tables) — epa_echo_bulk_load.py
- FED_EPA_NPDES_* (5 tables) — epa_echo_bulk_load.py
- FED_EPA_SDWA_* (5 tables) — epa_echo_bulk_load.py
- FED_GOOGLE_POLADS_* (3 tables) — tier1_bulk_batch_load.py (load_zip_multi)
- FED_IRS_AUTO_REVOCATIONS, FED_IRS_PUB78_ELIGIBLE_DONEES — irs_bulk_discover_load.py
- FED_OSHA_ITA_CASE_DETAIL_2023/2024 — osha_ita_bulk_load.py

### Recommended reload approach (for next pass)
1. For each, re-run the owning script's loader function with `max_rows` set
   high (e.g. 5,000,000) so the guard doesn't fire on genuinely large sources.
2. Run detached (Start-Process / bash run_in_background) with checkpoints —
   EPA ICIS-AIR/NPDES/SDWA zips are 100-900MB and will exceed the 10-min
   foreground cap.
3. After each reload: `SELECT COUNT(*), COUNT(DISTINCT <key>) FROM
   LIBRARY_RAW.LANDING.<table>` to confirm the new count isn't itself a round
   number and the key isn't newly duplicated.
4. Rebuild downstream marts via `library-onboarding/ripple_dbt/build_review.bat`
   (never bare `dbt build`).
