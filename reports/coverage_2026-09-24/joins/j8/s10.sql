-- Schedule A (money in) for the 19: itemized donors, copies across forms and lump rows dropped; donor = name + 5-digit zip; how many donors give to several of the 19
WITH g AS (SELECT column1 EIN FROM VALUES ('821194581'),('822366231'),('815214552'),('843153271'),('822315009'),('834686848'),('843763411'),('853307234'),('472041040'),('273594732'),('843763242'),
  ('921706849'),('922354897'),('861386683'),('843763606'),('922452599'),('923489519'),('854325630'),('923489713')),
a AS (SELECT s.EIN, REGEXP_REPLACE(UPPER(CONTRIBUTOR_NAME),'[^A-Z ]','') nm, LEFT(CONTRIBUTOR_ZIP,5) z, CONTRIBUTION_DATE d, CONTRIBUTION_AMOUNT amt, FORM_ID_NUMBER, COUNT(*) n,
   MAX(IFF(UPPER(CONTRIBUTOR_OCCUPATION) LIKE 'RETIRED%',1,0)) ret
  FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS s JOIN g ON g.EIN=s.EIN
  WHERE NOT REGEXP_LIKE(UPPER(CONTRIBUTOR_NAME),'.*(AGGREGATE|UNITEMIZED|TOTAL|BELOW THRESHOLD|VARIOUS|NON-ITEMIZED|NONITEMIZED|WITHHELD).*')
  GROUP BY 1,2,3,4,5,6),
k AS (SELECT EIN, nm, z, d, amt, MAX(n) n, MAX(ret) ret FROM a GROUP BY 1,2,3,4,5),
dn AS (SELECT nm, z, COUNT(DISTINCT EIN) groups, SUM(n*amt) tot, SUM(n) gifts, MAX(ret) ret FROM k GROUP BY 1,2)
SELECT 'all' k, NULL grp, COUNT(*) donors, SUM(gifts) gifts, ROUND(SUM(tot)/1e6,2) tot_m, ROUND(MEDIAN(tot),0) med_per_donor, ROUND(100*AVG(ret),1) pct_retired,
  SUM(IFF(groups>=2,1,0)) donors_2plus, SUM(IFF(groups>=5,1,0)) donors_5plus, MAX(groups) max_groups, ROUND(SUM(IFF(groups>=2,tot,0))/1e6,2) tot_2plus_m
FROM dn
UNION ALL
SELECT 'grp', EIN, COUNT(DISTINCT nm||z), SUM(n), ROUND(SUM(n*amt)/1e6,2), ROUND(MEDIAN(amt),0), ROUND(100*AVG(ret),1), NULL, NULL, NULL, NULL FROM k GROUP BY EIN
ORDER BY k, tot_m DESC
