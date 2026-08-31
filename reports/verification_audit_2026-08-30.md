# Verification Audit — ranked review list + survey receipts

Built 2026-08-30 by four parallel read-only surveys (loads/registry, reports/handbook, code/spine/dbt, git+transcripts).
No warehouse queries were run to build this. Repo evidence only.
Chris picked: work the list top-down, starting row 2.

**Structural finding:** the worst risks are not missing receipts — they are receipts that launder
unverified claims (a file named `location_columns_verified.csv` that was never value-scanned;
"SOLID" join verdicts on 25–58% name-match; dbt test *declarations* counted as test *results*).

---

## The ranked table

| # | Area | If wrong, costs | Check | Effort | Impact |
|---|---|---|---|---|---|
| 1 | Loads vs publisher reality — no expected-count control exists. MAUDE landed 13,042 of ~20M and registered clean; subawards checkpoint stops 2019-05; Senate LDA died mid-2011 (16 of 28 years missing); contracts R2 checkpoint 93.2M vs audit-measured 63.7M | any published number | expected-count manifest + COUNT(*) per source (Python door) | a day | 10 |
| 2 | ID-normalizer parity — 53 tests RED (`tests/test_staging_spine_id_parity.py`). Warehouse staging normalizes NPI/CCN/EIN differently than `connect/keys.py` | every entity join | run suite, diff normalizers | hours | 10 |
| 3 | Load registry VOLUME vs landed — backfills streamed rows, never re-registered (one source advertises 72K, landing holds 1.78M); `scripts/propose_registry_volume_sync.py` preview-only, never applied | registry is what downstream trusts | VOLUME vs COUNT(*) for ~2,778 sources | hours | 9 |
| 4 | Clock claims — 253 of 482 tables never reviewed ("floors, not verified totals" per `reports/handoff_canonical_clock_rollout.md`); canonical clock column never built; no planned/future category | every timeline claim | review unreviewed half via clock_index.csv method | a day | 9 |
| 5 | Join handbook precision — 52 of 96 pass-2 edges overlap-only; "SOLID" on 25–58% names_pct (HRSA→NPPES 35.6, FDIC 25.0, FEC 25.0, HMDA split 83.3 w/ visible mismatches); 4,512 main edges have zero precision data | "X connects to Y" claims | extend `scripts/pass2_precision_check_2026_08_29.py` to the 52; re-grade SOLID | hrs–day | 9 |
| 6 | Spec sheet numbers (`docs/ripple_technical_spec_2026-08-30.md`) — 1.25B rows / 4,512 edges / 33.3M entities; 4,512 disagrees with audit's 4,910; entity dedupe has no quality receipt | externally quotable numbers | re-run its 4 queries; reconcile 4512 vs 4910 | mins–hrs | 8 |
| 7 | dbt tests — no on-disk evidence any test run passed (target/run_results.json = 1 seed, 2026-08-27); 643 of 2,367 models zero tests; "25 failures fixed" commit `c8dc64e5` edited schema.yml — possibly relaxed not fixed | "models are tested" is a belief | read the 25 fixes; one real `dbt test` (note: dbt-fusion parse blockers reported 08-05) | hours | 8 |
| 8 | HMDA nationwide claim — 08-05 audit: `FED_CFPB_HMDA` is 100% Washington DC at full mart trust; no fix found since | flagship table lies about scope | one state-histogram query | mins | 8 |
| 9 | Entity spine rebuild — 36.9M entities atop rows 1–5; `data/spine_rebuild_2026-08-28.log` shows 10 stale-fingerprint skips, 7 geometry skips, 433 skipped pairs, no gate; `connect/entity_index_specs.py` 2,357 lines, no test file | graph inherits every load defect | after rows 1–3; fingerprint asserts | a day | 8 |
| 10 | "FEMA complete / PSC near-complete" (`589e78b4`, depth_triage 08-26) — same round-number method that failed 08-27 (80x pension truncation); FEMA mart 3,080,000 (round) vs 21.7M raw | depth claims that burned before | COUNT vs publisher; mart-vs-raw | hours | 7 |
| 11 | Root .done markers — `psc.done` is one word guarding 2.19GB CH PSC zip; no count/checksum; `ca_dl.err.log` is 0 bytes | tens of M of ownership records maybe short | COUNT on PSC/ICIJ/OCC landing vs snapshot counts | hours | 7 |
| 12 | Safety-gate holes — plain `git push` passes git guard; warehouse gate matches Bash only (MCP snowflake door unhooked; moot while its token is rejected); `connect/safety.py` 4th publish guarantee "(hook, ready to wire)"; `scripts/add_spine_columns.py` not in gate regex | don't-do-damage layer, 3 named gaps | patch review; model = hook 30-case self-test | hours | 7 |
| 13 | OSHA inspections — ~415K dup rows (~10%) from overlapping resume; appends, no dedupe; "do not blindly resume"; no follow-up | known-corrupt 4–5M table | COUNT(*) vs COUNT(DISTINCT ACTIVITY_NR) | mins | 6 |
| 14 | Ripples lead-lag reports (5 standing, 08-21) built on unreviewed clock half | temporal findings | falls out of row 4 | — | 6 |
| 15 | Master connections pass-1 — 22 "beyond reasonable doubt" families; pass-2 self-audit already found 8 pass-1 errors; medians have no re-runnable artifact | rationale doc for acquisitions | spot-check un-recorrected families | hours | 6 |
| 16 | Checkpoint-only recent loads — nobrainer bulk (ran 08-29, no log/report), FAERS quarters non-contiguous ~2014q2, SEC 13F 16KB unresolved error log, NEISS 2026 = -1 sentinel | recent self-reported "loaded" | counts vs checkpoints | hours | 5 |
| 17 | Place columns — value scan 08-30 is a real receipt (caught 36 false coordinate hits, 19 zero-zero traps, 27 FIPS leading-zero losses); but pass-1 still quotes unverified 2,244 name-scan figure; 3 tables failed to scan | stale number propagating | fix quote; rescan 3 | mins | 4 |
| 18 | Unregistered ID candidates — 3 of 13 have COUNT(DISTINCT) receipts (CAGE, OTHER_PROVIDER_ID_1, LICENSE_1); 10 are sample-profile/assertion; COLUMN_CATALOG only covers 751 cols; UPIN contradicted between files (474 vs 5,786) | new key families from unchecked cols | COUNT(DISTINCT)+sample the 10 | hours | 4 |
| 19 | 953 trendable-column plain-English descriptions — auto-generated (`0ed46425`), zero spot-checked, reader-facing | wrong prose to readers | spot-check random 30 | hours | 4 |
| 20 | Serve/dossier UI — well-tested but renders from tables row 2 may mis-join; 1 test red | falls out of row 2 | — | — | 3 |
| 21 | Orphan/duplicate tables — 11+ awaiting Chris's manual DROP since 08-05 | clutter | Chris + Snowsight | mins | 2 |
| 22 | build-state.md — printout of 08-25, defects last verified 07-12 | stale dashboard | regenerate | mins | 2 |
| 23 | Static HTML galleries (biome/spine-tree/scale, 08-24) — frozen, unlinked | only if shared | leave/regenerate | mins | 1 |

## Already earned — do not re-review

- Rulebook skeptic pass (`reports/skeptic_pass_rulebook_2026-08-30.md`) — run twice, caught 3 blockers + 4 bypasses incl. R3 (skeptic subagents inherited effortLevel: low → prior skeptic passes may have been rubber stamps).
- Hook self-test `.claude/hooks/test-gate.sh` — 30 adversarial cases; best-verified artifact in repo. (Header says "greenlight.sh"; that file is actually chris-words.sh.)
- Depth-triage arithmetic (1,567 = 1,563 portal + 4 real) — checkable; only the "FEMA complete" conclusion is unbacked (row 10).
- Location value scan (`reports/location_index/LOCATION_VALUES.md`, `scripts/location_value_scan_2026_08_30.py`).
- Docket trust downgrade (`d560feac`) — claim downgraded honestly.
- GUDID (`logs/gudid_full_checkpoint.json` + release .sha256) and DOL Form 5500 (`logs/dol_form5500_full_checkpoint.json`, per-year rows+sha) — best-instrumented loads.
- Gap audit `reports/gap_audit_2026-08-25.md` — counts matched checkpoints, caught OSHA dups. (Aging; underlying agent evidence lives outside repo.)
- `connect/keys.py` test coverage (`tests/test_keys_normalize.py`, `test_discover_keyguard.py`, `test_density_gate.py`).
- Pass-2 self-audit of pass-1 (section A, 8 corrections) — a receipt in the honest direction.
- The one honest SUSPECT edge (ARID_2017→CERT, 47.4%, "do NOT use until split by agency") — the model of what the 52 level-2 edges lack.
- RIPPLES functional check (`reports/ripples_functional_check_2026-08-21.md`); trend sweep (`083a5487`, deflationary conclusion).

## Key receipts index (for a fresh session)

- Parity failures: `.pytest_cache/v/cache/lastfailed` (69 total: 53 parity, 7 bench, 3 spine_inputs_live, rest singles incl. politics-folder guard).
- Pass-2 precision: `reports/recon/pass2/pass2_precision_2026-08-29.json` (41 edges, 60 pairs each), `hmda_split_precision_2026-08-30.json`.
- Pass-2 overlaps: `reports/recon/pass2/pass2_live_check_2026-08-29.json` via `scripts/pass2_connections_check_2026_08_29.py`.
- Handbook CSVs: `reports/viz/_build/handbook_edges_2026-08-29.csv` (4,512, tiers only), `handbook_pass2_edges_2026-08-29.csv` (96).
- Load checkpoints: `data/usaspending_subawards/checkpoint.json` (4.74M, stops 2019-05), `data/usaspending_full/checkpoint.json` (claims 93.2M), `logs/senate_lda_checkpoint.json` (last key filings_2010), `data/maude_resume_2026-08-28.log` (final line: 13,042 rows registered), `data/osha_inspections/checkpoint.json` (claims 5.2M).
- Registry sync: `scripts/propose_registry_volume_sync.py` (preview-only).
- Spine imports: `connect/spine.py` reachable via `python -m connect spine` (connect/__main__.py:124); `spine_entity.py` imported by hunch/census.py, 3 scripts; 86 `from connect import` across 54 files.
- Drift audit: `scripts/drift_audit.py` — heuristic word-match; the ~1/3 figure is a rate, not a list; likely an UNDERCOUNT (10-line stub tests pass its "test nearby" check). No artifact file for the number exists yet.
- Correction memory precedent: session 89bc29c5, 2026-08-27 — "depth basically solved" vs 80x/14,000x truncations found hours later.

## Progress log (append as rows close)

All checks below ran 2026-08-30, read-only, through the Python-scripts door (key-pair auth, ACCOUNTADMIN).

- **Row 2 — REOPENED after skeptic pass: repo in sync, warehouse is NOT.**
  `tests/test_staging_spine_id_parity.py` passes 71/71 — but it only reads `.sql` files on disk.
  Skeptic sampled 200 of 1,438 deployed views in `LIBRARY_STAGING.DBT_CROGERS`: of 10 with
  `spine_entity_id` expressions, **7 are drifted** — deployed CCN/EIN normalizers are missing the
  2026-07-28 digits-only guard and repeat-char guard (the exact "join to nothing, forever" failure the
  test's docstring warns about). Newest deployed view is 08-26; keys.py changed 08-28/29; no dbt run since.
  **Fix = gated `dbt run` (Chris's call) + a live-DDL parity test.** The 4 Utah mis-joins below may be this
  bug, not spec errors — same PORTAL_SOC_UTAH family as a confirmed-drifted EIN view.
  (The "53-red was a stale cache" story is plausible but no longer falsifiable — this session's run
  overwrote the cache.)
  Full-suite run: 12 test modules fail to *collect* — `streamlit` missing from .venv (environment drift, not code;
  `pip install streamlit` restores bench/serve/home coverage).
  Suite result (minus those 12): **1,816 passed, 2 failed, 2 skipped (18m46s)**. Both failures are real findings:
  - `test_connect_incremental.py::test_incremental_state_matches_full_rebuild_backstop` — **the persisted
    incremental spine keyset has 940,364 keys a full rebuild would NOT produce** (a-b=940,364, b-a=0; discover
    twin b-a=9). The "incremental and full rebuild converge" guarantee is currently false at the keyset level.
    Likely fallout from the 08-28 rebuild's skips + later incremental adds. Feeds row 9; fixing = gated spine
    work, own session.
  - `test_connection_agreement_live.py::test_no_new_join_disagrees_with_itself` — **4 live mis-joins**, all
    against Utah open-data portal tables: NPDES_ID edge at 36.2% name agreement (4,045 entities), three CCN
    edges at 32–48%. Either the portal column isn't that ID, or the spec's name column is wrong. Row 5's
    failure class, caught by the suite's own guard. Fix = spec correction or ACKNOWLEDGED entry, per test's
    guidance.
- **Row 13 — CONFIRMED, still live.** `FED_DOL_OSHA_INSPECTIONS`: 5,611,412 rows vs 5,196,412 distinct ACTIVITY_NR
  = **415,000 duplicates (7.4%)**, unchanged/uncorrected since the 08-25 gap audit. Table also grew since then
  (was 4.11M) — more appends happened. Fix = dedupe rebuild; needs Chris go (warehouse change).
- **Row 8 — CONFIRMED, trap is live.** `FED_CFPB_HMDA` (28,301 rows) and `FED_CFPB_HMDA_LAR` (17,474 rows) are
  **100% DC — 1 state each**. `FED_CFPB_HMDA_HISTORIC` (19,136,434 rows, 53 states, CA/TX/FL top) is the real
  nationwide table. Anything citing FED_CFPB_HMDA as nationwide is wrong. Fix = registry NOTES/trust downgrade
  on the two DC tables; needs Chris go (warehouse write).
- **Row 6 — MOSTLY CLOSED (amended by skeptic).** Live: edges 4,512 (single RUN_ID from the 08-28 rebuild —
  that rebuild, not a quoting bug, explains the old 4,910), entities 37,254,436 (spec 33.3M stale low),
  landing 2,220 BASE TABLEs / 1,327,505,327 rows (spec stale low). Spec numbers UNDERSELL, none overstate.
  **edges_inc 3,182 matches spec only because BOTH are stale** — `CONNECT_EDGES_INC` last altered 08-22, not
  rebuilt with CONNECT_EDGES on 08-28; its keyset lag (KEYSET_LIVE − KEYSET_SCRATCH = 940,355) is the same
  ~940K divergence the incremental test fails on. **Stale 4,910 corrected in 5 reader-facing files** (lab_map
  _VERIFIED_FACTS/_AGENT_BRIEF/_front, connections_audit graph_structure/join_layer). Entity dedupe *quality*
  still has no receipt (open). `CONNECT` is a Snowflake reserved word — quote the schema.
- **Row 3 — SWEPT.** Landing table = UPPER(SOURCE_ID) (`library-onboarding/naming.py:89`). 2,786 registry rows,
  2,220 live landing tables, 2,015 matched by name. **DATA TRAP: `VOLUME` is free text and usually describes the
  publisher's universe, not what landed** ("~470,000+ studies" on a 500-row tap) — 1,797 of 2,015 unparseable as
  a landed count. Parsed where possible:
  - **15 understated ≥2x** (registry stale-low; loads outran registration): NOAA AIS 3.7M claimed vs 58.1M landed,
    EOIR 5M vs 12.6M, STORM_EVENTS 72K vs 1.78M, EPA ECHO 1.5M vs 3.16M, NIH 206K vs 2.12M (see below).
  - **39 overstated ≥2x** — mostly API taps holding a sliver of the stated universe (CLINICALTRIALS 500 rows vs
    ~470K studies; FED_DOL_FORM5500 33K vs ~800K/yr — but FORM5500_FULL holds the real 4.3M; SEC_EDGAR 200 rows
    vs 35M filings). These feed row 1's truncation theme, though VOLUME semantics make them estimates-vs-taps,
    not proven truncation.
  - Fix = apply `scripts/propose_registry_volume_sync.py` (--apply is Chris-gated) or re-register; plus decide
    whether VOLUME means "universe" or "landed" going forward.
  - **Skeptic addendum — the unmatched populations were not examined:** 771 registry rows have NO landing
    table (16 of them INCLUDE=true — registered sources with nothing landed, the highest-risk set), and
    206 landing tables have no registry row. Also one landing table matches two registry rows (2,015 counts
    pairs, not tables). Open work for the row-1/row-3 session.
  - Other skeptic notes: ICIJ "triplicate" is identical *metadata row counts*, not proven identical content —
    fine for a DROP decision, don't state as content-identical. HMDA_HISTORIC also has 23,099 NULL STATE_ABBR
    rows. FEMA mart figure = the HOUSING schema BASE TABLE (a same-named VIEW exists in TIMELINE). NIH bonus
    receipt: FY2000+01+02 sum to exactly 206,333 — the old cap note described those 3 years precisely.
- **Row 10 (FEMA half) — CLOSED, better than feared.** Raw `FED_FEMA_IA_HOUSING_REGISTRATIONS` = 26,250,920
  (the 08-25 "stalled at 23.97M" run completed); mart `HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS` = 26,250,920
  — **exactly equal**. The warehouse map's "3,080,000 mart" note is stale/wrong, not the mart. PSC half: raw
  claims still need a publisher comparison (below).
- **Row 11 — mixed.** UK_COMPANIES_HOUSE_PSC = 15,804,612 landed (matches depth triage incl. its known 1.8%
  resume-seam dup) and INT_UK_COMPANIES_HOUSE = 5,734,780 — the 2.19GB payload did land at scale. OCC = tiny
  reference lists (724/218/62), fine. **ICIJ is in TRIPLICATE**: three full copies of every offshore-leaks
  table under `XC_ICIJ_OFFSHORE_*`, `FED_ICIJ_OFFSHORELEAKS_*`, and bare `ICIJ_OFFSHORE_LEAKS_*` prefixes,
  identical row counts (relationships 3,339,267 ×3, entities 814,344 ×3, officers 771,315 ×3…). The known
  orphan-duplicate problem, live and bigger than the 08-05 list. Needs Chris's canonical-name call + manual DROPs.
- **Row 1 partials — MAUDE and LDA confirmed broken; subawards confirmed short.**
  `FED_FDA_MAUDE_FULL` = 13,042 rows live (vs ~20M corpus — confirmed, registered clean).
  `FED_SENATE_LDA_FILINGS` = 831,376 rows covering **1999–2010 + 2020–2021 only; 14 years missing**
  (2011–2019, 2022–2026) — worse shape than the log implied (2020–21 came from an earlier partial).
  `FED_USASPENDING_SUBAWARDS_FULL` = 4,742,460 (matches checkpoint; coverage stops 2019-05 per done_months).
  **Publisher side:** openFDA reports 25,711,469 device events → MAUDE landed **0.05%**. Companies House
  publishes no PSC record count, but the snapshot is 32 files / ~2.2GB (matches what was pulled) and
  INT_UK_COMPANIES_HOUSE's 5.73M companies matches the real CH register size — PSC plausibly complete.
- **Row 1 — SWEPT (2026-08-30 session 2). Manifest at `reports/row1/expected_count_manifest.md`.**
  Landing = 2,220 base tables / 1,327,505,327 rows (`reports/row1/landing_counts.json`).
  Skeptic pass ran on this section and corrected it (details below marked ⚠). New findings beyond the known four:
  - `FED_USASPENDING_CONTRACTS_FULL` holds **exactly 20,000,000** rows (confirmed by COUNT(*)) vs
    registry "expect 100M+" — truncated, superseded by R2. R2 = 93,153,424 = checkpoint total_loaded,
    months contiguous 2006-10→2026-08. ⚠ Skeptic: that is the loader agreeing with itself, not a
    publisher check — R2 is INTERNALLY CONSISTENT, not publisher-verified (no publisher total exists;
    contiguous months ≠ complete months).
  - **Open Payments = PY2022–24 only, 43,392,397 of publisher's 93.97M** (~46%); PY2013–21 + 2025 not
    landed. ⚠ Denominator is all payment types; if landed tables are general-only, real coverage is higher.
  - **ARCOS = 2006–2012 only** (histogram-proven, 0 null dates); 2013–2019 missing. The 23%-of-760M
    ratio rests on WaPo's third-party figure.
  - **FEC indiv = 2023–2026 only, 84.2M** (583 null dates) vs ~268.8M for 2004–2026 (third-party;
    FEC publishes no count).
  - **HMDA_HISTORIC = 2015–2017 only** (6.1/7.0/6.0M by AS_OF_YEAR, 0 nulls) — 3 of 11 historic years,
    and unregistered (below). ⚠ The per-year ~40–50%-of-LAR shortfall uses approximate publisher
    figures; a benign filtered subset is possible — unresolved, not asserted.
  - **Part D prescriber-drug: single load run** (no year column, 1 _SOURCE_RUN_ID). ⚠ Skeptic: 1 run ≠
    1 year — coverage UNKNOWN, not "1 of 12"; check load metadata filenames.
  - **FAERS at report grain: DEMO = 5,811,086 vs 32.8M published reports = 18% landed** (⚠ sharper than
    the original DRUG-row comparison).
  - CFPB complaints: 11,501 dup Complaint IDs (0.07%) — minor.
  - **EPA RCRA tables doubled — 5 pairs** (incl. ENFORCEMENTS; ⚠ was reported as 4) — ICIJ-style
    DROP list, Chris's call.
  - ⚠ **399 tables sit at exact multiples of 1,000** — the truncation smell is a population, not one
    table. Not triaged.
  - NPPES (9.6M vs ~9.4M NPIs), NEISS (9.8M vs ~10.8M derived), PSC, FEMA: **OK**.
  - Many majors have **no publisher count at all** (13F, EOIR, FJC IDB, SDWA, CAMPD, NWIS, Elections
    Canada, USAspending itself) — recorded as "unverifiable cheaply", not a pass. Still unchecked
    majors listed in the manifest (MDS 31.4M, ASSISTANCE_FULL at a suspicious 19.9M, CourtListener
    per-table counts, third contracts copy).
- **Row 1/3 orphan populations — SPLIT verdict.** 771 registry-no-landing (INCLUDE=true = **16** —
  a first pass said 23; that was a 'Y'/'N' truthiness bug the skeptic caught, script fixed, 16
  confirmed on rerun); 206 landing-no-registry. Registry-side orphans are mostly naming mismatches
  (`fed_fjc_idb` → `FED_FJC_IDB_*` etc. — UPPER(SOURCE_ID) rule violated warehouse-wide). ⚠ But the
  landing side is NOT resolved: **≥10 large tables have no registry row under any name**, including
  FEMA IA (26.3M) and HMDA_HISTORIC (19.1M, the flagship). Genuinely registered-never-landed
  (INCLUDE=true): st_legiscan, st_openstates, xc_cspan_congress, fed_house_clerk_ptr,
  fed_oge_disclosures, fed_house_disbursements. Receipts: `reports/row1/orphans.json`,
  `reports/row1/registry_dump.json`.
- **Row 1 second pass (2026-08-31) — the truncation mechanism found (corrected by skeptic).**
  `FED_USASPENDING_ASSISTANCE_FULL` fiscal-year histogram: **FY2007–FY2026 each land at exactly
  1,000,000 rows** (only FY2014 under, at 902,879). First write-up said "loader caps each FY at 1M" —
  ⚠ skeptic found the real code: **the zip extractor keeps only the LARGEST CSV member per zip**
  (`infra/ddl/08_bulk_ingest.sql:179`), and USAspending splits each FY at ~1M rows/file; FY2014's
  short count is the tell (caps don't leak, file slices vary). Same proc + spec shape as
  `FED_USASPENDING_CONTRACTS_FULL` (`scripts/server_side_specs.py:558,608` — verified), explaining
  its exact 20,000,000. R2's month-chunked loader is a different path, unaffected.
  ⚠ **Blast radius: 18 of 27 `server_side_specs.py` specs are `kind: zip`** through the same
  extractor. **Swept 2026-08-31, then rewritten after a second skeptic pass** (manifest
  "Zip-spec sweep" section; receipts in `second_pass_receipts.json`). Corrected verdicts:
  - Extractor truncation proven only on the two USAspending tables.
  - ⚠ But the count screen cleared sources sliced by SPEC, not extractor — skeptic caught three:
    **FEC masters = 4 cycles only** (2018–2024 manifest; FEC publishes to 1980),
    **NHTSA_RECALLS = post-2010 URL** (full file runs from 1966),
    **SEC_INSIDER = 4 of ~8 zip members and manifest ends 2025Q1** (5 quarters stale).
  - **OSHA violations + accidents landed NOWHERE** (only inspections, via the dup-ridden loader).
  - **WHISARD absent from LANDING — a repeatedly-failed fetch** (4 URL attempts in repo), not untried.
  - Shrunk tables (FEC_CANDIDATES 27,095 vs 33,506 logged; COMMITTEES 60,031 vs 78,039;
    NHTSA_RECALLS 241,861 vs 242,993): each has exactly one ingest run, so no reload explains it —
    **rows were removed after the only load**; cause untriaged.
  Receipts persisted: `scripts/row1_second_pass_receipts.py` → `reports/row1/second_pass_receipts.json`.
  Also closed: **Part D = DY2022 only** (ingest-log URL `..._DY22_NPIBN.csv`, run 431c13fc — receipt,
  upgrading the skeptic's "unknown" to confirmed 1-of-12); **MDS Frequency = one Q2-2026 snapshot**
  (aggregate file, no history); **round-number population defused** — only 2 of the 399 are ≥100K
  non-portal: CONTRACTS_FULL (explained) and FED_CDC_INJURY_VIOLENCE_COUNTY (132,000, untriaged).
  CourtListener publishes no per-table counts (API count feature needs a free auth token — cheapest
  future check; a third-party citation count of 18,123,971 sits 183 off our 18,123,788, suggestive).
  **Dialysis facilities: EXACT publisher match** — CMS stats API total_rows 12,456,456 = landed.
  GUDID publisher DI count (5.18M) is a different grain than our identifiers table (6.77M) — n/a.
- **Row 16 — SWEPT (2026-08-31, corrected by skeptic pass).** Checkpoint-vs-landing exact for 13F,
  CAMPD daily, CAMPD facility; NEISS year sums exact; 13F "error log" = pandas warnings, defused.
  ⚠ Skeptic corrections, all confirmed against the logs:
  - **13F loaded 46 of 53 published zips** — missing 2021q3–q4 AND 2022q4–2023q4 (7 zips), plus
    Jun–Aug 2026. `sec13f_run_w172715.log` line 1 says "53 zips, 49 to load"; run died mid-2014q3
    redownload. My "2022q4–2023 gap" undercounted.
  - **FAERS non-contiguous CONFIRMED** (original row-16 concern was right, my "hard stop" was the
    FDA_DT smear): `faers_checkpoint.json` holds 41 quarters, 2004q1–2013q4 + 2014q2; 2014q1/q3/q4
    absent. AND 4 of 5 landing tables EXCEED the checkpoint (DRUG +901,608, REAC +754,668,
    DEMO +260,057, OUTC +170,437; INDI exact) — surplus unexplained, dup-load suspect.
  - **CAMPD daily = 2015–2025 only** — 1995–2014 never attempted; the facility sibling proves the
    publisher goes back to 1995. Missing chunks include MT and SD 2024, real coal states.
  - Method lesson recorded: checkpoint-sum = landing cannot detect never-attempted files.
  - NEISS 1999–2025 present, 2026 absent; third contracts copy = declared FY2025 subset;
    CDC injury exactly 132,000 "tranche2" — suspect cap, untriaged.
- **Row 4 — PREMISE STALE; layer exists live, coherence NOT fully verified (2026-08-31, amended
  by skeptic).** The ranked row was built from the 08-21 handoff ("not started") while
  `CLOCK_FINDINGS.md` carried the disproof — the audit builder cited the stale wrapper.
  What is confirmed:
  - Classification coverage: `clock_index.csv` = 2,089 rows / all 482 tables / every domain.
    "253 never reviewed" is dead. Coverage only — correctness of the review is NOT re-verified.
  - `planned` category: built per-row; 584 planned rows live in TIMELINE__WAREHOUSE.
  - Canonical layer: live — `LIBRARY_MARTS.TIMELINE` 435 objects, registry 643 = seed exactly,
    warehouse timeline 1,165,672 rows. ⚠ Registry live=seed proves the seed LOADED, nothing more.
  - Skeptic corrections folded in:
    - `TIMELINE_LAYER.md` doc numbers are wrong: says 647 tables / 244 unclocked / 230 happened;
      seed says 643 / 241 / 229. Doc needs the fix, warehouse is fine.
    - **One orphan view: `timeline__transport__fed_faa_registry`** — view model + clock_index rows,
      NO registry seed row. Exactly what the guard test should catch; it has no on-disk pass
      evidence, so either it doesn't check this or it hasn't run. FAA registry is also a known
      epoch-1970 trap table.
    - Drift arithmetic: ~61 net-new mart tables since 08-21 uncovered, not 58. Name-matching
      method itself validated against gen_time_views.py aliasing.
    - The handoff's planned/reported-vs-happened TRIPWIRE was never built — the guard only checks
      registry↔view agreement. Open item.
    - Underlying-row coverage of TIMELINE__WAREHOUSE not recomputed vs the doc's 720M claim.
  - Remaining: gated dbt refresh for the ~61 new tables; guard-test run evidence ties to row 7;
    26 "unclear" labels contradict CLOCK_FINDINGS's "zero malformed" line; row 14 inherits the
    unre-verified review quality.
- **Row 5 — SWEPT (2026-08-31): the 52 unchecked edges are now name-checked or classified name-free.**
  New script `scripts/pass2_level2_namecheck_2026_08_31.py` extends the 08-29 precision method;
  results in `reports/recon/pass2/pass2_level2_namecheck_2026-08-31.json`; handbook CSV
  (`handbook_pass2_edges_2026-08-29.csv`) verdicts patched, 52 rows.
  - **41 edges scored live (skeptic recount — an earlier "33/30" was double-subtraction):
    36 score ≥86%.** The five below the bar: HRSA-BHCMIS 35.0 (site-vs-grantee grain),
    FDIC PARCERT 36.7 (new SUSPECT), OSHA→IRS 70.2, FDIC ULTCERT 70.0 (lineage),
    OSHA→5500 80.4 — the last three graded SOLID-with-note, NOT ≥86 SOLID; the CSV notes
    carry the numbers. PECOS family: names 100%, states 93–100 (not "100/100").
    All three contractor-UEI→SAM copies: names 100%.
  - **1 new SUSPECT: FDIC direct-parent PARCERT** — names 36.7%, states 57.1% on its 49 pairs
    (near-census of the edge; z≈3.5 vs its ULTCERT sibling — not sampling noise).
  - **9 name-free classifications with reasons** in the JSON's name_free list. GLEIF successor:
    live full-table count, 0 of 34,181 successor rows carry a name.
  - **HRSA site NPI→NPPES: strongly supported, not "proven."** Two-hop: parent-grantee name vs
    NPPES 94.6%, either-name 96.6% vs site-name 28.3%. ⚠ Skeptic caveat: the matcher's
    false-positive rate on generic org names is ~12% on an offline null model, and
    health-center names are the most FP-prone family — 94.6% clears that bar comfortably
    but is not immune to it.
  - ⚠ **Matcher false-positive risk is real, was unmeasured**: containment + first-12-chars
    rules pass "UNIVERSITY OF MICHIGAN"="UNIVERSITY OF MISSOURI". Script now also samples
    matched pairs per edge so FPs are auditable; a shuffled-pair null test per edge is the
    outstanding improvement. Sampled mismatches remain false negatives — both directions err.
  - Reproducibility fixed post-skeptic: committed script now carries the corrected FHA name
    column (verified NOT tautological — originator name ≠ sponsor name, 0 of 15 identical)
    and GLEIF in NAME_FREE, matching the JSON. 53 CSV rows changed, not 52.
  - **Still open from row 5:** the 4,512 CONNECT_EDGES have zero per-edge precision receipts —
    that is spine-scale work (row 9 territory), not a session task; and FEC committees→candidates
    25% + FDIC successor 25% remain "by design" explanations that only a person-level check
    could fully close.
- **Row 12 — PATCHED where permissions allowed (2026-08-31).**
  `add_spine_columns` added to the warehouse-gate spine regex; self-test extended to 31 cases,
  ALL PASS. `trusted_source_predicate` confirmed defined-never-called (spine code, retired —
  wiring is gated spine work). ⚠ TWO FIXES BLOCKED by the permission classifier, need Chris:
  (a) adding `git push` to block-dangerous-git.sh; (b) widening the PreToolUse matcher from
  Bash to Bash|PowerShell — as it stands EVERY PowerShell command bypasses both the git guard
  and the warehouse gate, and this session ran the warehouse through PowerShell all day.
- **Row 7 (repo half) — "relaxed not fixed" fear mostly defused (2026-08-31).**
  `reports/test_fix_session_2026-08-25.md` + spot-checked yml diffs from `c8dc64e5`: the two
  sampled downgrades (IRS zip not_null, MPV unique) are warn-downgrades with live-verified,
  detailed inline justifications — exemplary, not silent relaxation. Still open: no on-disk
  full-suite pass evidence; 643 models with zero tests; one real `dbt test` run needs
  Chris's go on compute cost — no real number exists for it.
- **Row 17 — CLOSED (2026-08-31).** The stale 2,244 quote was already corrected in both
  pass-1/pass-2 files (working tree). The "3 tables failed to scan" are explained stale-index
  entries in LOCATION_VALUES.md — two marts no longer exist, one lost its indexed columns;
  nothing to rescan. FAA registry shows up again, consistent with row 4's orphan view.
- **Row 18 — SWEPT (2026-08-31), all candidates verified real.** COUNT/COUNT(DISTINCT)/samples
  run live on the catalog-only candidates: CONTRACT_AWARD_UNIQUE_KEY 5.72M distinct of 6.33M;
  TICKER 1,009; LDA CLIENT_ID 88,607 / REGISTRANT_ID 11,723; FJC NID unique 4,067 in judges,
  clean FK from appointments (4,766 rows → 4,067); COMMITTEE_CODE 228; BILL_NUMBER 10,564
  (composite, as flagged); JUSTICE_CODE 40; FEC SUB_ID 84,172,112 fully unique.
  **UPIN contradiction RESOLVED: the column holds empty strings, not NULLs** — blank-aware
  count 5,955 filled / 5,786 distinct; the old 474 was a catalog sample slice.
  LINKAGE_ID is not a column on FED_FEC_CAND_CMTE_LINKAGE under that name — needs the real
  column name before checking.
- **Row 19 — SWEPT + FIXED (2026-08-31, amended by skeptic).** Premise half-stale: the 953
  descriptions are hand-written dictionaries + rule fallback (`0ed46425`), not blind auto-gen.
  30-row sample of TRENDABLE.csv: labels sane. But the prose contradicted this audit's own
  coverage findings — **11 reader-facing descriptions corrected** in
  `scripts/census/plain_english.py` and `reports/time_index/trendable.html` rebuilt:
  CONTRACTS_FULL + ASSISTANCE_FULL (truncation), NHTSA_RECALLS (post-2010), HMDA_HISTORIC
  (2015–17), FED_CFPB_HMDA + **HMDA_LAR** (DC-only — LAR was a skeptic catch, missed on the
  first pass), FEC_INDIV (2 cycles), MAUDE (0.05%), SENATE_LDA (14 yrs), SUBAWARDS (stops
  2019-05), OPEN_PAYMENTS (PY2022–24), NOAA_AIS (8 days), FAERS DEMO+DRUG (2004–mid-2014).
  Skeptic also confirmed the row-7 commit holds only 3 severity downgrades total — read all
  three, all clean; one unquantified grain-widening (wayback epstein) is the residue.
  Row 18 receipts persisted post-skeptic: `scripts/row18_id_candidate_receipts.py` →
  `reports/row1/row18_id_candidate_receipts.json` — all 11 counts reproduced exactly.
- **Row 15 — SPOT-CHECKED (2026-08-31).** Six un-recorrected pass-1 claims re-measured live
  (`scripts/row15_pass1_spotcheck.py` → `reports/row1/row15_pass1_spotcheck.json`):
  - **Confirmed exactly:** DEA_NO 148,588 buyer-side distinct; MINE_ID violations→mines 100%
    on 31,277; PWSID violations→systems 100% on a 182K sample; CL_COURT dockets→courts 100%
    on 2,199 courts.
  - **Not reproducible:** IMO "8.7K distinct" — live count is 6,304 on USCG vessel docs;
    and pass-1's UK COMPANY_NO "97%" — live reproduces pass-2's 85.7% exactly, so pass-2's
    correction stands and pass-1's number belongs to some other cut.
  - Read: pass-1's un-recorrected core holds up well; its two soft numbers were already
    superseded or slightly stale. Medians for the big families remain re-runnable-artifact-free
    (the known gap; spine-scale work).
- **Row 12 addendum (2026-08-31, Chris approved fixes):** `git push` added to
  block-dangerous-git.sh and live-verified — the guard fired on the test command itself.
  ⚠ The Bash|PowerShell matcher widening in `.claude/settings.json` remains
  classifier-blocked even with approval — one-line manual edit for Chris:
  `"matcher": "Bash"` → `"matcher": "Bash|PowerShell"`.
- **Row 7 — run evidence CLOSED; warn population OPEN (2026-08-31, Chris go; amended by
  session-close skeptic).** Full `dbt test` via dbt-fusion: **5,156 tests / 4,898 pass /
  246 warn / 11 error + 1 fail** — first on-disk full-suite evidence
  (`target/run_results.json`; its elapsed_time says 2h24m wall, the console summary printed
  13m27s — discrepancy unexplained, quote run_results). 08-05 parse blockers gone.
  ⚠ Skeptic: the 246 warns hide **99.4M failing rows** (138 not_null warns; SDWA alone ~25M
  nulls; 5 key_is_real warns = the "looks like an ID, isn't" rule firing) — NOT the 3
  documented downgrades. Warn triage is open work. The 12 non-passes have exactly TWO root
  causes, both already-diagnosed drift classes:
  - 11 × LEIE: the deployed staging view for FED_HHS_OIG_LEIE lacks `_INGESTED_AT` — tests
    error at compile against the live view. Same deployed-view-drift disease as row 2;
    same fix, the gated `dbt run`.
  - 1 × `assert_ripple_timeline_registry` — the timeline guard FAILING is row 4's orphan
    FAA view + registry mismatch, caught by the guard exactly as designed. Fix rides the
    same gated run.
  - 643 zero-test models remain row 7's residue, alongside the warn triage above.
- **THE GATED DBT RUN — EXECUTED (2026-08-31, "greenlight rebuild").** 2,308 models,
  **2,237 success / 35 error / 36 skipped, 30m16s**. The August-28 normalizer fixes are now
  DEPLOYED — row 2's drift is closed: `tests/test_staging_spine_id_parity.py` 71/71 against
  the live warehouse. Error triage, every one explained:
  - ~28 politics-mirror models: BLOCKED by the standing no-overwrite guard — correct behavior,
    the guard protecting audited tables did its job.
  - 4 staging views (assistance_full, contracts_full, open_payments_gnrl, partd) —
    pre-existing breakage: those landing tables carry lowercase column names, the models
    reference them unquoted-uppercase. Repo fix queued, not caused by the run.
  - LEIE: root cause found and FIXED — that loader wrote `INGESTED_AT` unprefixed; model
    said `_INGESTED_AT`. One-line model fix, rebuilt, **11/11 LEIE tests now pass**.
  - Timeline guard still fails (4 rows) — the FAA orphan view needs a registry-seed
    decision (add the row or delete the view), not a rebuild. Chris's call.
  - Utah mis-joins still fail — expected: they live in CONNECT_EDGES, which only a gated
    spine rerun regenerates (row 9 session).
- **POST-REBUILD CLEANUP — ALL GREEN (2026-08-31).** Every remaining error fixed and re-proven:
  - 3 staging views fixed + rebuilt: the generator left pure-lowercase and digit-leading
    column names unquoted (`1862_land_grant_college` etc — Snowflake resolves unquoted to
    uppercase). Quoted 427 identifiers by script (skeptic recount); digit-leading aliases
    renamed `land_grant_college_1862` style — verified no downstream referenced the old
    form (it never compiled, so nothing could).
  - `stg_fed_cms_open_payments_gnrl` DISABLED with inline reason — its source table never
    landed (INCLUDE=N orphan from the row-1 sweep).
  - LEIE view fixed (unprefixed `INGESTED_AT`) — 11/11 tests green.
  - **Timeline guard PASSES.** Its 4 failing rows were NOT the FAA orphan — they were
    `planned` tags frozen in the environment rollup table on build day, whose dates
    (Aug 27–30) have since passed. Rebuilt the rollup + warehouse timeline: green.
  - ⚠ Design flaw exposed: the planned/actual tag is DERIVED against current_date but
    FROZEN into the two rollup tables — the guard re-fails whenever a rollup ages past a
    planned date. Right fix (skeptic-corrected): store base_kind in rollups and derive
    planned-vs-actual at read time; plus scheduled rollup refreshes. Do NOT freeze an
    as_of — that would make the check unfailable. Parked for Chris.
  - ⚠ Guard blind spot, named (skeptic): checks walk registry→warehouse and
    timeline→registry, but NOTHING walks warehouse→registry — a stray view in the
    TIMELINE schema that no index unions is permanently invisible. Guard green ≠
    schema clean.
  - FAA: (skeptic correction) both the mart and timeline models were ALREADY tombstoned
    2026-08-22 — enabled=false, `select 1 as retired`. The residue is stale warehouse
    OBJECTS dbt never drops on disable; they are already on Chris's drop list.
- **DUPLICATE DROPS — EXECUTED BY CHRIS (2026-08-31, "greenlight destroy").**
  `scripts/drop_duplicate_families_2026_08_31.py`, run by Chris's own hand after the
  harness refused Claude the destructive command. Log: `reports/row1/drop_log_2026-08-31.json`.
  - **8 tables DROPPED**, ~9.3M duplicate rows: all 5 `FED_EPA_RCRA_RCRA_*` doubles +
    2 bare-prefix ICIJ copies — each proven content-identical by HASH_AGG first.
  - ⚠ **8 copies SKIPPED — the "triplicate" was never true triplicate.** Same row counts,
    DIFFERENT content hashes: the whole `XC_ICIJ_OFFSHORE_*` family and 4 bare-prefix
    tables are a different snapshot vintage. The audit's earlier caveat ("identical
    metadata counts, not proven identical content") was exactly right — a count-based
    drop would have destroyed a distinct scrape. Vintage comparison = open work.
  - 2 OTHERS twins report zero data columns — empty shells or absent; untouched.
  - Canonical prefixes proven from what dbt staging reads: `FED_ICIJ_OFFSHORELEAKS_*`,
    `FED_EPA_RCRA_*`. CONTRACTS_FULL kept — labeled slice, staged, described honestly. `FED_NIH_REPORTER` is FULLY loaded:
  FY2000–2026 contiguous, 2,122,611 rows, **zero duplicate APPL_IDs**, FY2024 = 83,519 vs the API's published
  83,516. The "capped at 206,333, FY2000–2002 only" decision-log entry was later overtaken — the resume ran to
  completion. Registry NOTES still carry the stale cap text.
