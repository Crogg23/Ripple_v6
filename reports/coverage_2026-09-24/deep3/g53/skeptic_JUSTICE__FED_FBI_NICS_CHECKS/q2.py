import sys, pickle
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4]))
from connect import db
M = "LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS"
ALLC = ["PERMIT","PERMIT_RECHECK","HANDGUN","LONG_GUN","OTHER","MULTIPLE","ADMIN","PREPAWN_HANDGUN","PREPAWN_LONG_GUN","PREPAWN_OTHER","REDEMPTION_HANDGUN","REDEMPTION_LONG_GUN","REDEMPTION_OTHER","RETURNED_HANDGUN","RETURNED_LONG_GUN","RETURNED_OTHER","RENTALS_HANDGUN","RENTALS_LONG_GUN","PRIVATE_SALE_HANDGUN","PRIVATE_SALE_LONG_GUN","PRIVATE_SALE_OTHER","RETURN_TO_SELLER_HANDGUN","RETURN_TO_SELLER_LONG_GUN","RETURN_TO_SELLER_OTHER"]
N = lambda c: f"COALESCE(TRY_TO_NUMBER(TO_VARCHAR({c})),0)"
SUMALL = "+".join(N(c) for c in ALLC)
BLANK = "+".join(f"IFF(TO_VARCHAR({c})='',1,0)" for c in ALLC)
NEG = " OR ".join(f"TRY_TO_NUMBER(TO_VARCHAR({c}))<0" for c in ALLC+["TOTALS"])
Q = {
"K7_types": """SELECT COLUMN_NAME, DATA_TYPE FROM LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
 WHERE TABLE_SCHEMA='JUSTICE' AND TABLE_NAME='JUSTICE__FED_FBI_NICS_CHECKS' ORDER BY ORDINAL_POSITION""",
"K8_integrity": f"""SELECT COUNT(*) n, COUNT(DISTINCT MONTH||'|'||STATE) keys, COUNT(DISTINCT STATE) states, COUNT(DISTINCT MONTH) months,
 COUNT_IF(TRY_TO_NUMBER(TO_VARCHAR(TOTALS)) <> {SUMALL}) totals_mismatch, COUNT_IF({NEG}) neg_rows,
 SUM({BLANK}) blank_cells, COUNT_IF(TO_VARCHAR(PRIVATE_SALE_HANDGUN)='') priv_blank,
 COUNT_IF(TO_VARCHAR(PRIVATE_SALE_HANDGUN)='' AND MONTH>='2013-08') priv_blank_after_start,
 COUNT_IF(PRIVATE_SALE_HANDGUN IS NULL) priv_null,
 MIN(IFF(TO_VARCHAR(PRIVATE_SALE_HANDGUN)<>'', MONTH, NULL)) priv_first_month
 FROM {M}""",
}
c = db.connect(); cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for k, sql in Q.items():
    try:
        cur.execute(sql); cols=[d[0] for d in cur.description]; rows=cur.fetchall()
        print("==",k); print(" | ".join(cols))
        for r in rows: print(" | ".join("" if v is None else str(v) for v in r))
    except Exception as e: print("==",k,"ERROR",e)
cur.close(); c.close()
