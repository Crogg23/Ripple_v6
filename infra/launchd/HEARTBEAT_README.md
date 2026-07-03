# The Heartbeat — install + run runbook

Keeps the Library alive on a cadence with no hand on the wheel. One runner
(`scripts/heartbeat.py`) drives four tiers, each behind hard guards. **Preview by
default — it writes nothing and spends nothing until you pass `--run`.**

```
ACQUIRE   re-ingest DUE/OVERDUE sources   (OPT-IN, registry-gated, GREEN-budget only)
LINK      connect connect-changed --scope spine   (catch up the spine for movers)
MEASURE   build_freshness_ledger.py --apply        (refresh DATA recency)
RECONCILE connect all  (weekly)            (full rebuild + reseed twins; drift backstop)
```

The agent does NOT install launchd jobs or run writes. You do, from here.

---

## 0. Prove it first (read-only, 0 credits)

Run these in order. None of them write to Snowflake or spend credits.

```bash
cd /Users/chrisr./Documents/GitHub/Ripple_v6

# (a) OFFLINE guard proof: process-group hard-kill + lock + budget math. No warehouse at all.
python3 scripts/heartbeat.py --selftest
#   expect: [1] ... PASS   [2] ... PASS   [3] ... PASS   == selftest PASS ==

# (b) DRY-RUN tick: shows the live budget band + exactly which tiers WOULD run + their commands.
python3 scripts/heartbeat.py
#   The runner DOWN-SCOPES by band: GREEN = full heartbeat; YELLOW = link+measure only;
#   RED = clean no-op (nothing spins a warehouse). Budget is tight right now (RED), so a
#   live --run tick no-ops; ACQUIRE+RECONCILE need GREEN. (Dry-run still previews the plan.)

# (c) STATUS: budget, lock holder, ledger presence, per-tier due/not.
python3 scripts/heartbeat.py --status
```

Only when (a)/(b)/(c) look right do you install the scheduler.

---

## 1. Install the MAIN agent (LINK + MEASURE + weekly RECONCILE; ACQUIRE off)

```bash
cp infra/launchd/com.ripple.heartbeat.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/com.ripple.heartbeat.plist

# confirm it's registered
launchctl list | grep com.ripple.heartbeat
# watch it
tail -f outputs/_heartbeat.log
```

It ticks every 2h and on every boot/login (`RunAtLoad`). The Mac sleeping is fine:
cadence lives in the runner (run-if-overdue), so a missed tick just makes a tier
overdue and the next wake tick runs it once.

**Paths / interpreter:** the plists hardcode `/usr/bin/python3` and the repo path. The
runner spawns every tier with its OWN interpreter (`sys.executable`), so launchd's python
*is* the python that runs `connect` and the loaders — it must have the deps
(snowflake-connector-python, pandas, python-dotenv). Confirm the plist's interpreter is the
one your deps live under before `cp` by running `/usr/bin/python3 -c "import sys,
snowflake.connector, pandas; print(sys.executable)"`; if it errors or prints a different
path than your working `python3 -c "import sys; print(sys.executable)"`, edit the two
interpreter `<string>` lines in the `.plist` to the correct absolute python path first.

To stop:

```bash
launchctl unload -w ~/Library/LaunchAgents/com.ripple.heartbeat.plist
```

---

## 1b. (one-time, recommended) server-side hang backstop

The local hard-kill (`os.killpg`) only kills the runner's process tree. The spawned
`connect all` opens its **own** Snowflake connection, so a query it orphans keeps burning
warehouse credits server-side after the local kill — which would defeat the hang guard. The
runner closes that gap by forcing a warehouse-level `STATEMENT_TIMEOUT_IN_SECONDS` (= the
tier's local hard timeout + 600s) **before every heavy run**, so an abandoned query
self-cancels on its own.

That is automatic. To also pin it as a standing guardrail (in force even outside a heartbeat
run), set it once yourself — `RIPPLE_WH` is your `SNOWFLAKE_WAREHOUSE`:

```sql
-- 7800s = the reconcile local hard cap (7200s) + 600s, so the LOCAL kill still fires first.
ALTER WAREHOUSE RIPPLE_WH SET STATEMENT_TIMEOUT_IN_SECONDS = 7800;
```

The runner re-asserts the correct per-tier cap each heavy run regardless; if it ever can't
(PAT lost the grant, network), it logs `stmt_timeout_unset` loudly and falls back to killpg
+ warehouse AUTO_SUSPEND + the budget cap.

---

## 2. (Later) enable ACQUIRE — the riskiest tier

ACQUIRE re-ingests sources unattended. It is OFF unless you opt in. Before enabling:

1. Wait for budget headroom — `heartbeat.py --status` should show `band=GREEN`
   (below GREEN the runner down-scopes by band and ACQUIRE no-ops anyway).
2. Vet `scripts/acquire_recipes.json`. Only sources with `"enabled": true` ever run.
   The seed enables exactly one verified-safe loader (`fed_cisa_kev`) and ships
   `fed_usgs_earthquakes` **disabled** with the reason. Adding a source there is the
   opt-in act.
3. Try it by hand first:

```bash
# dry-run: what WOULD be re-ingested
python3 scripts/heartbeat.py --tier acquire --acquire-optin --max-sources 3

# do it (GREEN budget only; re-checks budget before every source)
python3 scripts/heartbeat.py --tier acquire --run --acquire-optin --max-sources 3
```

Only then, if you want it scheduled:

```bash
cp infra/launchd/com.ripple.heartbeat.acquire.plist ~/Library/LaunchAgents/
launchctl load -w ~/Library/LaunchAgents/com.ripple.heartbeat.acquire.plist
```

The runner lock serialises this against the main agent (no warehouse overlap).

---

## 3. First-ever MEASURE needs your blessing (one-time)

`V_SOURCE_FRESHNESS` / `SOURCE_FRESHNESS` do not exist on the warehouse yet (the
builder was previewed, never `--apply`'d). The first `--run` tick (or the line below)
creates them — this is the first warehouse write, so run it once yourself:

```bash
python3 scripts/build_freshness_ledger.py --apply     # creates the ledger + view
# or just let the first heartbeat --run tick do it (MEASURE is due on a fresh install)
```

After that, ACQUIRE has a DUE/OVERDUE feed to read.

---

## Guards (what stops a runaway)

| Guard | How |
|---|---|
| **Budget** | free `SHOW RESOURCE MONITORS` each tier. `spendable = quota*90% - used`. GREEN≥5 / YELLOW≥2 / RED<2. ACQUIRE+RECONCILE are GREEN-only; RED spins no warehouse. |
| **Hang** | every long job runs in its own process group; a pure-Python hard timeout `os.killpg`s the WHOLE tree (SIGTERM→SIGKILL). PLUS a **server-side backstop**: before each heavy run the runner forces the warehouse `STATEMENT_TIMEOUT_IN_SECONDS` to (tier hard timeout + 600s), so a query the spawned subprocess orphans self-cancels server-side even after the local kill. `connect all` local hard cap 120 min. No coreutils `timeout` needed. |
| **No overlap** | `outputs/_heartbeat.lock` flock + pidfile; a second tick (or a wrapped manual run) exits no-op. Dead-holder PID check reclaims a stale lock. |
| **Catch-up** | `outputs/_heartbeat_state.json` per-tier last-success; tier runs only when overdue. Survives sleep. |
| **ACQUIRE safety** | opt-in flag + registry-gated recipes + GREEN-only + max-sources + per-source budget re-check + SHA-skip in the loaders + cadence allowlist (no annual/static/irregular) + excludes dead/unknown. |

Logs: `outputs/_heartbeat.log` (structured), `outputs/_heartbeat_<tier>_<ts>.log` (per-run
tee), `outputs/_heartbeat.launchd.log` (launchd stdout). All gitignored.

---

## Cloud alternative (note, not the default)

A GitHub Actions `schedule:` cron runs on always-on infra (no asleep-miss), but: GA cron
is best-effort and can drop runs, auto-disables after 60 days of repo inactivity, needs the
Snowflake PAT as a repo secret, and moves unattended `exec()` of model-generated ingestion
into CI (a security surface). We default to **launchd** because everything already runs
locally and the PAT is already on disk. Same runner works under either — only the trigger
changes.

## Heads-up

The Snowflake PAT in `library-onboarding/.env` was rotated 2026-07-02 — current expiry
**2026-09-20**. Canonical credential expiries live in `infra/keys_ledger.json` (the preflight
gate reads it). If the token ever does die, the heartbeat fails auth loudly
(`budget read -> RED, reason=connect_error`) and no-ops rather than silently doing nothing
wrong. Rotate the token to keep it alive.
