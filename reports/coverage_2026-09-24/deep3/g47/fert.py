import pandas as pd
d = pd.read_csv("S02.csv", dtype=str, keep_default_na=False)
d["yr"] = d.YEAR.astype(int); d["tfr"] = d.TOTAL_FERTILITY_RATE.astype(float)
print(d.TOTAL_FERTILITY_RATE.value_counts().head(8))
for v in ["1", "3.724", "3.767"]:
    s = d[d.TOTAL_FERTILITY_RATE == v]
    print(v, s.ENTITY.value_counts().head(5).to_dict(), s.yr.min(), s.yr.max())
print("years per entity", d.groupby("ENTITY").yr.agg(["min","max","count"]).describe())
print("blank code entities:", sorted(d[d.CODE==""].ENTITY.unique()))
print("OWID_ codes:", sorted(d[d.CODE.str.startswith("OWID")].ENTITY.unique()))
