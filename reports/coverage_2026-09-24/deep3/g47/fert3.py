import pandas as pd
d = pd.read_csv("S02.csv", dtype=str, keep_default_na=False)
d["yr"] = d.YEAR.astype(int); d["tfr"] = d.TOTAL_FERTILITY_RATE.astype(float)
print("blank CODE rows:", (d.CODE=="").sum(), " rows with code SWE:", (d.CODE=="SWE").sum(), " ESP:", (d.CODE=="ESP").sum())
nv = d.groupby("ENTITY").tfr.nunique().sort_values()
print("fewest distinct values per entity:\n", nv.head(8).to_string())
# year-over-year jumps: biggest single-year moves among countries since 1950 (break check)
c = d[(d.CODE.str.len()==3)&(d.yr>=1950)].sort_values(["ENTITY","yr"]).copy()
c["dy"] = c.groupby("ENTITY").tfr.diff()
print("biggest one-year moves since 1950:\n", c.reindex(c.dy.abs().sort_values(ascending=False).index).head(10)[["ENTITY","yr","tfr","dy"]].round(3).to_string(index=False))
# covid bounce: 2020->2021 rises, 2021->2023 falls
p = c.pivot(index="ENTITY", columns="yr", values="tfr")
print("2020->2021 up:", (p[2021]>p[2020]).sum(), " 2021->2023 down:", (p[2023]<p[2021]).sum(), "of", p[2023].notna().sum())
# high-income aggregate vs US
a = d[d.ENTITY.isin(["High-income countries","World","United States","Europe"])&d.yr.isin([2013,2023])]
print(a.pivot(index="ENTITY", columns="yr", values="tfr").round(3))
