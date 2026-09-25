import sys, datetime, decimal
sys.path.insert(0, r'C:\Code\Ripple_v6')
from connect import db
SNF = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS"
NH = "LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME"
GRP = """CASE WHEN s.inc IS NULL THEN 'z_null' WHEN s.inc < '1900-01-01' THEN 'y_sent' WHEN s.inc >= '2022-01-01' THEN 'a_2022+' WHEN s.inc >= '2018-01-01' THEN 'b_2018-21' ELSE 'c_pre2018' END"""
Q = {}
Q['K1'] = f"""
WITH s AS (SELECT ccn, incorporation_date inc FROM {SNF}),
nall AS (SELECT cms_certification_number_ccn ccn, state, overall_rating r, ownership_type FROM {NH}),
n AS (SELECT * FROM nall WHERE ownership_type ILIKE 'for profit%'),
st AS (SELECT state, AVG(r) m, MEDIAN(r) md FROM n GROUP BY state),
j AS (SELECT s.ccn, n.r, st.m, st.md, {GRP} grp FROM s JOIN n ON n.ccn = s.ccn JOIN st ON st.state = n.state)
SELECT COALESCE(grp,'ALL') grp, COUNT(*) homes, COUNT(r) rated, COUNT(DISTINCT ccn) dccn,
 ROUND(AVG(r - m),3) mean_gap, ROUND(STDDEV(r - m)/SQRT(COUNT(r)),3) se, ROUND(MEDIAN(r - m),3) med_gap, MEDIAN(r) med_star, ROUND(AVG(r),3) mean_star,
 COUNT_IF(r=1) s1, COUNT_IF(r=2) s2, COUNT_IF(r=3) s3, COUNT_IF(r=4) s4, COUNT_IF(r=5) s5,
 ROUND(COUNT_IF(r=1)/COUNT(*),3) one_star_all, ROUND(COUNT_IF(r=1)/NULLIF(COUNT(r),0),3) one_star_rated,
 ROUND(COUNT_IF(r<=2)/NULLIF(COUNT(r),0),3) le2_rated,
 ROUND(MEDIAN(r - md),3) med_gap_vs_state_median, COUNT_IF(r < m) below_state_mean,
 (SELECT COUNT(*) FROM nall) nh_rows, (SELECT COUNT(DISTINCT ccn) FROM nall) nh_ccns,
 (SELECT COUNT(*) FROM {SNF}) snf_rows, (SELECT COUNT(DISTINCT ccn) FROM {SNF}) snf_ccns
FROM j GROUP BY ROLLUP(grp) ORDER BY grp
"""
Q['K2'] = f"""
WITH s AS (SELECT ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name),'') aff FROM {SNF}),
n AS (SELECT cms_certification_number_ccn ccn, state, overall_rating r FROM {NH} WHERE ownership_type ILIKE 'for profit%'),
st AS (SELECT state, AVG(r) m FROM n GROUP BY state),
j AS (SELECT s.ccn, s.aff, n.r - st.m gap FROM s JOIN n ON n.ccn = s.ccn JOIN st ON st.state = n.state WHERE s.inc >= '2022-01-01' AND n.r IS NOT NULL),
units AS (SELECT aff unit, COUNT(*) h, AVG(gap) ag FROM j WHERE aff IS NOT NULL GROUP BY aff
          UNION ALL SELECT 'IND:' || ccn, 1, gap FROM j WHERE aff IS NULL),
neg4 AS (SELECT aff FROM j WHERE aff IS NOT NULL GROUP BY aff ORDER BY SUM(gap) ASC LIMIT 4),
neg8 AS (SELECT aff FROM j WHERE aff IS NOT NULL GROUP BY aff ORDER BY SUM(gap) ASC LIMIT 8),
mu AS (SELECT AVG(gap) mu, COUNT(*) nn FROM j),
cl AS (SELECT COALESCE(aff, 'IND:' || ccn) g, SUM(gap - (SELECT mu FROM mu)) sres FROM j GROUP BY 1)
SELECT 'units_all' k, COUNT(*) n, ROUND(MEDIAN(ag),3) med, ROUND(AVG(ag),3) mean, COUNT_IF(ag < 0) below, NULL::VARCHAR note FROM units
UNION ALL SELECT 'chain_units', COUNT(*), ROUND(MEDIAN(ag),3), ROUND(AVG(ag),3), COUNT_IF(ag < 0), NULL FROM units WHERE unit NOT LIKE 'IND:%'
UNION ALL SELECT 'chain_units_3plus_homes', COUNT(*), ROUND(MEDIAN(ag),3), ROUND(AVG(ag),3), COUNT_IF(ag < 0), NULL FROM units WHERE unit NOT LIKE 'IND:%' AND h >= 3
UNION ALL SELECT 'homes_all', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), 'iid_se=' || TO_VARCHAR(ROUND(STDDEV(gap)/SQRT(COUNT(*)),3)) FROM j
UNION ALL SELECT 'homes_cluster_se', (SELECT nn FROM mu), NULL, ROUND((SELECT mu FROM mu),3), NULL, 'chain_cluster_se=' || TO_VARCHAR(ROUND(SQRT(SUM(sres*sres))/(SELECT nn FROM mu),3)) || ' clusters=' || COUNT(*) FROM cl
UNION ALL SELECT 'homes_drop_worst4', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), (SELECT LISTAGG(aff, ' | ') FROM neg4) FROM j WHERE aff IS NULL OR aff NOT IN (SELECT aff FROM neg4)
UNION ALL SELECT 'homes_drop_worst8', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), (SELECT LISTAGG(aff, ' | ') FROM neg8) FROM j WHERE aff IS NULL OR aff NOT IN (SELECT aff FROM neg8)
"""
Q['K3'] = f"""
WITH s AS (SELECT ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name),'') aff, organization_name op,
                  TRY_TO_DATE(SUBSTR(enrollment_id, 2, 8), 'YYYYMMDD') enr FROM {SNF}),
n AS (SELECT cms_certification_number_ccn ccn, state, overall_rating r FROM {NH} WHERE ownership_type ILIKE 'for profit%'),
st AS (SELECT state, AVG(r) m FROM n GROUP BY state),
j AS (SELECT s.*, n.state, n.r - st.m gap FROM s JOIN n ON n.ccn = s.ccn JOIN st ON st.state = n.state WHERE s.inc >= '2022-01-01')
SELECT 'align' k, NULL::VARCHAR d, COUNT(*) homes, COUNT_IF(enr >= inc) enr_on_or_after_inc, COUNT_IF(enr < inc) enr_before_inc,
       COUNT_IF(enr < DATEADD(year, -1, inc)) enr_1y_plus_before_inc, COUNT_IF(DATEDIFF(day, inc, enr) BETWEEN 0 AND 365) enr_within_1y_after,
       MEDIAN(DATEDIFF(day, inc, enr)) med_days_inc_to_enr, NULL::VARCHAR sample, NULL::FLOAT avg_gap
FROM j
UNION ALL
SELECT * FROM (
 SELECT 'pileup', TO_VARCHAR(inc), COUNT(*), COUNT(DISTINCT aff), COUNT(DISTINCT state), COUNT_IF(enr < inc), NULL, NULL,
        LEFT(LISTAGG(DISTINCT COALESCE(aff,'-'), ' | '), 120) || ' // ' || LEFT(ANY_VALUE(op), 50), ROUND(AVG(gap),2)
 FROM j GROUP BY inc HAVING COUNT(*) >= 4 ORDER BY COUNT(*) DESC LIMIT 14)
UNION ALL
SELECT 'pileup_totals', NULL, SUM(h), COUNT(*), NULL, NULL, NULL, NULL, 'homes sharing an inc date with 4+ others', ROUND(SUM(sg)/SUM(h),3)
FROM (SELECT inc, COUNT(*) h, SUM(gap) sg FROM j GROUP BY inc HAVING COUNT(*) >= 4)
"""
CYC = f"""
s AS (SELECT ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name),'') aff FROM {SNF}),
n AS (SELECT cms_certification_number_ccn ccn, state,
         rating_cycle_1_standard_survey_health_date c1d, rating_cycle_2_standard_health_survey_date c2d,
         rating_cycle_1_number_of_standard_health_deficiencies c1n, rating_cycle_2_number_of_standard_health_deficiencies c2n
  FROM {NH} WHERE ownership_type ILIKE 'for profit%'
    AND rating_cycle_1_standard_survey_health_date IS NOT NULL AND rating_cycle_2_standard_health_survey_date IS NOT NULL
    AND rating_cycle_1_number_of_standard_health_deficiencies IS NOT NULL AND rating_cycle_2_number_of_standard_health_deficiencies IS NOT NULL),
j AS (SELECT n.*, s.inc, s.aff, CASE WHEN s.inc > n.c2d AND s.inc < n.c1d THEN 'T'
              WHEN s.inc >= '1900-01-01' AND s.inc < '2018-01-01' THEN 'C' END grp FROM n JOIN s ON s.ccn = n.ccn)
"""
Q['K4'] = f"""
WITH {CYC},
t AS (SELECT * FROM j WHERE grp = 'T'), c AS (SELECT * FROM j WHERE grp = 'C'),
m1 AS (SELECT t.ccn, ANY_VALUE(t.state) state, ANY_VALUE(t.inc) inc, ANY_VALUE(t.c2n) c2n, ANY_VALUE(t.c1n) c1n,
              ANY_VALUE(DATEDIFF(day, t.c2d, t.c1d)) tgap, AVG(c.c2n) pc2, AVG(c.c1n) pc1, COUNT(*) np, AVG(DATEDIFF(day, c.c2d, c.c1d)) pgap
       FROM t JOIN c ON c.state = t.state AND ABS(DATEDIFF(day, c.c2d, t.c2d)) <= 365 AND ABS(DATEDIFF(day, c.c1d, t.c1d)) <= 365 GROUP BY t.ccn),
m2 AS (SELECT t.ccn, ANY_VALUE(t.state) state, ANY_VALUE(t.inc) inc, ANY_VALUE(t.c2n) c2n, ANY_VALUE(t.c1n) c1n,
              ANY_VALUE(DATEDIFF(day, t.c2d, t.c1d)) tgap, AVG(c.c2n) pc2, AVG(c.c1n) pc1, COUNT(*) np, AVG(DATEDIFF(day, c.c2d, c.c1d)) pgap
       FROM t JOIN c ON c.state = t.state AND ABS(DATEDIFF(day, c.c2d, c.c1d) - DATEDIFF(day, t.c2d, t.c1d)) <= 120 GROUP BY t.ccn),
v AS (
  SELECT 'A_state+both_dates_pm365' variant, * FROM m1 WHERE np >= 3
  UNION ALL SELECT 'A2_inc2022plus', * FROM m1 WHERE np >= 3 AND inc >= '2022-01-01'
  UNION ALL SELECT 'A3_no_VA_MD', * FROM m1 WHERE np >= 3 AND state NOT IN ('VA','MD')
  UNION ALL SELECT 'B_state+interval_pm120', * FROM m2 WHERE np >= 3
  UNION ALL SELECT 'B2_inc2022plus', * FROM m2 WHERE np >= 3 AND inc >= '2022-01-01'
  UNION ALL SELECT 'B3_no_VA_MD', * FROM m2 WHERE np >= 3 AND state NOT IN ('VA','MD')
  UNION ALL SELECT 'T_all_raw', t.ccn, t.state, t.inc, t.c2n, t.c1n, DATEDIFF(day, t.c2d, t.c1d), NULL, NULL, NULL, NULL FROM t
)
SELECT variant, COUNT(*) homes, COUNT_IF(inc >= '2022-01-01') inc2022p, COUNT_IF(inc < '2022-01-01') inc_pre2022, MIN(inc) inc_min,
  ROUND(AVG(c2n - pc2),2) gap_before, ROUND(AVG(c1n - pc1),2) gap_after,
  ROUND(AVG((c1n - c2n) - (pc1 - pc2)),2) did, ROUND(MEDIAN((c1n - c2n) - (pc1 - pc2)),2) did_med,
  ROUND(STDDEV((c1n - c2n) - (pc1 - pc2))/SQRT(COUNT(*)),2) se, COUNT_IF((c1n - c2n) > (pc1 - pc2)) worse,
  ROUND(AVG(tgap)) t_days, ROUND(AVG(pgap)) p_days, ROUND(AVG(np),1) avg_peers,
  COUNT_IF(state IN ('VA','MD')) va_md
FROM v GROUP BY variant ORDER BY variant
"""
Q['K5'] = f"""
WITH {CYC},
cs AS (SELECT state, AVG(c1n - c2n) sm FROM j WHERE grp = 'C' GROUP BY state)
SELECT grp, CASE WHEN DATEDIFF(day, c2d, c1d) < 450 THEN 'a_<450d' WHEN DATEDIFF(day, c2d, c1d) < 700 THEN 'b_450-699d'
                 WHEN DATEDIFF(day, c2d, c1d) < 1000 THEN 'c_700-999d' ELSE 'd_1000d+' END bucket,
  COUNT(*) homes, ROUND(AVG(c2n),2) mean_c2, ROUND(AVG(c1n),2) mean_c1, ROUND(AVG((c1n - c2n) - sm),2) chg_vs_state_peers,
  ROUND(STDDEV((c1n - c2n) - sm)/SQRT(COUNT(*)),2) se, COUNT_IF(state IN ('VA','MD')) va_md
FROM j JOIN cs ON cs.state = j.state WHERE grp IN ('C','T') GROUP BY 1, 2
UNION ALL
SELECT * FROM (SELECT 'T_by_state', state, COUNT(*), ROUND(AVG(c2n),2), ROUND(AVG(c1n),2), NULL, NULL, NULL FROM j WHERE grp = 'T' GROUP BY state ORDER BY COUNT(*) DESC LIMIT 8)
ORDER BY 1, 2
"""
DP = "COALESCE(TRY_TO_DATE(association_date_owner, 'YYYY-MM-DD'), TRY_TO_DATE(association_date_owner, 'MM/DD/YYYY'), TRY_TO_DATE(association_date_owner, 'YYYY/MM/DD'), TRY_TO_DATE(association_date_owner, 'YYYYMMDD'))"
Q['K6'] = f"""
WITH s AS (SELECT enrollment_id eid, ccn, incorporation_date inc FROM {SNF}),
n AS (SELECT cms_certification_number_ccn ccn FROM {NH} WHERE ownership_type ILIKE 'for profit%'),
o AS (SELECT enrollment_id oid, COUNT(*) owners, MAX(IFF(created_for_acquisition_owner = 'Y', 1, 0)) cfa,
             MIN({DP}) amin, MAX({DP}) amax,
             COUNT_IF({DP} IS NULL AND NULLIF(TRIM(association_date_owner), '') IS NOT NULL) unparsed,
             COUNT_IF(NULLIF(TRIM(association_date_owner), '') IS NULL) blank_dates
      FROM LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP GROUP BY enrollment_id),
j AS (SELECT s.*, o.*, {GRP} grp FROM s JOIN n ON n.ccn = s.ccn LEFT JOIN o ON o.oid = s.eid)
SELECT grp, COUNT(*) homes, COUNT(oid) in_owner_file, SUM(cfa) any_created_for_acq, ROUND(AVG(cfa),3) share_cfa,
  COUNT_IF(amin < DATEADD(year, -1, inc)) first_owner_1y_plus_before_inc, COUNT_IF(amin >= DATEADD(day, -365, inc)) first_owner_after,
  MEDIAN(DATEDIFF(day, inc, amin)) med_days_inc_to_first_owner, COUNT_IF(amax >= '2022-01-01') any_owner_2022p,
  SUM(unparsed) unparsed, SUM(blank_dates) blank_dates, SUM(owners) owner_rows,
  (SELECT LISTAGG(DISTINCT created_for_acquisition_owner, ',') FROM LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP) cfa_vals
FROM j GROUP BY grp ORDER BY grp
"""
def conv(v):
    if isinstance(v,(datetime.date,datetime.datetime)): return v.isoformat()
    if isinstance(v,decimal.Decimal): return float(v)
    return v
keys = sys.argv[1:] or ['K1','K2','K3','K4','K5','K6']
for k in keys:
    q = Q[k].strip().upper()
    assert q.startswith('WITH') or q.startswith('SELECT'), k
    assert ';' not in Q[k], k
c = db.connect()
cur = c.cursor()
cur.execute("ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300")
cur.execute("ALTER SESSION SET QUERY_TAG = 'deep3-skeptic-2026-09-24'")
for k in keys:
    print('=====', k, flush=True)
    try:
        cur.execute(Q[k])
        cols = [d[0] for d in cur.description]
        print(' | '.join(cols))
        for r in cur.fetchall(): print(' | '.join(str(conv(x)) for x in r))
    except Exception as e:
        print('ERROR', str(e)[:400])
    sys.stdout.flush()
c.close()
