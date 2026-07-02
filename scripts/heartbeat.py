#!/usr/bin/env python3
"""THE HEARTBEAT — keep the Library alive on a cadence with no hand on the wheel.

Phase 3 of the platform foundation. One runner orchestrates four tiers that tie the
foundation together, each behind hard guards. PREVIEW (dry-run) BY DEFAULT — it does
NOT write or spend until you pass --run.

    THE LOOP (run-if-overdue; the laptop sleeps, so cadence lives HERE, not in launchd)
      ACQUIRE   re-ingest DUE/OVERDUE sources (OPT-IN, registry-gated, GREEN-budget only)
      LINK      `connect connect-changed --scope spine` — catch up the spine for movers
      MEASURE   `build_freshness_ledger.py --apply` — refresh DATA recency
      RECONCILE (weekly) `connect all` — full rebuild + reseed twins; deletion/drift backstop

    THE GUARDS (the actual engineering)
      BUDGET    free `SHOW RESOURCE MONITORS` read -> spendable headroom below the 90%
                SUSPEND floor. RED/YELLOW down-scope; ACQUIRE+RECONCILE are GREEN-only.
      HANG      every long job runs in its OWN process group (start_new_session) with a
                pure-Python hard timeout that os.killpg(SIGTERM->SIGKILL)s the WHOLE tree
                (no coreutils `timeout` on this Mac; plain subprocess timeout leaks the
                snowflake driver child).
      LOCK      flock + pidfile (PID-alive stale detection). No two ticks — and no tick
                overlapping a manual `connect all` wrapped by this runner — ever overlap.
      CATCH-UP  per-tier last-success persisted in outputs/_heartbeat_state.json; a tier
                runs only when now-last_success >= its cadence. Missed ticks (asleep) just
                make the tier overdue; the next wake tick runs it ONCE.

USAGE
    python3 scripts/heartbeat.py                 # DRY-RUN: plan + live budget band, no writes
    python3 scripts/heartbeat.py --run           # execute every DUE tier (writes; ACQUIRE stays off)
    python3 scripts/heartbeat.py --status         # last-success + budget + ledger state (read-only)
    python3 scripts/heartbeat.py --selftest        # OFFLINE proof of lock + process-group kill (0 credits)
    python3 scripts/heartbeat.py --tier link --run         # force ONE tier (ignores cadence, still budget-gated)
    python3 scripts/heartbeat.py --tier acquire --run --acquire-optin --max-sources 3   # the riskiest tier

Read-only against the warehouse until --run. Writes go through the same ACCOUNTADMIN
PAT in library-onboarding/.env that the connect engine uses.
"""
from __future__ import annotations

import argparse
import json
import os
import platform
import signal
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeout
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# --------------------------------------------------------------------------- paths
REPO = Path(__file__).resolve().parents[1]
LIB = REPO / "library-onboarding"
OUTPUTS = REPO / "outputs"
SCRIPTS = REPO / "scripts"
PY = sys.executable or "/usr/bin/python3"

MASTER_LOG = OUTPUTS / "_heartbeat.log"
STATE_FILE = OUTPUTS / "_heartbeat_state.json"
LOCK_FILE = OUTPUTS / "_heartbeat.lock"
RECIPES_FILE = SCRIPTS / "acquire_recipes.json"
BUILD_LEDGER = SCRIPTS / "build_freshness_ledger.py"

# --------------------------------------------------------------------------- tunables
# Cadences (seconds) — how often each tier SHOULD run. Correctness, not the launchd tick.
CADENCE = {
    "link":      6 * 3600,        # 6h: catch up links the on-land hook missed
    "measure":   24 * 3600,       # daily: re-derive DATA recency
    "acquire":   24 * 3600,       # daily (but OPT-IN; off unless --acquire-optin)
    "reconcile": 7 * 24 * 3600,   # weekly: the full rebuild + reseed backstop
}

# Per-tier guard policy. bands = budget bands that may run it; min = min spendable credits
# (headroom below the 90% SUSPEND floor); soft/hard = timeout seconds (soft logs, hard kills).
TIER_POLICY = {
    "link":      {"bands": {"GREEN", "YELLOW"}, "min": 1.0, "soft": 1200, "hard": 1800},
    "measure":   {"bands": {"GREEN", "YELLOW"}, "min": 0.5, "soft": 600,  "hard": 1200},
    "reconcile": {"bands": {"GREEN"},           "min": 4.0, "soft": 4200, "hard": 7200},
    "acquire":   {"bands": {"GREEN"},           "min": 5.0, "soft": 1200, "hard": 2700},
}

# Budget band thresholds, keyed on SPENDABLE = (quota * suspend% / 100) - used.
BAND_GREEN = 5.0     # full heartbeat
BAND_YELLOW = 2.0    # cheap tiers only (link spine + measure); no ACQUIRE / RECONCILE
# below YELLOW = RED: nothing that spins a warehouse.

# ACQUIRE only considers sources whose cadence makes a NEWER vintage plausible. Annual /
# static / irregular series are usually already at their latest vintage -> re-ingest just
# recomputes the same SHA and wastes credits, so they are excluded from auto-selection.
ACQUIRE_CADENCES = ("daily", "weekly", "monthly", "quarterly", "real_time")
ACQUIRE_MAX_CAP = 10          # hard ceiling on --max-sources, whatever is passed
ACQUIRE_RECHECK_FLOOR = BAND_YELLOW   # abort the per-source loop if spendable drops below this

POLL_S = 5            # how often we poll a running child
KILL_GRACE_S = 15     # SIGTERM -> wait -> SIGKILL grace
# SERVER-SIDE hang backstop. The local killpg only kills THIS process tree; the spawned
# `connect all` opens its OWN snowflake connection (connect/db.py just delegates to
# snow.connect()), so an abandoned query keeps burning warehouse credits server-side
# AFTER the local kill — which would defeat the hang-guard. Before a heavy run we force
# the warehouse's STATEMENT_TIMEOUT_IN_SECONDS to (tier hard timeout + this buffer) so an
# orphaned query self-cancels regardless of the local kill. The buffer sits ABOVE the local
# hard timeout so the local kill always fires first on a healthy run (reconcile 7200s ->
# server cap 7800s). Belt-and-suspenders with killpg, not a replacement for it.
STMT_TIMEOUT_BUFFER_S = 600
FRESHNESS_VIEW = "LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS"

# --------------------------------------------------------------------------- process-group tracking
_CURRENT_CHILD = None   # the subprocess.Popen we are currently supervising (for signal cleanup)
_LOCK = None            # the HeartbeatLock held by this process (for signal cleanup)


# =========================================================================== #
# logging — structured key=value into outputs/_heartbeat.log (gitignored _*.log)
# =========================================================================== #
def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _fmt(v) -> str:
    s = "" if v is None else str(v)
    return f'"{s}"' if (" " in s or "=" in s) else s


def mlog(**kv) -> None:
    """One structured line to the master log AND stdout (which launchd captures)."""
    line = " ".join(f"{k}={_fmt(v)}" for k, v in kv.items())
    try:
        OUTPUTS.mkdir(parents=True, exist_ok=True)
        with open(MASTER_LOG, "a", encoding="utf-8") as f:
            f.write(f"{iso_now()} {line}\n")
    except Exception:
        pass
    print(line, flush=True)


# =========================================================================== #
# snowflake — short-lived connections through the SAME .env PAT the engine uses.
# Every parent-side warehouse touch is wrapped in a thread timeout (fail-closed) so a
# dead network can never wedge the scheduler.
# =========================================================================== #
def _snow_connect():
    """Open a connection the way connect/db.py does: load library-onboarding/.env, import snow."""
    try:
        from dotenv import load_dotenv
        load_dotenv(LIB / ".env", override=True)
    except Exception:
        pass
    if str(LIB) not in sys.path:
        sys.path.insert(0, str(LIB))
    import snow  # library-onboarding/snow.py (PAT-as-password, ACCOUNTADMIN)
    conn = snow.connect()
    # Scheduled-task wrapper sets RIPPLE_TASK_WAREHOUSE (COMPUTE_WH) so unattended
    # heartbeat work never contends with a live pour on RIPPLE_WH. SNOWFLAKE_WAREHOUSE
    # can't carry this: the load_dotenv(override=True) above clobbers a wrapper-set
    # value with .env's. Same convention as scripts/export_control_plane.py.
    task_wh = os.environ.get("RIPPLE_TASK_WAREHOUSE", "").strip()
    if task_wh and task_wh.replace("_", "").isalnum():
        try:
            conn.cursor().execute(f"USE WAREHOUSE {task_wh}")  # USE takes no binds; name validated
        except Exception:
            pass   # fall back to the .env warehouse rather than brick the tick
    return conn


def _with_timeout(fn, seconds: float, default):
    """Run fn() in a worker thread; return default on timeout OR error (fail-closed).
    The worker may linger but this is a short-lived process, so that is acceptable.

    NOTE: we do NOT use `with ThreadPoolExecutor(...)` — its __exit__ calls
    shutdown(wait=True), which on a FuturesTimeout would BLOCK the tick waiting for the
    hung worker (e.g. a wedged SHOW), stalling every later tier. shutdown(wait=False,
    cancel_futures=True) lets the daemonless worker linger and die with this short-lived
    process instead of stalling the tick."""
    ex = ThreadPoolExecutor(max_workers=1)
    fut = ex.submit(fn)
    try:
        return fut.result(timeout=seconds)
    except FuturesTimeout:
        return default
    except Exception:
        return default
    finally:
        try:
            ex.shutdown(wait=False, cancel_futures=True)
        except TypeError:        # cancel_futures added in 3.9; fall back gracefully
            ex.shutdown(wait=False)


def band_for(spendable: float) -> str:
    if spendable >= BAND_GREEN:
        return "GREEN"
    if spendable >= BAND_YELLOW:
        return "YELLOW"
    return "RED"


def read_budget(timeout_s: float = 60) -> dict:
    """FREE, authoritative budget gate via SHOW RESOURCE MONITORS (cloud-services, no
    warehouse). Fail-closed: any miss -> RED, spendable 0. Surfaces auth errors (PAT
    expiry) in 'reason' rather than silently no-opping."""
    def _inner() -> dict:
        try:
            conn = _snow_connect()
        except Exception as e:
            return {"ok": False, "reason": f"connect_error: {str(e)[:160]}", "band": "RED", "spendable": 0.0}
        try:
            cur = conn.cursor()
            cur.execute("SHOW RESOURCE MONITORS LIKE 'RIPPLE_BUDGET'")
            cols = [d[0] for d in cur.description]
            rows = cur.fetchall()
            if not rows:
                return {"ok": False, "reason": "monitor_not_found", "band": "RED", "spendable": 0.0}
            m = dict(zip(cols, rows[0]))
            quota = float(m.get("credit_quota") or 0)
            used = float(m.get("used_credits") or 0)
            remaining = max(0.0, float(m.get("remaining_credits") or 0))
            level = str(m.get("level") or "").upper()
            suspend_pct = int(float(str(m.get("suspend_at") or "90").rstrip("%") or 90))
            floor = quota * suspend_pct / 100.0
            spendable = max(0.0, floor - used)
            base = {"ok": True, "quota": quota, "used": used, "remaining": remaining,
                    "suspend_pct": suspend_pct, "suspend_floor": round(floor, 2),
                    "spendable": round(spendable, 2), "band": band_for(spendable), "level": level}
            if level != "ACCOUNT":
                # monitor not bound to the account -> the cap is NOT enforced -> fail closed.
                base.update({"ok": False, "reason": "not_account_level", "band": "RED", "spendable": 0.0})
            return base
        finally:
            conn.close()
    res = _with_timeout(_inner, timeout_s, None)
    if res is None:
        return {"ok": False, "reason": "budget_read_timeout", "band": "RED", "spendable": 0.0}
    return res


def tier_budget_ok(tier: str, budget: dict) -> tuple:
    """(allowed, why). A tier runs only if the band permits AND spendable >= its minimum."""
    pol = TIER_POLICY[tier]
    band = budget.get("band", "RED")
    spend = float(budget.get("spendable", 0.0))
    if band not in pol["bands"]:
        return False, f"band {band} not in {sorted(pol['bands'])}"
    if spend < pol["min"]:
        return False, f"spendable {spend} < min {pol['min']}"
    return True, "ok"


def _ensure_warehouse_timeout(cap_s: int) -> dict:
    """SERVER-SIDE backstop for the cost leak (MAJOR A). Force the warehouse's
    STATEMENT_TIMEOUT_IN_SECONDS to cap_s so a query the spawned `connect`/loader
    subprocess opened SELF-CANCELS server-side even after the local killpg fired (the
    local kill can't reach a query running on the subprocess's own connection). We set
    it on CURRENT_WAREHOUSE() — the SAME warehouse the spawned job uses (connect/db.py ->
    snow.connect() -> the one .env SNOWFLAKE_WAREHOUSE), so the cap actually governs it.

    cap_s is the tier's local hard timeout + STMT_TIMEOUT_BUFFER_S, so the local kill
    still fires first on a healthy run; this only catches the ABANDONED query. Idempotent
    (no ALTER when already at cap_s). Fail-SAFE: never raises and never wedges the tick —
    on any miss it WARNS LOUDLY and returns, leaving killpg + warehouse AUTO_SUSPEND +
    the budget cap as the remaining guards. ALTER WAREHOUSE is a cloud-services op (no
    warehouse spin, ~0 credits) and the .env PAT is ACCOUNTADMIN, so it has the grant."""
    def _inner() -> dict:
        conn = _snow_connect()
        try:
            cur = conn.cursor()
            cur.execute("SELECT CURRENT_WAREHOUSE()")
            row = cur.fetchone()
            wh = row[0] if row and row[0] else None
            if not wh:
                return {"ok": False, "reason": "no_current_warehouse"}
            cur.execute(f"SHOW PARAMETERS LIKE 'STATEMENT_TIMEOUT_IN_SECONDS' IN WAREHOUSE \"{wh}\"")
            cols = [d[0].lower() for d in cur.description]
            rows = cur.fetchall()
            cur_val = None
            if rows:
                m = dict(zip(cols, rows[0]))
                try:
                    cur_val = int(m.get("value"))
                except (TypeError, ValueError):
                    cur_val = None
            # Set to EXACTLY cap_s unless already there. Setting (rather than only
            # tightening a loose value) is deliberate: a cheaper earlier tier in the same
            # run may have left a LOWER cap that would prematurely kill this heavier tier,
            # so each tier re-asserts its own (hard + buffer) ceiling before it spawns.
            if cur_val != cap_s:
                cur.execute(f"ALTER WAREHOUSE \"{wh}\" SET STATEMENT_TIMEOUT_IN_SECONDS = {int(cap_s)}")
                return {"ok": True, "warehouse": wh, "was": cur_val, "set_to": int(cap_s), "action": "set"}
            return {"ok": True, "warehouse": wh, "was": cur_val, "set_to": cur_val, "action": "kept"}
        finally:
            conn.close()
    res = _with_timeout(_inner, 60, None)
    if not res or not res.get("ok"):
        mlog(event="stmt_timeout_unset", cap_s=cap_s,
             reason=(res or {}).get("reason", "timeout_or_error"),
             note="WARN: server-side STATEMENT_TIMEOUT not confirmed — an abandoned query "
                  "relies on killpg + warehouse AUTO_SUSPEND + the budget cap instead")
        return res or {"ok": False, "reason": "timeout_or_error"}
    mlog(event="stmt_timeout_backstop", warehouse=res.get("warehouse"),
         was=res.get("was"), set_to=res.get("set_to"), action=res.get("action"))
    return res


# =========================================================================== #
# LOCK — flock (kernel-enforced, auto-released on death) + pidfile (auditable
# stale detection via a PID-alive probe: OpenProcess on Windows, os.kill(pid,0)
# on POSIX). flock alone already prevents stale locks from our own crashes; the
# pidfile makes 'who holds it' visible and lets us reclaim on a filesystem where
# flock is unsupported. On Windows there is no fcntl at all — the ImportError
# path drops us to the pure pidfile fallback, which is the whole lock there.
# =========================================================================== #
class HeartbeatLock:
    def __init__(self, path: Path):
        self.path = path
        self._fd = None
        self._flocked = False

    @staticmethod
    def _alive(pid: int) -> bool:
        if not pid:
            return False
        if os.name == "nt":
            # Windows: NEVER os.kill(pid, 0) here — on Windows that call TERMINATES
            # the probed process (verified empirically; CPython maps it to
            # TerminateProcess, there is no harmless signal-0 probe). Ask the kernel
            # instead: OpenProcess + GetExitCodeProcess, stdlib ctypes only (psutil
            # is not installed on this machine).
            import ctypes
            PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
            STILL_ACTIVE = 259
            k32 = ctypes.windll.kernel32
            h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
            if not h:
                # ERROR_ACCESS_DENIED (5) => the process exists, just not ours to query.
                return k32.GetLastError() == 5
            try:
                code = ctypes.c_ulong()
                if not k32.GetExitCodeProcess(h, ctypes.byref(code)):
                    return False
                return code.value == STILL_ACTIVE
            finally:
                k32.CloseHandle(h)
        try:
            os.kill(pid, 0)   # POSIX only: signal 0 is the standard harmless probe
            return True
        except ProcessLookupError:
            return False
        except PermissionError:
            return True   # exists, just not ours to signal
        except Exception:
            return False

    def _read_meta(self) -> dict:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _write_meta(self, tier: str) -> None:
        # platform.node() instead of os.uname().nodename — os.uname does not exist
        # on Windows; platform is the cross-OS equivalent.
        meta = {"pid": os.getpid(), "host": platform.node(),
                "started_at": iso_now(), "tier": tier}
        os.ftruncate(self._fd, 0)
        os.lseek(self._fd, 0, os.SEEK_SET)
        os.write(self._fd, json.dumps(meta).encode("utf-8"))
        os.fsync(self._fd)

    def acquire(self, tier: str = "tick", force: bool = False) -> tuple:
        """Return (ok, holder_meta_or_None). ok=False means a live run holds it."""
        OUTPUTS.mkdir(parents=True, exist_ok=True)
        self._fd = os.open(str(self.path), os.O_CREAT | os.O_RDWR, 0o644)
        try:
            import fcntl
            try:
                fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                self._flocked = True
                self._write_meta(tier)
                return True, None
            except (BlockingIOError, OSError) as e:
                # flock unsupported on this FS -> fall back to pure pidfile + PID-alive check.
                if getattr(e, "errno", None) in (getattr(__import__("errno"), "ENOTSUP", -1),
                                                 getattr(__import__("errno"), "EOPNOTSUPP", -1)):
                    return self._pidfile_fallback(tier, force)
                holder = self._read_meta()
                if force or not self._alive(int(holder.get("pid") or 0)):
                    # holder is provably dead (or forced): flock should already be free; retry once.
                    try:
                        fcntl.flock(self._fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                        self._flocked = True
                        self._write_meta(tier)
                        return True, None
                    except Exception:
                        return False, holder
                return False, holder
        except ImportError:
            return self._pidfile_fallback(tier, force)

    def _pidfile_fallback(self, tier: str, force: bool) -> tuple:
        holder = self._read_meta()
        pid = int(holder.get("pid") or 0)
        if holder and self._alive(pid) and not force:
            return False, holder
        # stale or absent -> take it.
        self._write_meta(tier)
        return True, None

    def release(self) -> None:
        # flock-UN + close ONLY — do NOT unlink. Unlinking after releasing the flock is
        # the classic flock+unlink race: between our UN and the unlink, proc B can flock
        # this same inode; the unlink then drops the path, proc C creates a NEW lock file
        # and flocks THAT — two concurrent holders. A persistent lock file is the standard
        # flock pattern: the kernel auto-releases the flock on close/death, and the file's
        # pidfile content still drives stale (dead-PID) detection on a re-acquire.
        if self._fd is None:
            return
        try:
            if self._flocked:
                import fcntl
                fcntl.flock(self._fd, fcntl.LOCK_UN)
        except Exception:
            pass
        try:
            os.close(self._fd)
        except Exception:
            pass
        self._fd = None
        self._flocked = False


# =========================================================================== #
# STATE — per-tier last-success persistence => run-if-overdue catch-up.
# =========================================================================== #
def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            mlog(event="state_corrupt", note="resetting heartbeat state file")
    # First-ever run: bootstrap so MEASURE + LINK fire now (cheap, builds the ledger), but
    # RECONCILE waits a full week and ACQUIRE waits its cadence (never a surprise 85-min job).
    now = iso_now()
    epoch = "1970-01-01T00:00:00+00:00"
    return {
        "created_at": now,
        "tiers": {
            "link":      {"last_success": epoch, "last_attempt": None, "last_status": None},
            "measure":   {"last_success": epoch, "last_attempt": None, "last_status": None},
            "acquire":   {"last_success": now,   "last_attempt": None, "last_status": None},
            "reconcile": {"last_success": now,   "last_attempt": None, "last_status": None},
        },
    }


def save_state(state: dict) -> None:
    state["last_tick"] = iso_now()
    tmp = STATE_FILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)   # atomic


def _parse(ts: str):
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        return datetime.fromtimestamp(0, timezone.utc)


def tier_age_s(state: dict, tier: str) -> float:
    last = state["tiers"].get(tier, {}).get("last_success")
    if not last:
        return 1e12
    return (datetime.now(timezone.utc) - _parse(last)).total_seconds()


def tier_due(state: dict, tier: str) -> bool:
    return tier_age_s(state, tier) >= CADENCE[tier]


# =========================================================================== #
# GUARDED RUNNER — process-group hard timeout (the hang guard). Output streams
# straight to a per-run log file (no pipe to drain => no deadlock).
# =========================================================================== #
def _kill_group(p) -> bool:
    """Kill the child's WHOLE process tree.

    POSIX: SIGTERM the process group, grace, then SIGKILL.
    Windows: no killpg/process groups worth the name — shell out to
    `taskkill /PID <pid> /T /F`, the OS-native tree kill (walks descendants and
    force-terminates the lot, including the snowflake driver child)."""
    if os.name == "nt":
        if p.poll() is not None:
            return False   # already dead — mirror the POSIX ProcessLookupError path
        try:
            subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"],
                           capture_output=True, timeout=30)
        except Exception:
            pass
        try:
            p.wait(timeout=10)
        except Exception:
            pass
        return True
    try:
        pgid = os.getpgid(p.pid)
    except ProcessLookupError:
        return False
    try:
        os.killpg(pgid, signal.SIGTERM)
    except ProcessLookupError:
        return True
    for _ in range(KILL_GRACE_S):
        if p.poll() is not None:
            break
        time.sleep(1)
    if p.poll() is None:
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            pass
    try:
        p.wait(timeout=10)
    except Exception:
        pass
    return True


def run_guarded(tier: str, cmd: list, cwd: Path, soft_s: int, hard_s: int,
                wh_timeout_s: int = None) -> dict:
    """Spawn cmd in its own process group; hard-kill the tree at hard_s; tee to a log.

    wh_timeout_s (MAJOR A): when set, force the warehouse STATEMENT_TIMEOUT_IN_SECONDS to
    it BEFORE spawning, so a query the subprocess orphans self-cancels server-side even if
    the local killpg already fired. Real warehouse tiers pass (hard_s + buffer); the
    OFFLINE selftest leaves it None so it never touches the warehouse."""
    global _CURRENT_CHILD
    ts = datetime.now().strftime("%Y%m%dT%H%M%S")
    logpath = OUTPUTS / f"_heartbeat_{tier}_{ts}.log"
    started = time.time()
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    with open(logpath, "a", buffering=1, encoding="utf-8") as lf:
        lf.write(f"START {time.strftime('%a %b %d %H:%M:%S %Z %Y')}  tier={tier}\n")
        lf.write(f"CMD {' '.join(cmd)}  (cwd={cwd})\n")
        if wh_timeout_s is not None:
            bk = _ensure_warehouse_timeout(int(wh_timeout_s))
            lf.write(f"[heartbeat] server-side STATEMENT_TIMEOUT backstop: "
                     f"{bk.get('action', bk.get('reason'))} -> {bk.get('set_to')}s "
                     f"on warehouse {bk.get('warehouse')}\n")
        lf.flush()
        # Own group/session so the hang guard can kill the whole tree. On Windows,
        # start_new_session is SILENTLY IGNORED — CREATE_NEW_PROCESS_GROUP is the
        # real equivalent there (and taskkill /T does the tree walk regardless).
        if os.name == "nt":
            spawn_kw = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}
        else:
            spawn_kw = {"start_new_session": True}      # new process group => killpg the whole tree
        try:
            p = subprocess.Popen(
                cmd, cwd=str(cwd),
                stdout=lf, stderr=subprocess.STDOUT,
                env=os.environ.copy(),
                **spawn_kw,
            )
        except Exception as e:
            return {"tier": tier, "status": "spawn_error", "rc": None, "dur_s": 0,
                    "log": str(logpath), "note": str(e)[:200]}
        _CURRENT_CHILD = p
        softed = False
        while True:
            rc = p.poll()
            if rc is not None:
                break
            el = time.time() - started
            if not softed and el >= soft_s:
                softed = True
                lf.write(f"[heartbeat] soft timeout {soft_s}s — still running "
                         f"(connect-all geo-step can sit quiet); hard kill at {hard_s}s\n")
                lf.flush()
                mlog(event="soft_timeout", tier=tier, elapsed_s=int(el), hard_s=hard_s)
            if el >= hard_s:
                lf.write(f"[heartbeat] HARD TIMEOUT {hard_s}s — killing process group "
                         f"(SIGTERM->SIGKILL)\n")
                lf.flush()
                _kill_group(p)
                _CURRENT_CHILD = None
                return {"tier": tier, "status": "timeout_killed", "rc": p.poll(),
                        "dur_s": int(time.time() - started), "log": str(logpath),
                        "note": f"hard timeout {hard_s}s"}
            time.sleep(POLL_S)
        _CURRENT_CHILD = None
        dur = int(time.time() - started)
        tail = _tail(logpath, 1)
        return {"tier": tier, "status": "ok" if rc == 0 else "failed", "rc": rc,
                "dur_s": dur, "log": str(logpath), "note": tail}


def pour_running() -> str:
    """Return the command line of a live onboard.py pour, or '' when none is running.

    The heavy tiers (ACQUIRE re-ingest, RECONCILE full rebuild) must never contend
    with a live pour — shared onboarding_log.json, warehouse contention, and a
    mid-chunk collision is exactly what wiped NPPES. On Windows `tasklist` only
    shows python.exe, so the command line needs a Win32_Process CIM query; POSIX
    gets pgrep -f. Fail-open to '' on probe error (budget + lock guards still
    apply) — a broken probe must not brick the heartbeat forever."""
    try:
        if os.name == "nt":
            ps = ("Get-CimInstance Win32_Process -Filter \"Name LIKE 'python%'\" | "
                  "Where-Object { $_.CommandLine -match 'onboard\\.py' } | "
                  "Select-Object -First 1 -ExpandProperty CommandLine")
            r = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                capture_output=True, text=True, timeout=60)
            return (r.stdout or "").strip()
        r = subprocess.run(["pgrep", "-fal", "onboard.py"],
                           capture_output=True, text=True, timeout=30)
        lines = (r.stdout or "").strip().splitlines()
        return lines[0] if lines else ""
    except Exception:
        return ""


def _skip_if_pour(tier: str) -> dict:
    """Shared guard for the heavy tiers: skip with a logged reason when a pour is live."""
    pour = pour_running()
    if pour:
        mlog(event="pour_detected", tier=tier, cmdline=pour[:200])
        return {"tier": tier, "status": "skipped_pour",
                "note": f"live onboard.py pour detected — refusing to contend: {pour[:160]}"}
    return {}


def _tail(path: Path, n: int) -> str:
    try:
        lines = [l for l in path.read_text(encoding="utf-8", errors="replace").splitlines() if l.strip()]
        return " | ".join(lines[-n:])[:300]
    except Exception:
        return ""


# =========================================================================== #
# TIERS — each returns a result dict. dry_run => describe only (no spawn, no write).
# =========================================================================== #
def _planned(tier: str, cmd: list, cwd: Path, note: str = "") -> dict:
    return {"tier": tier, "status": "plan", "cmd": " ".join(cmd), "cwd": str(cwd), "note": note}


def tier_link(run: bool, budget: dict) -> dict:
    cmd = [PY, "-m", "connect", "connect-changed", "--scope", "spine"]
    if not run:
        return _planned("link", cmd + ["  (dry-run adds --dry-run)"], REPO,
                        "reslice only spine tables whose content-key moved (no-op if none)")
    ok, why = tier_budget_ok("link", budget)
    if not ok:
        return {"tier": "link", "status": "skipped_budget", "note": why}
    pol = TIER_POLICY["link"]
    return run_guarded("link", cmd, REPO, pol["soft"], pol["hard"],
                       wh_timeout_s=pol["hard"] + STMT_TIMEOUT_BUFFER_S)


def tier_measure(run: bool, budget: dict) -> dict:
    cmd = [PY, str(BUILD_LEDGER), "--apply"]
    if not run:
        return _planned("measure", [PY, str(BUILD_LEDGER), "--apply"], REPO,
                        "re-derive DATA_THROUGH + (re)create V_SOURCE_FRESHNESS")
    ok, why = tier_budget_ok("measure", budget)
    if not ok:
        return {"tier": "measure", "status": "skipped_budget", "note": why}
    pol = TIER_POLICY["measure"]
    return run_guarded("measure", cmd, REPO, pol["soft"], pol["hard"],
                       wh_timeout_s=pol["hard"] + STMT_TIMEOUT_BUFFER_S)


def tier_reconcile(run: bool, budget: dict) -> dict:
    cmd = [PY, "-m", "connect", "all"]
    if not run:
        return _planned("reconcile", cmd, REPO,
                        "FULL rebuild fingerprint->discover->spine->explore + reseed twins (~85min, geo HANG-RISK)")
    skip = _skip_if_pour("reconcile")
    if skip:
        return skip
    ok, why = tier_budget_ok("reconcile", budget)
    if not ok:
        return {"tier": "reconcile", "status": "skipped_budget", "note": why}
    pol = TIER_POLICY["reconcile"]
    res = run_guarded("reconcile", cmd, REPO, pol["soft"], pol["hard"],
                      wh_timeout_s=pol["hard"] + STMT_TIMEOUT_BUFFER_S)
    # connect all's tail reseed is fail-safe wrapped: exit 0 can still leave twins stale.
    # Verify SPINE_KEYSET_LIVE is populated rather than trusting the exit code alone.
    if res.get("status") == "ok":
        n = _with_timeout(lambda: _scalar('SELECT COUNT(*) FROM LIBRARY_META."CONNECT".SPINE_KEYSET_LIVE'),
                          120, None)
        if not n:
            res["status"] = "ok_twins_unverified"
            res["note"] = f"rebuild exit 0 but SPINE_KEYSET_LIVE count={n} — reseed may have been skipped"
    return res


def _scalar(sql: str):
    def _inner():
        conn = _snow_connect()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            r = cur.fetchone()
            return r[0] if r else None
        finally:
            conn.close()
    return _inner()


def _load_recipes() -> dict:
    try:
        doc = json.loads(RECIPES_FILE.read_text(encoding="utf-8"))
        return doc.get("recipes", {})
    except Exception as e:
        mlog(event="recipes_missing", note=str(e)[:160])
        return {}


def _expand_tokens(args: list) -> list:
    sub = {
        "{TODAY}": date.today().isoformat(),
        "{TOMORROW}": (date.today() + timedelta(days=1)).isoformat(),
        "{YESTERDAY}": (date.today() - timedelta(days=1)).isoformat(),
    }
    out = []
    for a in args:
        for k, v in sub.items():
            a = a.replace(k, v)
        out.append(a)
    return out


def _acquire_candidates(limit: int) -> list:
    """DUE/OVERDUE sources whose cadence makes a newer vintage plausible. Read-only.
    Returns [] (not an error) if the ledger view is missing — that just means MEASURE
    has not run yet."""
    cad = ",".join(f"'{c}'" for c in ACQUIRE_CADENCES)
    sql = (f"SELECT SOURCE_ID, LANDING_FQN, CADENCE_BUCKET, FRESHNESS_STATE, DATA_AGE_DAYS "
           f"FROM {FRESHNESS_VIEW} "
           f"WHERE FRESHNESS_STATE IN ('due','overdue') AND CADENCE_BUCKET IN ({cad}) "
           f"ORDER BY CASE FRESHNESS_STATE WHEN 'overdue' THEN 0 ELSE 1 END, "
           f"DATA_AGE_DAYS DESC NULLS LAST LIMIT {int(limit)}")
    def _inner():
        conn = _snow_connect()
        try:
            cur = conn.cursor()
            cur.execute(sql)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]
        finally:
            conn.close()
    return _with_timeout(_inner, 120, [])


def tier_acquire(run: bool, budget: dict, max_sources: int, optin: bool) -> dict:
    """The riskiest tier: re-ingest DUE/OVERDUE sources. OPT-IN + registry-gated +
    GREEN-only + bounded + per-source budget recheck + SHA-skip (in the loaders)."""
    if not optin:
        return {"tier": "acquire", "status": "disabled",
                "note": "ACQUIRE is opt-in — pass --acquire-optin (unattended scheduler never enables it)"}
    skip = _skip_if_pour("acquire")
    if skip:
        return skip
    max_sources = max(1, min(int(max_sources), ACQUIRE_MAX_CAP))
    recipes = _load_recipes()
    cands = _acquire_candidates(max_sources * 4)
    if not cands:
        return {"tier": "acquire", "status": "noop",
                "note": "no due/overdue sources in the actionable cadences (or ledger not built yet)"}

    attempted, results, skipped = 0, [], []
    for c in cands:
        if attempted >= max_sources:
            break
        sid = c["SOURCE_ID"]
        rec = recipes.get(sid)
        if not rec or not rec.get("enabled"):
            skipped.append({"source_id": sid, "why": "no enabled recipe (needs a human in acquire_recipes.json)"})
            continue
        # token-expanded command, resolved against the repo
        cwd = LIB if rec.get("cwd") == "lib" else REPO
        raw = rec.get("cmd", [])
        argv = _expand_tokens(raw)
        cmd = [PY, str((REPO / argv[0]).resolve())] + argv[1:] if argv and argv[0].endswith(".py") \
            else [PY] + argv
        cost = float(rec.get("cost_estimate_cr", 0.5))

        if not run:
            results.append(_planned("acquire", cmd, cwd, f"{sid} ({c['FRESHNESS_STATE']}, est {cost}cr)"))
            attempted += 1
            continue

        # RE-CHECK budget before each source (free SHOW); abort the loop if headroom drops.
        b = read_budget()
        ok, why = tier_budget_ok("acquire", b)
        if not ok or b["spendable"] < ACQUIRE_RECHECK_FLOOR:
            mlog(event="acquire_abort", source=sid, reason=why, spendable=b.get("spendable"))
            skipped.append({"source_id": sid, "why": f"budget floor hit ({why})"})
            break
        if b["spendable"] < cost * 2:
            skipped.append({"source_id": sid, "why": f"spendable {b['spendable']} < 2x est {cost}"})
            continue

        pol = TIER_POLICY["acquire"]
        r = run_guarded("acquire", cmd, cwd, pol["soft"], pol["hard"],
                        wh_timeout_s=pol["hard"] + STMT_TIMEOUT_BUFFER_S)
        r["source_id"] = sid
        results.append(r)
        attempted += 1

    status = "plan" if not run else ("ok" if results and all(
        x.get("status") in ("ok", "plan") for x in results) else "partial")
    if run and not results:
        status = "noop"
    return {"tier": "acquire", "status": status, "attempted": attempted,
            "results": results, "skipped": skipped}


TIER_FN = {"link": tier_link, "measure": tier_measure, "reconcile": tier_reconcile}


# =========================================================================== #
# PLANNER — which DUE tiers to run, in order. RECONCILE subsumes LINK and defers
# ACQUIRE (never stack two heavy spenders on a tight cap).
# =========================================================================== #
def plan_tiers(state: dict, acquire_optin: bool) -> list:
    due = [t for t in ("reconcile", "acquire", "link", "measure") if tier_due(state, t)]
    if "acquire" in due and not acquire_optin:
        due.remove("acquire")
    if "reconcile" in due:
        return ["reconcile", "measure"]            # weekly path; link is subsumed, acquire deferred
    plan = []
    if "acquire" in due:
        plan.append("acquire")                     # acquire self-bootstraps the ledger view if missing
    if "link" in due:
        plan.append("link")
    if "measure" in due:
        plan.append("measure")                     # trailing measure reflects any newly-acquired recency
    return plan


# =========================================================================== #
# DRIVERS
# =========================================================================== #
def _advance(state: dict, tier: str, status: str) -> None:
    rec = state["tiers"].setdefault(tier, {})
    rec["last_attempt"] = iso_now()
    rec["last_status"] = status
    if status in ("ok", "ok_twins_unverified", "noop"):
        rec["last_success"] = iso_now()
        if tier == "reconcile":                    # a full rebuild also satisfies LINK
            link = state["tiers"].setdefault("link", {})
            link["last_success"] = iso_now()


def run_tick(args) -> int:
    global _LOCK
    budget = read_budget()
    mlog(event="tick_start", mode=("run" if args.run else "dry-run"),
         band=budget.get("band"), spendable=budget.get("spendable"),
         used=budget.get("used"), quota=budget.get("quota"),
         budget_ok=budget.get("ok"), reason=budget.get("reason", ""))

    # PAT calendar gate (Wave 7.1) — zero-network: decodes the token's own JWT exp
    # locally. A dying PAT doesn't stop the tick (read paths keep working right up
    # to expiry), but it must be LOUD in the log every hour so it's impossible to
    # miss before the token dies mid-week. Never logs the token itself.
    try:
        if str(REPO) not in sys.path:
            sys.path.insert(0, str(REPO))
        from loadkit.preflight import live_pat_expiry, pat_expiry_check
        chk = pat_expiry_check(live_pat_expiry(), datetime.now(timezone.utc))
        if not chk.ok or chk.warn:
            mlog(event="pat_expiry", level=("BLOCK" if not chk.ok else "WARN"), note=chk.detail)
    except Exception:
        pass   # advisory only — a broken import must never stop the heartbeat

    if budget.get("band") == "RED" and args.run and not args.tier:
        # Clean no-op: in RED every tier's band gate fails (link/measure are GREEN/YELLOW,
        # acquire/reconcile are GREEN-only), so a full --run tick can do nothing that spins
        # a warehouse. Log ONCE and return — don't churn the planner + per-tier budget
        # skips. (A deliberate `--tier X --run` still proceeds; its own gate handles it.)
        mlog(event="tick_skip_red", note="spendable below the YELLOW floor; no tier may spin a warehouse in RED")
        return 0

    state = load_state()
    if args.tier:
        plan = [args.tier]
    else:
        plan = plan_tiers(state, args.acquire_optin)
    mlog(event="plan", tiers=",".join(plan) or "none")

    if not plan:
        mlog(event="tick_done", note="nothing due")
        return 0

    # Lock only for real runs (a dry-run must be safe to inspect alongside a live run).
    if args.run:
        _LOCK = HeartbeatLock(LOCK_FILE)
        ok, holder = _LOCK.acquire(tier=",".join(plan), force=args.force_unlock)
        if not ok:
            mlog(event="lock_held", holder_pid=(holder or {}).get("pid"),
                 holder_host=(holder or {}).get("host"), holder_since=(holder or {}).get("started_at"),
                 note="another heartbeat/connect run is active — exiting no-op")
            return 0

    try:
        for tier in plan:
            budget = read_budget()                 # fresh, free, per-tier
            if tier == "acquire":
                res = tier_acquire(args.run, budget, args.max_sources, args.acquire_optin)
            else:
                res = TIER_FN[tier](args.run, budget)
            _log_result(res, budget)
            if args.run:
                _advance(state, tier, res.get("status", "unknown"))
        if args.run:
            save_state(state)
    finally:
        if _LOCK:
            _LOCK.release()

    mlog(event="tick_done")
    return 0


def _log_result(res: dict, budget: dict) -> None:
    tier = res.get("tier")
    if res.get("status") == "plan":
        mlog(event="would_run", tier=tier, cmd=res.get("cmd"), note=res.get("note", ""))
        return
    if tier == "acquire":
        mlog(event="acquire_result", status=res.get("status"), attempted=res.get("attempted", 0),
             skipped=len(res.get("skipped", [])))
        for r in res.get("results", []):
            if r.get("status") == "plan":
                mlog(event="acquire_would_run", source=r.get("note"), cmd=r.get("cmd"))
            else:
                mlog(event="acquire_ran", source=r.get("source_id"), status=r.get("status"),
                     dur_s=r.get("dur_s"), log=r.get("log"), note=r.get("note", ""))
        for s in res.get("skipped", []):
            mlog(event="acquire_skip", source=s.get("source_id"), why=s.get("why"))
        return
    mlog(event="tier_result", tier=tier, status=res.get("status"), rc=res.get("rc"),
         dur_s=res.get("dur_s"), band=budget.get("band"), spendable=budget.get("spendable"),
         log=res.get("log", ""), note=res.get("note", ""))


def print_status() -> int:
    budget = read_budget()
    print("=" * 72)
    print("  RIPPLE HEARTBEAT — status (read-only)")
    print("=" * 72)
    if budget.get("ok"):
        print(f"  budget: band={budget['band']} spendable={budget['spendable']}cr "
              f"(used {budget['used']}/{budget['quota']}, SUSPEND floor {budget['suspend_floor']})")
    else:
        print(f"  budget: UNAVAILABLE ({budget.get('reason')}) -> treated as RED")
    # lock holder?
    lk = HeartbeatLock(LOCK_FILE)
    meta = lk._read_meta() if LOCK_FILE.exists() else {}
    if meta:
        alive = HeartbeatLock._alive(int(meta.get("pid") or 0))
        print(f"  lock: pid={meta.get('pid')} host={meta.get('host')} since={meta.get('started_at')} "
              f"alive={alive}{'  (STALE)' if not alive else ''}")
    else:
        print("  lock: free")
    # ledger view present?
    present = _with_timeout(
        lambda: _scalar("SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.SOURCE_FRESHNESS"), 60, None)
    print(f"  ledger: SOURCE_FRESHNESS rows={present if present is not None else 'MISSING (run MEASURE --apply)'}")
    state = load_state()
    print("  tiers:")
    for t in ("acquire", "link", "measure", "reconcile"):
        age = tier_age_s(state, t)
        due = "DUE" if tier_due(state, t) else f"in {int((CADENCE[t]-age)/3600)}h"
        last = state["tiers"].get(t, {}).get("last_success")
        print(f"    {t:<10} last_success={last}  cadence={CADENCE[t]//3600}h  -> {due}")
    print("=" * 72)
    return 0


# =========================================================================== #
# SELFTEST — OFFLINE proof of the two hardest guards. Zero warehouse, zero credits.
# =========================================================================== #
def selftest() -> int:
    print("== heartbeat selftest (offline, 0 credits) ==")
    ok = True

    # 1) process-group hard-timeout kill: a child that sleeps 600s must die at ~2s, and so
    #    must its grandchild (proving killpg reaches the whole tree, not just the direct child).
    print("[1] process-group hard-timeout kill ...")
    grandchild_marker = OUTPUTS / "_heartbeat_selftest_grandchild.pid"
    try:
        grandchild_marker.unlink()
    except Exception:
        pass
    # child spawns a grandchild that writes its pid, then both sleep 600s.
    pyprog = (
        "import os,sys,time,subprocess;"
        f"open(r'{grandchild_marker}','w').close();"
        "g=subprocess.Popen([sys.executable,'-c','import time;time.sleep(600)']);"
        f"open(r'{grandchild_marker}','w').write(str(g.pid));"
        "time.sleep(600)"
    )
    t0 = time.time()
    res = run_guarded("selftest", [PY, "-c", pyprog], REPO, soft_s=1, hard_s=2)
    el = time.time() - t0
    gpid = None
    try:
        gpid = int(grandchild_marker.read_text().strip() or 0)
    except Exception:
        pass
    time.sleep(1)
    g_alive = HeartbeatLock._alive(gpid) if gpid else False
    killed = res.get("status") == "timeout_killed" and el < 30 and not g_alive
    print(f"    -> status={res.get('status')} elapsed={el:.1f}s grandchild_pid={gpid} "
          f"grandchild_alive={g_alive}  {'PASS' if killed else 'FAIL'}")
    ok = ok and killed
    try:
        grandchild_marker.unlink()
    except Exception:
        pass

    # 2) lock mutual-exclusion + stale (dead-PID) detection.
    print("[2] lock: hold, contend, stale-reclaim ...")
    p = OUTPUTS / "_heartbeat_selftest.lock"
    try:
        p.unlink()
    except Exception:
        pass
    a = HeartbeatLock(p)
    ok_a, _ = a.acquire("A")
    b = HeartbeatLock(p)
    ok_b, holder = b.acquire("B")              # must FAIL — A holds it
    contend_pass = ok_a and not ok_b and holder is not None
    a.release()
    # stale: write a dead PID into the file, then a fresh acquire must reclaim it.
    # Spawn-and-reap our OWN child to get a GUARANTEED-dead PID — a fixed constant
    # like 2**22 can be a live PID on Windows (PIDs there are large and recycled),
    # which would make this check flaky-fail on somebody else's process.
    dead = subprocess.Popen([PY, "-c", "pass"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    dead.wait(timeout=60)
    p.write_text(json.dumps({"pid": dead.pid, "host": "x", "started_at": iso_now(), "tier": "dead"}))
    c = HeartbeatLock(p)
    ok_c, _ = c.acquire("C", force=False)
    c.release()
    try:
        p.unlink()
    except Exception:
        pass
    print(f"    -> hold={ok_a} contend_blocked={not ok_b} stale_reclaimed={ok_c}  "
          f"{'PASS' if (contend_pass and ok_c) else 'FAIL'}")
    ok = ok and contend_pass and ok_c

    # 3) budget band math (pure, offline).
    print("[3] budget band thresholds ...")
    band_pass = (band_for(6) == "GREEN" and band_for(3) == "YELLOW" and band_for(1) == "RED")
    print(f"    -> GREEN@6={band_for(6)} YELLOW@3={band_for(3)} RED@1={band_for(1)}  "
          f"{'PASS' if band_pass else 'FAIL'}")
    ok = ok and band_pass

    print(f"== selftest {'PASS' if ok else 'FAIL'} ==")
    return 0 if ok else 1


# =========================================================================== #
# CLI
# =========================================================================== #
def _install_signal_handlers() -> None:
    def _handler(signum, frame):
        if _CURRENT_CHILD is not None:
            _kill_group(_CURRENT_CHILD)
        if _LOCK is not None:
            _LOCK.release()
        os._exit(143)
    for s in (signal.SIGTERM, signal.SIGINT):
        try:
            signal.signal(s, _handler)
        except Exception:
            pass


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="heartbeat.py",
                                description="The Library heartbeat (preview by default; --run to execute).")
    p.add_argument("--run", action="store_true", help="EXECUTE due tiers (default is dry-run preview).")
    p.add_argument("--tier", choices=["link", "measure", "acquire", "reconcile"],
                   help="Force ONE tier (ignores cadence; still budget-gated).")
    p.add_argument("--acquire-optin", action="store_true",
                   help="Enable the ACQUIRE re-ingest tier (off by default, even with --run).")
    p.add_argument("--max-sources", type=int, default=3,
                   help=f"ACQUIRE: max sources to re-ingest per run (cap {ACQUIRE_MAX_CAP}).")
    p.add_argument("--force-unlock", action="store_true",
                   help="Reclaim the lock from a provably-dead holder (use only when sure).")
    p.add_argument("--status", action="store_true", help="Print last-success + budget + ledger state, then exit.")
    p.add_argument("--selftest", action="store_true", help="Offline proof of lock + process-group kill (0 credits).")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    _install_signal_handlers()
    if args.selftest:
        return selftest()
    if args.status:
        return print_status()
    return run_tick(args)


if __name__ == "__main__":
    sys.exit(main())
