import sys, pandas as pd
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db
OUT = r"C:\Code\Ripple_v6\reports\coverage_2026-09-24\deep3\g27\skeptic_FINANCE__INTL_WB_IDS"
T = "LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS"
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
def q(sql):
    s = sql.strip(); assert s.upper().startswith(("SELECT", "WITH"))
    cur.execute(s); cols = [d[0] for d in cur.description]
    print('qid', cur.sfqid)
    return pd.DataFrame(cur.fetchall(), columns=cols)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_colwidth', 150)
# K1: integrity, keys, sentinels
k1 = q(f"""
SELECT COUNT(*) n_rows,
 COUNT(DISTINCT TRIM(COUNTRY_CODE)) n_cc,
 COUNT(DISTINCT SERIES_CODE) n_series,
 COUNT(DISTINCT TRIM(COUNTRY_CODE)||'|'||SERIES_CODE||'|'||COALESCE(TRIM(COUNTERPART_AREA_CODE),'')) n_keys,
 COUNT(DISTINCT COUNTERPART_AREA_CODE) n_cp,
 SUM(IFF(TRIM(C_2024) <> '' AND TRY_TO_DOUBLE(TRIM(C_2024)) IS NULL,1,0)) bad24,
 SUM(IFF(TRIM(C_2026) <> '' AND TRY_TO_DOUBLE(TRIM(C_2026)) IS NULL,1,0)) bad26,
 SUM(IFF(LOWER(TRIM(C_2024)) IN ('nan','inf','-inf','none','null','..'),1,0)) sent24,
 SUM(IFF(LOWER(TRIM(C_2026)) IN ('nan','inf','-inf','none','null','..'),1,0)) sent26,
 SUM(IFF(C_2024 IS NULL,1,0)) null24, SUM(IFF(TRIM(C_2024)='',1,0)) blank24,
 ARRAY_SLICE(ARRAY_AGG(DISTINCT IFF(TRIM(C_2024)<>'' AND TRY_TO_DOUBLE(TRIM(C_2024)) IS NULL, C_2024, NULL)),0,10) bad24_vals,
 SUM(IFF(TRY_TO_DOUBLE(TRIM(C_2026)) < 0,1,0)) neg26
FROM {T}""")
print(k1.T.to_string())
# K2: duplicate (country, series) keys if any
k2 = q(f"""
SELECT TRIM(COUNTRY_CODE) cc, SERIES_CODE, COUNT(*) n, COUNT(DISTINCT C_2026) d26
FROM {T} GROUP BY 1,2 HAVING COUNT(*) > 1 ORDER BY n DESC LIMIT 20""")
print('dup keys:', len(k2)); print(k2.to_string())
# K3: wide pull of the series behind the claim, all 134 codes, 2019-2032
yrs = ", ".join(f"C_{y}" for y in range(2015, 2033))
k3 = q(f"""
SELECT TRIM(COUNTRY_CODE) cc, COUNTRY_NAME, SERIES_CODE, SERIES_NAME, {yrs}
FROM {T}
WHERE SERIES_CODE LIKE 'DT.TDS.%' OR SERIES_CODE LIKE 'DT.IXA.%' OR SERIES_CODE LIKE 'DT.AXA.%'
   OR SERIES_CODE IN ('BX.GSR.TOTL.CD','DT.DOD.DPPG.CD','DT.DOD.DECT.CD','DT.DOD.DLXF.CD','FI.RES.TOTL.CD','NY.GNP.MKTP.CD',
                      'DT.AMT.DPPG.CD','DT.INT.DPPG.CD','DT.AMT.PBND.CD','DT.AMT.PCBK.CD','DT.INT.PCBK.CD','DT.DOD.PCBK.CD','DT.DOD.PBND.CD',
                      'DT.DIS.PCBK.CD','DT.DIS.DPPG.CD','DT.COM.PCBK.CD','DT.COM.DPPG.CD','DT.DOD.DIMF.CD')""")
k3.to_pickle(OUT + r"\k3.pkl")
print('k3 rows', len(k3), 'codes', k3.CC.nunique(), 'series', k3.SERIES_CODE.nunique())
cur.close(); c.close()
