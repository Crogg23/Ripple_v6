"""Local join: IRS FATCA FFI list x OFAC SDN (via OpenSanctions rows sourced from the SDN list).
Name match after stripping legal-form words, then the country must agree (FATCA GIIN country vs OpenSanctions countries).
No warehouse statements; reads r03 and r17 pulls."""
import csv
import collections
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
LEGAL = set("""JSC PJSC OJSC CJSC AO PAO OAO ZAO OOO LLC LTD LIMITED LIABILITY COMPANY CO JOINT STOCK PUBLIC CLOSED OPEN
INC CORP CORPORATION SA S A PLC THE OF AG GMBH NV BV SAL SPA SRL LLP LP SE KG QSC PSC PJSC. JOINTSTOCK""".split())

# FATCA country name -> ISO2 for the countries that matter for sanctions matching (checked by hand)
ISO2 = {
    "RUSSIAN FEDERATION": "ru", "BELARUS": "by", "IRAN, ISLAMIC REPUBLIC OF": "ir", "SYRIAN ARAB REPUBLIC": "sy",
    "VENEZUELA, BOLIVARIAN REPUBLIC OF": "ve", "CUBA": "cu", "MYANMAR": "mm", "NICARAGUA": "ni", "LEBANON": "lb",
    "IRAQ": "iq", "AFGHANISTAN": "af", "SUDAN": "sd", "SOUTH SUDAN": "ss", "YEMEN": "ye", "LIBYA": "ly",
    "ZIMBABWE": "zw", "UNITED ARAB EMIRATES": "ae", "TURKEY": "tr", "CHINA": "cn", "HONG KONG": "hk", "CYPRUS": "cy",
    "KYRGYZSTAN": "kg", "KAZAKHSTAN": "kz", "ARMENIA": "am", "GEORGIA": "ge", "UZBEKISTAN": "uz", "TAJIKISTAN": "tj",
    "AZERBAIJAN": "az", "UKRAINE": "ua", "SWITZERLAND": "ch", "UNITED KINGDOM": "gb", "GERMANY": "de", "FRANCE": "fr",
    "AUSTRIA": "at", "LATVIA": "lv", "LITHUANIA": "lt", "ESTONIA": "ee", "SERBIA": "rs", "MOLDOVA, REPUBLIC OF": "md",
    "INDIA": "in", "SINGAPORE": "sg", "MALAYSIA": "my", "PAKISTAN": "pk", "CAYMAN ISLANDS": "ky",
    "VIRGIN ISLANDS (BRITISH)": "vg", "PANAMA": "pa", "LUXEMBOURG": "lu", "NETHERLANDS": "nl", "ITALY": "it",
    "HUNGARY": "hu", "BULGARIA": "bg", "MONGOLIA": "mn", "VIET NAM": "vn", "THAILAND": "th", "CURACAO": "cw",
    "KOREA, REPUBLIC OF": "kr", "JAPAN": "jp", "MALTA": "mt", "ISRAEL": "il", "JORDAN": "jo", "EGYPT": "eg",
    "SAUDI ARABIA": "sa", "QATAR": "qa", "BAHRAIN": "bh", "OMAN": "om", "KUWAIT": "kw", "TURKMENISTAN": "tm",
}


def norm(s):
    s = s.upper().replace("&", " AND ")
    s = re.sub(r"[^A-Z0-9 ]", " ", s)
    toks = [t for t in s.split() if t not in LEGAL]
    return " ".join(toks)


def main():
    ff = list(csv.DictReader(open(HERE / "r03_fatca_all.csv", encoding="utf-8")))
    os_ = list(csv.DictReader(open(HERE / "r17_opensanctions_orgs.csv", encoding="utf-8")))
    sdn = [r for r in os_ if "US OFAC Specially Designated Nationals" in r["DATASET"]
           and r["SCHEMA"] in ("Organization", "Company", "LegalEntity")]
    idx = collections.defaultdict(list)
    for r in sdn:
        names = [r["NAME"]] + [a for a in r["ALIASES"].split(";") if a]
        for n in names:
            k = norm(n)
            if len(k) >= 6 and len(k.split()) >= 1:
                idx[k].append(r)
    hits = []
    for f in ff:
        k = norm(f["INSTITUTION_NAME"])
        if k in idx and k not in ("BANK",):
            for r in idx[k]:
                c_ok = ISO2.get(f["COUNTRY_NAME"]) in (r["COUNTRIES"] or "").split(";")
                hits.append({"giin": f["GIIN"], "fatca_name": f["INSTITUTION_NAME"], "fatca_country": f["COUNTRY_NAME"],
                             "sdn_name": r["NAME"], "sdn_countries": r["COUNTRIES"], "programs": r["PROGRAM_IDS"],
                             "first_seen": r["FIRST_SEEN"], "country_agrees": c_ok, "key": k})
    # one row per GIIN, prefer a country-agreeing match
    best = {}
    for h in hits:
        if h["giin"] not in best or (h["country_agrees"] and not best[h["giin"]]["country_agrees"]):
            best[h["giin"]] = h
    out = sorted(best.values(), key=lambda h: (not h["country_agrees"], h["fatca_country"], h["fatca_name"]))
    (HERE / "fatca_sdn_hits.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("SDN org rows used:", len(sdn), "| FATCA rows:", len(ff))
    print("GIINs with a name hit:", len(out), "| country agrees:", sum(h["country_agrees"] for h in out))
    print(collections.Counter(h["fatca_country"] for h in out if h["country_agrees"]).most_common())
    for h in out:
        print(("OK " if h["country_agrees"] else "-- ") + f"{h['giin']} | {h['fatca_name'][:60]} | {h['fatca_country'][:18]} | {h['sdn_name'][:50]} | {h['sdn_countries']} | {h['programs'][:40]}")


if __name__ == "__main__":
    main()
