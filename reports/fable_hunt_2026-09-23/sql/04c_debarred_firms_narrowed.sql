-- B5 as narrowed after the skeptic: government-wide exclusions only, orders split from standalone awards.
with ex as (
  select UEI, min(ACTIVATION_DATE) first_excl, max(coalesce(TERMINATION_DATE, '2099-12-31')) last_term, max(ENTITY_NAME) ename, max(EXCLUDING_AGENCY) agency, max(EXCLUSION_TYPE) etype, max(EXCLUSION_PROGRAM) program
  from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
  where UEI is not null and UEI <> '' and IS_ENTITY_NOT_INDIVIDUAL
    and EXCLUSION_PROGRAM in ('Reciprocal','Procurement') and EXCLUSION_TYPE not ilike 'Prohibition%'
  group by 1),
c as (
  select c.RECIPIENT_UEI, c.CONTRACT_AWARD_UNIQUE_KEY k, split_part(c.CONTRACT_AWARD_UNIQUE_KEY,'_',5) parent_piid, try_to_date(c.ACTION_DATE) adate, c.FEDERAL_ACTION_OBLIGATION obl, c.AWARDING_AGENCY_NAME agency, c.RECIPIENT_NAME rname
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 c join ex on ex.UEI = c.RECIPIENT_UEI),
first_action as (select k, min(adate) k_first from c group by 1),
parent_first as (
  select split_part(CONTRACT_AWARD_UNIQUE_KEY,'_',5) parent_piid, min(try_to_date(ACTION_DATE)) p_first
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2
  where split_part(CONTRACT_AWARD_UNIQUE_KEY,'_',5) in (select distinct parent_piid from c where parent_piid <> '-NONE-') group by 1),
hits as (
  select ex.ename, ex.UEI, ex.agency excl_by, ex.etype, ex.program, ex.first_excl, ex.last_term, c.k, c.parent_piid, c.adate, c.obl, c.agency, c.rname,
    case when c.parent_piid = '-NONE-' then 'standalone award'
         when pf.p_first < ex.first_excl then 'order under parent from before exclusion'
         when pf.p_first >= ex.first_excl then 'order under parent from after exclusion'
         else 'order under parent, parent not in table' end kind
  from c join ex on ex.UEI = c.RECIPIENT_UEI join first_action fa on fa.k = c.k left join parent_first pf on pf.parent_piid = c.parent_piid
  where c.adate > ex.first_excl and c.adate < ex.last_term and c.obl > 0 and fa.k_first > ex.first_excl)
select kind, count(distinct UEI) firms, count(*) actions, round(sum(obl)) usd, sum(iff(obl < 10000,1,0)) under_10k from hits group by 1 order by usd desc;
with ex as (
  select UEI, min(ACTIVATION_DATE) first_excl, max(coalesce(TERMINATION_DATE, '2099-12-31')) last_term, max(ENTITY_NAME) ename, max(EXCLUDING_AGENCY) agency, max(EXCLUSION_TYPE) etype, max(EXCLUSION_PROGRAM) program
  from LIBRARY_MARTS.PROCUREMENT.PROCUREMENT__FED_SAM_EXCLUSIONS
  where UEI is not null and UEI <> '' and IS_ENTITY_NOT_INDIVIDUAL
    and EXCLUSION_PROGRAM in ('Reciprocal','Procurement') and EXCLUSION_TYPE not ilike 'Prohibition%'
  group by 1),
c as (
  select c.RECIPIENT_UEI, c.CONTRACT_AWARD_UNIQUE_KEY k, split_part(c.CONTRACT_AWARD_UNIQUE_KEY,'_',5) parent_piid, try_to_date(c.ACTION_DATE) adate, c.FEDERAL_ACTION_OBLIGATION obl, c.AWARDING_AGENCY_NAME agency, c.RECIPIENT_NAME rname
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2 c join ex on ex.UEI = c.RECIPIENT_UEI),
first_action as (select k, min(adate) k_first from c group by 1),
parent_first as (
  select split_part(CONTRACT_AWARD_UNIQUE_KEY,'_',5) parent_piid, min(try_to_date(ACTION_DATE)) p_first
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2
  where split_part(CONTRACT_AWARD_UNIQUE_KEY,'_',5) in (select distinct parent_piid from c where parent_piid <> '-NONE-') group by 1),
hits as (
  select ex.ename, ex.UEI, ex.agency excl_by, ex.etype, ex.program, ex.first_excl, ex.last_term, c.k, c.parent_piid, c.adate, c.obl, c.agency, c.rname,
    case when c.parent_piid = '-NONE-' then 'standalone award'
         when pf.p_first < ex.first_excl then 'order under parent from before exclusion'
         when pf.p_first >= ex.first_excl then 'order under parent from after exclusion'
         else 'order under parent, parent not in table' end kind
  from c join ex on ex.UEI = c.RECIPIENT_UEI join first_action fa on fa.k = c.k left join parent_first pf on pf.parent_piid = c.parent_piid
  where c.adate > ex.first_excl and c.adate < ex.last_term and c.obl > 0 and fa.k_first > ex.first_excl)
select ename, excl_by, etype, first_excl, last_term, rname, count(*) actions, round(sum(obl)) usd, listagg(distinct kind, '; ') kinds, min(adate) first_after, max(adate) last_after, listagg(distinct agency, '; ') agencies
from hits group by 1,2,3,4,5,6 order by usd desc
