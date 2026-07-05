"""The Ripple Control Panel server — one local page to see the Library's health and
push real refreshes, with the whole ingestion process visible and auditable.

    python3 ripple.py panel               # serves http://127.0.0.1:8899 (auto-opens)

Design rules (inherited from the repo):
  * Reads go through ripple.common.connect() -> COMPUTE_WH. Never RIPPLE_WH (pour lane),
    never SERVE_WH (5cr/month monitor would suspend it under load).
  * Refresh is HONEST: every button maps to a real command that is shown before it runs.
    No per-source path exists for most sources -- the UI says so instead of pretending.
  * Jobs run exactly like heartbeat runs them: subprocess in its own process group,
    output straight to a log file (no pipe deadlock), hard timeout -> kill the group.
  * One job at a time. Pre-flight = budget band + pour detection + heartbeat lock.
  * The browser never supplies a command. It supplies an ACTION; the server builds the
    argv from its own resolver and validates every user-editable value by regex.
"""
from __future__ import annotations

import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
import uuid
import webbrowser
from datetime import date, datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from . import common

REPO = common.REPO
LIB = common.LIB
SCRIPTS = REPO / "scripts"
OUTPUTS = REPO / "outputs"
PAGE_PATH = Path(__file__).with_name("panel_page.html")
JOBS_JSONL = OUTPUTS / "_panel_jobs.jsonl"
RECIPES_PATH = SCRIPTS / "acquire_recipes.json"
HB_STATE = OUTPUTS / "_heartbeat_state.json"
HB_LOCK = OUTPUTS / "_heartbeat.lock"

DEFAULT_PORT = 8899

# ------------------------------------------------------------------ Snowflake reads
# A small lazy connection POOL, not one shared connection: ThreadingHTTPServer gives
# each request its own thread, and a page load fires ~9 reads (overview's 6 + sources +
# runs) plus 2s job polling. One shared connection would serialize all of them behind a
# single lock, so a cold-warehouse read (~seconds) would freeze the whole panel. The pool
# lets independent reads run concurrently; each read borrows a connection and returns it.
_POOL_MAX = 5
_pool: list = []           # idle connections
_pool_lock = threading.Lock()
_pool_sem = threading.BoundedSemaphore(_POOL_MAX)   # caps total live connections


def _is_conn_error(e: Exception) -> bool:
    s = str(e).lower()
    return any(t in s for t in ("connection", "socket", "expired", "not connected", "terminated"))


def _error_public(e: Exception) -> dict:
    """Translate an exception into what the page shows. Connection/auth failures get a
    `kind` + a plain one-liner so the UI can raise ONE banner with the fix, instead of
    toasting the same raw DatabaseError once per request."""
    detail = f"{type(e).__name__}: {str(e)[:400]}"
    low = str(e).lower()
    if "token is expired" in low or "token expired" in low:
        return {"error": "Snowflake access token expired", "kind": "token_expired", "detail": detail}
    if "password" in low or "authentication" in low or "not authorized" in low or "250001" in low:
        return {"error": "Snowflake didn't accept the login", "kind": "auth", "detail": detail}
    if _is_conn_error(e) or "failed to connect" in low or "timed out" in low:
        return {"error": "Couldn't reach Snowflake", "kind": "network", "detail": detail}
    return {"error": detail}


def _fresh_secret() -> str | None:
    """Re-read library-onboarding/.env at connect time. config.settings freezes the env
    at import, so a new PAT pasted in after an expiry would otherwise need a panel
    restart -- this makes 'paste token, hit Try again' just work."""
    try:
        from dotenv import dotenv_values
        vals = dotenv_values(LIB / ".env")
        return (vals.get("SNOWFLAKE_PAT") or vals.get("SNOWFLAKE_PASSWORD") or "").strip() or None
    except Exception:
        return None


def _acquire():
    _pool_sem.acquire()
    try:
        with _pool_lock:
            if _pool:
                return _pool.pop()
        return common.connect(pat=_fresh_secret())
    except BaseException:
        _pool_sem.release()   # never leak a permit if connect() blows up
        raise


def _release(conn, broken: bool = False):
    if broken:
        try:
            conn.close()
        except Exception:
            pass
        _pool_sem.release()
        return
    with _pool_lock:
        _pool.append(conn)
    _pool_sem.release()


def _pool_drain_idle():
    """Close and discard every IDLE pooled connection. Used after a dead-connection error:
    an overnight idle expiry kills the WHOLE pool at once, so the next borrow would just
    hand out another corpse -> retry every read all morning. Drain them so the retry (and
    every read after it) reconnects fresh. In-use connections aren't in _pool; when their
    borrower returns them they'll fail their own next borrow and self-heal the same way."""
    with _pool_lock:
        conns, _pool[:] = list(_pool), []
    for c in conns:
        try:
            c.close()
        except Exception:
            pass


def qd(sql: str, params: tuple = ()):  # -> list[dict], retry-once on a dead connection
    conn = _acquire()
    try:
        rows = common.dicts(conn, sql, params)
        _release(conn)
        return rows
    except Exception as e:
        _release(conn, broken=True)   # this connection may be dead -> don't reuse it
        if not _is_conn_error(e):
            raise
        _pool_drain_idle()            # the rest of the pool is probably dead too
    # retry exactly once on a guaranteed-fresh connection (pool now empty -> _acquire connects)
    conn = _acquire()
    try:
        rows = common.dicts(conn, sql, params)
        _release(conn)
        return rows
    except Exception:
        _release(conn, broken=True)
        raise


def _pool_close_all():
    _pool_drain_idle()


def _json_default(o):
    if isinstance(o, (datetime, date)):
        return o.isoformat()
    try:  # Decimal and friends
        f = float(o)
        return int(f) if f.is_integer() else f
    except Exception:
        return str(o)


# ------------------------------------------------------------------ tiny TTL cache
_cache: dict = {}
_cache_lock = threading.Lock()
_cache_gen = 0  # bumped by cache_clear so in-flight reads can't re-cache pre-clear data


def cached(key: str, ttl_s: int, fn):
    now = time.time()
    with _cache_lock:
        gen = _cache_gen
        hit = _cache.get(key)
        if hit and now - hit[0] < ttl_s:
            return hit[1]
    val = fn()
    with _cache_lock:
        if _cache_gen == gen:
            _cache[key] = (now, val)
    return val


def cache_clear(prefix: str = ""):
    global _cache_gen
    with _cache_lock:
        _cache_gen += 1
        for k in [k for k in _cache if k.startswith(prefix)]:
            _cache.pop(k, None)


# ------------------------------------------------------------------ heartbeat bridge
_hb_mod = None


def _heartbeat():
    """Import scripts/heartbeat.py once (it is a script, not a package module)."""
    global _hb_mod
    if _hb_mod is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location("_panel_heartbeat", SCRIPTS / "heartbeat.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _hb_mod = mod
    return _hb_mod


def budget(refresh: bool = False) -> dict:
    if refresh:
        cache_clear("budget")
    def _read():
        try:
            return _heartbeat().read_budget(timeout_s=45)
        except Exception as e:
            return {"ok": False, "reason": f"budget_read_error: {str(e)[:160]}",
                    "band": "RED", "spendable": 0.0}
    val = cached("budget", 600, _read)
    if not val.get("ok"):
        cache_clear("budget")  # never pin a failed read for the whole TTL
    return val


def _pid_alive(pid: int) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except (ProcessLookupError, ValueError, TypeError):
        return False
    except PermissionError:
        return True


def heartbeat_status() -> dict:
    out = {"state": {}, "lock": None, "last_tick": None}
    try:
        st = json.loads(HB_STATE.read_text())
        out["last_tick"] = st.get("last_tick")
        out["state"] = {k: v for k, v in st.get("tiers", st).items() if isinstance(v, dict)}
    except Exception:
        pass
    # heartbeat's release() deliberately never unlinks the lock file, so the pid in it is
    # usually a DEAD past tick (and macOS reuses pids). Probe the real primitive: if a
    # non-blocking shared flock succeeds, nobody holds the lock — whatever the pid says.
    try:
        lk = json.loads(HB_LOCK.read_text())
        held = False
        try:
            import fcntl
            with open(HB_LOCK, "rb") as fd:
                try:
                    fcntl.flock(fd.fileno(), fcntl.LOCK_SH | fcntl.LOCK_NB)
                    fcntl.flock(fd.fileno(), fcntl.LOCK_UN)
                except OSError:
                    held = True
        except ImportError:  # non-POSIX fallback: pid probe with the 0-guard
            pid = lk.get("pid") or 0
            held = pid > 0 and _pid_alive(pid)
        if held:
            out["lock"] = lk  # a live heartbeat tick is running right now
    except Exception:
        pass
    return out


# ------------------------------------------------------------------ refreshability resolver
_SID_RE = re.compile(r"^(?:SID|SOURCE_ID)\s*=\s*['\"]([a-z0-9_]+)['\"]", re.M)
# capture the flag AND the rest of its add_argument(...) call so we can read type=/default=
_FLAG_RE = re.compile(r"add_argument\(\s*['\"](--[a-z][a-z0-9\-]*)['\"]([^)]*)\)")
_WINPATH_RE = re.compile(r"[cC]:[/\\]")
_REPLACE_RE = re.compile(r"TRUNCATE TABLE|overwrite\s*=\s*True|overwrite_first|overwrite\s*=\s*first_write")

# per-kind value validators. A flag declared type=int (e.g. storm_events --start=YEAR) is a
# YEAR, not a YYYY-MM-DD date -- validating it as a date would accept a value the loader crashes on.
FLAG_VALIDATORS = {
    "date": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "year": re.compile(r"^\d{4}$"),
    "float": re.compile(r"^\d{1,4}(\.\d{1,3})?$"),
    "int": re.compile(r"^\d{1,9}$"),
}


def _flag_kind(flag: str, arg_src: str) -> str:
    """Classify a loader flag by how its value must be validated + labelled."""
    if "type=int" in arg_src.replace(" ", ""):
        return "year" if flag in ("--start", "--end", "--year", "--since", "--until") else "int"
    if "type=float" in arg_src.replace(" ", ""):
        return "float"
    if flag in ("--min-mag",):
        return "float"
    if flag in ("--start", "--end", "--since", "--until"):
        return "date"
    if flag in ("--year", "--years", "--month", "--months"):
        return "year"
    return "int"


# flags the panel is willing to let Chris edit (whitelist); everything else is ignored
EDITABLE_FLAGS = {"--start", "--end", "--since", "--until", "--min-mag", "--year", "--days"}


def scan_loaders() -> dict:
    """Live scan of scripts/*.py for SID-pinned deterministic loaders. Never a
    hardcoded list -- new loaders appear here on the next rescan."""
    found: dict = {}
    for py in sorted(SCRIPTS.glob("*.py")):
        try:
            text = py.read_text(errors="replace")
        except Exception:
            continue
        m = _SID_RE.search(text)
        if not m:
            continue
        sid = m.group(1)
        date_flags, flag_kinds = [], {}
        for flag, arg_src in _FLAG_RE.findall(text):
            if flag not in EDITABLE_FLAGS:
                continue
            date_flags.append(flag)
            flag_kinds[flag] = _flag_kind(flag, arg_src)
        has_run = '"--run"' in text or "'--run'" in text
        replace = bool(_REPLACE_RE.search(text))
        append_only = ("overwrite=False" in text) and not replace
        found[sid] = {
            "script": f"scripts/{py.name}",
            "windows_broken": bool(_WINPATH_RE.search(text)),
            "date_flags": sorted(set(date_flags)),
            "flag_kinds": flag_kinds,
            "write_mode": "append" if append_only else ("replace" if replace else "unknown"),
            "has_run_flag": has_run,
        }
    return found


def load_recipes() -> dict:
    try:
        data = json.loads(RECIPES_PATH.read_text())
        return data.get("recipes", {})
    except Exception:
        return {}


def refresh_plan_for(sid: str, url: str = "") -> dict:
    """Resolve what 'refresh' means for one source. Tiers, most to least direct:
    recipe / recipe_disabled / script (append-only) / script_replace (manual, footgun) /
    script_broken / llm / none.

    A recipe is a HUMAN-VETTED command (someone confirmed it does a full, safe reload), so
    even a replace-mode loader is fine THROUGH a recipe. A raw script that replaces the whole
    landing table is NOT offered a one-click button: run with anything but its exact full
    window and it silently truncates the table to that window (usaspending's default is a
    1-DAY probe). Those get 'script_replace' -> shown as manual-only with the reason."""
    recipes = cached("recipes", 60, load_recipes)
    loaders = cached("loaders", 60, scan_loaders)
    r = recipes.get(sid)
    l = loaders.get(sid)
    if r and r.get("enabled"):
        return {"tier": "recipe", "cmd_preview": r.get("cmd", []), "cwd": r.get("cwd", "repo"),
                "cost_estimate_cr": r.get("cost_estimate_cr"), "note": r.get("note", ""),
                "loader": l or {}}
    if r:
        return {"tier": "recipe_disabled", "cmd_preview": r.get("cmd", []), "cwd": r.get("cwd", "repo"),
                "cost_estimate_cr": r.get("cost_estimate_cr"), "note": r.get("note", ""),
                "loader": l or {}}
    if l and l["windows_broken"]:
        return {"tier": "script_broken",
                "note": "this loader still has old Windows paths baked in -- needs a code fix before it can run",
                "loader": l}
    if l and l["write_mode"] == "append":
        return {"tier": "script", "note": "", "loader": l}
    if l:  # replace or unknown write mode -> a one-click run could truncate the table
        why = ("wipes and rewrites the whole table when it runs" if l["write_mode"] == "replace"
               else "couldn't be verified as add-only")
        return {"tier": "script_replace",
                "note": f"manual only: {l['script']} {why} -- a partial run would shrink the table. "
                        f"Run it from a terminal with the full date range, or save a vetted recipe.",
                "loader": l}
    if url:
        return {"tier": "llm",
                "note": "no saved loader script -- refreshing means the AI rebuilds it from scratch (costs API credits)",
                "loader": {}}
    return {"tier": "none", "note": "no loader script, no saved recipe, no URL on file -- nothing to refresh with", "loader": {}}


# ------------------------------------------------------------------ job manager
class Job:
    def __init__(self, action: str, label: str, cmd: list, cwd: Path, hard_s: int, meta: dict):
        self.id = uuid.uuid4().hex[:12]
        self.action = action
        self.label = label
        self.cmd = [str(c) for c in cmd]
        self.cwd = str(cwd)
        self.hard_s = hard_s
        self.meta = meta
        self.started_at = datetime.now(timezone.utc).isoformat()
        self.ended_at = None
        self.status = "running"
        self.rc = None
        self.log_path = str(OUTPUTS / f"_panel_job_{self.id}.log")
        self.proc = None
        self.cancel_requested = False

    def public(self) -> dict:
        return {k: getattr(self, k) for k in
                ("id", "action", "label", "cmd", "cwd", "hard_s", "meta",
                 "started_at", "ended_at", "status", "rc", "log_path")}


RUNNING_MARKER = OUTPUTS / "_panel_job_running.json"


class JobManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.current: Job | None = None

    # ---- orphan detection (job survived a server restart) -----------------
    @staticmethod
    def orphan() -> dict | None:
        """A prior server's job marker whose process group is still alive."""
        try:
            mk = json.loads(RUNNING_MARKER.read_text())
        except Exception:
            return None
        pgid = mk.get("pgid") or 0
        try:
            if pgid > 0:
                os.killpg(pgid, 0)
                return mk  # still alive
        except (ProcessLookupError, ValueError):
            pass
        except PermissionError:
            return mk
        try:
            RUNNING_MARKER.unlink()  # holder is dead -> stale marker, clear it
        except Exception:
            pass
        return None

    # ---- pre-flight ------------------------------------------------------
    def preflight(self, action: str, fresh: bool = False) -> dict:
        b = budget(refresh=fresh)
        pour = common.pour_running()
        hb = heartbeat_status()
        blockers = []
        if self.current and self.current.status == "running":
            blockers.append(f"another panel job is already running ({self.current.label})")
        orphan = self.orphan()
        if orphan and not (self.current and self.current.id == orphan.get("job_id")):
            blockers.append("a job from an earlier panel session is still running "
                            f"(pid {orphan.get('pid')}: {orphan.get('label')}) -- "
                            "wait for it to finish, or cancel it from the Jobs tab")
        if hb.get("lock"):
            blockers.append("the autopilot (scheduled background task) is running right now "
                            "(pid %s) -- wait a few minutes" % hb["lock"].get("pid"))
        if pour and action in ("acquire", "source", "onboard"):
            blockers.append("a batch of new sources is being onboarded right now -- "
                            "refreshing at the same time would clash with it")
        band = b.get("band", "RED")
        need = {"measure": ("GREEN", "YELLOW"), "acquire": ("GREEN",),
                "source": ("GREEN",), "onboard": ("GREEN",)}.get(action, ("GREEN",))
        if band not in need:
            blockers.append(f"the spending light is {band} and this needs {' or '.join(need)} -- "
                            f"{b.get('spendable', 0)} credits left")
        return {"budget": b, "pour_running": pour, "heartbeat": hb, "blockers": blockers}

    # ---- launch ----------------------------------------------------------
    def launch(self, action: str, label: str, cmd: list, cwd: Path, hard_s: int, meta: dict) -> dict:
        # fail fast under the lock, run the slow preflight I/O (budget/pgrep) outside it,
        # then re-check + spawn under the lock — so cancel() never stalls behind preflight.
        with self.lock:
            if self.current and self.current.status == "running":
                return {"error": f"another panel job is already running ({self.current.label})"}
        pf = self.preflight(action, fresh=True)  # live budget read at the moment of launch
        if pf["blockers"]:
            return {"error": "; ".join(pf["blockers"]), "preflight": pf}
        with self.lock:
            if self.current and self.current.status == "running":
                return {"error": f"another panel job is already running ({self.current.label})"}
            job = Job(action, label, cmd, cwd, hard_s, meta)
            env = dict(os.environ)
            # Same convention as the scheduled-task wrapper: unattended work goes to
            # COMPUTE_WH where the runner honors it (heartbeat does; standalone
            # loaders use their own .env warehouse, exactly as a manual run would).
            env.setdefault("RIPPLE_TASK_WAREHOUSE", "COMPUTE_WH")
            env.setdefault("RIPPLE_NO_OPEN", "1")
            try:
                logf = open(job.log_path, "ab")
                logf.write(("$ " + " ".join(job.cmd) + "\n").encode())
                logf.flush()
                job.proc = subprocess.Popen(
                    job.cmd, cwd=job.cwd, stdout=logf, stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL, start_new_session=True, env=env)
            except Exception as e:
                try:
                    logf.close()
                except Exception:
                    pass
                job.status, job.rc = "spawn_error", -1
                job.ended_at = datetime.now(timezone.utc).isoformat()
                self._record(job)
                return {"error": f"spawn failed: {e}", "job": job.public()}
            self.current = job
            try:  # marker lets the NEXT server session detect a still-running job
                RUNNING_MARKER.write_text(json.dumps({
                    "job_id": job.id, "pid": job.proc.pid, "pgid": os.getpgid(job.proc.pid),
                    "label": job.label, "cmd": job.cmd, "started_at": job.started_at}))
            except Exception:
                pass
            threading.Thread(target=self._watch, args=(job, logf), daemon=True).start()
            return {"job": job.public(), "preflight": pf}

    def _watch(self, job: Job, logf):
        # monotonic clock: an NTP step or (on Intel Macs) a lid-close can jump time.time()
        # past hard_s and falsely kill a healthy job
        t0 = time.monotonic()
        killed_for = None
        kill_attempts = 0
        last_kill = 0.0
        while True:
            rc = job.proc.poll()
            if rc is not None:
                break
            now = time.monotonic()
            if killed_for is None and job.cancel_requested:
                killed_for = "cancelled"
            elif killed_for is None and now - t0 > job.hard_s:
                killed_for = "timeout"
            if killed_for and now - last_kill > 20:
                if kill_attempts >= 4:  # unkillable (e.g. uninterruptible I/O) -> stop pretending
                    job.status = "kill_failed"
                    break
                self._kill_group(job, force=kill_attempts > 0)
                kill_attempts += 1
                last_kill = now
            time.sleep(2)
        job.rc = job.proc.poll()
        if job.status != "kill_failed":
            job.status = killed_for or ("ok" if job.rc == 0 else "failed")
        job.ended_at = datetime.now(timezone.utc).isoformat()
        try:
            logf.close()
        except Exception:
            pass
        try:
            RUNNING_MARKER.unlink()
        except Exception:
            pass
        self._record(job)
        cache_clear("")  # data changed -> drop every cached read

    @staticmethod
    def _kill_group(job: Job, force: bool = False):
        try:
            pgid = os.getpgid(job.proc.pid)
            os.killpg(pgid, signal.SIGKILL if force else signal.SIGTERM)
            if force:
                return
            for _ in range(15):
                if job.proc.poll() is not None:
                    return
                time.sleep(1)
            os.killpg(pgid, signal.SIGKILL)
        except Exception:
            pass

    @staticmethod
    def _record(job: Job):
        try:
            OUTPUTS.mkdir(exist_ok=True)
            with open(JOBS_JSONL, "a") as f:
                f.write(json.dumps(job.public()) + "\n")
        except Exception:
            pass

    # ---- introspection ---------------------------------------------------
    @staticmethod
    def _orphan_public(mk: dict) -> dict:
        """Present a previous-session orphan as a read-only 'running' job the UI can
        tail and cancel, without a Job object (this process never spawned it)."""
        return {"id": mk.get("job_id"), "action": mk.get("action", "orphan"),
                "label": (mk.get("label") or "job from previous session") + " (recovered)",
                "cmd": mk.get("cmd", []), "cwd": mk.get("cwd", ""), "hard_s": mk.get("hard_s", 0),
                "meta": {"orphan": True, "pid": mk.get("pid"), "pgid": mk.get("pgid")},
                "started_at": mk.get("started_at"), "ended_at": None, "status": "running",
                "rc": None, "log_path": str(OUTPUTS / f"_panel_job_{mk.get('job_id')}.log")}

    def cancel(self, job_id: str) -> dict:
        with self.lock:
            j = self.current
            if j and j.id == job_id:
                j.cancel_requested = True
                return {"ok": True}
        # not our job -> maybe an orphan from a previous session; kill it by pgid
        mk = self.orphan()
        if mk and mk.get("job_id") == job_id:
            pgid = mk.get("pgid") or 0
            try:
                if pgid > 0:
                    os.killpg(pgid, signal.SIGTERM)
                    return {"ok": True, "note": "told the old job to stop"}
            except ProcessLookupError:
                pass
            try:
                RUNNING_MARKER.unlink()
            except Exception:
                pass
            return {"ok": True, "note": "that old job was already gone -- cleared it"}
        return {"error": "no such running job"}

    def jobs(self) -> dict:
        cur = self.current.public() if self.current else None
        if cur is None:  # after a restart, surface a still-running orphan so it's visible + cancellable
            mk = self.orphan()
            if mk:
                cur = self._orphan_public(mk)
        hist = []
        try:
            for line in reversed(JOBS_JSONL.read_text().strip().splitlines()[-25:]):
                try:
                    hist.append(json.loads(line))
                except Exception:
                    continue  # one truncated line must not wipe the whole history
        except Exception:
            pass
        return {"current": cur, "history": hist}

    def job_log(self, job_id: str, offset: int) -> dict:
        j = self.current if (self.current and self.current.id == job_id) else None
        log_path = j.log_path if j else str(OUTPUTS / f"_panel_job_{job_id}.log")
        status = j.public() if j else None
        if status is None:
            for h in self.jobs()["history"]:
                if h["id"] == job_id:
                    status = h
                    break
        start = 0
        try:
            size = os.path.getsize(log_path)
            with open(log_path, "rb") as f:
                start = max(0, min(offset, size))
                f.seek(start)
                raw = f.read(65536)
                next_offset = start + len(raw)  # true read-end in BYTES (chunk is decoded)
                chunk = raw.decode("utf-8", "replace")
                size = max(size, next_offset)
        except Exception:
            size, chunk, next_offset = 0, "", 0
        return {"job": status, "offset": start, "next_offset": next_offset,
                "size": size, "chunk": chunk}


JOBS = JobManager()

# ------------------------------------------------------------------ actions -> argv
_TOKEN_MAP = {"{TODAY}": lambda: date.today().isoformat(),
              "{TOMORROW}": lambda: (date.today() + timedelta(days=1)).isoformat(),
              "{YESTERDAY}": lambda: (date.today() - timedelta(days=1)).isoformat()}


def _expand_tokens(argv: list) -> list:
    # substring replace, mirroring heartbeat's _expand_tokens — a recipe arg like
    # "--end={TOMORROW}" must behave identically under panel refresh and ACQUIRE
    out = []
    for a in argv:
        for tok, fn in _TOKEN_MAP.items():
            if tok in a:
                a = a.replace(tok, fn())
        out.append(a)
    return out


def _resolve_cwd(tag: str) -> Path:
    return LIB if tag == "lib" else REPO


def build_refresh_job(body: dict) -> dict:
    """Translate a validated UI action into (label, argv, cwd, hard_s). The browser
    never sends a command -- only an action + whitelisted values."""
    action = body.get("action")
    py = sys.executable or "python3"

    if action == "measure":
        return {"action": "measure", "label": "re-check data dates (no downloads)",
                "cmd": [py, "scripts/heartbeat.py", "--tier", "measure", "--run"],
                "cwd": REPO, "hard_s": 1800, "meta": {}}

    if action == "acquire":
        n = int(body.get("max_sources", 3))
        n = max(1, min(n, 10))
        return {"action": "acquire", "label": f"grab new data (up to {n} due sources)",
                "cmd": [py, "scripts/heartbeat.py", "--tier", "acquire", "--run",
                        "--acquire-optin", "--max-sources", str(n)],
                "cwd": REPO, "hard_s": 3300, "meta": {"max_sources": n}}

    if action == "source":
        sid = str(body.get("source_id", ""))
        if not re.match(r"^[a-z0-9_]{3,80}$", sid):
            return {"error": "bad source_id"}
        plan = refresh_plan_for(sid)
        if plan["tier"] in ("recipe", "recipe_disabled"):
            argv = _expand_tokens(list(plan["cmd_preview"]))
            if argv and str(argv[0]).endswith(".py"):
                argv = [py] + argv
            return {"action": "source", "label": f"refresh {sid} (one-click recipe)", "cmd": argv,
                    "cwd": _resolve_cwd(plan.get("cwd", "repo")), "hard_s": 3300,
                    "meta": {"source_id": sid, "tier": plan["tier"]}}
        if plan["tier"] == "script":
            loader = plan["loader"]
            # defense in depth: the resolver already routes replace-mode loaders to
            # 'script_replace', but never let a script-tier refresh run a non-append loader
            if loader.get("write_mode") != "append":
                return {"error": f"{sid}: {loader.get('script')} isn't add-only, so the panel "
                                 f"refuses to run it (it could wipe the table)"}
            argv = [py, loader["script"]]
            if loader.get("has_run_flag"):
                argv.append("--run")
            kinds = loader.get("flag_kinds", {})
            for flag, val in (body.get("args") or {}).items():
                rx = FLAG_VALIDATORS.get(kinds.get(flag, ""))
                if flag not in loader["date_flags"] or not rx:
                    return {"error": f"flag {flag} not allowed for this loader"}
                if not rx.fullmatch(str(val)):  # fullmatch: '$' alone still admits '\n'
                    return {"error": f"bad value for {flag} (expected {kinds.get(flag)}): {val!r}"}
                argv += [flag, str(val)]
            return {"action": "source", "label": f"refresh {sid} ({loader['script']})",
                    "cmd": argv, "cwd": REPO, "hard_s": 3300,
                    "meta": {"source_id": sid, "tier": "script",
                             "write_mode": loader["write_mode"]}}
        return {"error": f"no way to refresh {sid} from the panel: {plan['note']}"}

    if action == "onboard":
        sid = str(body.get("source_id", ""))
        if not re.match(r"^[a-z0-9_]{3,80}$", sid):
            return {"error": "bad source_id"}
        if not os.environ.get("ANTHROPIC_API_KEY"):
            return {"error": "ANTHROPIC_API_KEY isn't set -- add it to library-onboarding/.env "
                             "and restart the panel. AI rebuild won't work until then."}
        rows = qd("SELECT SOURCE_ID, NAME, URL, JURISDICTION FROM LIBRARY_META.REGISTRY.CATALOG "
                  "WHERE SOURCE_ID = %s", (sid,))
        if not rows or not rows[0].get("URL"):
            return {"error": f"{sid} has no URL in the catalog -- the AI has nothing to rebuild from"}
        r = rows[0]
        qfile = OUTPUTS / f"_panel_onboard_{sid}.json"
        queue_entry = {
            "name": r.get("NAME") or sid, "url": r["URL"], "source_id": sid,
            "jurisdiction": (r.get("JURISDICTION") or "").lower() or sid.split("_")[0],
            "identifiers": [], "include_landed": True,
        }
        # the file is written at LAUNCH (from the nonce-pinned spec), so what the preview
        # shows -- including the queue payload in meta -- is exactly what runs
        return {"action": "onboard", "label": f"AI rebuild {sid}",
                "cmd": [py, "onboard.py", "--queue", str(qfile), "--yes", "--include-landed"],
                "cwd": LIB, "hard_s": 5400,
                "meta": {"source_id": sid, "tier": "llm",
                         "queue_file": str(qfile), "queue_entry": queue_entry}}

    return {"error": f"unknown action {action!r}"}


# Preview->launch pinning: the confirm modal shows a command; the launch must run THAT
# command, not a re-resolution of it (recipes can be edited, {TOMORROW} rolls over at
# midnight). Previews park the fully-built spec under a nonce; launch consumes the nonce.
_SPECS: dict = {}
_SPECS_LOCK = threading.Lock()
SPEC_TTL_S = 900


def park_spec(spec: dict) -> str:
    nonce = uuid.uuid4().hex
    with _SPECS_LOCK:
        now = time.time()
        for k in [k for k, (ts, _) in _SPECS.items() if now - ts > SPEC_TTL_S]:
            _SPECS.pop(k, None)
        _SPECS[nonce] = (now, spec)
    return nonce


def take_spec(nonce: str) -> dict | None:
    with _SPECS_LOCK:
        hit = _SPECS.pop(str(nonce), None)
    if not hit or time.time() - hit[0] > SPEC_TTL_S:
        return None
    return hit[1]


# ------------------------------------------------------------------ data endpoints
def api_overview(days: int) -> dict:
    # V_STATE goes through qd() so it gets the same lock + reconnect-retry as every other
    # read (common.vstate swallows errors into {}, which would cache blank tiles for 120s)
    vs = cached("vstate", 120, lambda: {r["METRIC"]: r["VALUE"] for r in qd(
        "SELECT METRIC, VALUE FROM LIBRARY_META.REGISTRY.V_STATE")})
    fresh = cached("fresh_counts", 120, lambda: qd(
        "SELECT FRESHNESS_STATE AS STATE, COUNT(*) AS N "
        "FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS GROUP BY 1"))
    unmeasured = cached("unmeasured", 300, lambda: qd(
        "SELECT COUNT(*) AS N FROM LIBRARY_META.REGISTRY.CATALOG c "
        "LEFT JOIN LIBRARY_META.REGISTRY.SOURCE_FRESHNESS f ON c.SOURCE_ID = f.SOURCE_ID "
        "WHERE c.LIFECYCLE IN ('landed','modeled') AND f.SOURCE_ID IS NULL"))
    daily = cached(f"daily_{days}", 120, lambda: qd(
        "SELECT TO_DATE(STARTED_AT) AS D, STATUS, COUNT(*) AS RUNS, "
        "SUM(COALESCE(ROW_COUNT,0)) AS ROWS_LOADED "
        "FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
        "WHERE STARTED_AT >= DATEADD(day, %s, CURRENT_TIMESTAMP()) "
        "GROUP BY 1, 2 ORDER BY 1", (-days,)))
    failures = cached(f"fails_{days}", 120, lambda: qd(
        "SELECT SOURCE_ID, STATUS, STARTED_AT, LEFT(COALESCE(MESSAGE,''), 220) AS MESSAGE "
        "FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
        "WHERE STATUS IN ('failed','error') AND STARTED_AT >= DATEADD(day, %s, CURRENT_TIMESTAMP()) "
        "ORDER BY STARTED_AT DESC LIMIT 12", (-days,)))
    overdue = cached("overdue", 300, lambda: qd(
        "SELECT SOURCE_ID, FRESHNESS_STATE, DATA_AGE_DAYS, CADENCE_BUCKET "
        "FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS "
        "WHERE FRESHNESS_STATE IN ('overdue','stale','due') "
        "ORDER BY CASE FRESHNESS_STATE WHEN 'overdue' THEN 0 WHEN 'due' THEN 1 ELSE 2 END, "
        "DATA_AGE_DAYS DESC NULLS LAST LIMIT 12"))
    return {"vstate": vs, "freshness": fresh, "unmeasured": (unmeasured or [{}])[0].get("N", 0),
            "daily": daily, "failures": failures, "overdue": overdue,
            "budget": budget(), "heartbeat": heartbeat_status(),
            "pour_running": common.pour_running(), "days": days,
            "generated_at": datetime.now(timezone.utc).isoformat()}


def api_sources() -> dict:
    cat = cached("cat_sources", 120, lambda: qd(
        "SELECT SOURCE_ID, NAME, DOMAIN_PRIMARY, LIFECYCLE, LANDED_ROW_COUNT, "
        "LAST_INGESTED_AT, URL, PUBLISHER, TRUST_LAYER "
        "FROM LIBRARY_META.REGISTRY.CATALOG "
        "WHERE LIFECYCLE IN ('landed','modeled','stale','empty','sampled') ORDER BY SOURCE_ID"))
    fresh = cached("fresh_all", 120, lambda: qd(
        "SELECT * FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS"))
    fmap = {f.get("SOURCE_ID"): f for f in fresh}
    out = []
    for c in cat:
        sid = c["SOURCE_ID"]
        f = fmap.get(sid, {})
        plan = refresh_plan_for(sid, url=c.get("URL") or "")
        out.append({
            "source_id": sid, "name": c.get("NAME"), "domain": c.get("DOMAIN_PRIMARY"),
            "lifecycle": c.get("LIFECYCLE"), "rows": c.get("LANDED_ROW_COUNT"),
            "last_ingested_at": c.get("LAST_INGESTED_AT"), "url": c.get("URL"),
            "trust_layer": c.get("TRUST_LAYER"),
            "freshness_state": f.get("FRESHNESS_STATE") or "unmeasured",
            "data_through": f.get("DATA_THROUGH_ISO"),
            "data_age_days": f.get("DATA_AGE_DAYS"),
            "cadence": f.get("CADENCE_BUCKET"),
            "last_run_status": f.get("LAST_RUN_STATUS"),
            "last_run_at": f.get("LAST_RUN_AT"),
            "last_run_rows": f.get("LAST_RUN_ROWS"),
            "refresh": plan,
        })
    return {"sources": out}


def api_runs(days: int, status: str, q: str, limit: int) -> dict:
    limit = max(1, min(limit, 1000))
    sql = ("SELECT SOURCE_ID, RUN_ID, STARTED_AT, ENDED_AT, STATUS, ROW_COUNT, FILE_BYTES, "
           "SHA256, SOURCE_URL, MESSAGE, DATEDIFF('second', STARTED_AT, ENDED_AT) AS DUR_S "
           "FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
           "WHERE STARTED_AT >= DATEADD(day, %s, CURRENT_TIMESTAMP())")
    params: list = [-days]
    if status and re.match(r"^[a-z_]{2,20}$", status):
        sql += " AND STATUS = %s"
        params.append(status)
    if q:
        sql += " AND SOURCE_ID ILIKE %s"
        params.append(f"%{q[:60]}%")
    sql += " ORDER BY STARTED_AT DESC LIMIT %s"
    params.append(limit)
    return {"runs": qd(sql, tuple(params))}


def api_source_detail(sid: str) -> dict:
    if not re.match(r"^[a-z0-9_%.]{2,90}$", sid):
        return {"error": "bad sid"}
    cat = qd("SELECT * FROM LIBRARY_META.REGISTRY.CATALOG WHERE SOURCE_ID = %s", (sid,))
    fresh = qd("SELECT * FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS WHERE SOURCE_ID = %s", (sid,))
    runs = qd("SELECT RUN_ID, STARTED_AT, ENDED_AT, STATUS, ROW_COUNT, FILE_BYTES, SHA256, "
              "LEFT(COALESCE(MESSAGE,''), 500) AS MESSAGE, "
              "DATEDIFF('second', STARTED_AT, ENDED_AT) AS DUR_S "
              "FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS WHERE SOURCE_ID = %s "
              "ORDER BY STARTED_AT DESC LIMIT 50", (sid,))
    c = cat[0] if cat else {}
    return {"catalog": c, "freshness": fresh[0] if fresh else None, "runs": runs,
            "refresh": refresh_plan_for(sid, url=(c.get("URL") or ""))}


# ------------------------------------------------------------------ HTTP layer
_PLOTLY_JS = None


def _plotly_js_path():
    global _PLOTLY_JS
    if _PLOTLY_JS is None:
        try:
            import plotly
            p = Path(plotly.__file__).parent / "package_data" / "plotly.min.js"
            _PLOTLY_JS = p if p.exists() else False
        except Exception:
            _PLOTLY_JS = False
    return _PLOTLY_JS


class Handler(BaseHTTPRequestHandler):
    server_version = "RipplePanel/1.0"

    def log_message(self, fmt, *args):  # quiet; jobs have their own logs
        pass

    def _host_ok(self) -> bool:
        """Anti DNS-rebinding / cross-origin gate: the browser always sends the Host
        it connected to. Anything but our own loopback host is a hostile page."""
        host = (self.headers.get("Host") or "").split(":")[0].strip("[]").lower()
        return host in ("127.0.0.1", "localhost", "::1")

    # ---- plumbing --------------------------------------------------------
    def _send(self, code: int, body: bytes, ctype: str):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        if ctype.startswith("text/html"):
            # inline script/style are ours by construction; block everything remote
            self.send_header("Content-Security-Policy",
                             "default-src 'self'; script-src 'self' 'unsafe-inline'; "
                             "style-src 'self' 'unsafe-inline'; img-src 'self' data:; "
                             "connect-src 'self'; object-src 'none'; base-uri 'none'")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code: int = 200):
        self._send(code, json.dumps(obj, default=_json_default).encode(), "application/json")

    def _qs(self) -> dict:
        return {k: v[0] for k, v in parse_qs(urlparse(self.path).query).items()}

    # ---- GET ---------------------------------------------------------------
    def do_GET(self):
        if not self._host_ok():
            return self._json({"error": "bad Host header"}, 403)
        path = urlparse(self.path).path
        qs = self._qs()
        try:
            if path in ("/", "/index.html"):
                return self._send(200, PAGE_PATH.read_bytes(), "text/html; charset=utf-8")
            if path == "/favicon.ico":
                return self._send(204, b"", "image/x-icon")
            if path == "/static/plotly.min.js":
                p = _plotly_js_path()
                if not p:
                    return self._send(404, b"plotly not installed", "text/plain")
                return self._send(200, p.read_bytes(), "application/javascript")
            if path == "/api/overview":
                return self._json(api_overview(int(qs.get("days", 30))))
            if path == "/api/sources":
                if qs.get("rescan"):
                    cache_clear("")
                return self._json(api_sources())
            if path == "/api/runs":
                return self._json(api_runs(int(qs.get("days", 30)), qs.get("status", ""),
                                           qs.get("q", ""), int(qs.get("limit", 300))))
            if path == "/api/source":
                return self._json(api_source_detail(qs.get("sid", "")))
            if path == "/api/preflight":
                return self._json(JOBS.preflight(qs.get("action", "source")))
            if path == "/api/budget":
                return self._json(budget(refresh=bool(qs.get("refresh"))))
            if path == "/api/jobs":
                return self._json(JOBS.jobs())
            if path == "/api/job":
                return self._json(JOBS.job_log(qs.get("id", ""), int(qs.get("offset", 0))))
            return self._json({"error": f"no route {path}"}, 404)
        except BrokenPipeError:
            pass
        except Exception as e:
            return self._json(_error_public(e), 500)

    # ---- POST --------------------------------------------------------------
    def do_POST(self):
        if not self._host_ok():
            return self._json({"error": "bad Host header"}, 403)
        # a cross-origin form/text POST is a CORS "simple request" that skips preflight;
        # requiring the JSON content type forces a preflight no hostile page passes.
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        if ctype != "application/json":
            return self._json({"error": "Content-Type must be application/json"}, 415)
        path = urlparse(self.path).path
        try:
            n = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(min(n, 65536)) or b"{}")
        except Exception:
            return self._json({"error": "bad JSON body"}, 400)
        try:
            if path == "/api/refresh":
                if body.get("nonce"):  # launch of a previously previewed, pinned spec
                    spec = take_spec(body["nonce"])
                    if not spec:
                        return self._json({"error": "that preview expired -- open it again"}, 410)
                else:
                    spec = build_refresh_job(body)
                    if "error" in spec:
                        return self._json(spec, 400)
                    spec["cmd"] = [str(c) for c in spec["cmd"]]
                    spec["cwd"] = str(spec["cwd"])
                    if body.get("preview"):
                        out = dict(spec)
                        out["nonce"] = park_spec(spec)
                        # fresh budget read so the modal's band matches the launch gate
                        out["preflight"] = JOBS.preflight(spec["action"], fresh=True)
                        return self._json(out)
                if spec["action"] == "onboard" and spec["meta"].get("queue_entry"):
                    Path(spec["meta"]["queue_file"]).write_text(
                        json.dumps([spec["meta"]["queue_entry"]], indent=1))
                res = JOBS.launch(spec["action"], spec["label"], spec["cmd"],
                                  spec["cwd"], spec["hard_s"], spec["meta"])
                return self._json(res, 409 if "error" in res else 200)
            if path == "/api/job/cancel":
                return self._json(JOBS.cancel(str(body.get("id", ""))))
            return self._json({"error": f"no route {path}"}, 404)
        except Exception as e:
            return self._json(_error_public(e), 500)


def _prune_job_logs(days: int = 14):
    """Old per-job logs pile up forever otherwise; history (jsonl) is kept."""
    cutoff = time.time() - days * 86400
    for p in OUTPUTS.glob("_panel_job_*.log"):
        try:
            if p.stat().st_mtime < cutoff:
                p.unlink()
        except Exception:
            pass
    # loader download temp files (multi-GB: AIS/Open-Payments/SEC zips) can be orphaned by
    # a cancelled/killed refresh -- reclaim the disk. Repo-relative dir set by the round-2
    # loader fix; skip anything modified in the last day (a live download).
    scratch = REPO / ".scratch" / "loader_downloads"
    day_ago = time.time() - 86400
    if scratch.is_dir():
        for p in scratch.iterdir():
            try:
                if p.is_file() and p.stat().st_mtime < day_ago:
                    p.unlink()
            except Exception:
                pass


def serve(port: int = DEFAULT_PORT, open_browser: bool = True) -> int:
    global RUNNING_MARKER
    OUTPUTS.mkdir(exist_ok=True)
    # port-scope the running-marker so a SECOND panel (suggested on a port clash) doesn't
    # collide on one shared file and falsely block launches / orphan the other's job
    RUNNING_MARKER = OUTPUTS / f"_panel_job_running_{port}.json"
    _prune_job_logs()
    orphan = JobManager.orphan()
    if orphan:
        print(f"[!!] a panel job from a previous session is still running: "
              f"pid {orphan.get('pid')} -- {orphan.get('label')} (launches are blocked until it ends)")
    ThreadingHTTPServer.allow_reuse_address = True  # instant restart, no TIME_WAIT bind failure
    try:
        httpd = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    except OSError as e:
        if getattr(e, "errno", None) in (48, 98):  # EADDRINUSE (mac/linux)
            print(f"[XX] port {port} is already in use -- another panel running? "
                  f"Open http://127.0.0.1:{port} or start with --port {port + 1}")
            return 1
        raise
    url = f"http://127.0.0.1:{port}"
    print(f"[OK] Ripple Control Panel -> {url}   (ctrl-C to stop)")
    if open_browser and not os.environ.get("RIPPLE_NO_OPEN"):
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[OK] panel stopped")
    finally:
        _pool_close_all()
    return 0
