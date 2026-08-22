"""The Ripples wire-confirm pass -- resemblance queue meets the wires.

The lead-lag pass (same day) produced 1,830 stream pairs that co-move beyond
chance -- a QUEUE, per the resemblance doctrine (docs/RIPPLES.md Ripple 2):
resemblance finds suspects, wires confirm connections, and only a pattern
surviving both is worth a human's attention.

This pass runs the confirm step: for each surviving pair, are the two tables
actually CONNECTED in the entity spine -- directly (they share a key) or at
one remove (both wired to the same third table)? Connection tier is carried
through so nobody mistakes a fuzzy-name wire for a hard-ID wire.

One small warehouse read (the ~4,900-edge connection list); everything else
is local. Impartial: every queue pair gets the identical check.
"""
import json
import os
import sys
from collections import defaultdict
from datetime import date

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(BASE, "scripts"))

TIER_RANK = {"STEEL": 6, "STRONG": 5, "BRIDGE": 4, "CORROBORATED": 3,
             "GEO": 2, "PROBABILISTIC": 1}


def node_id(table):
    """'HEALTH.HEALTH__FED_FDA_MAUDE' -> 'FED_FDA_MAUDE' (spine node id)."""
    t = table.split(".")[-1]
    if "__" in t:
        t = t.split("__", 1)[1]
    return t.upper()


def load_edges():
    from _snowflake_conn import connect
    conn = connect()
    cur = conn.cursor()
    cur.execute('select A, B, KEY, TIER, MATCHED, MATCH_RATE '
                'from LIBRARY_META."CONNECT".CONNECT_EDGES')
    rows = cur.fetchall()
    conn.close()
    return rows


def main():
    with open(os.path.join(
            BASE, "reports",
            "ripples_lead_lag_deseasonalized_2026-08-21.json")) as fh:
        queue = json.load(fh)["survivors"]

    edges = load_edges()
    print(f"{len(edges):,} spine edges pulled; {len(queue):,} queue pairs to check")

    direct = {}           # frozenset({a,b}) -> best (tier, key)
    neighbors = defaultdict(set)   # node -> {(other, tier, key)}
    for a, b, key, tier, matched, rate in edges:
        pk = frozenset({a, b})
        if pk not in direct or TIER_RANK.get(tier, 0) > TIER_RANK.get(direct[pk][0], 0):
            direct[pk] = (tier, key)
        neighbors[a].add((b, tier, key))
        neighbors[b].add((a, tier, key))

    # Triage stamps (queue_triage_pass.py): a MACRO pair has a side with no
    # entity in it at all -- no wire can ever exist, so it is excluded from the
    # wiring-debt accounting instead of being counted as fixable forever.
    triage = {}
    for fn in sorted(os.listdir(os.path.join(BASE, "reports"))):
        if fn.startswith("ripples_queue_triage_") and fn.endswith(".json"):
            with open(os.path.join(BASE, "reports", fn)) as fh:
                for t in json.load(fh)["pairs"]:
                    triage[frozenset({t["a"], t["b"]})] = t["tag"]

    spine_nodes = set(neighbors)
    confirmed, one_hop, unwired, off_spine = [], [], [], []
    macro_skipped = 0
    for p in queue:
        na, nb = node_id(p["a_table"]), node_id(p["b_table"])
        tag = triage.get(frozenset({p["a_table"], p["b_table"]}))
        p = dict(p, a_node=na, b_node=nb, triage=tag)
        if tag == "MACRO":
            macro_skipped += 1
            continue
        if na not in spine_nodes or nb not in spine_nodes:
            off_spine.append(p)
            continue
        d = direct.get(frozenset({na, nb}))
        if d:
            p["wire"] = {"kind": "direct", "tier": d[0], "key": d[1]}
            confirmed.append(p)
            continue
        # one remove: a shared third table, keep the weakest tier on the path
        shared = {t for t, _, _ in neighbors[na]} & {t for t, _, _ in neighbors[nb]}
        if shared:
            best = None
            for via in shared:
                ta = max(TIER_RANK.get(t, 0) for o, t, _ in neighbors[na] if o == via)
                tb = max(TIER_RANK.get(t, 0) for o, t, _ in neighbors[nb] if o == via)
                path = min(ta, tb)
                if best is None or path > best[0]:
                    best = (path, via)
            tier_name = next(k for k, v in TIER_RANK.items() if v == best[0])
            p["wire"] = {"kind": "one_hop", "via": best[1], "path_tier": tier_name}
            one_hop.append(p)
        else:
            unwired.append(p)

    def hard(pairs, kinds=("STEEL", "STRONG", "BRIDGE")):
        return [p for p in pairs
                if (p["wire"].get("tier") or p["wire"].get("path_tier")) in kinds]

    judgeable = len(queue) - macro_skipped
    out = {
        "checked": len(queue),
        "macro_excluded": macro_skipped,
        "judgeable": judgeable,
        "direct_wired": len(confirmed),
        "direct_wired_hard_id": len(hard(confirmed)),
        "one_hop_wired": len(one_hop),
        "one_hop_hard_id": len(hard(one_hop)),
        "on_spine_but_unwired": len(unwired),
        "off_spine": len(off_spine),
        "confirmed_direct": confirmed,
        "confirmed_one_hop_hard": hard(one_hop),
    }
    path = os.path.join(BASE, "reports",
                        f"ripples_wire_confirm_{date.today().isoformat()}.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"queue {len(queue)}; {macro_skipped} MACRO pairs excluded "
          f"(no entity exists on one side); {judgeable} judgeable")
    print(f"direct-wired: {len(confirmed)} ({len(hard(confirmed))} on hard IDs)")
    print(f"one-hop-wired: {len(one_hop)} ({len(hard(one_hop))} hard the whole path)")
    print(f"on spine, no wire: {len(unwired)}   off the spine entirely: {len(off_spine)}")
    print(f"Wrote {path}")
    for p in sorted(hard(confirmed), key=lambda x: -x["margin_over_null"])[:15]:
        w = p["wire"]
        print(f"  {p['best_corr']:+.2f} lag{p['best_lag_periods']:+3d}{p['bucket'][0]} "
              f"[{w['tier']}:{w['key']}] {p['a_node']} <-> {p['b_node']}")


if __name__ == "__main__":
    main()
