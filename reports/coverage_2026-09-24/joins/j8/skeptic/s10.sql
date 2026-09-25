-- peer group with a STRICT fundraising classifier (explicit words only: fundrais/telefund/caging/solicit/donor acqu/list rental/mail house); builder's loose one alongside
WITH g AS (SELECT column1 EIN FROM VALUES ('821194581'),('822366231'),('815214552'),('843153271'),('822315009'),('834686848'),('843763411'),('853307234'),('472041040'),('273594732'),('843763242'),
  ('921706849'),('922354897'),('861386683'),('843763606'),('922452599'),('923489519'),('854325630'),('923489713')),
f AS (SELECT EIN, UPPER(TRIM(REGEXP_REPLACE(RECIPIENT_NAME,'[^A-Za-z0-9& ]',''))) r, EXPENDITURE_DATE d, EXPENDITURE_AMOUNT a, FORM_ID_NUMBER, COUNT(*) n,
    MAX(IFF(REGEXP_LIKE(EXPENDITURE_PURPOSE, '.*(fundrais|telemarket|telefund|direct mail|solicit|caging|donor acqu|mail house|list rental|phone).*', 'i'),1,0)) fr,
    MAX(IFF(REGEXP_LIKE(EXPENDITURE_PURPOSE, '.*(fundrais|fund rais|telefund|caging|solicit|donor acqu|mail house|list rental).*', 'i'),1,0)) frs
   FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES WHERE EXPENDITURE_DATE >= '2014-01-01' GROUP BY 1,2,3,4,5),
k AS (SELECT EIN, r, d, a, MAX(n) n, MAX(fr) fr, MAX(frs) frs FROM f GROUP BY 1,2,3,4),
e AS (SELECT k.EIN, IFF(MAX(g.EIN) IS NULL,'N','Y') in19, SUM(n*a) tot, SUM(IFF(fr=1,n*a,0))/SUM(n*a) pfr, SUM(IFF(frs=1,n*a,0))/SUM(n*a) pfrs FROM k LEFT JOIN g ON g.EIN=k.EIN GROUP BY 1 HAVING SUM(n*a) >= 1e6)
SELECT in19, COUNT(*) groups, ROUND(100*MEDIAN(pfr),1) med_loose, ROUND(100*MEDIAN(pfrs),1) med_strict, COUNT_IF(pfr>0.5) over50_loose, COUNT_IF(pfrs>0.5) over50_strict,
  ROUND(100*MIN(pfrs),1) min_strict, ROUND(100*MAX(pfrs),1) max_strict FROM e GROUP BY in19
UNION ALL SELECT 'all', COUNT(*), ROUND(100*MEDIAN(pfr),1), ROUND(100*MEDIAN(pfrs),1), COUNT_IF(pfr>0.5), COUNT_IF(pfrs>0.5), ROUND(100*MIN(pfrs),1), ROUND(100*MAX(pfrs),1) FROM e
