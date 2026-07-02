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


# ---------------------------------------------------------------------------
# Batch state (onboarding_log.json)
# ---------------------------------------------------------------------------
def load_log() -> dict:
    if LOG_PATH.exists():
        try:
            return json.loads(LOG_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cp.warn(f"{LOG_PATH.name} is corrupt; starting fresh.")
    return {}


def save_log(log: dict) -> None:
    LOG_PATH.write_text(json.dumps(log, indent=2), encoding="utf-8")


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
# The 6-checkpoint flow for one source
# ---------------------------------------------------------------------------
def onboard_source(source: dict, position=None) -> dict:
    """Run the full flow for one source. Returns a log record."""
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
    return {"status": status, "updated_at": _now()}


# ---------------------------------------------------------------------------
# Modes
# ---------------------------------------------------------------------------
def run_single(source: dict) -> int:
    record = onboard_source(source, position=None)
    log = load_log()
    log[source["name"]] = record
    save_log(log)
    return 0 if record.get("status") in ("complete", "skipped") else 1


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
                "and suspend the warehouse mid-load. Raise it first (ACCOUNTADMIN):\n"
                "  ALTER RESOURCE MONITOR RIPPLE_BUDGET SET CREDIT_QUOTA = 300;"
            )
    except Exception as exc:
        cp.warn(f"Budget preflight skipped ({exc}).")


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
    for i, source in enumerate(queue, 1):
        name = source["name"]
        prior = log.get(name, {})
        if prior.get("status") == "complete":
            cp.info(f"[{i} of {total}] {name} already complete -- skipping.")
            continue
        # Quarantine a repeatedly-failing source so re-runs don't burn spend on a
        # permanently-dead URL. (Transient failures still retry until max_attempts.)
        if prior.get("status") == "failed" and prior.get("attempts", 1) >= settings.max_attempts:
            cp.warn(f"[{i} of {total}] {name} quarantined after {prior.get('attempts')} failed "
                    f"attempts -- skipping. Delete its onboarding_log.json entry to retry.")
            continue
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
            record = {"status": "failed", "error": str(exc), "updated_at": _now()}
        if record.get("status") == "failed":  # carry a running attempt count
            record["attempts"] = int(prior.get("attempts", 0)) + 1
        log[name] = record
        save_log(log)
        if record.get("status") == "aborted":  # a real human abort inside a stage
            aborted = True
            cp.warn("Batch aborted by foreman. Re-run --batch to resume.")
            break
        # 'failed' / 'skipped' / 'pending' -> skip and CONTINUE the pour; a re-run
        # retries them (only 'complete' is skipped above).

    done = sum(1 for r in log.values() if r.get("status") == "complete")
    failed = sum(1 for r in log.values() if r.get("status") == "failed")
    if aborted:
        cp.warn(f"Batch stopped. {done}/{total} complete, {failed} failed so far. Re-run --batch to resume.")
    else:
        cp.success(
            f"Batch finished. {done}/{total} complete"
            + (f", {failed} failed (re-run --batch to retry them)." if failed else ".")
        )
    return 0


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
             "Resumes via the same onboarding_log.json (keyed on name).",
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
    for i, e in enumerate(data):
        if not isinstance(e, dict) or not e.get("name") or not e.get("url"):
            raise SystemExit(f"--queue entry {i} must have at least 'name' and 'url'.")
        if e["name"] in seen:
            raise SystemExit(f"--queue has a duplicate name ('{e['name']}') -- names must be "
                             "unique (they key the resume log).")
        seen.add(e["name"])
    return data


def main(argv=None) -> int:
    global SKIP_DBT
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
