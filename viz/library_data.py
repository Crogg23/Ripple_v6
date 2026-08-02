"""
Loads outputs/library.json once and derives the small lookup structures the
figures and the dossier both need. Import from here; never re-read the file.

    python -m viz.compile_library     # builds the file this module reads
"""

from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "outputs" / "library.json"

if not DATA.exists():
    raise SystemExit(
        f"{DATA} is missing.\nBuild it first:  python -m viz.compile_library")

A = json.loads(DATA.read_text(encoding="utf-8"))

TABLES = A["tables"]
EDGES = A["edges"]
LADDER = A["ladder_labels"]          # [[short name, what it means], ...]
STAGES = {s["id"]: s for s in A["stages"]}
LAY = A["layouts"]
POS = A["positions"]                 # lens -> [[x, y], ...] parallel to TABLES
XREF = A["xref"]                     # table i -> its seat in refinery.nodes
META = A["meta"]
BOX_W, BOX_H = A["box"]
N = len(TABLES)

REF = LAY["refinery"]
CELL = {c["i"]: c for c in LAY["stacks"]["cells"]}
MAX_LINKS = max(1, max(t["deg"] for t in TABLES))

# An ID only tells you something if it's rare. The cutoff is compiled, not
# guessed here.
_CUTOFF = META["common_id_cutoff"]
_ID_USAGE: dict[str, int] = {}
for _t in TABLES:
    if _t["state"] == 3:
        continue                     # the parked crawl doesn't vote
    for _k in _t["keys"]:
        _ID_USAGE[_k] = _ID_USAGE.get(_k, 0) + 1


def is_rare(key: str) -> bool:
    return _ID_USAGE.get(key, 0) <= _CUTOFF


# Which link rows touch each dataset, so a click answers instantly.
NEIGHBOURS: list[list[int]] = [[] for _ in range(N)]
for _i, _e in enumerate(EDGES):
    NEIGHBOURS[_e[0]].append(_i)
    NEIGHBOURS[_e[1]].append(_i)

# What runs after what on the pipeline.
KIDS: list[list[int]] = [[] for _ in REF["nodes"]]
PARENTS: list[list[int]] = [[] for _ in REF["nodes"]]
for _a, _b in REF["links"]:
    KIDS[_a].append(_b)
    PARENTS[_b].append(_a)
