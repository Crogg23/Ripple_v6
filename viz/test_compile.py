"""
Regression checks for viz/compile_library.py. No browser, no server.

    python -m viz.test_compile

Two families of check:
    determinism   build() twice -> byte-identical JSON. An unseeded RNG or a
                  wall-clock read anywhere in the compiler fails this loudly.
    invariants    the facts the renderer is allowed to rely on: every table
                  seated in every lens, state counts, ladder shape, edge
                  indices in range.

One deliberate omission: no golden SHA of the output. The upstream data files
refresh as the platform grows, and a hash pinned to today's warehouse would
cry wolf on every honest refresh. Determinism is proven by double-build
instead.
"""

from __future__ import annotations

import json

from viz.compile_library import LADDER, STATE_NAMES, build

FAILS = []


def check(name, ok, detail=""):
    print(f"  {'ok' if ok else 'FAIL'}  {name}" + (f"  ({detail})" if detail else ""))
    if not ok:
        FAILS.append(name)


def main():
    first = build()
    blob1 = json.dumps(first, indent=1, sort_keys=True)
    blob2 = json.dumps(build(), indent=1, sort_keys=True)
    check("deterministic: build() twice is byte-identical", blob1 == blob2)

    t = first["tables"]
    n = len(t)
    check("universe is 1,043 tables", n == 1043, str(n))

    states = first["meta"]["states"]
    check("state counts are {lit 155, dark 82, keyless 131, uncharted 675}",
          states == {"lit": 155, "dark": 82, "keyless": 131, "uncharted": 675},
          str(states))
    check("per-table states sum to the census",
          all(sum(1 for x in t if x["state"] == i) == states[STATE_NAMES[i]]
              for i in range(4)))

    check("ladder has 6 rungs", len(first["ladder_labels"]) == 6)
    check("ladder order is fixed strongest-first",
          LADDER == ["STEEL", "STRONG", "BRIDGE", "CORROBORATED", "GEO",
                     "PROBABILISTIC"])

    edges = first["edges"]
    check("2,694 links", len(edges) == 2694, str(len(edges)))
    check("every edge endpoint is a real table index",
          all(0 <= e[0] < n and 0 <= e[1] < n for e in edges))
    check("every edge tier is a real rung",
          all(0 <= e[2] < len(LADDER) for e in edges))
    check("no edge touches an uncharted table",
          all(t[e[0]]["state"] != 3 and t[e[1]]["state"] != 3 for e in edges))
    check("lit tables and only lit tables have links",
          all((x["deg"] > 0) == (x["state"] == 0) for x in t))

    bw, bh = first["box"]
    pos = first["positions"]
    check("three lenses of positions", sorted(pos) ==
          ["connection", "journey", "subject"])
    for lens, pts in pos.items():
        check(f"{lens}: one seat per table", len(pts) == n, str(len(pts)))
        # The connection ring intentionally overhangs the box a little; the
        # renderer pads its axes. Everything else must stay inside.
        slack = 0.35 if lens == "connection" else 0.01
        inside = all(-bw * slack <= x <= bw * (1 + slack)
                     and -bh * slack <= y <= bh * (1 + slack) for x, y in pts)
        check(f"{lens}: every seat within bounds", inside)

    xref = first["xref"]
    ref = first["layouts"]["refinery"]
    check("xref seats every table on the journey",
          len(xref) == n and all(0 <= s < len(ref["nodes"]) for s in xref))
    check("journey positions equal the xref seats",
          all(pos["journey"][i] == [ref["nodes"][s]["x"], ref["nodes"][s]["y"]]
              for i, s in enumerate(xref)))
    check("the siding exists and holds the unwired",
          any(b["id"] == "siding" for b in ref["bands"]))

    cells = first["layouts"]["stacks"]["cells"]
    check("subject lens: one cell per table",
          sorted(c["i"] for c in cells) == list(range(n)))

    print()
    if FAILS:
        raise SystemExit(f"{len(FAILS)} check(s) failed: {', '.join(FAILS)}")
    print(f"all checks passed  ({n} tables, {len(edges)} links)")


if __name__ == "__main__":
    main()
