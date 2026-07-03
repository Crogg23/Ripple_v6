# Instrument Hardening — Handoff (2026-07-02, Fable)

One session, audit → plan → 8-lens adversarial stress-test → execution. Every BAD finding and every
instrument-side COULD-BE from `outputs/FABLE_AUDIT_2026-07-02.md` is addressed. Songs deferred by design.

## What shipped (committed, tests green)
| Wave | What | Commit |
|---|---|---|
| 0 | rapidfuzz pin (CI was red 14 runs), pour-log gitignore, dbt FAKE_LLM fixture removed | d22d733 |
| 1 | pour guards: empty/auth/collision gates, exec env blocklist, honest exit codes + error text, fence-retry + compile check, ISO watermark validation, sid-keyed atomic resume, TLS-on-by-default, fake-dbt redirect | 51fba4a |
| 2 | safety chokepoint: dashboards route through `leads.published()`, overlay from JOBS, archive-honest vessel titles, date-gate engine capability, parameterized receipts, rung-display honesty | a324a7d |
| 3 | loader atomicity: bridge_fuel chunked staging-swap (crash drops STAGING not LIVE), facet-clobber guard, fec_itcont smoke-no-swap + failed-run log, empty-registration alignment, 8 backfills deprecated + provenance fixed, conformance test | 46488d9 |
| 7 | keep-alive on Windows: heartbeat port (selftest PASSES), PAT-expiry check + keys_ledger + check_keys, 4 scheduled tasks (StartWhenAvailable), budget-restore step | bc22214 |
| 8 | docs reconciled: 6 checkpoints, V_STATE-not-prose, 5 stale PAT alarms resolved, overclaim fixes, provenance contract | 8982542 |
| 4 | warehouse truth layer | 9189859 + 83650f3 |
| 6 | spine expansion (politics keys + EIN detector) | _pending commit_ |

## What is LIVE in Snowflake now (applied read-only-safely alongside the running pour)
- **`LIBRARY_META.REGISTRY.V_STATE`** — one row per metric, derived. Query this; stop trusting prose numbers.
- **`LIBRARY_META."CONNECT".CONNECT_EDGES`** — the canonical edge store (shell; populated by the post-pour rebuild).
- **First-ever DR export** — `backups/dr/20260702_091350/` holds 6,341 rows of non-rebuildable control-plane
  content (registry, run log, leads, entity links, vocab) off-platform with a manifest.
- **Freshness ledger DEPLOYED** — `SOURCE_FRESHNESS` (102 sources) + `V_SOURCE_FRESHNESS` (32 fresh / 39 stale /
  6 overdue / 3 due / 22 unknown). serve/ freshness badges light up.
- **`SOURCE_REGISTRY.REDISTRIBUTION_RESTRICTED`** column; `intl_acled` flagged; the registry queue excludes
  restricted sources; ACLED pruned from `pour_queue_keyless.json`.
- **4 Windows scheduled tasks** registered (weekly DR export, weekly refresh, hourly heartbeat, daily nag).

## ⚠️ ACTION ITEMS FOR YOU (Chris)

### 1. Restart the pour to activate the new guards (do this before ~entry 110; ACLED is entry 118)
The running process (PID 1720) holds the OLD code + OLD queue (still contains ACLED) in memory. Your edits
are on disk and take effect on restart. Stop procedure (from the stress-test):
- Watch `library-onboarding/pour_keyless.log` for an inter-source boundary (after `onboarded -> SOURCE_ID`
  / `skipped` / `failed`, before the next `Onboarding` banner).
- `Ctrl+C` there (handled cleanly; log saved; resume-safe). Confirm `onboarding_log.json` still parses.
- Re-run the SAME command: `python onboard.py --batch --yes --skip-dbt --repair 1 --queue outputs/pour_queue_keyless.json`
- Resume skips everything already `complete`; the new empty/auth/collision gates now apply; ACLED is gone from
  the queue and flagged restricted so it can never re-enter one.
- Note: a keyless pour now exits nonzero when real failures occur and `needs_key` sources are expected — that's
  by design; don't treat nonzero as a crash.

### 2. Run the op2022 reconcile (I was correctly blocked — it's a 13.25M-row live rewrite)
`python scripts/reconcile_op2022.py --apply` (from a normal shell, not the agent's auto-mode). Flips the
mislogged 13.25M-row `fed_cms_open_payments_2022` from lifecycle `scouted` → `landed`.

### 3. NPPES — DONE live this session (✅). AIS mart rebuild is the only remainder.
NPPES re-landed clean via the atomic loader: **9,606,683 rows** swapped over the wiped 700K landing,
the facet-clobber guard preserved the curated registry row. NPPES landing now == its 9.6M mart — that
drift is closed, no dbt rebuild needed for it. **Remaining (optional, lower priority):** the AIS mart is
still frozen at 7.3M vs a 58.1M landing. To rebuild it (dbt-core venv `.dbt-venv`, from inside
`library-onboarding/ripple_dbt`, env sourced): `dbt build --select stg_fed_noaa_ais__ais_vessel_positions+`
— an 8x mart over 58M rows, so run it on COMPUTE_WH when the pour is quiet. Do NOT `dbt build` the
politics models (they mirror Python-built canon; `dbt test --select marts.politics` only).

### 4. Post-pour session (deferred by design — needs the pour finished + quiet warehouse)
- Full connect rebuild over the complete poured landing zone: `python -m connect discover` (populates
  CONNECT_EDGES + regenerates the JSON) → `spine` → `entity-index` → `connect connect-changed` (sweeps every
  source whose checkpoint-6 refused during the Wave-6 keys.py window) → `connect leads --run` (updates vessel
  titles in place + fires the new EIN detector).
- `python scripts/regrade_empty_loads.py --apply` (safe once the pour is done — it samples live landing tables).
- One elevated re-run of `scripts/register_windows_tasks.ps1` upgrades the 3 worker tasks to S4U logon.
- After the pour: `python scripts/budget_sprint.py --restore` (drop the 300-credit sprint quota back to 15).

## Bonus this session — the `ripple` CLI (5 quality-of-life optimizations)
One front door instead of 54 scripts. `python -m ripple <verb>` (or `python ripple.py <verb>`):
- **`ripple status`** — the Morning Deck: live pour + scale + freshness (worst rotting sources) + your
  to-do queues (1,030 leads / 661 domains) + since-last-time deltas + budget + health, one screen.
- **`ripple review leads|domains`** — the batch cockpit: agent pre-fills a date-gated recommendation,
  you decide N-at-a-time, verdicts write through the safety spine (never auto-confirms a named person).
- **`ripple pour watch|plan|run`** — live meter (no more grepping the log) + deterministic-first router
  (93 of 719 sources land LLM-free; only 626 novel shapes pay for the agent).
- **`ripple doctor`** — one GREEN/RED go/no-go (PAT, deps, keys, tasks, DR age, freshness, budget).
All read through COMPUTE_WH so they never fight the pour; writers refuse while a pour holds the log.
+106 tests, verified live. Run `ripple doctor` at the start of every session; `ripple status` to see where you are.

## Ship note
This branch (`politics-itcont-money-mart`) carries `ee1cb55` with 51k-line pour-log blobs in history.
**Squash-merge the PR** so main's tree gets the clean final state without those blobs (they're already
untracked; squash collapses history to one commit whose tree has no logs).
