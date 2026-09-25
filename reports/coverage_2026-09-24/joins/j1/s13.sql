-- OSHA inspections: establishment name starts with a Reliant home name (punctuation stripped), same state and same city; or name contains RELIANT CARE
with n as (select distinct PROVIDER_NAME, upper(CITY) city, STATE, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446'),
o as (select ACTIVITY_NR, ESTAB_NAME, upper(SITE_CITY) city, SITE_STATE, SITE_ADDRESS, OPEN_DATE, CLOSE_CASE_DATE, INSP_TYPE, INSP_SCOPE, SAFETY_HLTH, NAICS_CODE, OWNER_TYPE, regexp_replace(upper(ESTAB_NAME),'[^A-Z0-9]','') k
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_DOL_OSHA_INSPECTIONS where SITE_STATE in ('MO','KS'))
select n.PROVIDER_NAME, n.city home_city, o.ESTAB_NAME, o.city osha_city, o.SITE_ADDRESS, o.OPEN_DATE, o.INSP_TYPE, o.INSP_SCOPE, o.SAFETY_HLTH, o.NAICS_CODE, o.ACTIVITY_NR
from o left join n on o.SITE_STATE=n.STATE and o.k like n.k||'%'
where (n.k is not null) or o.ESTAB_NAME ilike '%RELIANT CARE%'
order by o.OPEN_DATE desc
