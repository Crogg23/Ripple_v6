"""Injury rates against each company's own exact industry, the company itself left out of its benchmark.

OSHA 300A 2023+2024, recordable cases per 200,000 hours (the standard rate: 100 full-time workers a year).
Benchmark: all other establishments in the same 6-digit NAICS; if they log under 5M hours, the 4-digit group.
Also re-pulls EPA with QUARTERS_WITH_NONCOMPLIANCE, since SIGNIFICANT_NONCOMPLIANCE_FLAG is 'N' on every row.
Joins contract dollars from harm_rank.csv. Writes injury_rank.csv.
"""
import collections
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from connect import db  # noqa: E402
import scan_500 as S  # noqa: E402
from rank_harm import JUNK, pats_cte, matcher  # noqa: E402

OUT = Path(__file__).parent


def main():
    rows, pats = S.load_seeds()
    pats = [p for p in pats if p[3] not in JUNK]
    c = db.connect()
    db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 600")
    raw = """
      SELECT ESTABLISHMENT_ID eid, COMPANY_NAME cn, ESTABLISHMENT_NAME en, NAICS_CODE::varchar n6,
             COALESCE(TRY_TO_NUMBER(TOTAL_DAFW_CASES::varchar),0)+COALESCE(TRY_TO_NUMBER(TOTAL_DJTR_CASES::varchar),0)
               +COALESCE(TRY_TO_NUMBER(TOTAL_OTHER_CASES::varchar),0) cases,
             COALESCE(TRY_TO_NUMBER(TOTAL_DEATHS::varchar),0) deaths, TRY_TO_NUMBER(TOTAL_HOURS_WORKED::varchar) hrs, '{y}' yr
      FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_{y}"""
    base = f"""raw AS ({raw.format(y=2023)} UNION ALL {raw.format(y=2024)}),
      base AS (SELECT ROW_NUMBER() OVER (ORDER BY yr, eid) k, * FROM raw WHERE hrs BETWEEN 2000 AND 200000000)"""
    ind = {n6: (float(cs), float(h)) for n6, cs, h in db.rows(c, f"WITH {base} SELECT n6, SUM(cases), SUM(hrs) FROM base GROUP BY 1")}
    co = db.rows(c, f"""WITH {pats_cte(pats)}, {base}, {matcher('base', 'k', ['cn', 'en'])}
        SELECT t.id, b.n6, COUNT(*), SUM(b.cases), SUM(b.deaths), SUM(b.hrs)
        FROM tagged t JOIN base b ON b.k = t.k GROUP BY 1, 2""")
    epa = {i: (int(f), float(fa or 0), float(q or 0)) for i, f, fa, q in db.rows(c, f"""WITH {pats_cte(pats)},
        base AS (SELECT FRS_ID k, FACILITY_NAME fn, TRY_TO_NUMBER(FORMAL_ACTION_COUNT::varchar) fa,
                        TRY_TO_NUMBER(QUARTERS_WITH_NONCOMPLIANCE::varchar) q
                 FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO),
        {matcher('base', 'k', ['fn'])}
        SELECT t.id, COUNT(DISTINCT b.k), SUM(b.fa), SUM(b.q) FROM tagged t JOIN base b ON b.k = t.k GROUP BY 1""")}

    ind4 = collections.defaultdict(lambda: [0.0, 0.0])
    for n6, (cs, h) in ind.items():
        ind4[n6[:4]][0] += cs
        ind4[n6[:4]][1] += h
    by = collections.defaultdict(lambda: dict(sites=0, cases=0.0, deaths=0.0, hours=0.0, expected=0.0, n6=collections.Counter()))
    mine6 = collections.defaultdict(lambda: [0.0, 0.0])
    for i, n6, sites, cs, d, h in co:
        mine6[(i, n6)][0] += float(cs)
        mine6[(i, n6)][1] += float(h)
    for (i, n6), (cs, h) in mine6.items():
        oc, oh = ind.get(n6, (0.0, 0.0))
        oc, oh = oc - cs, oh - h  # the company is not its own benchmark
        if oh < 5e6:
            oc, oh = ind4[n6[:4]][0] - cs, ind4[n6[:4]][1] - h
        rate = oc / oh if oh > 0 else None
        b = by[i]
        b["cases"] += cs
        b["hours"] += h
        b["expected"] += h * rate if rate else cs  # no benchmark: count it as exactly average
        b["n6"][n6] += h
    for i, n6, sites, cs, d, h in co:
        by[i]["sites"] += int(sites)
        by[i]["deaths"] += float(d)

    money = {r["company"]: float(r["contract_usd"] or 0) for r in csv.DictReader(open(OUT / "harm_rank.csv", encoding="utf-8"))}
    cols = ["company", "contract_usd", "osha_sites", "cases", "deaths", "hours", "rate", "industry_rate", "x_industry",
            "top_naics", "epa_sites", "epa_formal_actions", "epa_noncompliance_quarters"]
    with (OUT / "injury_rank.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for i in set(by) | set(epa):
            b = by.get(i, {})
            h = b.get("hours", 0)
            e = epa.get(i, (0, 0, 0))
            w.writerow(dict(company=rows[i]["core"], contract_usd=money.get(rows[i]["core"], 0),
                            osha_sites=b.get("sites", 0), cases=b.get("cases", 0), deaths=b.get("deaths", 0), hours=h,
                            rate=round(b["cases"] * 2e5 / h, 2) if h else "",
                            industry_rate=round(b["expected"] * 2e5 / h, 2) if h else "",
                            x_industry=round(b["cases"] / b["expected"], 2) if h and b["expected"] else "",
                            top_naics=b["n6"].most_common(1)[0][0] if h else "",
                            epa_sites=e[0], epa_formal_actions=e[1], epa_noncompliance_quarters=e[2]))
    print("done", len(by), "companies with injuries,", len(epa), "with EPA", flush=True)


if __name__ == "__main__":
    main()
