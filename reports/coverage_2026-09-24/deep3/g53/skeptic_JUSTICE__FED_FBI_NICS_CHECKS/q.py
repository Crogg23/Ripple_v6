import sys, csv, pickle
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[4]))
from connect import db

M = "LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FBI_NICS_CHECKS"
PRIV = "COALESCE(PRIVATE_SALE_HANDGUN,0)+COALESCE(PRIVATE_SALE_LONG_GUN,0)+COALESCE(PRIVATE_SALE_OTHER,0)"
DEAL = "COALESCE(HANDGUN,0)+COALESCE(LONG_GUN,0)+COALESCE(OTHER,0)+COALESCE(MULTIPLE,0)"
ALLC = ["PERMIT","PERMIT_RECHECK","HANDGUN","LONG_GUN","OTHER","MULTIPLE","ADMIN","PREPAWN_HANDGUN","PREPAWN_LONG_GUN","PREPAWN_OTHER","REDEMPTION_HANDGUN","REDEMPTION_LONG_GUN","REDEMPTION_OTHER","RETURNED_HANDGUN","RETURNED_LONG_GUN","RETURNED_OTHER","RENTALS_HANDGUN","RENTALS_LONG_GUN","PRIVATE_SALE_HANDGUN","PRIVATE_SALE_LONG_GUN","PRIVATE_SALE_OTHER","RETURN_TO_SELLER_HANDGUN","RETURN_TO_SELLER_LONG_GUN","RETURN_TO_SELLER_OTHER"]
SUMALL = "+".join(f"COALESCE({c},0)" for c in ALLC)
NEG = " OR ".join(f"{c}<0" for c in ALLC+["TOTALS"])

Q = {
"K1_integrity": f"""SELECT COUNT(*) n, COUNT(DISTINCT MONTH||'|'||STATE) n_keys, COUNT(DISTINCT STATE) n_states,
 COUNT(DISTINCT MONTH) n_months, MIN(MONTH), MAX(MONTH),
 COUNT_IF(TOTALS <> {SUMALL}) totals_mismatch, COUNT_IF({NEG}) neg_rows,
 COUNT_IF(PRIVATE_SALE_HANDGUN IS NULL) priv_hg_null, COUNT_IF(PRIVATE_SALE_HANDGUN IS NULL AND MONTH>='2013-08') priv_null_after_start,
 MAX(PRIVATE_SALE_HANDGUN), MAX(PRIVATE_SALE_LONG_GUN), MAX(TOTALS), COUNT(DISTINCT STATE) FROM {M}""",
"K2_vt2022": f"""SELECT STATE, COUNT(*) months, COUNT(DISTINCT MONTH) dmonths, SUM(PRIVATE_SALE_HANDGUN) p_hg, SUM(PRIVATE_SALE_LONG_GUN) p_lg,
 SUM(PRIVATE_SALE_OTHER) p_oth, SUM({PRIV}) priv, SUM({DEAL}) dealer,
 SUM(COALESCE(RETURN_TO_SELLER_HANDGUN,0)+COALESCE(RETURN_TO_SELLER_LONG_GUN,0)+COALESCE(RETURN_TO_SELLER_OTHER,0)) rts,
 ROUND(100*SUM({PRIV})/NULLIF(SUM({DEAL}),0),3) per100, MIN({PRIV}) min_m, MAX({PRIV}) max_m, COUNT_IF({PRIV}=0) zero_months
 FROM {M} WHERE MONTH LIKE '2022-%' AND STATE='Vermont' GROUP BY 1""",
"K3_state2022": f"""SELECT STATE, COUNT(*) months, SUM({PRIV}) priv, SUM({DEAL}) dealer, SUM(TOTALS) totals,
 COUNT_IF({PRIV}=0) zero_months FROM {M} WHERE MONTH LIKE '2022-%' GROUP BY 1 ORDER BY 1""",
"K4_monthly": f"""SELECT STATE, MONTH, {PRIV} priv, {DEAL} dealer, COALESCE(PERMIT,0) permit, TOTALS,
 PRIVATE_SALE_HANDGUN, PRIVATE_SALE_LONG_GUN, PRIVATE_SALE_OTHER FROM {M}
 WHERE STATE IN ('Vermont','Maine','New Hampshire','New York','New Mexico','Delaware','Washington','Nevada','Connecticut','Rhode Island','New Jersey','Maryland','Massachusetts')
 ORDER BY 1,2""",
"K5_raw_vt2022": """SELECT COUNT(*) n, COUNT(DISTINCT MONTH) dm, MIN(MONTH), MAX(MONTH), COUNT(DISTINCT INGESTED_AT) loads,
 SUM(TRY_TO_NUMBER(TO_VARCHAR(PRIVATE_SALE_HANDGUN))) p_hg, SUM(TRY_TO_NUMBER(TO_VARCHAR(PRIVATE_SALE_LONG_GUN))) p_lg,
 SUM(TRY_TO_NUMBER(TO_VARCHAR(PRIVATE_SALE_OTHER))) p_oth, LISTAGG(DISTINCT TO_VARCHAR(PRIVATE_SALE_HANDGUN), ',') hg_vals
 FROM LIBRARY_RAW.LANDING.FED_FBI_NICS_CHECKS WHERE STATE='Vermont' AND TO_VARCHAR(MONTH) LIKE '2022-%'""",
"K6_raw_whole": """SELECT COUNT(*) n, COUNT(DISTINCT TO_VARCHAR(MONTH)||'|'||TO_VARCHAR(STATE)) keys, MAX(TO_VARCHAR(MONTH)) maxm, COUNT(DISTINCT INGESTED_AT) loads
 FROM LIBRARY_RAW.LANDING.FED_FBI_NICS_CHECKS""",
}

c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
out = {}
for k, sql in Q.items():
    first = sql.lstrip().split(None,1)[0].upper()
    assert first in ("SELECT","WITH"), k
    try:
        cur.execute(sql)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        out[k] = (cols, rows)
        print("==", k, len(rows), "rows")
        print(" | ".join(cols))
        for r in rows[:60]:
            print(" | ".join("" if v is None else str(v) for v in r))
    except Exception as e:
        print("==", k, "ERROR", e)
        out[k] = ("ERR", str(e))
cur.close(); c.close()
pickle.dump(out, open(HERE / "out.pkl", "wb"))
