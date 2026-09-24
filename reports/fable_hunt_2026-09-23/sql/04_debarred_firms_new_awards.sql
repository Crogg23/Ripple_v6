with ex as (
  select UEI, min(ACTIVATION_DATE) first_excl, max(coalesce(TERMINATION_DATE, '2099-12-31')) last_term, max(ENTITY_NAME) ename, max(EXCLUDING_AGENCY) agency, max(EXCLUSION_TYPE) etype
  from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS where UEI is not null and UEI <> '' and IS_ENTITY_NOT_INDIVIDUAL group by 1),
c as (
  select c.RECIPIENT_UEI, c.AWARD_ID_PIID, c.CONTRACT_AWARD_UNIQUE_KEY, try_to_date(c.ACTION_DATE) adate, c.FEDERAL_ACTION_OBLIGATION obl, c.AWARDING_AGENCY_NAME agency, c.RECIPIENT_NAME rname, c.AWARD_TYPE, c.TRANSACTION_DESCRIPTION descr
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 c join ex on ex.UEI = c.RECIPIENT_UEI),
piid as (select CONTRACT_AWARD_UNIQUE_KEY, min(adate) piid_first from c group by 1)
select ex.ename, ex.UEI, ex.agency excl_by, ex.etype, ex.first_excl, ex.last_term,
  count(*) actions_during, round(sum(c.obl)) obligated_during,
  sum(iff(p.piid_first > ex.first_excl,1,0)) new_award_actions, round(sum(iff(p.piid_first > ex.first_excl, c.obl, 0))) new_award_dollars,
  count(distinct iff(p.piid_first > ex.first_excl, c.CONTRACT_AWARD_UNIQUE_KEY, null)) new_awards,
  listagg(distinct c.agency, '; ') agencies
from c join ex on ex.UEI = c.RECIPIENT_UEI join piid p on p.CONTRACT_AWARD_UNIQUE_KEY = c.CONTRACT_AWARD_UNIQUE_KEY
where c.adate > ex.first_excl and c.adate < ex.last_term and c.obl > 0
group by 1,2,3,4,5,6 having new_award_dollars > 0 order by new_award_dollars desc limit 40
