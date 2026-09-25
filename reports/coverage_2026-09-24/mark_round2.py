"""Write round 2's 84 deep verdicts into the ledger singles layer. Run fix_live.py after it."""
import json, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import ledger as L

d = json.loads((HERE / "round2.json").read_text(encoding="utf-8"))
res = {r["table"]: r for x in d["deep"] for r in x["results"]}
with L.locked():
    rows = L.read_tsv("singles")
    for r in rows:
        if r["table"] in res and r["by"] == "battery-a":
            x = res[r["table"]]
            r["status"] = x["verdict"]
            r["found"] = f"coverage R2 {x['verdict']}: {x['headline']} // {r['found']}".replace("\t", " ").replace("\n", " ")
            r["by"], r["date"] = "coverage-r2", L.today()
    L.write_tsv("singles", rows, L.COLS["singles"])
