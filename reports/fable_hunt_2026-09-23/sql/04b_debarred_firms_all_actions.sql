select CLASSIFICATION, EXCLUSION_TYPE, count(*) n, count(UEI) with_uei, sum(iff(IS_CURRENTLY_EXCLUDED,1,0)) current from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS group by 1,2 order by n desc limit 20;
select min(ACTIVATION_DATE), max(ACTIVATION_DATE), count(distinct UEI) ueis from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where UEI is not null and UEI <> '';
with ex as (
  select UEI, min(ACTIVATION_DATE) first_excl, max(coalesce(TERMINATION_DATE, '2099-12-31')) last_term, max(ENTITY_NAME) ename, max(EXCLUDING_AGENCY) agency, max(EXCLUSION_TYPE) etype, max(STATE) est
  from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where UEI is not null and UEI <> '' and IS_ENTITY_NOT_INDIVIDUAL group by 1)
select ex.ename, ex.UEI, ex.agency, ex.etype, ex.first_excl, ex.last_term, c.RECIPIENT_NAME, c.RECIPIENT_STATE_CODE, ex.est,
  count(*) actions_after, round(sum(c.FEDERAL_ACTION_OBLIGATION)) obligated_after, min(try_to_date(c.ACTION_DATE)) first_after, max(try_to_date(c.ACTION_DATE)) last_after, listagg(distinct c.AWARDING_AGENCY_NAME, '; ') agencies
from ex join LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 c on c.RECIPIENT_UEI = ex.UEI
where try_to_date(c.ACTION_DATE) > ex.first_excl and try_to_date(c.ACTION_DATE) < ex.last_term and c.FEDERAL_ACTION_OBLIGATION > 0
group by 1,2,3,4,5,6,7,8,9 order by obligated_after desc limit 50
