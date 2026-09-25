-- S30 who are the Part B = N clinicians on order/refer (NPI still active in NPPES): trainee share, enumeration year, top primary taxonomy codes, vs Part B = Y
WITH o AS (SELECT npi, ANY_VALUE(partb) partb FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_ORDER_AND_REFERRING GROUP BY npi),
n AS (SELECT npi, healthcare_provider_taxonomy_code_1 tx, YEAR(provider_enumeration_date) ey, npi_deactivation_date dd, npi_reactivation_date rd
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES),
j AS (SELECT o.partb, n.tx, n.ey FROM o JOIN n ON n.npi = o.npi WHERE n.dd IS NULL OR n.rd >= n.dd)
SELECT 'share' kind, partb, NULL tx, COUNT(*) npis, COUNT_IF(tx = '390200000X') trainees, ROUND(MEDIAN(ey)) med_enum_year, COUNT_IF(ey >= 2020) enum_2020_on
FROM j GROUP BY partb
UNION ALL
SELECT * FROM (
  SELECT 'top_tx_partb_N', partb, tx, COUNT(*), NULL, ROUND(MEDIAN(ey)), COUNT_IF(ey >= 2020)
  FROM j WHERE partb = 'N' GROUP BY partb, tx ORDER BY COUNT(*) DESC LIMIT 10
)
ORDER BY kind, npis DESC;
