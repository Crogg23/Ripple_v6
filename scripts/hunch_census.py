"""Lattice census CLI — Hunch Engine step 1. Read-only, metadata-only.

What it does, in order:
  1. Loads the measured lattice inputs from disk (zero Snowflake):
     outputs/connect_fingerprints.json, outputs/connect_graph.json,
     outputs/xref_bridges.csv.
  2. Builds the census with hunch/census.py (pure functions).
  3. Optionally (--with-registry) runs METADATA-ONLY SELECTs on the guarded
     read lane (viz/sqlrun, RIPPLE_READER) to fill blind-spot numbers the
     local files can't know: the landing universe, the mart universe, time
     axes, COLUMN_CATALOG status, declared-tier disagreements. No table
     scans, no LIMIT-10k profiling, no writes to the warehouse — ever.
  4. Writes outputs/hunch_lattice.json + reports/hunch_lattice_census_<date>.md
     and prints the headline numbers.

Guards:
  1. Refuses to run if a required input file is missing (points at the
     connect/ command that regenerates it) — before touching anything.
  2. Offline is the DEFAULT and fully functional; registry-derived fields
     stay null offline, never fabricated.
  3. --with-registry degrades per-probe: a failed probe becomes a blind-spot
     note, never a crash and never a guess.

Usage:
  python scripts/hunch_census.py                  # offline, full census
  python scripts/hunch_census.py --with-registry  # + registry metadata pass
  python scripts/hunch_census.py --sample 20 --seed 20260801
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from hunch import census  # noqa: E402

FINGERPRINTS = REPO / "outputs" / "connect_fingerprints.json"
GRAPH = REPO / "outputs" / "connect_graph.json"
XREF = REPO / "outputs" / "xref_bridges.csv"
TIER_REVIEW = REPO / "outputs" / "join_key_tier_review.csv"

REGENERATE = {
    FINGERPRINTS: "python -m connect fingerprint",
    GRAPH: "python -m connect discover",
    XREF: "python -m connect xref",
}


def _load_xref(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def registry_pass(fingerprints: dict) -> dict:
    """Metadata-only SELECTs on the guarded read lane. Each probe degrades to
    a note on failure — the census never guesses."""
    from dotenv import load_dotenv
    load_dotenv(REPO / "library-onboarding" / ".env", override=True)
    from viz import sqlrun

    reg: dict = {}

    def probe(label, fn):
        try:
            fn()
        except Exception as exc:                       # degrade, never crash
            reg.setdefault("probe_failures", []).append(f"{label}: {exc}")
            print(f"  [warn] registry probe failed ({label}): {exc}")

    def _landing():
        df, _ = sqlrun.run(
            "SELECT DISTINCT LANDING_FQN FROM LIBRARY_META.REGISTRY.CATALOG "
            "WHERE LIFECYCLE IN ('landed','modeled','sampled') "
            "AND LANDED_ROW_COUNT > 0", limit_rows=100_000)
        landing = {str(f).rsplit(".", 1)[-1].upper() for f in df.iloc[:, 0]}
        reg["landing_universe"] = len(landing)
        reg["unfingerprinted_landing"] = len(landing - {t.upper() for t in fingerprints})

    def _marts():
        df, _ = sqlrun.run(
            "SELECT COUNT(*) FROM LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES "
            "WHERE TABLE_TYPE = 'BASE TABLE'")
        reg["marts_uncovered"] = int(df.iloc[0, 0])

    def _time_axes():
        df, _ = sqlrun.run(
            "SELECT COUNT(*) FROM LIBRARY_META.REGISTRY.V_SOURCE_FRESHNESS "
            "WHERE RECENCY_KIND IS NOT NULL AND RECENCY_KIND <> 'none'")
        reg["time_axis_tables"] = int(df.iloc[0, 0])

    def _column_catalog():
        df, _ = sqlrun.run(
            "SELECT COUNT(*), COUNT(DISTINCT FQN) "
            "FROM LIBRARY_META.REGISTRY.COLUMN_CATALOG")
        rows, fqns = int(df.iloc[0, 0]), int(df.iloc[0, 1])
        reg["column_catalog_status"] = (
            f"provisioned: {rows:,} column rows over {fqns:,} tables"
            if rows else "provisioned but EMPTY (builder not run yet — A16 step 3)")

    probe("landing universe", _landing)
    probe("mart universe", _marts)
    probe("time axes", _time_axes)
    probe("COLUMN_CATALOG", _column_catalog)
    if "column_catalog_status" not in reg and reg.get("probe_failures"):
        reg["column_catalog_status"] = "absent (A16 DDL not run yet)"

    if TIER_REVIEW.exists():
        with open(TIER_REVIEW, newline="", encoding="utf-8") as fh:
            reg["tier_disagreements"] = sum(1 for _ in csv.DictReader(fh))
    return reg


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fingerprints", default=str(FINGERPRINTS))
    ap.add_argument("--graph", default=str(GRAPH))
    ap.add_argument("--xref", default=str(XREF))
    ap.add_argument("--sample", type=int, default=20)
    ap.add_argument("--seed", type=int, default=20260801)
    ap.add_argument("--with-registry", action="store_true",
                    help="add metadata-only registry SELECTs (read lane; no scans)")
    ap.add_argument("--out", default=str(REPO / "outputs" / "hunch_lattice.json"))
    ap.add_argument("--report",
                    default=str(REPO / "reports" / f"hunch_lattice_census_{date.today().isoformat()}.md"))
    args = ap.parse_args()

    inputs = {Path(args.fingerprints): REGENERATE.get(FINGERPRINTS, ""),
              Path(args.graph): REGENERATE.get(GRAPH, ""),
              Path(args.xref): REGENERATE.get(XREF, "")}
    for path, fix in inputs.items():
        if not path.exists():
            print(f"REFUSED: missing input {path}" + (f" — regenerate with: {fix}" if fix else ""))
            return 2

    fingerprints = json.loads(Path(args.fingerprints).read_text(encoding="utf-8"))
    graph = json.loads(Path(args.graph).read_text(encoding="utf-8"))
    xref_rows = _load_xref(Path(args.xref))

    reg = registry_pass(fingerprints) if args.with_registry else None
    result = census.build_census(fingerprints, graph, xref_rows,
                                 sample_n=args.sample, seed=args.seed, registry=reg)

    out, report = Path(args.out), Path(args.report)
    out.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=1, default=str), encoding="utf-8")
    report.write_text(census.render_report(result, generated=date.today().isoformat()),
                      encoding="utf-8")

    roll, ov = result["rollup"], result["verified_overlay"]
    print(f"Distinct comparable table-pairs (strongest tier): {roll['total_distinct_pairs']:,}")
    print("  by tier: " + ", ".join(
        f"{t} {n:,}" for t, n in sorted(roll["distinct_pairs_strongest_tier"].items())))
    print(f"  bridge-only pairs: {roll['bridge_only_pairs']:,}; "
          f"corroborated candidates: {roll['corroborated_candidate_pairs']:,}")
    print(f"  verified already: {ov['verified_in_lattice']:,}; "
          f"never tested: {ov['never_tested']:,}")
    if ov["verified_missing_from_lattice"]:
        print(f"  CENSUS BUG: {len(ov['verified_missing_from_lattice'])} verified edges "
              "are missing from the lattice — see report")
    print(f"json:   {out}")
    print(f"report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
