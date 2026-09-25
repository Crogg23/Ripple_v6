"""Write battery A and stage B results into the ledger's singles layer, one locked write.

Deep-pass tables get their verdict; fix_live.py then swaps in the skeptic's corrected headline on live rows.
Every other battery table becomes probed: its first check, the lead-number profile, is answered.
Rows not untouched are left alone, so hand work is never overwritten.
"""
import json, sys
from collections import defaultdict
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import ledger as L

B = json.loads((HERE / "stage_b.json").read_text(encoding="utf-8"))
scores, angle = defaultdict(list), {}
for blk in B["triage"]:
    for x in blk["items"]:
        scores[x["table"]].append(x["score"])
        angle.setdefault(x["table"], x["angle"])
deep = {r["table"]: r for d in B["deep"] for r in d["results"]}
facts = {}
import csv
for r in csv.DictReader((HERE / "facts.tsv").open(encoding="utf-8"), delimiter="\t"):
    facts[r["table"]] = r["facts"]
traps = defaultdict(list)
for r in csv.DictReader((HERE / "traps.tsv").open(encoding="utf-8"), delimiter="\t"):
    traps[r["table"]].append(r["detail"])

n = defaultdict(int)
with L.locked():
    rows = L.read_tsv("singles")
    for r in rows:
        t = r["table"]
        if r["status"] != "untouched" or t not in facts:
            continue
        s = scores.get(t)
        tri = f"triage {sum(s) / len(s):.1f}/10: {angle[t]}" if s else "triage: no score"
        trap = f" TRAP: {'; '.join(traps[t])}" if traps[t] else ""
        if t in deep:
            d = deep[t]
            r["status"] = d["verdict"]
            note = f"coverage B {d['verdict']}: {d['headline']}"
            if d["verdict"] == "live":
                note += " // skeptic NARROWED, see reports/coverage_2026-09-24/menu.md"
            r["by"] = "coverage-b"
        else:
            r["status"] = "probed"
            note = f"battery A: {facts[t][:300]} // {tri}"
            r["by"] = "battery-a"
        r["found"] = (note + trap).replace("\t", " ").replace("\n", " ")
        r["date"] = L.today()
        n[r["status"]] += 1
    L.write_tsv("singles", rows, L.COLS["singles"])
print(dict(n))
