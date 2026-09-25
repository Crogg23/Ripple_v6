"""g19 local analysis. Reads the r*.json pulls; sends nothing to the warehouse.
Run from this folder: python analyze.py"""
import re
import numpy as np
import pandas as pd
from load import L

pd.set_option("display.width", 250)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_colwidth", 60)

# ---------- IRS 8871 ----------
o = L(2)
o["ins"] = pd.to_datetime(o.INSERT_DATETIME, errors="coerce")
o["iy"] = o.ins.dt.year
POL = (r"candidat|elect|campaign|politic|office|ballot|\bpac\b|committee|legislat|vote|voter|advoca|party|"
       r"public policy|issue|referend|initiative|govern|mayor|council|sheriff|judge|senat|congress|school board|"
       r"measure|lobby|democra|republic|conservat|progressiv|liberal|527")
o["pol"] = (o.PURPOSE.str.contains(POL, case=False, na=False)
            | o.ORGANIZATION_NAME.str.contains(POL + r"|friends of|for (?:congress|senate|mayor|sheriff|judge)|elect\b|citizens for",
                                               case=False, na=False))
o["noem"] = o.EMAIL_ADDRESS.str.lower().eq("no@email")
o["grow"] = (o.PURPOSE.str.contains(r"b\w*ness\w* +grow|small business", case=False, na=False)
             & o.PURPOSE.str.len().lt(60))
i = o[o.INITIAL_REPORT_IND == "1"]

print("== 8871: non-political share of initial notices, three windows")
for nm, lo, hi in [("2019-01..2022-11", "2019-01-01", "2022-12-01"),
                   ("2022-12..2025-12", "2022-12-01", "2026-01-01"),
                   ("2026-01..2026-07", "2026-01-01", "2027-01-01")]:
    x = i[(i.ins >= lo) & (i.ins < hi)]
    print(f"  {nm}: {len(x)} initial, {(~x.pol).sum()} non-political = {(~x.pol).mean()*100:.1f}%")
print("  initial notices by year:", i.groupby("iy").size().loc[2021:].to_dict())
print("  political-only by year:", i[i.pol].groupby("iy").size().loc[2021:].to_dict())

g = o[o.grow & o.noem & (o.iy == 2025)].copy()
g["e"] = g.EIN.astype(int)
print(f"\n== 2025 'help small business grow' + no@email: {len(g)} filings, {g.EIN.nunique()} EINs, "
      f"{g.MAILING_STATE.nunique()} states, LLC share {g.ORGANIZATION_NAME.str.upper().str.contains(r'LLC').mean():.2f}")
print("  amended:", (g.AMENDED_REPORT_IND == "1").sum(), " final:", (g.FINAL_REPORT_IND == "1").sum())


def pair_rate(df, gap=500):
    e = np.sort(df.e.values)
    n, c = len(e), 0
    for a in range(n):
        b = a + 1
        while b < n and e[b] - e[a] <= gap:
            c += 1
            b += 1
    return c, n * (n - 1) / 2


rest = i[(i.iy == 2025) & ~(i.grow & i.noem)].copy()
rest["e"] = rest.EIN.astype(int)
for pre in ["39", "33"]:
    c1, p1 = pair_rate(g[g.EIN.str[:2] == pre])
    c2, p2 = pair_rate(rest[rest.EIN.str[:2] == pre])
    print(f"  EIN prefix {pre}: cluster pairs <=500 apart {c1}/{int(p1)} = {c1/p1:.4%}; "
          f"other 2025 filers {c2}/{int(p2)} = {c2/p2:.4%}; ratio {c1/p1/(c2/p2):.0f}x")
b = g[g.INSERT_DATETIME.str.startswith("2025-07-08")]
print(f"  2025-07-08 batch: {len(b)} filings, {b.MAILING_STATE.nunique()} states, EINs {b.e.min()}-{b.e.max()}, "
      f"filed {b.INSERT_DATETIME.min()[11:16]}-{b.INSERT_DATETIME.max()[11:16]}")

r = L(7)
print(f"  cluster EINs with any 8872 money report: {g.EIN.isin(set(r.EIN)).sum()} of {len(g)}")
pol25 = i[(i.iy == 2025) & i.pol & (i.EXEMPT_8872_IND == "0")]
print(f"  2025 political non-exempt filers with an 8872: {pol25.EIN.isin(set(r.EIN)).sum()} of {len(pol25)}")

# ---------- FEC candidates ----------
c = L(5)
s = L(6)
num = ["TTL_RECEIPTS", "TTL_DISB", "CASH_ON_HAND_CLOSE", "DEBTS_OWED_BY", "TTL_INDIV_CONTRIB"]
for n in num:
    s[n] = pd.to_numeric(s[n], errors="coerce")
c["ey"] = pd.to_numeric(c.CAND_ELECTION_YR, errors="coerce")
c["lag"] = c.CYCLE.astype(int) - c.ey

s2 = s.merge(c[["CAND_ID", "CYCLE", "PRINCIPAL_CMTE_ID"]], on=["CAND_ID", "CYCLE"], how="left")
d = (s2[s2.PRINCIPAL_CMTE_ID.notna()].groupby(["CYCLE", "PRINCIPAL_CMTE_ID"])
     .agg(n=("CAND_ID", "size"), rec=("TTL_RECEIPTS", "first"), nrec=("TTL_RECEIPTS", "nunique")).reset_index())
d = d[(d.n > 1) & (d.nrec == 1)]
print(f"\n== FEC summary: {len(d)} committees counted under 2+ candidate IDs with identical money; "
      f"double-counted receipts 2024 ${(d[d.CYCLE=='2024'].rec*(d[d.CYCLE=='2024'].n-1)).sum()/1e9:.2f}B "
      f"of ${s[s.CYCLE=='2024'].TTL_RECEIPTS.sum()/1e9:.2f}B")

c26 = c[c.CYCLE == "2026"]
minlag = c26.groupby("PRINCIPAL_CMTE_ID").lag.min()
cur = set(zip(c26[c26.lag < 10].CAND_NAME.str.split(",").str[0], c26[c26.lag < 10].OFFICE_STATE))
m = c26.merge(s[s.CYCLE == "2026"][["CAND_ID"] + num], on="CAND_ID")
m["minlag"] = m.PRINCIPAL_CMTE_ID.map(minlag)
z = m[m.minlag >= 10].drop_duplicates("PRINCIPAL_CMTE_ID")
z = z[[(n.split(",")[0], st) not in cur for n, st in zip(z.CAND_NAME, z.OFFICE_STATE)]]
s24 = (s[s.CYCLE == "2024"].merge(c[c.CYCLE == "2024"][["CAND_ID", "PRINCIPAL_CMTE_ID"]], on="CAND_ID")
       .drop_duplicates("PRINCIPAL_CMTE_ID").set_index("PRINCIPAL_CMTE_ID"))
zz = z.set_index("PRINCIPAL_CMTE_ID")
print(f"== old-race committees (last race 2016 or earlier, no current tie): {len(z)}")
print(f"  2026 cycle: cash ${zz.CASH_ON_HAND_CLOSE.sum():,.0f}, spent ${zz.TTL_DISB.sum():,.0f}, "
      f"took in ${zz.TTL_RECEIPTS.sum():,.0f} (individual donors ${zz.TTL_INDIV_CONTRIB.sum():,.0f})")
print(f"  2024 cycle, same committees: spent ${s24.reindex(zz.index).TTL_DISB.sum():,.0f}")
print(f"  median cash ${zz.CASH_ON_HAND_CLOSE.median():,.0f}; top 10 hold "
      f"{zz.CASH_ON_HAND_CLOSE.nlargest(10).sum()/zz.CASH_ON_HAND_CLOSE.sum():.0%} of cash; "
      f"{(zz.TTL_DISB > 0).sum()} spent anything in 2026 cycle")
gifts = L(16)
gifts["AMT"] = gifts.AMT.astype(float)
print(f"  gifts to candidates (non-memo), both cycles: ${gifts.AMT.sum():,.0f} from {gifts.CMTE_ID.nunique()} committees")
