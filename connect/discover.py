"""Discover the REAL connections across the whole landed Library.

Reads the fingerprints, forms candidate pairs (two tables that carry the same
live key), runs the overlap engine on each, and keeps the ones that actually
return matched rows. The result is an honest, weighted edge-list: the graph the
explorer draws.

Tiers are computed strongest-first (STEEL/STRONG/GEO/PROBABILISTIC). Name/address
("PROBABILISTIC") joins over very large tables are skipped by default and LOGGED
— never silently dropped — because fuzzy name-matching at multi-million-row scale
is slow and low-trust. Raise --name-max-rows to include them.

Output: outputs/connect_graph.json  { nodes:[...], edges:[...], meta:{...} }
"""

from __future__ import annotations

import json
from pathlib import Path

from . import db
from .fingerprint import OUT as FP_PATH
from .keys import TIER_RANK, normalize_sql, quote_ident
from .overlap import _is_lon, spatial_overlap

GRAPH_OUT = Path(__file__).resolve().parents[1] / "outputs" / "connect_graph.json"

# Set-based discovery materializes every table's distinct normalized keys here,
# then ONE self-join finds all co-occurring pairs + overlap counts -- instead of
# a live full-scan query per candidate pair (the O(n^2) crawl).
CONNECT_DB, CONNECT_SCHEMA = "LIBRARY_META", "CONNECT"   # CONNECT is reserved -> always quote
KEYSET_FQN = f'"{CONNECT_DB}"."{CONNECT_SCHEMA}"."KEYSET_SCRATCH"'

MIN_POP_PCT = 1.0          # a key must be at least this populated to count as live
NAME_MAX_ROWS = 300_000    # skip name/address joins when EITHER table exceeds this
SPATIAL_POINT_MAX = 100_000  # skip point-in-polygon when the point table exceeds this
PROBABILISTIC = {"NAME", "ADDRESS"}

# --- confidence: refuse to draw a fluke. A connection isn't real just because one
# normalized value coincided. Require an absolute floor AND that the match count
# beats what random collision would produce over the key's value space. This is
# what kills the Alabama/Puerto-Rico-style phantom STEEL edge.
MIN_MATCH = 3            # value joins: at least this many matched distinct keys
MIN_MATCH_PROB = 5       # name/address: stricter (common-name noise)
COLLISION_MULT = 5.0     # matched must beat expected-by-chance by this factor
KEY_DOMAIN = {           # ~size of each key's value space, for the collision math
    "NPI": 10**10, "EIN": 10**9, "CIK": 10**7, "DUNS": 10**9, "PATENT": 10**8,
    "IMO": 10**7, "MMSI": 10**9, "UEI": 36**12, "LEI": 36**20,
    "CCN": 10**6, "NAICS": 10**6, "NCES": 10**7, "DOCKET": 10**6, "SIC": 10**4,
    "FIPS": 10**5, "ZIP": 10**5, "COUNTRY": 300,
}


def confidence(key, tier, a_distinct, b_distinct, matched):
    """Return (score 0-1, keep?). A coincidental handful of matches on a short
    numeric key scores ~0 and is dropped; a dense overlap on a hard ID scores ~1."""
    if matched <= 0:
        return 0.0, False
    floor = MIN_MATCH_PROB if tier == "PROBABILISTIC" else MIN_MATCH
    if matched < floor:
        return 0.0, False
    cover = matched / (min(a_distinct, b_distinct) or 1)    # coverage of the smaller set
    dom = KEY_DOMAIN.get(key)
    if dom:
        expected = (a_distinct * b_distinct) / dom          # ~random collisions over the value space
        if matched < COLLISION_MULT * expected:             # indistinguishable from chance -> drop
            return round(matched / (matched + expected + 1e-9), 3), False
        chance_free = matched / (matched + expected)        # fraction of matches not explained by chance
    elif key in PROBABILISTIC:
        chance_free = 0.5                                   # name/address: unscored -> medium-low
    else:
        chance_free = 0.9                                   # spatial: geometry already verifies it
    score = chance_free * (0.4 + 0.6 * min(cover, 1.0))     # reward covering the smaller set (subset joins)
    if tier == "PROBABILISTIC":
        score *= 0.5
    return round(min(score, 1.0), 3), True

# table -> investigation domain (drives node color in the explorer). Prefix fallback.
DOMAIN_KEYWORDS = [
    ("health", ("CMS", "CLINICAL", "FDA", "NPPES", "HCRIS", "OIG_LEIE", "HHS")),
    ("justice", ("DOJ", "FJC", "SCDB", "OYEZ", "HUDOC", "NAAG", "CRT")),
    ("economics", ("SEC", "TREASURY", "FDIC", "EDGAR", "ISTAT", "EMBER")),
    ("foreign_influence", ("FARA",)),
    ("governance", ("REVOLVINGDOOR", "USASPENDING", "FEDERAL_REGISTER")),
    ("maritime", ("NOAA", "AIS")),
    ("hazards", ("USGS", "EARTHQUAKE")),
    ("housing", ("MAPPING_INEQUALITY",)),
    ("corporate_registry", ("ZEFIX", "BORME", "GEMI", "CRO", "SERCOP")),
    ("history", ("SLAVE", "WPA", "NARA", "WAYBACK", "EPSTEIN", "BIORXIV", "WIKIPEDIA")),
]


def domain_of(table: str) -> str:
    t = table.upper()
    for dom, kws in DOMAIN_KEYWORDS:
        if any(k in t for k in kws):
            return dom
    return "other"


def _best_value_col(keys: list[dict], key: str) -> dict | None:
    cands = [k for k in keys if k["key"] == key and k["mode"] == "value"
             and k["populated_pct"] >= MIN_POP_PCT]
    return max(cands, key=lambda k: k["distinct"]) if cands else None


def _latlon_cols(keys: list[dict]) -> tuple[str, str] | None:
    ll = [k["column"] for k in keys if k["key"] == "LATLON" and k["populated_pct"] >= MIN_POP_PCT]
    lat = next((c for c in ll if not _is_lon(c)), None)
    lon = next((c for c in ll if _is_lon(c)), None)
    return (lat, lon) if lat and lon else None


def _geom_col(keys: list[dict]) -> str | None:
    cands = [k for k in keys if k["key"] == "GEOM" and k["nonnull"] > 0]
    return max(cands, key=lambda k: k["nonnull"])["column"] if cands else None


def run(name_max_rows: int = NAME_MAX_ROWS, write: bool = True) -> dict:
    fp = json.loads(FP_PATH.read_text())
    conn = db.connect()
    tested = skipped = gated = 0
    edges: list[dict] = []

    try:
        # ---- value-key connections (set-based: keyset table + one self-join) --
        v_edges, v_gated, v_skipped, v_tested = _value_edges_bulk(conn, fp, name_max_rows)
        edges += v_edges
        gated += v_gated
        skipped += v_skipped
        tested += v_tested

        # ---- spatial connections (point-in-polygon) ------------------------
        pt_tables = {t: ll for t, info in fp.items()
                     if (ll := _latlon_cols(info["keys"]))}
        poly_tables = {t: g for t, info in fp.items()
                       if (g := _geom_col(info["keys"]))}
        for pt, (lat, lon) in pt_tables.items():
            if fp[pt]["rows"] > SPATIAL_POINT_MAX:
                skipped += 1
                print(f"  [skip spatial] {pt} has {fp[pt]['rows']:,} points (> {SPATIAL_POINT_MAX:,})")
                continue
            for poly, geom in poly_tables.items():
                if pt == poly:
                    continue
                tested += 1
                try:
                    ov = spatial_overlap(conn, pt, lat, lon, poly, geom)
                except Exception as e:
                    print(f"  [err] spatial {pt} in {poly}: {str(e)[:80]}")
                    continue
                if ov["matched"] > 0:
                    conf, keep = confidence("GEO_IN", "GEO", ov["a_distinct"], ov["b_distinct"], ov["matched"])
                    if keep:
                        edges.append(_edge(pt, poly, "GEO_IN", "GEO", f"{lat}/{lon}", geom, ov, conf))
                        print(f"  [edge {conf:.2f}] SPATIAL {pt} in {poly}: {ov['matched']:,} ({ov['match_rate']}%)")
                    else:
                        gated += 1
    finally:
        conn.close()

    nodes = [{
        "id": t,
        "rows": info["rows"],
        "domain": domain_of(t),
        "keys": sorted({k["key"] for k in info["keys"] if k["populated_pct"] >= MIN_POP_PCT}),
    } for t, info in fp.items()]

    graph = {
        "meta": {"pairs_tested": tested, "pairs_skipped": skipped, "gated_out": gated,
                 "edges": len(edges), "name_max_rows": name_max_rows},
        "nodes": nodes,
        "edges": sorted(edges, key=lambda e: (-e.get("confidence", 0), -e["matched"])),
    }
    print(f"\n{len(edges)} real connections kept ({gated} flukes gated out) "
          f"from {tested} pairs tested ({skipped} skipped).")
    if write:
        GRAPH_OUT.write_text(json.dumps(graph, indent=2))
        print(f"wrote {GRAPH_OUT}")
    return graph


# --- set-based value discovery ---------------------------------------------- #
def _build_keysets(conn, fp, name_max_rows) -> tuple[dict, int]:
    """Materialize every table's DISTINCT normalized keys into ONE scratch table.
    Returns {(table,key): (column, tier)} and the count of skipped name-keysets.
    One INSERT per (table,key) -- linear in tables, not pairs."""
    db.rows(conn, f'CREATE SCHEMA IF NOT EXISTS "{CONNECT_DB}"."{CONNECT_SCHEMA}"')
    db.rows(conn, f"CREATE OR REPLACE TRANSIENT TABLE {KEYSET_FQN} "
                  f"(table_name STRING, key STRING, val STRING)")
    members, skipped = {}, 0
    for tbl, info in fp.items():
        seen = set()
        for k in info["keys"]:
            key = k["key"]
            if k["mode"] != "value" or key in seen:
                continue
            best = _best_value_col(info["keys"], key)
            if not best:
                continue
            seen.add(key)
            if key in PROBABILISTIC and info["rows"] > name_max_rows:
                skipped += 1                      # fuzzy name-matching huge tables: skip + log
                print(f"  [skip name] {tbl} on {key} ({info['rows']:,} rows > {name_max_rows:,})")
                continue
            members[(tbl, key)] = (best["column"], _tier(fp, key))
            norm = normalize_sql(key, quote_ident(best["column"]))
            db.rows(conn, f"INSERT INTO {KEYSET_FQN} "
                          f"SELECT DISTINCT '{tbl}', '{key}', {norm} "
                          f"FROM {db.fqn(tbl)} WHERE {norm} IS NOT NULL")
    return members, skipped


def _value_edges_bulk(conn, fp, name_max_rows) -> tuple[list, int, int, int]:
    members, skipped = _build_keysets(conn, fp, name_max_rows)
    if not members:
        return [], 0, skipped, 0

    counts = {(r["TABLE_NAME"], r["KEY"]): int(r["ND"])
              for r in db.dicts(conn, f"SELECT table_name, key, COUNT(*) nd FROM {KEYSET_FQN} GROUP BY 1, 2")}

    # ONE self-join: all co-occurring (table_a, table_b) pairs per key + overlap + a sample.
    pairs = db.dicts(conn, f"""
        SELECT a.key AS jkey, a.table_name AS ta, b.table_name AS tb,
               COUNT(*) AS matched,
               ARRAY_SLICE(ARRAY_AGG(a.val), 0, 4) AS samp
        FROM {KEYSET_FQN} a
        JOIN {KEYSET_FQN} b ON a.key = b.key AND a.val = b.val AND a.table_name < b.table_name
        GROUP BY 1, 2, 3
        HAVING COUNT(*) >= {MIN_MATCH}
    """)

    edges, gated = [], 0
    for r in pairs:
        key, ta, tb, matched = r["JKEY"], r["TA"], r["TB"], int(r["MATCHED"])
        a_d, b_d = counts.get((ta, key), 0), counts.get((tb, key), 0)
        col_a, tier = members.get((ta, key), ("", "PROBABILISTIC"))
        col_b = members.get((tb, key), ("", ""))[0]
        conf, keep = confidence(key, tier, a_d, b_d, matched)
        if not keep:
            gated += 1
            continue
        samp = r["SAMP"]
        samp = json.loads(samp) if isinstance(samp, str) else (samp or [])
        ov = {"mode": "value", "a_distinct": a_d, "b_distinct": b_d, "matched": matched,
              "match_rate": round(matched / (min(a_d, b_d) or 1) * 100, 1), "sample": samp[:4]}
        edges.append(_edge(ta, tb, key, tier, col_a, col_b, ov, conf))
    print(f"  [value] {len(edges)} kept / {gated} gated from {len(pairs)} co-occurring pairs (set-based)")
    return edges, gated, skipped, len(pairs)


# --- small helpers ---------------------------------------------------------- #
def _tier(fp: dict, key: str) -> str:
    from .keys import KEY_TOKENS
    return KEY_TOKENS.get(key, ("PROBABILISTIC",))[0]


def _edge(a, b, key, tier, a_col, b_col, ov, conf) -> dict:
    return {
        "a": a, "b": b, "key": key, "tier": tier,
        "a_col": a_col, "b_col": b_col,
        "mode": ov["mode"], "matched": ov["matched"],
        "a_distinct": ov["a_distinct"], "b_distinct": ov["b_distinct"],
        "match_rate": ov["match_rate"], "confidence": conf,
        "sample": ov.get("sample", []),
    }


if __name__ == "__main__":
    run()
