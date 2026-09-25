-- S15 Facility affiliation shape by facility type: rows, distinct pairs (duplicate check), clinicians, facilities, widest clinician
WITH a AS (SELECT NULLIF(TRIM(npi),'') npi, ccn, facility_type, ind_pac_id, facility_type_certification_number ftcn
           FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION),
w AS (SELECT facility_type, npi, COUNT(DISTINCT ccn) k FROM a GROUP BY 1,2)
SELECT a.facility_type, COUNT(*) rows_, COUNT(DISTINCT a.npi, a.ccn) pairs, COUNT(DISTINCT a.npi) npis, COUNT(DISTINCT a.ccn) ccns,
       COUNT_IF(a.npi IS NULL) npi_blank, COUNT(DISTINCT a.ind_pac_id) pacs, COUNT_IF(NULLIF(TRIM(a.ftcn),'') IS NOT NULL) ftcn_filled,
       ANY_VALUE(a.ccn) eg_ccn,
       (SELECT MAX(k) FROM w WHERE w.facility_type = a.facility_type) max_fac_per_npi,
       (SELECT MEDIAN(k) FROM w WHERE w.facility_type = a.facility_type) med_fac_per_npi,
       (SELECT COUNT_IF(k >= 10) FROM w WHERE w.facility_type = a.facility_type) npis_10plus
FROM a GROUP BY a.facility_type ORDER BY rows_ DESC
