"""Queue triage — stamp every resemblance-queue pair with what wiring can
ever do for it.

The scout audited every dark table's candidate keys. This pass folds that in:

  MACRO        — at least one side is a national aggregate with no entity in
                 it (no company/person/facility ids at all). No wire can ever
                 exist; the co-movement is a macro/climate question. These
                 stop counting as wiring debt.
  GEO_ONLY     — both sides have at best state/county/zip granularity; the
                 strongest possible wire is shared geography (GEO tier).
  WIREABLE     — both sides carry (or sit on the spine with) real entity ids;
                 an edge is buildable.

Local only — reads the deseasonalized queue, the scout JSON, and one
read-only pull of the edge list. Writes reports/ripples_queue_triage_<date>.*
"""
import json
import os
import sys
from collections import Counter
from datetime import date

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
sys.path.insert(0, os.path.join(BASE, "scripts"))

GEO_KINDS = {"STATE", "FIPS", "ZIP"}


def node_id(table):
    t = table.split(".")[-1]
    if "__" in t:
        t = t.split("__", 1)[1]
    return t.upper()


def main():
    with open(os.path.join(
            BASE, "reports",
            "ripples_lead_lag_deseasonalized_2026-08-21.json")) as fh:
        queue = json.load(fh)["survivors"]
    with open(os.path.join(BASE, "reports",
                           "wiring_scout_2026-08-21.json")) as fh:
        scout = json.load(fh)["scouted"]

    from _snowflake_conn import connect
    conn = connect()
    cur = conn.cursor()
    cur.execute('select A, B from LIBRARY_META."CONNECT".CONNECT_EDGES')
    spine = set()
    for a, b in cur.fetchall():
        spine.add(a)
        spine.add(b)
    conn.close()

    # side class per dark table, from the scout's verified keys
    side = {}
    for r in scout:
        node = node_id(r["table"])
        kinds = {k["kind"] for k in r.get("keys", [])
                 if k.get("verdict") == "REAL"}
        if kinds - GEO_KINDS:
            side[node] = "entity"
        elif kinds & GEO_KINDS:
            side[node] = "geo"
        else:
            side[node] = "none"

    def cls(table):
        n = node_id(table)
        if n in spine:
            return "entity"          # on the spine = has proven ids
        return side.get(n, "none")   # unscouted dark stragglers: assume none

    tags = Counter()
    tagged = []
    for p in queue:
        ca, cb = cls(p["a_table"]), cls(p["b_table"])
        if "none" in (ca, cb):
            tag = "MACRO"
        elif "geo" in (ca, cb):
            tag = "GEO_ONLY"
        else:
            tag = "WIREABLE"
        tags[tag] += 1
        tagged.append({"a": p["a_table"], "b": p["b_table"],
                       "best_corr": p["best_corr"],
                       "lag": p["best_lag_periods"], "tag": tag})

    out = {"as_of": str(date.today()), "n_pairs": len(tagged),
           "tag_counts": dict(tags), "pairs": tagged}
    path = os.path.join(BASE, "reports",
                        f"ripples_queue_triage_{date.today()}.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1)
    total = len(tagged)
    print(f"{total} pairs triaged:")
    for t, c in tags.most_common():
        print(f"  {t:9s} {c:5d}  ({c/total:.0%})")
    print("wrote", path)


if __name__ == "__main__":
    main()
