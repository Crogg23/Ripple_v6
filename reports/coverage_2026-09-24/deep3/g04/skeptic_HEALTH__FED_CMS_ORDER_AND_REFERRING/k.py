"""Skeptic read-only runner. SELECT/WITH only. Usage: python k.py Q1 [Q2 ...]"""
import sys, json, re, datetime, decimal
from pathlib import Path
HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
sys.path.insert(0, str(REPO))
from connect import db

CTE = """
o AS (SELECT npi, MAX(partb) pb, MAX(pmd) pmd, MAX(dme) dme, MAX(hha) hha, MAX(hospice) hos
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
f AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FISCAL_INTERMEDIARY_SHARED_SYSTEM_ATTENDING_AND_RENDERING),
b AS (SELECT rndrng_npi npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
      WHERE rndrng_prvdr_ent_cd = 'I' GROUP BY 1)
"""

Q = {}
Q['Q1'] = """
WITH n AS (
  SELECT npi, npi_deactivation_date dd, npi_reactivation_date rd, entity_type_code et,
         npi_deactivation_reason_code rc, replacement_npi rn
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES WHERE npi_deactivation_date >= '2024-07-01'
),""" + CTE + """,
j AS (
  SELECT n.*, IFF(rd IS NULL OR rd < dd, 1, 0) sd, o.npi onpi, o.pb, o.pmd, o.dme, o.hha, o.hos, f.npi fnpi, b.npi bnpi
  FROM n LEFT JOIN o ON o.npi = n.npi LEFT JOIN f ON f.npi = n.npi LEFT JOIN b ON b.npi = n.npi
)
SELECT 'month' kind, TO_CHAR(DATE_TRUNC('month', dd), 'YYYY-MM') k,
  COUNT(*) rows_all, COUNT(DISTINCT npi) npi_all,
  COUNT_IF(sd = 1) deact, COUNT_IF(sd = 1 AND onpi IS NOT NULL) on_o,
  COUNT_IF(sd = 1 AND onpi IS NOT NULL AND pb = 'N') on_o_pbn,
  COUNT_IF(sd = 1 AND onpi IS NOT NULL AND pmd = 'Y') on_o_pmdy,
  COUNT_IF(sd = 1 AND onpi IS NOT NULL AND (hha = 'Y' OR hos = 'Y')) on_o_hha_or_hos_y,
  COUNT_IF(sd = 1 AND fnpi IS NOT NULL) on_f,
  COUNT_IF(sd = 1 AND bnpi IS NOT NULL) billed24,
  COUNT_IF(sd = 1 AND bnpi IS NOT NULL AND onpi IS NOT NULL) billed24_on_o,
  COUNT_IF(sd = 1 AND bnpi IS NOT NULL AND fnpi IS NOT NULL) billed24_on_f,
  COUNT_IF(sd = 0) reactivated, COUNT_IF(sd = 0 AND onpi IS NOT NULL) react_on_o,
  COUNT_IF(sd = 1 AND NULLIF(TRIM(et), '') IS NOT NULL) et_filled,
  COUNT_IF(sd = 1 AND NULLIF(TRIM(rc), '') IS NOT NULL) rc_filled,
  COUNT_IF(sd = 1 AND NULLIF(TRIM(rn), '') IS NOT NULL) rn_filled
FROM j GROUP BY 1, 2
UNION ALL
SELECT 'week', TO_CHAR(DATE_TRUNC('week', dd), 'YYYY-MM-DD'),
  COUNT(*), COUNT(DISTINCT npi), COUNT_IF(sd = 1), COUNT_IF(sd = 1 AND onpi IS NOT NULL),
  COUNT_IF(sd = 1 AND onpi IS NOT NULL AND pb = 'N'), NULL, NULL,
  COUNT_IF(sd = 1 AND fnpi IS NOT NULL), COUNT_IF(sd = 1 AND bnpi IS NOT NULL),
  COUNT_IF(sd = 1 AND bnpi IS NOT NULL AND onpi IS NOT NULL), NULL, NULL, NULL, NULL, NULL, NULL
FROM j WHERE dd >= '2025-06-01' AND dd < '2025-11-01' GROUP BY 1, 2
ORDER BY 1, 2
"""

Q['Q2'] = """
WITH l AS (
  SELECT npi, MIN(exclusion_date) ed, MAX(IFF(has_waiver, 1, 0)) w, MAX(IFF(was_reinstated, 1, 0)) r
  FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE
  WHERE npi_is_real AND NOT COALESCE(is_entity_not_individual, FALSE) AND exclusion_date >= '2024-07-01'
  GROUP BY npi
),
n AS (SELECT npi, npi_deactivation_date dd FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES
      WHERE npi_deactivation_date IS NOT NULL AND (npi_reactivation_date IS NULL OR npi_reactivation_date < npi_deactivation_date)),
""" + CTE + """
SELECT TO_CHAR(DATE_TRUNC('quarter', l.ed), 'YYYY-MM') q, COUNT(*) excl, SUM(w) waiver, SUM(r) reinst,
  COUNT(b.npi) billed24, COUNT(o.npi) on_o, COUNT_IF(o.pb = 'N') on_o_pbn,
  COUNT_IF(b.npi IS NOT NULL AND o.npi IS NOT NULL) billed24_on_o,
  COUNT(f.npi) on_f, COUNT_IF(b.npi IS NOT NULL AND f.npi IS NOT NULL) billed24_on_f,
  COUNT(n.npi) nppes_deact, COUNT_IF(n.npi IS NOT NULL AND o.npi IS NOT NULL) deact_on_o
FROM l LEFT JOIN o ON o.npi = l.npi LEFT JOIN f ON f.npi = l.npi LEFT JOIN b ON b.npi = l.npi LEFT JOIN n ON n.npi = l.npi
GROUP BY 1 ORDER BY 1
"""

Q['Q3'] = """
WITH n AS (SELECT DISTINCT npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES),
""" + CTE + """
SELECT COUNT(*) o_npis, COUNT_IF(n.npi IS NULL) o_not_in_nppes,
  COUNT_IF(n.npi IS NULL AND o.pb = 'N') o_not_in_nppes_pbn,
  (SELECT COUNT(*) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES) nppes_rows,
  (SELECT COUNT(DISTINCT npi) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES) nppes_npis,
  (SELECT MAX(provider_enumeration_date) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES) nppes_max_enum,
  (SELECT MAX(npi_deactivation_date) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES) nppes_max_deact,
  (SELECT MAX(last_update_date) FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES) nppes_max_upd,
  (SELECT COUNT(DISTINCT _source_run_id) FROM LIBRARY_RAW.LANDING.FED_CMS_ORDER_AND_REFERRING) o_runs,
  (SELECT MIN(_ingested_at) || ' / ' || MAX(_ingested_at) FROM LIBRARY_RAW.LANDING.FED_CMS_ORDER_AND_REFERRING) o_ingested
FROM o LEFT JOIN n ON n.npi = o.npi
"""

def conv(v):
    if isinstance(v, (datetime.date, datetime.datetime)): return v.isoformat()
    if isinstance(v, decimal.Decimal): return float(v)
    return v

todo = sys.argv[1:]
for k in todo:
    s = re.sub(r'--[^\n]*', '', Q[k]).strip()
    assert s.split(None, 1)[0].upper() in ('SELECT', 'WITH') and ';' not in s, k
c = db.connect()
cur = c.cursor()
cur.execute('ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300')
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for k in todo:
    print('=====', k)
    try:
        cur.execute(Q[k])
        cols = [d[0] for d in cur.description]
        rows = [[conv(v) for v in r] for r in cur.fetchall()]
        (HERE / f'out_{k}.json').write_text(json.dumps({'q': k, 'sql': Q[k], 'cols': cols, 'rows': rows}, indent=1))
        print('\t'.join(cols))
        for r in rows: print('\t'.join(str(x) for x in r))
    except Exception as e:
        print('ERROR', k, e)
c.close()
