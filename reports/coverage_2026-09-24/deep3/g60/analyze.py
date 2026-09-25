"""g60 local analysis: reproduces every number in g60.md from the out_S*.csv extracts. No warehouse calls."""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)


def ember():
    e = pd.read_csv(HERE / "out_S10.csv")
    c = e[e.AREA_TYPE != "Region"]
    a = c[c.YEAR == 2024].set_index("COUNTRY")
    b = c[c.YEAR == 2025].set_index("COUNTRY")
    k = b.index
    print("EMBER 2025 countries:", len(k), "| their share of 2024 generation:",
          round(100 * a.loc[k, "GEN_TWH"].sum() / a.GEN_TWH.sum(), 1))
    dc = b.COAL_TWH - a.loc[k, "COAL_TWH"]
    us = "United States of America"
    print("US coal 2024 -> 2025:", a.loc[us, "COAL_TWH"], "->", b.loc[us, "COAL_TWH"], "| change", round(dc[us], 2),
          "| pct", round(100 * dc[us] / a.loc[us, "COAL_TWH"], 1))
    others = dc.drop(us)
    print("other countries with a coal rise:", int((others > 0).sum()), "| their rises combined:", round(others[others > 0].sum(), 1))
    print("countries with coal data both years:", int(dc.notna().sum()))
    big = a.loc[k, "COAL_TWH"] >= 10
    pct = (100 * dc / a.loc[k, "COAL_TWH"])[big].sort_values(ascending=False)
    print("countries with >=10 TWh coal in 2024:", int(big.sum()), "| median pct change:", round(pct.median(), 1))
    print(pct.round(1).head(5).to_string())
    w = e[e.COUNTRY == "World"].set_index("YEAR")
    u = e[e.COUNTRY == us].set_index("YEAR")
    wx = w.COAL_TWH - u.COAL_TWH
    print("World coal 2024 -> 2025:", w.loc[2024, "COAL_TWH"], "->", w.loc[2025, "COAL_TWH"],
          "| world minus US change:", round(wx[2025] - wx[2024], 1),
          "| US rise as share of rest-of-world fall:", round(100 * dc[us] / -(wx[2025] - wx[2024]), 1))
    print("US gas change", round(b.loc[us, "GAS_TWH"] - a.loc[us, "GAS_TWH"], 2),
          "| US wind+solar change", round(b.loc[us, "WS_TWH"] - a.loc[us, "WS_TWH"], 2),
          "| US demand change", round(b.loc[us, "DEMAND_TWH"] - a.loc[us, "DEMAND_TWH"], 2),
          "| US power CO2 change", round(b.loc[us, "CO2_MT"] - a.loc[us, "CO2_MT"], 2))
    dco2 = b.CO2_MT - a.loc[k, "CO2_MT"]
    print("power CO2 change, other 90 reporting countries:", round(dco2.drop(us).sum(), 1),
          "| World:", round(w.loc[2025, "CO2_MT"] - w.loc[2024, "CO2_MT"], 2))
    yoy = u.COAL_YOY_ABS.dropna().sort_values(ascending=False)
    print("US coal biggest yearly rises since 2000:", yoy.head(4).round(1).to_dict())
    # 2015 -> 2024 fossil share vs region, hydro as the dull explanation
    a15 = c[c.YEAR == 2015].set_index("COUNTRY")
    kk = a15.index.intersection(a.index)
    d = pd.DataFrame({"region": a.loc[kk, "EMBER_REGION"], "dem24": a.loc[kk, "DEMAND_TWH"],
                      "dfos": a.loc[kk, "FOSSIL_PCT"] - a15.loc[kk, "FOSSIL_PCT"],
                      "dhyd": a.loc[kk, "HYDRO_PCT"] - a15.loc[kk, "HYDRO_PCT"],
                      "dnuc": a.loc[kk, "NUCLEAR_PCT"] - a15.loc[kk, "NUCLEAR_PCT"],
                      "dcoal": a.loc[kk, "COAL_PCT"] - a15.loc[kk, "COAL_PCT"]})
    d = d[d.dem24 >= 10]
    up = d[d.dfos > 0]
    print("2015->2024, countries >=10 TWh:", len(d), "| fossil share rose in", len(up),
          "| of those, hydro share fell >=2 pts:", int((up.dhyd <= -2).sum()), "| median fossil change all:", round(d.dfos.median(), 1))
    asia = d[d.region == "Asia"].sort_values("dcoal", ascending=False)
    print("Asia coal-share change, top 4 and median:", asia.dcoal.round(1).head(4).to_dict(), round(asia.dcoal.median(), 1), "n", len(asia))
    print("2024 missing countries vs 2023:", len(set(c[c.YEAR == 2023].COUNTRY) - set(a.index)))


def wind():
    w = pd.read_csv(HERE / "out_S11.csv")
    w["mwt"] = w.NAMEPLATE_CAPACITY_MW / w.NUMBER_OF_TURBINES
    print("\nWIND rows", len(w), "| MW", round(w.NAMEPLATE_CAPACITY_MW.sum(), 1), "| status", w.STATUS.value_counts().to_dict())
    leg = w[(w.OPERATING_YEAR <= 2004) & (w.mwt < 1.0)]
    print("legacy (start <=2004, <1 MW per turbine):", len(leg), "gens,", round(leg.NAMEPLATE_CAPACITY_MW.sum(), 1), "MW,",
          int(leg.NUMBER_OF_TURBINES.sum()), "turbines | with a repower year:", int(leg.G_REPOWER_YEAR.notna().sum()),
          "| with a retirement year:", int(leg.G_RET_YEAR.notna().sum()))
    rp = w[w.G_REPOWER_YEAR.notna()]
    print("planned repowers:", len(rp), "gens,", round(rp.NAMEPLATE_CAPACITY_MW.sum(), 1), "MW, median start year", rp.OPERATING_YEAR.median())
    rt = w[w.G_RET_YEAR.notna()]
    print("planned retirements:", len(rt), "gens,", round(rt.NAMEPLATE_CAPACITY_MW.sum(), 1), "MW")
    odd = w[(w.OPERATING_YEAR <= 2004) & (w.mwt >= 1.5)]
    print("start <=2004 but >=1.5 MW per turbine:", len(odd), "gens,", round(odd.NAMEPLATE_CAPACITY_MW.sum(), 1), "MW")
    big = {"GE", "Vestas", "VESTAS", "Siemens", "Siemens Gamesa", "Gamesa", "Nordex"}
    w["big"] = w.PREDOMINANT_TURBINE_MANUFACTURER.isin(big)
    w["down"] = w.STATUS != "OP"
    w["old"] = w.OPERATING_YEAR <= 2010
    print(pd.crosstab([w.old, w.big], w.down))


def storage():
    s = pd.read_csv(HERE / "out_S12.csv")
    b = s[s.PRIME_MOVER == "BA"]
    tot = b.NAMEPLATE_CAPACITY_MW.sum()
    bl = b[b.STORAGE_ENCLOSURE_TYPE == "BL"]
    two = bl[bl.PLANT_CODE.isin([260, 63834])]
    print("\nSTORAGE battery units", len(b), "MW", round(tot, 1), "| building (BL) units", len(bl), "MW", round(bl.NAMEPLATE_CAPACITY_MW.sum(), 1),
          "share", round(100 * bl.NAMEPLATE_CAPACITY_MW.sum() / tot, 2))
    print("Moss Landing (260) + Gateway (63834):", two.NAMEPLATE_CAPACITY_MW.sum(), "MW =",
          round(100 * two.NAMEPLATE_CAPACITY_MW.sum() / bl.NAMEPLATE_CAPACITY_MW.sum(), 1), "% of BL MW;",
          two.NAMEPLATE_ENERGY_CAPACITY_MWH.sum(), "of", round(bl.NAMEPLATE_ENERGY_CAPACITY_MWH.sum(), 1), "BL MWh")
    pre = b[b.OPERATING_YEAR <= 2021]
    post = b[b.OPERATING_YEAR >= 2022]
    sh = lambda x: round(100 * x[x.STORAGE_ENCLOSURE_TYPE == "BL"].NAMEPLATE_CAPACITY_MW.sum() / x.NAMEPLATE_CAPACITY_MW.sum(), 1)
    print("BL share of MW: start <=2021", sh(pre), "| 2022-2024", sh(post), "| 2024 alone", sh(b[b.OPERATING_YEAR == 2024]))
    print("units >=100 MW:", int((b.NAMEPLATE_CAPACITY_MW >= 100).sum()), "| of them BL:", int((bl.NAMEPLATE_CAPACITY_MW >= 100).sum()),
          "at", bl[bl.NAMEPLATE_CAPACITY_MW >= 100].PLANT_CODE.nunique(), "sites")
    tiny = s[s.PLANT_CODE.isin([64851, 64852, 65058])]
    print("4.6 MWh rows:", tiny[["PLANT_NAME", "NAMEPLATE_CAPACITY_MW", "NAMEPLATE_ENERGY_CAPACITY_MWH", "MAXIMUM_CHARGE_RATE_MW"]].to_string(index=False))
    d = b[b.DIRECT_SUPPORT_OF_ANOTHER_UNIT == "Y"]
    print("direct-support batteries:", len(d), "| target not in operable list:", int(d.T1_TECH.isna().sum()), round(d[d.T1_TECH.isna()].NAMEPLATE_CAPACITY_MW.sum(), 1), "MW")
    dur = lambda x: round(x.NAMEPLATE_ENERGY_CAPACITY_MWH.sum() / x.NAMEPLATE_CAPACITY_MW.sum(), 2)
    print("MWh per MW: CA", dur(b[b.STATE == "CA"]), "| TX", dur(b[b.STATE == "TX"]), "| all", dur(b))


if __name__ == "__main__":
    ember()
    wind()
    storage()
