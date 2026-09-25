-- S26 DERA 2024Q1: business addresses shared by many different filers (street line + 5-digit ZIP, letters and digits only), with filer size, blank-EIN share, SIC mix and names
WITH s AS (SELECT *, UPPER(REGEXP_REPLACE(BAS1, '[^A-Za-z0-9]', '')) || '|' || LEFT(ZIPBA, 5) addr FROM LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2024Q1
           WHERE NULLIF(TRIM(BAS1),'') IS NOT NULL)
SELECT addr, ANY_VALUE(CITYBA) city, ANY_VALUE(STPRBA) st, ANY_VALUE(COUNTRYBA) ctry, COUNT(DISTINCT CIK) ciks, COUNT(*) filings,
       COUNT(DISTINCT IFF(LEFT(AFS,1) = '4', CIK, NULL)) non_accel, COUNT(DISTINCT IFF(EIN = '000000000' OR NULLIF(TRIM(EIN),'') IS NULL, CIK, NULL)) ein_blank,
       COUNT(DISTINCT SIC) sics, MODE(SIC) top_sic, COUNT(DISTINCT BAPH) phones,
       ARRAY_SLICE(ARRAY_AGG(DISTINCT NAME) WITHIN GROUP (ORDER BY NAME), 0, 8) names, ARRAY_AGG(DISTINCT FORM) forms
FROM s GROUP BY 1
HAVING COUNT(DISTINCT CIK) >= 6
ORDER BY ciks DESC
LIMIT 40;
