select year(DATE_RECEIVED) yr, count(*) n from LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS group by 1 order by 1;
with orders as (
  select CERT_NUMBER cert, max(BANK_NAME) bank, count(*) orders, min(ORDER_DATE) first_order, sum(CMP_AMOUNT_TOTAL) cmp
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS
  where ORDER_YEAR between 2019 and 2024 and CERT_NUMBER is not null and (ORDER_TYPE ilike '%cease%' or ORDER_TYPE ilike '%civil money%' or ORDER_TYPE ilike '%restitution%') group by 1),
dep as (
  select FDIC_CERT::number cert, SURVEY_YEAR, max(INSTITUTION_NAME) iname, sum(BRANCH_DEPOSITS_THOUSANDS) dep_k, count(*) branches
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS where SURVEY_YEAR in (2018, 2024) group by 1,2),
d18 as (select * from dep where SURVEY_YEAR=2018), d24 as (select * from dep where SURVEY_YEAR=2024)
select iff(o.cert is null,'no order','order 2019-24') grp, count(*) banks, round(median(100.0*(d24.dep_k-d18.dep_k)/nullif(d18.dep_k,0)),1) med_dep_growth_pct, round(median(100.0*(d24.branches-d18.branches)/nullif(d18.branches,0)),1) med_branch_growth_pct
from d18 join d24 on d24.cert = d18.cert left join orders o on o.cert = d18.cert group by 1;
with orders as (
  select CERT_NUMBER cert, max(BANK_NAME) bank, count(*) orders, min(ORDER_DATE) first_order, sum(CMP_AMOUNT_TOTAL) cmp, listagg(distinct ORDER_TYPE, '; ') types
  from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_FDIC_ENFORCEMENT_ORDERS
  where ORDER_YEAR between 2019 and 2024 and CERT_NUMBER is not null and (ORDER_TYPE ilike '%cease%' or ORDER_TYPE ilike '%civil money%' or ORDER_TYPE ilike '%restitution%') group by 1),
dep as (
  select FDIC_CERT::number cert, max(INSTITUTION_NAME) iname, sum(BRANCH_DEPOSITS_THOUSANDS) dep_k, count(*) branches
  from LIBRARY_MARTS.FINANCE.FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS where SURVEY_YEAR = 2024 group by 1),
cf as (
  select upper(COMPANY) company, count(*) complaints from LIBRARY_MARTS.CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS where DATE_RECEIVED between '2022-01-01' and '2024-12-31' group by 1)
select o.bank, o.cert, o.orders, o.types, o.cmp, round(dep.dep_k/1e6,1) dep_bn, dep.branches, cf.company, cf.complaints, round(1e6*cf.complaints/nullif(dep.dep_k*1000,0),1) complaints_per_bn_dep
from orders o join dep on dep.cert = o.cert
left join cf on cf.company = upper(o.bank) or cf.company = upper(dep.iname)
order by o.cmp desc nulls last limit 30
