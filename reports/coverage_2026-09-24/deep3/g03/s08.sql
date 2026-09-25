-- S08 UDS site NPIs -> NPPES: is the NPI a person or an org, active or deactivated, which state, which name
WITH s AS (SELECT DISTINCT fqhc_site_npi_number npi FROM LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES
           WHERE fqhc_site_npi_number IS NOT NULL AND fqhc_site_npi_number <> '')
SELECT s.npi, n.entity_type_code, n.provider_organization_name_legal_business_name org, n.provider_last_name_legal_name ln,
       n.provider_first_name fn, n.provider_business_practice_location_address_state_name pst,
       n.provider_business_practice_location_address_city_name pcity, n.healthcare_provider_taxonomy_code_1 tax1,
       n.provider_enumeration_date enum_dt, n.npi_deactivation_date deact, n.npi_reactivation_date react
FROM s LEFT JOIN LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n ON n.npi = s.npi
