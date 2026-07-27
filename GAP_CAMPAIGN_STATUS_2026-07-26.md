# Gap Acquisition Campaign — Status (2026-07-26, tied off ~19:00 PDT)

Mission: land the 10 highest-priority connective-tissue datasets into
`LIBRARY_RAW.LANDING`. **All loaders and the watchdog have been stopped
cleanly.** Every partial in-flight unit (a quarter/zip/year that was mid-load
when killed) was purged from Snowflake, so every table below is consistent —
no half-loaded rows anywhere. All loaders are checkpointed in `logs/*.json`
and safe to resume any time with `python scripts/<name>.py --run` — they will
pick up exactly where they left off, nothing re-downloads or double-loads.

## Landed & validated (stable, nothing pending)

| # | Dataset | Table(s) | Rows |
|---|---------|----------|------|
| 1 | GLEIF Level 2 relationships | `INTL_GLEIF_RELATIONSHIPS` | 481,900 (99.92% join to `INTL_GLEIF.LEI` — criterion >95% ✅) |
| 1 | GLEIF Reporting Exceptions | `INTL_GLEIF_REPEX` | 6,259,489 |
| 9 | CMS NH Penalties | `FED_CMS_NURSING_HOME_PENALTIES` | 16,180 (100% CCN join ✅) |
| 9 | CMS NH Health/Fire Deficiencies | `FED_CMS_NURSING_HOME_DEFICIENCIES` / `_FIRE_` | 418,479 / 200,030 |
| 5 | CourtListener dockets | `FED_COURTLISTENER_DOCKETS` | 71,677,647 (full bulk export, all courts) |
| 10 | EPA↔Corporate crosswalk | `XC_EPA_CORPORATE_CROSSWALK` | 499,995 facilities (1.9% LEI match — see "crosswalk reality" below) |

## Landed partially — safe to resume, currently paused

| # | Dataset | Tables | Rows so far | Checkpoint |
|---|---------|--------|-------------|------------|
| 3 | FDA FAERS | `FED_FDA_FAERS_{DEMO,DRUG,REAC,OUTC,INDI}` | 838K / 3.16M / 3.53M / 848K / 1.17M | 11 of 89 quarters (2004q1–2006q3) in `logs/faers_checkpoint.json` |
| 6 | SEC 13F | `FED_SEC_13F_{HOLDINGS,FILERS,SUBMISSIONS}` | 39.4M / 126K / 126K | 15 of 53 quarterly zips in `logs/sec13f_checkpoint.json` |
| 7 | CPSC NEISS | `FED_CPSC_NEISS` (+ `_CODES` lookup, complete) | 2,793,015 | 8 of 26 years (1999–2006) in `logs/neiss_checkpoint.json` |
| 8 | DEA ARCOS full | — | **0** | Never completed a COPY; scaffold table dropped. Local 6.9GB download may still be cached in scratch — loader will re-verify hash and re-PUT on next run. |

To resume any of these, just re-run the same command:
```
python scripts/fda_faers_load.py --run
python scripts/sec_13f_load.py --run
python scripts/cpsc_neiss_load.py --run
python scripts/dea_arcos_full_load.py --run
```
The connection kept dropping mid-download during this session (not a bug in
the loaders — all four have retry logic and resumed cleanly each time), which
is what made the remaining ~78 FAERS quarters / 38 13F zips / 18 NEISS years
slow going. Re-running on a more stable connection should finish them in a
few hours, unattended.

## Blocked — needs Chris (2-minute signups)

1. **#4 DOL WHD**: bulk CSVs retired; needs a free key from
   https://dataportal.dol.gov/api-keys → `DOL_API_KEY` in `library-onboarding/.env`.
2. **#2 SOPR lobbying**: bulk XML discontinued (2020); anonymous API capped at
   25/page. Free key at https://lda.senate.gov/api/register/ raises it to 250
   → `LDA_API_KEY` in `.env`.
3. **#7 CPSC SaferProducts incidents**: CSV export endpoint returns 503
   "Under Construction" — server-side outage on their end, retry later.
4. **#5 CourtListener parties**: no bulk export exists (API/RECAP only,
   would be a separate crawl) — dockets are landed; decide if parties are
   worth a dedicated API-based loader.

## Crosswalk reality (item 10)

Packet expected 60–70% match; actual 1.9%. Method is sound (exact + fuzzy
name ladder, ultimate-parent via Level 2, CIK/UEI bridges, REVIEW_FLAG on
low confidence) — the ceiling is data coverage: GLEIF only has 356K US
entities (mostly financial/large firms) against EPA's facility set, and our
landed FRS/ECHO tables are capped at 500K rows by an earlier discovery
loader (full FRS is ~4M facilities). Re-landing FRS/ECHO uncapped would be
the highest-leverage next step here.

## Ops notes

- Loader logs: `logs/*_run*.log` / `*_err*.log`; watchdog log: `logs/watchdog.log` (stopped).
- Every landed table carries `_INGESTED_AT`, `_SOURCE_RUN_ID`, `_SRC_SHA256`
  (+ `_SRC_QUARTER`/`_SRC_YEAR`/`_SRC_FILE` where multi-file), so provenance
  is intact even mid-campaign.
- Remaining validations once fully landed: FAERS drugname↔Part D overlap,
  NEISS weight-column completeness, 13F CUSIP↔ticker join rate.
