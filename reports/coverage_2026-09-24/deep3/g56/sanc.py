"""Local math for the GLEIF x sanctions lead. Inputs: out_S07/S08/S09/S10 csv. Output: sanc_candidates.csv + printed tables."""
import re
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
pd.set_option("display.width", 320)
pd.set_option("display.max_columns", 40)
pd.set_option("display.max_colwidth", 38)
pd.set_option("display.max_rows", 400)

s7 = pd.read_csv("out_S07.csv", keep_default_na=False)
s8 = pd.read_csv("out_S08.csv", keep_default_na=False)
s9 = pd.read_csv("out_S09.csv", keep_default_na=False)
s10 = pd.read_csv("out_S10.csv", keep_default_na=False)
SNAP = pd.Timestamp("2026-07-23")
NSD = "253400M18U5TB02TW421"

lou = s8.drop_duplicates("LOU").set_index("LOU").LOU_NAME.to_dict()
lou_short = {k: v[:22] for k, v in lou.items()}

# --- noise in the OFAC remark regex
nl = s9[s9.G_LEI == ""]
cin = nl.LEI.str.match(r"^[UL]\d{5}[A-Z]{2}\d{4}[A-Z]{3}")
print("OFAC remark hits:", s9.LEI.nunique(), "landed:", s9[s9.G_LEI != ""].LEI.nunique(),
      "misses:", nl.LEI.nunique(), "of which Indian company numbers:", nl[cin].LEI.nunique())
print(nl[~cin][["LEI", "SDN_NAME"]].drop_duplicates("LEI").to_string())

# --- the SDN universe: OFAC's own printed LEIs, plus OpenSanctions SDN linkage
off = set(s9[s9.G_LEI != ""].LEI)
s7 = s7[s7.G_LEI != ""].copy()
s7["sdn"] = s7.DATASETS.str.contains("US OFAC Specially Designated Nationals")
s7["recip"] = pd.to_datetime(s7.OS_SANCTIONS.str.extract(r"Reciprocal - Active - (\d{4}-\d{2}-\d{2})")[0], errors="coerce")
s7["fs"] = pd.to_datetime(s7.FIRST_SEEN.str[:10])
os_sdn = s7[s7.sdn].sort_values("recip").drop_duplicates("LEI").set_index("LEI")
g9 = s9[s9.G_LEI != ""].drop_duplicates("LEI").set_index("LEI")

u = sorted(off | set(os_sdn.index))
rows = []
for lei in u:
    src = g9.loc[lei] if lei in g9.index else None
    o = os_sdn.loc[lei] if lei in os_sdn.index else None
    base = src if src is not None else o
    rows.append(dict(
        LEI=lei, on_ofac_list=lei in off, os_sdn=lei in os_sdn.index,
        sdn_name=(src.SDN_NAME if src is not None else o.OS_NAME),
        program=(src.PROGRAM if src is not None else o.PROGRAM_IDS),
        g_name=base.G_NAME, g_ctry=base.G_CTRY, g_rstatus=base.G_RSTATUS, g_lou=base.G_LOU,
        reg0=pd.Timestamp(str(base.G_REG0)[:10]), upd=pd.Timestamp(str(base.G_UPD)[:10]), nxt=pd.Timestamp(str(base.G_NEXT)[:10]),
        recip=(o.recip if o is not None else pd.NaT), fs=(o.fs if o is not None else pd.NaT),
    ))
d = pd.DataFrame(rows)
d["lou"] = d.g_lou.map(lou_short)
d["russian_office"] = d.g_lou == NSD
# listing-date proxy: SAM reciprocal exclusion date when present, else OpenSanctions first-seen
d["listed"] = d.recip.fillna(d.fs)
d["current"] = d.g_rstatus == "ISSUED"
d["paid_after"] = d.current & d.listed.notna() & ((d.nxt - pd.Timedelta(days=365)) > d.listed) & (d.upd > d.listed)
d["new_after"] = d.reg0 > d.listed

# second field: name agreement using GLEIF legal, other and Latin names
n10 = s10.set_index("LEI")


def norm(x):
    x = str(x).upper()
    x = re.sub(r"\b(LIMITED|LTD|LLC|L\.L\.C|PRIVATE|PVT|CO|COMPANY|INC|GMBH|AG|SA|S\.A|PLC|DMCC|FZE|FZCO|JSC|PJSC|OOO|LLP|AND|THE|OF)\b", " ", x)
    return set(t for t in re.findall(r"[A-Z0-9]{3,}", x))


def agree(r):
    a = norm(r.sdn_name)
    names = [r.g_name]
    if r.LEI in n10.index:
        z = n10.loc[r.LEI]
        names += [z.OTHER1, z.OTHER2, z.TRANSLIT1]
    for nm in names:
        b = norm(nm)
        if a and b and len(a & b) >= max(1, min(len(a), len(b)) // 2):
            return True
    return False


d["name_agree"] = d.apply(agree, axis=1)
d.to_csv("sanc_candidates.csv", index=False)

print("\nSDN universe landed in GLEIF:", len(d), "| on OFAC's own list:", d.on_ofac_list.sum(), "| OpenSanctions only:", (~d.on_ofac_list).sum())
print(pd.crosstab([d.russian_office], d.g_rstatus, margins=True))

nr = d[~d.russian_office]
print("\nNon-Russian offices, SDN LEIs: current", nr.current.sum(), "of", len(nr))
print("  paid period starts after listing:", nr.paid_after.sum(), "| new LEI issued after listing:", (nr.new_after & nr.current).sum())
print("  same, with name agreement:", (nr.paid_after & nr.name_agree).sum(), "| on OFAC's own list:", (nr.paid_after & nr.on_ofac_list).sum())

# peer: each office's current share, all its LEIs vs its SDN LEIs
allsh = s8.assign(N=s8.N.astype(int)).groupby("LOU").apply(lambda x: pd.Series({"all_n": x.N.sum(), "all_cur": x[x.RS == "ISSUED"].N.sum()}))
p = d.groupby("g_lou").agg(sdn_n=("LEI", "size"), sdn_cur=("current", "sum"), paid_after=("paid_after", "sum")).join(allsh)
p["sdn_cur_pct"] = (100 * p.sdn_cur / p.sdn_n).round(1)
p["all_cur_pct"] = (100 * p.all_cur / p.all_n).round(1)
p.index = p.index.map(lou_short)
print("\nPeer, by office:\n", p.sort_values("sdn_n", ascending=False).to_string())

show = nr[nr.paid_after].sort_values(["lou", "listed"])
print("\nCurrent SDN LEIs at non-Russian offices, paid period after listing:")
print(show[["LEI", "sdn_name", "g_name", "g_ctry", "lou", "on_ofac_list", "name_agree", "listed", "reg0", "upd", "nxt"]].to_string())


# ---------------- jurisdiction-matched pass (EU list at EU offices, UK list at UK office, US list at US office)
# Bound from S16: across all ISSUED records, the renewal date never sits more than 430 days past the last touch
# (0 exceptions at the offices below). So a renewal date D was set no earlier than D - 430 days.
s7a = pd.read_csv("out_S07.csv", keep_default_na=False)
s7a = s7a[s7a.G_LEI != ""].drop_duplicates("LEI").copy()
lc = s8.drop_duplicates("LOU").set_index("LOU").LOU_CTRY.to_dict()
s7a["lou_ctry"] = s7a.G_LOU.map(lc)
s7a["lou"] = s7a.G_LOU.map(lou_short)
s7a["nxt"] = pd.to_datetime(s7a.G_NEXT.str[:10])
s7a["upd"] = pd.to_datetime(s7a.G_UPD.str[:10])
s7a["reg0"] = pd.to_datetime(s7a.G_REG0.str[:10])
EU = {"FI", "DE", "BE", "IT", "SI", "SE", "LV", "FR", "NL", "ES", "PL", "CZ", "IE", "SK", "RO", "HR", "DK", "LU", "AT"}


def eudate(t):
    ds = re.findall(r"du (\d{2})/(\d{2})/(\d{4})", t)
    ds = [pd.Timestamp(f"{y}-{m}-{dd}") for dd, m, y in ds]
    return min(ds) if ds else pd.NaT


s7a["eu_dt"] = s7a.OS_SANCTIONS.apply(eudate)
# official EU publication dates from S14 (EU consolidated file dated 05/06/2026) override the parsed text
official = {"2549000P3CW62BCZQP37": "2025-07-19", "549300V3GQ2MCTQAIV68": "2025-07-19", "2549002ZHX4XEY7DNN77": "2025-07-19",
            "984500SAI1E9CB88DC54": "2026-04-23", "391200Y7BOFEZOE3X484": "2025-09-29", "39120020BBOSP6DZUC29": "2025-09-29",
            "5493007MJ3BLX55XSZ63": "2025-09-29", "8156003F584B25AD6C97": "2025-09-29", "894500MDF6I8J93LO347": "2025-09-29",
            "549300CGXEGG4L7QYT45": "2025-10-23"}
for k, v in official.items():
    s7a.loc[s7a.LEI == k, "eu_dt"] = pd.Timestamp(v)
e = s7a[s7a.DATASETS.str.contains("EU Financial Sanctions Files") & s7a.lou_ctry.isin(EU)].copy()
e["current"] = e.G_RSTATUS == "ISSUED"
e["set_after"] = e.current & ((e.nxt - pd.Timedelta(days=430)) > e.eu_dt)
print("\nEU-listed, ID at an EU office:", len(e), "| current:", e.current.sum(), "| renewal date set after EU listing (430-day bound):", e.set_after.sum())
print(e[["LEI", "OS_NAME", "G_NAME", "G_CTRY", "lou", "G_RSTATUS", "eu_dt", "reg0", "upd", "nxt", "set_after"]].sort_values(["G_RSTATUS", "eu_dt"]).to_string())
uk = s7a[s7a.DATASETS.str.contains("UK FCDO Sanctions List") & (s7a.lou_ctry == "GB")]
print("\nUK-listed, ID at the UK office:", len(uk), "| current:", (uk.G_RSTATUS == "ISSUED").sum())
us = s7a[s7a.DATASETS.str.contains("US OFAC Specially Designated Nationals") & (s7a.lou_ctry == "US")]
print("SDN-listed, ID at the US office:", len(us), "| current:", (us.G_RSTATUS == "ISSUED").sum())
print("  of those on OFAC's own printed list:", us.LEI.isin(off).sum(), "| current:", ((us.G_RSTATUS == "ISSUED") & us.LEI.isin(off)).sum())

d["set_after_430"] = d.current & d.listed.notna() & ((d.nxt - pd.Timedelta(days=430)) > d.listed)
nr = d[~d.russian_office]
print("\nSDN at non-Russian offices: current", nr.current.sum(), "| renewal date set after listing (430 bound):", nr.set_after_430.sum(),
      "| of those on OFAC's own list:", (nr.set_after_430 & nr.on_ofac_list).sum())
print(nr[nr.set_after_430 & nr.on_ofac_list][["LEI", "sdn_name", "g_ctry", "lou", "listed", "upd", "nxt"]].to_string())
