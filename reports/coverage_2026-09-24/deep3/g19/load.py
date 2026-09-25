import json, pandas as pd, glob
def L(n):
    f = glob.glob(f"r{n:02d}_*.json")[0]
    d = json.load(open(f, encoding="utf-8"))
    return pd.DataFrame(d["rows"], columns=d["cols"])
