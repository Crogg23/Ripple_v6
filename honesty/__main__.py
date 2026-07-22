"""CLI: python -m honesty [--manifest PATH] — grade the marts, write artifacts."""

from __future__ import annotations

import argparse
from pathlib import Path

from .report import DEFAULT_MANIFEST, write_artifacts


def main() -> int:
    ap = argparse.ArgumentParser(description="Machine-check mart provenance from the dbt manifest.")
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST),
                    help="path to dbt manifest.json (default: the in-repo target/)")
    args = ap.parse_args()

    manifest = Path(args.manifest)
    if not manifest.exists():
        print(f"HALT: no manifest at {manifest} — run `dbt parse` first (see honesty/README.md).")
        return 2

    payload = write_artifacts(manifest)
    counts: dict[str, int] = {}
    for g in payload["grades"].values():
        counts[g["grade"]] = counts.get(g["grade"], 0) + 1
    print(f"graded {payload['n_marts']} marts from {manifest}")
    print("  " + " · ".join(f"{v} {k}" for k, v in sorted(counts.items())))
    print("wrote honesty/mart_grades.json + honesty/MART_GRADES.md — commit both.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
