"""g55 local analysis. Reruns every number in g55.md from the out_Sxx.csv pulls. No warehouse calls."""
import pandas as pd
from pathlib import Path

H = Path(__file__).resolve().parent
pd.set_option("display.width", 250)
pd.set_option("display.max_rows", 200)


def dts():
    d = pd.read_csv(H / "out_S05.csv", low_memory=False)
    d["RECORD_DATE"] = pd.to_datetime(d.RECORD_DATE)
    print("== DTS traps")
    print("rows", len(d), "withdrawal rows", (d.TRANSACTION_TYPE == "Withdrawals").sum())
    tot = d.ACCOUNT_TYPE.str.contains("Total") | d.TRANSACTION_CATG.fillna("").str.contains("Sub-Total")
    pdc = d.TRANSACTION_CATG.fillna("").str.contains("Public Debt")
    s = d.TRANSACTION_TODAY_AMT.sum()
    print("total/subtotal rows", tot.sum(), "share of sum", round(d[tot].TRANSACTION_TODAY_AMT.sum() / s, 3))
    print("public debt rows", pdc.sum(), "share of sum", round(d[pdc].TRANSACTION_TODAY_AMT.sum() / s, 3))
    print(d.groupby("ACCOUNT_TYPE").RECORD_DATE.agg(["min", "max", "size"]))

    t = d[d.ACCOUNT_TYPE == "Treasury General Account (TGA)"].copy()
    t["md"] = t.RECORD_DATE.dt.strftime("%m%d")
    t["fy"] = t.RECORD_FISCAL_YEAR.astype(int)
    cbp = t[(t.TRANSACTION_TYPE == "Withdrawals") & (t.TRANSACTION_CATG == "DHS - Customs & Border Protection (CBP)")]
    cus = t[(t.TRANSACTION_TYPE == "Deposits") & t.TRANSACTION_CATG.isin(
        ["DHS - Customs and Certain Excise Taxes", "DHS - Customs Duties, Taxes, and Fees"])]
    win = lambda x: x[(x.md >= "1001") | (x.md <= "0807")]
    print("== CBP withdrawals, Oct 1 - Aug 7, $M by FY", win(cbp).groupby("fy").TRANSACTION_TODAY_AMT.sum().to_dict())
    print("== Customs deposits, Oct 1 - Aug 7, $M by FY", win(cus).groupby("fy").TRANSACTION_TODAY_AMT.sum().to_dict())
    base = cbp[(cbp.RECORD_DATE >= "2022-10-01") & (cbp.RECORD_DATE < "2025-10-01")].TRANSACTION_TODAY_AMT
    print("FY23-25 CBP daily: mean", round(base.mean(), 1), "median", base.median(), "max", base.max(),
          "on", cbp.loc[base.idxmax(), "RECORD_DATE"].date())
    since = cbp[cbp.RECORD_DATE >= "2026-05-11"].TRANSACTION_TODAY_AMT
    print("since 2026-05-11: $M", since.sum(), "days", len(since), "excess over FY23-25 mean pace",
          round(since.sum() - base.mean() * len(since)))
    top = cbp.sort_values("TRANSACTION_TODAY_AMT").tail(3)[["RECORD_DATE", "TRANSACTION_TODAY_AMT"]]
    print(top.to_string())
    old = d[(d.TRANSACTION_TYPE == "Withdrawals") & (d.TRANSACTION_CATG_DESC == "Customs and Borders Protection (DHS)")]
    print("old-format CBP line max", old.TRANSACTION_TODAY_AMT.max(), "on",
          old.loc[old.TRANSACTION_TODAY_AMT.idxmax(), "RECORD_DATE"].date())
    m = lambda x: x.groupby(x.RECORD_DATE.dt.to_period("M")).TRANSACTION_TODAY_AMT.sum()
    mm = pd.DataFrame({"customs_in": m(cus), "cbp_out": m(cbp)}).loc["2025-01":]
    mm["net"] = mm.customs_in - mm.cbp_out
    print(mm.to_string())

    # peer: every withdrawal category with a Dec-Jul history FY2023-26 and >= $1B in FY2025
    w = t[(t.TRANSACTION_TYPE == "Withdrawals") & ((t.md >= "1201") | (t.md <= "0731"))]
    p = w.pivot_table(index="TRANSACTION_CATG", columns="fy", values="TRANSACTION_TODAY_AMT", aggfunc="sum")[[2023, 2024, 2025, 2026]]
    p = p[p[[2023, 2024, 2025]].notna().all(axis=1) & p[2026].notna() & (p[2025] >= 1000)]
    p["r26"] = p[2026] / p[2025]
    print("== peer: categories", len(p), "median FY26/FY25 (Dec-Jul)", round(p.r26.median(), 2))
    print(p.sort_values("r26", ascending=False).head(4).round(2).to_string())
    print(p.sort_values("r26").head(4).round(2).to_string())


def mts():
    m = pd.read_csv(H / "out_S10.csv")
    m["RECORD_DATE"] = pd.to_datetime(m.RECORD_DATE)
    m["g"] = m.CURRENT_MONTH_GROSS_RCPT_AMT / 1e9
    m["r"] = m.CURRENT_MONTH_REFUND_AMT / 1e9
    m["n"] = m.CURRENT_MONTH_NET_RCPT_AMT / 1e9
    print("== MTS customs: months", len(m), m.RECORD_DATE.min().date(), "to", m.RECORD_DATE.max().date())
    pre = m[m.RECORD_DATE < "2026-05-01"]
    print("before May 2026: median monthly refund $B", round(pre.r.median(), 2), "max", round(pre.r.max(), 2),
          "on", pre.loc[pre.r.idxmax(), "RECORD_DATE"].date(), "sum", round(pre.r.sum(), 2),
          "max refund/gross", round((pre.r / pre.g).max(), 3))
    last = m[m.RECORD_DATE >= "2026-05-01"][["RECORD_DATE", "g", "r", "n"]].copy()
    last["net_calc"] = last.g - last.r
    print(last.round(2).to_string())
    print("May+June 2026 refunds $B", round(last.r.sum(), 2))
    fy = m[m.RECORD_DATE.between("2025-10-01", "2026-04-30")].r.sum()
    fy0 = m[m.RECORD_DATE.between("2024-10-01", "2025-04-30")].r.sum()
    print("Oct-Apr refunds FY26 vs FY25 $B", round(fy, 2), round(fy0, 2))


def pbgc():
    p = pd.read_csv(H / "out_S01.csv", low_memory=False)
    g = p.groupby(["DATA_YEAR", "TABLE_NAME", "METRIC_NAME"], dropna=False).size()
    print("== PBGC rows", len(p), "rows sharing edition+table+label with other values", g[g > 1].sum(),
          "null METRIC_NAME", p.METRIC_NAME.isna().sum(), "editions", p.DATA_YEAR.nunique())
    x = p[(p.DATA_YEAR == 2023) & (p.TABLE_NAME == "S-1") & (p.METRIC_NAME == "1980")]
    print("2023 edition S-1, label 1980:", x.METRIC_VALUE.tolist())
    y = p[(p.TABLE_NAME == "S-1") & (p.METRIC_NAME == "2008")]
    print("S-1 label 2008 appears in", y.DATA_YEAR.nunique(), "editions,", len(y), "rows")


def aid():
    f = pd.read_csv(H / "out_S02.csv", low_memory=False)
    k = ["COUNTRY", "MANAGING_AGENCY", "FUNDING_AGENCY", "FISCAL_YEAR", "TRANSACTION_TYPE"]
    print("== aid rows", len(f), "dups on 5-col key", f.duplicated(k).sum(), "blank FY", f.FISCAL_YEAR.isna().sum())
    print("filled", f.notna().sum().to_dict())
    print(f.groupby("FISCAL_YEAR").size().loc[2020:].to_dict())
    a = f.groupby(["FISCAL_YEAR", "MANAGING_AGENCY"]).COUNTRY.nunique().unstack(fill_value=0)
    print(a.loc[2021:, [1, 2, 7, 16]])


def api():
    u = pd.read_csv(H / "out_S03.csv", low_memory=False)
    print("== API rows", len(u), "CFDA filled", u.CFDA_NUMBER.notna().sum(), "min amount", u.AWARD_AMOUNT.min(),
          "sum $T", round(u.AWARD_AMOUNT.sum() / 1e12, 2))
    s = pd.read_csv(H / "out_S13.csv")
    s["hit"] = s.R2_ROWS.notna()
    print(pd.crosstab(s.hit, s.END_DATE.isna(), rownames=["in R2"], colnames=["END_DATE blank"]))


def orgs527():
    o = pd.read_csv(H / "out_S04.csv", low_memory=False, dtype=str)
    print("== 527 rows", len(o), "EINs", o.EIN.nunique(), "AMENDED_FLAG", o.AMENDED_FLAG.value_counts().to_dict(),
          "STATUS_FLAG", o.STATUS_FLAG.value_counts().to_dict())
    o["a0"] = (o.MAIL_ADDRESS1.fillna("").str.upper().str.replace(r"[^A-Z0-9 ]", "", regex=True)
               .str.replace(r"\s+", " ", regex=True).str.replace(r" (SUITE|STE|NO)\b.*$", "", regex=True).str.strip()
               + " | " + o.MAIL_CITY.fillna("").str.upper().str.strip())
    a = o.groupby("a0").agg(eins=("EIN", "nunique"),
                            cust=("CUSTODIAN_NAME", lambda s: "; ".join(s.value_counts().index[:2])))
    print(a.sort_values("eins", ascending=False).head(8).to_string())


if __name__ == "__main__":
    dts()
    mts()
    pbgc()
    aid()
    api()
    orgs527()
