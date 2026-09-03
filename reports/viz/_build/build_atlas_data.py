"""Build atlas_data.json — the one payload behind reports/viz/atlas.html.

Three layers:
  paved  — the measured edges from handbook_pass2_edges_2026-08-29.csv
           (self-loop rows dropped: an intra-table edge is not a road)
  ghost  — same strong key on both sides, never measured (candidates)
  spokes — table -> key membership from KEYSET_LIVE (drawn as hub glow)

Weak keys (ZIP, NAME@ZIP, COUNTRY, NAME, ADDRESS) never make ghost roads —
sharing a zip column is not a join candidate.

Card fields come from SOURCE_REGISTRY. Trap: landing name != UPPER(SOURCE_ID)
in general, so the match is exact-uppercase first, then LIKE fallback, and a
miss just means a thinner card (name only). VOLUME is free-text prose, not a
count — it is not used.

Run:  python reports/viz/_build/build_atlas_data.py
Reads the warehouse twice (keyset + registry), both tiny metadata reads.
"""

from __future__ import annotations

import csv
import json
from itertools import combinations
from pathlib import Path

BUILD = Path(__file__).resolve().parent
VIZ = BUILD.parent
EDGES_CSV = BUILD / "handbook_pass2_edges_2026-08-29.csv"
OUT = BUILD / "atlas_data.json"

WEAK_KEYS = {
    "ZIP", "NAME@ZIP", "COUNTRY", "NAME", "ADDRESS", "NAME@FIPS",
    # category codes, not identities — sharing one is not a join candidate
    "FIPS", "SIC", "NAICS", "DOCKET",
}


def fetch_warehouse():
    import sys

    sys.path.insert(0, str(BUILD.parents[2]))
    from connect.db import connect

    cn = connect()
    cur = cn.cursor()
    cur.execute(
        'select distinct TABLE_NAME, "KEY" from LIBRARY_META."CONNECT".KEYSET_LIVE'
    )
    keyset = cur.fetchall()
    cur.execute(
        """select upper(SOURCE_ID), NAME, DESCRIPTION, PUBLISHER,
                  coalesce(DOMAIN_PRIMARY, CATEGORY), JOIN_KEYS_STD
           from LIBRARY_META.REGISTRY.SOURCE_REGISTRY
           where INCLUDE = 'Y'"""
    )
    registry = cur.fetchall()
    cn.close()
    return keyset, registry


def load_paved():
    with EDGES_CSV.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    paved = []
    for r in rows:
        if r["table_a"] == r["table_b"]:
            continue  # self-loops are intra-table facts, not roads
        paved.append(
            {
                "a": r["table_a"],
                "b": r["table_b"],
                "key": r["key"],
                "col_a": r["col_a"],
                "col_b": r["col_b"],
                "match_rate": float(r["match_rate"]) if r["match_rate"] else None,
                "verdict": r["verdict"],
                "note": r["note"],
                "tier": r["tier"],
                "norm": r.get("norm", ""),
            }
        )
    return paved


def main():
    paved = load_paved()
    keyset, registry = fetch_warehouse()

    # table -> set of keys
    table_keys: dict[str, set[str]] = {}
    for t, k in keyset:
        table_keys.setdefault(t, set()).add(k)

    # every table we know about: keyset tables + handbook tables
    tables = set(table_keys)
    for e in paved:
        tables.add(e["a"])
        tables.add(e["b"])

    # registry lookup: exact upper(SOURCE_ID) match, else substring either way
    reg = {row[0]: row for row in registry}

    def card(name: str):
        row = reg.get(name)
        fallback = False
        if row is None:
            hits = [r for sid, r in reg.items() if sid in name or name in sid]
            row = hits[0] if len(hits) == 1 else None
            fallback = row is not None
        if row is None:
            return {}
        out = {
            "title": row[1],
            "desc": row[2],
            "publisher": row[3],
            "domain": row[4],
        }
        if fallback:
            out["card_parent"] = True  # card describes the parent source, not this table
        return out

    paved_pairs = {frozenset((e["a"], e["b"])) for e in paved}

    # ghost candidates: strong key shared, pair not measured
    ghost = []
    key_tables: dict[str, list[str]] = {}
    for t, ks in table_keys.items():
        for k in ks:
            key_tables.setdefault(k, []).append(t)
    for k, ts in sorted(key_tables.items()):
        if k in WEAK_KEYS:
            continue
        for a, b in combinations(sorted(ts), 2):
            if frozenset((a, b)) not in paved_pairs:
                ghost.append({"a": a, "b": b, "key": k})

    nodes = []
    for t in sorted(tables):
        nodes.append(
            {
                "name": t,
                "keys": sorted(table_keys.get(t, ())),
                **card(t),
            }
        )

    data = {
        "built_on": "2026-09-02",
        "nodes": nodes,
        "paved": paved,
        "ghost": ghost,
        "weak_keys": sorted(WEAK_KEYS),
    }
    OUT.write_text(json.dumps(data, indent=1), encoding="utf-8")
    n_carded = sum(1 for n in nodes if n.get("title"))
    print(f"nodes {len(nodes)}  carded {n_carded}  paved {len(paved)}  ghost {len(ghost)}")


if __name__ == "__main__":
    main()
