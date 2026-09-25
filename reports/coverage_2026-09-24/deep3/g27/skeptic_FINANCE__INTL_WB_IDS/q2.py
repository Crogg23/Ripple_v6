import sys, pandas as pd, numpy as np
sys.path.insert(0, r"C:\Code\Ripple_v6")
from connect import db
OUT = r"C:\Code\Ripple_v6\reports\coverage_2026-09-24\deep3\g27\skeptic_FINANCE__INTL_WB_IDS"
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
s = """SELECT TRIM(COUNTRY_CODE) cc, SERIES_CODE, SERIES_NAME, C_2019, C_2020, C_2021, C_2022, C_2023, C_2024
FROM LIBRARY_MARTS.FINANCE.FINANCE__INTL_WB_IDS
WHERE SERIES_CODE LIKE 'DT.MAT.%' OR SERIES_CODE LIKE 'DT.INR.%' OR SERIES_CODE LIKE 'DT.GPA.%' OR SERIES_CODE LIKE 'DT.COM.%'"""
assert s.upper().startswith('SELECT')
cur.execute(s); print('qid', cur.sfqid)
df = pd.DataFrame(cur.fetchall(), columns=[d[0] for d in cur.description]); cur.close(); c.close()
df.to_pickle(OUT + r"\k4.pkl"); print(len(df))
