"""Bridge layer — connect tables that DON'T share a key, through a hop.

Direct discovery (discover.py) links two tables only when they carry the SAME
key. But a huge amount of real connection is *transitive*: table X carries NPI,
table Y carries EIN, and NPPES carries BOTH in the same rows — so every provider
in X that maps (via NPPES) to an EIN present in Y is a real connection X<->Y the
direct pass can never see.

A "bridge" is any landed table that carries two different SPINE keys (hard entity
IDs or structured codes) in the same rows. Each yields a crosswalk relation
keyA<->keyB: the set of observed (valA, valB) equivalences. We materialize the
union of every table's crosswalks once, then ONE set-join over the existing
KEYSET_SCRATCH finds every transitive table pair + how many distinct value-pairs
bridge them.

Honesty rails (so a hop never poses as a direct fact):
  * SPINE only — never bridge through NAME/ADDRESS/COUNTRY (too fuzzy / too coarse).
  * Valuable pairs only — at least one hard entity key, or the FIPS<->ZIP geo
    crosswalk. (NAICS<->SIC etc. would connect half the warehouse spuriously.)
  * Fan-out guard — drop crosswalk source values that map to > FANOUT_MAX targets
    (a junk/placeholder ID, or a giant umbrella EIN, is noise not signal).
  * Degenerate guard — drop all-same-char values ('000000000', '9999').
  * Endpoint != bridge source — NPPES<->X is already a DIRECT edge; exclude it
    (also keeps the big join bounded to the small non-bridge tables).
  * Dedup vs direct — a bridged edge is only kept when the pair has NO direct
    edge. The whole point is connections you could NOT see before.
  * Hop penalty — a 2-hop edge is capped below a direct one, tagged via=<bridge>
    and hop=keyA->keyB so it's transparent and filterable in the explorer.
"""

from __future__ import annotations

import json

from . import db
from .discover import (
    CONNECT_DB,
    CONNECT_SCHEMA,
    KEYSET_FQN,
    MIN_POP_PCT,
    _best_value_col,
    _edge,
)
from .keys import normalize_sql, quote_ident

CROSSWALK_FQN = f'"{CONNECT_DB}"."{CONNECT_SCHEMA}"."CROSSWALK_SCRATCH"'

# spine keys we allow as crosswalk sides — hard IDs + structured codes, never
# NAME/ADDRESS/COUNTRY (those are corroboration material, not a join spine).
HARD = {"NPI", "EIN", "CIK", "DUNS", "CCN", "IMO", "MMSI", "UEI", "LEI"}
CODE = {"NAICS", "SIC", "NCES", "DOCKET", "PATENT", "FIPS", "ZIP"}
SPINE = HARD | CODE

HOP_PENALTY = 0.55   # a bridged (2-hop) edge can never score as high as a direct one
FANOUT_MAX = 40      # drop crosswalk source values mapping to > this many targets
MIN_MATCH = 3        # bridged floor: at least this many distinct bridged value-pairs


def _valuable(a: str, b: str) -> bool:
    """A crosswalk relation worth materializing: BOTH ends must be hard entity IDs.

    A bridge is only an ENTITY connection when both sides identify a specific
    thing (NPI<->EIN, NPI<->CCN). Bridging an entity to a COARSE key (NPI->ZIP,
    EIN->NAICS) just says "same place / same industry" — geographic/industry
    co-location shared by thousands of unrelated entities, NOT a connection. That
    is the exact fluke class the engine exists to kill; allowing a coarse
    destination smuggled it back in. (Geo crosswalks like FIPS<->ZIP belong in the
    spatial layer, not here.)"""
    return a in HARD and b in HARD


def _guard(expr: str) -> str:
    """SQL: TRUE unless the normalized value is empty, length<2, or a single
    repeated char (placeholder IDs like 000000000 / 9999 manufacture fake links)."""
    return f"LENGTH({expr}) >= 2 AND LENGTH(REPLACE({expr}, LEFT({expr}, 1), '')) > 0"


def _build_crosswalk(conn, fp: dict) -> tuple[set, int]:
    """Materialize every dual-spine-key table's (keyA, keyB, valA, valB) pairs into
    ONE scratch table. Returns the set of relations and the number of INSERTs."""
    db.rows(conn, f'CREATE SCHEMA IF NOT EXISTS "{CONNECT_DB}"."{CONNECT_SCHEMA}"')
    db.rows(conn, f"CREATE OR REPLACE TRANSIENT TABLE {CROSSWALK_FQN} "
                  f"(key_a STRING, key_b STRING, val_a STRING, val_b STRING, src STRING)")
    relations: set = set()
    inserts = 0
    for tbl, info in fp.items():
        bykey = {}
        for k in info["keys"]:
            if k["mode"] == "value" and k["key"] in SPINE and k["populated_pct"] >= MIN_POP_PCT:
                best = _best_value_col(info["keys"], k["key"])
                if best:
                    bykey[k["key"]] = best["column"]
        ks = sorted(bykey)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                a, b = ks[i], ks[j]
                if not _valuable(a, b):
                    continue
                na = normalize_sql(a, quote_ident(bykey[a]))
                nb = normalize_sql(b, quote_ident(bykey[b]))
                db.rows(conn, f"""INSERT INTO {CROSSWALK_FQN}
                    SELECT DISTINCT '{a}', '{b}', {na}, {nb}, '{tbl}'
                    FROM {db.fqn(tbl)}
                    WHERE {na} IS NOT NULL AND {nb} IS NOT NULL
                      AND {_guard(na)} AND {_guard(nb)}""")
                relations.add((a, b))
                inserts += 1
    return relations, inserts


def _bridged_conf(matched: int, a_d: int, b_d: int) -> tuple[float, bool]:
    if matched < MIN_MATCH:
        return 0.0, False
    cover = matched / (min(a_d, b_d) or matched or 1)
    return round(HOP_PENALTY * (0.4 + 0.6 * min(cover, 1.0)), 3), True


def discover_bridged(conn, fp: dict, direct_pairs: set, fanout_max: int = FANOUT_MAX) -> tuple[list, dict]:
    """Find every transitive table pair bridged by a crosswalk. Assumes
    KEYSET_SCRATCH already exists (built by discover._build_keysets)."""
    relations, inserts = _build_crosswalk(conn, fp)
    stats = {"relations": len(relations), "crosswalk_inserts": inserts,
             "crosswalk_pairs": 0, "bridged": 0, "gated": 0, "deduped_direct": 0}
    if not relations:
        return [], stats
    stats["crosswalk_pairs"] = int(db.scalar(conn, f"SELECT COUNT(*) FROM {CROSSWALK_FQN}") or 0)

    counts = {(r["TABLE_NAME"], r["KEY"]): int(r["ND"])
              for r in db.dicts(conn, f"SELECT table_name, key, COUNT(*) nd FROM {KEYSET_FQN} GROUP BY 1, 2")}

    rows = db.dicts(conn, f"""
        WITH xw AS (
            SELECT key_a, key_b, val_a, val_b, src
            FROM {CROSSWALK_FQN}
            QUALIFY COUNT(DISTINCT val_b) OVER (PARTITION BY key_a, key_b, val_a, src) <= {fanout_max}
                AND COUNT(DISTINCT val_a) OVER (PARTITION BY key_a, key_b, val_b, src) <= {fanout_max}
        )
        SELECT LEAST(a.table_name, b.table_name)    AS t1,
               GREATEST(a.table_name, b.table_name) AS t2,
               xw.key_a AS ka, xw.key_b AS kb,
               COUNT(DISTINCT xw.val_a || '>' || xw.val_b)                       AS matched,
               ARRAY_SLICE(ARRAY_AGG(DISTINCT xw.val_a || ' -> ' || xw.val_b), 0, 4) AS samp,
               ANY_VALUE(xw.src) AS via
        FROM xw
        JOIN {KEYSET_FQN} a ON a.key = xw.key_a AND a.val = xw.val_a AND a.table_name <> xw.src
        JOIN {KEYSET_FQN} b ON b.key = xw.key_b AND b.val = xw.val_b AND b.table_name <> xw.src
        WHERE a.table_name <> b.table_name
        GROUP BY 1, 2, 3, 4
        HAVING COUNT(DISTINCT xw.val_a || '>' || xw.val_b) >= {MIN_MATCH}
    """)

    edges: list = []
    for r in rows:
        ta, tb = r["T1"], r["T2"]
        if frozenset((ta, tb)) in direct_pairs:    # already directly connected -> not new
            stats["deduped_direct"] += 1
            continue
        ka, kb, matched = r["KA"], r["KB"], int(r["MATCHED"])
        a_d = max(counts.get((ta, ka), 0), counts.get((ta, kb), 0))
        b_d = max(counts.get((tb, kb), 0), counts.get((tb, ka), 0))
        conf, keep = _bridged_conf(matched, a_d, b_d)
        if not keep:
            stats["gated"] += 1
            continue
        samp = r["SAMP"]
        samp = json.loads(samp) if isinstance(samp, str) else (samp or [])
        ov = {"mode": "bridge", "a_distinct": a_d, "b_distinct": b_d, "matched": matched,
              "match_rate": round(matched / (min(a_d, b_d) or 1) * 100, 1), "sample": samp[:4]}
        e = _edge(ta, tb, f"{ka}~{kb}", "BRIDGE", "", "", ov, conf)
        e["via"] = r["VIA"]
        e["hop"] = f"{ka}->{kb}"
        edges.append(e)
    stats["bridged"] = len(edges)
    print(f"  [bridge] {len(edges)} transitive edges via {len(relations)} crosswalk relations "
          f"({stats['crosswalk_pairs']:,} pairs); {stats['gated']} gated, {stats['deduped_direct']} already-direct")
    return edges, stats
