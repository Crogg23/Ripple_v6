# Warehouse Verification — 2026-08-11

**The question this answers:** "Do I have a working data warehouse that is ACCURATE
and RELIABLE or not?" — measured, not asserted. This session fixed nothing (by
design); it measured questions 5–10 of the nine-ways-data-can-be-wrong frame.
Questions 1–4 were swept and fixed on 2026-08-10/11.

## Verdict in one paragraph

The core is real: 16 of 18 records spot-checked field-by-field against the
publishers' own sites match exactly, and of the 181 sources where a publisher
total could be found, 128 (71%) are complete. But roughly 50 of 558 sources are
materially wrong in a way that would produce a confident, wrong chart today:
33.5M exact-duplicate rows (mostly one runaway loader), one table loaded with
the wrong file entirely, one national registry with a blank key column and
epoch-corrupted dates, 30 sources materially short vs the publisher, and 8
holding more than the publisher advertises.

## Counts per question

| # | Question | Coverage | Result |
|---|----------|----------|--------|
| 5 | Completeness vs publisher | all 558 sources attempted | 128 COMPLETE / 30 SHORT / 8 OVER / 15 declared samples / 376 UNKNOWN (publisher advertises no total) |
| 6 | Are ID/join keys real? | 590 of 606 mart tables scanned (16 errored, listed below) | 104 ID-named columns ≥99% blank across 43 tables; FAA registry tail-number key 100% blank; plus known truncated-LEI issue (already documented) |
| 7 | Are values correct? | 18 tables, 1 record each, 2–3 fields vs publisher | 16 MATCH, 2 MISMATCH (OpenSanctions epoch birth dates; NCUA call reports = wrong file) |
| 8 | Double-counting | 590 tables, full-row-hash | 33 tables >1% exact dups; 33.5M duplicate rows total; 17 tables serious (>10%) |
| 9 | Dates/text mangled | dates: full scan; text: 2,000-row sample/table | 9 date columns >50% epoch-1970 across 6 sources; 1970-01-01 sentinel birth dates in sanctions; mojibake in only 9 tables at ≤1.25% of sampled rows |
| 10 | Grain / uniqueness | repo analysis | 505 of 607 marts carry a dbt uniqueness test; 1 declares grain without a test; NO evidence the dbt test suite has been run recently (no run artifacts; last dbt log 2026-07-31) |

## Ranked list of what is genuinely broken

1. **FHFA NMDB (mortgage database), 19,054,246 rows — 7,204 real.** Every
   distinct row repeated 1,612–202,350 times. A paginated loader re-fetched the
   same content in a loop. Any aggregate over this table is wrong by ~2,600x.
2. **NCUA call reports (121,713 rows) — wrong content.** Rows are the
   account-description dictionary sheet (header strings like `CU_NUMBER` as
   values), not call-report data. The table is unusable as-is.
3. **FAA aircraft registry (314,417 rows) — key blank, dates corrupted.**
   `N_NUMBER` (tail number, the natural key) is 100% blank; all four date
   columns (`CERT_ISSUE_DATE`, `AIR_WORTH_DATE`, `EXPIRATION_DATE`,
   `LAST_ACTION_DATE`) are YYYYMMDD-parsed-as-epoch → all read 1970-08.
4. **CFTC COT (futures + financial): `AS_OF_DATE_IN_FORM_YYMMDD` 100%
   epoch-corrupted** (every row 1970-01-03). The second date column is correct,
   so the tables are rescuable. Both also sit under the EDUCATION schema
   (routing-bug residue — repo files were moved 2026-08-11, warehouse schemas
   were not). Also SHORT: publisher full history 287k rows vs our 16.8k.
5. **ForeignAssistance.gov: 3,967,456 rows, 97.6% exact duplicates** (95,658
   real). Same runaway-loader shape as #1.
6. **openFDA family: 8 landing tables truncated/wiped** (1–2,542 rows) while
   their marts are full and match publisher totals — the raw copies were lost
   after the marts were built. Two marts ARE short vs publisher: MAUDE device
   events (2.7M of 25.7M) and establishment registrations (263k of 333k).
7. **30 sources SHORT vs publisher** (full list in
   `outputs/_completeness_vs_publisher_2026-08-11.csv`). Largest gaps:
   Senate LDA filings 9% of 1.98M; Federal Register 9% of 1.0M; CFTC COT 6%;
   GLEIF relationships 73% of 658k; SAM exclusions 9,000 of ~168k (round-cap
   trap) and its mart is stale at 2,940; FEMA NFIP community status 77%;
   ransomware victims 63%; plus small/husk sources (SEC EDGAR 200 rows, OSF 10,
   NSF 125, Oyez 25, voteview 3%, French open-data portal 4%).
8. **8 sources OVER what the publisher advertises**: GLEIF reporting exceptions
   9.5x; EPA ECHO 2.1x vs "1.5M+ facilities" (may be partly legit growth);
   4 FEC bulk tables 1.2–2x current single-cycle files (multi-cycle loads under
   one source id — needs a cycle column check, may be intentional); CDC portal
   catalog 15,000 vs 1,471 assets; OWID fossil-share 30% over.
9. **Remaining exact-duplicate tables** (>10%, ≥1,000 rows): EPA ICIS Title V
   certs 81%, Google political-ads creative mapping 80%, FDA FAERS outcomes
   78%, DHS immigration stats 77%, EPA/NPDES informal enforcement 48%/42%, UK
   sanctions list 42%, court financial disclosures 38%, FEC committees 23% /
   candidates 19%, PBGC 10%. Also: senate-trades exists twice as two identical
   sources; several marts hold exactly 2x their landing table (GLEIF
   relationships, MSHA accidents, NHTSA investigations, FBI crime data —
   direction varies).
10. **104 dead ID columns across 43 tables** (≥99% blank/sentinel) — the
    silently-empty-column class again, this time in ID-named columns
    specifically (NTSB docket numbers, biorxiv funder IDs, NSF EINs, etc.).
11. **OpenSanctions birth dates: 7,406 rows read 1970-01-01** (epoch sentinel
    for unknown), plus 5 rows in 2068 (century-pivot). Purple Book approval
    dates also show 2069 pivots. 56 far-future date columns found overall; most
    are legitimate expiration dates, the pivot cases are not.
12. **Uniqueness tests exist but may not run.** 505/607 marts declare
    uniqueness tests, but there are no dbt test artifacts in the repo and the
    last dbt log predates the last two weeks of mart rebuilds. Unverified
    guards are not guards.
13. **16 tables errored out of the scan** (numeric overflow / cursor issues) —
    ICIJ Offshore Leaks (6 tables), OpenSanctions default, ICE detainers, two
    SEC fund tables, EIA balancing authority, and 5 others; listed in the scan
    JSONL. Not yet verified either way.
14. **Cosmetic:** mojibake in 9 tables at ≤1.25% of sampled rows (NOAA storm
    events worst); Treasury DTS holds a literal "null" category string; senate
    trades hold embedded HTML markup in asset descriptions.

## What was verified clean

- 128 sources hold everything the publisher advertises (incl. the two big
  re-pulls from 2026-08-10: bank directory 27,836 exact; daily cash ledger
  478,149 exact — the sweep's stale-input SHORT on the ledger was re-checked
  live and is COMPLETE).
- 16 of 18 value spot-checks matched the publisher field-for-field, including
  FDIC, FEC, FJC judges, NTSB, CMS nursing homes, FDA 510(k), SCDB, UK
  Companies House, FRA accidents (down to a $4,000 damage figure), MSHA mines,
  NHTSA complaints, Treasury DTS (3 rows exact), Senate PTR, EPA Superfund,
  IHS facilities, DPRK missile tests.
- 557 of 606 mart tables have no material exact-duplicate problem.
- Encoding is broadly sound (9 tables, low rates).
- FEMA disaster-aid reload was mid-flight during the sweep (20.1M of 25.9M at
  measurement) — its SHORT verdict is expected and will self-resolve.

## Method + evidence

- Completeness: 10 agents, publisher APIs/pages only, no warehouse compute →
  `outputs/_completeness_vs_publisher_2026-08-11.csv` (input row counts were a
  day-old snapshot; SHORT/OVER rows re-checked against live metadata).
- Key/date/dup scan: one aggregate query per mart table (counts, approx
  distinct, length bounds, min/max, sentinel counts, 1970/future date counts,
  full-row-hash distinct) → `outputs/_mart_key_date_dup_scan_2026-08-11.jsonl`.
- Value spot-checks: 3 sample rows per table, verified live against publisher →
  `outputs/_value_spot_checks_A_2026-08-11.csv`, `_B_`.
- Encoding: 2,000-row block sample per table, mojibake regex →
  `outputs/_mart_mojibake_2026-08-11.jsonl`.
- Grain test coverage: parsed dbt schema files; no warehouse compute.
- Warehouse cost: ~$2–4 (one aggregate pass over 590 tables + sampled scans on
  an X-Small; metadata queries free).

*Nothing was fixed in this session by design; every defect above is logged, not
repaired. No publish decisions are implied anywhere in this report.*
