"""g52 local math on the extracts (no warehouse calls). Run from g52/: python local.py
Recomputes every number quoted in g52.md from out_S02..out_S11 csv files."""
import re
import pandas as pd

pd.set_option("display.width", 250)
MO = "ABCDEFGHJKLM"  # ATF expiration month letters, no I


def norm(s):
    s = s.upper().replace(".", " ").replace(",", " ")
    s = re.sub(r"\b(SUITE|STE|UNIT|BLDG|BUILDING|APT|RM|ROOM|SPACE|SPC|BOX|LOT|OFFICE|OFC|BAY|DOOR|#).*$", "", s)
    for a, b in [("ROAD", "RD"), ("STREET", "ST"), ("AVENUE", "AVE"), ("HIGHWAY", "HWY"), ("DRIVE", "DR"), ("BOULEVARD", "BLVD")]:
        s = re.sub(rf"\b{a}\b", b, s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"(\s[0-9A-Z]{0,3}-?[0-9]+[A-Z]?(-[0-9A-Z]+)*)$",
               lambda m: "" if re.match(r"^\d+\s", s) and len(s.split()) > 3 else m.group(0), s)
    return s


# ---------- ATF ----------
f = pd.read_csv("out_S02.csv", dtype=str, keep_default_na=False)
print("ATF rows", len(f), "distinct FFL", f.FFL_NUMBER.nunique())
print("types", f.LIC_TYPE.value_counts().to_dict())
print("zip widths", f.PREMISE_ZIP_CODE.str.len().value_counts().to_dict())
f["bldg"] = f.PREMISE_STREET.map(norm) + "|" + f.PREMISE_CITY.str.upper() + "|" + f.PREMISE_STATE
b = f.groupby("bldg").agg(n=("FFL_NUMBER", "size"), names=("LICENSE_NAME", "nunique"),
                          t07=("LIC_TYPE", lambda s: (s == "7").sum()), phones=("VOICE_PHONE", "nunique"),
                          mailcities=("MAIL_CITY", "nunique")).sort_values("names", ascending=False)
print(b.head(6).to_string())
print("buildings", len(b), "median licenses/building", b.n.median(), ">=10 names", (b.names >= 10).sum())
sh = b[b.names >= 4].copy()
sh["st"] = sh.index.str.split("|").str[-1]
t = sh.groupby("st").agg(bldgs=("n", "size"), t07=("t07", "sum"))
t["t07_state"] = f[f.LIC_TYPE == "7"].groupby("PREMISE_STATE").size()
t["share"] = t.t07 / t.t07_state
print(t.sort_values("share", ascending=False).head(6).round(3).to_string())
print("median state share of type-07 in shared buildings (all states, 0 if none):",
      (t.share.reindex(f.PREMISE_STATE.unique()).fillna(0)).median())
ma = f[f.PREMISE_STATE == "MA"]
print("MA 07+10", ma.LIC_TYPE.isin(["7", "10"]).sum(), "MA 01+02", ma.LIC_TYPE.isin(["1", "2"]).sum())
f["exp"] = f.LIC_EXPIRATION_CODE.map(lambda c: pd.Timestamp(2020 + int(c[0]), MO.index(c[1]) + 1, 1))
print("expiration months, last 3:", f.exp.dt.to_period("M").value_counts().sort_index().tail(3).to_dict())
old = f[f.exp < "2026-04-01"]
print("listed but expired before 2026-04:", len(old), old.exp.min().date(), old.exp.max().date())
print("expired 2026-04..06:", ((f.exp >= "2026-04-01") & (f.exp < "2026-07-01")).sum())

# ---------- DPRK ----------
a = pd.read_csv("out_S03.csv", dtype=str, keep_default_na=False)
n = pd.read_csv("out_S04.csv", dtype=str, keep_default_na=False)
n["F1"] = n.F1.astype(int)
n = n.sort_values("F1").reset_index(drop=True)
a303 = a[a.DATE <= "2024-11-04"].reset_index(drop=True)
same_outcome = (a303.OUTCOME.str.lower() == n.TEST_OUTCOME.str.lower()).sum()
same_month = (a303.DATE.str[:7] == n.DATE.str[:7]).sum()
print("NAGIX rows", len(a), "<=2024-11-04", len(a303), "NTI", len(n), "same outcome", same_outcome, "same month", same_month)
late = a[a.DATE > "2024-11-04"]
print("extra rows", len(late), late.DATE.min(), late.DATE.max(), late.OUTCOME.value_counts().to_dict())
a["md"] = a.DATE.str[5:10]
for y in range(2022, 2027):
    s = a[(a.DATE.str[:4] == str(y)) & (a.DATE.str.len() == 10) & (a.md <= "05-26")]
    print(y, "Jan1-May26 missiles", len(s), "days", s.DATE.nunique())

# ---------- OFAC ----------
v = pd.read_csv("sdn_vessels.csv", dtype=str, keep_default_na=False)
hits = pd.read_csv("out_S06.csv", dtype=str)
print("AIS hits", len(hits), hits[["VESSEL_NAME", "IMO", "PINGS", "DAYS", "LAT", "LON"]].to_dict("records"))
os_ = pd.read_csv("out_S11.csv", dtype=str, keep_default_na=False)
os_["fs"] = pd.to_datetime(os_.FIRST_SEEN.str[:10])
m = os_[os_.IMO != ""].groupby("IMO").fs.min()
v["fs"] = v.imo.map(m)
print("SDN vessels", len(v), "dated", v.fs.notna().sum(), "before 2024", (v.fs < "2024-01-01").sum(), "after AIS week", (v.fs >= "2024-01-09").sum())
