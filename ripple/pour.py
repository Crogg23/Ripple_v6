"""pour — plan / watch / run the onboarding pour (deterministic-first router).

Three actions under one verb:

  ripple pour watch            live meter over a running pour (or last pour's tally)
  ripple pour plan <queue>     read-only: split a queue into DETERMINISTIC vs LLM
  ripple pour run  <queue>     guarded executor (DRY by default; --run to land)

WHY deterministic-first: a source we already have a verified spec for (bridge_fuel_specs
or backfill_specs) or a plain portal dataset (Socrata/ArcGIS) can be landed LLM-free and
~free. Only novel sources need the LLM agent (~$0.10-0.30 each). Routing the free ones
around the agent is the whole point of #5.

Safety: `run --run` REFUSES if a pour is live (they'd share onboarding_log.json). During
build we never execute it — the classifier / meter parse / refuse-guard are unit-tested
with stubs (tests/test_ripple_pour.py).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
from pathlib import Path

from . import common as C

ONBOARD_LOG = C.LIB / "onboarding_log.json"
POUR_LOG = C.LIB / "pour_keyless.log"

# onboarding_log statuses we tally in the meter, in display order.
STATUS_ORDER = ["complete", "failed", "empty", "needs_key", "already_cataloged"]
# short labels so the one-liner stays compact
STATUS_LABEL = {
    "complete": "done",
    "failed": "failed",
    "empty": "empty",
    "needs_key": "need-key",
    "already_cataloged": "cataloged",
}

# URL / platform tokens that mark a source as a plain portal dataset the portal
# loader templates (Socrata / ArcGIS) can handle without an LLM.
PORTAL_TOKENS = ("socrata", "arcgis", "opendata", ".hub.", "data.gov", "/resource/")


# --------------------------------------------------------------- arg wiring
def add_arguments(parser) -> None:
    parser.add_argument("action", choices=["watch", "plan", "run"],
                        help="watch = live meter; plan = router preview; run = guarded executor")
    parser.add_argument("queue", nargs="?",
                        help="queue JSON path (required for plan/run)")
    parser.add_argument("--interval", type=int, default=5,
                        help="watch refresh seconds (default 5)")
    parser.add_argument("--once", action="store_true",
                        help="watch: print one snapshot and exit")
    parser.add_argument("--run", action="store_true",
                        help="run: actually land (default is a DRY plan)")


# --------------------------------------------------------------- pure helpers
def load_queue(path: str | Path) -> list[dict]:
    """Read a queue JSON (a list of source entries). Raises on bad shape."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError("queue file must be a JSON list of source entries")
    return data


def known_spec_ids(specs_modules=None) -> set[str]:
    """The set of source_ids we have a verified deterministic spec for.

    Imports scripts/bridge_fuel_specs.py + scripts/backfill_specs.py lazily so a
    missing module (or a test injecting stubs) never hard-fails classification.
    Pass specs_modules (a list of objects with a .SPECS list) to override in tests.
    """
    if specs_modules is None:
        specs_modules = []
        scripts = C.REPO / "scripts"
        if str(scripts) not in sys.path:
            sys.path.insert(0, str(scripts))
        for name in ("bridge_fuel_specs", "backfill_specs"):
            try:
                specs_modules.append(__import__(name))
            except Exception:  # a missing/broken spec module just contributes nothing
                pass
    ids: set[str] = set()
    for mod in specs_modules:
        for spec in getattr(mod, "SPECS", []) or []:
            sid = spec.get("source_id")
            if sid:
                ids.add(sid)
    return ids


def is_portal(entry: dict) -> bool:
    """True if the entry looks like a plain Socrata/ArcGIS portal dataset — the
    URL or an identifier carries a known portal platform token."""
    hay = (entry.get("url") or "").lower()
    ids = entry.get("identifiers") or []
    hay += " " + " ".join(str(x).lower() for x in ids)
    return any(tok in hay for tok in PORTAL_TOKENS)


def classify(queue: list[dict], spec_ids: set[str]) -> dict:
    """Split a queue into deterministic vs LLM.

    DETERMINISTIC when the source_id has a verified spec, OR it's a portal dataset.
    LLM otherwise (novel). Returns {'deterministic': [...], 'llm': [...]} lists of
    the original entries, each tagged with a 'route_reason'.
    """
    deterministic, llm = [], []
    for entry in queue:
        sid = entry.get("source_id") or ""
        if sid in spec_ids:
            e = dict(entry, route_reason="bridge_fuel spec")
            deterministic.append(e)
        elif is_portal(entry):
            e = dict(entry, route_reason="portal loader")
            deterministic.append(e)
        else:
            llm.append(dict(entry, route_reason="novel"))
    return {"deterministic": deterministic, "llm": llm}


# --------------------------------------------------------------- meter parse
def parse_position(log_text: str) -> tuple[int, int] | None:
    """Pull the latest '[N of M]' position marker out of a pour log's text.
    Returns (n, m) or None if no marker present."""
    matches = re.findall(r"\[(\d+)\s+of\s+(\d+)\]", log_text)
    if not matches:
        return None
    n, m = matches[-1]
    return int(n), int(m)


def queue_total_from_cmdline(cmdline: str | None) -> int | None:
    """Parse the --queue path out of a pour cmdline and count its entries, so the
    meter total is right even when the log has no position markers yet."""
    if not cmdline:
        return None
    m = re.search(r"--queue[= ]+(\S+)", cmdline)
    if not m:
        return None
    path = m.group(1).strip().strip('"').strip("'")
    try:
        return len(load_queue(path))
    except Exception:
        return None


def tally_log(log: dict) -> dict[str, int]:
    """Count onboarding_log.json entries by status. Unknown statuses roll into
    'other' so the meter still sums to the real total."""
    counts = {s: 0 for s in STATUS_ORDER}
    counts["other"] = 0
    for rec in log.values():
        st = (rec or {}).get("status") if isinstance(rec, dict) else None
        if st in counts:
            counts[st] += 1
        else:
            counts["other"] += 1
    return counts


def render_meter(counts: dict[str, int], pos: tuple[int, int] | None,
                 total: int | None, last_fail: str | None,
                 running: bool) -> str:
    """Build the compact one-line meter string.

    'POUR [72/720] 10%  |  done 39 . failed 29 . need-key 4 . empty 2  |  last fail: <id> (<why>)'
    """
    done = sum(counts.get(s, 0) for s in STATUS_ORDER) + counts.get("other", 0)
    n = pos[0] if pos else done
    m = (pos[1] if pos else None) or total or done
    pct = f"{int(100 * n / m)}%" if m else "--"
    head = f"POUR [{n}/{m}] {pct}" if running else f"POUR (ended) [{done}/{m or done}]"

    parts = []
    for s in STATUS_ORDER:
        if counts.get(s):
            parts.append(f"{STATUS_LABEL[s]} {counts[s]}")
    if counts.get("other"):
        parts.append(f"other {counts['other']}")
    body = " . ".join(parts) if parts else "no results yet"

    tail = f"  |  last fail: {last_fail}" if last_fail else ""
    return f"{head}  |  {body}{tail}"


# --------------------------------------------------------------- data pulls
def read_onboard_log() -> dict:
    """Read onboarding_log.json read-only. Returns {} if missing/unreadable — the
    live pour owns this file, we never write it."""
    try:
        return json.loads(ONBOARD_LOG.read_text(encoding="utf-8"))
    except Exception:
        return {}


def read_pour_log_text() -> str:
    try:
        return POUR_LOG.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def last_failures_from_log(log: dict, limit: int = 5) -> list[str]:
    """Best-effort recent failures from the onboarding_log alone (no DB): the
    entries whose status is failed/empty, newest-updated first."""
    bad = []
    for name, rec in log.items():
        if not isinstance(rec, dict):
            continue
        if rec.get("status") in ("failed", "empty"):
            when = rec.get("updated_at") or rec.get("completed_at") or ""
            sid = rec.get("source_id") or name
            bad.append((when, f"{sid} ({rec.get('status')})"))
    bad.sort(reverse=True)
    return [s for _, s in bad[:limit]]


def last_failures_from_db(limit: int = 5) -> list[str]:
    """Recent failed/empty ingest runs with their one-line message. Degrades to []
    if Snowflake is unreachable — the meter still renders off the log."""
    try:
        conn = C.connect()
    except Exception:
        return []
    try:
        rows = C.rows(conn, """
            SELECT SOURCE_ID, STATUS, LEFT(COALESCE(MESSAGE,''), 60)
            FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
            WHERE STATUS IN ('failed','empty','error')
            ORDER BY COALESCE(ENDED_AT, STARTED_AT) DESC
            LIMIT %s
        """, (limit,))
    except Exception:
        rows = []
    finally:
        try:
            conn.close()
        except Exception:
            pass
    out = []
    for sid, status, msg in rows:
        why = (msg or status or "").strip()
        out.append(f"{sid} ({why})" if why else str(sid))
    return out


# --------------------------------------------------------------- watch (#3)
def _snapshot() -> str:
    cmdline = C.pour_running()
    running = cmdline is not None
    log = read_onboard_log()
    counts = tally_log(log)

    pos = parse_position(read_pour_log_text())
    total = queue_total_from_cmdline(cmdline)

    # prefer DB reasons (they carry the actual 404 / message); fall back to the log.
    fails = last_failures_from_db(1) or last_failures_from_log(log, 1)
    last_fail = fails[0] if fails else None

    line = render_meter(counts, pos, total, last_fail, running)
    if not running:
        line += "  |  no pour running"
    return line


def run_watch(args) -> int:
    if args.once or C.pour_running() is None:
        # one snapshot: either asked for, or nothing to loop on
        print(_snapshot())
        if C.pour_running() is None and not args.once:
            # extra context when idle: recent failures block
            log = read_onboard_log()
            fails = last_failures_from_db(5) or last_failures_from_log(log, 5)
            if fails:
                print(C.hr())
                print("last pour recent failures:")
                for f in fails:
                    print(f"  {C.BAD} {f}")
        return 0

    interval = max(1, int(args.interval or 5))
    print(f"watching pour (refresh {interval}s, Ctrl+C to stop)")
    try:
        while True:
            print(_snapshot(), flush=True)
            if C.pour_running() is None:
                print("pour ended.")
                return 0
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nstopped watching (pour still running).")
        return 0


# --------------------------------------------------------------- plan (#5 preview)
def _sample(entries: list[dict], n: int = 5) -> list[str]:
    out = []
    for e in entries[:n]:
        sid = e.get("source_id") or e.get("name") or "?"
        out.append(f"{sid} [{e.get('route_reason','')}]")
    return out


def run_plan(args) -> int:
    if not args.queue:
        print("usage: ripple pour plan <queue.json>")
        return 2
    try:
        queue = load_queue(args.queue)
    except Exception as e:
        print(f"{C.BAD} cannot read queue: {e}")
        return 2

    split = classify(queue, known_spec_ids())
    det, llm = split["deterministic"], split["llm"]

    print(C.header(f"POUR PLAN — {Path(args.queue).name}  ({len(queue)} sources)"))
    print(f"DETERMINISTIC: {len(det)} (~free, bridge_fuel/portal)"
          f"  .  LLM AGENT: {len(llm)} (~$0.10-0.30 each)")
    print(C.hr())
    if det:
        print("DETERMINISTIC sample:")
        for s in _sample(det):
            print(f"  {C.OK} {s}")
    if llm:
        print("LLM AGENT sample:")
        for s in _sample(llm):
            print(f"  {C.DASH} {s}")
    return 0


# --------------------------------------------------------------- run (#5 executor)
def write_remainder(entries: list[dict], src_queue: str) -> Path:
    """Write the LLM-set remainder queue next to the source queue and return its path.
    Strips the internal 'route_reason' tag we added during classify."""
    clean = [{k: v for k, v in e.items() if k != "route_reason"} for e in entries]
    out = Path(src_queue).with_name(Path(src_queue).stem + "_remainder.json")
    out.write_text(json.dumps(clean, indent=1), encoding="utf-8")
    return out


def run_run(args) -> int:
    if not args.queue:
        print("usage: ripple pour run <queue.json> [--run]")
        return 2

    # HARD GUARD: never run concurrently with a live pour — they share the log.
    live = C.pour_running()
    if live:
        print(f"{C.BAD} REFUSING: a pour is already running — no concurrent pours "
              f"(they share onboarding_log.json).")
        print(f"     live: {live[:120]}")
        return 1

    try:
        queue = load_queue(args.queue)
    except Exception as e:
        print(f"{C.BAD} cannot read queue: {e}")
        return 2

    split = classify(queue, known_spec_ids())
    det, llm = split["deterministic"], split["llm"]
    det_ids = [e["source_id"] for e in det if e.get("source_id")]

    print(C.header(f"POUR RUN — {Path(args.queue).name}"))
    print(f"DETERMINISTIC: {len(det)} via bridge_fuel  .  LLM AGENT: {len(llm)} via onboard.py")

    if not args.run:
        # DRY plan is the default — show exactly what --run would do, execute nothing.
        print(C.hr())
        print("DRY plan (add --run to execute):")
        if det_ids:
            print(f"  1. python scripts/bridge_fuel_load.py --spec {','.join(det_ids)} --run")
        remainder_hint = Path(args.queue).with_name(Path(args.queue).stem + "_remainder.json").name
        if llm:
            print(f"  2. python onboard.py --batch --yes --queue {remainder_hint}  ({len(llm)} sources)")
        return 0

    # --- actually execute (guarded; Chris runs this, not the build agent) --------
    rc = 0
    if det_ids:
        print(f"{C.OK} landing {len(det_ids)} deterministic via bridge_fuel...")
        cmd = [sys.executable, str(C.REPO / "scripts" / "bridge_fuel_load.py"),
               "--spec", ",".join(det_ids), "--run"]
        try:
            rc = subprocess.run(cmd, cwd=str(C.REPO)).returncode
        except Exception as e:
            print(f"{C.BAD} bridge_fuel failed to launch: {e}")
            return 1

    if llm:
        remainder = write_remainder(llm, args.queue)
        print(f"{C.OK} wrote remainder queue: {remainder}")
        cmd = [sys.executable, str(C.LIB / "onboard.py"),
               "--batch", "--yes", "--queue", str(remainder)]
        print(f"     launching LLM batch: {' '.join(cmd)}")
        try:
            rc = subprocess.run(cmd, cwd=str(C.LIB)).returncode or rc
        except Exception as e:
            print(f"{C.BAD} onboard batch failed to launch: {e}")
            return 1

    return rc


# --------------------------------------------------------------- dispatch
def run(args) -> int:
    action = getattr(args, "action", None)
    if action == "watch":
        return run_watch(args)
    if action == "plan":
        return run_plan(args)
    if action == "run":
        return run_run(args)
    print("usage: ripple pour {watch|plan|run}")
    return 2
