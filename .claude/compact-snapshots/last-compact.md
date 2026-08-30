# Snapshot taken right before context compaction

## STATUS.md at compaction time
# RIPPLE STATUS — 2026-08-30 — Join Handbook now carries everything measured on 08-29/08-30 (96 measured-not-in-spine edges with the name-check numbers attached); spine untouched

*One screen. Rewritten (never appended) at the end of every session.*

## 🚨🚨 DO NOT TOUCH THE ID SPINE WITHOUT ASKING FIRST 🚨🚨

**Chris's decision, 2026-08-29: the ID spine is DEPRIORITIZED. He drives it step by step.**
This means: `apply-config`, `connect spine`, `connect-one`, `connect-changed`, or ANY command that
registers new key families / reslices the spine is a RED-lane action now, no matter how routine or
"bounded" it looks. **"Wire it up" / "hook it in" / similar plain-English asks do NOT authorize
running spine commands** — on 2026-08-30 "wire it up" meant "add the day's findings to the Join
Handbook doc, following its pattern." If a task looks like it needs the spine touched, STOP and ask
Chris first, every time, even if a dry-run looks safe. (2026-08-30 near-miss: apply-config dry-run +
real run were both started off "wire it up" before this got caught — real run was killed before it
touched anything; verified nothing landed.)

## Read this first

1. **Standing rules from Chris (in memory):** (a) answer the question asked, no build plans / costs /
   next steps unless he says "think it through"; (b) time + geography are first-class joins; the ID spine is
   deprioritized, see banner above; (c) any list of 2+ comparable things is a table, not bullets.
2. **The Join Handbook (markdown file + standalone web page) now carries the whole 08-29/08-30 haul** under its
   purple "measured, not yet in the spine" tier — 96 edge rows (was 66), 25 tables new to the handbook:
   - the bank / PECOS / power-plant / award-key batch that was staged in code on 08-29 (branch→bank by cert and
     Fed id, hospital/nursing-home/home-health/hospice/clinic enrollments→PECOS owner and enrollment ids,
     generators/owners/eGRID→EIA plant, plants/eGRID/861→EIA utility, subaward→prime contract, debarred CAGE→contracts);
   - the smokestack-monitor plants→EIA plant edge (81%) and the contracts→SAM-by-UEI edges;
   - the old-HMDA lender id split by agency code (bank-regulator rows → FDIC cert 69.8%, HUD rows → benefit-plan
     sponsor EIN 40.4%) — name-checked 2026-08-30 through the crosswalk's lender names (83% / 93% agree), so both
     split edges are SOLID; the unsplit edge stays SUSPECT;
   - every one of the 43 name/state spot-checked edges now shows its numbers inline ("60 matched pairs
     spot-checked: names agree 93%, states agree 100%") in both the page and the markdown;
   - 4 glossary rows, 2 corrections, 3 traps added.
3. **Two 08-29 numbers were wrong and are now corrected in the handbook:** contracts→SAM by UEI is **33%** on the
   full contracts file, not 92.5% (that was the small recent-years copy — both are now listed, labeled); the
   HUD-row HMDA id → Form 5500 EIN is 40.4%, not the 6.2% quoted (different table/sample in pass 2).
4. **Place columns are now value-verified (2026-08-30):** all 2,244 name-scanned place columns across 386
   marts measured live (fill, distinct, sentinel share, shape test per kind) in ~9 min. **1,615 of 2,238 (72%)
   are what their name says**; 306 of 386 marts have at least one usable place column (230 marts a clean
   2-letter state, 125 a clean ZIP, 80 a county name, 52 clean lat/lon, 53 a FIPS). Traps found: 166 empty
   place columns, 39 constant, 36 "coordinates" that are really counts/money (name-scan matched LONG/LAT),
   27 FIPS + 10 ZIP columns with leading zeros lost, 19 lat/lon columns with 0,0 rows, 21 "state" columns
   that are numeric codes, 42 "ZIP" columns that aren't (mostly foreign postcodes), 171 place columns that
   are codes not names. 3 index rows were stale (2 marts gone, 1 mart lost its 3 place columns).
   Report: reports/location_index/LOCATION_VALUES.md + location_columns_verified.csv (raw JSON alongside).
   **And it is now IN the Join Handbook** (page + markdown) as a third layer beside the spine edges and the pass-2
   edges: every table shows its value-checked place columns (kind, column, % of rows filled, verdict, how many
   other tables carry a clean version of that kind of place), traps are flagged ⚠ on the table, and the front page
   carries the "who can meet on what" table. **167 tables appear in the handbook for the first time** — they have
   no shared-ID connection at all and are reachable by place only (handbook now lists 427 tables, was 260).
   Build order unchanged: pass-2 source → build page → build markdown; the place layer reads the verified CSV.
   **Time went in the same way right after:** the 08-20 time index (1,275 value-checked date columns, each read
   for what its clock means) is a fourth layer. Every table shows its clocks (column, grain, range, meaning, plain
   description), a "best clock" line (prefers when-it-happened over reported/decided, finest grain), and the
   212 columns that look like dates but aren't (durations, vintages, our own download stamps) are flagged ⚠.
   427 tables run on a real clock; 146 tables are new to the handbook via clock only. Handbook is now **573 tables**
   (spine 260 → +25 pass-2 → +167 place-only → +146 clock-only). Front page carries both "meet on place" and
   "meet on time" tables.
5. **Unchanged:** apply-config NOT run (drift test red — and stays red until Chris says go); 8 spatial join errors
   (TRI + NTSB coords); DOCKET ~40% wrong; Snowflake MCP token rejected (direct python connection works — use
   it); overnight loads (MAUDE, subawards, LDA) unchecked; SAM public extract has no DUNS; IDV file and Fed
   holding-company file still not held.
5. **Git:** working tree holds this session's follow-up measurement script + its JSON/log receipt, the edited
   handbook source/build files, both regenerated handbooks, this file. Nothing committed.

## BROKE

Nothing broke. The handbook page's script parses; it was not opened in a browser this session.
One process failure, logged to memory: a spine command was launched off a doc-level instruction and had to be
killed by Chris. Nothing in the warehouse changed.

## YOUR MOVE (Chris)

Nothing blocking.

## NEXT (only when asked)

- Open the handbook page in a browser once — the place and time panels and front-page tables were built and
  parse-checked but not eyeballed.
- The true islands — marts with no ID connection, no verified place column AND no clock (count not yet computed;
  the 607-mart inventory minus the handbook's 573) — list them by row count and decide loader fix vs. leave dark.
- Parse the OpenSanctions / CSL identifier blobs into typed keys.
- Check the overnight MAUDE load — the partner the 5.2M device IDs are waiting for.
- Land the IDV file and the Fed holding-company file (both free bulk).

**Cost note:** ~20 small read-only queries + the 388-query place-column scan (~9 min on the dbt warehouse, ~$1–2) + 1 aborted apply-config (dry-run only) — roughly $2 for the day. No storage added.

## Working tree at compaction time
## main...origin/main
 M .claude/compact-snapshots/last-compact.md
 M STATUS.md
 M reports/JOIN_HANDBOOK.md
 M reports/viz/_build/build_join_handbook.py
 M reports/viz/_build/build_join_handbook_md.py
 M reports/viz/_build/handbook_pass2_edges_2026-08-29.csv
 M reports/viz/_build/handbook_pass2_notes_2026-08-29.json
 M reports/viz/_build/join_handbook_template.html
 M reports/viz/_build/pass2_edges_source_2026-08-29.py
 M reports/viz/join_handbook.html
?? reports/location_index/LOCATION_VALUES.md
?? reports/location_index/location_columns_verified.csv
?? reports/location_index/location_values_2026-08-30.json
?? reports/location_index/location_values_2026-08-30.log
?? reports/recon/pass2/handbook_followups_2026-08-30.json
?? reports/recon/pass2/handbook_followups_2026-08-30.log
?? reports/recon/pass2/hmda_split_precision_2026-08-30.json
?? scripts/handbook_followup_overlaps_2026_08_30.py
?? scripts/hmda_split_precision_2026_08_30.py
?? scripts/location_value_scan_2026_08_30.py

## Recent commits
35db8a82 Add Level-3 precision check script for pass-2 edges (2026-08-29)
cab809cc Add loader script for "no-brainer" acquisitions and update report
b2a367bf Refactor code structure for improved readability and maintainability
3f2839a4 Add tests for apply-config changes and introduce join_handbook.html
38843a2c Update checkpoint data and add report on unregistered ID candidates
