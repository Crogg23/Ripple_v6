"""Pick ~500 companies from the data itself: the biggest names in eight 'who gets money or does harm' lists.

No hand picking. Each list gives its top names by its own measure; names are normalized and merged.
A company that tops several lists is a better cross-domain candidate, so the source count is kept.
Writes lists.json (raw list results, so cleaning fixes need no warehouse rerun) and seeds.csv.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

OUT = Path(__file__).parent
TOP = 80
LISTS = {
    "contracts": """SELECT RECIPIENT_PARENT_NAME n, SUM(TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::varchar,38,2)) m
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 WHERE RECIPIENT_PARENT_NAME IS NOT NULL GROUP BY 1""",
    "doctor_payments": """SELECT APPLICABLE_MANUFACTURER_OR_APPLICABLE_GPO_MAKING_PAYMENT_NAME n, SUM(TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS) m
        FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS GROUP BY 1""",
    "lobbying": """SELECT CLIENT_NAME n, SUM(COALESCE(TRY_TO_NUMBER(INCOME::varchar,38,2),0)+COALESCE(TRY_TO_NUMBER(EXPENSES::varchar,38,2),0)) m
        FROM LIBRARY_MARTS.EDUCATION.EDUCATION__FED_SENATE_LDA_FILINGS GROUP BY 1""",
    "pacs": """SELECT CONNECTED_ORG_NM n, COUNT(*) m FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM
        WHERE CONNECTED_ORG_NM IS NOT NULL AND CMTE_TP IN ('Q','N') GROUP BY 1""",
    "toxic_release": """SELECT COALESCE(STANDARDIZED_PARENT_COMPANY, PARENT_CO_NAME) n, COUNT(*) m
        FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY GROUP BY 1""",
    "complaints": """SELECT COMPANY n, COUNT(*) m FROM LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS GROUP BY 1""",
    "injuries": """SELECT COMPANY_NAME n, SUM(TRY_TO_NUMBER(TOTAL_INJURIES::varchar)) m
        FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 GROUP BY 1""",
    "visas": """SELECT EMPLOYER_NAME n, COUNT(*) m FROM LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_DOL_OFLC GROUP BY 1""",
}
# Legal endings, stripped only from the end and repeatedly: "ELI LILLY AND COMPANY" -> "ELI LILLY".
# "BANK OF AMERICA" keeps "OF AMERICA" because it is in the middle of nothing: it is the name.
END = re.compile(r"\s+(INCORPORATED|INC|CORPORATION|CORP|COMPANY|CO|LLC|L L C|LLP|LP|L P|LTD|LIMITED|PLC|"
                 r"HOLDINGS|HOLDING|GROUP|N A|NA|AND|&|SUBSIDIARIES|SERVICES|SERVICE|BANK|USA|U S A|US|U S)$")
# A one-word core this common is a surname, a place or a plain word, not a company
TOO_COMMON = set("""AMERICAN NATIONAL UNITED GENERAL FIRST INTERNATIONAL GLOBAL STATE CITY COUNTY FEDERAL UNIVERSITY
    HEALTH MEDICAL CARE BANK CAPITAL ENERGY POWER SYSTEMS SOLUTIONS TECHNOLOGIES PARTNERS ASSOCIATES
    NORTHROP JOHNSON SMITH WILLIAMS BROWN JONES MILLER DAVIS WILSON ANDERSON TAYLOR THOMAS MOORE MARTIN
    JACKSON WHITE HARRIS CLARK LEWIS ROBINSON WALKER ALLEN KING WRIGHT SCOTT HILL GREEN ADAMS BAKER
    NELSON CARTER MITCHELL ROBERTS TURNER PHILLIPS CAMPBELL PARKER EVANS EDWARDS COLLINS STEWART LEE
    MORRIS MURPHY COOK ROGERS MORGAN BELL CHASE AMAZON APPLE ORACLE SHELL VISA TARGET CVS HCA LAUF""".split())


def clean(name):
    s = re.sub(r"[^A-Z0-9& ]", " ", (name or "").upper())
    return re.sub(r"\s+", " ", s).strip()


def core(name):
    s = re.sub(r"^THE\s+", "", clean(name))
    while True:
        t = END.sub("", s).strip()
        if t == s or not t:
            return s
        s = t


def pattern(c, raw_names=()):
    """Word-bounded words of the core. A short or common one-word core needs its full legal name instead."""
    words = c.split()
    if len(words) == 1 and (c in TOO_COMMON or len(c) < 3):
        full = sorted({clean(r) for r in raw_names if clean(r) != c}, key=len)
        if not full:
            return None  # a bare common word or two-letter acronym misfires; the pilot proved it
        words = full[0].split()
    return r"\s+".join(re.escape(w).replace("\\&", "&") for w in words)


def fetch():
    from connect import db
    c = db.connect()
    db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    got = {}
    for lst, sql in LISTS.items():
        got[lst] = [[n, float(m or 0)] for n, m in
                    db.rows(c, f"SELECT n, m FROM ({sql}) WHERE n IS NOT NULL ORDER BY m DESC NULLS LAST LIMIT {TOP * 2}")]
        print(f"{lst}: {len(got[lst])} rows", flush=True)
    got["_sec"] = [[cik, n] for cik, n in db.rows(c, """SELECT DISTINCT TRY_TO_NUMBER(CIK)::varchar, COMPANY_NAME
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE""")]
    (OUT / "lists.json").write_text(json.dumps(got), encoding="utf-8")
    return got


def main():
    cache = OUT / "lists.json"
    got = json.loads(cache.read_text(encoding="utf-8")) if cache.exists() and "--refetch" not in sys.argv else fetch()
    seeds = {}
    for lst in LISTS:
        kept = 0
        for n, _ in got[lst]:
            k = core(n)
            if not k or kept >= TOP:
                continue
            s = seeds.setdefault(k, {"lists": set(), "raw": set()})
            s["lists"].add(lst)
            s["raw"].add(n)
            kept += 1
    sec = {core(n): cik for cik, n in got["_sec"]}
    with (OUT / "seeds.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["core", "pattern", "n_lists", "lists", "cik", "raw_names"])
        for k, s in sorted(seeds.items(), key=lambda kv: (-len(kv[1]["lists"]), kv[0])):
            w.writerow([k, pattern(k, s["raw"]) or "", len(s["lists"]), " ".join(sorted(s["lists"])),
                        sec.get(k, ""), " | ".join(sorted(s["raw"]))[:300]])
    print(f"seeds: {len(seeds)}; with a usable pattern: {sum(1 for k, v in seeds.items() if pattern(k, v['raw']))}", flush=True)


if __name__ == "__main__":
    main()
