# Warehouse Repair — 2026-08-11 (same-day answer to the verification)

The morning verification asked "is the warehouse accurate and reliable?" and
found ~50 broken sources across 14 defect classes. This session repaired,
guarded, or honestly labeled every class the same day. Delta below, in the
same frame.

## Scoreboard vs the ranked list

| # | Verification finding | Outcome |
|---|---|---|
| 1 | Mortgage DB 19.05M rows, 7,204 real (~2,600x dups) | **FIXED** — mart rebuilt at 7,204 true rows (dedupe on cast values); guard test red→green; raw-layer swap queued for human |
| 2 | Credit-union call reports = wrong file (dictionary sheet) | **FIXED** — correct roster + financial files reloaded (4,336 CUs, charter key unique); Navy Federal total assets matches NCUA's own published figure exactly; old models retired, table drop queued |
| 3 | Aircraft registry blank key + epoch dates | **FALSE ALARM (stale twin)** — defect lives only in the retired July snapshot already on the drop list; the current registry mart has 312k distinct tail numbers and real dates |
| 4 | Commodity-trading epoch date + 6% of history | **FIXED** — date cast corrected (guard green); futures history backfilled 1986–2026 to the publisher-exact 287,053 rows, spot-checked against a 2010 file; financial extended 2010+; one mis-sliced bundle (7,790 rows) shielded in the mart pending a human DELETE, and 2006-09 lands after it |
| 5 | Foreign-aid 97.6% duplicates | **FIXED** — mart rebuilt at 95,658 unique rows; guarded; swap queued |
| 6 | 8 FDA landing tables "wiped" | **RETRACTED — false alarm.** They are JSON chunk tables (1 row ≈ 2,000 records); counted correctly all are full and publisher-matched. Checker fix documented. Genuinely short remain: device adverse events 2.7M/25.7M and establishment reg 330k/333k — priced, human go/no-go |
| 7 | 30 sources SHORT | **7 re-pulled to publisher-complete** (sanctions-exclusions 167,928; voteview 113,512 exact; French portal 130,431; CDC catalog 1,471 exact; GLEIF relationships 484,142 = golden-copy exact; FEMA flood-community book complete; ransomware complete) — 3 of those "SHORT" verdicts were the publisher's own bad metadata, now documented. **10 husks labeled** as declared samples (control table now 23 entries). Remaining: lobbying (key-gated on Chris), federal register + device adverse events (priced, gated), disaster aid (still loading) |
| 8 | 8 sources OVER | **CLOSED, zero data repairs** — GLEIF exceptions = true grain (3.14M entities × 2 directions, all unique; wrong publisher figure); FEC = intentional multi-cycle (labeled); EPA facilities unique (ad-copy total); CDC was the pager bug (re-pulled exact); OWID = version drift (labeled) |
| 9 | 33 exact-dup mart tables | **FIXED** — root causes: missing dimension columns (immigration stats: 6 columns restored, dups were fake), blanket numeric casts nulling text keys (corporate-relationship files), single-load/append dup loads (4 EPA tables, FDA outcomes, political-ads mapping, court disclosures, pension agency — deduped with documented qualify), publisher-side byte-dups (UK sanctions 652 — deduped; senate trades 4.5% — documented as intentional). 10 duplicate/orphaned model files retired. FBI crime "2x" was a deliberate pivot — false positive |
| 10 | 104 dead ID columns | **TRIAGED (all 193 by the honest rule)**: 61 publisher-absent (documented traps), 25 lost-in-ingest (ALL fixed today — casts, wrong-file, stale twin), 107 need source-file byte checks (backlog, outputs/dead_id_columns_triage_2026-08-11.md) |
| 11 | Date sentinels + century pivots | **FIXED + GUARDED** — sanctions birth dates: the "1970 sentinel" was year-only strings parsed as epoch seconds; now strict-format parse + raw preserved. Biologics approval dates: pivot rolled back 100y where future. Guard test verified red→green |
| 12 | dbt uniqueness tests never run | **RUN + WIRED** — first-ever full run: 1,173/1,186 pass; the 13 failures were all diagnosed (9 belonged to class-9/7 defects fixed today, 2 grain declarations corrected, 2 DB errors from stale models). Sanctioned test wrapper added; scheduled cadence needs Chris's DDL |
| 13 | 16 tables errored out of scan | **CLOSED** — scan hardened (extreme-date overflow), all 16 re-scanned clean (worst 0.2% dups); ICIJ offshore leaks fully verified |
| 14 | Cosmetic (mojibake, 'null' text, HTML) | **'null' repaired** (433k treasury cells; tool now takes any sentinel). Mojibake (≤1.25% sampled, 9 tables) and senate-trade HTML documented as known-cosmetic, not worth a reload |

## Guard tests added this session (the streak continues)

- Runaway-duplication guard on the two fixed marts (fails build at >1% exact dups)
- Epoch/pivot date guard (1970 pile-ups, future birth/approval dates) — both
  verified to FAIL on the broken state before the fix and pass after
- Duplication detection added to the degenerate-load detector (its documented
  blind spot — wholesale row repetition)
- Sha-guard in the commodity-trading history loader (refuses double-appends)
- Unit tests for the dedupe tool (offline suite: 2,807 passed)

## What is honestly still open

- Raw-layer cleanups are queued as human one-liners
  (reports/repair_session_chris_gates_2026-08-11.md): dedupe swap, wrong-file
  drop, 9 orphaned tables, the 7,790-row DELETE, superseded `_FULL` twins.
- Priced go/no-gos: device adverse events full pull (~3-6h, ~$5-10),
  establishment registrations top-up (<$1), federal register 1.0M docs
  (~$2-5 + hours).
- Key-gated: lobbying filings (biggest single completeness gap left),
  broadband map, wage-and-hour.
- Backlog: 107 category-(c) dead-column byte checks; schema-routing table
  moves (repo files fixed 2026-08-11, warehouse schemas cosmetic-wrong);
  immigration court records husk (no loader yet).
- Disaster-aid reload still finishing; its chain (sentinel repair → rebuild →
  label → reseed) runs when it lands.

*No publish decisions are implied anywhere in this report; findings remain
human-gated per the constitution.*
