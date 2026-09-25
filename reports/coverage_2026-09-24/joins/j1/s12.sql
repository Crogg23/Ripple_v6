-- Provider Relief Fund: prebuilt chain row for CHAIN_ID 446, plus raw PRF lines in MO/KS whose name matches a Reliant home name or entity (name + state)
select 'chain_row' src, CHAIN_NAME name, null city, MATCHED_HOMES::varchar homes, MATCHED_RELIEF_DOLLARS amt, EXACT_MATCH_DOLLARS::varchar extra from LIBRARY_MARTS.HEALTH.HEALTH__NURSING_HOME_RELIEF_BY_CHAIN where CHAIN_ID='446'
union all
select 'prf_line', f.PROVIDER_NAME, f.CITY, f.STATE, f.PAYMENT_AMOUNT, n.PROVIDER_NAME
from LIBRARY_MARTS.HEALTH.HEALTH__FED_HRSA_PROVIDER_RELIEF_FUND f
join (select distinct PROVIDER_NAME, upper(CITY) city, STATE, regexp_replace(upper(PROVIDER_NAME),'[^A-Z0-9]','') k from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME where CHAIN_ID='446') n
  on f.STATE=n.STATE and (regexp_replace(upper(f.PROVIDER_NAME),'[^A-Z0-9]','') like n.k||'%' or f.PROVIDER_NAME ilike '%RELIANT CARE%')
where f.STATE in ('MO','KS')
order by 1, 2
