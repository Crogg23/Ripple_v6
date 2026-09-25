-- Timing test for the Lahaina burn tracts: when did registrations arrive, and do late ones verify less? (days from declaration)
with f as (
  select left(CENSUS_GEOID,11) tr, REGISTRATION_ID,
    datediff('day', try_to_timestamp(DECLARATION_DATE::text), try_to_timestamp(APPLIED_DATE::text)) d,
    VERIFIED_OCCUPANCY::text in ('True','true','1') ver, IHP_ELIGIBLE::text in ('True','true','1') elig,
    PRIMARY_RESIDENCE::text in ('True','true','1') prim, REGISTRATION_METHOD rm
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where DISASTER_NUMBER::text = '4724' and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405'))
select tr, case when d is null then 'z_null' when d<=7 then 'a_0-7d' when d<=30 then 'b_8-30d' when d<=90 then 'c_31-90d' else 'd_90d+' end wk,
  count(distinct REGISTRATION_ID) regs, round(100*count_if(ver)/count(*),1) pct_ver_occ, round(100*count_if(elig)/count(*),1) pct_elig,
  round(100*count_if(prim)/count(*),1) pct_primary, listagg(distinct rm,'|') methods, mode(rm) top_method
from f group by 1,2 order by 1,2;
