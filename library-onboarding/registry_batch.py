#!/usr/bin/env python3
"""Registry-driven live batch -- onboard candidates straight from the catalog.

Where ``live_batch.py`` walks a hand-curated SOURCES list, this walks the live
``LIBRARY_META.REGISTRY.SOURCE_REGISTRY`` (~900 sources), prioritized by
``PRIORITY_TIER`` and skipping anything already onboarded or landed. The catalog
drives the queue -- the scaling unlock for getting to hundreds of sources.

Safe by default: with no ``--run`` it only PREVIEWS the selected queue (read-only).
Add ``--run`` to actually onboard them through the full unattended agent
(RECON -> SCRIPT -> LOAD -> DBT -> REGISTRY, auto-approve + auto-repair).

    python registry_batch.py                          # preview the top 5 (read-only)
    python registry_batch.py --tier 1 --limit 10      # preview top 10 tier-1
    python registry_batch.py --source-id fed_oyez --run   # onboard one vetted candidate
    python registry_batch.py --limit 3 --run          # onboard the top 3 (live)
"""

from __future__ import annotations

import argparse
import os

# --- environment: unattended, live, with the scaffolded dbt project ---------
os.environ["ONBOARD_AUTO_APPROVE"] = "1"
os.environ.setdefault("ONBOARD_AUTO_REPAIR", "3")
if not os.environ.get("SNOWFLAKE_WAREHOUSE", "").strip():
    os.environ["SNOWFLAKE_WAREHOUSE"] = "RIPPLE_WH"
if not os.environ.get("DBT_PROJECT_PATH", "").strip():
    os.environ["DBT_PROJECT_PATH"] = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ripple_dbt")

import checkpoint as cp  # noqa: E402
import registry_queue  # noqa: E402
from onboard import onboard_source  # noqa: E402


def _preview(candidates: list) -> None:
    cp.info("=" * 70)
    for i, s in enumerate(candidates, 1):
        idents = ", ".join(s.get("identifiers", [])) or "(none)"
        cp.info(f"  [{i:>2}] tier {s.get('_tier','?')}  {s['source_id']}")
        cp.info(f"       {s['name'][:64]}")
        cp.info(f"       {s.get('_access_method','')} | {s.get('_format','')} | keys: {idents}")
        cp.info(f"       {s['url']}")
    cp.info("=" * 70)


def main() -> int:
    p = argparse.ArgumentParser(prog="registry_batch.py", description=__doc__)
    p.add_argument("--limit", type=int, default=5, help="max candidates (default 5).")
    p.add_argument("--tier", help="filter to one PRIORITY_TIER (e.g. 1).")
    p.add_argument("--jurisdiction", help="federal / international / cross-cutting / local / state.")
    p.add_argument("--source-id", help="target one specific candidate SOURCE_ID.")
    p.add_argument("--auth", default="none", choices=["none", "no-secret", "any"],
                   help="auth policy. 'none' (default) is the only fully-unattended-safe set.")
    p.add_argument("--include-landed", action="store_true",
                   help="don't skip sources that already have a successful ingest run.")
    p.add_argument("--run", action="store_true",
                   help="actually onboard (default is a read-only preview).")
    args = p.parse_args()

    candidates = registry_queue.fetch_candidates(
        limit=args.limit, tier=args.tier, jurisdiction=args.jurisdiction,
        source_id=args.source_id, auth=args.auth, include_landed=args.include_landed,
    )
    if not candidates:
        cp.warn("No candidates matched -- the registry queue is drained for these filters.")
        return 0

    scope = f"tier={args.tier or 'all'} jurisdiction={args.jurisdiction or 'all'} auth={args.auth}"
    cp.info(f"Registry queue: {len(candidates)} candidate(s)  [{scope}]")
    _preview(candidates)

    if not args.run:
        cp.info("(preview only -- nothing onboarded. Add --run to onboard these.)")
        return 0

    results = []
    total = len(candidates)
    for i, source in enumerate(candidates, 1):
        record = onboard_source(source, position=(i, total))
        results.append((source["source_id"], record))

    cp.info("\n" + "=" * 70)
    cp.info("REGISTRY BATCH SUMMARY")
    cp.info("=" * 70)
    for sid, rec in results:
        cp.info(f"  {rec.get('status','?'):<9} {sid}  run={(rec.get('run_id') or '')[:8]}")
    complete = sum(1 for _, r in results if r.get("status") == "complete")
    cp.info(f"\n{complete}/{total} complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
