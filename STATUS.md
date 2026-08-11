# RIPPLE STATUS — 2026-08-11 (evening) — the verification session: the warehouse got its first full physical

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE: nothing new broken by this session — but the sweep FOUND ~50 broken
sources.** This session measured and logged; it deliberately fixed nothing.

**The question this session answered:** "Is my warehouse accurate and reliable?"
Full verdict with evidence: `reports/warehouse_verification_2026-08-11.md`.

**The one-paragraph answer:** The core is real. 16 of 18 records spot-checked
field-by-field against publishers' own sites match exactly, and of 181 sources
where a publisher total could be found, 128 (71%) are complete. But ~50 of 558
sources would produce a confident wrong chart today: 33.5M exact-duplicate rows
(mostly one runaway loader), one table loaded with the wrong file entirely, one
registry with a blank key column and epoch-dates, 30 sources materially short,
8 holding more than the publisher advertises.

**Worst offenders (full ranked list of 14 classes in the report):**

1. Mortgage database: 19.05M rows are 7,204 real rows duplicated ~2,600x.
2. Credit-union call reports: the column-dictionary sheet got loaded as the
   data — table is unusable.
3. Aircraft registry: tail-number key 100% blank AND all four date columns
   epoch-corrupted to 1970.
4. Commodity-trading reports: one date column 100% epoch-corrupted (second date
   column fine, rescuable); also only 6% of publisher's full history.
5. Foreign-aid spending: 97.6% duplicate rows.
6. Eight FDA raw landing tables truncated/wiped (their marts are mostly fine;
   two marts genuinely short: device adverse events 2.7M of 25.7M, establishment
   registrations 263k of 333k).
7. 30 sources short vs publisher (lobbying filings 9%, federal register 9%,
   GLEIF relationships 73%, sanctions-exclusions round-cap, etc.); 8 sources
   OVER (FEC multi-cycle loads, GLEIF exceptions 9.5x, EPA facilities 2x).
8. 104 ID-named columns ≥99% blank across 43 tables; sanctions birth dates
   carry a 1970-01-01 sentinel on 7,406 rows.
9. Uniqueness tests exist on 505/607 marts but there's no evidence the dbt
   suite has actually been RUN since the last two weeks of rebuilds.
10. 16 tables errored out of the scan (ICIJ offshore leaks among them) — still
    unverified either way.

**Verified clean:** encoding basically fine (9 tables, ≤1.25% sampled rows);
557/606 mart tables free of material exact-dups; both big 2026-08-10 re-pulls
(banks 27,836, daily cash ledger 478,149) confirmed exact against publisher.

**Evidence files (receipts, not homework):** completeness per source, key/date/
dup scan per table, 18 value spot-checks, mojibake scan — all in `outputs/`
with date suffix 2026-08-11, referenced from the report.

**Live/open items carried forward:**

- Disaster-aid reload still running (20.1M of 25.9M at last check, checkpoint
  updating). When done: repair 'nan' cells, rebuild staging+mart, drop sample
  label, reseed connections.
- UK company-ownership load still blocked on the Chris-only wipe (same
  one-liner as before).
- Drop list (Chris-only, ~50 tables): `reports/duplicate_ingest_drop_list_2026-08-10.md`.
- Key-gated on Chris: broadband map, wage-and-hour, Senate lobbying.
- Immigration court records still a husk (12.6M rows, no loader yet).
- Repo-side routing fix (2026-08-11) moved model FILES but warehouse tables
  still sit in wrong schemas (hospice under immigration, commodity-trading
  under education, lobbying under education). Cosmetic in warehouse, visible in
  every scan.

**YOUR MOVE:**

1. Read the verdict (it's in the chat brief + report). Decide repair order —
   suggested first wave is the top 5 above, all truth-lane fixes a session can
   do without you, but the ORDER of what gets fixed first is yours if you care;
   otherwise next session starts at #1.
2. Same two one-liners as before (UK wipe; drop list).
3. Separate call worth making soon (not this session's lane): whether the next
   sessions keep hardening data or first make the platform USABLE end-to-end
   (workbench/catalog/reading room have never produced a satisfying answer
   end-to-end). That's a taste call, so it's yours.

**NEXT SESSION:**

1. Boot trust check; finish disaster-aid chain when the load lands.
2. Repair wave 1 (dup purges, credit-union reload, aircraft registry re-parse,
   commodity-trading date fix) with regression tests per the tdd streak.
3. Get the dbt uniqueness suite actually running on a schedule and captured in
   artifacts, so "guarded" means guarded.

**COST:** ~$2–4 warehouse credit (one aggregate pass over 590 tables + sampled
scans, X-Small; metadata free). Agent spend: 12 background agents for publisher
checks (~10-15 min each). Single session.
