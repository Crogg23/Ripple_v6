"""Load a connect_graph.json edge list into LIBRARY_META.CONNECT.CONNECT_EDGES.

discover.run() now writes CONNECT_EDGES itself, but this lets you light up (or
refresh) the queryable graph from an ALREADY-COMPUTED JSON without paying for a
full ~1hr rebuild -- e.g. straight after a fresh checkout, or to restore the
canonical table from the regenerable projection.

    python3 scripts/load_connect_graph.py                    # PREVIEW: counts + tier/key mix
    python3 scripts/load_connect_graph.py --apply            # full-replace CONNECT_EDGES
    python3 scripts/load_connect_graph.py --file outputs/connect_graph.json --apply

Full-replace + idempotent: re-running --apply lands the same rows. A_COL/B_COL
are carried so an edge is a real SQL join (A.A_COL = B.B_COL).
"""
from __future__ import annotations

import argparse
import json
import sys
import uuid
import warnings
from collections import Counter
from pathlib import Path

warnings.filterwarnings("ignore")
REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

DEFAULT_JSON = REPO / "outputs" / "connect_graph.json"


def main() -> int:
    ap = argparse.ArgumentParser(description="Load connect_graph.json -> CONNECT_EDGES")
    ap.add_argument("--file", default=str(DEFAULT_JSON), help="graph JSON path")
    ap.add_argument("--apply", action="store_true", help="write (default: preview)")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        raise SystemExit(f"graph JSON not found: {path}")
    graph = json.loads(path.read_text())
    edges = graph.get("edges", [])
    print(f"  source:  {path}  ({path.stat().st_size / 1e6:.1f} MB)")
    print(f"  edges:   {len(edges):,}   nodes: {len(graph.get('nodes', [])):,}")

    tiers = Counter(e.get("tier") for e in edges)
    keys = Counter(e.get("key") for e in edges)
    have_cols = sum(1 for e in edges if e.get("a_col") and e.get("b_col"))
    print(f"  by tier: {dict(tiers.most_common())}")
    print(f"  top keys: {keys.most_common(10)}")
    print(f"  edges with both join columns: {have_cols:,} / {len(edges):,}")

    from connect import db, store

    if not args.apply:
        print("\n  PREVIEW only -- nothing written. Re-run with --apply.")
        return 0

    conn = db.connect()
    try:
        run_id = uuid.uuid4().hex[:16]
        n = store.write_edges(conn, edges, run_id)
        live = int(db.scalar(conn, f"SELECT COUNT(*) FROM {store.cfqn(store.EDGES_TABLE)}") or 0)
        print(f"\n  wrote {n:,} edges -> {store.cfqn(store.EDGES_TABLE)} (run {run_id})")
        print(f"  live row count now: {live:,}")
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
