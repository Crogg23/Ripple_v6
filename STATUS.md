# RIPPLE STATUS — 2026-08-22 — Warehouse cleaning sprint, day 1 (final)

*One screen. Rewritten (never appended) at the end of every session. Sessions read
this at boot and brief Chris in chat — Chris never has to open it.*

**BROKE (found this session, one still open):**
1. **The "full" federal contracts table is a truncated sample.** Exactly 1M rows
   per FY 2007–2026, each FY covering only ~2–3 months of `action_date`
   (FY2024 = Jun 24–Aug 18). ~10–15% of reality wearing a "FULL" name; no
   loader survives in the repo. Any trend analysis on it is silently wrong.
   **Re-pull needs a priced plan and Chris's go (RED, still open).**
2. ~~UK beneficial-ownership 56% missing~~ — **FIXED**: landing matches source
   exactly (15,804,612; was 7,000,000), mart rebuilt on full data, plus 7M rows
   of literal "None" strings repaired.

Carried, untouched: column-classifier substring cosmetic bug; count-question
generator caps; July's unverified defects (FAERS column-shift, MSHA zero
deaths, EPA penalty stamping, SEC 13F scale split, debarment stub, NHTSA dedup).

## The typing layer is LIVE (Chris chose clock-style, built same day)

- Pieces, all committed-pending: value-check sweep (`scripts/typing/
  value_check_sweep.py` — all 962 worklist columns measured live, 0 errors),
  rulings file (`reports/typing_index/typing_rulings.csv` — 587 castable, 375
  keep-text; 39% of the name heuristic was wrong, mostly zero-padded IDs),
  guarded macros (`macros/ripple_typing.sql` — three-lane date parse defusing
  the epoch trap), two appliers (`apply_rulings.py` aliased+bare lines,
  `apply_star_rulings.py` select-star), guard tests
  (`tests/test_typing_layer.py` — type match + 1800-2100 range sweep).
- **285 columns across ~61 models rebuilt typed; guard tests pass.**
- Remaining castable: 119 columns on tables with NO dbt model file (mostly
  Google political-ads misfootnoted under EDUCATION, findings/agg tables),
  31 politics-guarded (need the Python canonical path, not dbt), 6 complex
  expressions incl. 3 web-archive 14-digit timestamps needing an explicit
  format parse (ripple_dt would null them — do NOT bulk-apply).
- Marts text share: 75.6% → **74.0%** this session.

## Other wins today (all verified live)

- **Polygons exist now**: Census boundaries as GEOGRAPHY marts — 3,235
  counties, 56 states, 33,791 ZCTAs, 100% parse, point-in-polygon verified
  (`REFERENCE.REFERENCE__CENSUS_CB_*`; loader `scripts/census_boundaries_load.py`).
  Warehouse-wide geography columns: 2 → 5. All five geographic Laboratory
  techniques now undegraded.
- **OSHA inspections re-pull running** (~300k of ~4.5M rows; DOL API
  rate-limits hard — multi-day trickle, checkpointed, resume with
  `python scripts/osha_inspections_api_load.py --run`).
- 19.9M-row assistance table typed; GLEIF entity+relationship dates typed;
  bridge-entities filled (53,799); ZIP→point table built; roll-call
  divergence documented as intended; full test suite green (3,100 tests).

## YOUR MOVE (Chris)

1. **Contracts re-pull**: wants a priced plan before anything moves.
2. Carried: RIPPLES.md 5th landmine; healthcare pilot weak signal; Laboratory
   opportunity ranking. None urgent.

**NEXT:** (a) finish OSHA trickle + build its mart; (b) hand-pass the 6 complex
typing columns; (c) decide/flag the 119 model-less tables (many look mis-filed
by domain — flag to Chris, don't silently move); (d) July defect verifications.

**Cost note:** ~$8–12 of warehouse compute today total (meter-verified ~1.7
credits by mid-afternoon, plus the typing rebuilds and polygon builds since).
Nothing running can spike; the $300-day alert rule is in memory.

## Not committed

Everything from the last two sessions plus: typing layer (scripts/typing/,
macros, tests, reports/typing_index/), ~61 edited mart models, boundary loader
+ 3 reference models, OSHA + PSC loaders, STATUS.md, refreshed lab_map dump.
