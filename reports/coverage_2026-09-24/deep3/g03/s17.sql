-- S17 Dialysis-affiliated clinicians x clinic chain (Dialysis Facility Compare, CCN) x PY2024 industry payments from Fresenius (NPI)
--     Peer test: do doctors listed at Fresenius clinics get Fresenius money at a different rate than doctors at DaVita or other clinics?
WITH a AS (SELECT DISTINCT npi, ccn FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION WHERE facility_type = 'Dialysis facility'),
d AS (SELECT ccn, CASE WHEN chain_organization ILIKE '%fresenius%' THEN 'FRESENIUS' WHEN chain_organization ILIKE '%davita%' THEN 'DAVITA'
                       WHEN chain_organization IS NULL OR TRIM(chain_organization) = '' THEN 'NONE_LISTED' ELSE 'OTHER' END grp
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS),
an AS (SELECT a.npi, IFF(COUNT(DISTINCT COALESCE(d.grp,'NO_CCN_MATCH')) > 1, 'MIXED', MAX(COALESCE(d.grp,'NO_CCN_MATCH'))) grp, COUNT(*) clinics
       FROM a LEFT JOIN d ON d.ccn = a.ccn GROUP BY 1),
p AS (SELECT NULLIF(TRIM(npi),'') npi,
             SUM(total_amount_of_payment_usdollars) tot,
             SUM(IFF(applicable_manufacturer_or_applicable_gpo_making_payment_name ILIKE '%fresenius%', total_amount_of_payment_usdollars, 0)) fres,
             SUM(IFF(applicable_manufacturer_or_applicable_gpo_making_payment_name ILIKE '%fresenius%'
                     AND nature_of_payment_or_transfer_of_value NOT ILIKE '%food%', total_amount_of_payment_usdollars, 0)) fres_nonfood,
             LISTAGG(DISTINCT IFF(applicable_manufacturer_or_applicable_gpo_making_payment_name ILIKE '%fresenius%', nature_of_payment_or_transfer_of_value, NULL), '; ') fres_natures
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS
      WHERE NULLIF(TRIM(npi),'') IN (SELECT npi FROM an) GROUP BY 1)
SELECT an.grp, COUNT(*) npis, ROUND(AVG(an.clinics),2) avg_clinics, COUNT(p.npi) any_pay, COUNT_IF(p.fres > 0) fres_paid,
       ROUND(COUNT_IF(p.fres > 0)/COUNT(*)*100,1) pct_fres, COUNT_IF(p.fres_nonfood > 0) fres_nonfood_paid,
       ROUND(SUM(p.fres)) fres_dollars, ROUND(SUM(p.fres_nonfood)) fres_nonfood_dollars,
       ROUND(MEDIAN(IFF(p.fres > 0, p.fres, NULL)),2) med_fres_paid, ROUND(MAX(p.fres)) max_fres, ROUND(SUM(p.tot)) all_industry_dollars,
       ANY_VALUE(p.fres_natures) eg_natures
FROM an LEFT JOIN p ON p.npi = an.npi GROUP BY 1 ORDER BY npis DESC
