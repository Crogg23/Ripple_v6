-- S16 Affiliated clinicians whose NPI NPPES lists as deactivated and not reactivated, by deactivation year; plus NPIs missing from NPPES
WITH a AS (SELECT npi, MAX(provider_last_name) ln, MAX(provider_first_name) fn, COUNT(*) k,
                  LISTAGG(DISTINCT facility_type, '|') types
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION GROUP BY 1),
n AS (SELECT npi, TRY_TO_DATE(npi_deactivation_date::string) dd, TRY_TO_DATE(npi_reactivation_date::string) rd, entity_type_code et,
             provider_last_name_legal_name nln
      FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES WHERE npi IN (SELECT npi FROM a)),
j AS (SELECT a.*, n.dd, n.rd, n.et, n.nln, (n.npi IS NULL) missing FROM a LEFT JOIN n ON n.npi = a.npi)
SELECT IFF(missing, 'not_in_nppes', IFF(dd IS NOT NULL AND (rd IS NULL OR rd < dd), 'deactivated', 'active')) status,
       YEAR(dd) dyear, COUNT(*) npis, SUM(k) rows_, COUNT_IF(types ILIKE '%Hospital%') in_hospital,
       COUNT_IF(et = '2') org_npi, ANY_VALUE(npi || ' ' || fn || ' ' || ln) eg
FROM j GROUP BY 1,2 ORDER BY 1,2
