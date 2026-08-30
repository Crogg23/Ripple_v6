---
name: warehouse-truncation-findings-2026-08-22
description: "2026-08-22 confirmed truncations — CONTRACTS_FULL is a 2-3-months-per-FY sample (1M/FY exactly, no loader in repo); PSC snapshot was 56% loaded (silent chunk-boundary death); DOL API quirks for the OSHA re-pull"
metadata: 
  node_type: memory
  type: project
  originSessionId: 4154f5c7-5881-4657-8fd6-ec08f82f44ab
  modified: 2026-08-22T18:27:39.478Z
---

Measured 2026-08-22 during the warehouse cleaning sprint:

- **`FED_USASPENDING_CONTRACTS_FULL` (20,000,000 rows) is a truncated sample, not full data.** Exactly 1,000,000 rows per FY 2007–2026, and each FY's `action_date` spans only ~2–3 months (FY2024 = Jun 24–Aug 18). No loader for it exists in the repo. Re-pull is a Chris-priced decision ([[feedback-no-publish-nudging]] class: RED-lane money). Any per-year or trend analysis on this table is invalid until re-pulled.
- **`UK_COMPANIES_HOUSE_PSC`**: source zip (`library-onboarding/_dl/ch_psc_snapshot.zip`, still on disk) holds 15,804,612 records; only 7,000,000 loaded — original streamed load died at the 28th 250k-chunk boundary with no error. Remainder re-loaded via `library-onboarding/_dl/resume_psc.py` (checkpointed). The original loader also wrote literal `'None'` strings ([[loader-writes-nan-sentinel]] class) — repaired via UPDATE 2026-08-22.
- **DOL API (for the OSHA inspections re-pull, `scripts/osha_inspections_api_load.py`)**: key in `.env` works; old enforcedata.dol.gov bulk zips are dead (Drupal page). Keyset-paginate on `activity_nr` (offset paging risks caps); `filter_object` value 0 returns a 500 — start at 1; rate limits are aggressive (429 walls lasting many minutes) so the loader waits up to 10 min per retry, 30 retries. Checkpoint: `data/osha_inspections/checkpoint.json`.
- **write_pandas `auto_create_table` types columns off the first batch** — an all-null column on page 1 lands as NUMBER and later text kills the append. Always CREATE TABLE explicitly with VARCHAR columns for landing.

**Why:** three separate "load logged success but data is missing/corrupt" events in one day — silent truncation is this platform's #1 recurring failure class.
**How to apply:** any exact round row count (1M/FY, 7M, 10k) is a truncation hypothesis until date-coverage inside partitions is checked; a load is not done until row count is reconciled against the source's own count.
