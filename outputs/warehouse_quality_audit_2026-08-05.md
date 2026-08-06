# Warehouse quality/health/reliability audit — 2026-08-05 (evening)

**Method:** 6 independent read-only agents, each given the same brief (find NEW evidence, don't
recite CHRIS_DECISIONS.md, run real queries, cite real numbers/files, rate severity). No writes, no
loader runs. Live against `LIBRARY_RAW`/`LIBRARY_META`/`LIBRARY_MARTS` as of ~22:00-22:45 PT.

**Bottom line:** the individual fixes this platform has made (the density gate, the read-only role,
the append-only review-writer role, CI role scoping) are well-built where they're used. The problem
is coverage — most of the warehouse, most of the loaders, and most of the catalog sit *outside* the
disciplined path, and the disciplined path itself has two live, active blind spots being used again
tonight.

---

## CRITICAL — act on these first

### 1. The review queue is live-broken, right now, in violation of the platform's one hard rule
`LIBRARY_MARTS.REVIEW.LEAD_QUEUE` (17,302 rows) is missing **4 leads** that exist in the real
detection output (`LIBRARY_META."CONNECT".V_LEADS_PUBLISHED`, 17,306 pending/needs_work rows) —
confirmed by a live `dbt test` failure (`assert_lead_queue_reconciles`) and a direct `MINUS` query.
`LEAD_QUEUE` is only refreshed by `dbt build --select marts.review`, and it wasn't rebuilt after the
last detection run. CLAUDE.md's one non-negotiable: *"Human sign-off on every finding. Auto-publish
is blocked. No exceptions."* Right now 4 findings aren't blocked — they're just invisible to the
human reviewer. Nobody would know without running this exact test.
**Likely root cause (see #7):** two different `dbt` binaries share the `dbt` command name, and the
sanctioned rebuild script doesn't pin either one — a plausible reason the queue silently drifted.
**Fix:** run `dbt build --select marts.review` to catch it up (that's a write, so I didn't do it
under the read-only audit constraint), then pin the build wrapper to one dbt engine.

### 2. A "mart"-trust table is lying about its own scope — the exact false-claim scenario this audit was asked to look for
`FED_CFPB_HMDA` (28,301 rows, `LIFECYCLE='modeled'`, `TRUST_LAYER='mart'` — the platform's highest
trust label) claims to be the nationwide 2022 HMDA mortgage dataset. Every single row is
`STATE_CODE='DC'`, `ACTIVITY_YEAR='2022'`. Real nationwide 2022 HMDA has ~15M+ records; this is a
sliver of one non-state jurisdiction. The density gate passed it (67.9% populated — real columns,
just for DC only). The mart carries `derived_race`, `derived_ethnicity`, `derived_sex`,
`action_taken`, `denial_reason_1-4` — exactly the columns a fair-lending investigation would query.
Its only test is `not_null` on `state_code`, which trivially passes on a column 100% populated with
one wrong value. **A reporter filtering this for any state but DC gets zero rows and could read that
as "no red flags."** Made worse: the real 19.1M-row historic HMDA file is already sitting in the
warehouse under a *different, unregistered* name (`FED_CFPB_HMDA_HISTORIC`, see #5) — the good data
exists, it's just not the table anyone would query.
**Fix:** needs a human call now — re-pull the real nationwide file, or relabel this table honestly
(`FED_CFPB_HMDA_DC_2022`) before anyone uses it for a lending-discrimination story.

### 3. The quality gate has an active, currently-used bypass — 42% of warehouse volume never touches it
**152 of 2,061 landing tables (366M rows, ~42% of total warehouse row volume) have zero rows in the
run-log** — never assessed, never logged, no status at all. This includes flagship tables:
`FED_SEC_13F_HOLDINGS` (101.3M), `FED_COURTLISTENER_DOCKETS` (71.7M), `FED_CFPB_HMDA_HISTORIC`
(19.1M), `UK_COMPANIES_HOUSE_PSC` (7M), the FDA FAERS tables (5-21M each). Root cause: at least 3
scripts (`fac_single_audit_load.py`, `hmda_historic_lar_load.py`, `cms_bulk_discover_load.py`, the
last being a multi-table discovery loader) hand-roll a staging→swap with `if row_count == 0: skip`
as their entire gate — no per-column blank check, no `assess_density`, no `_log_run`. **This is
happening again tonight**: the FJC re-ingestion (genuinely real data this time,
`FED_FJC_IDB_APPELLATE`, 988K rows) went through this exact unlogged path — the fix for the
platform's own most notorious incident is itself invisible to every governance mechanism the
platform has.
Separately: the one manual tool that's actually *stronger* than the load-time gate
(`audit_blank_landing.py`, catches non-blank single-value columns) is not scheduled anywhere — runs
only when a human remembers.

### 4. 0 of 3,801 dbt tests can catch the platform's own signature bug
66.9% of all dbt tests are `not_null` — the exact test type that already failed to catch NPPES `EIN`
and NOAA_AIS `imo_number` per CLAUDE.md's own history, because it passes on `''`. Zero tests anywhere
in the project check for blank-string/sentinel masking, a distinct-count floor, or anything beyond
null/uniqueness/enum membership. Confirmed concretely: `FED_DOL_FORM5500`'s own schema.yml has real
tests — just not on `EIN`/`SPONSOR_DFE_EIN`, the two columns that turned out to be the trap. If a raw
table silently goes blank/masked today, this test suite would not catch it before the mart looks
clean.
**189 of 1,440 dbt models (13%) have zero tests at all**, and 23 mart models — including the two
20M-row FDA FAERS tables this project hand-verified healthy in a chat transcript, never a durable
test — aren't even referenced in a schema.yml. Wider still: **~half of all 2,062 raw landing tables
have zero dbt presence, full stop** (not "zero tests" — zero model).

### 5. The catalog is not a reliable gate or a reliable description
- **65 unregistered landing tables (69.6M rows)** — 2 are *already live in production marts*
  (`HEALTH__FED_HRSA_NPDB`, 1.9M malpractice records; `JUSTICE__FED_ATF_FFL`, 77.5K firearms
  licensees) with zero documented license terms, join keys, or accountability rating. 30 more have
  dbt staging models already built (one `dbt run` from a mart), including the entire EIA860/861
  electricity domain (25 tables), `FED_FEMA_IA_HOUSING_REGISTRATIONS` (3.08M person-level disaster
  records), and the real 19.1M-row HMDA historic file mentioned in #2.
- **Every sampled "daily"-cadence source (33/33) is 13-34 days stale.** No scheduler/cron exists
  anywhere in the codebase. `FED_CFPB_COMPLAINTS` (17.2M rows, ANCHOR tier, "daily") has been loaded
  exactly once. `UPDATE_CADENCE` describes how often the government publishes, not how often Ripple
  refreshes — nothing in the schema distinguishes the two.
- **29% of a 244-source sample has a >5x gap between the registry's stated VOLUME and the real live
  count** (both directions; up to 15,000x — `fed_david_rumsey` claims "~150,000+ map records," holds
  10). 27 of the 71 mismatches are ANCHOR tier, the platform's highest-trust bucket.
- **A new genuine duplicate**, not on the known-11 list: `INTL_NTI_CNS_DPRK_MISSILE_TESTS` and
  `XC_NAGIX_DPRK_MISSILE_TESTS` are verbatim-identical text under two registered source IDs — citing
  both as corroboration would be citing the same record twice.

### 6. The "mystery parallel writer" is solved — and the real answer is worse than an intruder
Snowflake's `ACCOUNT_USAGE.QUERY_HISTORY` shows all 6 duplicate tables from tonight's incident were
created by the **same single identity** (`CROGG23`, role `ACCOUNTADMIN`) across a dozen-plus
concurrent sessions in a 7-minute window. It wasn't a breach — it was Ripple's own concurrent agent
processes, all riding one shared credential, invisible to each other. Every `query_tag` in that
window is blank, so even now there's no way to tell which process wrote what.
Structurally, this can happen again at any time: `config.py` defaults `SNOWFLAKE_ROLE` to
`ACCOUNTADMIN`, the live `.env`'s PAT is bound to that role, and 168 files in the repo connect via
this path with no override. `CHRIS_DECISIONS.md`'s own open item **A00** (cut over to a scoped
`RIPPLE_TRANSFORM_RW` PAT) is still `OPEN`. **No concurrency control exists anywhere** — not for the
warehouse (no session tagging, no lock table) and not for `CHRIS_DECISIONS.md` itself (currently 29
uncommitted insertions on disk with zero lock/version check; two sub-agents wrote to it concurrently
in this very session tonight).
**And there's effectively no undo.** Time Travel is 1 day on every database (Standard Edition
default, never raised) — the only recovery path for an overwritten table, closing in 24 hours. The
one file-based DR backup (`backups/dr/`) covers 8 small control tables, is **31 days stale**, and
never covered `LIBRARY_RAW.LANDING` (875M+ rows) in the first place. The "never-shrink floor" that
would stop a truncated load from overwriting good data (`ingest._latest_success_rows`) is fully
built but has exactly **one caller** in the whole codebase (`politics/loaders/build_skeleton.py`) —
every other loader overwrites before the density gate even runs.

---

## SIGNIFICANT

- **45% of sampled "hard-tier" join keys are broken** (stratified sample, 88 tokens / 27 sources,
  15 domains): masked-blank sentinels, columns that don't exist in the schema, or mislabeled
  semantics. Worst case: `FED_DOJ_FCA_SETTLEMENTS` (fraud-settlement data, `TRUST_LAYER='mart'`) is a
  scraped DOJ nav-menu, not case data — `CASE_TITLE` values are page-link labels like "Fraud
  Section." Also newly found: `FED_USASPENDING_CONTRACTS.RECIPIENT_DUNS` is 100% masked-blank across
  6.3M rows, directly contradicting a "verified, exhaustive" claim already recorded in
  CHRIS_DECISIONS.md (which checked presence, not `COUNT(DISTINCT)`, on the same column). The newer
  `NATURAL_KEY` registry field is far more trustworthy (6/6 real in-sample) but only covers 43% of
  included sources.
- **Every quality gate in the codebase runs after the write, not before.** `ingest.py::run_ingest`
  writes via `overwrite=True`, *then* runs `assess_density` — a bad load can only be re-labeled
  `'empty'` after it has already replaced the last-known-good raw table. Same order in
  `_small_flat_loader.py`. This is the FED_FJC_IDB failure mode, structurally still possible today,
  on the ~40 loaders that go through this exact path.
- **`tier1_bulk_batch_load.py`** (~30 no-auth bulk sources: CFTC, Fed Reserve, OSHA, DOL WHD, EPA
  TRI/eGRID, Treasury, OPM, CourtListener, Mapping Police Violence, more) has **no quality gate and
  no audit-log call anywhere**, and `main()` always `return 0` regardless of how many datasets
  failed. Two retry scripts (`tier1_bulk_retry.py`, `tier1_bulk_retry2.py`) exist specifically
  because the first run already had real silent failures found by hand — and both retries copy the
  same no-gate pattern.
- **`_bulk_load_utils.py`'s row-count-regression guard is dead code** — only fires if a caller passes
  `prev_row_count`, which none of the 9+ callers ever do.
- **Two `dbt` binaries share the `dbt` command name** (project venv has dbt-core 1.11.12; global PATH
  has dbt-fusion 2.0.0-preview) and the sanctioned `build_review.bat`/`.sh` wrapper doesn't pin
  either. Re-tested tonight: both engines actually parse/compile clean right now — the "dbt-fusion
  breaks the whole project" note in CHRIS_DECISIONS.md is not currently reproducible at that scope.
  The real, narrower issue: 3 staging models are permanently broken (unquoted `GROUP`, unquoted
  hyphenated column) — already fixed once at the mart layer, never propagated back to the
  auto-generated staging model.
- **`fda_faers_load.py` and `sec_13f_load.py` discard the quality-gate's return value** — print
  "DONE," exit 0, regardless of gate result. Other callers of the same function handle it correctly,
  so this is inconsistency, not a missing capability.
- **The read-only role is real but narrow.** `RIPPLE_READER` is genuinely zero-write (verified via
  live `SHOW GRANTS`), and `viz/sqlrun.py`'s `_verify_lane()` does real defense-in-depth checking.
  But it only activates when a caller explicitly supplies the serve PAT — every other one of the 168
  files connecting via `snow.connect()` gets the ACCOUNTADMIN default. The good control exists; it's
  the exception, not the rule.

## MINOR

- 4 fully-built loader scripts from tonight (`fjc_idb_load.py` — the actual fix for the flagship
  FJC incident — plus the ICE/MO/PBGC loaders) are uncommitted; the fix only exists on disk.
- One live-failing dbt enum test (`FDA drug enforcement classification`) is a test-completeness gap,
  not a data bug — but it trains reviewers to see red next to genuinely critical failures, real
  alert-fatigue risk. 185 tests (4.9%) are permanently `severity: warn` with no tracked promotion
  path.
- A meta-column naming inconsistency (`INGESTED_AT` vs `_INGESTED_AT`) lets provenance columns leak
  into density measurement on at least one table (Harris County facility listing), slightly inflating
  its measured density.
- `FED_OFAC_SDN.IMO` is 89.4% masked-blank — semantically expected (most SDN entries aren't vessels)
  but the same masking mechanism CLAUDE.md warns about; a naive coverage stat on this column would be
  badly wrong.

## What's genuinely solid (say the good news too)
- The density gate itself, where it runs, works exactly as designed for the shape it was built for.
- `RIPPLE_READER` (zero-write) and `RIPPLE_REVIEW_WRITER` (append-only, insert+select only, no
  update/delete) are both real, verified live tonight.
- CI's role was actually fixed 2026-07-31 (`RIPPLE_TRANSFORM_RW`, confirmed in `.github/workflows/dbt.yml`).
- `write_pandas(overwrite=True, auto_create_table=True)` is safer than it sounds — swap-based, not a
  naive truncate-then-load; every `overwrite=True` call in the codebase pairs it correctly.
- Today's newest loaders (10 spot-checked, including the ones built earlier tonight) are consistent
  and follow the disciplined pattern — the convergence problem is in older/parallel bulk-tier code,
  not in the newest work.
- The lock-file pattern (`outputs/_heartbeat.lock`) and the shrink-guard pattern
  (`build_skeleton.py`) both already exist in the codebase — this is a "built once, didn't
  generalize" gap, not a "don't know how" gap. Cheaper to fix than it looks.
- `FED_NIH_REPORTER`, recorded in the 2026-07-31 baseline as 5,000 rows all-blank, now shows 405,000
  rows with 5 of 6 declared keys real — a genuine prior fix that held.

## Recommended order of attack
1. Rebuild `LEAD_QUEUE` now (#1) — it's a one-command fix and it's the rule with zero exceptions.
2. Human call on `FED_CFPB_HMDA` (#2) — re-pull or relabel before anyone queries it for a story.
3. Pin the `dbt` build wrapper to one engine (#1's likely root cause) — cheap, prevents recurrence.
4. Route `fac_single_audit_load.py` / `hmda_historic_lar_load.py` / `cms_bulk_discover_load.py` /
   `tier1_bulk_batch_load.py` through the real gate (#3, #Significant) — copy
   `politics/loaders/build_skeleton.py`'s pattern, it already does this correctly.
5. Cut the default credential over to a scoped, non-ACCOUNTADMIN PAT (#6) — CHRIS_DECISIONS.md's own
   open item A00, still not done.
6. Decide whether snapshot-replace-with-no-backup is acceptable architecture for irreplaceable public
   records, or whether landing tables need real backup/versioning (#6) — this is a taste/scope call,
   not a bug fix.
7. Registry sweep: the 65 unregistered tables, starting with the 2 already live in marts (#5).
