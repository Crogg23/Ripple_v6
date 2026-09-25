"""Rewrite every coverage live row in the ledger with the skeptic's corrected headline.

Round 1 and round 2 first wrote the deep-pass headline, which the skeptic had narrowed.
Reads the table-tagged checks saved from each workflow's return value.
"""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import ledger as L

fixed = {}
for f in ("checks_round1.json", "checks_round2.json"):
    for c in json.loads((HERE / f).read_text(encoding="utf-8")):
        fixed[c["table"]] = c
n = 0
with L.locked():
    rows = L.read_tsv("singles")
    for r in rows:
        c = fixed.get(r["table"])
        if c and r["status"] == "live" and r["by"] in ("coverage-b", "coverage-r2"):
            rnd = "R1" if r["by"] == "coverage-b" else "R2"
            r["found"] = (f"coverage {rnd} live, skeptic {c['verdict'].upper()}: {c['corrected_headline']}"
                          " // detail in reports/coverage_2026-09-24/menu.md").replace("\t", " ").replace("\n", " ")
            n += 1
    L.write_tsv("singles", rows, L.COLS["singles"])
print(n, "live rows rewritten from", len(fixed), "skeptic checks")
