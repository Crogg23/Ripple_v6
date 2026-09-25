from wq import run
import json
T="LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_OUTPATIENT_HOSPITALS_BY_PROVIDER_AND_SERVICE"
q1=f"""
WITH b AS (
  SELECT RNDRNG_PRVDR_CCN ccn, APC_CD apc, TRY_TO_DOUBLE(CAPC_SRVCS) s, TRY_TO_DOUBLE(OUTLIER_SRVCS) o,
         AVG_MDCR_OUTLIER_AMT oa, AVG_MDCR_PYMT_AMT pa
  FROM {T}),
a AS (SELECT apc, SUM(o*oa)/SUM(s) rate FROM b WHERE s IS NOT NULL AND o IS NOT NULL GROUP BY apc),
h AS (
  SELECT b.ccn, SUM(IFF(o IS NOT NULL, s, 0)) srv, SUM(IFF(o IS NOT NULL, o*oa, 0)) obs,
         SUM(IFF(o IS NOT NULL, s*a.rate, 0)) exp, COUNT_IF(s IS NOT NULL AND o IS NULL) hidden_rows,
         SUM(IFF(o IS NOT NULL, o, 0)) osrv
  FROM b JOIN a ON a.apc=b.apc GROUP BY b.ccn),
r AS (SELECT ccn, obs, ROW_NUMBER() OVER (ORDER BY obs DESC) rk FROM h)
SELECT
  (SELECT COUNT(*) FROM b) n_rows,
  (SELECT COUNT(DISTINCT ccn||'|'||apc) FROM b) n_pairs,
  (SELECT COUNT_IF(s IS NULL) FROM b) stub_rows,
  (SELECT COUNT_IF(s IS NOT NULL AND o IS NULL) FROM b) hidden_outlier_rows,
  (SELECT COUNT_IF(o BETWEEN 1 AND 10) FROM b) shown_1_to_10,
  (SELECT COUNT_IF(o = 0) FROM b) shown_zero,
  (SELECT SUM(o*oa) FROM b WHERE o IS NOT NULL) shown_outlier_usd,
  (SELECT SUM(s*pa) FROM b WHERE s IS NOT NULL) paid_usd,
  (SELECT SUM(obs) FROM r WHERE rk<=50) top50_usd,
  (SELECT COUNT(*) FROM h WHERE srv>=1000) big,
  (SELECT COUNT(*) FROM h WHERE srv>=1000 AND obs=0) big_zero,
  (SELECT COUNT(*) FROM h WHERE srv>=1000 AND obs=0 AND hidden_rows>0) big_zero_with_hidden,
  (SELECT SUM(obs) FROM h WHERE ccn IN ('390004','390096','390256','390336','390339')) psh_obs,
  (SELECT SUM(exp) FROM h WHERE ccn IN ('390004','390096','390256','390336','390339')) psh_exp,
  (SELECT SUM(osrv)||' of '||SUM(srv) FROM h WHERE ccn IN ('390004','390096','390256','390336','390339')) psh_cases,
  (SELECT osrv||' of '||srv||' oe '||ROUND(obs/exp,1) FROM h WHERE ccn='390339') lancaster,
  (SELECT osrv||' of '||srv||' oe '||ROUND(obs/exp,1) FROM h WHERE ccn='390256') hershey
"""
print(json.dumps(run('W1_mart_rederive',q1),indent=1))
q2="""SELECT TABLE_SCHEMA, TABLE_NAME, LISTAGG(COLUMN_NAME, ',') WITHIN GROUP (ORDER BY ORDINAL_POSITION) cols
FROM LIBRARY_RAW.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME ILIKE '%OUTPATIENT%' OR TABLE_NAME ILIKE '%OPPS%' GROUP BY 1,2"""
for x in run('W2_landing_outpatient_tables',q2): print(x)
