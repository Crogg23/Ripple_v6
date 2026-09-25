-- #19 carbon-date the supplier file: newest NPPES enumeration date among its supplier NPIs, and counts enumerated per year 2023-2026
with s as (select distinct SUPLR_NPI npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DURABLE_MEDICAL_EQUIPMENT_DEVICES_SUPPLIES_BY_SUPPL)
select year(n.PROVIDER_ENUMERATION_DATE) yr, count(*) npis, max(n.PROVIDER_ENUMERATION_DATE)::varchar newest
from s join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NPPES n on n.NPI=s.npi where n.PROVIDER_ENUMERATION_DATE >= '2023-01-01' group by 1 order by 1
