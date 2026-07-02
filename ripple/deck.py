"""status - the Morning Deck.

One screen that collapses 20 minutes of session-open archaeology into a glance.
Read-only: nothing here writes to Snowflake or touches the pour's files. The only
thing it persists is the ripple state file (outputs/_ripple_state.json) so the next
run can diff 'since last time'.

Sections, each degrades gracefully when its source is missing:
  HEADER    - timestamp + the live pour line (parsed from onboarding_log tallies)
  SCALE     - the big numbers from V_STATE
  FRESHNESS - one-line rollup + the worst rotting sources
  QUEUES    - your to-do: leads pending, review queue depth, unclassified landed
  SINCE     - what changed vs the last time you ran status
  BUDGET    - credit headroom to the 90% auto-suspend line
  HEALTH    - PAT days-left + any 'dead' freshness, one line

The pure helpers (freshness_rollup / since_diff / parse_pour_tally / pour_position)
take plain dicts and lists so they unit-test with no live DB.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone

from ripple import common as C

# The pour writes onboarding_log.json keyed by source name; these are the statuses
# we bucket into the header tally. Anything unrecognized falls into 'other'.
_DONE = {"complete", "already_cataloged"}
_FAILED = {"failed", "error"}
_NEEDKEY = {"needs_key"}
_EMPTY = {"empty"}


# --------------------------------------------------------------- pure helpers
def parse_pour_tally(log: dict) -> dict:
    """Bucket an onboarding_log.json dict ({name: {status,...}}) into header counts.
    Pure: hand it a sample dict in tests. Unknown statuses land in 'other'."""
    t = {"done": 0, "failed": 0, "need_keys": 0, "empty": 0, "other": 0, "total": 0}
    for entry in (log or {}).values():
        status = str((entry or {}).get("status", "")).lower()
        t["total"] += 1
        if status in _DONE:
            t["done"] += 1
        elif status in _FAILED:
            t["failed"] += 1
        elif status in _NEEDKEY:
            t["need_keys"] += 1
        elif status in _EMPTY:
            t["empty"] += 1
        else:
            t["other"] += 1
    return t


def pour_position(log_text: str) -> tuple[int, int] | None:
    """Pull the latest '[N of TOTAL]' progress marker out of a pour log's text.
    Returns (n, total) for the last marker, or None if the log has none."""
    matches = re.findall(r"\[(\d+)\s+of\s+(\d+)\]", log_text or "")
    if not matches:
        return None
    n, total = matches[-1]
    return int(n), int(total)


def _cmdline_queue_path(cmdline: str) -> str | None:
    """Best-effort: pull a --queue / --batch path off the live pour command line,
    if one was passed. The default pour uses --batch with no path (queue is baked in),
    so this is usually None and the header just shows the log-derived tallies."""
    if not cmdline:
        return None
    # Only --queue takes a path; --batch is a bare flag (queue baked into sources_queue.py).
    # Require the captured token to NOT itself be a flag, so 'onboard.py --batch --yes'
    # doesn't misread '--yes' as a queue path.
    m = re.search(r"--queue[=\s]+(?!--)(\S+)", cmdline)
    return m.group(1) if m else None


def freshness_rollup(fresh_rows: list[dict]) -> dict:
    """Count V_SOURCE_FRESHNESS rows by FRESHNESS_STATE. Pure: pass sample dicts.
    Returns every known state key (0 when absent) so the rollup line is stable."""
    counts = {s: 0 for s in ("fresh", "due", "overdue", "stale", "dead", "unknown")}
    for r in fresh_rows or []:
        state = str(r.get("FRESHNESS_STATE", "unknown") or "unknown").lower()
        counts[state] = counts.get(state, 0) + 1
    return counts


def worst_rotting(fresh_rows: list[dict], limit: int | None = 8) -> list[dict]:
    """The overdue+stale sources, worst DATA_AGE_DAYS first. limit=None -> all of them."""
    rotting = [r for r in (fresh_rows or [])
               if str(r.get("FRESHNESS_STATE", "") or "").lower() in ("overdue", "stale")]

    def age(r):
        try:
            return float(r.get("DATA_AGE_DAYS") or 0)
        except (TypeError, ValueError):
            return 0.0

    rotting.sort(key=age, reverse=True)
    return rotting if limit is None else rotting[:limit]


def _int(v, default=0):
    try:
        return int(float(str(v).replace(",", "")))
    except (TypeError, ValueError):
        return default


def since_diff(prev: dict, cur: dict) -> dict:
    """Diff the previous saved snapshot against the current one.

    Both snapshots look like:
      {"ts": iso, "metrics": {metric: value}, "success_ids": [source_id, ...]}
    Returns newly-landed / newly-failed source id lists plus metric deltas. When
    prev is empty (first run) 'first_run' is True and the caller prints the baseline
    line instead of a diff."""
    if not prev:
        return {"first_run": True, "newly_landed": [], "newly_failed": [], "deltas": {}}

    prev_ok = set(prev.get("success_ids") or [])
    cur_ok = set(cur.get("success_ids") or [])
    newly_landed = sorted(cur_ok - prev_ok)

    prev_bad = set(prev.get("failed_ids") or [])
    cur_bad = set(cur.get("failed_ids") or [])
    newly_failed = sorted(cur_bad - prev_bad)

    deltas = {}
    pm, cm = prev.get("metrics") or {}, cur.get("metrics") or {}
    # Only surface the movement metrics that matter for a morning glance.
    for key in ("taps.landed", "taps.modeled", "taps.scouted",
                "leads.total.active", "connect.edges", "landing.tables", "landing.rows"):
        d = _int(cm.get(key)) - _int(pm.get(key))
        if d:
            deltas[key] = d
    return {"first_run": False, "newly_landed": newly_landed,
            "newly_failed": newly_failed, "deltas": deltas}


def leads_active_total(vstate: dict) -> int:
    """Sum the per-rule leads.<rule>.active metrics out of V_STATE (there is no
    single 'total' row). Used for the queue count and the since-last-time delta."""
    total = 0
    for k, v in (vstate or {}).items():
        if k.startswith("leads.") and k.endswith(".active"):
            total += _int(v)
    return total


# --------------------------------------------------------------- data gathering
def _read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _read_text(path):
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _newest_pour_log():
    """The most-recently-modified pour_*.log in library-onboarding, if any."""
    logs = sorted(C.LIB.glob("pour_*.log"), key=lambda p: p.stat().st_mtime, reverse=True)
    return logs[0] if logs else None


def _fetch_freshness(conn):
    try:
        return C.dicts(conn,
                       "SELECT SOURCE_ID, FRESHNESS_STATE, DATA_AGE_DAYS, CADENCE_BUCKET "
                       "FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS")
    except Exception:
        return []


def _fetch_queues(conn, vstate):
    """The three 'your to-do' counts. Each is independently best-effort."""
    q = {"leads_pending": None, "review_queue": None, "unclassified": None}
    # leads pending review = active leads minus leads already decided
    active = leads_active_total(vstate)
    try:
        decided = C.scalar(conn,
                           'SELECT COUNT(DISTINCT TARGET_ID) FROM LIBRARY_META."CONNECT".DECISIONS '
                           "WHERE TARGET_KIND = %s", ("lead",))
        q["leads_pending"] = max(0, active - _int(decided))
    except Exception:
        q["leads_pending"] = active or None
    try:
        q["review_queue"] = _int(C.scalar(conn, "SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.V_REVIEW_QUEUE"))
    except Exception:
        pass
    try:
        q["unclassified"] = _int(C.scalar(conn,
                                          "SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.CATALOG "
                                          "WHERE LIFECYCLE IN ('landed','modeled') "
                                          "AND DOMAIN_PRIMARY = 'UNCLASSIFIED'"))
    except Exception:
        pass
    return q


def _fetch_since(conn, vstate):
    """Build the current snapshot and diff it against the saved one. Newly-landed /
    newly-failed come from INGEST_RUNS rows that ended after the last snapshot's ts."""
    prev = C.load_state()
    since_ts = prev.get("ts") if prev else None

    success_ids, failed_ids = [], []
    if conn is not None:
        try:
            if since_ts:
                sql = ("SELECT SOURCE_ID, STATUS FROM LIBRARY_META.INGEST_LOGS.INGEST_RUNS "
                       "WHERE ENDED_AT > %s")
                recent = C.dicts(conn, sql, (since_ts,))
            else:
                recent = []
            success_ids = sorted({r["SOURCE_ID"] for r in recent if str(r.get("STATUS")) == "success"})
            failed_ids = sorted({r["SOURCE_ID"] for r in recent
                                 if str(r.get("STATUS")) in ("failed", "error")})
        except Exception:
            success_ids, failed_ids = [], []

    cur = {
        "ts": C.now_iso(),
        "metrics": {**(vstate or {}), "leads.total.active": leads_active_total(vstate)},
        # carry forward the running set so the diff shows deltas, not just this-window rows
        "success_ids": sorted(set(prev.get("success_ids") or []) | set(success_ids)),
        "failed_ids": sorted(set(prev.get("failed_ids") or []) | set(failed_ids)),
    }
    # Diff uses this window's fresh ids against the prior running set.
    window = {"newly_landed": success_ids, "newly_failed": failed_ids}
    if not prev:
        diff = {"first_run": True, "newly_landed": [], "newly_failed": [], "deltas": {}}
    else:
        diff = since_diff(prev, {"metrics": cur["metrics"],
                                 "success_ids": cur["success_ids"],
                                 "failed_ids": cur["failed_ids"]})
        # Prefer the actual INGEST_RUNS window for the human-facing lists.
        diff["newly_landed"] = window["newly_landed"] or diff["newly_landed"]
        diff["newly_failed"] = window["newly_failed"] or diff["newly_failed"]
    return diff, cur


def _fetch_budget(conn):
    """(quota, used, headroom_to_90pct) via loadkit.preflight; graceful on failure."""
    try:
        from loadkit import preflight
        quota, used = preflight.live_budget_credits(conn)
    except Exception:
        return None
    if not quota:
        return None
    suspend_at = quota * 0.90
    return {"quota": quota, "used": used, "headroom": suspend_at - used, "suspend_at": suspend_at}


def _fetch_health(fresh_rows):
    """PAT days-left + a 'dead freshness present?' flag, both best-effort."""
    h = {"pat_msg": None, "pat_ok": None, "dead": 0}
    try:
        from loadkit import preflight
        exp = preflight.live_pat_expiry()
        chk = preflight.pat_expiry_check(exp, C.now())
        h["pat_msg"] = chk.detail
        h["pat_ok"] = chk.ok and not getattr(chk, "warn", False)
    except Exception:
        pass
    h["dead"] = sum(1 for r in (fresh_rows or [])
                    if str(r.get("FRESHNESS_STATE", "") or "").lower() == "dead")
    return h


# --------------------------------------------------------------- rendering
def _fmt_pour_header(cmdline, tally, position):
    """'POUR LIVE: 72/720 - 39 done / 29 failed / 4 need-keys' plus queue path if any."""
    if position:
        pos = f"{position[0]}/{position[1]}"
    elif tally["total"]:
        pos = f"{tally['done'] + tally['failed'] + tally['need_keys'] + tally['empty'] + tally['other']}"
    else:
        pos = "?"
    bits = [f"{tally['done']} done", f"{tally['failed']} failed"]
    if tally["need_keys"]:
        bits.append(f"{tally['need_keys']} need-keys")
    if tally["empty"]:
        bits.append(f"{tally['empty']} empty")
    line = f"POUR LIVE: {pos} - " + " / ".join(bits)
    qp = _cmdline_queue_path(cmdline)
    if qp:
        line += f"  (queue: {qp})"
    return line


def _print_scale(vstate):
    print(C.hr())
    print("SCALE")
    if not vstate:
        print(f"  {C.DASH} V_STATE unavailable")
        return
    g = lambda k: C.human_int(vstate.get(k, "?"))
    print(f"  landing:  {g('landing.tables')} tables / {g('landing.rows')} rows")
    print(f"  taps:     {g('taps.landed')} landed / {g('taps.modeled')} modeled / {g('taps.scouted')} scouted")
    # CONNECT_EDGES is the canonical store; it's empty until the next full rebuild, so fall
    # back to the incremental edge count (tagged) rather than reporting a scary "0 edges".
    edges = _int(vstate.get("connect.edges"))
    edges_txt = C.human_int(edges) if edges else f"{C.human_int(vstate.get('connect.edges_inc', 0))} (incremental)"
    print(f"  connect:  {g('connect.entities')} entities / {edges_txt} edges"
          f"    reading-room: {g('reading_room.views')} views")


def _print_freshness(fresh_rows, full):
    print(C.hr())
    print("FRESHNESS")
    if not fresh_rows:
        print(f"  {C.DASH} V_SOURCE_FRESHNESS unavailable")
        return
    roll = freshness_rollup(fresh_rows)
    print("  " + " / ".join(f"{roll[s]} {s}" for s in
                            ("fresh", "due", "overdue", "stale", "dead", "unknown")))
    rot = worst_rotting(fresh_rows, None if full else 8)
    if not rot:
        print(f"  {C.OK} nothing rotting")
        return
    data = [[r.get("SOURCE_ID", "?"),
             str(r.get("FRESHNESS_STATE", "?")),
             C.human_int(r.get("DATA_AGE_DAYS")) if r.get("DATA_AGE_DAYS") is not None else "?",
             str(r.get("CADENCE_BUCKET", "?") or "?")] for r in rot]
    print(C.table(["SOURCE", "STATE", "AGE", "CADENCE"], data))
    if not full and len(worst_rotting(fresh_rows, None)) > len(rot):
        print(f"  ... {len(worst_rotting(fresh_rows, None)) - len(rot)} more (ripple status --full)")


def _print_queues(q):
    print(C.hr())
    print("YOUR TO-DO")
    fmt = lambda v: C.human_int(v) if v is not None else "?"
    print(f"  leads pending review:  {fmt(q['leads_pending'])}")
    print(f"  review queue depth:    {fmt(q['review_queue'])}")
    print(f"  unclassified landed:   {fmt(q['unclassified'])}")


def _print_since(diff):
    print(C.hr())
    print("SINCE LAST TIME")
    if diff.get("first_run"):
        print("  first run - baseline saved")
        return
    nl, nf = diff.get("newly_landed") or [], diff.get("newly_failed") or []
    deltas = diff.get("deltas") or {}
    if not nl and not nf and not deltas:
        print(f"  {C.DASH} nothing new")
        return
    if nl:
        shown = ", ".join(nl[:6]) + (f" (+{len(nl) - 6})" if len(nl) > 6 else "")
        print(f"  {C.OK} newly landed ({len(nl)}): {shown}")
    if nf:
        shown = ", ".join(nf[:6]) + (f" (+{len(nf) - 6})" if len(nf) > 6 else "")
        print(f"  {C.BAD} newly failed ({len(nf)}): {shown}")
    if deltas:
        print("  deltas: " + "  ".join(f"{k} {'+' if v > 0 else ''}{v}" for k, v in deltas.items()))


def _print_budget(b):
    print(C.hr())
    print("BUDGET")
    if not b:
        print(f"  {C.DASH} resource monitor unavailable")
        return
    pct = (b["used"] / b["quota"] * 100) if b["quota"] else 0
    marker = C.OK if b["headroom"] > 0 else C.BAD
    print(f"  {marker} {b['used']:.1f}/{b['quota']:.0f} credits ({pct:.0f}%) - "
          f"~{b['headroom']:.1f} to the 90% suspend line")


def _print_health(h):
    print(C.hr())
    parts = []
    if h.get("pat_msg"):
        marker = C.OK if h.get("pat_ok") else C.WARN
        parts.append(f"{marker} {h['pat_msg']}")
    if h.get("dead"):
        parts.append(f"{C.WARN} {h['dead']} source(s) freshness=dead")
    if not parts:
        parts.append(f"{C.DASH} health unknown (run: ripple doctor)")
    print("HEALTH: " + "   ".join(parts) + "   (full check: ripple doctor)")


# --------------------------------------------------------------- assemble JSON
def _build_json(cmdline, tally, position, vstate, fresh_rows, q, diff, budget, health):
    return {
        "generated_at": C.now_iso(),
        "pour": ({"cmdline": cmdline, "tally": tally,
                  "position": list(position) if position else None} if cmdline else None),
        "scale": {k: vstate.get(k) for k in
                  ("landing.tables", "landing.rows", "taps.landed", "taps.modeled",
                   "taps.scouted", "connect.entities", "connect.edges", "reading_room.views")},
        "freshness": {"rollup": freshness_rollup(fresh_rows),
                      "rotting": worst_rotting(fresh_rows, None)},
        "queues": q,
        "since": diff,
        "budget": budget,
        "health": {"pat_msg": health.get("pat_msg"), "pat_ok": health.get("pat_ok"),
                   "dead": health.get("dead")},
    }


# --------------------------------------------------------------- CLI
def add_arguments(parser) -> None:
    parser.add_argument("--json", action="store_true",
                        help="emit the whole deck as one JSON dict")
    parser.add_argument("--full", action="store_true",
                        help="show the complete rotting-sources list, not just the worst 8")


def run(args) -> int:
    want_json = getattr(args, "json", False)
    full = getattr(args, "full", False)

    # --- pour detection (works even if Snowflake is down) ---
    cmdline = C.pour_running()
    onboarding_log = _read_json(C.LIB / "onboarding_log.json")
    tally = parse_pour_tally(onboarding_log)
    pour_log = _newest_pour_log()
    position = pour_position(_read_text(pour_log)) if pour_log else None

    # --- Snowflake sections (each degrades to empty on failure) ---
    conn = None
    try:
        conn = C.connect()
    except Exception as e:
        if not want_json:
            print(f"{C.WARN} Snowflake unreachable ({type(e).__name__}) - showing offline sections only")

    vstate = C.vstate(conn) if conn is not None else {}
    fresh_rows = _fetch_freshness(conn) if conn is not None else []
    queues = _fetch_queues(conn, vstate) if conn is not None else {
        "leads_pending": None, "review_queue": None, "unclassified": None}
    diff, snapshot = _fetch_since(conn, vstate)
    budget = _fetch_budget(conn) if conn is not None else None
    health = _fetch_health(fresh_rows)

    # Persist the fresh snapshot so the NEXT run can diff (read-only re: Snowflake).
    try:
        C.save_state(snapshot)
    except Exception:
        pass

    if conn is not None:
        try:
            conn.close()
        except Exception:
            pass

    if want_json:
        deck = _build_json(cmdline, tally, position, vstate, fresh_rows,
                           queues, diff, budget, health)
        print(json.dumps(deck, indent=2, default=str))
        return 0

    # --- render the screen ---
    print(C.header(f"RIPPLE - {C.now().strftime('%Y-%m-%d %H:%M UTC')}"))
    if cmdline:
        print("  " + _fmt_pour_header(cmdline, tally, position))
    elif tally["total"]:
        print(f"  {C.DASH} no live pour (last log: {tally['done']} done / {tally['failed']} failed)")
    else:
        print(f"  {C.DASH} no live pour")

    _print_scale(vstate)
    _print_freshness(fresh_rows, full)
    _print_queues(queues)
    _print_since(diff)
    _print_budget(budget)
    _print_health(health)
    print(C.hr())
    return 0
