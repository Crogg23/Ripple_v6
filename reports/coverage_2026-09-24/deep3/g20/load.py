import json, pandas as pd
from pathlib import Path
H = Path(__file__).resolve().parent
def df(n):
    f = sorted(H.glob(f"r{n:02d}_*.json"))[0]
    d = json.loads(f.read_text(encoding="utf-8"))
    return pd.DataFrame(d["rows"], columns=d["cols"])
