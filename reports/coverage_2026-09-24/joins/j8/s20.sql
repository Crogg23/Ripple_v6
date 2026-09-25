-- peer group: every 527 with $1M+ spending 2014 on (copies dropped). how many sit at 89.5-91.0% fundraising, and where do the rest fall?
WITH f AS (SELECT EIN, UPPER(TRIM(REGEXP_REPLACE(RECIPIENT_NAME,'[^A-Za-z0-9& ]',''))) r, EXPENDITURE_DATE d, EXPENDITURE_AMOUNT a, FORM_ID_NUMBER, COUNT(*) n,
    MAX(IFF(REGEXP_LIKE(EXPENDITURE_PURPOSE, '.*(fundrais|telemarket|telefund|direct mail|solicit|caging|donor acqu|mail house|list rental|phone).*', 'i'),1,0)) fr,
    MAX(IFF(EXPENDITURE_PURPOSE ILIKE '%contribution%' OR EXPENDITURE_PURPOSE ILIKE '%donation%',1,0)) ct
   FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES WHERE EXPENDITURE_DATE >= '2014-01-01' GROUP BY 1,2,3,4,5),
k AS (SELECT EIN, r, d, a, MAX(n) n, MAX(fr) fr, MAX(ct) ct FROM f GROUP BY 1,2,3,4),
e AS (SELECT EIN, SUM(n*a) tot, SUM(IFF(fr=1,n*a,0))/SUM(n*a) pfr, SUM(IFF(ct=1,n*a,0))/SUM(n*a) pct FROM k GROUP BY 1 HAVING SUM(n*a) >= 1e6),
o AS (SELECT EIN, MAX_BY(ORG_NAME, EXPENDITURE_DATE) org FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES GROUP BY 1)
SELECT 'bucket' k, CASE WHEN pfr >= 0.895 AND pfr < 0.91 THEN '89.5-91.0' WHEN pfr >= 0.5 THEN '50+ other' WHEN pfr >= 0.2 THEN '20-50' ELSE 'under 20' END b,
  COUNT(*) groups, ROUND(SUM(tot)/1e6,1) tot_m, ROUND(MEDIAN(pfr)*100,1) med_pfr, ROUND(MEDIAN(pct)*100,1) med_pct_contrib, NULL org
FROM e GROUP BY 1,2
UNION ALL SELECT 'all', 'all', COUNT(*), ROUND(SUM(tot)/1e6,1), ROUND(MEDIAN(pfr)*100,1), ROUND(MEDIAN(pct)*100,1), NULL FROM e
UNION ALL SELECT 'in_band', e.EIN, NULL, ROUND(tot/1e6,2), ROUND(pfr*100,1), ROUND(pct*100,1), o.org FROM e JOIN o USING (EIN) WHERE pfr >= 0.895 AND pfr < 0.91
ORDER BY 1, 4 DESC
