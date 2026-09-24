"""Actor pilot: find 25 well-known companies in every mart table that names parties.

Question it answers: does one company show up across enough domains, with clean matches,
to make "every public record about one company" worth building?

Read-only. One SELECT per table, all 25 companies at once. Python door only.
Writes hits.csv (one row per table x company) and log.txt next to this file.
"""
import csv
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
import ledger as L  # noqa: E402
from connect import db  # noqa: E402

OUT = Path(__file__).parent

# name, cheap substring for a prefilter, word-bounded pattern on the upper-cased value
COMPANIES = [
    ("Pfizer", "PFIZER", r"PFIZER"),
    ("Johnson & Johnson", "JOHNSON", r"JOHNSON ?(&|AND) ?JOHNSON"),
    ("Eli Lilly", "LILLY", r"ELI LILLY|LILLY USA"),
    ("AbbVie", "ABBVIE", r"ABBVIE"),
    ("Merck", "MERCK", r"MERCK SHARP|MERCK ?(&|AND) ?CO"),
    ("Lockheed Martin", "LOCKHEED", r"LOCKHEED"),
    ("Boeing", "BOEING", r"BOEING"),
    ("RTX Raytheon", "RAYTHEON", r"RAYTHEON|RTX CORP"),
    ("General Dynamics", "DYNAMICS", r"GENERAL DYNAMICS|ELECTRIC BOAT"),
    ("Northrop Grumman", "NORTHROP", r"NORTHROP"),
    ("Exxon Mobil", "EXXON", r"EXXON"),
    ("Chevron", "CHEVRON", r"CHEVRON"),
    ("Alliance Resource Partners", "ALLIANCE", r"ALLIANCE RESOURCE|ALLIANCE COAL"),
    ("Peabody Energy", "PEABODY", r"PEABODY (ENERGY|COAL|WESTERN|MIDWEST|POWDER|HOLDING)"),
    ("Duke Energy", "DUKE ENERGY", r"DUKE ENERGY"),
    ("Wells Fargo", "WELLS FARGO", r"WELLS FARGO"),
    ("JPMorgan Chase", "MORGAN", r"J\.? ?P\.? ?MORGAN|JPMORGAN|CHASE BANK"),
    ("Bank of America", "BANK OF AMERICA", r"BANK OF AMERICA"),
    ("HCA Healthcare", "HCA", r"HCA HEALTHCARE|HCA INC|HCA HOLDINGS|HOSPITAL CORPORATION OF AMERICA"),
    ("UnitedHealth", "UNITED", r"UNITEDHEALTH|UNITED HEALTHCARE|UNITED HEALTH GROUP|OPTUM"),
    ("CVS Health", "CVS", r"CVS"),
    ("Walmart", "MART", r"WAL-?MART"),
    ("Amazon", "AMAZON", r"AMAZON\.?COM|AMAZON WEB SERVICES|AMAZON LOGISTICS"),
    ("Tyson Foods", "TYSON", r"TYSON (FOODS|FRESH|CHICKEN)"),
    ("3M", "3M", r"3M COMPANY|3M CO|MINNESOTA MINING"),
]
# Columns labeled NAME that hold a category or an agency, not a party
SKIP_TOKENS = {"AGENCY", "OFFICE", "PURPOSE", "OCCUPANCY", "PREAPPROVAL", "ACTION", "RESPONSE", "SPECIALTY",
               "FIRST", "MIDDLE", "SURNAME", "TYPE", "DESCRIPTION", "STATUS", "COUNTY", "CITY", "STATE",
               "COUNTRY", "DRUG", "PRODUCT", "GENERIC", "BRAND", "PROGRAM", "PLAN", "LOAN", "PROPERTY"}
# The one giant where only one column matters
ONLY_COLS = {"FINANCE__FED_FEC_INDIV_CONTRIBUTIONS": ["EMPLOYER"]}
DOMAIN = {"HEALTH": "health", "JUSTICE": "justice", "CRIMINAL_JUSTICE": "justice", "JUDICIARY": "justice",
          "LEGAL_ENFORCEMENT": "justice", "POLITICS": "politics", "EDUCATION": "politics", "FINANCE": "money",
          "ECONOMICS": "money", "PROCUREMENT": "money", "CORPORATE_REGISTRY": "companies",
          "ENVIRONMENT": "environment", "ENERGY": "environment", "LABOR": "labor", "HOUSING": "housing",
          "IMMIGRATION": "immigration", "CONSUMER_PROTECTION": "consumer", "CONSUMER_SAFETY": "consumer",
          "TRANSPORT": "transport", "SCIENCE_RESEARCH": "science", "SCIENCE": "science", "MARITIME": "transport",
          "FOREIGN_INFLUENCE": "politics", "INVESTIGATIONS": "justice", "REGULATORY": "politics"}

lock = threading.Lock()
log = open(OUT / "log.txt", "a", encoding="utf-8")
stats = {"statements": 0, "errors": 0}


def say(msg):
    with lock:
        log.write(time.strftime("%H:%M:%S ") + msg + "\n")
        log.flush()
        print(msg, flush=True)


def party_cols(t):
    # a surname column fakes company hits, like a doctor named Northrop; keep LAST only beside ORG
    cols = ONLY_COLS.get(t["table"]) or [c for c in t["names"] if not set(L.toks(c)) & SKIP_TOKENS
                                         and not ("LAST" in L.toks(c) and "ORG" not in L.toks(c))]
    return cols[:6]


def sql_for(t, cols):
    fq = f'LIBRARY_MARTS."{t["schema"]}"."{t["table"]}"'
    union = " UNION ALL ".join(f'SELECT \'{c}\' AS col, UPPER("{c}"::varchar) AS v FROM {fq} WHERE "{c}" IS NOT NULL' for c in cols)
    likes = ", ".join(f"'%{sub}%'" for _, sub, _ in COMPANIES)
    cases = "\n".join(f"      WHEN REGEXP_INSTR(v, '(^|[^A-Z0-9])({pat.replace(chr(92), chr(92) * 2)})([^A-Z0-9]|$)') > 0 THEN {i}"
                      for i, (_, _, pat) in enumerate(COMPANIES))
    return f"""
WITH vals AS ({union}),
pre AS (SELECT col, v FROM vals WHERE v LIKE ANY ({likes})),
hit AS (SELECT col, v, CASE
{cases}
    END AS m FROM pre)
SELECT m, col, COUNT(*) AS n, COUNT(DISTINCT v) AS nd,
       ARRAY_TO_STRING(ARRAY_SLICE(ARRAY_AGG(DISTINCT v), 0, 6), ' | ') AS samp
FROM hit WHERE m IS NOT NULL GROUP BY m, col"""


def run(t, conn_pool):
    cols = party_cols(t)
    if not cols:
        return []
    c = conn_pool.get()
    try:
        t0 = time.time()
        rows = db.rows(c, sql_for(t, cols))
        stats["statements"] += 1
        say(f"ok  {time.time() - t0:6.1f}s  {t['table']}  hits={len(rows)}")
        return [dict(table=t["table"], schema=t["schema"], domain=DOMAIN.get(t["schema"], t["schema"].lower()),
                     company=COMPANIES[m][0], col=col, rows=n, distinct=nd, sample=s) for m, col, n, nd, s in rows]
    except Exception as e:  # a bad table must not stop the pilot
        stats["errors"] += 1
        say(f"ERR {t['table']}: {str(e)[:160]}")
        return []
    finally:
        conn_pool.put(c)


def main():
    import queue
    T = L.load_catalog()
    ts = [t for t in T.values() if t["names"] and not t["derived"] and not t["reference"]
          and t["table"] not in L.DUPLICATE_OF and t["rows"]]
    ts.sort(key=lambda t: t["rows"])  # small first, so progress shows early
    pool = queue.Queue()
    for _ in range(4):
        c = db.connect()
        db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
        pool.put(c)
    say(f"start: {len(ts)} tables, {len(COMPANIES)} companies")
    out = []
    with ThreadPoolExecutor(4) as ex:
        for res in ex.map(lambda t: run(t, pool), ts):
            out += res
    with (OUT / "hits.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["company", "domain", "schema", "table", "col", "rows", "distinct", "sample"])
        w.writeheader()
        for r in sorted(out, key=lambda r: (r["company"], r["domain"], -r["rows"])):
            w.writerow(r)
    say(f"done: {len(out)} hits, {stats['statements']} statements, {stats['errors']} errors")


if __name__ == "__main__":
    main()
