# Gap Acquisition Campaign — Status (2026-07-26)

Mission: land the 10 highest-priority connective-tissue datasets into
`LIBRARY_RAW.LANDING`. All loaders are checkpointed, run as detached
processes, and a watchdog (`scripts/campaign_watchdog.ps1`) relaunches any
that die until they print DONE.

## Landed & validated

| # | Dataset | Tables | Rows | Validation |
|---|---------|--------|------|-----------|
| 1 | GLEIF Level 2 | `INTL_GLEIF_RELATIONSHIPS` | 481,900 | 99.92% of StartNode LEIs join `INTL_GLEIF.LEI` (criterion: >95% ✅). Packet's ~2M estimate was stale — current golden copy is 482K relationships. |
| 1 | GLEIF Reporting Exceptions | `INTL_GLEIF_REPEX` | 6,259,489 | full file, sha logged |
| 9 | CMS NH Penalties | `FED_CMS_NURSING_HOME_PENALTIES` | 16,180 | 100% CCN join to `FED_CMS_NURSING_HOME` ✅. NOTE: current CMS file only carries recent penalty cycles (packet expected ~100K — historical snapshots would need archive pulls). |
| 9 | CMS NH Deficiencies | `FED_CMS_NURSING_HOME_DEFICIENCIES` (+`_FIRE_`) | 418,479 + 200,030 | scope/severity + F-tags present |
| 10 | EPA↔Corporate crosswalk | `XC_EPA_CORPORATE_CROSSWALK` | 499,995 facilities | 9,456 LEI-matched (1.9%), 1,478 ultimate parents, 1,207 CIKs, 6,889 UEIs. See "crosswalk reality" below. |

## In flight (detached, watchdog-supervised)

| # | Dataset | Progress at write time |
|---|---------|------------------------|
| 3 | FDA FAERS 2004–2026 (DEMO/DRUG/REAC/OUTC/INDI) | ~10/89 quarters, resuming; checkpoint `logs/faers_checkpoint.json` |
| 5 | CourtListener dockets (2026-06-30 bulk, 5GB bz2) | download done, PUT/COPY in progress |
| 6 | SEC 13F 2013Q2–2026 (53 quarterly zips → HOLDINGS/FILERS/SUBMISSIONS) | 2/53 zips |
| 7 | CPSC NEISS 1999–2025 + product-code lookup | 5 years + codes table done |
| 8 | DEA ARCOS full (WaPo 2006–2014, 6.9GB tsv.gz) | download ~15%, then PUT/COPY |

## Blocked — needs Chris (2-minute signups)

1. **#4 DOL WHD**: DOL retired all bulk CSVs (everything 301s to data.dol.gov).
   Only path is the v4 API with a free key: https://dataportal.dol.gov/api-keys
   → put in `library-onboarding/.env` as `DOL_API_KEY`.
2. **#2 SOPR lobbying**: Senate discontinued bulk XML (2020). Anonymous API is
   capped at 25/page @ ~6s/request (days for 1.97M filings). Free key at
   https://lda.senate.gov/api/register/ raises page size to 250 (~a day, feasible)
   → `LDA_API_KEY` in .env.
   I did not create accounts with your identity — that's your call.
3. **#7 CPSC SaferProducts incidents**: their CSV export endpoint returns
   503 "Under Construction" — server-side outage, retry in a week or two.
   (NEISS half of #7 is landing fine.)
4. **#5 CourtListener parties**: no bulk export exists (API/RECAP only).
   Dockets landed; parties would be a separate API crawl — decide if wanted.

## Crosswalk reality (item 10)

The packet expected 60–70% match. Actual: 1.9% overall, and the ">50% on
facilities with >10 enforcement actions" criterion fails (1/16). Two honest
reasons: (a) GLEIF only has 356K US entities — mostly financial/large firms,
while EPA facilities are mostly small operating LLCs; (b) our landed
FRS/ECHO tables were capped at 500K rows by the earlier discovery loader
(FRS is really ~4M facilities). The crosswalk is built correctly (exact +
fuzzy ladder, ultimate-parent via Level 2, CIK/UEI bridges, REVIEW_FLAG on
low confidence) — the ceiling is data coverage, not the method. Follow-up
options: re-land full FRS/ECHO uncapped, and/or bring in ECHO's parent
company field + SAM.gov entity registrations as the small-business bridge.

## Ops notes

- Loader logs: `logs/*_run*.log`; watchdog log: `logs/watchdog.log`.
- Every table has `_INGESTED_AT`, `_SOURCE_RUN_ID`, `_SRC_SHA256`
  (+ `_SRC_QUARTER`/`_SRC_YEAR`/`_SRC_FILE` where multi-file).
- Remaining validations to run when loads finish: FAERS drugname overlap
  with Part D, 13F/dockets row counts, NEISS weight column non-null.
