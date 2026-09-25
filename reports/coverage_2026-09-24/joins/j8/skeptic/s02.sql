-- independent total: 8872 TOTAL_SCHED_B, one report per EIN+period (latest form id), vs every report summed
WITH g AS (SELECT column1 EIN FROM VALUES ('821194581'),('822366231'),('815214552'),('843153271'),('822315009'),('834686848'),('843763411'),('853307234'),('472041040'),('273594732'),('843763242'),
  ('921706849'),('922354897'),('861386683'),('843763606'),('922452599'),('923489519'),('854325630'),('923489713')),
r AS (SELECT r.EIN, r.FORM_ID_NUMBER, PERIOD_BEGIN_DATE pb, PERIOD_END_DATE pe, TRY_TO_DOUBLE(TOTAL_SCHED_B::string) tb,
   ROW_NUMBER() OVER (PARTITION BY r.EIN, PERIOD_BEGIN_DATE, PERIOD_END_DATE ORDER BY r.FORM_ID_NUMBER::number DESC) rn
  FROM LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS r JOIN g ON g.EIN=r.EIN),
lat AS (SELECT * FROM r WHERE rn=1),
ov AS (SELECT a.EIN, COUNT(*) overlaps, SUM(LEAST(a.tb,b.tb)) ov_amt FROM lat a JOIN lat b ON a.EIN=b.EIN AND a.FORM_ID_NUMBER<b.FORM_ID_NUMBER AND a.pb<=b.pe AND b.pb<=a.pe GROUP BY 1)
SELECT r.EIN, COUNT(*) reports, COUNT_IF(rn=1) periods, ROUND(SUM(tb)/1e6,2) all_reports_m, ROUND(SUM(IFF(rn=1,tb,0))/1e6,2) latest_per_period_m,
  MIN(pb) first_pb, MAX(pe) last_pe, ANY_VALUE(ov.overlaps) overlapping_pairs, ROUND(ANY_VALUE(ov.ov_amt)/1e6,2) overlap_m
FROM r LEFT JOIN ov ON ov.EIN=r.EIN GROUP BY r.EIN
UNION ALL
SELECT 'TOTAL', COUNT(*), COUNT_IF(rn=1), ROUND(SUM(tb)/1e6,2), ROUND(SUM(IFF(rn=1,tb,0))/1e6,2), MIN(pb), MAX(pe), NULL, NULL FROM r
ORDER BY 5 DESC
