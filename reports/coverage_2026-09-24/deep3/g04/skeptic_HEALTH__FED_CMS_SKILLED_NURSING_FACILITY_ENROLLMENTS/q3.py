import sys
src = open(r'C:/Code/Ripple_v6/reports/coverage_2026-09-24/deep3/g04/skeptic_HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS/q.py').read()
exec(src.split('def conv(v):')[0])
Q['K7'] = f"""
WITH s AS (SELECT ccn, incorporation_date inc, NULLIF(TRIM(affiliation_entity_name),'') aff FROM {SNF}),
n AS (SELECT cms_certification_number_ccn ccn, state, overall_rating r FROM {NH} WHERE ownership_type ILIKE 'for profit%' AND overall_rating IS NOT NULL),
st AS (SELECT state, AVG(r) m, AVG(IFF(r = 1, 1, 0)) p1, AVG(IFF(r <= 2, 1, 0)) p12 FROM n GROUP BY state),
j AS (SELECT s.ccn, COALESCE(s.aff, 'IND:' || s.ccn) g, IFF(n.r = 1, 1, 0) - st.p1 d1, IFF(n.r <= 2, 1, 0) - st.p12 d12, n.r - st.m dr
      FROM s JOIN n ON n.ccn = s.ccn JOIN st ON st.state = n.state WHERE s.inc >= '2022-01-01'),
mu AS (SELECT AVG(d1) m1, AVG(d12) m12, AVG(dr) mr, COUNT(*) nn FROM j),
cl AS (SELECT j.g, SUM(j.d1 - mu.m1) e1, SUM(j.d12 - mu.m12) e12, SUM(j.dr - mu.mr) er FROM j CROSS JOIN mu GROUP BY j.g)
SELECT ANY_VALUE(mu.nn) homes, COUNT(*) clusters,
  ROUND(ANY_VALUE(mu.m1), 4) onestar_gap_vs_state, ROUND(SQRT(SUM(e1*e1))/ANY_VALUE(mu.nn), 4) onestar_cl_se,
  ROUND(ANY_VALUE(mu.m12), 4) le2star_gap_vs_state, ROUND(SQRT(SUM(e12*e12))/ANY_VALUE(mu.nn), 4) le2star_cl_se,
  ROUND(ANY_VALUE(mu.mr), 4) star_gap_vs_state, ROUND(SQRT(SUM(er*er))/ANY_VALUE(mu.nn), 4) star_cl_se
FROM cl CROSS JOIN mu
"""
tail = 'def conv(v):' + src.split('def conv(v):')[1]
sys.argv = [sys.argv[0], 'K7']
exec(tail)
