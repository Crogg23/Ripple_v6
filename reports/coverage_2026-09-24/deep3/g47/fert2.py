import pandas as pd
d = pd.read_csv("S02.csv", dtype=str, keep_default_na=False)
d["yr"] = d.YEAR.astype(int); d["tfr"] = d.TOTAL_FERTILITY_RATE.astype(float)
g = d.groupby("ENTITY").yr.agg(["min","max","count"])
print(g[(g["max"]<2023)|(g["count"]!=74)].sort_values("count"))
c = d[(d.CODE.str.len()==3)]  # countries with ISO3
print("countries with ISO3:", c.ENTITY.nunique())
y23 = c[c.yr==2023].set_index("ENTITY").tfr
print("2023 n:", len(y23), "median", y23.median())
print("lowest 2023:\n", y23.sort_values().head(15).round(3).to_string())
print("highest 2023:\n", y23.sort_values().tail(5).round(3).to_string())
# below 1.0 / 1.3 / 2.1 counts over time
for yr in [1950,1975,2000,2010,2015,2020,2023]:
    s = c[c.yr==yr].tfr
    print(yr, "n", len(s), "<2.1:", (s<2.1).sum(), "<1.5:", (s<1.5).sum(), "<1.3:", (s<1.3).sum(), "<1.0:", (s<1.0).sum(), "median", round(s.median(),3))
# at all-time low in 2023 (within this table's own series)
mn = c.groupby("ENTITY").tfr.min()
at_low = [e for e in y23.index if abs(y23[e]-mn[e])<1e-9]
print("countries whose 2023 value is their series low:", len(at_low), "of", len(y23))
# 10-year drop 2013->2023, absolute and relative
y13 = c[c.yr==2013].set_index("ENTITY").tfr
ch = pd.DataFrame({"t13":y13,"t23":y23}).dropna()
ch["drop"] = ch.t13-ch.t23; ch["pct"] = ch["drop"]/ch.t13
print("median 10y drop", round(ch["drop"].median(),3), "median pct", round(ch.pct.median(),3))
print("biggest pct drops 2013-2023:\n", ch.sort_values("pct",ascending=False).head(12).round(3).to_string())
print("rises 2013-2023:", (ch["drop"]<0).sum())
print("USA:", c[(c.CODE=="USA")&(c.yr.isin([1950,1960,1976,1990,2007,2013,2020,2021,2022,2023]))][["yr","tfr"]].to_string(index=False))
