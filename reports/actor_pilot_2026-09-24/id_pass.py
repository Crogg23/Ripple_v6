"""Actor pilot, pass two: the same 25 companies found by ID instead of name.

Anchors: ticker -> SEC CIK -> EIN from SEC financials; contractor UEIs from contracts R2 by name.
Then every mart table carrying a CIK, EIN or UEI column is counted for those IDs.
Name hits can be namesakes; ID hits can't. Comparing the two grades the name matches.

Read-only. Writes ids.csv (the anchors) and id_hits.csv next to this file.
"""
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
import ledger as L  # noqa: E402
from connect import db  # noqa: E402
from pilot import COMPANIES, DOMAIN  # noqa: E402

OUT = Path(__file__).parent
TICKERS = ["PFE", "JNJ", "LLY", "ABBV", "MRK", "LMT", "BA", "RTX", "GD", "NOC", "XOM", "CVX", "ARLP", "BTU",
           "DUK", "WFC", "JPM", "BAC", "HCA", "UNH", "CVS", "WMT", "AMZN", "TSN", "MMM"]
KEYS = {"CIK", "EIN", "UEI"}


def norm(k, col):
    """One form per ID. EINs pad to 9 digits, CIKs compare as numbers (trap ein-and-cik-width-mismatch)."""
    c = f'"{col}"'
    if k == "EIN":
        return f"LPAD(REGEXP_REPLACE({c}::varchar, '[^0-9]', ''), 9, '0')"
    if k == "CIK":
        return f"TRY_TO_NUMBER(REGEXP_REPLACE({c}::varchar, '[^0-9]', ''))::varchar"
    return f"UPPER(TRIM({c}::varchar))"


def main():
    c = db.connect()
    db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
    n_stmt = 0
    ids = {i: {"CIK": set(), "EIN": set(), "UEI": set()} for i in range(len(COMPANIES))}

    tick = ",".join(f"'{t}'" for t in TICKERS)
    for cik, tk in db.rows(c, f"""SELECT DISTINCT TRY_TO_NUMBER(CIK)::varchar, TICKER
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE WHERE TICKER IN ({tick})"""):
        ids[TICKERS.index(tk)]["CIK"].add(cik)
    n_stmt += 1
    cik_to_i = {cik: i for i, v in ids.items() for cik in v["CIK"]}
    ciks = ",".join(f"'{k}'" for k in cik_to_i)
    for cik, ein in db.rows(c, f"""SELECT DISTINCT TRY_TO_NUMBER(CIK)::varchar, LPAD(REGEXP_REPLACE(EIN::varchar,'[^0-9]',''),9,'0')
        FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_EDGAR_FINANCIALS
        WHERE TRY_TO_NUMBER(CIK)::varchar IN ({ciks}) AND EIN IS NOT NULL AND EIN::varchar NOT IN ('', '000000000')"""):
        ids[cik_to_i[cik]]["EIN"].add(ein)
    n_stmt += 1

    # contractor UEIs: recipients whose own or parent name matches, top 20 by dollars per company
    likes = ", ".join(f"'%{sub}%'" for _, sub, _ in COMPANIES)
    cases = "\n".join(f"WHEN REGEXP_INSTR(v, '(^|[^A-Z0-9])({pat.replace(chr(92), chr(92) * 2)})([^A-Z0-9]|$)') > 0 THEN {i}"
                      for i, (_, _, pat) in enumerate(COMPANIES))
    t0 = time.time()
    rows = db.rows(c, f"""WITH r AS (
        SELECT UPPER(TRIM(RECIPIENT_UEI)) uei, UPPER(COALESCE(RECIPIENT_PARENT_NAME, RECIPIENT_NAME)) v,
               SUM(TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::varchar, 38, 2)) dollars
        FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2
        WHERE RECIPIENT_UEI IS NOT NULL
          AND UPPER(COALESCE(RECIPIENT_PARENT_NAME, RECIPIENT_NAME)) LIKE ANY ({likes})
        GROUP BY 1, 2),
      m AS (SELECT uei, dollars, CASE {cases} END AS co FROM r)
      SELECT co, uei, dollars FROM m WHERE co IS NOT NULL
      QUALIFY ROW_NUMBER() OVER (PARTITION BY co ORDER BY dollars DESC NULLS LAST) <= 20""")
    n_stmt += 1
    print(f"UEI anchor scan {time.time() - t0:.0f}s, {len(rows)} UEIs", flush=True)
    for co, uei, _ in rows:
        ids[co]["UEI"].add(uei)

    with (OUT / "ids.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["company", "ticker", "ciks", "eins", "ueis"])
        for i, (name, _, _) in enumerate(COMPANIES):
            w.writerow([name, TICKERS[i], " ".join(sorted(ids[i]["CIK"])), " ".join(sorted(ids[i]["EIN"])),
                        " ".join(sorted(ids[i]["UEI"]))])

    # every table with one of these keys, counted per company
    T = L.load_catalog()
    out = []
    for t in sorted(T.values(), key=lambda t: t["rows"]):
        if t["derived"] or t["reference"] or t["table"] in L.DUPLICATE_OF or not t["rows"]:
            continue
        for k in sorted(KEYS & set(t["keys"])):
            if (k, t["table"]) in L.KEY_DEAD:
                continue
            vals = [(i, v) for i in ids for v in ids[i][k]]
            if not vals:
                continue
            lst = ", ".join(f"({i}, '{v}')" for i, v in vals)
            for col in t["keys"][k][:3]:
                if (t["table"], col) in L.BAD_COLS:
                    continue
                sql = f"""WITH ids(co, v) AS (SELECT * FROM VALUES {lst})
                    SELECT ids.co, COUNT(*) FROM LIBRARY_MARTS."{t['schema']}"."{t['table']}" x
                    JOIN ids ON {norm(k, col)} = ids.v GROUP BY 1"""
                try:
                    t0 = time.time()
                    res = db.rows(c, sql)
                    n_stmt += 1
                    print(f"ok {time.time() - t0:5.1f}s {t['table']}.{col} hits={len(res)}", flush=True)
                    for co, n in res:
                        out.append(dict(company=COMPANIES[co][0], domain=DOMAIN.get(t["schema"], t["schema"].lower()),
                                        table=t["table"], key=k, col=col, rows=n))
                except Exception as e:
                    print(f"ERR {t['table']}.{col}: {str(e)[:140]}", flush=True)
    with (OUT / "id_hits.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["company", "domain", "table", "key", "col", "rows"])
        w.writeheader()
        w.writerows(sorted(out, key=lambda r: (r["company"], r["domain"])))
    print(f"done: {len(out)} id hits, {n_stmt} statements", flush=True)


if __name__ == "__main__":
    main()
