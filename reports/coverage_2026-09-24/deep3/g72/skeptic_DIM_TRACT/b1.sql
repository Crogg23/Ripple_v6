-- @@ s1_geocode_96761
select coalesce(nullif(left(f.CENSUS_GEOID,11),''),'NO_CODE') tr, f.CENSUS_YEAR cy, count(*) n, count(distinct f.REGISTRATION_ID) regs,
  round(100*count_if(f.VERIFIED_OCCUPANCY::text in ('True','true','1'))/count(*),1) pct_ver,
  round(100*count_if(f.DESTROYED::text in ('True','true','1'))/count(*),1) pct_destr,
  mode(f.DAMAGED_CITY) city, max(d.POPULATION_2020) pop, max(d.VINTAGE) vint
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS f
left join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = left(f.CENSUS_GEOID,11)
where f.DISASTER_NUMBER = '4724' and f.DAMAGED_ZIP_CODE like '96761%'
group by 1,2 order by n desc;

-- @@ s2_strata
with f as (
  select left(CENSUS_GEOID,11) tr, PRIMARY_RESIDENCE::text pr, OWN_RENT orr,
    case when RESIDENCE_TYPE in ('A','H','C') then RESIDENCE_TYPE else 'other' end rt,
    VERIFIED_OCCUPANCY::text in ('True','true','1') v
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where DISASTER_NUMBER = '4724' and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405'))
select tr, pr, orr, rt, count(*) n, round(100*count_if(v)/count(*),1) pct_ver
from f group by grouping sets ((tr), (tr,pr), (tr,pr,orr), (tr,pr,orr,rt))
order by tr, pr nulls first, orr nulls first, rt nulls first;

-- @@ s3_inelig_reason
with f as (
  select left(CENSUS_GEOID,11) tr, VERIFIED_OCCUPANCY::text in ('True','true','1') v, coalesce(INELIGIBLE_REASON,'<null>') rsn
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where DISASTER_NUMBER = '4724' and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405')),
g as (select tr, v, rsn, count(*) n, row_number() over (partition by tr, v order by count(*) desc) rk from f group by 1,2,3)
select tr, v, rsn, n from g where rk <= 8 order by tr, v, n desc;

-- @@ s4_ids_and_raw
select 'table_ids' k, count(*)::text a, count(distinct REGISTRATION_ID)::text b, min(length(REGISTRATION_ID))::text c, max(length(REGISTRATION_ID))::text d, min(REGISTRATION_ID) e
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
union all
select 'refresh_4724', count(*)::text, count(distinct LAST_REFRESH)::text, min(LAST_REFRESH), max(LAST_REFRESH), max(REGISTRATION_ID)
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS where DISASTER_NUMBER = '4724'
union all
select 'VO_raw|'||coalesce(left(CENSUS_GEOID,11),'null'), count(*)::text, coalesce(VERIFIED_OCCUPANCY::text,'<null>'), coalesce(INSPN_RETURNED::text,'<null>'), coalesce(VERIFIED_OWNERSHIP::text,'<null>'), null
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where DISASTER_NUMBER = '4724' and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405')
group by 1,3,4,5
order by 1, 2 desc;

-- @@ s5_neardup
with f as (
  select left(CENSUS_GEOID,11) tr, left(CENSUS_GEOID,12) bg, APPLIED_DATE, APPLICANT_AGE, HOUSEHOLD_COMPOSITION, GROSS_INCOME, OWN_RENT, RESIDENCE_TYPE,
    PRIMARY_RESIDENCE, OCCUPANTS_UNDER_TWO, OCCUPANTS_2_TO_5, OCCUPANTS_6_TO_18, OCCUPANTS_19_TO_64, OCCUPANTS_65_AND_OVER, REGISTRATION_METHOD,
    VERIFIED_OCCUPANCY::text in ('True','true','1') v
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where DISASTER_NUMBER = '4724' and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405')),
g as (select tr, bg, APPLIED_DATE, APPLICANT_AGE, HOUSEHOLD_COMPOSITION, GROSS_INCOME, OWN_RENT, RESIDENCE_TYPE, PRIMARY_RESIDENCE,
        OCCUPANTS_UNDER_TWO, OCCUPANTS_2_TO_5, OCCUPANTS_6_TO_18, OCCUPANTS_19_TO_64, OCCUPANTS_65_AND_OVER, REGISTRATION_METHOD,
        count(*) k, count_if(v) kv from f group by all)
select tr, sum(k) n, count(*) profiles, sum(iff(k>1,k,0)) rows_in_repeat_profiles, max(k) max_k,
  round(100*sum(iff(k>1,kv,0))/nullif(sum(iff(k>1,k,0)),0),1) pct_ver_in_repeats,
  round(100*sum(iff(k=1,kv,0))/nullif(sum(iff(k=1,k,0)),0),1) pct_ver_in_singles,
  count_if(GROSS_INCOME is null)::text null_income_profiles
from g group by tr order by tr;

-- @@ s6_peer_rank
with f as (
  select DISASTER_NUMBER dn, left(CENSUS_GEOID,11) tr, count(*) regs,
    count_if(VERIFIED_OCCUPANCY::text in ('True','true','1')) ver,
    count_if(PRIMARY_RESIDENCE::text in ('True','true','1')) prim,
    count_if(PRIMARY_RESIDENCE::text in ('True','true','1') and VERIFIED_OCCUPANCY::text in ('True','true','1')) prim_ver,
    count_if(DESTROYED::text in ('True','true','1')) destr, count_if(OWN_RENT = 'R') rent,
    mode(DAMAGED_CITY) city, any_value(DAMAGED_STATE_ABBREVIATION) st
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where year(DECLARATION_DATE) >= 2022 and regexp_like(CENSUS_GEOID, '[0-9]{11,12}(\.0)?')
  group by 1,2 having count(*) >= 500),
r as (select f.*, round(100*ver/regs,1) pv, round(100*prim_ver/nullif(prim,0),1) pvp, round(100*destr/regs,1) pd, round(100*rent/regs,1) pr,
        round(100*prim/regs,1) pprim,
        rank() over (order by ver/regs) rk, rank() over (order by prim_ver/nullif(prim,0)) rk_prim, count(*) over () npairs,
        count_if(destr/regs >= 0.3) over () n_destr30,
        median(iff(destr/regs >= 0.3, 100*ver/regs, null)) over () med_pv_destr30
      from f)
select dn, tr, st, city, regs, pv, pvp, pd, pr, pprim, rk, rk_prim, npairs, n_destr30, round(med_pv_destr30,1) med_pv_destr30
from r where rk <= 25 or rk_prim <= 15 or tr in ('15009031404','15009031402','15009031405') or (pd >= 30 and pv < 85)
order by rk;

-- @@ s7_hhsize
with f as (
  select left(CENSUS_GEOID,11) tr, OWN_RENT orr,
    case when try_to_number(HOUSEHOLD_COMPOSITION::text) is null then 'unk' when try_to_number(HOUSEHOLD_COMPOSITION::text) = 1 then '1'
         when try_to_number(HOUSEHOLD_COMPOSITION::text) = 2 then '2' when try_to_number(HOUSEHOLD_COMPOSITION::text) <= 4 then '3-4' else '5+' end hh,
    VERIFIED_OCCUPANCY::text in ('True','true','1') v
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where DISASTER_NUMBER = '4724' and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405')
    and PRIMARY_RESIDENCE::text in ('True','true','1'))
select tr, orr, hh, count(*) n, round(100*count_if(v)/count(*),1) pct_ver
from f group by 1,2,3 order by 1,2,3;
