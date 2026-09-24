"""Rank the cross-reference companies by harm, fairly.

Per company, from name matches with the same strict rules as scan_500.py:
  contracts  R2 obligations with ACTION_DATE in FY2023-24, by recipient or parent name
  injuries   OSHA 300A 2023+2024: recordable cases, deaths, hours; expected cases at the company's own
             industry rate (NAICS 3-digit), so a meatpacker is compared to meatpackers
  pollution  ECHO facilities, formal actions, serious-violator flags, allocated last penalty (trap: never TOTAL_PENALTIES)
Read-only. Writes harm_rank.csv.
"""
import csv
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).parent))
from connect import db  # noqa: E402
import scan_500 as S  # noqa: E402

OUT = Path(__file__).parent
JUNK = {"NONE", "DE LA CRUZ", "WASTE MANAGEMENT", "METHODIST HOSPITAL", "PROVIDENCE HEALTH", "SIERRA NEVADA",
        "COMPUTER SCIENCES", "HEALTH NET", "DISCOUNT TIRE", "CHAMBER OF COMMERCE OF THE",
        "GOVERNMENT OF THE UNITED STATES", "COMPASS", "AEROSPACE", "AARP LIMITED", "SAFEWAY COMPANY LIMITED", "ASHLAND"}


def pats_cte(pats):
    vals = ",\n".join("({}, '{}', '{}')".format(i, a.replace("'", "''"), S.rx(p).replace("\\", "\\\\").replace("'", "''"))
                      for i, a, p, _ in pats)
    return f"pats(id, anchor, rx) AS (SELECT * FROM VALUES {vals})"


def matcher(src, key_cols, name_cols):
    """Rows of src tagged with the company ids whose pattern matches any of the name columns."""
    names = " UNION ".join(f"SELECT {key_cols}, TRIM(REGEXP_REPLACE(UPPER({c}::varchar), '[^A-Z0-9&]+', ' ')) nv FROM {src} WHERE {c} IS NOT NULL"
                           for c in name_cols)
    return f"""named AS ({names}),
words AS (SELECT DISTINCT {key_cols}, nv, w.value::string tok FROM named, LATERAL SPLIT_TO_TABLE(nv, ' ') w),
tagged AS (SELECT DISTINCT {key_cols}, p.id FROM words JOIN pats p ON words.tok = p.anchor WHERE REGEXP_INSTR(words.nv, p.rx) > 0)"""


def main():
    rows, pats = S.load_seeds()
    pats = [p for p in pats if p[3] not in JUNK]
    c = db.connect()
    db.rows(c, "ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 900")
    P = pats_cte(pats)
    out = {}

    t0 = time.time()
    q = f"""WITH {P},
    src AS (SELECT RECIPIENT_NAME rn, RECIPIENT_PARENT_NAME pn, SUM(TRY_TO_NUMBER(FEDERAL_ACTION_OBLIGATION::varchar,38,2)) d
            FROM LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2
            WHERE TRY_TO_DATE(ACTION_DATE::varchar) BETWEEN '2022-10-01' AND '2024-09-30' GROUP BY 1, 2),
    keyed AS (SELECT ROW_NUMBER() OVER (ORDER BY rn, pn) k, * FROM src),
    {matcher('keyed', 'k', ['rn', 'pn'])}
    SELECT t.id, SUM(keyed.d) FROM tagged t JOIN keyed ON keyed.k = t.k GROUP BY 1"""
    for i, d in db.rows(c, q):
        out.setdefault(i, {})["contract_usd"] = float(d or 0)
    print(f"contracts {time.time() - t0:.0f}s", flush=True)

    t0 = time.time()
    q = f"""WITH {P},
    raw AS (
      SELECT ESTABLISHMENT_ID eid, COMPANY_NAME cn, ESTABLISHMENT_NAME en, LEFT(NAICS_CODE::varchar, 3) n3,
             COALESCE(TRY_TO_NUMBER(TOTAL_DAFW_CASES::varchar),0)+COALESCE(TRY_TO_NUMBER(TOTAL_DJTR_CASES::varchar),0)
               +COALESCE(TRY_TO_NUMBER(TOTAL_OTHER_CASES::varchar),0) cases,
             COALESCE(TRY_TO_NUMBER(TOTAL_DEATHS::varchar),0) deaths, TRY_TO_NUMBER(TOTAL_HOURS_WORKED::varchar) hrs, '2023' yr
      FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023
      UNION ALL
      SELECT ESTABLISHMENT_ID, COMPANY_NAME, ESTABLISHMENT_NAME, LEFT(NAICS_CODE::varchar, 3),
             COALESCE(TRY_TO_NUMBER(TOTAL_DAFW_CASES::varchar),0)+COALESCE(TRY_TO_NUMBER(TOTAL_DJTR_CASES::varchar),0)
               +COALESCE(TRY_TO_NUMBER(TOTAL_OTHER_CASES::varchar),0),
             COALESCE(TRY_TO_NUMBER(TOTAL_DEATHS::varchar),0), TRY_TO_NUMBER(TOTAL_HOURS_WORKED::varchar), '2024'
      FROM LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024),
    base AS (SELECT ROW_NUMBER() OVER (ORDER BY yr, eid) k, * FROM raw
             WHERE hrs BETWEEN 2000 AND 200000000),  -- trap: employee and hour counts have typos up to 172M
    rate AS (SELECT n3, SUM(cases) / SUM(hrs) r FROM base GROUP BY 1),
    {matcher('base', 'k', ['cn', 'en'])}
    SELECT t.id, COUNT(*) sites, SUM(b.cases), SUM(b.deaths), SUM(b.hrs), SUM(b.hrs * r.r)
    FROM tagged t JOIN base b ON b.k = t.k JOIN rate r ON r.n3 = b.n3 GROUP BY 1"""
    for i, sites, cases, deaths, hrs, exp in db.rows(c, q):
        o = out.setdefault(i, {})
        o.update(osha_sites=sites, cases=float(cases), deaths=float(deaths), hours=float(hrs), expected=float(exp or 0))
    print(f"osha {time.time() - t0:.0f}s", flush=True)

    t0 = time.time()
    q = f"""WITH {P},
    base AS (SELECT FRS_ID k, FACILITY_NAME fn, TRY_TO_NUMBER(FORMAL_ACTION_COUNT::varchar) fa,
                    IFF(SIGNIFICANT_NONCOMPLIANCE_FLAG::varchar IN ('Y','TRUE','true','1'), 1, 0) snc,
                    TRY_TO_NUMBER(LAST_PENALTY_AMT_ALLOCATED::varchar,38,2) pen
             FROM LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO),
    {matcher('base', 'k', ['fn'])}
    SELECT t.id, COUNT(DISTINCT b.k), SUM(b.fa), SUM(b.snc), SUM(b.pen)
    FROM tagged t JOIN base b ON b.k = t.k GROUP BY 1"""
    for i, fac, fa, snc, pen in db.rows(c, q):
        out.setdefault(i, {}).update(epa_sites=fac, formal_actions=float(fa or 0), serious_violator=float(snc or 0),
                                      penalty_alloc=float(pen or 0))
    print(f"echo {time.time() - t0:.0f}s", flush=True)

    cols = ["company", "lists", "contract_usd", "osha_sites", "cases", "deaths", "hours", "expected", "epa_sites",
            "formal_actions", "serious_violator", "penalty_alloc"]
    with (OUT / "harm_rank.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for i, o in out.items():
            w.writerow(dict(company=rows[i]["core"], lists=rows[i]["lists"], **o))
    print(f"done: {len(out)} companies", flush=True)


if __name__ == "__main__":
    main()
