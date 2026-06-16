#!/usr/bin/env python3
"""Source Onboarding Agent -- entry point.

Onboards a data source into the Library end to end through five foreman-approved
checkpoints: RECON -> SCRIPT -> LOAD -> DBT -> CATALOG.

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
import sys
from pathlib import Path
from typing import Callable, Optional, Tuple
from urllib.parse import urlparse

import checkpoint as cp
from checkpoint import ABORT, EDIT, GO, SKIP
from config import settings
from ingest import generate_ingest_script, run_ingest
from recon import run_recon
from register import register_source
from scaffold_dbt import generate_dbt_models, write_dbt_models
from sources_queue import SOURCES, find_source

LOG_PATH = Path(__file__).resolve().parent / "onboarding_log.json"


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
            # Auto-approve has no human to fix the cause, and any human will
            # eventually give up: bail out rather than retry a failure forever.
            if settings.auto_approve or errors >= 5:
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
# The 5-checkpoint flow for one source
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

    # --- Checkpoint 4: DBT ---------------------------------------------
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
        error_hint="Check Snowflake credentials for RIPPLE_META, then retry.",
    )
    if action != GO:
        return _record(action)

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
    status = {SKIP: "skipped", ABORT: "aborted"}.get(action, "pending")
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


def run_batch() -> int:
    log = load_log()
    total = len(SOURCES)
    cp.info(f"Batch mode: {total} sources in the queue.")
    aborted = False
    for i, source in enumerate(SOURCES, 1):
        name = source["name"]
        if log.get(name, {}).get("status") == "complete":
            cp.info(f"[{i} of {total}] {name} already complete — skipping.")
            continue
        record = onboard_source(source, position=(i, total))
        log[name] = record
        save_log(log)
        if record.get("status") == "aborted":
            aborted = True
            cp.warn("Batch aborted by foreman. Re-run --batch to resume.")
            break

    if not aborted:
        done = sum(1 for r in log.values() if r.get("status") == "complete")
        cp.success(f"Batch finished. {done}/{total} sources complete.")
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
        description="Onboard data sources into the Library through 5 approved checkpoints.",
    )
    p.add_argument("--url", help="Documentation URL of a single source to onboard.")
    p.add_argument("--name", help="Source name (looks up the queue, or labels a --url).")
    p.add_argument("--batch", action="store_true", help="Run the full pre-loaded queue.")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)

    if settings.fake_llm:
        cp.warn("ONBOARD_FAKE_LLM=1 — using offline fixtures, nothing real will be called.")

    if args.batch:
        if args.url or args.name:
            cp.warn("--batch ignores --url/--name; running the full queue.")
        return run_batch()

    source = source_from_args(args.url, args.name)
    if not source:
        build_parser().print_help()
        return 2
    return run_single(source)


if __name__ == "__main__":
    sys.exit(main())
