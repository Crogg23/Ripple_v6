-- Concentration with a denominator: FEMA registrations per 2020 resident, per tract, inside one disaster (peer = same disaster).
-- Vintage-safe slice: disasters declared 2022+, tract codes that land on DIM_TRACT. Registrations deduped by REGISTRATION_ID.
with f as (
  select DISASTER_NUMBER dn, left(CENSUS_GEOID,11) tr, count(*) n_rows, count(distinct REGISTRATION_ID) regs,
         sum(try_to_number(IHP_AMOUNT::text,12,2)) ihp, count_if(IHP_ELIGIBLE::text in ('True','true','1')) ihp_elig,
         any_value(DAMAGED_STATE_ABBREVIATION) st, any_value(INCIDENT_TYPE_CODE) inc, min(DECLARATION_DATE)::text decl,
         mode(DAMAGED_CITY) city
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where year(try_to_timestamp(DECLARATION_DATE::text)) >= 2022 and regexp_like(CENSUS_GEOID, '[0-9]{11,12}(\.0)?')
  group by 1,2),
j as (select f.*, d.POPULATION_2020 pop, f.regs/nullif(d.POPULATION_2020,0) ratio
      from f join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = f.tr),
dis as (select dn, count(*) tracts, sum(regs) dis_regs, median(ratio) med_ratio, count_if(ratio>1 and pop>=1000) over1 from j where pop>=1000 group by 1),
top as (select j.*, dis.tracts, dis.dis_regs, dis.med_ratio, dis.over1 from j join dis using (dn) where pop>=1000 order by ratio desc limit 25)
select 'top' k, dn::text, tr, st, city, inc, decl, pop::text, regs::text, n_rows::text, round(ratio,2)::text, round(med_ratio,3)::text, tracts::text, over1::text, round(ihp)::text, ihp_elig::text from top
union all
select 'summary', null, null, null, null, null, null, count(*)::text, sum(regs)::text, sum(n_rows)::text,
  count_if(ratio>1)::text, count_if(ratio>0.5)::text, count(distinct dn)::text, null, null, null from j where pop>=1000;
