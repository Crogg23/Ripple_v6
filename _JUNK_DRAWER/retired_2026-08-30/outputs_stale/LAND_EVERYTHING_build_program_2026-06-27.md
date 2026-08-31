# THE DE-SILO BACKFILL — GATED BUILD PROGRAM
*Land + Wire + Catalog. ~50 sources, 6 waves, crosswalks first. No detectors, no leads.*

---

## 1. THE PLAN IN ONE BREATH

We're turning ~50 verified free/bulk sources into a hardened, idempotent, unattended backfill that lands them all-TEXT, **wires them into your existing 720-node graph crosswalks-first so three dead hard keys (EIN, LEI, CIK) finally light up across money/corporate/maritime instead of healthcare-only**, and registers each one into CATALOG with *measured* join keys and an honest lifecycle. End state: **~870 graph nodes, ~28–32k edges, STEEL/BRIDGE connectivity spread off the healthcare island for the first time, every source catalogued with real facets or honestly flagged `NEEDS_TOPIC`.** It runs as one detached command per wave, survives a credit-suspend or a 403, and converges to the same tables on re-run. Cost: **~30 credits, ~one bounded sprint week** of mostly-unattended runs you approve at each GO.

---

## 2. ARCHITECTURE — the reliable landing machine

**One spine, four front-ends, one tail.** Everything funnels through hardened primitives that already exist in `ingest.py`; the new code is the *seam* that forces every loader through the same gates.

```
4 FRONT-ENDS                 ONE LANDING SPINE                  TAIL
bulk CSV/ZIP   ─┐         (landing.py wraps ingest.py)
paginated API  ─┤   →   hash(SOURCE bytes) → SHA-skip   →   write_pandas (default)
s3/SPARQL      ─┤        → _stringify (+collision guard)      or fastload COPY (opt-in)
portal Socrata ─┘        → DENSITY GATE (every path)
                         → one INGEST_RUNS row (atomic w/ registry MERGE)
                         → facet-enriched, vocab-checked catalog upsert
```

**The four access archetypes:**

| Archetype | Loader (reuse) | New code |
|---|---|---|
| Bulk CSV / ZIP (chunked) | `bridge_fuel_load.py` + spec dicts | spec rows + **multi-member ZIP fan-out** (real, see below) |
| Paginated REST + token | `scripts/paginated_load.py` (generalize SAM's loop) | new harness, checkpoint sidecar |
| S3 bulk / SPARQL | new thin front-ends → spine tail | small |
| Socrata / ArcGIS | `connect/portal_loader.py` | none (point at dataset IDs) |

**Hardening baked in (the must-fixes that change the machine, not just the specs):**

- **Density gate is NOT currently wired into `bridge_fuel_load` — it must be ADDED, not "reused."** Confirmed: `_load_chunked` line 383 logs `success` with zero density check. *This is build step 0a, every spec depends on it.*
- **Chunked path = NOT atomic and NOT idempotent today.** Confirmed: no try/except around the chunk loop (partial table + no run row on crash → next run *skips* it as "already landed"); SHA-skip exists only in the non-chunked branch; resume keys on `_latest_success_sha is not None` so an `empty`-status prior run **appends onto garbage**. All three are blockers fixed before any giant runs.
- **SHA is over SOURCE bytes, pre-stamp** — never the stamped frame (the `_INGESTED_AT`/`_SOURCE_RUN_ID` stamps change every run and would defeat skip).
- **Column-collision disambiguator** (`order`+`Order` → same identifier) lives in `_stringify`, post-sanitization, the single seam.
- **fastload (PUT-many→single COPY) ships OFF** behind `RIPPLE_FASTLOAD=1`; `write_pandas` stays the proven default for the whole first sprint. fastload only gets turned on per-giant after a CSV round-trip test passes (quotes, embedded newlines, empty strings) + `MATCH_BY_COLUMN_NAME` + a post-COPY `COUNT(*)` assert. **Don't gate the sprint on it.**

---

## 3. THE WAVES — ordered, gated execution

Rule of order: **crosswalks before spines · no-new-key before new-key · deterministic before scrape · giants LAST.** Wire once per wave (whole-graph self-join), never per-source. Each GO is yours.

| # | Wave | What loads | New keys (gate) | Wire after | GO gate (the spend/human decision) | Est |
|---|---|---|---|---|---|---|
| **0** | Infra + Geo | DDL (ingest_runs, checkpoints, monitor, writer role); HUD ZIP↔FIPS; Step-K **batch-1 keys** | ISIN BIC BIOGUIDE RSSD ORCID CUSIP NTEE-as-category (Wave-K below) | — | **GO-0: raise RIPPLE_BUDGET 15→60; register API keys; set `RIPPLE_CONTACT_UA`; flip `SNOWFLAKE_ROLE`** | ~2 cr |
| **1** | Tier-A Crosswalks | IRS EO BMF, SEC SUB, company_tickers, GLEIF L1+RR+ISIN+BIC, FFIEC NPW, HMDA panel 2018-23, congress-legislators, Wikidata xwalk | declared-crosswalk specs (ship CIK↔EIN, LEI↔EIN first — no new key) | `wire --wave A` | **GO-1a: catalog `--apply` · GO-1b: confirm EIN/LEI/CIK lit before B** | ~3 cr |
| **2** | Tier-B spines (no new key) | SEC insiders/13F/Form D/FTD, SAM entity+exclusions, USASpending subawards, FEC bulk, LDA, FARA, IRS 990 index, FAPIIS, Open Payments (already speced) | CUSIP/CRD/FEC/TAIL gated in **Wave K batch-2** first | `wire --wave B1`, `B2`… | **GO-2: per-batch GO; SEC/FFIEC UA must be set** | ~10 cr |
| **3** | Beneficial-owner / sanctions / intl | OpenSanctions (targets.simple.csv), ICIJ, UK PSC, OpenSanctions maritime, OpenCorporates (free sample) | IMO_COMPANY_NUMBER, UK_COMPANY_NUMBER, OPENCORPORATES_ID | `wire --wave C` | **GO-3: LICENSE_TERMS correct per source (CC-BY-NC, ODbL, OGL) before catalog `--apply`** | ~4 cr |
| **4** | Enforcement / geo-soft / property | NYC ACRIS (portal), PLUTO, PPP, FSA, labordata SQLite, OLMS, LEIE, CFTC/FTC | PARCEL **as PARCEL@FIPS composite only** | `wire --wave D` | **GO-4: NAME@ZIP corroboration rule live before discover** | ~4 cr |
| **5** | Heavy parse lifts | 990-XML, OpenSanctions FtM edges, BODS | — | separate | **Deferred — own sprint, not this backfill** | — |
| **6** | Tier-C rulings | Equasis, GJF, PACER, ATTOM, OpenCorporates full | — | — | **Blocked until you rule. Driver hard-asserts tier='C' excluded from default set** | — |

**Discover runs a bounded number of times (3 budgeted), never per-source** — it's the credit hog, not the loads.

---

## 4. STEP K — the new-key table (safe-first, gated)

Every key needs **four** edits not three: `KEY_TOKENS` (tagger) + `NORM_RULES` (keys.py) + `PAIR_RULES` (tagger) + **`KEY_DOMAIN` (discover.py)** — the last one was missed and without it a new key gets `chance_free=0.9` with **no collision guard**. Two code prereqs before any token: add the **`alnum_upper`** norm mode (referenced but doesn't exist → KeyError today), and **fix `detect_key` to return strongest-tier**, not first-insertion-order match (today a new STEEL key appended at the end loses to an earlier GEO key on an overlapping column).

| Batch | Keys | norm rule | KEY_DOMAIN | FP-risk | dry-run gate |
|---|---|---|---|---|---|
| **K1** safe, coined, batch together | CUSIP `(fixed,9)`, ISIN `(fixed,12)`, ORCID `(fixed,16)`, RSSD `(pad,10)`, BIOGUIDE `(alnum_upper)` | per cell | 10⁴–10⁶ | LOW | one fingerprint+discover, keydiff each |
| **K2** pair-guarded | FEC_CMTE_ID/FEC_CAND_ID (require `*_id` or pair), ROR, FRN `(fixed,10)` not pad | — | 10⁵–10⁷ | LOW-MED | keydiff, audit bare hits |
| **K3** needs a ruling | **NDC** (10-vs-11-digit → dedicated segment-aware normalizer, NOT `code`; a 0-overlap keydiff = FAILURE to wire, not a pass), **NTEE** (category → **skip value-join entirely**, faceting only), FRS_ID | special | — | per-key, alone |
| **K4** false-positive-prone, one at a time, full eyeball | ICAO24 `(fixed,6)`, TAIL_NUMBER (`n_number` only, never bare tail/reg), ORI (`ori9` only, never bare ori), **PARCEL → PARCEL@FIPS composite only, never raw** (same APN repeats across 3000 counties = flood) | `alnum_upper` | — | one at a time, isolated diff |

**Gate mechanics (`connect/keydiff.py`, new, offline, no Snowflake cost):** freeze `connect_graph.BASELINE.json`, add ONE key, fingerprint→discover, set-diff. Classify edges **three ways** (the must-fix): `on_key` / `derived_ok` (key *contains* NEWKEY as component — `~`, `@`, bridge `hop`/`via` chains are legitimate) / `suspicious` (everything else = real regression, exit 1). Read `discover.GRAPH_OUT` not `OUT` (that's the fingerprints file). **Re-freeze the baseline immediately before each key's run** — concurrent landing pollutes a stale baseline. Run `discover --no-spatial --no-bridge` for the pure value-key check so 16 gate runs don't trip the budget.

**Never broaden the value-sniffing path. Column-name-anchored only.**

---

## 5. WIRE & CATALOG

**Wire = wave cadence, incrementally cached.** New `connect/wire_wave.py` runs `fingerprint.run_incremental → discover.run(fp, full) → spine.run` once per wave.

- **Cache key = the loader's stable manifest SHA from `INGEST_RUNS.SHA256`** (read it from the metadata table) — **NOT** `MAX(_SRC_SHA256)||COUNT(*)`, which is unstable for chunked giants (hundreds of distinct per-chunk SHAs; MAX picks an arbitrary unstable one → cache never hits or silently collides). This is free (no giant scan).
- **Persistent versioned `KEYSET_CACHE` + `SPATIAL_CACHE`** (use `store.cfqn()` — CONNECT is a reserved word): the giants' DISTINCT extraction happens ONCE; only their participation in the recurring self-join repeats. Version-stamp written LAST, in-transaction, all-or-nothing (a budget-suspend mid-extract must not leave poison rows that read as valid). Orphan-reconcile dropped tables each run. **Preserve the NAME@ZIP composite branch** in the rewrite or you silently lose the CORROBORATED tier.
- **Pre-join fan-out cap + degenerate-value guard on the direct value self-join** (port bridge.py's `_guard`): EIN/LEI activation is exactly what introduces a junk umbrella ID shared across 100k rows → Cartesian blowup *before* the confidence gate trims. Must land in the same change as the activation.
- **Crosswalk bridges:** SEC SUB (CIK+EIN), GLEIF/HMDA (LEI+EIN), FFIEC (LEI) auto-qualify under bridge.py's both-HARD gate **with zero code change** — ship these first. Declared multi-ID crosswalks (`crosswalk_specs.py`) skip the both-HARD gate but keep fan-out/degenerate/dedup rails, are **`enabled`-flagged and skip+log (never crash) if their key lacks a NORM_RULES entry**, and must **earn** `authoritative=True` by passing a per-spec population + fan-out validation. **Wikidata is almost certainly tall (one id-property/row), not wide** — needs a pivot-to-(entity,idA,idB) step before it's a usable crosswalk.

**Catalog = atomic, facet-rich, honest:**

- New `register_load.register_landed()` wraps `_log_run` + registry MERGE in **one explicit transaction with `conn.autocommit(False)` on the same cursor** (autocommit is ON by default → naive BEGIN/COMMIT is illusory). No DDL between BEGIN and COMMIT.
- Deterministic `facets.py` (no LLM — `ANTHROPIC_API_KEY` is absent). **`detect_join_keys` calls the existing `tag_columns(cols)`** — do NOT reimplement the matcher (KEY_TOKENS values are `(tier, set)` tuples; naive iteration crashes, and you'd diverge from what the wire step actually fingerprints).
- **`JOIN_KEY_TIER_PROVISIONAL=FALSE` gated on DENSITY, not column-name presence** — an all-blank EIN column must not claim STEEL (the fjc_idb husk lie at the key layer).
- Vocab check uses the **real facet names** (`DOMAIN`, not `DOMAIN_PRIMARY`; drop `JOIN_KEY_TIER` from the vocab check — tiers are a code constant). Domain rules: **multi-match → UNCLASSIFIED + NEEDS_TOPIC**, never confident-wrong first-match-wins. Vocab violation on domain → warn+downgrade to review queue, never halt the sprint.
- `_build_row` must actually **read JOIN_KEYS_STD/tier/NEEDS_TOPIC from `enrichment`** (today it reads `config` and hardcodes `NEEDS_TOPIC=False`) — and exclude the JOIN_KEY_* trio from `COALESCE_ON_MERGE` so a measured upgrade isn't frozen by a stale provisional value.
- All catalog mutations beyond the loader's own self-upsert ship **preview/--apply/rollback-snapshotted** (classifier blocks agent writes).

**Islands lit + lift:** Wave 1 activates the **EIN spine** (27 phantom-EIN tables get real values: +150–300 edges), welds the **CIK island** (1 edge) to EIN via SEC SUB, and brings **LEI** its first-ever data via GLEIF/FFIEC/HMDA. Wave 3 lights **maritime** (AIS↔OFAC↔Wikidata on IMO). Headline isn't the count — it's **hard-key connectivity spreading off healthcare for the first time.**

---

## 6. OPS ENVELOPE

- **Budget sprint = 60 credits** (2× the ~30-cr estimate). `scripts/budget_sprint.py --apply` (step 0) / `--restore` (last step). **Use `ALTER RESOURCE MONITOR` not `CREATE OR REPLACE`** (replace detaches the warehouse binding → uncapped sprint); read+re-assert the binding, verify via SHOW, treat unbound as fatal. **SUSPEND@75%** (not 90 — a long discover/chunk statement overshoots past finish), SUSPEND_IMMEDIATE@100% backstop. Poll budget *between* sources, stop clean at threshold, giants ordered LAST.
- **Secrets checklist (step 0):** `RIPPLE_CONTACT_UA` (name+email — SEC/FFIEC 403 without it; **one shared `_fetch.ripple_headers(contact_required=True)`**, grep-gate that no sec.gov/ffiec.gov fetch bypasses it), `SAM_API_KEY`, `CENSUS_API_KEY`, `COURTLISTENER_TOKEN`, `SOCRATA_APP_TOKEN`, `LDA.gov` token. `pip install tenacity` (missing; httpx/boto3 present). PAT check = **live connect smoke-test** (authoritative), age is a warning only. `chmod 600 .env`.
- **Least-priv role:** `LIBRARY_WRITER` via `SNOWFLAKE_ROLE` in `.env`. **Must OWN landing tables** (write_pandas overwrite = DROP+RENAME, needs OWNERSHIP not CREATE) → `GRANT OWNERSHIP ON ALL + FUTURE TABLES IN LANDING`. Grant CONNECT schema usage+CREATE for wire scratch, or run the gated wire step as ACCOUNTADMIN. **Dry-run every loader + the wire step as LIBRARY_WRITER before flipping `.env`.**
- **Infra-as-DDL:** `infra/` tree (`GET_DDL`-captured, human-reviewed into `_captured/` before promotion — never auto-bless drift). Closes the DR hole on monitor + INGEST_RUNS + SOURCE_REGISTRY + CATALOG view.
- **Abort/rollback runbook:** non-chunked loads are safe to kill (snapshot-replace idempotent). **Chunked loads are NOT atomic** — a killed chunked giant leaves a partial table + no success row; *before trusting any post-abort state, find sources with STARTED_AT but no success/empty ENDED_AT and force-re-run fresh, and do NOT run discover until every chunked source has a clean success row.* `--restore` caps spend instantly. `drop_scratch.py` only in teardown.

---

## 7. STRESS-TEST LEDGER — top must-fixes, now handled

| # | Finding | How the plan handles it |
|---|---|---|
| 1 | **Density gate not actually wired** into bridge_fuel (claimed "reused") | **Build step 0a:** add `assess_density` before `_log_run` success in both bridge paths; demote to `empty`, skip register |
| 2 | **Chunked load partial-corrupt + skip-on-rerun** (no try/except, no run row → next run skips) | try/except logs `failed` + drops partial table; `_already_landed` requires a **success run row**, not table existence |
| 3 | **SHA-skip dead on every chunked giant** (only non-chunked branch has it) | Pre-land file-level SHA short-circuit before first overwrite, for chunked too |
| 4 | **Chunked resume appends onto `empty` tables** (`had_success` keys on success-sha) | Resume off the explicit STATUS state machine: `success`→replace, `failed+rows`→append, `empty`→full replace |
| 5 | **Round-number rows silently demoted to `sampled`** by the trust-gate view | Stop classifying `sampled` off magic row counts; key it off an explicit `capped` flag in the message/manifest |
| 6 | **New sources land facet-blind** (UNCLASSIFIED, no keys) | `facets.py` via `tag_columns`; measured JOIN_KEYS_STD; multi-match→NEEDS_TOPIC |
| 7 | **Multi-table ZIP doesn't exist** (SEC 13F/insiders, ICIJ, GLEIF RR drop all but largest member) | Real loader feature: spec `members=[{pattern,sid_suffix,key_cols}]`, land each as `<SID>_<SUFFIX>` |
| 8 | **Wire cache key wrong for giants** (`MAX(_SRC_SHA256)` unstable) | Use `INGEST_RUNS.SHA256` manifest hash from metadata; zero giant scan |
| 9 | **Dense-key self-join blowup** on EIN/LEI activation | Pre-join fan-out cap + degenerate-value guard ported from bridge.py, same change as activation |
| 10 | **detect_key returns first-match not strongest-tier**; `alnum_upper` mode missing; `KEY_DOMAIN` forgotten | All three fixed before any token; keydiff 3-way classifier (derived_ok ≠ suspicious) |
| 11 | **`CREATE OR REPLACE` monitor detaches warehouse → uncapped** | `ALTER` not replace; read+re-assert+verify binding; unbound = fatal |
| 12 | **LIBRARY_WRITER can't snapshot-replace existing tables** (DROP needs OWNERSHIP) + atomicity illusory under autocommit | `GRANT OWNERSHIP ALL+FUTURE`; `autocommit(False)` same-cursor txn; dry-run before flip |

---

## 8. THE FIRST GO

**The smallest safe wave that proves the whole pipeline end-to-end: Wave 0 infra + one tiny Tier-A crosswalk (IRS EO BMF) + wire + catalog.** EO BMF is ~2M rows of clean EIN+NAME — it activates the dead EIN spine on its own, so you see land→wire→catalog *and* a real island light up in one shot, for ~1 credit.

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CHECKPOINT 0 — INFRA + FIRST CROSSWALK   [Wave 0+1a of 6]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What lands:  xc_irs_eo_bmf (EIN+NAME+NTEE, ~2M rows)
Proves:      density gate · atomic register · facet enrichment · wire cache · EIN activation
Cost:        ~1 credit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Exact commands — BUILT + TESTED 2026-06-27 (these scripts/specs now exist; 58 offline tests green).
Run in order; stop if any step fails its check:

```bash
# 0. preflight + raise the budget. (--apply is yours: ACCOUNTADMIN.)
#    LIVE STATE 2026-06-27: RIPPLE_BUDGET used 13.29 / 15 -> only 1.71 credits left.
#    The raise is REQUIRED before the load, not optional, or it'll suspend mid-stream.
python scripts/secrets_check.py            # creds smoke-test; flags .env perms + missing keys
python scripts/budget_sprint.py            # PREVIEW: prints live used/quota + the exact DDL
python scripts/budget_sprint.py --apply    # ALTER monitor 15 -> 100cr (preserves binding). YOU run this.
chmod 600 library-onboarding/.env          # .env is currently 644 (group/world-readable)

# 1. land the EO BMF crosswalk through the hardened loader (preview first — reads 1 file for shape)
python scripts/bridge_fuel_load.py --spec xc_irs_eo_bmf           # PREVIEW (no --run)
python scripts/bridge_fuel_load.py --spec xc_irs_eo_bmf --run     # LAND: density gate + auto-register

# CHECK: one 'success' row with real rows (not 'empty')
#   SELECT status, row_count, message FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
#   WHERE source_id='xc_irs_eo_bmf' ORDER BY ended_at DESC LIMIT 1;

# 2. wire — freeze a baseline, then the EXISTING connect verbs (fingerprint -> discover).
#    discover.run() now calls validate_key_config() first (the Step-K guard).
cp outputs/connect_graph.json outputs/connect_graph.BASELINE.json
python -m connect fingerprint     # measures EIN/NAME/ZIP on the new table
python -m connect discover        # rebuilds edges -> the EIN spine lights up

# CHECK: EIN edges jump from ~0. discover prints "by tier: ... STEEL=N"; diff vs the baseline:
#   python -c "import json;b=json.load(open('outputs/connect_graph.BASELINE.json'));a=json.load(open('outputs/connect_graph.json'));print('edges',b['meta']['edges'],'->',a['meta']['edges'])"

# teardown only when the WHOLE sprint is done, not after this checkpoint:
# python scripts/budget_sprint.py --restore     # back to 15cr
```

Notes: catalog registration happens automatically inside `bridge_fuel_load` (`_register`) — no separate
catalog `--apply` for this first GO; the facet-rich catalog upsert is a deferred Wave-1 build. The
least-priv `LIBRARY_WRITER` role + `apply_infra.py` (infra-as-DDL, INGEST_CHECKPOINTS) are also deferred —
they harden the FULL multi-wave sprint, not this one-table proof (which is a single snapshot-replace CREATE).

**The one thing if you do nothing else:** `python scripts/budget_sprint.py --apply`. At 1.71 credits left,
the load suspends mid-stream without it — that's the only silent killer for this checkpoint.

→ **go / edit [feedback] / skip / abort**

---

Honest cost/time/what-needs-you: **~30 credits, sprint-week of mostly-unattended wave runs.** What genuinely needs you and can't be automated: the **budget raise** (ACCOUNTADMIN), the **API-key registrations** (SAM/Census/CourtListener/LDA — free but manual signups), the **Tier-C rulings** (Equasis/GJF/PACER — legal calls, not technical), and the **per-batch GO** before each wave spends.

**BUILD STATUS (2026-06-27, uncommitted on `main`):**
- ✅ DONE — the 7 code blockers (density gate wired both paths, chunked atomicity + drop-partial, skip-on-success-run, resume-not-onto-empty, `detect_key` strongest-tier, `alnum_upper` mode, `KEY_DOMAIN` guard); multi-file (`csv_multi` urls) loader; `xc_irs_eo_bmf` spec; `scripts/budget_sprint.py`; `scripts/secrets_check.py`. **58 offline tests green; adversarially reviewed (no blockers).**
- ⏭️ DEFERRED to next build (Wave-1 hardening, not needed for the EO BMF proof): `apply_infra.py` (LIBRARY_WRITER least-priv role + INGEST_CHECKPOINTS + infra-as-DDL/DR), the facet-rich catalog upsert, the rest of the Tier-A specs (SEC SUB, GLEIF, FFIEC, HMDA, congress, Wikidata), multi-member ZIP fan-out (SEC 13F/insiders, ICIJ), and incremental/cached wire.

Relevant paths: `/Users/chrisr./Documents/GitHub/Ripple_v6/library-onboarding/ingest.py` (spine primitives + the chunked-resume bug at line 381), `/Users/chrisr./Documents/GitHub/Ripple_v6/scripts/bridge_fuel_load.py` (density-not-wired at line 383), `/Users/chrisr./Documents/GitHub/Ripple_v6/connect/{keys.py,discover.py,bridge.py,fingerprint.py}`, `/Users/chrisr./Documents/GitHub/Ripple_v6/portal_recon/tag_portal_index.py` (KEY_TOKENS), `/Users/chrisr./Documents/GitHub/Ripple_v6/outputs/_scout_de_silo_raw_2026-06-27.json` (per-source reality).