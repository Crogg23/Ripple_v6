"""pour — plan / watch / run the onboarding pour (4-way deterministic-first router).

Three actions under one verb:

  ripple pour watch            live meter over a running pour (or last pour's tally)
  ripple pour plan <queue>     read-only: split a queue into DETERMINISTIC vs LLM
  ripple pour run  <queue>     guarded executor (DRY by default; --run to land)

Routing tiers (deterministic-first):
  bridge_fuel   — verified spec in bridge_fuel_specs / backfill_specs / sprint specs (~free)
  server_side   — GB-scale files fetched cloud-to-cloud via Snowflake stored procs
  portal        — Socrata / ArcGIS template loaders
  onboard       — LLM agent for novel sources (~$0.10-0.30 each)

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

# Late import — avoid circular at parse time; used only when spec_files need loading.
_spec_schema = None


def _get_spec_schema():
    global _spec_schema
    if _spec_schema is None:
        from loadkit import spec_schema
        _spec_schema = spec_schema
    return _spec_schema


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
    parser.add_argument("action", choices=["watch", "plan", "run", "status"],
                        help="watch = live meter; plan = router preview; run = guarded executor; "
                             "status = per-source status for a sprint queue")
    parser.add_argument("queue", nargs="?",
                        help="queue JSON path (required for plan/run/status)")
    parser.add_argument("--interval", type=int, default=5,
                        help="watch refresh seconds (default 5)")
    parser.add_argument("--once", action="store_true",
                        help="watch: print one snapshot and exit")
    parser.add_argument("--run", action="store_true",
                        help="run: actually land (default is a DRY plan)")


# --------------------------------------------------------------- pure helpers
def load_queue(path: str | Path) -> list[dict]:
    """Read a queue JSON. Accepts either a flat list of source entries or a
    manifest dict with a "sources" key. Raises on bad shape."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict) and "sources" in data:
        data = data["sources"]
    if not isinstance(data, list):
        raise ValueError("queue file must be a JSON list of source entries (or a manifest with 'sources')")
    return data


def _load_spec_modules(extra_files: list[str] | None = None):
    """Load all known spec modules + any extra spec files from a queue manifest.
    Returns list of modules with a .SPECS attribute."""
    specs_modules = []
    scripts = C.REPO / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))
    for name in ("bridge_fuel_specs", "backfill_specs", "server_side_specs"):
        try:
            specs_modules.append(__import__(name))
        except Exception:
            pass
    # Load sprint/extra spec files by path
    if extra_files:
        import importlib.util
        for fpath in extra_files:
            p = Path(fpath) if Path(fpath).is_absolute() else C.REPO / fpath
            if p.exists():
                try:
                    spec_ = importlib.util.spec_from_file_location(p.stem, str(p))
                    mod = importlib.util.module_from_spec(spec_)
                    spec_.loader.exec_module(mod)
                    specs_modules.append(mod)
                except Exception:
                    pass
    return specs_modules


def known_specs(specs_modules=None, extra_files=None) -> dict[str, dict]:
    """Map of source_id -> spec dict for all known deterministic specs.

    Imports scripts/bridge_fuel_specs.py, backfill_specs.py, server_side_specs.py,
    and any extra spec files. Pass specs_modules to override in tests.
    """
    if specs_modules is None:
        specs_modules = _load_spec_modules(extra_files)
    out: dict[str, dict] = {}
    for mod in specs_modules:
        for spec in getattr(mod, "SPECS", []) or []:
            sid = spec.get("source_id")
            if sid:
                out[sid.upper()] = spec
    return out


def known_spec_ids(specs_modules=None) -> set[str]:
    """The set of source_ids we have a verified deterministic spec for.
    Kept for backwards compatibility with tests."""
    return set(known_specs(specs_modules).keys())


def is_portal(entry: dict) -> bool:
    """True if the entry looks like a plain Socrata/ArcGIS portal dataset — the
    URL or an identifier carries a known portal platform token."""
    hay = (entry.get("url") or "").lower()
    ids = entry.get("identifiers") or []
    hay += " " + " ".join(str(x).lower() for x in ids)
    return any(tok in hay for tok in PORTAL_TOKENS)


def classify(queue: list[dict], specs: dict[str, dict] | None = None,
             spec_ids: set[str] | None = None) -> dict:
    """Route each queue entry to a loader tier.

    Returns {'bridge_fuel': [...], 'server_side': [...], 'portal': [...], 'onboard': [...]}
    with each entry tagged with 'route' and 'route_reason'.

    Backwards-compat: accepts spec_ids (old set) OR specs (new dict).
    """
    if specs is None:
        specs = {sid: {} for sid in (spec_ids or set())}

    buckets = {"bridge_fuel": [], "server_side": [], "portal": [], "onboard": []}
    for entry in queue:
        sid = (entry.get("source_id") or "").upper()
        spec = specs.get(sid)
        if spec:
            # Determine loader from spec's loader field (default bridge_fuel)
            loader = spec.get("loader", "bridge_fuel")
            # server_side_specs sources don't have a loader field but live in that module
            if not spec.get("loader") and spec.get("resolver"):
                loader = "server_side"
            e = dict(entry, route=loader, route_reason=f"{loader} spec")
            buckets.setdefault(loader, buckets["bridge_fuel"]).append(e) if loader not in buckets else buckets[loader].append(e)
        elif is_portal(entry):
            e = dict(entry, route="portal", route_reason="portal loader")
            buckets["portal"].append(e)
        else:
            buckets["onboard"].append(dict(entry, route="onboard", route_reason="novel"))
    return buckets


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

    # Load queue manifest for extra spec_files if present
    extra_files = None
    try:
        raw = json.loads(Path(args.queue).read_text(encoding="utf-8"))
        if isinstance(raw, dict) and raw.get("spec_files"):
            extra_files = raw["spec_files"]
            # The queue entries are in raw["sources"]
            queue = raw["sources"]
    except Exception:
        pass

    specs = known_specs(extra_files=extra_files)
    buckets = classify(queue, specs=specs)

    total = sum(len(v) for v in buckets.values())
    det_count = len(buckets["bridge_fuel"]) + len(buckets["server_side"]) + len(buckets["portal"])
    llm_count = len(buckets["onboard"])

    print(C.header(f"POUR PLAN — {Path(args.queue).name}  ({total} sources)"))
    print(f"DETERMINISTIC: {det_count} (~free)  .  LLM AGENT: {llm_count} (~$0.10-0.30 each)")
    print(C.hr())

    labels = {
        "bridge_fuel": ("BRIDGE_FUEL (laptop CSV)", C.OK),
        "server_side": ("SERVER_SIDE (cloud-to-cloud)", C.OK),
        "portal": ("PORTAL (Socrata/ArcGIS)", C.OK),
        "onboard": ("ONBOARD (LLM agent)", C.DASH),
    }
    for tier, entries in buckets.items():
        if not entries:
            continue
        label, icon = labels[tier]
        print(f"{label}: {len(entries)}")
        for s in _sample(entries):
            print(f"  {icon} {s}")

    # Egress check for server-side sources
    ss_hosts = set()
    for entry in buckets["server_side"]:
        sid = (entry.get("source_id") or "").upper()
        spec = specs.get(sid, {})
        url = spec.get("download_url") or spec.get("url") or entry.get("url") or ""
        from urllib.parse import urlparse
        if url:
            h = urlparse(url).hostname
            if h:
                ss_hosts.add(h)
        resolver = spec.get("resolver")
        if resolver and resolver.get("url"):
            h = urlparse(resolver["url"]).hostname
            if h:
                ss_hosts.add(h)
    if ss_hosts:
        print(C.hr())
        print("SERVER_SIDE hosts (must be on RIPPLE_BULK_EGRESS):")
        for h in sorted(ss_hosts):
            print(f"  {h}")

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

    # Load queue manifest for extra spec_files if present
    extra_files = None
    try:
        raw = json.loads(Path(args.queue).read_text(encoding="utf-8"))
        if isinstance(raw, dict) and raw.get("spec_files"):
            extra_files = raw["spec_files"]
            queue = raw["sources"]
    except Exception:
        pass

    specs = known_specs(extra_files=extra_files)
    buckets = classify(queue, specs=specs)

    bf_ids = [(e.get("source_id") or "").upper() for e in buckets["bridge_fuel"] if e.get("source_id")]
    ss_ids = [(e.get("source_id") or "").upper() for e in buckets["server_side"] if e.get("source_id")]
    portal_entries = buckets["portal"]
    llm_entries = buckets["onboard"]

    total = len(bf_ids) + len(ss_ids) + len(portal_entries) + len(llm_entries)
    print(C.header(f"POUR RUN — {Path(args.queue).name}  ({total} sources)"))
    print(f"  bridge_fuel: {len(bf_ids)}  |  server_side: {len(ss_ids)}"
          f"  |  portal: {len(portal_entries)}  |  onboard: {len(llm_entries)}")

    if not args.run:
        print(C.hr())
        print("DRY plan (add --run to execute):")
        step = 1
        if bf_ids:
            print(f"  {step}. python scripts/bridge_fuel_load.py --spec {','.join(bf_ids)} --run")
            step += 1
        if ss_ids:
            print(f"  {step}. python scripts/server_side_load.py --spec {','.join(ss_ids)} --run")
            step += 1
        if portal_entries:
            p_ids = [e.get("source_id", "?") for e in portal_entries]
            print(f"  {step}. portal_loader for: {', '.join(p_ids)}")
            step += 1
        if llm_entries:
            remainder_hint = Path(args.queue).with_name(Path(args.queue).stem + "_remainder.json").name
            print(f"  {step}. python onboard.py --batch --yes --queue {remainder_hint}  ({len(llm_entries)} sources)")
        return 0

    # --- actually execute (guarded; Chris runs this, not the build agent) --------
    rc = 0

    # Tier 1: bridge_fuel (laptop CSV)
    if bf_ids:
        print(f"{C.OK} landing {len(bf_ids)} via bridge_fuel...")
        cmd = [sys.executable, str(C.REPO / "scripts" / "bridge_fuel_load.py"),
               "--spec", ",".join(bf_ids), "--run"]
        try:
            rc = subprocess.run(cmd, cwd=str(C.REPO)).returncode
        except Exception as e:
            print(f"{C.BAD} bridge_fuel failed to launch: {e}")
            rc = 1

    # Tier 2: server_side (cloud-to-cloud)
    if ss_ids:
        print(f"{C.OK} landing {len(ss_ids)} via server_side...")
        cmd = [sys.executable, str(C.REPO / "scripts" / "server_side_load.py"),
               "--spec", ",".join(ss_ids), "--run"]
        try:
            result = subprocess.run(cmd, cwd=str(C.REPO)).returncode
            rc = rc or result
        except Exception as e:
            print(f"{C.BAD} server_side failed to launch: {e}")
            rc = rc or 1

    # Tier 3: portal (Socrata/ArcGIS)
    if portal_entries:
        print(f"{C.OK} landing {len(portal_entries)} via portal_loader...")
        for entry in portal_entries:
            sid = entry.get("source_id") or entry.get("name") or "?"
            url = entry.get("url") or entry.get("download_url") or ""
            cmd = [sys.executable, str(C.REPO / "connect" / "portal_loader.py"),
                   "--url", url, "--source-id", sid, "--run"]
            try:
                result = subprocess.run(cmd, cwd=str(C.REPO)).returncode
                rc = rc or result
            except Exception as e:
                print(f"{C.BAD} portal_loader failed for {sid}: {e}")
                rc = rc or 1

    # Tier 4: LLM agent (novel sources)
    if llm_entries:
        remainder = write_remainder(llm_entries, args.queue)
        print(f"{C.OK} wrote remainder queue: {remainder}")
        cmd = [sys.executable, str(C.LIB / "onboard.py"),
               "--batch", "--yes", "--queue", str(remainder)]
        print(f"     launching LLM batch: {' '.join(cmd)}")
        try:
            result = subprocess.run(cmd, cwd=str(C.LIB)).returncode
            rc = rc or result
        except Exception as e:
            print(f"{C.BAD} onboard batch failed to launch: {e}")
            rc = rc or 1

    return rc


# --------------------------------------------------------------- status (sprint view)
def _sprint_status_from_db(source_ids: list[str]) -> dict[str, dict]:
    """Query INGEST_RUNS for the latest run per source_id in the list.
    Returns {SOURCE_ID: {status, rows, ended_at, message, edges}} or {} on failure."""
    if not source_ids:
        return {}
    try:
        conn = C.connect()
    except Exception:
        return {}
    try:
        placeholders = ",".join(["%s"] * len(source_ids))
        rows = C.rows(conn, f"""
            SELECT SOURCE_ID, STATUS, ROW_COUNT, ENDED_AT, LEFT(COALESCE(MESSAGE,''),80)
            FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS
            WHERE SOURCE_ID IN ({placeholders})
            QUALIFY ROW_NUMBER() OVER (PARTITION BY SOURCE_ID ORDER BY COALESCE(ENDED_AT, STARTED_AT) DESC) = 1
        """, tuple(source_ids))
    except Exception:
        rows = []
    # Also grab edge counts for landed sources
    edge_counts = {}
    try:
        landed_ids = [r[0] for r in rows if r[1] == "success"]
        if landed_ids:
            ph2 = ",".join(["%s"] * len(landed_ids))
            edge_rows = C.rows(conn, f"""
                SELECT TABLE_NAME, COUNT(*)
                FROM LIBRARY_META."CONNECT".CONNECT_EDGES
                WHERE TABLE_NAME IN ({ph2})
                GROUP BY TABLE_NAME
            """, tuple(landed_ids))
            edge_counts = {r[0]: r[1] for r in edge_rows}
    except Exception:
        pass
    try:
        conn.close()
    except Exception:
        pass

    out = {}
    for r in rows:
        sid, status, row_count, ended, msg = r[0], r[1], r[2], r[3], r[4]
        out[sid.upper()] = {
            "status": status,
            "rows": row_count,
            "ended_at": str(ended) if ended else "",
            "message": msg or "",
            "edges": edge_counts.get(sid.upper(), 0),
        }
    return out


def run_status(args) -> int:
    """Show per-source status for a sprint queue (post-pour diagnostic)."""
    if not args.queue:
        print("usage: ripple pour status <queue.json>")
        return 2
    try:
        queue = load_queue(args.queue)
    except Exception as e:
        print(f"{C.BAD} cannot read queue: {e}")
        return 2

    source_ids = [(e.get("source_id") or "").upper() for e in queue if e.get("source_id")]
    if not source_ids:
        print("No source_ids found in queue.")
        return 1

    # Try reading manifest for sprint label
    sprint_label = ""
    try:
        raw = json.loads(Path(args.queue).read_text(encoding="utf-8"))
        if isinstance(raw, dict):
            sprint_label = raw.get("sprint", "")
    except Exception:
        pass

    label = f"Sprint {sprint_label}" if sprint_label else Path(args.queue).stem
    print(C.header(f"POUR STATUS — {label}  ({len(source_ids)} sources)"))

    db_status = _sprint_status_from_db(source_ids)
    total_rows = 0
    total_edges = 0
    done = 0
    failed = 0

    for sid in source_ids:
        info = db_status.get(sid, {})
        status = info.get("status", "not_started")
        rows = info.get("rows")
        edges = info.get("edges", 0)
        msg = info.get("message", "")

        if status == "success":
            icon = C.OK
            done += 1
            total_rows += (rows or 0)
            total_edges += edges
            row_str = f"{rows:,} rows" if rows else ""
            edge_str = f"{edges} edges" if edges else ""
            detail = "  ".join(filter(None, [row_str, edge_str]))
        elif status in ("failed", "error"):
            icon = C.BAD
            failed += 1
            detail = msg[:60] if msg else "failed"
        elif status == "empty":
            icon = C.DASH
            detail = "empty (density gate)"
        else:
            icon = " "
            detail = "not landed yet"

        print(f"  {icon} {sid:40} {detail}")

    print(C.hr())
    print(f"  landed: {done}/{len(source_ids)}  |  rows: {total_rows:,}  |  "
          f"edges: {total_edges}  |  failed: {failed}")
    return 0


# --------------------------------------------------------------- dispatch
def run(args) -> int:
    action = getattr(args, "action", None)
    if action == "watch":
        return run_watch(args)
    if action == "plan":
        return run_plan(args)
    if action == "run":
        return run_run(args)
    if action == "status":
        return run_status(args)
    print("usage: ripple pour {watch|plan|run|status}")
    return 2
