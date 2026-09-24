"""Read hits_500.csv and find the crossings: companies that sit where money, harm and power meet.

Each hit table is sorted into a role by the ledger's own tags and schema:
  money  - the company is paid or pays: contracts, grants, doctor payments, loans
  harm   - the company is cited, fined, sued, complained about, injures or pollutes
  power  - the company lobbies, runs a PAC, or its people donate
A hit only counts when the matched column looks like a party column and the group is not a namesake swarm.
Writes crossings.csv (one row per company) and prints the summary.
"""
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import ledger as L  # noqa: E402

OUT = Path(__file__).parent
csv.field_size_limit(10 ** 8)
POWER = ("LDA", "LOBBY", "FEC", "PAC", "IRS527", "CAMPAIGN", "CFB", "CONTRIBUTION", "FARA")
MONEY_T = ("USASPENDING", "CONTRACT", "GRANT", "ASSISTANCE", "OPEN_PAYMENTS", "PPP", "SBA", "SBIR", "NIH",
           "PROCUREMENT", "SUBSIDY")
HARM_T = ("ECHO", "TRI_", "VIOLATION", "PENALT", "ENFORCE", "COMPLAINT", "RECALL", "DOCKET", "OPINION",
          "OSHA", "MSHA", "EXCLUSION", "DEBAR", "SANCTION", "FAERS", "DEFICIEN", "ACCIDENT", "INCIDENT",
          "SPILL", "GHGRP", "WARNING", "CASE")


def role(table, tags):
    t = table.upper()
    if any(k in t for k in POWER):
        return "power"
    if any(k in t for k in HARM_T) or "HARM" in tags:
        return "harm"
    if any(k in t for k in MONEY_T) or "MONEY" in tags:
        return "money"
    return "other"


def main():
    T = L.load_catalog()
    hits = list(csv.DictReader(open(OUT / "hits_500.csv", encoding="utf-8")))
    co = collections.defaultdict(lambda: {"domains": set(), "roles": collections.defaultdict(set), "tables": set(), "lists": ""})
    swarm = 0
    for h in hits:
        # a group with thousands of distinct matched names is a namesake swarm, not one company
        if int(h["distinct"] or 0) > 400:
            swarm += 1
            continue
        c = co[h["company"]]
        c["lists"] = h["lists"]
        c["domains"].add(h["domain"])
        c["tables"].add(h["table"])
        c["roles"][role(h["table"], T.get(h["table"], {}).get("tags", []))].add(h["table"].split("__", 1)[-1])
    rows = []
    for name, c in co.items():
        r = c["roles"]
        rows.append(dict(company=name, lists=c["lists"], domains=len(c["domains"]), tables=len(c["tables"]),
                         money=len(r["money"]), harm=len(r["harm"]), power=len(r["power"]),
                         all_three="yes" if r["money"] and r["harm"] and r["power"] else "",
                         domain_list=" ".join(sorted(c["domains"])),
                         harm_tables=" | ".join(sorted(r["harm"]))[:400], power_tables=" | ".join(sorted(r["power"]))[:300],
                         money_tables=" | ".join(sorted(r["money"]))[:300]))
    rows.sort(key=lambda r: (-(r["all_three"] == "yes"), -r["domains"], -r["tables"]))
    with (OUT / "crossings.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    n = len(rows)
    print(f"companies found: {n} · namesake swarms dropped: {swarm}")
    print(f"money + harm + power: {sum(r['all_three'] == 'yes' for r in rows)}")
    for k in (4, 6, 8, 10):
        print(f"  in {k}+ domains: {sum(r['domains'] >= k for r in rows)}")
    print("\ntop 15 by domains")
    for r in rows[:15]:
        print(f"  {r['company'][:30]:30} dom={r['domains']:2} tab={r['tables']:3} money={r['money']:2} harm={r['harm']:2} power={r['power']:2}")


if __name__ == "__main__":
    main()
