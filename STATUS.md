# RIPPLE STATUS — 2026-08-09 (full-day sprint)

*One screen. Rewritten (never appended) at the end of every session. Sessions read this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (still open):**
- The bulk loader's post-land dbt scaffolder emits a DEGENERATE staging model (a
  phantom `"ID"` column + meta only) for any spec without key_cols, and it GUTTED
  the curated intl_ie_cro schema.yml doing so. Damage reverted this session
  (junk deleted, schema restored, nothing committed); the scaffolder itself in
  `scripts/bridge_fuel_load.py` (~line 664 lifecycle hook) is still un-fixed —
  next bulk load without key_cols will re-emit junk. Fix or gate before the next
  spec-based load.
- The 7 rebuilt/new sources have NO staging models yet (raw landing only):
  fed_va_suicide_national/state, fed_cdc_wonder, fed_cdc_leading_causes_state,
  intl_ie_cro (curated schema exists, model refers to old landing shape — verify),
  fed_faa_aircraft_registry, fed_fra_* (3), fed_fbi_cde. Real dbt work, not autogen.
- 11 orphan twin tables still need dropping (Chris-only, unchanged).
- Old junk marts keep two demoted sources (`fed_faa_data_portal`,
  `fed_va_suicide_appendix`) reading as "modeled" in the catalog — their marts
  should be dropped with the orphans.
- FBI CDE key now lives in `library-onboarding/.env` (`FBI_CDE_API_KEY`) — key
  was pasted in chat 2026-08-09, treat as semi-exposed; rotate at leisure via
  api.data.gov if it ever matters.

**INCIDENT (fixed, logged, guarded — read this):**
The dead-scrape demote command handed to Chris was generated BEFORE this
session rebuilt 3 dead sources under their old names — running it demoted the
fresh 821k-row Irish CRO, CDC WONDER, and VA all-cause loads. Caught and
re-promoted within minutes (verified back to landed/modeled). Two permanent
fixes: (1) `propose_dead_scrape_demote.py` now REFUSES latest-success runs
that are big (>5k rows) or fresh (<7 days) — no override flag on purpose;
(2) memory note `stale-commands-are-live-ammo`: re-verify any queued command
against CURRENT state before handing it over.

**DONE this session (all verified live):**
- 7 approved dead-source rebuilds ALL LANDED, quality-gated (~3.3M rows total):
  VA suicide national (700) + state (19,704), VA all-cause mortality (2,808),
  CDC WONDER national year×cause×sex grid (880; API is NATIONAL-ONLY by CDC
  policy — state grouping rejected), NCHS leading-causes-by-state companion
  (10,868), Irish CRO companies (821,697), FAA aircraft registry (315,447),
  FRA rail casualties (1,150,788) + crossing incidents (251,149) + equipment
  accidents (224,941), FBI CDE state monthly crime counts (477,360; new
  summarized endpoints — the old estimate API is retired).
- 12 other dead sources stay demoted with receipts (FDIC enforcement, DOJ FCA,
  DOJ CRT re-checked: still no machine path; AustLII/Georgia/ADB/NARA buried;
  Zefix/Oyez/BORME are soft-buries with working paths if priorities change).
- ZIP country-gate (Chris picked Option A): rows with a non-US country now
  contribute NO zip key. In `connect/keys.py` (+ discover + incremental mirror),
  28 zip+country tables resliced, 2 new offline tests.
- Full fingerprint (1,273 tables) + discover rebuild: 4,538 edges; incremental
  twins reseeded from it; the incremental==full-rebuild proof test now PASSES.
- Catalog view now excludes Snowpark temp tables (ghost purged, rollback saved).
- Chunked profiler for ultra-wide tables (`scripts/wide_table_profiler.py`):
  College Scorecard data confirmed REAL (6% degenerate); 2 duplicate copies
  identified and dropped by Chris.
- Chris ran: mortgage-table drop, scorecard-twin + ghost drops, demote --apply.
- Offline suite green all day: 2,679 passed / 2 skipped / 0 failed. CI green.

**YOUR MOVE:**
1. Nothing is blocking. Optional: orphan-table + junk-mart drop list whenever
   you want it printed again.

**NEXT SESSION:**
1. Fix or gate the degenerate dbt scaffolder in the bulk loader (top priority —
   it silently destroys curated schemas).
2. Write real staging models for the 7 new sources; wire FRA/FBI/CDC into marts
   (rail deaths by railroad, crime baselines, mortality baselines).
3. Phase 0 leftovers: orphan drops, remaining API signups (DOL WHD, Senate LDA).

**COST:** 6.08 Snowflake credits today (~$15-18) — well above the ~$5 running
estimate I gave Chris. Drivers: the planned loads/reslices (~2), but mostly the
full fingerprint re-scan of all 1,273 tables (~1.5h) that I expected to resume
from cache and didn't (its cache keys on a format bump + the purged JSON), plus
the full discover + 3 warehouse-proof runs. Flagged before the go ("$4-5"), but
the fingerprint overshoot was not re-flagged mid-run — noted as a miss.

**TEST STATUS:** offline 2,679 passed / 2 skipped / 15 deselected / 0 failed;
warehouse-marked incremental proof PASSES post-reseed. CI green on main.
