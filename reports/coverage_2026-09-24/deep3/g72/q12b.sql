-- (rerun of q12 after a compile error) Test inside the group: Ian (4673), Maui (4724), LA fires (4856). Per tract: registrations and PEOPLE CLAIMED (sum of household size) vs 2020 residents,
-- verified occupancy, primary residence, renters, IHP-eligible. Top 6 tracts per disaster by registrations per resident, plus the rest of each disaster pooled.
with f as (
  select DISASTER_NUMBER dn, left(CENSUS_GEOID,11) tr, count(distinct REGISTRATION_ID) regs,
    sum(try_to_number(HOUSEHOLD_COMPOSITION::text)) people, count_if(try_to_number(HOUSEHOLD_COMPOSITION::text) is null) hh_null,
    count_if(VERIFIED_OCCUPANCY::text in ('True','true','1')) ver_occ, count_if(PRIMARY_RESIDENCE::text in ('True','true','1')) prim,
    count_if(OWN_RENT='R') renters, count_if(IHP_ELIGIBLE::text in ('True','true','1')) elig, sum(try_to_number(IHP_AMOUNT::text,12,2)) ihp,
    count_if(INSUFFICIENT_DAMAGE::text in ('True','true','1')) insuff, count_if(DESTROYED::text in ('True','true','1')) destroyed,
    mode(DAMAGED_CITY) city
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where DISASTER_NUMBER::text in ('4673','4724','4856') and regexp_like(CENSUS_GEOID, '[0-9]{11,12}(\.0)?')
  group by 1,2),
j as (select f.*, d.POPULATION_2020 pop, f.regs/nullif(d.POPULATION_2020,0) ratio,
        row_number() over (partition by dn order by f.regs/nullif(d.POPULATION_2020,0) desc) rk,
        count(*) over (partition by dn) ntr
      from f join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = f.tr where d.POPULATION_2020 >= 1000)
select dn::text dn, iff(rk<=6, tr, 'rest ('||(ntr-6)||' tracts)') tract, max(iff(rk<=6, city, null)) city,
  sum(pop) pop, sum(regs) regs, sum(people) people_claimed, round(sum(people)/sum(pop),2) people_per_resident,
  round(sum(regs)/sum(pop),2) regs_per_resident, round(sum(people)/nullif(sum(regs)-sum(hh_null),0),2) hh_size,
  round(100*sum(ver_occ)/sum(regs),1) pct_ver_occ, round(100*sum(prim)/sum(regs),1) pct_primary, round(100*sum(renters)/sum(regs),1) pct_rent,
  round(100*sum(elig)/sum(regs),1) pct_elig, round(100*sum(destroyed)/sum(regs),1) pct_destroyed, round(100*sum(insuff)/sum(regs),1) pct_insuff, round(sum(ihp)) ihp
from j group by dn, iff(rk<=6, tr, 'rest ('||(ntr-6)||' tracts)')
order by 1, min(rk);
