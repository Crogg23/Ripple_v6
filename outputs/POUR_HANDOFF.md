# POUR HANDOFF — new Claude Code session (2026-07-01)

MISSION: Orchestrate the data pour for the Ripple Library — turn on the ~900 confirmed-keyless
(≈1,400 incl. likely-keyless) sources that are hooked up and ready, resumably and unattended, and
see it through to landed data + a refreshed reading room.

## STATE (already done — do NOT redo)
- The ingestion pipeline was stress-tested twice (64-agent readiness + 25-agent QA) and hardened:
  memory-safe (OOM guard -> chunked streaming), hang-safe (socket read timeout), cost-guarded
  (dead-source quarantine + budget preflight), corruption-guarded (null/int _stringify + density
  gate), Windows-clean. 111 tests pass (`python -m pytest tests/ -q`).
- Repo: c:\Code\Ripple_v6 (Windows, PowerShell + git-bash, Python 3.12). Entry point:
  library-onboarding/onboard.py. Unattended pour = `python onboard.py --batch --yes`.
- Snowflake: account ONEAFDA-UMB20733, user CROGG23, role ACCOUNTADMIN, warehouse RIPPLE_WH.
  Landing = LIBRARY_RAW.LANDING.<UPPER(SOURCE_ID)>; runs log = LIBRARY_META.INGEST_LOGS.INGEST_RUNS;
  catalog = LIBRARY_META.REGISTRY.CATALOG. Read-only checks via library-onboarding/snow.py:connect().
- Tap census: 124 ON (landed+modeled); ~900 confirmed-keyless + ~470 auth-unrecorded scouted;
  ~129 free-key; ~21 paid; 20 hand-written loaders in scripts/ fire with no LLM.
- Read first: outputs/POUR_GO_CHECKLIST.md, outputs/pour_readiness_REPORT_2026-07-01.md,
  outputs/pour_final_qa_2026-07-01.md, build-state.md (CURRENT FOCUS).

## STEP 0 — confirm prereqs (STOP if any fail; these are Chris's, not yours to guess)
```bash
cd c:\Code\Ripple_v6\library-onboarding
python -c "from config import settings; settings.require('anthropic_api_key'); print('key OK, model:', settings.anthropic_model)"
python -c "import tenacity, bs4, lxml; print('deps OK')"    # if fails: pip install -r requirements.txt
```
- Budget: `SHOW RESOURCE MONITORS` -> confirm RIPPLE_BUDGET quota is raised well above the pour
  (Chris must `ALTER RESOURCE MONITOR RIPPLE_BUDGET SET CREDIT_QUOTA = 300;` — agent is blocked from it).
- If any prereq is unmet, tell Chris exactly which and stop. Do not start a pour that will fail on #1.

## STEP 1 — validate end-to-end on a small real wave (do this FIRST)
`onboard.py --batch` runs the 37 marquee sources in library-onboarding/sources_queue.py. Run it and
watch the first few LAND for real:
```bash
python onboard.py --batch --yes > pour_wave1.log 2>&1
```
Then verify in Snowflake (read-only): recent INGEST_RUNS by status, and spot-check 2-3 landing tables
for `'nan'`/`'.0'` corruption and real row counts. Confirm the batch skip-and-continues past any
failure and writes onboarding_log.json. FIX any systemic problem before scaling.

## STEP 2 — scale to the ~900 keyless (the main event)
The 37-source queue is not the 900. To pour the keyless scouted catalog rows, drive onboard over them.
RECOMMENDED: generate sources_queue-style entries from the catalog and run --batch (it's resumable,
quarantines dead sources, skips complete):
```sql
-- the keyless, not-yet-loaded pool (run via snow helper):
SELECT c.source_id, r.NAME, r.URL, c.jurisdiction
FROM LIBRARY_META.REGISTRY.CATALOG c JOIN LIBRARY_META.REGISTRY.SOURCE_REGISTRY r USING (source_id)
WHERE c.lifecycle = 'scouted'
  AND LOWER(COALESCE(r.AUTH_REQUIRED,'')) IN ('','none','no','false')
ORDER BY (ARRAY_SIZE(c.join_keys_std) > 0) DESC, c.source_id;   -- connectable first
```
Write these as a batch queue (pin source_id + jurisdiction per entry so the LLM can't collide — recon
honors foreman pins), in waves of ~50-100, and run `python onboard.py --batch --yes >> pour.log 2>&1`.
Prefer connectable (has a join key) sources first — they light up the graph, not just land.
Also: the 20 hand-written scripts/*_load.py + *_backfill.py fire immediately with no LLM (FEC,
USASpending, OFAC, IRS BMF, CMS Open Payments, SEC EDGAR, NOAA, UCDP...) — run any not already landed.

## STEP 3 — monitor + resume (unattended)
- Watch spend: re-check RIPPLE_BUDGET periodically; the pour prints a budget heads-up at batch start.
- Watch health: `SELECT STATUS, COUNT(*) FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
  WHERE _LOADED_AT > DATEADD('hour',-6,CURRENT_TIMESTAMP()) GROUP BY 1;`
- Resume: just re-run the same `--batch --yes` — complete sources skip, failed/pending retry, a source
  that failed ONBOARD_MAX_ATTEMPTS (3) times is quarantined (delete its onboarding_log.json entry to
  force a retry). A source stuck on a missing key logs loudly and skips — that's expected.

## STEP 4 — after the pour: WIRE UP CONNECTIONS + FIRE DETECTORS (do NOT skip)
onboard.py auto-links each landed source per-source (checkpoint 6 = `connect connect-one`, best-effort),
BUT: bespoke-loader sources skip it, incremental misses cross-source matches a full discover finds, and
crucially the DETECTORS never auto-run. Landing data without this = a pile of tables, not findings.
Run the full reconcile + detectors ONCE after the pour:
```bash
python scripts/thelibrary_refresh.py --apply   # rebuild FRIENDLY_LAYER + THE_LIBRARY reading room
python -m connect all           # fingerprint -> discover -> spine (full graph rebuild; discover = the compute hog, one-time OK)
python -m connect seed          # re-init incremental twins/watermark AFTER the full rebuild
python -m connect leads --run   # FIRE THE DETECTORS -> LIBRARY_META.CONNECT.LEADS (this is where findings appear)
python -m connect entity-index  # rebuild the search/dossier index
```
Then review new findings: `python -m connect leads --top 40`. Nothing about a named person is a
published fact until reviewed (`connect review --id LEAD_xxxx ...`) — that safety gate stays on.

## GUARDRAILS
- Cost is fine for a ONE-TIME pour, but don't loop chunked re-pours (they re-download; no SHA-skip).
- Never commit secrets. Read-only in Snowflake unless loading. The agent is classifier-blocked from
  ALTER RESOURCE MONITOR and grants — those are Chris's.
- If a whole class of sources fails the same way (e.g. a parser gap, a 403), fix the shared loader /
  the generate_ingest.txt prompt once, don't paper over per-source.

FIRST ACTION: run STEP 0, report prereq status, then propose the STEP 1 wave and wait for Chris's go.
