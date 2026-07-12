#!/usr/bin/env python3
"""Run every open defect's evidence check and report still_broken / clear.

Move 2 of RIPPLE_GOVERN_THYSELF (2026-07-12). The defect registry
(LIBRARY_META.BUILD.DEFECTS) stores, per defect, an EVIDENCE_SQL that returns
rows WHILE BROKEN and zero rows when fixed. This script runs them all and
reports. THE VERIFIER NEVER CLOSES A DEFECT — a 'clear' verdict is a
recommendation; only Chris flips STATUS (CLOSED_BY is always a human).

    python3 scripts/verify_defects.py            # verify + print (no writes)
    python3 scripts/verify_defects.py --apply    # also stamp LAST_VERIFIED_AT /
                                                 # LAST_VERDICT / LAST_ROWCOUNT

Verify methods:
  sql        — EVIDENCE_SQL runs against the warehouse (';'-separated statements
               allowed: SHOW ...; SELECT ... FROM TABLE(RESULT_SCAN(LAST_QUERY_ID())))
  filesystem — a named check in FS_CHECKS below (repo state, not warehouse state)
  human      — skipped; needs eyes, not a query

Reader-lane note: verification itself is read-only and runs fine on the READER
PAT. --apply needs UPDATE on LIBRARY_META.BUILD.DEFECTS (a write-lane token).
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "library-onboarding"))


# ── filesystem evidence checks ──────────────────────────────────────────────
# Each returns an int "rowcount": >0 = still broken, 0 = clear.
# Keyed by DEFECT title slug (the stable part of the content-addressed ID).

def _read(p: Path) -> str:
    try:
        return p.read_text(errors="replace")
    except OSError:
        return ""


def fs_build_state_hand_typed() -> int:
    return 0 if "GENERATED FILE. DO NOT EDIT" in _read(REPO / "build-state.md") else 1


def fs_env_source_keys_missing() -> int:
    env = _read(REPO / "library-onboarding" / ".env")
    keys = ["CENSUS_API_KEY", "COURTLISTENER_TOKEN", "SOCRATA_APP_TOKEN", "RIPPLE_CONTACT_UA"]
    return sum(1 for k in keys if not re.search(rf"^{k}=.+", env, re.M))


def fs_keys_ledger_stale() -> int:
    return 0 if '"programmatic_access_tokens"' in _read(REPO / "infra" / "keys_ledger.json") else 1


def fs_evidence_dev_read_lane_dark() -> int:
    conn_yaml = _read(REPO / "evidence" / "sources" / "library" / "connection.yaml")
    env = _read(REPO / "library-onboarding" / ".env")
    broken = 0
    if "INTERIM LANE" in conn_yaml:
        broken += 1
    if not re.search(r"^SNOWFLAKE_SERVE_PAT=.+", env, re.M):
        broken += 1
    return broken


def fs_append_loaders_partial_silent() -> int:
    n = 0
    for f in ("noaa_ais_backfill.py", "noaa_storm_events_backfill.py"):
        if "leaves a partial" in _read(REPO / "scripts" / f):
            n += 1
    return n


def fs_leads_overlay_stale() -> int:
    # crude but honest: the Jun-27 render baked in "353" leads / 4 detectors
    return 1 if "353" in _read(REPO / "outputs" / "leads_overlay.html") else 0


def fs_cdn_plotly_offline_dead() -> int:
    n = 0
    for f in ("connection_explorer.html", "leads_overlay.html"):
        if "cdn.plot.ly" in _read(REPO / "outputs" / f):
            n += 1
    return n


def fs_ladder_regression_gaps() -> int:
    n = 0
    if not (REPO / "tests" / "fixtures" / "ladder_holdout.parquet").exists():
        n += 1
    if not (REPO / "tests" / "test_ladder_invariants.py").exists():
        n += 1
    return n


def fs_nppes_schema_drift() -> int:
    # FED_CMS_NPPES was re-landed with single-underscore headers; resolve.py's PAIRS
    # spec still carries the old double-underscore column -> resolve/calibrate broken.
    return 1 if "PROVIDER_LAST_NAME__LEGAL_NAME" in _read(REPO / "connect" / "resolve.py") else 0


FS_CHECKS = {
    "build-state.md is hand-typed, not generated": fs_build_state_hand_typed,
    "source API keys still missing from .env": fs_env_source_keys_missing,
    "keys_ledger.json does not track the live PAT population": fs_keys_ledger_stale,
    "evidence.dev read lane is dark (dead interim token)": fs_evidence_dev_read_lane_dark,
    "append-mode loaders leave silent partial loads on crash": fs_append_loaders_partial_silent,
    "leads_overlay.html stale (4 detectors/353 leads vs live 6/1030)": fs_leads_overlay_stale,
    "explorer/overlay HTML pull Plotly from CDN, die offline": fs_cdn_plotly_offline_dead,
    "no ladder regression tests (5 named gaps, no holdout fixture)": fs_ladder_regression_gaps,
    "resolve.py PAIRS spec broken by NPPES re-land (column rename)": fs_nppes_schema_drift,
}


# ── sql evidence runner ─────────────────────────────────────────────────────

def exec_evidence(cur, sql: str) -> int:
    """Execute ';'-separated statements; rowcount of the LAST one is the verdict."""
    rows = []
    for stmt in [s.strip() for s in sql.split(";") if s.strip()]:
        cur.execute(stmt)
        rows = cur.fetchall()
    return len(rows)


def verify_all(conn, apply: bool = False):
    """Yield (defect_id, title, method, verdict, rowcount) for every open defect."""
    cur = conn.cursor()
    cur.execute(
        "SELECT DEFECT_ID, TITLE, VERIFY_METHOD, EVIDENCE_SQL "
        "FROM LIBRARY_META.BUILD.DEFECTS WHERE STATUS='open' ORDER BY SEVERITY, TITLE")
    defects = cur.fetchall()
    results = []
    for defect_id, title, method, evidence_sql in defects:
        if method == "human":
            verdict, n = "needs_human", None
        elif method == "filesystem":
            fn = FS_CHECKS.get(title)
            if fn is None:
                verdict, n = "error", None
            else:
                n = fn()
                verdict = "still_broken" if n > 0 else "clear"
        else:
            try:
                n = exec_evidence(cur, evidence_sql)
                verdict = "still_broken" if n > 0 else "clear"
            except Exception as e:  # noqa: BLE001
                verdict, n = "error", None
                print(f"  ! {title}: {str(e).splitlines()[0]}")
        results.append((defect_id, title, method, verdict, n))
        if apply and verdict != "needs_human":
            cur.execute(
                "UPDATE LIBRARY_META.BUILD.DEFECTS "
                "SET LAST_VERIFIED_AT=CURRENT_TIMESTAMP(), LAST_VERDICT=%s, LAST_ROWCOUNT=%s "
                "WHERE DEFECT_ID=%s", (verdict, n, defect_id))
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description="Verify open defects; never closes them.")
    ap.add_argument("--apply", action="store_true",
                    help="stamp LAST_VERIFIED_AT/LAST_VERDICT/LAST_ROWCOUNT (needs write lane)")
    args = ap.parse_args()

    import snow  # noqa: E402
    conn = snow.connect()
    try:
        results = verify_all(conn, apply=args.apply)
    finally:
        conn.close()

    w = max(len(t) for _, t, _, _, _ in results) if results else 10
    print(f"\n{'TITLE':<{w}}  {'METHOD':<10}  {'VERDICT':<12}  ROWS")
    for _, title, method, verdict, n in results:
        print(f"{title:<{w}}  {method:<10}  {verdict:<12}  {n if n is not None else '-'}")
    broken = sum(1 for r in results if r[3] == "still_broken")
    clear = sum(1 for r in results if r[3] == "clear")
    print(f"\n{len(results)} open defects: {broken} still_broken, {clear} clear "
          f"(clear = recommend close — Chris flips STATUS, never this script)"
          + ("" if args.apply else "   [no writes: preview]"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
