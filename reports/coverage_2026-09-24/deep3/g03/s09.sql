-- S09 Open Payments profile roster shape: is it a one-row-per-person crosswalk? duplicate NPIs, blank NPIs, alternate names
WITH r AS (SELECT * FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_PROFILE_SUPPLEMENT),
d AS (SELECT npi, COUNT(*) k, COUNT(DISTINCT profile_id) p FROM r WHERE NULLIF(TRIM(npi),'') IS NOT NULL GROUP BY 1)
SELECT (SELECT COUNT(*) FROM r) n, (SELECT COUNT(DISTINCT profile_id) FROM r) profiles,
       (SELECT COUNT_IF(npi IS NULL) FROM r) npi_null, (SELECT COUNT_IF(TRIM(npi)='') FROM r) npi_empty,
       (SELECT COUNT(*) FROM d) npis, (SELECT COUNT_IF(k>1) FROM d) npis_multi_row, (SELECT COUNT_IF(p>1) FROM d) npis_multi_profile,
       (SELECT MAX(p) FROM d) max_profiles_per_npi,
       (SELECT COUNT_IF(NULLIF(TRIM(alternate_last_name),'') IS NOT NULL) FROM r) alt_last,
       (SELECT COUNT_IF(NULLIF(TRIM(alternate_last_name),'') IS NOT NULL AND UPPER(alternate_last_name)<>UPPER(last_name)) FROM r) alt_last_diff,
       (SELECT COUNT_IF(NULLIF(TRIM(associated_profile_id_1),'') IS NOT NULL) FROM r) assoc1,
       (SELECT COUNT_IF(NULLIF(TRIM(license_state_code_5),'') IS NOT NULL) FROM r) lic5,
       (SELECT COUNT(DISTINCT source_run_id) FROM r) runs, (SELECT ARRAY_AGG(DISTINCT profile_type) FROM r) types,
       (SELECT COUNT_IF(npi IS NULL OR TRIM(npi)='') FROM r WHERE profile_type ILIKE '%Non-Physician%') npp_blank_npi
