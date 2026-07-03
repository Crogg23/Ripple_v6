"""doctor -- one read-only GREEN/RED go/no-go health check.

Answers a single question: "is the platform safe to operate right now?" It runs a
fixed battery of checks, each returning (status, name, detail), prints them as one
STATUS/CHECK/DETAIL table, and ends with a verdict:
  * GREEN -- good to go        -> exit 0
  * RED -- N blocking problem  -> exit 1

Only BAD blocks. WARN is advisory (act soon, but you can still run). This is
deliberately read-only: it NEVER writes, launches a pour, or touches the live
onboarding log -- a health check that changes state isn't a health check.

Design notes:
  * The aggregation logic (check-results -> verdict + exit code) is a PURE function
    (`verdict`) so it can be unit-tested without a DB.
  * Each check is written to DEGRADE, never crash: if Snowflake is unreachable the
    reachability check goes BAD and every DB-dependent check reports WARN 'skipped,
    no DB' instead of throwing.
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from datetime import timedelta

from . import common as C

# Status constants -- three-state, ordered by severity. Only BAD blocks the verdict.
OK, WARN, BAD = "OK", "WARN", "BAD"

# The runtime dependency set the pour path imports. If any is missing, a load that
# looks green on paper dies at import time -- so a missing dep is BAD.
RUNTIME_DEPS = [
    ("snowflake.connector", "snowflake-connector-python"),
    ("pandas", "pandas"),
    ("requests", "requests"),
    ("plotly", "plotly"),
    ("bs4", "beautifulsoup4"),
    ("tenacity", "tenacity"),
    ("lxml", "lxml"),
]

# Optional per-wave API keys (mirrors scripts/check_keys.py / secrets_check.py's list).
# Unset is a WARN, never a block -- keyless Wave-1 sources don't need any of these.
OPTIONAL_KEYS = [
    "RIPPLE_CONTACT_UA",
    "SAM_API_KEY",
    "CENSUS_API_KEY",
    "COURTLISTENER_TOKEN",
    "SOCRATA_APP_TOKEN",
    "ANTHROPIC_API_KEY",
]

# Thresholds (kept as module constants so tests can reason about the same numbers).
DR_MAX_AGE_DAYS = 8            # a disaster-recovery export older than this -> WARN
FRESHNESS_WARN_THRESHOLD = 25  # this many overdue+stale sources -> WARN
BUDGET_MIN_HEADROOM_CREDITS = 15.0  # credits-to-suspend under this -> WARN


def add_arguments(parser) -> None:
    parser.add_argument("--json", action="store_true",
                        help="emit the check results as JSON instead of a table")


# --------------------------------------------------------------------------- #
# PURE aggregation -- the heart of the verdict, unit-tested with no DB.
# --------------------------------------------------------------------------- #
def verdict(results):
    """Fold a list of (status, name, detail) into (exit_code, headline).

    RED (exit 1) the instant ANY check is BAD; the headline counts the blockers.
    Otherwise GREEN (exit 0) -- WARN never blocks. Empty list is vacuously GREEN."""
    blockers = [r for r in results if r[0] == BAD]
    if blockers:
        n = len(blockers)
        return 1, f"RED -- {n} blocking problem{'s' if n != 1 else ''}"
    return 0, "GREEN -- good to go"


# --------------------------------------------------------------------------- #
# PURE checks -- inputs injected so they unit-test without touching disk/DB.
# --------------------------------------------------------------------------- #
def check_dr_export_age(dr_root, now):
    """Newest immediate subdir of backups/dr must exist and be recent.

    dr_root is a Path (may not exist). now is an aware datetime. Directory names
    are timestamps but we trust the filesystem mtime for age -- simpler and it
    survives a rename. Missing or stale -> WARN (a cold backup never blocks a read
    but the operator should know DR is drifting)."""
    try:
        if not dr_root.exists():
            return (WARN, "dr_export_age", f"no DR backups dir at {dr_root}")
        subdirs = [p for p in dr_root.iterdir() if p.is_dir()]
        if not subdirs:
            return (WARN, "dr_export_age", f"{dr_root} has no export subdirs")
        newest = max(subdirs, key=lambda p: p.stat().st_mtime)
        from datetime import datetime, timezone
        mtime = datetime.fromtimestamp(newest.stat().st_mtime, tz=timezone.utc)
        age_days = (now - mtime).total_seconds() / 86400.0
        if age_days > DR_MAX_AGE_DAYS:
            return (WARN, "dr_export_age",
                    f"newest DR export {newest.name} is {age_days:.1f}d old "
                    f"(over {DR_MAX_AGE_DAYS}d) -- re-run the DR export")
        return (OK, "dr_export_age", f"newest DR export {newest.name} ({age_days:.1f}d old)")
    except Exception as e:
        return (WARN, "dr_export_age", f"could not read DR dir: {str(e)[:80]}")


def check_freshness(freshness_rows):
    """Fold V_SOURCE_FRESHNESS rows into a single status.

    freshness_rows is a list of (FRESHNESS_STATE, count) pairs (already grouped).
    Any 'dead' source -> BAD (a source we thought we had is gone). A large pile of
    overdue+stale -> WARN. None (view absent / query failed) -> WARN 'ledger not
    deployed'."""
    if freshness_rows is None:
        return (WARN, "freshness", "freshness ledger not deployed (V_SOURCE_FRESHNESS absent)")
    counts = {}
    for state, n in freshness_rows:
        counts[str(state or "unknown").lower()] = int(n or 0)
    dead = counts.get("dead", 0)
    if dead:
        return (BAD, "freshness",
                f"{dead} source(s) DEAD in the freshness ledger -- investigate before pouring")
    lagging = counts.get("overdue", 0) + counts.get("stale", 0)
    if lagging >= FRESHNESS_WARN_THRESHOLD:
        return (WARN, "freshness",
                f"{lagging} sources overdue+stale (>= {FRESHNESS_WARN_THRESHOLD}) -- refresh queue backing up")
    return (OK, "freshness",
            f"no dead sources; {lagging} overdue+stale, {counts.get('fresh', 0)} fresh")


def check_budget(quota, used):
    """Headroom to the resource-monitor SUSPEND line. A mid-write suspend aborts the
    COPY across every warehouse, so thin headroom is a WARN worth surfacing.

    quota/used are credits (or None if the monitor couldn't be read). We measure
    headroom to the 90% suspend ceiling -- the same line loadkit.preflight guards."""
    if quota is None or used is None:
        return (WARN, "budget", "budget monitor unreadable (RIPPLE_BUDGET not found)")
    ceiling = quota * 0.90
    headroom = ceiling - used
    if headroom < BUDGET_MIN_HEADROOM_CREDITS:
        return (WARN, "budget",
                f"only {headroom:.1f}cr to the suspend line ({ceiling:.1f}cr of {quota:.0f}) "
                f"-- raise the quota or wait for reset")
    return (OK, "budget", f"{headroom:.1f}cr headroom to suspend ({used:.1f}/{quota:.0f} used)")


def check_deps(import_module=importlib.import_module):
    """Every runtime dependency imports. import_module is injectable so a test can
    simulate a missing package without uninstalling anything."""
    missing = []
    for mod, pip_name in RUNTIME_DEPS:
        try:
            import_module(mod)
        except Exception:
            missing.append(pip_name)
    if missing:
        return (BAD, "deps", "missing: " + ", ".join(missing) + " -- pip install them")
    return (OK, "deps", f"all {len(RUNTIME_DEPS)} runtime deps import")


def check_keys(getenv=os.environ.get):
    """Snowflake creds must be present (BAD if not -- nothing runs without them);
    optional per-wave keys are reported as WARN when unset. getenv is injectable."""
    have_account = bool((getenv("SNOWFLAKE_ACCOUNT", "") or "").strip())
    have_user = bool((getenv("SNOWFLAKE_USER", "") or "").strip())
    have_auth = bool((getenv("SNOWFLAKE_PAT", "") or "").strip()
                     or (getenv("SNOWFLAKE_PASSWORD", "") or "").strip())
    if not (have_account and have_user and have_auth):
        gaps = []
        if not have_account:
            gaps.append("SNOWFLAKE_ACCOUNT")
        if not have_user:
            gaps.append("SNOWFLAKE_USER")
        if not have_auth:
            gaps.append("SNOWFLAKE_PAT/PASSWORD")
        return (BAD, "keys", "missing Snowflake creds: " + ", ".join(gaps))
    unset = [k for k in OPTIONAL_KEYS if not (getenv(k, "") or "").strip()]
    if unset:
        return (WARN, "keys",
                f"Snowflake creds present; {len(unset)} optional key(s) unset: " + ", ".join(unset))
    return (OK, "keys", "Snowflake creds present; all optional keys set")


# --------------------------------------------------------------------------- #
# Live checks -- thin wrappers around the real I/O (not unit-tested).
# --------------------------------------------------------------------------- #
def _check_snowflake(conn):  # pragma: no cover -- needs a live DB
    """conn is an already-open connection (or None). SELECT 1 to prove it answers."""
    if conn is None:
        return (BAD, "snowflake_reachable", "connect() failed -- no Snowflake")
    try:
        one = C.scalar(conn, "SELECT 1")
        if one == 1:
            return (OK, "snowflake_reachable", "connected, SELECT 1 answered")
        return (BAD, "snowflake_reachable", f"SELECT 1 returned {one!r}")
    except Exception as e:
        return (BAD, "snowflake_reachable", f"query failed: {str(e)[:80]}")


def _check_pat_expiry():  # pragma: no cover -- reads the live token
    """Decode the live PAT's JWT exp locally and gate on calendar distance."""
    try:
        from loadkit.preflight import live_pat_expiry, pat_expiry_check
        exp = live_pat_expiry()
        chk = pat_expiry_check(exp, C.now())
        status = BAD if not chk.ok else (WARN if chk.warn else OK)
        return (status, "pat_expiry", chk.detail)
    except Exception as e:
        return (WARN, "pat_expiry", f"could not read PAT expiry: {str(e)[:80]}")


def _skipped(name):
    """Uniform 'DB-dependent check skipped because Snowflake is down' result."""
    return (WARN, name, "skipped, no DB")


def _fetch_freshness_rows(conn):  # pragma: no cover -- needs a live DB
    """Grouped V_SOURCE_FRESHNESS states, or None if the view isn't there."""
    try:
        return C.rows(conn,
                      "SELECT FRESHNESS_STATE, COUNT(*) "
                      "FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS GROUP BY 1")
    except Exception:
        return None


def _check_v_state(conn):  # pragma: no cover -- needs a live DB
    """V_STATE returns rows (it's the derived source of truth; empty/absent -> WARN)."""
    state = C.vstate(conn)
    if state:
        return (OK, "v_state", f"V_STATE returns {len(state)} metrics")
    return (WARN, "v_state", "V_STATE returned nothing (view absent or empty)")


def _check_scheduled_tasks():  # pragma: no cover -- Windows-only, calls PowerShell
    """Windows scheduled tasks named Ripple-* should exist and be enabled. Off
    Windows this check is skipped cleanly (returns None so the caller drops it)."""
    if not sys.platform.startswith("win"):
        return None
    try:
        ps = ("Get-ScheduledTask -TaskName 'Ripple-*' -ErrorAction SilentlyContinue | "
              "Select-Object TaskName,State | ConvertTo-Json -Compress")
        out = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                             capture_output=True, text=True, timeout=30)
        raw = (out.stdout or "").strip()
        if not raw:
            return (WARN, "scheduled_tasks", "no Ripple-* scheduled tasks found")
        parsed = json.loads(raw)
        tasks = parsed if isinstance(parsed, list) else [parsed]
        disabled = [t.get("TaskName") for t in tasks
                    if str(t.get("State", "")).lower() == "disabled"]
        if disabled:
            return (WARN, "scheduled_tasks",
                    f"{len(disabled)} Ripple task(s) disabled: " + ", ".join(disabled))
        return (OK, "scheduled_tasks", f"{len(tasks)} Ripple task(s) present, none disabled")
    except Exception as e:
        return (WARN, "scheduled_tasks", f"could not query scheduled tasks: {str(e)[:80]}")


def _check_budget_live(conn):  # pragma: no cover -- needs a live DB
    try:
        from loadkit.preflight import live_budget_credits
        quota, used = live_budget_credits(conn)
        return check_budget(quota, used)
    except Exception as e:
        return (WARN, "budget", f"could not read budget: {str(e)[:80]}")


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def gather_checks():  # pragma: no cover -- wires the live readers together
    """Run every check in order and return the list of (status, name, detail).

    Order matters for readability: the DB reachability check runs first so, when it
    fails, the DB-dependent checks can all report 'skipped, no DB' instead of each
    throwing its own error."""
    results = []

    # Offline checks first -- these work even with Snowflake down.
    results.append(check_deps())
    results.append(check_keys())
    results.append(_check_pat_expiry())
    results.append(check_dr_export_age(C.REPO / "backups" / "dr", C.now()))
    sched = _check_scheduled_tasks()
    if sched is not None:  # None means "not on Windows" -- drop the row entirely
        results.append(sched)

    # Snowflake reachability gates everything DB-dependent.
    conn = None
    try:
        conn = C.connect()
    except Exception:
        conn = None
    sf = _check_snowflake(conn)
    results.append(sf)

    if sf[0] == BAD:
        # No DB -- report the DB-dependent checks as skipped rather than crashing.
        results.append(_skipped("freshness"))
        results.append(_skipped("v_state"))
        results.append(_skipped("budget"))
    else:
        results.append(check_freshness(_fetch_freshness_rows(conn)))
        results.append(_check_v_state(conn))
        results.append(_check_budget_live(conn))

    if conn is not None:
        try:
            conn.close()
        except Exception:
            pass
    return results


_MARKER = {OK: C.OK, WARN: C.WARN, BAD: C.BAD}


def _print_table(results):
    """Render the STATUS/CHECK/DETAIL table using the shared cp1252-safe helper."""
    data = [[_MARKER.get(s, C.DASH), name, detail] for (s, name, detail) in results]
    print(C.table(["STATUS", "CHECK", "DETAIL"], data))


def run(args) -> int:
    results = gather_checks()
    code, headline = verdict(results)

    if getattr(args, "json", False):
        payload = {
            "verdict": "RED" if code else "GREEN",
            "exit_code": code,
            "headline": headline,
            "checks": [{"status": s, "name": n, "detail": d} for (s, n, d) in results],
            "generated_at": C.now_iso(),
        }
        print(json.dumps(payload, indent=2))
        return code

    print(C.header("ripple doctor -- go/no-go"))
    _print_table(results)
    print(C.hr())
    warns = sum(1 for r in results if r[0] == WARN)
    tail = f"   ({warns} warning{'s' if warns != 1 else ''}, advisory only)" if warns else ""
    print(f"  {_MARKER[BAD] if code else _MARKER[OK]}  {headline}{tail}")
    return code
