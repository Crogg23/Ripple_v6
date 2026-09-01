# Fix plan — hiring-manager review, connect + landing
2026-09-01. Source: reports/recon/hiring_manager_review_2026-09-01.md
Ordered by the review's own severity list. Each item: the fix, the proof, the risk.

---

## Phase 1 — stop the bleeding (data loss + dead guardrail)

### 1. Landing W1 — incremental append crash = silent permanent data loss
Files: `library-onboarding/ingest.py:426, 463-470, 1006-1009, 1027-1040`

**Fix — make the append atomic, same trick the chunked path already uses:**
- `_load_landing` incremental path writes to a `_STAGE_APPEND` temp table first
- one `INSERT INTO target SELECT * FROM stage` — single statement, atomic
- on exception: DROP the stage table, target untouched, watermark never advances
- watermark advance moves to *after* the insert commits and a row-count check passes
- delete or reuse the chunked resume machinery for this path — do not fork a third one

**Proof:** unit test with a fake connection that raises mid-write; assert target rowcount
unchanged and watermark unmoved. Then one real incremental load, small source, verify counts.

**Risk:** temp-table doubles transient storage for the append slice. Tiny — appends are small.

### 2. Landing W2 — `_latest_success_rows` dead guardrail
File: `library-onboarding/ingest.py:1053-1068`

**Fork — DECIDED 2026-09-01: A, wire it.**
- A. Wire it: call before every `overwrite=True` load; refuse when new rows < floor
  unless a `--shrink-ok` flag passed. The SAM incident it cites is real.
- B. Delete it, move the lesson to `.claude/traps.md`. Honest, but the incident can recur.

Recommend A. Small: one call site in `_load_landing` overwrite branch + one in atomic_load.
**Proof:** test with a mock registry showing 1M prior rows, attempt 10-row overwrite, assert refusal.

---

### Phase 1 skeptic verdict (2026-09-01) — DISAGREE, findings adopted
- W1 premise wrong: old append was ONE write_pandas chunk = one COPY INTO,
  already atomic. Verified in the installed connector source
  (pandas_tools.py:388 — chunk_size defaults to len(df)).
  The stage-and-insert is hardening, not a fix. Fork for Chris: keep or revert.
- Real hole found + fixed: finally-DROP masked the original load error; now
  swallowed with its own try/except, tested.
- Real hole found + fixed: chunked fresh loads SWAP the live table with no
  floor; _shrink_refusal now runs before the swap, staging dropped, tested.
- Review's "zero callers" for _latest_success_rows was false: 4 live callers
  in scripts/ (_bulk_load_utils.py:442, _small_flat_loader.py:71,
  fec_itcont_load.py:155, fema_ia_load.py:181). Dead only inside ingest.py.
- Noted, not fixed: stage-name collision on concurrent same-source runs;
  unquoted column identifiers precondition; per-append cost doubles writes.
- Offline tests prove statement ordering, not warehouse atomicity.

## Phase 2 — the copied trap (zip member heuristic)

### 3. Landing W4 — largest-member zip selection, 6+ live copies
Files: `scripts/issue_batch_load.py:101-105,118`, `nobrainer_bulk_load_2026_08_29.py:283`,
`bridge_fuel_load.py:253-254`, `cftc_cot_history_load.py:114`,
`dol_enforce_bulk_load.py:147`, `osha_ita_bulk_load.py:164`

**Fix — one helper, loud failure:**
- new `loadkit/archive.py::pick_member(zf, pattern=None)`:
  - one member → return it
  - pattern given → glob match, error if 0 or >1 match
  - multiple members, no pattern → **raise** with the member list printed
- same shape for Excel sheets: `pick_sheet(xl, name=None)`
- migrate all 6+ call sites; each gets an explicit pattern from what it actually loads today
- grep gate: add a check to test-gate.sh or a unit test that greps scripts/ for
  `max(.*getsize|key=len` on zip members — new copies fail CI

**Proof:** unit tests on synthetic multi-member zips; re-run one affected loader dry.
**Follow-up decision for Chris:** the 18 at-risk zip specs from the trap memo — re-land or not.
That is warehouse spend; price it first.

---

### Phase 2 outcome (2026-09-01) — done after two skeptic rounds
- loadkit/archive.py: pick_member / pick_sheet, one-or-raise, size never decides.
- Skeptic round caught: gate regex matched 1 of 5 real shapes (fixed and
  verified against the deleted originals); recon_ exemption whitelisted two
  live 73-dataset loaders (exemption removed); real copy count was 16+, not 6.
- 22 call sites migrated across 13 files: issue_batch_load(+2 sheet picks),
  issue_batch_load2, cftc_cot_history, osha_ita_bulk, dol_enforce_bulk,
  bridge_fuel, nobrainer(2 incl. SAM monthly infolist[0]), tier1_bulk_batch(2),
  tier1_bulk_retry, tier1_bulk_retry2, recon_bulk_load_2026-08-07(3),
  recon_bulk_load_tier1_remaining(4 incl. sqlite+mdb), sam_exclusions_extract,
  sec_ftd_cusip_bridge, uk_ch_psc.
- 7 deliberate top-N multi-file loads keep size-sort under an audited
  `# archive-gate: allow` inline waiver; gate skips only those lines.
- Gate now also bans namelist()[0] / infolist()[0] blind-first picks.
- INTENDED behavior change: any zip/workbook with several candidates now
  RAISES listing members instead of silently loading the biggest. Known
  tripwire: issue_batch spec `intl_ti_cpi` has no sheet opt — first rerun
  will raise and name the sheets; add the sheet opt then.
- Not done: opening the real CFTC/MSHA/OSHA/USCG/SAM archives to confirm
  single-member. Cheap offline downloads; flagged as follow-up.

## Phase 3 — connect correctness

### 4. Connect W5 — `_merge_nodes` KEY_TYPE scope
File: `connect/incremental.py:789-790`

**Fix:** add `KEY_TYPE` to the DELETE predicate so it matches the re-INSERT join,
matching `_merge_index`'s comment at :806-809. Also fix the overstating stats
at :837-839 and :960-961 — count actual merged rows, not slice size.
**Proof:** regression test: two key types, same KEY_VALUE, same table; run merge;
assert both rows survive. This is exactly the offline-harness test from item 5.

### 5. Connect W1 — MERGE logic has zero executing coverage; docs lie
Files: `connect/incremental.py:13-16, 216, 605, 1161-1167`, `__main__.py:123-127`,
`tests/test_connect_incremental.py:309, 322-325`

**Fix, two halves:**
- Docs today: rewrite the three docstrings — validate() needs scratch twins the
  retired rebuild wrote; it is not a live backstop. Cheap, honest, do first.
- Harness: run the MERGE/keyset SQL against DuckDB or SQLite in-memory with
  tiny fixture tables. Snowflake-specific syntax (MERGE, MINUS) may need a
  translation shim or splitting statements into portable form.
  **Fork — DECIDED 2026-09-01: A, DuckDB shim.** Portable-SQL refactor parked.
**Proof:** the KEY_TYPE regression test from item 4 runs green locally, no warehouse.

---

### Phase 3 outcome (2026-09-01) — done after one skeptic round
- _merge_nodes DELETE now pair-scoped (KEY_TYPE, KEY_VALUE); skeptic
  mutation-tested it: old SQL loses the DUNS row, new SQL keeps it.
- Stats honest: _merge_index returns rows inserted, _backfill_leads returns
  rows the UPDATE touched. Note: index_rows metric meaning changed --
  run logs before/after this commit are not comparable on that number.
- DuckDB harness (tests/test_connect_merge_offline.py, 4 tests): the actual
  module SQL executes against a real engine, no warehouse. Row-IN NULL
  semantics probed, matches Snowflake; CURRENT_TIMESTAMP() the only shim.
- Docs de-lied in 6 spots: incremental.py header, sync_after_rebuild,
  validate banner + module CLI help, __main__.py seed/reseed/validate help,
  test_connect_incremental docstring. All now say the rebuild is retired
  and validate() cannot currently run.
- Still uncovered: _merge_entity_map, _merge_golden, _merge_pairs,
  _merge_index SQL (MERGE / OBJECT_CONSTRUCT / ANY_VALUE do not run on
  DuckDB without a bigger shim). W1 is "mostly covered", not covered.
- Parked for Chris: scripts/heartbeat.py + launchd README still schedule a
  weekly `connect all` calling it "full rebuild + drift backstop" -- the
  scheduler repeats the dead-backstop claim, outside this plan's scope.

## Phase 4 — hygiene sweep (one commit each, mechanical)

6. `incremental.py:514` — delete `if True:`, dedent 65 lines. Diff is whitespace-only + one line.
7. `_guard_config` (:244-257) — rename to `_sync_config_or_die` or split check from mutate;
   mutation on drift should hit the existing greenlight gate.
8. Config baselining (:327-374) — strip `ENABLE_SPINE_BATCH_2026_08` too; longer term,
   build `DISPLAY_SPECS` from one registration function instead of six import-time updates.
   Do the flag fix now; park the registry refactor.
9. SQL interpolation — one `q(identifier)` helper in db.py; use at :649, :866, :1271-1274,
   and `db.fqn`. Validate against `^[A-Z0-9_.]+$`, raise otherwise.
10. Except-pass sweep — `register.py:209-210`, `ingest.py:1039-1040`, `snow.py:128-129`:
    log at WARNING with the exception, and for `_watermark` distinguish
    "no watermark row" (return None) from "query failed" (raise).
11. Outward claims — change "hard IDs only" to "no name matching in the identity layer"
    in SPEC sheet / README wherever it appears.

### Phase 4 outcome (2026-09-01) — done after one skeptic round
- if True: removed, 65 lines dedented, diff verified clean by the skeptic.
- _guard_config -> _apply_config_drift_or_raise; docstring says it mutates.
  FORK CLOSED (Chris: "go", 2026-09-01): implicit drift now RAISES with
  preview instructions instead of auto-reslicing. Explicit `apply-config`
  stays ungated; RIPPLE_APPLY_CONFIG=1 re-opens the implicit path on
  purpose. Two gate tests added.
- Flags-off baseline strips BOTH staged batches. Skeptic feared this flips
  the live pin; checked read-only against the warehouse via the Python door:
  stored CONFIG_SENTINEL == CURRENT fingerprint, baseline branch inert.
  Regression test added (norm + spec units stripped, dicts restored).
- db.ident() validator + fqn() validation; two-part names raise now instead
  of building 4-part garbage; injection-shape tests added. store.cfqn() is
  the other builder -- it quotes, not validated, noted not fixed.
- Except-passes speak: _enrich and session-guard failures print WARNING;
  _watermark treats "does not exist" as first-run ONLY after an
  INFORMATION_SCHEMA probe confirms absence -- Snowflake folds missing and
  unauthorized into one message, so the probe is what separates them.
- Outward claims sharpened in RIPPLE_DESIGN_BRIEF + technical spec:
  "no name matching in the identity layer", NAME@geo edge-lane only.
- Final suite: 716 passed, 3 skipped, 0 failed. The bash-missing hook and
  shape-gate tests are the only exclusions, broken before this work started.

## Explicitly not doing
- `exec()` of LLM code (landing W3) — review itself calls it defensible solo. Park.
- dbt 39K-file review — out of scope.
- SPINE table rename — separate open decision, already tracked.

## Order and gates
Phase 1 → 2 → 3 → 4. No warehouse spend needed except:
- item 1 final verification load (small, price first)
- item 3 follow-up re-lands (Chris decision, price first)
