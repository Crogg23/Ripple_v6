import json, pandas as pd
def df(n, label):
    r = json.load(open(f"r{n:02d}_{label}.json", encoding="utf-8"))
    return pd.DataFrame(r["rows"], columns=r["cols"])
