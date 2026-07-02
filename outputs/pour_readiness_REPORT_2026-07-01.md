Confirmed: `ANTHROPIC_API_KEY=` blank, `ANTHROPIC_MODEL=` blank, `ONBOARD_AUTO_APPROVE=` blank, and tenacity/bs4/lxml all uninstalled (only anthropic present). The findings hold against live state. Report:

---

# POUR-READINESS REPORT — Ripple v6 onboarding
Audited: 2026-07-01 · Scope: can Chris say "go" and pour many sources unattended, resumably, without babysitting?

## 1. VERDICT

**NOT READY TO POUR.** The documented pour command `python onboard.py --batch` cannot land a single row today, and even once unblocked it lacks unattended resilience (any one bad source kills the whole batch).

**Single biggest risk:** the pour path is stacked with hard blockers that each individually zero it out — blank `ANTHROPIC_API_KEY`, blank `ANTHROPIC_MODEL`, missing Python deps, and no auto-approve — and behind them a batch loop that aborts the entire queue on the first unfixable source. It fails silently or stalls, not loudly.

---

## 2. BLOCKERS (must fix before 'go')

| # | Blocker | Owner | Exact fix |
|---|---------|-------|-----------|
| B1 | `ANTHROPIC_API_KEY=` blank → every source dies at RECON (findings 3,5,8,9,12) | **chris** | Set real key on `.env:10`. Must be in the file — `load_dotenv(override=True)` makes a blank line beat a shell export. |
| B2 | `ANTHROPIC_MODEL=` blank → `model=''` sent to API, 400 on every call even after key set (findings 6,10,13) | **chris + agent** | Chris: set `.env:13` `ANTHROPIC_MODEL=claude-sonnet-4-6` (confirm id valid) OR delete the line. Agent: coalesce in `config.py:52-54` → `default_factory=lambda: (os.getenv("ANTHROPIC_MODEL") or "").strip() or "claude-sonnet-4-6"`. |
| B3 | `tenacity`, `beautifulsoup4`, `lxml` not installed → `_real_call` ImportErrors on first LLM call (finding 14) | **chris** | `pip install -r library-onboarding/requirements.txt` into the interpreter that runs onboard.py (no venv active). Verify `python -c "import tenacity, bs4, lxml"`. |
| B4 | `ONBOARD_AUTO_APPROVE=` blank → `--batch` blocks on `input()` / aborts on EOF at checkpoint 1 (findings 2,8,11,15,32) | **chris + agent** | Chris: set `.env:60` `ONBOARD_AUTO_APPROVE=1`. Agent: add `--yes/--auto` flag to onboard.py that sets it, and fail-fast in `run_batch()` if `not auto_approve and not sys.stdin.isatty()`. |
| B5 | One unfixable source ABORTS the whole batch — auto-repair exhaustion returns `ABORT`, same token as foreman-abort → `run_batch` breaks the loop (findings 16,17,39) | **agent** | Add a `FAILED` sentinel in `checkpoint.py`; `_run_stage` returns `FAILED` (not `ABORT`) on auto-repair exhaustion; `_record` maps `FAILED→"failed"`; `run_batch` **continues** on `"failed"`, only breaks on `"aborted"` (real Ctrl-C). Also wrap `onboard_source(...)` in try/except in all 3 loops (onboard.py:246, registry_batch.py:88, live_batch.py:100). |
| B6 | Null cells in numeric columns land as literal `"nan"` — corrupts data AND defeats the density gate (all-NaN numeric frame scores 100% populated, FJC_IDB-class junk rides in as success) (findings 4,21) | **agent** | Fix `_stringify` (ingest.py:693): null-aware cell coerce — `'' if v is None or (isinstance(v,float) and v!=v) else (str(int(v)) if isinstance(v,float) and v.is_integer() else str(v))`. Also harden `_is_blank` to treat `nan/nat/none/<na>` as blank. This also fixes integer join keys landing as `'1.0'` (FIPS/EIN/CIK corruption). Add regression tests. |
| B7 | Checkpoint banner/prompt crash the pour under redirected stdout (Windows cp1252 can't encode `━`/`→`/`…`); crash is outside `_run_stage` try/except → kills batch at first checkpoint (finding 1) | **agent** | Top of onboard.py/live_batch.py/registry_batch.py `main()`: `for s in (sys.stdout,sys.stderr): try: s.reconfigure(encoding='utf-8',errors='replace') except: pass`. Better: build the `Console(file=sys.stdout, legacy_windows=False)` in checkpoint.py. Optionally swap glyphs for ASCII. |

**B1–B4 are launch prerequisites (nothing pours without them). B5–B7 are unattended-resilience blockers (the pour starts but silently dies or corrupts partway).**

---

## 3. GREEN-LIGHT CHECKLIST (all must be true before 'go')

- [ ] `.env:10` `ANTHROPIC_API_KEY` = real key (verify: `python -c "from config import settings; settings.require('anthropic_api_key'); print(settings.anthropic_model)"` prints, doesn't raise) — **B1/B2**
- [ ] `.env:13` `ANTHROPIC_MODEL` = valid id (not blank) — **B2**
- [ ] `.env:60` `ONBOARD_AUTO_APPROVE=1` (verify: `python -c "import config; print(config.settings.auto_approve)"` → `True`) — **B4**
- [ ] `python -c "import tenacity, bs4, lxml"` succeeds — **B3**
- [ ] Batch continues past a failing source (B5 fix landed) — smoke via `ONBOARD_FAKE_LLM` batch with one raising stage
- [ ] Redirected-stdout smoke passes: `python -c "import checkpoint as cp; cp.banner(1,(1,5))" > log` doesn't raise — **B7**
- [ ] `_stringify` regression tests pass: NaN→`''`, int-with-null→`'1'` not `'1.0'`, all-NaN numeric frame flagged empty — **B6**
- [ ] Data-source API keys for in-scope sources present in `.env` (FRED, FEC, EIA, CENSUS, BLS, SAM, PROPUBLICA as needed) — finding 30
- [ ] `RIPPLE_BUDGET` quota raised well above pour cost (≥120; ~24cr headroom today) AND `NOTIFY_USERS=(CROGG23)` — findings 24,29,31,37
- [ ] `SNOWFLAKE_PAT` won't expire mid-pour (exp 2026-09-20; rotate if pour runs long) — finding 49
- [ ] Statement timeout clamped in `snow.connect()` (`ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS=3600`, `ABORT_DETACHED_QUERY=TRUE`) — finding 26
- [ ] `sources_queue.py` entries pinned with `source_id`+`jurisdiction`, large sources set to chunked/parked — finding 18

---

## 4. FIX PLAN

### (A) Agent can fix now — code/config
1. **B2** — `config.py:52-54`: coalesce blank model → default. Sweep other `os.getenv(name, literal)` fields for the same present-empty trap (finding 6).
2. **B5** — `checkpoint.py` add `FAILED`; `onboard.py` `_run_stage`/`_record`/`run_batch` distinguish failed-vs-aborted; wrap `onboard_source` in try/except in all 3 batch loops (findings 16,17,39).
3. **B6** — `ingest.py` `_stringify` null/int-float fix + `_is_blank` token hardening + regression tests (findings 4,21).
4. **B7** — UTF-8 stdout reconfigure + non-legacy Console (finding 1).
5. **B4 (partial)** — `--yes` flag + non-TTY fail-fast in `run_batch` (findings 2,32).
6. **Fetch timeout** — wrap generated `fetch_data` in `ThreadPoolExecutor(...).result(timeout=900)` in `_execute_fetch`/chunks (finding 28).
7. **Density gate** — `assess_density` full-frame pass, not `df.head(2000)`; fold counts across ALL chunks (finding 19).
8. **Column collision** — dedup sanitized names in `_stringify` (`_2/_3` suffix) so two headers collapsing to one don't fail CREATE TABLE (finding 20).
9. **Snapshot size guard** — promote to chunked when `unknown` volume or frame > ~2M rows / ~500MB, else OOM stalls the pour (finding 22).
10. **Wire loadkit.preflight** — call budget/PAT/key gate at top of `run_batch`/`run_ingest`; implement missing `live_pat_expiry` (findings 23,25,33).
11. **Queue pinning** — add `source_id`+`jurisdiction`+`load_mode` to `sources_queue.py`; hard-gate collision with existing SOURCE_REGISTRY rows (finding 18).
12. **Registry robustness** — `register._encode` coerce non-list array facets instead of asserting; add tests for register.py/naming.py (findings 35,42).
13. **SEC/UA prompt** — add descriptive-UA mandate to `generate_ingest.txt` (finding 45).
14. **Quarantine** — dead-letter gate in `registry_queue.fetch_candidates` for N-consecutive-fail sources (finding 38); INGEST_RUNS-based skip for portal empties (finding 53).
15. **Portal tail progress** — exclude landed/empty source_ids from candidate query (finding 27).
16. **Post-pour hook** — regenerate FRIENDLY_LAYER / THE_LIBRARY / density probe once at batch end (findings 41,43).
17. **Smoke test** — offline `test_onboard_smoke.py` driving `onboard_source` under `fake_llm` (finding 34).
18. **Windows paths** — fix 8 hardcoded macOS-path scripts with `Path(__file__).resolve().parents[1]` (finding 50).
19. **DR DDL** — `infra/ddl/03_...sql:47` `CREDIT_QUOTA=60` (matches live), don't switch to OR REPLACE (finding 51).

### (B) Needs Chris — one-line actions
- **Set `ANTHROPIC_API_KEY`** in `library-onboarding/.env:10` (real key).
- **Set `ANTHROPIC_MODEL`** in `.env:13` to a valid id (e.g. `claude-sonnet-4-6`).
- **Set `ONBOARD_AUTO_APPROVE=1`** in `.env:60`.
- **Run** `pip install -r library-onboarding/requirements.txt` in the onboard.py interpreter.
- **Add data-source API keys** to `.env` for in-scope sources (FRED, FEC, EIA, CENSUS, BLS, SAM, PROPUBLICA).
- **Raise budget:** `ALTER RESOURCE MONITOR RIPPLE_BUDGET SET CREDIT_QUOTA = 120;` (cost is not a constraint).
- **Enable alerts:** `ALTER RESOURCE MONITOR RIPPLE_BUDGET SET NOTIFY_USERS = (CROGG23);`
- **Rotate `SNOWFLAKE_PAT`** to a fresh token if the pour will run near/past 2026-09-20, update `.env:23`.

---

## 5. RECOMMENDED POUR SEQUENCE

**Pre-flight (Chris, once):** do all of section 4(B). Confirm:
```bash
cd library-onboarding
python -c "from config import settings; settings.require('anthropic_api_key'); print('key OK, model:', settings.anthropic_model, 'auto:', settings.auto_approve)"
python -c "import tenacity, bs4, lxml; print('deps OK')"
```

**Pre-flight (agent, once):** land B5, B6, B7 code fixes + the `--yes` flag. Run `pytest -q`.

**Step 1 — smoke (no spend):**
```bash
ONBOARD_FAKE_LLM=1 python onboard.py --batch    # verify it walks sources, continues past a failure, writes onboarding_log.json
```

**Step 2 — one real source:**
```bash
python onboard.py --url <one-bounded-source> --yes   # confirms key/model/deps/warehouse on a single source
```
Check `LIBRARY_META.INGEST_LOGS.INGEST_RUNS` for a `success` row; spot-check the landing table for `'nan'`/`'.0'` corruption.

**Step 3 — the pour.** Pin `sources_queue.py` first (finding 18), park unbounded sources, then:
```bash
python onboard.py --batch --yes > pour.log 2>&1   # resumes via onboarding_log.json; failed sources skip-and-continue (B5)
```
For the curated/pinned unattended paths, `live_batch.py` and `registry_batch.py --run` already set auto-approve.

**Step 4 — resume as needed.** Re-run the same command; `complete` sources are skipped, `failed`/`pending` retried.

**Step 5 — post-load regeneration (after pour completes):**
```bash
python scripts/thelibrary_inventory.py
python scripts/thelibrary_build.py --apply           # rebuild FRIENDLY_LAYER + THE_LIBRARY reading room
python scripts/propose_catalog_trust_gate.py --apply  # refresh LANDING_DENSITY_PROBE
```
`CATALOG` is a live view and self-updates; the three above are materialized snapshots that go stale otherwise (findings 41,43).

---

## 6. WHAT'S ALREADY SOLID

- **Idempotency** — snapshot-replace + SHA-256 skip-on-unchanged means re-running never duplicates or corrupts landed data. Resume is safe (finding 47/48/52/55).
- **Bespoke `scripts/*_load.py` loaders** — deterministic, use `dtype=str, keep_default_na=False`, dodge the `_stringify` corruption, don't need the LLM key. `bridge_fuel_load.py` chunked path is atomic (DROP-on-fail) and density-gated (finding 44).
- **Shared ingest primitives** — both LLM and bespoke paths funnel through the same `ingest.py` (`assess_density`, `_log_run`, reserved-word guard); one fix covers both.
- **CATALOG view** — live, self-updating on new sources; faceted navigation intact.
- **loadkit.preflight** — the budget/PAT/key gate is correct and unit-tested; it just needs wiring (findings 23,25,33).
- **Snowflake auth** — PAT works now (ACCOUNTADMIN, RIPPLE_WH); good until 2026-09-20.
- **Registry MERGE** — COALESCE-protects curated facets; won't clobber the hand-set columns it guards.
- **Test suite** — 100 offline tests pass in ~5s (density gate, keys, loadkit logic).

**Bottom line:** the loader engine and data-integrity primitives are sound. The gap is entirely in the pour *entrypoint's* configuration (4 blank env values + missing deps) and its *batch resilience* (one bad source kills the queue, plus three silent-corruption/crash traps). Fix B1–B7 and the checklist, and it pours.

## MEDIUM/LOW findings (appendix)

- [medium][agent] (resume / idempotency) live_batch/registry_batch resume can't recover a source that partially onboarded but never logged a success run
- [medium][chris] (budget) Nobody is notified at 75% — the NOTIFY trigger has no recipients, so the first signal Chris gets is a dead pour at 90%
- [medium][agent] (queue/registry_queue) Dead/empty sources are re-attempted on every run with no quarantine — permanent wasted RECON+SCRIPT spend
- [medium][agent] (entrypoint/batch) Batch loops have no per-source isolation for exceptions raised OUTSIDE a stage — one crash kills the whole pour
- [medium][agent] (ingest/chunked-resume) Only 'failed' triggers chunked resume; a batch killed hard (warehouse suspend / process kill) can leave a partial table logged as nothing, forcing a silent stale-append or full re-stream
- [medium][agent] (postload) THE_LIBRARY reading room + FRIENDLY_LAYER are materialized snapshots, not wired to the pour -- they go stale on every landed source
- [medium][agent] (postload/register) register._enrich swallows all errors -> transient LLM failures silently register sources as UNCLASSIFIED with no facets
- [medium][agent] (postload/catalog) LANDING_DENSITY_PROBE is a separate table the pour never populates, weakening the catalog's empty-detection for new sources
- [medium][agent] (pour-target) No single ordered runnable pour queue -- sources_queue.py (37, onboard.py) and outputs/LAND_EVERYTHING (~50, bespoke bridge_fuel_load) are two different machines
- [medium][agent] (ingest) generate_ingest prompt instructs the model to use a Mozilla UA -- SEC EDGAR (in the queue) will 403 on the onboard.py path
- [medium][agent] (dbt/safety-net) Generated dbt models are written but never compiled/tested during the pour
- [low][agent] (loader core / incremental append + _watermark) Incremental append is not crash-safe: a mid-COPY failure can leave partial rows, and re-run recomputes the watermark from MAX(cursor) — risking skipped or duplicated rows
- [low][agent] (loader core / write_pandas overwrite semantics) Snapshot overwrite is a non-transactional DROP+RENAME — a crash between the two statements deletes the landing table (no auto-recovery)
- [low][chris] (auth/secrets (Snowflake)) Active Snowflake PAT (LIBRARY_PAT, ACCOUNTADMIN) expires 2026-09-20 -- a pour that slips past it dies mid-write with no failed-marker
- [low][agent] (portability) Hardcoded macOS paths (/Users/chrisr.) crash 8 scripts on this Windows box
- [low][agent] (infra) Resource monitor exists only as reconstructed DDL with a stale quota (30, not 60) — re-running the DR script would HALVE the cap and instantly suspend a live pour
- [low][agent] (resume/state) Batch progress ledger for LLM onboarding is a single local JSON file — not concurrency-safe and only records terminal state
- [low][agent] (harvest/portal_loader) Portal harvest retries 0-row/empty datasets every run (no table created => never 'landed')
- [low][agent] (postload/catalog) CATALOG mislabels genuine full loads that land a round row-count as 'sampled'
- [low][agent] (resume) No onboarding_log.json -- --batch restarts from source 1 every run, and a mid-pour crash has no resume record for the LLM path