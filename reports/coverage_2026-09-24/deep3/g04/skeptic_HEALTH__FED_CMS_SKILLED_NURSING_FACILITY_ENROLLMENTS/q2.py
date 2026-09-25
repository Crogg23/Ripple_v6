import sys
sys.argv = [sys.argv[0]]
src = open(r'C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep3/g04/skeptic_HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS/q.py').read()
defs = src.split('def conv(v):')[0]
exec(defs)
Q['K2b'] = f"""
WITH s AS (SELECT ccn, enrollment_id eid, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name),'') aff FROM {SNF}),
n AS (SELECT cms_certification_number_ccn ccn, state, overall_rating r FROM {NH} WHERE ownership_type ILIKE 'for profit%'),
st AS (SELECT state, AVG(r) m FROM n GROUP BY state),
o AS (SELECT enrollment_id oid, MAX(IFF(created_for_acquisition_owner = 'Y', 1, 0)) cfa FROM LIBRARY_RAW.LANDING.FED_CMS_SNF_OWNERSHIP GROUP BY 1),
j AS (SELECT s.ccn, s.aff, n.r, n.r - st.m gap, COALESCE(o.cfa, 0) cfa FROM s JOIN n ON n.ccn = s.ccn JOIN st ON st.state = n.state LEFT JOIN o ON o.oid = s.eid
      WHERE s.inc >= '2022-01-01' AND n.r IS NOT NULL),
units AS (SELECT aff unit, COUNT(*) h, AVG(gap) ag FROM j WHERE aff IS NOT NULL GROUP BY aff
          UNION ALL SELECT 'IND:' || ccn, 1, gap FROM j WHERE aff IS NULL),
neg4 AS (SELECT aff FROM j WHERE aff IS NOT NULL GROUP BY aff ORDER BY SUM(gap) ASC LIMIT 4),
neg8 AS (SELECT aff FROM j WHERE aff IS NOT NULL GROUP BY aff ORDER BY SUM(gap) ASC LIMIT 8),
l4 AS (SELECT LISTAGG(aff, ' | ') l FROM neg4), l8 AS (SELECT LISTAGG(aff, ' | ') l FROM neg8),
mu AS (SELECT AVG(gap) mu, COUNT(*) nn FROM j),
cl AS (SELECT COALESCE(j.aff, 'IND:' || j.ccn) g, SUM(j.gap - mu.mu) sres FROM j CROSS JOIN mu GROUP BY 1),
d4 AS (SELECT j.* FROM j LEFT JOIN neg4 ON neg4.aff = j.aff WHERE neg4.aff IS NULL),
d8 AS (SELECT j.* FROM j LEFT JOIN neg8 ON neg8.aff = j.aff WHERE neg8.aff IS NULL)
SELECT 'units_all' k, COUNT(*) n, ROUND(MEDIAN(ag),3) med, ROUND(AVG(ag),3) mean, COUNT_IF(ag < 0) below, NULL::FLOAT onestar, NULL::VARCHAR note FROM units
UNION ALL SELECT 'chain_units', COUNT(*), ROUND(MEDIAN(ag),3), ROUND(AVG(ag),3), COUNT_IF(ag < 0), NULL, NULL FROM units WHERE unit NOT LIKE 'IND:%'
UNION ALL SELECT 'chain_units_3plus_homes', COUNT(*), ROUND(MEDIAN(ag),3), ROUND(AVG(ag),3), COUNT_IF(ag < 0), NULL, NULL FROM units WHERE unit NOT LIKE 'IND:%' AND h >= 3
UNION ALL SELECT 'homes_all', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), ROUND(AVG(IFF(r = 1, 1, 0)),3), 'iid_se=' || TO_VARCHAR(ROUND(STDDEV(gap)/SQRT(COUNT(*)),3)) FROM j
UNION ALL SELECT 'homes_cluster_se', ANY_VALUE(mu.nn), NULL, ROUND(ANY_VALUE(mu.mu),3), NULL, NULL, 'chain_cluster_se=' || TO_VARCHAR(ROUND(SQRT(SUM(sres*sres))/ANY_VALUE(mu.nn),3)) || ' clusters=' || COUNT(*) FROM cl CROSS JOIN mu
UNION ALL SELECT 'homes_drop_worst4', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), ROUND(AVG(IFF(r = 1, 1, 0)),3), ANY_VALUE(l4.l) FROM d4 CROSS JOIN l4
UNION ALL SELECT 'homes_drop_worst8', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), ROUND(AVG(IFF(r = 1, 1, 0)),3), ANY_VALUE(l8.l) FROM d8 CROSS JOIN l8
UNION ALL SELECT 'homes_created_for_acq_Y', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), ROUND(AVG(IFF(r = 1, 1, 0)),3), NULL FROM j WHERE cfa = 1
UNION ALL SELECT 'homes_created_for_acq_N', COUNT(*), ROUND(MEDIAN(gap),3), ROUND(AVG(gap),3), COUNT_IF(gap < 0), ROUND(AVG(IFF(r = 1, 1, 0)),3), NULL FROM j WHERE cfa = 0
"""
Q['K3b'] = Q['K3'].replace(' sample,', ' smp,')
Q['K5b'] = Q['K5'].replace("COUNT_IF(state IN ('VA','MD')) va_md\nFROM j JOIN cs", "COUNT_IF(j.state IN ('VA','MD')) va_md\nFROM j JOIN cs")
assert 'smp' in Q['K3b'] and 'j.state IN' in Q['K5b']
tail = 'def conv(v):' + src.split('def conv(v):')[1]
sys.argv = [sys.argv[0]] + sys.argv_keys if False else [sys.argv[0], 'K2b', 'K3b', 'K5b']
exec(tail)
