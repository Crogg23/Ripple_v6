# Tier 1 + Tier 2 Build Plan — Stress-Test & Correction
_2026-06-30_

## Verdict

**GO-AFTER-STEP-0.** The strategy is sound and the join-key moat is real, but the plan was built from web recon and never grepped the live repo — so it will fail at import on the first loader and double-load at least 4 already-onboarded sources. **Two STEP-0 blockers gate everything: (1) 20 loader/registry files hardcode `c:\Code\Ripple_v6` and load zero creds on this mac; (2) `~/.snowflake/connections.toml` points at a DIFFERENT account (UKB67948, OAuth, no PAT) than `.env`/`snow.py` (ONEAFDA-UMB20733, PAT), so dbt and the `snow` CLI silently authenticate to the wrong warehouse.** Fix both, prove `current_account()=ONEAFDA` and one politics loader lands, reconcile the duplicate SIDs — then the queue is runnable.

---

## BLOCKERS — fix before any build (Step 0)

| # | Blocker | Evidence (file:line / url) | Fix | Effort |
|---|---------|---------------------------|-----|--------|
| **B1** | **20 files hardcode `c:\Code\Ripple_v6`** in `sys.path.insert` + `load_dotenv(r"c:\...\.env")`. On mac these paths don't exist → `import snow`/`import ingest` die at import, `.env` loads NO creds. The 3 clone-templates carry the bug → cloning propagates it into all 17 new loaders. | `scripts/fec_pas2_load.py:21-27`, `politics/loaders/build_skeleton.py:37`; full list: `politics/loaders/{build_bills_leg,build_cm26_refresh,build_indiv_donations,build_money_spine,build_skeleton,build_votes_leg,build_who_won,smoke_bills,smoke_itcont,smoke_money,smoke_test,smoke_votes,smoke_who_won,verify_cm26}.py`, `politics/registry/{promote_keys_and_fix_domain,register_political_sources}.py`, `scripts/{congress_committee_membership_load,fec_independent_expenditure_load,fec_itcont_load,fec_pas2_load}.py` | Replace the 3 hardcoded lines fleet-wide with the repo's OWN portable pattern (`scripts/irs_bmf_load.py:26-31`): `_REPO = Path(__file__).resolve().parents[1]; _LIB = _REPO/"library-onboarding"; sys.path.insert(0, str(_LIB)); load_dotenv(_LIB/".env", override=True)`. **Fix `build_skeleton.py` + the 2 registry writers FIRST**, then the other 17. Works on both mac and the Windows box. | **0.5d** (incl. smoke-import of every loader) |
| **B2** | **Two-credential conflict.** `.env` (what `snow.py:44` reads via `config.py`) = ONEAFDA-UMB20733 + `SNOWFLAKE_PAT`. `~/.snowflake/connections.toml` (created today, 102 B) = UKB67948, `OAUTH_AUTHORIZATION_CODE`, empty role, no PAT. `snow.connect()` never reads the toml → toml is inert for loaders but IS what the `snow` CLI and dbt read by default. Loader lands in ONEAFDA; dbt/CLI browser-OAuths into UKB67948 → wrong-account marts or an interactive prompt hang. | `snow.py:44`; `config.py`; `~/.snowflake/connections.toml`; CLAUDE.md + `.env` both say ONEAFDA (canonical) | Pick ONE truth. Either (a) delete/rename `connections.toml` so nothing silently grabs UKB67948, or (b) rewrite it to `account=ONEAFDA-UMB20733` with the PAT as `token`/`password`. **Ship nothing until** `python -c 'import snow; print(snow.connect().cursor().execute("select current_account()").fetchone())'` returns ONEAFDA. | **0.25d** |
| **B3** | **`DBT_PROJECT_PATH` not set** → `config.dbt_dir()` raises `ConfigError` the moment any dbt checkpoint runs. Live `.env` keys are only `SNOWFLAKE_ACCOUNT/USER/PAT/WAREHOUSE, SAM_API_KEY`. Separately, dbt would resolve to the B2 wrong-account toml. | `config.py:80`; live `.env` key list | Decide the mart path: EITHER set `DBT_PROJECT_PATH` to the mac dbt root (verify `dbt_project.yml` exists) AND fix dbt's profile to ONEAFDA — OR **build politics marts with in-loader `CREATE OR REPLACE TABLE` DDL** (the `build_skeleton.py` idiom the existing politics loaders already use) and skip the dbt checkpoint for this batch. Recommend the in-loader DDL path — it's what the domain already does. | **0.25d** (decision + wire) |
| **B4** | **land() has no completeness referee** — the exact mechanism that let SAM land 1k of 167k rows as `status='success'`. Density gate measures POPULATED-CELL fraction (1% floor), blind to row COUNT. `land()` takes only `(df, sid, url, msg)` — no `expect_rows`, no envelope reconcile. A stream that dies at row 2,001 of 6M lands dense, logs success. | `ingest.py:61,81-169`; `build_skeleton.py:107-131` (confirmed signature: 4 args, `overwrite=True`, no count check); `sam_exclusions_load.py:176-207` | Add `land(df, sid, url, msg, expect_rows=None, min_rows=None)`: log `status='partial'` (not success) when `len(df) < expect_rows` or when a paginated/streamed load ended on a throttle/cap. Add a **"never shrink below last success"** floor before snapshot-replace overwrites (protects 527/pas2 destructive refresh). Every new smoke test asserts an ABSOLUTE landed-count vs source-declared total. | **1d** (shared helper — pays off across all 18) |
| **B5** | **Duplicate SIDs** — 4+ proposed sources already exist as committed loaders + registered rows. Building them = second landing table + second registry row for identical data. | See Duplicate/reuse map below | Reconcile the SID map (next section) BEFORE any build. `register_political_sources.py` is append-only (`INSERT ... WHERE NOT EXISTS`, lines 41-42) — it CANNOT fix an existing row; metadata corrections ship as authorized scoped UPDATE (preview→`--apply`). | **0.5d** (reconcile + UPDATE scripts) |

**Step 0 total: ~2.5d.** Non-negotiable. Nothing runs until B1 + B2 are green.

---

## Duplicate / reuse map

| Plan item | Proposed id | ALREADY EXISTS as | Action |
|-----------|-------------|-------------------|--------|
| T1 #1 Committee membership | `fed_unitedstates_committees` | `fed_congress_committee_membership` — loader `scripts/congress_committee_membership_load.py:28` fetches the SAME `committee-membership-current.yaml` + `committees-current.yaml` from the SAME GH repo; registered `political_sources.py:402` (TIER 1, STEEL bioguide, landed) | **REUSE.** Kill the new id. Only genuine net-new = `committees-historical.yaml` + a one-row-per-committee sibling table → add as EXTENSION of existing loader. |
| T2 #7 House STOCK Act PTR | `fed_house_ptr` | `fed_house_clerk_ptr` — registered `political_sources.py:509` (same publisher, endpoint, PTR/XML+PDF pattern, 2014-present, same "don't build on House Stock Watcher" gotcha). Annual net-worth FDs = sibling `fed_house_financialdisclosure:530` | **RENAME** to `fed_house_clerk_ptr`. Land under `FED_HOUSE_CLERK_PTR`, refresh existing row. Route annual-FD PDFs to `fed_house_financialdisclosure`. |
| T2 #5 IRS 990/EO-BMF nonprofit (Phase 1 BMF) | `fed_irs_990_nonprofit` | `fed_irs_bmf` — loader `scripts/irs_bmf_load.py:41-43` pulls `eo{1..4}.csv` (same ~1.97M-org master, partitioned by region) to `LANDING.FED_IRS_BMF`, snapshot-idempotent | **REUSE for Phase 1.** Only the 990 e-file MeF XML is net-new → `fed_irs_990_efile` (NEW). Build `POLITICS__NONPROFIT_POLITICAL` on top of existing `fed_irs_bmf` + the new 990 table. |
| T2 #8 Federal lobbying LDA | `fed_lda_lobbying` | THREE registered ids: `fed_senate_lda`, `fed_senate_lda_bulk`, `fed_house_lda` (`political_sources.py:791-792`, loader-skipped, append-only). Sibling FARA = `fed_fara` | **RECONCILE, don't add a 4th.** Reuse `fed_senate_lda` as canonical (+`_bulk` children). Ship authorized UPDATE to repoint URL `lda.senate.gov`→`lda.gov`. |
| T1 #7 Bill full text | `fed_congress_govinfo_bills` | Correct reuse, WRONG mechanics. NOT a stub at `:188` (that's prose inside `fed_govinfo_billstatus` NOTES). Real row lives in `_ALREADY_REGISTERED:794` → loader SKIPS it, no dict to edit | **REUSE the id.** Land to `FED_CONGRESS_GOVINFO_BILLS`; metadata via authorized UPDATE, NOT a new dict (append loader would skip it). Add `fed_govinfo_plaw` as genuine net-new sibling. |
| T2 #9 Open States | `st_openstates` | Full registered row `political_sources.py:623` — but stale: `AUTH_REQUIRED='api_key'`, `PROBABILISTIC`, dead URL `openstates.org/data/`, `LICENSE="CC0 (verify per-dataset)"` | **REUSE id** (correct). Ship UPDATE: AUTH none (bulk S3 ungated), LICENSE public-domain-dedication, add BIOGUIDE for us-subset, URL→`open.pluralpolicy.com/data`. |
| T1 #4 Voteview HSall | `fed_voteview_hsall` | THREE rows (plan miscounts "4"): `fed_voteview_members:102`, `fed_voteview_rollcalls:123`, `fed_voteview_rollcall_meta:143`. `FED_VOTEVIEW_MEMBERS` already full-history | **REUSE the 3 ids.** No new overlapping id. Backfill INTO the same landing tables by expanding the congress range; marts key on `congress` and extend automatically. |
| T1 #8 SCOTUS→SCDB crosswalk (moat) | (moat infra) | `fed_scdb` — landed + modeled: `stg_fed_scdb__supreme_court_cases.sql`, `justice__fed_scdb.sql`, `freshness_mapping.json:347` | **REUSE landed source.** SCDB is not infra to build; only the tiny 49-justice hand crosswalk is new. |

---

## HIGH-severity corrections (per source)

### Voteview HSall (`fed_voteview_*`, 3 existing ids)
- **"Supersede the 4 rows" is a forbidden mutation.** `register_political_sources.py` is append-only (skips existing SIDs). It CANNOT supersede — it silently skips. **Fix:** backfill data into the SAME 3 landing tables via expanded congress range; if row metadata truly needs changing, ship a human-approved one-row UPDATE, never via the loader. Correct "4 rows" → "3 rows."
- **"One loader = 1789-present" is false for votes.** `FED_VOTEVIEW_MEMBERS` is ALREADY full-history (`build_skeleton.py:98-105` fetches unfiltered `HSall_members.csv`). Only votes/rollcalls is scoped — and `build_votes_leg.py:47-48` does per-congress files (`H118_votes.csv`, `CONGRESSES=['118','119']`), NOT the single `HSall_votes.csv`. **Fix:** switch votes leg to `HSall_votes.csv` (700MB) or loop congresses 1..119.
- **Mart silently amputates blank-bioguide members.** `politics__member_voting_record.sql:35` filters `congress in ('118','119')` AND `:120 where bioguide is not null` — a 19th-c. member with blank bioguide vanishes with no error. The plan's `>=95%` gate is MODERN-congress only, so a pre-1900 hole passes undetected. **Fix:** key historical voting/ideology marts on **ICPSR (the true 100% PK)**, carry bioguide as optional enrichment, REMOVE the `where bioguide is not null` amputation (replace with a `has_bioguide` flag), measure + store bioguide non-null % per-congress, add a pre-1900 smoke gate.

### FEC PAC→candidate money (`fed_fec_committee_to_candidate`)
- **pas2 SUM ties to NO OpenFEC field.** itpas2 mixes 24K (direct contributions) with 24A/24E/24F/24N (independent expenditures FOR/AGAINST — never hit candidate receipts). `SUM(TRANSACTION_AMT)` = no candidate-totals field. **Fix:** referee ONLY the 24K subset (`MEMO_CD<>'X'`, netted, cycle-by-date) against OpenFEC `other_political_committee_contributions + political_party_committee_contributions`, modeled on `smoke_itcont.py`. Build 24A/24E into a SEPARATE for/against mart cross-checked against already-landed `FED_FEC_INDEPENDENT_EXPENDITURES`, never against candidate totals. Run the fanout guard from `build_indiv_donations.py` (committee→>1 member = exclude, not sum).
- **Money spine is CURRENT members WITH an FEC id — NOT "the whole spine."** `politics__member_fec_id.sql:18` drops members with empty `fec_ids`; `politics__member_money_raised.sql:15` + `build_indiv_donations.py:86-88` hard-filter `legislator_set='current'`. Structurally excludes everyone pre-1979 and all former members. **Fix:** state the real population up front. Decide explicitly whether to keep `current`-only. Print a coverage metric: distinct bioguides total vs. with ≥1 fec_id vs. in the money mart.
- **"refresh in 0.5-1d" is mis-sized** — its target mart `politics__member_pac_money` is UNBUILT and depends on the money spine + fanout guard. **Fix:** split "refresh landing (independent, ~0.5d)" from "build the mart (depends on spine)."

### House PTR trades (`fed_house_clerk_ptr`)
- **OCR premise is largely WRONG.** Sampled 2025 DocIDs (20032062/20033337/20026590/20030630/20029138) are ALL text-PDFs (embedded Georgia fonts, `/ProcSet [/PDF /Text]`, one signature image each) — extract with pdfplumber alone. **But the entire PDF stack is absent:** no `tesseract`, no pdfplumber/pytesseract anywhere in repo or requirements. Greenfield, not a "fallback." **Fix:** verify scan-vs-text ratio on 100+ 2025 PTRs; if >90% text (likely), drop Tesseract from v1 → build shrinks to ~4-5d. Add real setup cost: `brew install tesseract` + pin `pdfplumber pytesseract` in requirements.
- **"ZERO null bioguide" gate incentivizes amputation** — contradicts the plan's own quarantine doctrine (line 411) and the detective-trust doctrine. **Fix:** matched rows carry `match_method`+`confidence`; unmatched → quarantine table; report match rate as a metric, never a pass/fail on completeness. Add EXTERNAL parse reconciliation: for 3-5 named members, reconcile disclosed transaction COUNT + count-by-band against the House Clerk cover count (or Capitol Trades/Unusual Whales as referee-only). Gate publish on that reconcile.
- **License: NOT commercial-safe.** `5 U.S.C. 13107(c)(1)` carve-out attaches to the USE (news-media dissemination to public), not the person. Ripple's ceiling is a commercial data product → PTR-derived marts in any paid Library tier = "any commercial purpose," unlawful. **Fix:** tag landing + marts `REFERENCE_ONLY / journalism-output-only`; any commercial release gate must EXCLUDE `fed_house_clerk_ptr`-derived tables.

### DIME CFscores (`xc_dime_cfscores`)
- **"FEC_CAND_ID / steel" badge is a half-empty key in disguise.** Real FEC `^[HSP]#` on only ~9.5% of the 479,502 recipient rows; ~85-90% are state/local/PAC synthetic IDs; ICPSR ~0% real (synthetic). **Fix:** re-badge as "STEEL on ~10% of rows, WALL on ~85%." Regex-gate to real `^[HSP]#`/`^C\d{8}` before any member join; NEVER join synthetic-ICPSR to Voteview; store `match_method`+`confidence`; report realized join count (target >2,000 members). **Defer the contributors file** (850M+ rows, tens of GB) or re-cost at 4-6d — it is NOT a "+1-2d" footnote.

### LDA lobbying (`fed_senate_lda` canonical)
- **`windowed.py` is pre-solved LOGIC, not a pre-solved loader.** `loadkit/windowed.py:35-78` is real and correct but does nothing until the not-yet-written loader calls `count_fn` per leaf window + `assert_window_complete`. **Path drift: it's at repo-root `loadkit/`, NOT `politics/loadkit/`** — a clone importing `from politics.loadkit import windowed` ImportErrors. **Fix:** import from `loadkit`. Also `reconcile()` uses `pages*page_size >= envelope` — proves you PAGED far enough, not that you RECEIVED every record. Add `records_received == envelope_count` assertion. Surface `windowed.overflow` (unsplittable >2500 windows) as a LOGGED known truncation, never silent.
- **"≥1 honoree matches" is a dead-matcher floor, proves no precision.** **Fix:** hand-label ~30-50 honoree strings, report matcher precision/recall, quarantine unmatched, gate the honoree→member bridge on a stated precision threshold + human sign-off. Bind or drop "LD-203 amounts reconcile" (LDA publishes no per-member honoree total).

### Cross-cutting: referee escape hatches
- Cloned loaders silently inherit BYPASSES: `build_indiv_donations.py:305` has `--skip-referee`; `smoke_money.py:108` + `smoke_itcont.py:184-189` treat OpenFEC unavailability (DEMO_KEY 429) as a tolerated SKIP → a run goes green having NEVER hit external truth. **Fix:** for any mart publishing a person-level dollar/count headline, require a real `OPENFEC_API_KEY`; make "referee attempted >0 AND 0 real mismatches" the pass condition — an ALL-SKIPPED run must FAIL. Forbid `--skip-referee` in the mart-build path.

---

## Corrected load order

**Step 0 (BLOCKING, ~2.5d):** B1 fleet path-fix (templates first) → B2 resolve creds, prove `current_account()=ONEAFDA` → B3 mart-path decision (recommend in-loader DDL) → B4 add completeness referee to `land()` → B5 reconcile duplicate SIDs. **Prove one politics loader lands end-to-end before proceeding.**

| # | Load | Reuse/New | Infra it needs | Effort | Notes |
|---|------|-----------|----------------|--------|-------|
| 1 | **`fed_congress_committee_membership` refresh** | REUSE | none | **0.25d** | Was "T1 #1 new build." Path-fix + re-run. Optionally extend with `committees-historical.yaml`. |
| 2 | **`fed_scdb` — verify landed + build 49-justice SCOTUS crosswalk** | REUSE | none | 0.5d | JCS-SCOTUS leg is INDEPENDENT (closed 49-justice set) — needs NO FJC, NO moat. Decouple from #7. |
| 3 | **`fed_fec_committee_to_candidate` — refresh landing** | REFRESH | OPENFEC_API_KEY | 0.5d | Landing only. Mart is a separate item (#11). |
| 4 | **`fed_congress_press` / `fed_congresstweets`** | NEW | none (bioguide steel exists) | 1d each | congresstweets: assert all ~2210 date files fetched (none 404-skipped); 2-hop resolve with `match_method` per row; spot-check ~25 tweets vs handle-at-date (user_id recycling). |
| 5 | **`fed_voteview_*` votes backfill** | REUSE (3 ids) | **chunked-land helper (700MB stream)** | **3-4d** | Switch votes leg to `HSall_votes.csv`, chunked stage-append (land() can't stream a 700MB→2-4GB frame tripled to 6-12GB peak on 29GB-free disk). Re-run `smoke_votes.py` post-swap; key history on ICPSR. |
| 6 | **`fed_congress_govinfo_bills` full text + `fed_govinfo_plaw`** | REUSE id / NEW sibling | none | 2d | Land to `FED_CONGRESS_GOVINFO_BILLS`; metadata via UPDATE not new dict. |
| 7 | **`fed_fjc_judges` → `fed_courtlistener`** | NEW | none | 2-3d | FJC first (CourtListener `fjc_id` crosswalks INTO FJC nid). |
| 8 | **`fed_irs_bmf` refresh (Phase 1)** | REUSE | none | 0.25d | Was "T2 #5 new." Already landed — just path-fix + re-run. |
| 9 | **[moat] name→bioguide + name→EIN crosswalks** | connect/ (exists) | none | 2-3d | Gates ONLY member-join marts, NOT landing. `bridge.py/match.py/resolve.py/fingerprint.py` exist. |
| 10 | **JCS-CoA leg (name+circuit → FJC nid)** | NEW | none (needs #7) | 1d | Only piece of JCS that waits on FJC. |
| 11 | **`fed_senate_lda` (LDA) — land + mart** | RECONCILE | none | 3-4d | Import from `loadkit` (repo root). Wire `count_fn`+`assert_window_complete`+`records_received==envelope`. Honoree precision gate. |
| 12 | **`politics__member_pac_money` mart** | NEW | OPENFEC_API_KEY | 1.5d | 24K-only referee vs OpenFEC; fanout guard; separate for/against mart. |
| 13 | **`fed_house_clerk_ptr` (PTR) — land + parse** | RENAME | **pdfplumber (pin); tesseract IF needed** | **4-5d** (7d if OCR truly needed) | Land Stage A/B in parallel with moat (DocID self-sufficient). REFERENCE_ONLY license tag. Quarantine unmatched, external count reconcile. |
| 14 | **`fed_irs_990_efile` (Phase 2 XML)** | NEW | **lxml (exists); IRSx spike first** | +4-6d | Spike `pip install irsx` on 3.9 FIRST (0.5d) — Py2-era, likely won't import; fall back to hand-rolled lxml XPath (schema-versioned by tax year = the real work). |
| 15 | **`st_openstates` Phase 1 (people)** | REUSE | none | 1.5d | People CSVs, direct S3, public-domain. Registry UPDATE. |
| 16 | **`xc_dime_cfscores` recipients-only** | NEW | chunked-land helper | 2-3d | Recipients only (479,502 rows, assert `==`). DEFER contributors. Regex-gate real IDs. |
| 17 | **`st_openstates` Phase 2 (bills)** | REUSE | **Postgres + ~50GB disk (NEITHER exists)** | **5-7d** | 10.63GB dump, restores to 30-50GB on a 29GB-free/87%-full disk. Provision external disk + Postgres FIRST — OR skip pg_restore, pull per-table CSV/JSONL exports and `land()` direct. |

---

## Effort re-costing

| Item | Old | New | Why |
|------|-----|-----|-----|
| T1 #1 Committee membership | 1-1.5d | **0.25d** | Duplicate — existing loader, just path-fix + re-run. |
| T2 #5 IRS BMF (Phase 1) | part of 4-6d | **0.25d** | Duplicate `fed_irs_bmf` — already landed. |
| Voteview HSall | 1.5-2.5d | **3-4d** | 700MB votes file needs a chunked-land helper; `land()` triple-copies the whole frame (6-12GB peak). |
| IRS 990 XML (Phase 2) | +2-3d | **+4-6d** | IRSx is Py2/3.4-3.6, likely won't import on 3.9; download path dead (AWS Dec-2024). Schema-versioned XPath is the real work. |
| House PTR | 6-7d | **4-5d** (7d if OCR) | Most 2025 filings are text-PDFs, not scans — drop Tesseract from v1. But PDF stack is greenfield (add setup). |
| DIME cfscores | 2-3d (+1-2 contributors) | **2-3d recipients-only; contributors = 4-6d SEPARATE** | Contributors = 850M+ rows / tens of GB, not a "+1-2d" footnote. Defer. |
| Open States Phase 2 | 3-4d | **5-7d + provisioning** | No Postgres, no pg_restore, 29GB free vs 10.6GB dump → 30-50GB restore. |
| **Step 0 (new)** | 0 (per-file footnotes) | **~2.5d** | Fleet path-fix + cred resolution + land() referee + SID reconcile. Systemic, precedes everything. |
| Environment prereq | assumed present | **~1d** | Pinned venv on Python 3.11+ (system Python 3.9.6 + LibreSSL 2.8.3 is fragile for GB HTTPS streams); pre-flight `tesseract`/`pg_restore`. |

---

## Risk register (accepted)

| Risk | Severity | Proceed with this guardrail |
|------|----------|-----------------------------|
| congresstweets 2-hop resolution (user_id recycles over 6yr) | MED | Quarantine unmatched user_ids; report hop-1 (tweet→account) + hop-2 (account→bioguide) rates SEPARATELY; spot-check ~25 tweets vs handle-at-date; store `match_method`. |
| Snapshot-replace on append-only sources (527/pas2/committee amendments overwrite history) | MED | B4 regression floor: refuse overwrite when new count < prior_success × 0.98 (log `partial`, keep prior table). Consider append+dedup for 527/pas2. |
| DIME license (ODC-BY vs "academic use only" — both on the same page) | LOW | Land/analyze internal freely. Gate any COMMERCIAL DIME-derived publication on written confirmation from bonica@stanford.edu; record reply (or absence) in registry NOTES. Blocking-for-commercial, not optional. |
| Shor-McCarty NC successor (`SGOQ7G`=CC BY-NC-SA) | MED | Registry MUST pin exact CC0 DOI (`NWSYOS`) + hard-flag the NC successor. Pre-flight: query SOURCE_REGISTRY for the SID first; if it exists, route the flag via authorized UPDATE, not the append-only insert. |
| ProPublica reference ban | HIGH→accepted | NEVER land or reference in ANY artifact including registry NOTES. Pre-flight existence check as above. |
| st_openstates license path unenforceable via append-only script | MED | Ship scoped UPDATE (preview→`--apply`): LICENSE = "Public-domain (data.openstates.org direct) — DO NOT source via OpenSanctions mirror (CC BY-NC)"; repoint URL. |
| Committee/PTR/LDA member joins are fuzzy (name-match) | MED | Detective-trust doctrine: `match_method`+`confidence` on every row; quarantine unmatched; report match rate as a build metric; NO person-level published claim without reproducible SQL + hard-ID + human sign-off. Spot-check gavel-holders (Chair/Ranking) explicitly. |

---

## My take — what to actually do first

**Do Step 0. All of it. In this order — it's ~2.5d and everything else is dead until it's done:**
1. **B1** — fleet path-fix, starting with `build_skeleton.py` + the 2 registry writers (templates first, or every new loader inherits the disease). Copy the pattern from `scripts/irs_bmf_load.py:26-31` verbatim.
2. **B2** — kill or repoint `connections.toml`. Prove `current_account()=ONEAFDA`.
3. **B3** — decide marts = in-loader DDL (recommended) and skip dbt for this batch.
4. **B4** — add `expect_rows`/`min_rows` + never-shrink floor to `land()`. This one helper closes the SAM-class silent-truncation hole across all 18 loads.
5. **B5** — reconcile the 7 duplicate/stale SIDs; write the scoped UPDATE scripts (preview mode).

**Then the first 3 loads that are genuinely safe on existing steel — no new infra, no fuzzy joins, fast wins:**
- **`fed_congress_committee_membership` refresh** (~0.25d) — pure path-fix + re-run. Real gavel dimension, STEEL bioguide, already registered.
- **`fed_irs_bmf` refresh** (~0.25d) — same story, already landed, closes the "no nonprofit source" gap for free.
- **`fed_scdb` verify + 49-justice SCOTUS crosswalk** (~0.5d) — SCDB is already landed+modeled; the crosswalk is 49 hand rows, needs neither FJC nor the moat.

That's **~1 day of loads that ship real capability** and prove the fixed rig end-to-end before you touch anything expensive.

**Defer hard until infra exists:** Open States Phase 2 (no Postgres, disk won't hold the 10.6GB dump — provision external disk OR skip pg_restore for per-table exports first), IRS 990 XML (spike IRSx before you trust the +4-6d), DIME contributors (850M rows — recipients-only is where the member CFscores live anyway). **Move House PTR's OCR-heavy ingest EARLIER than its member marts** — DocID is a self-sufficient landing key, so land + parse in parallel with the moat; only gate the member-facing trades mart on the crosswalk + external count reconcile.

**Bottom line: the moat thesis is right and the sources are real. The plan just never met this mac. Fix Step 0, dedup the 7 collisions, and the first day of builds is safe steel.**