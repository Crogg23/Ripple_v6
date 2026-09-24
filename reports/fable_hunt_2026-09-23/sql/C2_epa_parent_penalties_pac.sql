with x as (
  select EPA_REGISTRY_ID frs, PARENT_LEGAL_NAME parent, PARENT_CIK cik, PARENT_UEI uei from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK where PARENT_LEGAL_NAME is not null and MATCH_METHOD in ('exact','brand')),
p as (
  select x.parent, max(x.cik) cik, count(*) facilities, sum(e.FORMAL_ACTION_COUNT) formal_actions, sum(e.PENALTY_COUNT) penalties, round(sum(e.TOTAL_PENALTIES)/1e6,2) pen_m, sum(iff(e.COMPLIANCE_STATUS='Significant Violation',1,0)) sig_viol_now
  from x join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on e.FRS_ID = x.frs group by 1),
pac as (
  select upper(regexp_replace(split_part(CONNECTED_ORG_NM,' ',1),'[^A-Z0-9]','')) w1, CMTE_ID, CMTE_NM, CONNECTED_ORG_NM
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FEC_COMMITTEES_DIM where CYCLE >= 2020 and CONNECTED_ORG_NM is not null and CMTE_TP in ('Q','N') and ORG_TP = 'C'),
pacsum as (
  select pac.w1, count(distinct pac.CMTE_ID) pacs, listagg(distinct pac.CMTE_NM, ' | ') pac_names
  from pac group by 1)
select p.parent, p.cik, p.facilities, p.formal_actions, p.penalties, p.pen_m, p.sig_viol_now, ps.pacs, ps.pac_names
from p left join pacsum ps on ps.w1 = upper(regexp_replace(split_part(p.parent,' ',1),'[^A-Z0-9]','')) and length(ps.w1) >= 4
order by p.pen_m desc nulls last limit 40
