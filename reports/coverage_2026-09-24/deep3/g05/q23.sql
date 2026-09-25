-- ASM base rate: share of same-specialty, same-state Part B 2024 clinicians NOT in the model who are on the OIG list or the opt-out list; plus when the ASM table was loaded (mart + landing metadata)
with a as (select distinct NPI from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_AMBULATORY_SPECIALTY_MODEL_PARTICIPANTS),
b as (select RNDRNG_NPI npi, RNDRNG_PRVDR_TYPE typ, RNDRNG_PRVDR_STATE_ABRVTN st from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER
      where RNDRNG_PRVDR_TYPE in ('Cardiology','Physical Medicine and Rehabilitation','Orthopedic Surgery','Pain Management','Anesthesiology','Interventional Pain Management','Neurosurgery')),
l as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE where NPI_IS_REAL),
o as (select distinct trim(NPI) npi from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS)
select 'base' k, iff(a.NPI is null,'not_in_model','in_model') a, count(*)::text b, count(l.npi)::text c, count(o.npi)::text d, round(100*count(l.npi)/count(*),3)::text e, round(100*count(o.npi)/count(*),3)::text f
from b left join a on a.NPI=b.npi left join l on l.npi=b.npi left join o on o.npi=b.npi group by 2
union all select 'mart_meta', table_name, row_count::text, created::text, last_altered::text, null, null from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where table_name ilike '%AMBULATORY_SPECIALTY%'
union all select 'landing_meta', table_name, row_count::text, created::text, last_altered::text, null, null from LIBRARY_RAW.INFORMATION_SCHEMA.TABLES where table_name ilike '%AMBULATORY%' or table_name ilike '%ASM%PARTIC%'
