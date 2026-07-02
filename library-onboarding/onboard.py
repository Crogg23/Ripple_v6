#!/usr/bin/env python3
"""Source Onboarding Agent -- entry point.

Onboards a data source into the Library end to end through six foreman-approved
checkpoints: RECON -> SCRIPT -> LOAD -> DBT -> REGISTRY -> CONNECT (CONNECT is
best-effort and never downgrades an onboarded source).

    # Single source
    python onboard.py --url https://fred.stlouisfed.org/docs/api/fred/
    python onboard.py --name FRED            # look up a queued source by name

    # Batch -- walk the whole pre-loaded queue, resuming where it left off
    python onboard.py --batch

At every checkpoint you type:  go | edit <feedback> | skip | abort
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from pathlib import Path
from typing import Callable, Optional, Tuple
from urllib.parse import urlparse

import checkpoint as cp
import snow
from checkpoint import ABORT, EDIT, FAILED, GO, SKIP
from config import settings
from ingest import generate_ingest_script, run_ingest
from recon import run_recon
from register import register_source
from scaffold_dbt import generate_dbt_models, write_dbt_models
from sources_queue import SOURCES, find_source

LOG_PATH = Path(__file__).resolve().parent / "onboarding_log.json"

# Land-only pour switch (set by --skip-dbt in main()): skip the DBT checkpoint so a
# breadth pour just LANDS raw data fast; models get built later. Landing, registry,
# and connect still run.
SKIP_DBT = False

# Collision-gate escape (set by --include-landed in main(), same convention as
# registry_batch.py): deliberately re-onboard a source whose SOURCE_ID already has
# a successful ingest run (e.g. a fuller chunked reload of an existing table).
INCLUDE_LANDED = False

# Last stage exception text (truncated), stashed by _run_stage so a 'failed' log
# record can say WHY -- the keyless pour logged 35 failures with no error field.
_LAST_STAGE_ERROR: Optional[str] = None


# ---------------------------------------------------------------------------
# Batch state (onboarding_log.json)
# ---------------------------------------------------------------------------
def load_log() -> dict:
    if LOG_PATH.exists():
        try:
            return json.loads(LOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            # Fail LOUDLY. Silently "starting fresh" here means losing all resume
            # state: completed sources re-run, quarantine counters reset, and a
            # snapshot-replace re-land can clobber good tables. Preserve the
            # evidence and make the foreman decide.
            corrupt = LOG_PATH.with_suffix(LOG_PATH.suffix + ".corrupt")
            try:
                if corrupt.exists():
                    corrupt.unlink()
                LOG_PATH.rename(corrupt)
                moved = f"; moved it aside to {corrupt.name}"
            except OSError:
                moved = " (could not move it aside)"
            raise RuntimeError(
                f"{LOG_PATH.name} is corrupt JSON ({exc}){moved}. Inspect and "
                "repair it (it holds the batch resume state), or delete it to "
                "genuinely start fresh, then re-run."
            ) from exc
    return {}


def save_log(log: dict) -> None:
    # Atomic: write a temp file, then os.replace. A kill mid-write (the NPPES-wipe
    # class of failure) can no longer leave a half-written log that torches resume.
    tmp = LOG_PATH.with_suffix(LOG_PATH.suffix + ".tmp")
    tmp.write_text(json.dumps(log, indent=2), encoding="utf-8")
    os.replace(tmp, LOG_PATH)


def _log_key(source: dict) -> str:
    """Resume-log key: the QUEUE-PINNED source_id when present, else the name.

    Never the recon-minted sid -- the resume decision happens before recon runs,
    so the key must be knowable from the queue entry alone.
    """
    return source.get("source_id") or source["name"]


def _prior_entry(log: dict, source: dict) -> Tuple[str, dict]:
    """Find a source's prior log entry: sid key first, then the legacy name key
    (older pours keyed everything on name). Returns ``(write_key, prior)`` -- the
    caller always WRITES under the sid key, carrying attempts over from a
    name-keyed entry automatically (prior is that entry when it's all we have)."""
    key = _log_key(source)
    if key in log:
        return key, log[key]
    name = source["name"]
    if key != name and name in log:
        return key, log[name]
    return key, {}


def _now() -> str:
    return _dt.datetime.now(_dt.timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Generic checkpoint stage runner
# ---------------------------------------------------------------------------
def _run_stage(
    produce: Callable[[Optional[str]], object],
    render: Callable[[object], None],
    error_hint: str = "",
) -> Tuple[str, object]:
    """Produce an artifact, render it, and capture the foreman's decision.

    ``produce(feedback)`` may raise; on error the foreman can edit/retry/skip/
    abort. ``edit`` re-runs ``produce`` with the feedback text. Returns the
    terminal action (GO/SKIP/ABORT) and the last good artifact (or None).
    """
    global _LAST_STAGE_ERROR
    feedback: Optional[str] = None
    errors = 0
    while True:
        try:
            artifact = produce(feedback)
            errors = 0
        except KeyboardInterrupt:
            return ABORT, None
        except Exception as exc:  # fail loudly, let the foreman decide
            errors += 1
            _LAST_STAGE_ERROR = str(exc)[:500]  # so the log record can say WHY
            cp.error(str(exc))
            if error_hint:
                cp.warn(error_hint)
            # Unattended (auto-approve): no human to fix the cause, so feed the
            # error back as foreman feedback and let the model repair itself, up
            # to ONBOARD_AUTO_REPAIR times before giving up on the source.
            if settings.auto_approve:
                if errors > settings.auto_repair:
                    cp.error(f"Giving up after {settings.auto_repair} auto-repair attempts.")
                    # FAILED (not ABORT): skip THIS source, let the batch continue.
                    return FAILED, None
                cp.warn(f"Auto-repair {errors}/{settings.auto_repair} — feeding the error back to Claude.")
                feedback = (
                    "The previous attempt failed with this error:\n"
                    f"{exc}\n"
                    "Fix it so the step succeeds."
                )
                continue
            # Interactive: any human will eventually give up; cap the retries.
            if errors >= 5:
                cp.error("Giving up on this stage after repeated errors.")
                return ABORT, None
            action, fb = cp.prompt_action()
            if action in (SKIP, ABORT):
                return action, None
            feedback = fb if action == EDIT else None
            continue

        render(artifact)
        action, feedback = cp.prompt_action()
        if action in (GO, SKIP, ABORT):
            return action, artifact
        # EDIT -> loop again with feedback applied


# ---------------------------------------------------------------------------
# Post-RECON gates (non-raising -- they SKIP a source, never crash the pour)
# ---------------------------------------------------------------------------
def _collision_gate(source: dict, config: dict) -> Optional[dict]:
    """Skip a source whose minted SOURCE_ID already has LANDED EVIDENCE.

    One cheap SELECT against INGEST_RUNS for a STATUS='success' row. Gate on
    landed evidence, NOT registry existence -- ~854 scouted registry rows would
    false-skip. Applies to pinned sids too; --include-landed (or an
    'include_landed' pin on the queue entry) is the deliberate-re-land escape.
    This is what fed_us_sec_edgar / fed_us_usaspending_api needed: recon minted a
    fresh sid right next to an already-landed family and nothing stopped it.
    Non-raising: if the check itself fails, the source proceeds (guard, not a
    dependency). Also emits a warn-only line when near-family registry sids exist.
    """
    if settings.fake_llm or not settings.snowflake_ready():
        return None
    if INCLUDE_LANDED or source.get("include_landed"):
        return None
    sid = config["source_id"]
    runs = (f'"{settings.meta_database}"."{settings.ingest_log_schema}"'
            f'."{settings.ingest_log_table}"')
    reg = (f'"{settings.meta_database}"."{settings.registry_schema}"'
           f'."{settings.registry_table}"')
    hit = None
    near: list = []
    try:
        conn = snow.connect()
        try:
            hit = snow.fetch_scalar(
                conn,
                f"SELECT 1 FROM {runs} WHERE SOURCE_ID=%s AND STATUS='success' LIMIT 1",
                (sid,),
            )
            # Near-family smell test (warn-only): existing registry sids sharing
            # this sid's trailing tokens (fed_us_sec_edgar vs fed_sec_edgar_*).
            body = sid.split("_", 1)[-1]
            toks = body.split("_")
            needle = "_".join(toks[-2:]) if len(toks) >= 2 else body
            cur = conn.cursor()
            try:
                cur.execute(
                    f"SELECT SOURCE_ID FROM {reg} WHERE SOURCE_ID LIKE %s "
                    "AND SOURCE_ID <> %s LIMIT 5",
                    (f"%{needle}%", sid),
                )
                near = [r[0] for r in cur.fetchall()]
            finally:
                cur.close()
        finally:
            conn.close()
    except Exception as exc:
        cp.warn(f"Collision check skipped ({exc}).")
        return None
    if near:
        cp.warn(f"{sid}: near-family sids already in the registry "
                f"({', '.join(str(s) for s in near)}) -- check this isn't a "
                "duplicate family before trusting the new sid.")
    if hit:
        cp.warn(f"{sid} already has a successful ingest run -- skipping before "
                "SCRIPT (re-run with --include-landed to re-land it deliberately).")
        return {"status": "already_cataloged", "source_id": sid, "updated_at": _now()}
    return None


def _auth_gate(config: dict) -> Optional[dict]:
    """Skip a keyed source whose key env var is blank -- BEFORE burning codegen.

    Recon measured the auth requirement and named the conventional env var
    (auth.env_var, new in the recon prompt; older outputs lack it and pass this
    gate untouched). The skip records the env var so a resume retries the source
    ONLY once the key actually appears. Best-effort writeback of the measured
    requirement to SOURCE_REGISTRY.AUTH_REQUIRED via a targeted UPDATE -- never
    the register MERGE, which would clobber curated facets. ~15 of the keyless
    pour's 35 failures were this class of dead-on-arrival source.
    """
    if settings.fake_llm:
        return None
    auth = config.get("auth") or {}
    auth_type = str(auth.get("type") or "none").strip().lower()
    env_var = str(auth.get("env_var") or "").strip()
    if auth_type in ("", "none") or not env_var:
        return None
    if os.environ.get(env_var, "").strip():
        return None  # key present -- proceed to SCRIPT
    if settings.snowflake_ready():
        try:
            conn = snow.connect()
            try:
                reg = (f'"{settings.meta_database}"."{settings.registry_schema}"'
                       f'."{settings.registry_table}"')
                # Targeted UPDATE: a no-op when the row doesn't exist yet.
                snow.execute(conn,
                             f"UPDATE {reg} SET AUTH_REQUIRED=%s WHERE SOURCE_ID=%s",
                             (str(auth.get("type") or ""), config["source_id"]))
            finally:
                conn.close()
        except Exception as exc:
            cp.warn(f"AUTH_REQUIRED writeback skipped ({exc}).")
    cp.warn(f"{config['source_id']} needs {auth.get('type')} but {env_var} is not "
            "set -- skipping before SCRIPT (set it in .env; the batch retries "
            "automatically once the key appears).")
    return {
        "status": "needs_key",
        "source_id": config["source_id"],
        "needs_env_var": env_var,
        "auth_type": str(auth.get("type") or ""),
        "updated_at": _now(),
    }


# ---------------------------------------------------------------------------
# The 6-checkpoint flow for one source
# ---------------------------------------------------------------------------
def onboard_source(source: dict, position=None) -> dict:
    """Run the full flow for one source. Returns a log record."""
    global _LAST_STAGE_ERROR
    _LAST_STAGE_ERROR = None
    name = source["name"]
    cp.info(f"\nOnboarding [bold]{name}[/bold] — {source['url']}")
    state: dict = {"code": None}

    # --- Checkpoint 1: RECON -------------------------------------------
    def _recon(fb):
        cfg = run_recon(source, feedback=fb)
        auth = cfg.get("auth", {})
        if auth.get("type", "none") != "none":
            cp.warn(
                f"This source needs {auth['type']}. {auth.get('notes','')} "
                "Set the key in .env before the LOAD checkpoint."
            )
        return cfg

    action, config = _run_stage(_recon, lambda c: cp.render_recon(c, position))
    if action != GO:
        return _record(action)

    # --- Gates between RECON and SCRIPT (non-raising skips) ------------
    # Here, not inside _resolve/produce, so registry_batch.py / live_batch.py
    # callers (which call onboard_source directly) are covered too.
    gate = _collision_gate(source, config) or _auth_gate(config)
    if gate:
        return gate

    # --- Checkpoint 2: SCRIPT ------------------------------------------
    def _script(fb):
        code = generate_ingest_script(config, feedback=fb)
        state["code"] = code
        return code

    action, _ = _run_stage(_script, lambda code: cp.render_script(config, code, position))
    if action != GO:
        return _record(action)

    # --- Checkpoint 3: LOAD --------------------------------------------
    def _load(fb):
        if fb:  # adjust the script, then re-run
            state["code"] = generate_ingest_script(config, feedback=fb)
            cp.render_script(config, state["code"], position)
        return run_ingest(config, state["code"])

    action, load_result = _run_stage(
        _load,
        lambda r: cp.render_load(config, r, position),
        error_hint="Check Snowflake credentials / source schema, then edit or retry.",
    )
    if action != GO:
        return _record(action)

    # --- EMPTY GATE: the load landed but carried no real data ----------
    # A density-demoted load (INGEST_RUNS STATUS='empty') must not ride into dbt
    # models or a registry row -- that's exactly how fed_dea_arcos and
    # fed_ed_fsa_datacenter retired as 'complete' while holding nothing. Record
    # it as 'empty'; the batch counts it toward quarantine like a failure.
    if (load_result or {}).get("empty"):
        cp.warn(f"{name}: empty load -- skipping DBT + REGISTRY (status='empty').")
        return {
            "status": "empty",
            "source_id": config["source_id"],
            "landing_table": config["landing_table"],
            "run_id": (load_result or {}).get("run_id"),
            "message": (load_result or {}).get("status", ""),
            "updated_at": _now(),
        }

    # --- Checkpoint 4: DBT (skipped in a --skip-dbt land-only pour) ----
    if not SKIP_DBT:
        def _dbt(fb):
            models = generate_dbt_models(config, feedback=fb)
            return write_dbt_models(config, models)

        action, _ = _run_stage(
            _dbt,
            lambda files: cp.render_dbt(config, files, position),
            error_hint="Set DBT_PROJECT_PATH to your dbt project root, then retry.",
        )
        if action != GO:
            return _record(action)

    # --- Checkpoint 5: REGISTRY ----------------------------------------
    action, _ = _run_stage(
        lambda fb: register_source(config),
        lambda r: cp.render_registry(config, r, position),
        error_hint="Check Snowflake credentials for LIBRARY_META, then retry.",
    )
    if action != GO:
        return _record(action)

    # --- Checkpoint 6: CONNECT (incremental link of the just-landed table) -----
    # The source is already onboarded + registered; linking is BEST-EFFORT and
    # never downgrades it. Fire only when the load actually changed the table:
    # live, not a skip/dry-run, not demoted-empty, and rows > 0.
    _lr = load_result or {}
    _landed = bool(_lr) and not _lr.get("skipped") and not _lr.get("empty") and (_lr.get("rows") or 0) > 0
    if _landed:
        def _connect(fb):
            from connect_hook import connect_one
            return connect_one(config["source_id"], config["landing_table"])
        # Run through the normal stage UX, but IGNORE the action — a non-GO here
        # must not mark an already-registered source incomplete.
        _run_stage(
            _connect,
            lambda r: cp.render_connect(config, r, position),
            error_hint="Check LIBRARY_META.CONNECT perms; `connect connect-changed` will retry.",
        )

    cp.success(f"{name} onboarded -> SOURCE_ID {config['source_id']} ({config['landing_table']})")
    return {
        "status": "complete",
        "source_id": config["source_id"],
        "landing_table": config["landing_table"],
        "run_id": (load_result or {}).get("run_id"),
        "staging_model": config["staging_model"],
        "mart_model": config["mart_model"],
        "completed_at": _now(),
    }


def _record(action: str) -> dict:
    status = {SKIP: "skipped", ABORT: "aborted", FAILED: "failed"}.get(action, "pending")
    cp.warn(f"Source {status}.")
    rec = {"status": status, "updated_at": _now()}
    if status == "failed" and _LAST_STAGE_ERROR:
        rec["error"] = _LAST_STAGE_ERROR  # truncated stage error: the WHY
    return rec


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------
def run_single(source: dict) -> int:
    record = onboard_source(source, position=None)
    log = load_log()
    key, prior = _prior_entry(log, source)  # sid-first keying, name fallback
    if record.get("status") in ("failed", "empty"):
        record["attempts"] = int(prior.get("attempts", 0)) + 1
    log[key] = record
    save_log(log)
    return 0 if record.get("status") in ("complete", "skipped", "already_cataloged") else 1


def _budget_preflight() -> None:
    """Visibility, not a hard block (the foreman decides): read RIPPLE_BUDGET and warn
    up front if a large pour is likely to hit the 90% suspend line mid-flight -- so the
    first signal isn't a silently-dead pour at 90%."""
    if settings.fake_llm or not settings.snowflake_ready():
        return
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # repo root for loadkit
        from loadkit.preflight import live_budget_credits
        conn = snow.connect()
        try:
            quota, used = live_budget_credits(conn)
        finally:
            conn.close()
        if not quota:
            return
        headroom = quota * 0.90 - used
        cp.info(f"Budget: {used:.1f}/{quota:.0f} credits used; ~{headroom:.1f} to the 90% suspend line.")
        if headroom < 15:
            cp.warn(
                f"LOW BUDGET HEADROOM (~{headroom:.1f} cr). A large pour may trip RIPPLE_BUDGET "
                "and suspend the warehouse mid-load. Raise it first via the governed tool "
                "(python scripts/budget_sprint.py — restore to steady-state after the sprint)."
            )
    except Exception as exc:
        cp.warn(f"Budget preflight skipped ({exc}).")
    # PAT calendar gate: the pour dies silently when the token expires (~2026-09-20), so warn
    # while there's still time to rotate. Advisory only — the foreman decides.
    try:
        from loadkit.preflight import live_pat_expiry, pat_expiry_check
        check = pat_expiry_check(live_pat_expiry())
        if check.blocked:
            cp.error(f"PAT EXPIRY: {check.reason} — rotate before pouring (see infra/keys_ledger.json).")
        elif getattr(check, "warn", False):
            cp.warn(f"PAT expiry: {check.reason}")
    except Exception as exc:
        cp.warn(f"PAT-expiry preflight skipped ({exc}).")


def run_batch(sources: Optional[list] = None, limit: Optional[int] = None) -> int:
    # Unattended pour needs auto-approve; a detached/redirected run has no TTY, so
    # the interactive prompt would EOF-abort on source #1. Fail fast and loud.
    if not settings.auto_approve and not sys.stdin.isatty():
        cp.error(
            "Unattended batch has no interactive stdin. Re-run with --yes "
            "(or set ONBOARD_AUTO_APPROVE=1 in .env) to pour without babysitting."
        )
        return 2

    _budget_preflight()
    log = load_log()
    queue = SOURCES if sources is None else sources
    total = len(queue)
    cp.info(f"Batch mode: {total} sources in the queue"
            + (f" (this wave: up to {limit} not-yet-complete)." if limit else "."))
    aborted = False
    attempted = 0  # sources actually onboarded this run (skips don't count toward --limit)
    # Per-RUN counters: the exit code must reflect THIS run only -- the shared log
    # carries failures from earlier pours that this run legitimately skipped.
    counts = {"complete": 0, "failed": 0, "needs_key": 0, "empty": 0,
              "already_cataloged": 0, "other": 0}
    for i, source in enumerate(queue, 1):
        name = source["name"]
        key, prior = _prior_entry(log, source)  # sid-first keying, name fallback
        status = prior.get("status")
        # Terminal statuses: done is done; already-cataloged means it landed via
        # another route -- re-running would just re-skip after burning recon.
        if status in ("complete", "already_cataloged"):
            cp.info(f"[{i} of {total}] {name} already {status} -- skipping.")
            continue
        # Quarantine a repeatedly-dead source so re-runs don't burn spend on it.
        # 'empty' counts like 'failed': a density-demoted load is a failure to land
        # real data, and it retries the same way until max_attempts.
        if status in ("failed", "empty") and prior.get("attempts", 1) >= settings.max_attempts:
            cp.warn(f"[{i} of {total}] {name} quarantined after {prior.get('attempts')} "
                    f"{status} attempts -- skipping. Delete its onboarding_log.json "
                    "entry to retry.")
            continue
        # needs_key: retry ONLY once its recorded env var actually holds a value --
        # otherwise every pour re-burns recon on a source that can only skip again.
        if status == "needs_key":
            env_var = str(prior.get("needs_env_var") or "").strip()
            if not (env_var and os.environ.get(env_var, "").strip()):
                cp.info(f"[{i} of {total}] {name} waiting on {env_var or 'an API key'} "
                        "-- skipping (set it in .env to retry).")
                continue
            cp.info(f"[{i} of {total}] {name}: {env_var} is now set -- retrying.")
        if limit is not None and attempted >= limit:
            cp.info(f"Reached --limit {limit} for this wave -- stopping. Re-run to continue.")
            break
        attempted += 1
        try:
            record = onboard_source(source, position=(i, total))
        except KeyboardInterrupt:
            cp.warn("Interrupted by foreman. Re-run --batch to resume.")
            aborted = True
            break
        except Exception as exc:  # a crash OUTSIDE a stage must not kill the pour
            cp.error(f"{name} crashed: {exc}")
            record = {"status": "failed", "error": str(exc)[:500], "updated_at": _now()}
        rstatus = record.get("status")
        if rstatus in ("failed", "empty"):  # carry a running attempt count
            record["attempts"] = int(prior.get("attempts", 0)) + 1
        counts[rstatus if rstatus in counts else "other"] += 1
        log[key] = record
        save_log(log)
        if rstatus == "aborted":  # a real human abort inside a stage
            aborted = True
            cp.warn("Batch aborted by foreman. Re-run --batch to resume.")
            break
        # 'failed' / 'skipped' / 'pending' -> skip and CONTINUE the pour; a re-run
        # retries them (only the terminal statuses are skipped above).

    done = sum(1 for r in log.values() if r.get("status") == "complete")
    failed = sum(1 for r in log.values() if r.get("status") == "failed")
    this_run = ", ".join(f"{k}={v}" for k, v in counts.items() if v) or "nothing attempted"
    if aborted:
        cp.warn(f"Batch stopped. {done}/{total} complete, {failed} failed so far "
                f"(this run: {this_run}). Re-run --batch to resume.")
    else:
        cp.success(
            f"Batch finished. {done}/{total} complete"
            + (f", {failed} failed (re-run --batch to retry them)" if failed else "")
            + f" (this run: {this_run})."
        )
    # Exit code from THIS run only: nonzero means something actually BROKE now.
    # needs_key / empty are recorded, actionable outcomes -- not pour breakage.
    return 1 if counts["failed"] > 0 else 0


def source_from_args(url: Optional[str], name: Optional[str]) -> Optional[dict]:
    """Resolve CLI args into a source dict, preferring the curated queue entry."""
    if name:
        queued = find_source(name)
        if queued:
            return queued
    if url:
        queued = find_source(url)
        if queued:
            return queued
        derived = name or urlparse(url).netloc.replace("www.", "").split(".")[0].upper()
        return {"name": derived, "url": url, "layer": "unknown", "identifiers": []}
    if name:  # name given but not in queue, no url
        cp.error(f"'{name}' is not in the queue and no --url was given.")
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="onboard.py",
        description="Onboard data sources into the Library through 6 approved checkpoints.",
    )
    p.add_argument("--url", help="Documentation URL of a single source to onboard.")
    p.add_argument("--name", help="Source name (looks up the queue, or labels a --url).")
    p.add_argument("--batch", action="store_true", help="Run the full pre-loaded queue.")
    p.add_argument(
        "--queue", metavar="PATH",
        help="Batch from an external JSON queue file (list of {name,url,source_id,"
             "jurisdiction,identifiers}) instead of the built-in sources_queue. "
             "Resumes via the same onboarding_log.json (keyed on the pinned "
             "source_id when present, else name).",
    )
    p.add_argument(
        "--limit", type=int, metavar="N",
        help="Batch: onboard at most N not-yet-complete sources this run (wave pacing). "
             "Re-run to continue; complete sources are skipped.",
    )
    p.add_argument(
        "--yes", "--auto", dest="auto", action="store_true",
        help="Unattended: auto-approve every checkpoint (implies ONBOARD_AUTO_APPROVE=1).",
    )
    p.add_argument(
        "--skip-dbt", action="store_true",
        help="Land-only pour: skip DBT model generation (build models later). Landing + "
             "registry + connect still run. Much faster per source.",
    )
    p.add_argument(
        "--repair", type=int, metavar="N",
        help="Cap unattended auto-repair attempts per stage (overrides ONBOARD_AUTO_REPAIR; "
             "--repair 1 gives up fast on dead sources instead of burning 3 tries).",
    )
    p.add_argument(
        "--include-landed", action="store_true",
        help="Collision-gate escape: onboard a source even when its SOURCE_ID already "
             "has a successful ingest run (a deliberate re-land). Same convention as "
             "registry_batch.py.",
    )
    return p


def _load_queue(path: str) -> list:
    """Load + validate an external batch queue (JSON list of source entries)."""
    p = Path(path).expanduser()
    if not p.exists():
        raise SystemExit(f"--queue file not found: {p}")
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"--queue file is not valid JSON: {exc}")
    if not isinstance(data, list) or not data:
        raise SystemExit("--queue file must be a non-empty JSON list of source entries.")
    seen = set()
    seen_sids = set()
    for i, e in enumerate(data):
        if not isinstance(e, dict) or not e.get("name") or not e.get("url"):
            raise SystemExit(f"--queue entry {i} must have at least 'name' and 'url'.")
        if e["name"] in seen:
            raise SystemExit(f"--queue has a duplicate name ('{e['name']}') -- names must be "
                             "unique (they key the resume log).")
        seen.add(e["name"])
        # Pinned sids key the resume log too (sid-first) -- two entries sharing one
        # sid would silently overwrite each other's resume state.
        sid = str(e.get("source_id") or "").strip()
        if sid:
            if sid in seen_sids:
                raise SystemExit(f"--queue has a duplicate source_id ('{sid}') -- pinned "
                                 "sids must be unique (they key the resume log).")
            seen_sids.add(sid)
    return data


def main(argv=None) -> int:
    global SKIP_DBT, INCLUDE_LANDED
    args = build_parser().parse_args(argv)

    # Unattended pour switch: set the env AND the live setting (settings is already
    # instantiated at import, so the env var alone wouldn't take effect this run).
    if args.auto:
        os.environ["ONBOARD_AUTO_APPROVE"] = "1"
        settings.auto_approve = True
        cp.info("Unattended mode (--yes): every checkpoint auto-approves.")

    # Speed switches for a breadth pour (land now, model later; fail fast on the dead).
    if args.skip_dbt:
        SKIP_DBT = True
        cp.info("Land-only mode (--skip-dbt): DBT model generation skipped.")
    if args.repair is not None:
        settings.auto_repair = max(0, args.repair)
        cp.info(f"Auto-repair capped at {settings.auto_repair} attempt(s).")
    if args.include_landed:
        INCLUDE_LANDED = True
        cp.info("--include-landed: collision gate off (deliberate re-land).")

    if settings.fake_llm:
        cp.warn("ONBOARD_FAKE_LLM=1 - using offline fixtures, nothing real will be called.")

    # Fail fast on a real pour with no LLM key, instead of aborting per-source after
    # burning auto-repair retries on an error the model can never fix.
    if not settings.fake_llm and (args.batch or args.url or args.name):
        try:
            settings.require("anthropic_api_key")
        except Exception as exc:
            cp.error(str(exc))
            return 2

    if args.queue and not args.batch:
        args.batch = True  # --queue implies a batch run

    if args.batch:
        if args.url or args.name:
            cp.warn("--batch ignores --url/--name; running the full queue.")
        sources = _load_queue(args.queue) if args.queue else None
        return run_batch(sources=sources, limit=args.limit)

    source = source_from_args(args.url, args.name)
    if not source:
        build_parser().print_help()
        return 2
    return run_single(source)


if __name__ == "__main__":
    sys.exit(main())
