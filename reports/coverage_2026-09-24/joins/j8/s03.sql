-- the 19: per-group totals, copies across forms dropped (EIN+payee+date+amount, keep the largest single-form count)
WITH g AS (SELECT column1 EIN FROM VALUES ('821194581'),('822366231'),('815214552'),('843153271'),('822315009'),('834686848'),('843763411'),('853307234'),('472041040'),('273594732'),('843763242'),
  ('921706849'),('922354897'),('861386683'),('843763606'),('922452599'),('923489519'),('854325630'),('923489713')),
f AS (SELECT b.EIN, UPPER(TRIM(REGEXP_REPLACE(RECIPIENT_NAME,'[^A-Za-z0-9& ]',''))) r, EXPENDITURE_DATE d, EXPENDITURE_AMOUNT a, FORM_ID_NUMBER, COUNT(*) n,
    MAX(IFF(REGEXP_LIKE(EXPENDITURE_PURPOSE, '.*(fundrais|telemarket|telefund|direct mail|solicit|caging|donor acqu|mail house|list rental|phone).*', 'i'),1,0)) fr,
    MAX(IFF(EXPENDITURE_PURPOSE ILIKE '%contribution%' OR EXPENDITURE_PURPOSE ILIKE '%donation%',1,0)) ct
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES b JOIN g ON g.EIN=b.EIN GROUP BY 1,2,3,4,5),
k AS (SELECT EIN, r, d, a, MAX(n) n, MAX(fr) fr, MAX(ct) ct FROM f GROUP BY 1,2,3,4),
o AS (SELECT b.EIN, MAX_BY(ORG_NAME, EXPENDITURE_DATE) org, COUNT(*) raw_rows, SUM(EXPENDITURE_AMOUNT) raw_amt FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_B_EXPENDITURES b JOIN g ON g.EIN=b.EIN GROUP BY 1)
SELECT k.EIN, o.org, MIN(YEAR(d)) y0, MAX(d) last_d, o.raw_rows, ROUND(o.raw_amt/1e6,2) raw_m, ROUND(SUM(n*a)/1e6,2) dedup_m,
  ROUND(100*SUM(IFF(fr=1,n*a,0))/SUM(n*a),1) pct_fr, ROUND(SUM(IFF(ct=1,n*a,0))/1e3,1) contrib_k,
  ROUND(SUM(IFF(r LIKE 'BF%TELECOM%',n*a,0))/1e6,2) bftel_m, MIN(IFF(r LIKE 'BF%TELECOM%',d,NULL)) bftel_first,
  ROUND(SUM(IFF(r LIKE 'RESIDENTIAL PROGRAMS%',n*a,0))/1e6,2) rpi_m
FROM k JOIN o USING (EIN) GROUP BY k.EIN, o.org, o.raw_rows, o.raw_amt ORDER BY dedup_m DESC
