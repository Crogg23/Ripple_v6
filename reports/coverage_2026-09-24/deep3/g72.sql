-- deep3 / g72: proper look at five glance-only tables, 2026-09-24
-- Tables: OPEN_DATA__INTL_ES_DATOSGOB, OPEN_DATA__INTL_CA_OPEN_CANADA, OPEN_DATA__INTL_GE_DATAGOV,
--         OPEN_DATA__INTL_GH_DATAGOVGH, DIM_TRACT
-- Door: Python (connect/db.py) via g72/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g72/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- Spain datos.gob.es: fill rate of every column, distincts, date span (Spanish text dates, year = last 4 chars)
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_ES_DATOSGOB)
select count(*) n,
  count_if(nullif(trim(URI),'') is not null) uri_filled, count_if(nullif(trim(TITLE),'') is not null) title_filled,
  count_if(nullif(trim(DESCRIPTION),'') is not null) desc_filled, count_if(nullif(trim(PUBLISHER),'') is not null) pub_filled,
  count_if(nullif(trim(SECTOR),'') is not null) sector_filled, count_if(nullif(trim(GEOGRAPHIC_COVERAGE),'') is not null) geo_filled,
  count_if(nullif(trim(DISTRIBUTION_URL),'') is not null) dist_filled, count_if(nullif(trim(FORMAT),'') is not null) fmt_filled,
  count_if(nullif(trim(LICENSE),'') is not null) lic_filled, count_if(nullif(trim(ISSUED),'') is not null) issued_filled,
  count_if(nullif(trim(MODIFIED),'') is not null) mod_filled,
  count(distinct PUBLISHER) pubs, count(distinct SECTOR) sectors, count(distinct DISTRIBUTION_URL) dist_urls,
  count(distinct FORMAT) fmts, count(distinct LICENSE) lics,
  min(try_to_number(right(trim(ISSUED),4))) issued_min_yr, max(try_to_number(right(trim(ISSUED),4))) issued_max_yr,
  min(try_to_number(right(trim(MODIFIED),4))) mod_min_yr, max(try_to_number(right(trim(MODIFIED),4))) mod_max_yr,
  count(distinct _SOURCE_URL) src_urls, any_value(_SOURCE_URL) src, min(_LOADED_AT)::text loaded_min, max(_LOADED_AT)::text loaded_max,
  any_value(ISSUED) issued_eg, any_value(FORMAT) fmt_eg, any_value(DISTRIBUTION_URL) dist_eg
from t;

-- [q02] statement 2
-- Spain: full publisher and sector strings (glance truncated them), plus year issued / modified
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_ES_DATOSGOB)
select * from (
 select 'publisher' k, PUBLISHER v, count(*) n from t group by 2 order by 3 desc limit 12)
union all select * from (
 select 'sector', SECTOR, count(*) from t group by 2 order by 3 desc limit 8)
union all select * from (
 select 'issued_yr', right(trim(ISSUED),4), count(*) from t group by 2 order by 2)
union all select * from (
 select 'modified_yr', right(trim(MODIFIED),4), count(*) from t group by 2 order by 2)
union all select * from (
 select 'format', FORMAT, count(*) from t group by 2 order by 3 desc limit 8)
union all select * from (
 select 'dup_dist_url', DISTRIBUTION_URL, count(*) from t group by 2 having count(*)>1 order by 3 desc limit 5);

-- [q03] statement 3
-- Canada: profile, dupes, sentinel coverage dates, created/modified span, resource files per package
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CA_OPEN_CANADA)
select count(*) n, count(distinct DATASET_ID) ids,
  min(METADATA_CREATED)::text created_min, max(METADATA_CREATED)::text created_max,
  min(METADATA_MODIFIED)::text mod_min, max(METADATA_MODIFIED)::text mod_max,
  count_if(TIME_PERIOD_COVERAGE_START::text like '0001%') cov_start_0001, count_if(TIME_PERIOD_COVERAGE_START is null) cov_start_null,
  count_if(nullif(trim(TIME_PERIOD_COVERAGE_END::text),'') is null) cov_end_blank,
  count_if(nullif(trim(NOTES_EN),'') is null) notes_en_blank, count_if(nullif(trim(TITLE_FR),'') is null) title_fr_blank,
  count_if(nullif(trim(DATE_PUBLISHED::text),'') is null) datepub_blank,
  count_if(TAGS = '[]') tags_empty, count(distinct LICENSE_ID) lics, listagg(distinct LICENSE_ID,'|') lic_vals,
  listagg(distinct FREQUENCY,'|') freq_vals,
  sum(array_size(try_parse_json(RESOURCES))) resource_files, count_if(try_parse_json(RESOURCES) is null) res_unparsed,
  max(array_size(try_parse_json(RESOURCES))) max_files, median(array_size(try_parse_json(RESOURCES))) med_files,
  count(distinct _SOURCE_URL) src_urls, any_value(_SOURCE_URL) src
from t;

-- [q04] statement 4
-- Canada: organization x year created, and subject lists
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CA_OPEN_CANADA)
select * from (select 'org_year' k, left(C_ORGANIZATION,60) a, year(METADATA_CREATED)::text b, count(*) n,
   min(METADATA_MODIFIED)::text c, max(METADATA_MODIFIED)::text d from t group by 2,3 order by 2,3)
union all select * from (select 'subject', SUBJECT, null, count(*), null, null from t group by 2 order by 4 desc limit 8)
union all select * from (select 'mod_month', to_char(METADATA_MODIFIED,'YYYY-MM'), null, count(*), null, null from t group by 2 order by 4 desc limit 10);

-- [q05] statement 5
-- Georgia (1 row) and Ghana (10 rows): print every row whole
select 'GE' k, to_json(object_construct_keep_null(*))::text row_json from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GE_DATAGOV
union all
select 'GH', to_json(object_construct_keep_null(*))::text from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GH_DATAGOVGH;

-- [q06] statement 6
-- DIM_TRACT: key integrity, padding, sentinels, territories, zero-pop tracts, coordinate sanity
with t as (select * from LIBRARY_MARTS.CORE.DIM_TRACT)
select count(*) n, count(distinct TRACT_GEOID) geoids, count_if(length(TRACT_GEOID)<>11) geoid_not11,
  count_if(length(STATE_FIPS)<>2) st_not2, count_if(length(COUNTY_FIPS)<>5) cty_not5, count_if(length(TRACT_CE)<>6) ce_not6,
  count_if(left(TRACT_GEOID,5)<>COUNTY_FIPS) geoid_cty_mismatch, count_if(left(COUNTY_FIPS,2)<>STATE_FIPS) cty_st_mismatch,
  count_if(right(TRACT_GEOID,6)<>TRACT_CE) ce_mismatch,
  count(distinct STATE_FIPS) states, count(distinct COUNTY_FIPS) counties, listagg(distinct VINTAGE,'|') vintages,
  count_if(POPULATION_2020 is null) pop_null, count_if(POPULATION_2020=0) pop_zero, sum(POPULATION_2020) pop_sum,
  median(POPULATION_2020) pop_med, max(POPULATION_2020) pop_max,
  count_if(POPULATION_2020>8000) over_8000, count_if(POPULATION_2020 between 1 and 1199) under_1200,
  count_if(POP_CENTER_LAT is null or POP_CENTER_LON is null) latlon_null, count_if(POP_CENTER_LON>0) lon_pos,
  min(POP_CENTER_LAT) lat_min, max(POP_CENTER_LAT) lat_max, min(POP_CENTER_LON) lon_min, max(POP_CENTER_LON) lon_max,
  count_if(STATE_FIPS='72') pr_tracts, sum(iff(STATE_FIPS='72',POPULATION_2020,0)) pr_pop,
  count_if(STATE_FIPS in ('60','66','69','78')) island_tracts,
  count_if(TRACT_CE like '99%') ce_99_water, count_if(TRACT_CE like '99%' and POPULATION_2020=0) ce_99_zero,
  count_if(TRACT_CE like '98%') ce_98_special, count_if(TRACT_CE like '98%' and POPULATION_2020=0) ce_98_zero,
  count_if(POPULATION_2020=0 and POP_CENTER_LAT is not null) zero_with_center,
  listagg(distinct iff(STATE_FIPS='09', COUNTY_FIPS, null), ',') ct_counties
from t;

-- [q07] statement 7
-- DIM_TRACT vs DIM_COUNTY: county-code land rate and population agreement, per state (state = left 2 of county code)
with tc as (select COUNTY_FIPS, count(*) tracts, sum(POPULATION_2020) pop from LIBRARY_MARTS.CORE.DIM_TRACT group by 1),
dc as (select COUNTY_FIPS, POPULATION_2020 pop from LIBRARY_MARTS.CORE.DIM_COUNTY),
j as (select coalesce(tc.COUNTY_FIPS, dc.COUNTY_FIPS) cf, tc.COUNTY_FIPS t_cf, dc.COUNTY_FIPS d_cf, tc.pop t_pop, dc.pop d_pop, tc.tracts
      from tc full outer join dc on tc.COUNTY_FIPS = dc.COUNTY_FIPS)
select left(cf,2) st, count(t_cf) tract_counties, count(d_cf) dim_counties,
  count_if(t_cf is not null and d_cf is not null) matched, sum(t_pop) tract_pop, sum(d_pop) county_pop,
  sum(iff(d_cf is null, t_pop, 0)) tract_pop_unmatched, sum(iff(d_cf is null, tracts, 0)) tracts_unmatched,
  count_if(t_cf is not null and d_cf is not null and t_pop<>d_pop) pop_diff_counties,
  listagg(iff(t_cf is null, d_cf, null), ',') dim_only, listagg(iff(d_cf is null, t_cf, null), ',') tract_only
from j group by 1
having count(t_cf)<>count(d_cf) or count_if(t_cf is not null and d_cf is not null)<>count(t_cf)
    or count_if(t_cf is not null and d_cf is not null and t_pop<>d_pop)>0 or left(cf,2) in ('06','09','48')
union all
select 'ALL', count(t_cf), count(d_cf), count_if(t_cf is not null and d_cf is not null), sum(t_pop), sum(d_pop),
  sum(iff(d_cf is null, t_pop, 0)), sum(iff(d_cf is null, tracts, 0)),
  count_if(t_cf is not null and d_cf is not null and t_pop<>d_pop), null, null
from j
order by 1;

-- [q08] statement 8
-- DIM_TRACT outliers: 12 biggest tracts, with their state's median tract and the state's share of tracts over 8,000 (Census aims for 1,200-8,000)
with t as (select * from LIBRARY_MARTS.CORE.DIM_TRACT),
st as (select STATE_FIPS, count(*) tracts, median(POPULATION_2020) st_med, count_if(POPULATION_2020>8000) over8k,
         round(100*count_if(POPULATION_2020>8000)/count(*),1) pct_over8k, count_if(POPULATION_2020>15000) over15k from t group by 1),
top as (select t.TRACT_GEOID, t.POPULATION_2020 pop, t.POP_CENTER_LAT, t.POP_CENTER_LON, c.COUNTY_NAME, c.STATE_NAME
        from t left join LIBRARY_MARTS.CORE.DIM_COUNTY c on c.COUNTY_FIPS = t.COUNTY_FIPS
        order by pop desc limit 12)
select 'top' k, top.TRACT_GEOID a, top.pop::text b, top.COUNTY_NAME||', '||top.STATE_NAME c,
  round(top.POP_CENTER_LAT,4)||','||round(top.POP_CENTER_LON,4) d, st.st_med::text e, round(top.pop/st.st_med,1)::text f
from top join st on st.STATE_FIPS = left(top.TRACT_GEOID,2)
union all
select * from (select 'state_over8k', STATE_FIPS, tracts::text, over8k::text, pct_over8k::text, st_med::text, over15k::text from st order by pct_over8k desc limit 10)
union all
select 'nat', 'all', count(*)::text, count_if(POPULATION_2020>8000)::text, round(100*count_if(POPULATION_2020>8000)/count(*),2)::text,
  median(POPULATION_2020)::text, count_if(POPULATION_2020>15000)::text from t;

-- [q09] statement 9
-- DIM_TRACT: which states carry which VINTAGE, and CT tract-code sample
select VINTAGE, left(TRACT_GEOID,2) st, count(*) tracts, count(distinct COUNTY_FIPS) counties, sum(POPULATION_2020) pop,
  min(TRACT_GEOID) geoid_min, max(TRACT_GEOID) geoid_max
from LIBRARY_MARTS.CORE.DIM_TRACT
group by 1,2 having VINTAGE <> '2020' or left(TRACT_GEOID,2) in ('09','72')
union all
select VINTAGE, 'ALL', count(*), count(distinct COUNTY_FIPS), sum(POPULATION_2020), null, null
from LIBRARY_MARTS.CORE.DIM_TRACT group by 1
order by 1,2;

-- [q10] statement 10
-- One join: FEMA IA registrations (block group -> first 11 digits = tract) to DIM_TRACT. Aggregate FEMA first. Land rate by census vintage, declaration era, CT vs rest
with f as (
  select coalesce(nullif(trim(CENSUS_YEAR),''),'blank') cy,
         year(try_to_timestamp(DECLARATION_DATE::text)) dy,
         iff(DAMAGED_STATE_ABBREVIATION='CT','CT', iff(DAMAGED_STATE_ABBREVIATION='PR','PR','rest')) grp,
         left(CENSUS_GEOID,11) tr, count(*) n
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
  where regexp_like(CENSUS_GEOID, '[0-9]{11,12}(\.0)?')
  group by 1,2,3,4),
g as (
  select cy, case when dy is null then 'nodate' when dy<2012 then 'a<2012' when dy<2022 then 'b2012-21' else 'c2022+' end era, grp,
    sum(n) rows_, count(distinct tr) tracts, sum(iff(d.TRACT_GEOID is not null, n, 0)) rows_landed,
    count(distinct iff(d.TRACT_GEOID is not null, tr, null)) tracts_landed
  from f left join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = f.tr
  group by 1,2,3)
select *, round(100*rows_landed/nullif(rows_,0),1) pct_rows_landed from g
union all
select 'no_geoid', null, null, count(*), null, null, null, null
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where not regexp_like(coalesce(CENSUS_GEOID,''), '[0-9]{11,12}(\.0)?')
order by 1,2,3;

-- [q11] statement 11
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

-- [q12] statement 12
-- Test inside the group: Ian (4673), Maui (4724), LA fires (4856). Per tract: registrations and PEOPLE CLAIMED (sum of household size) vs 2020 residents,
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
        row_number() over (partition by dn order by f.regs/nullif(d.POPULATION_2020,0) desc) rk
      from f join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = f.tr where d.POPULATION_2020 >= 1000)
select dn::text dn, iff(rk<=6, tr, 'rest ('||count(*)||' tracts)') tract, max(iff(rk<=6, city, null)) city,
  sum(pop) pop, sum(regs) regs, sum(people) people_claimed, round(sum(people)/sum(pop),2) people_per_resident,
  round(sum(regs)/sum(pop),2) regs_per_resident, round(sum(people)/nullif(sum(regs)-sum(hh_null),0),2) hh_size,
  round(100*sum(ver_occ)/sum(regs),1) pct_ver_occ, round(100*sum(prim)/sum(regs),1) pct_primary, round(100*sum(renters)/sum(regs),1) pct_rent,
  round(100*sum(elig)/sum(regs),1) pct_elig, round(100*sum(destroyed)/sum(regs),1) pct_destroyed, round(100*sum(insuff)/sum(regs),1) pct_insuff, round(sum(ihp)) ihp
from j group by dn, iff(rk<=6, tr, 'rest ('||count(*)||' tracts)')
order by 1, min(rk);

-- [q12b] statement 13
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

-- [q13] statement 14
-- Dull-explanation test: do the two over-1 tracts soak up geocoder fallbacks? Registrations by 12-digit block group and ZIP,
-- for the two outliers and their burn-zone peers (Lahaina 314.02, 314.05; Fort Myers Beach 601.02).
select DISASTER_NUMBER::text dn, left(CENSUS_GEOID,11) tr, left(CENSUS_GEOID,12) bg, count(distinct REGISTRATION_ID) regs,
  count(distinct DAMAGED_ZIP_CODE) zips, mode(DAMAGED_ZIP_CODE) top_zip, mode(DAMAGED_CITY) top_city,
  round(100*count_if(VERIFIED_OCCUPANCY::text in ('True','true','1'))/count(*),1) pct_ver_occ,
  round(100*count_if(PRIMARY_RESIDENCE::text in ('True','true','1'))/count(*),1) pct_primary,
  round(100*count_if(OWN_RENT='R')/count(*),1) pct_rent, listagg(distinct RESIDENCE_TYPE, '|') res_types,
  mode(RESIDENCE_TYPE) top_res
from LIBRARY_MARTS.HOUSING.HOUSING__FED_FEMA_IA_HOUSING_REGISTRATIONS
where DISASTER_NUMBER::text in ('4673','4724')
  and left(CENSUS_GEOID,11) in ('15009031404','15009031402','15009031405','12071001910','12071060102')
group by 1,2,3 order by 1,2,3;

-- [q14] statement 15
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

-- [q15] statement 16
-- DIM_TRACT key vintage vs the biggest tract-level money table: HMDA historic 2015-2017 (2010 tracts). Aggregate first, then join.
-- Tract = 2-digit state + 3-digit county + 6-digit tract (dot removed). Also shows how STATE_CODE / COUNTY_CODE are written.
with h as (
  select AS_OF_YEAR yr, STATE_CODE, COUNTY_CODE, CENSUS_TRACT_NUMBER, count(*) n
  from LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_HISTORIC group by 1,2,3,4),
k as (select yr, n, STATE_CODE, COUNTY_CODE, CENSUS_TRACT_NUMBER,
        iff(try_to_number(STATE_CODE::text) is not null and try_to_number(COUNTY_CODE::text) is not null and nullif(trim(CENSUS_TRACT_NUMBER::text),'') is not null,
            lpad(try_to_number(STATE_CODE::text)::text,2,'0') || lpad(try_to_number(COUNTY_CODE::text)::text,3,'0')
            || lpad(replace(trim(CENSUS_TRACT_NUMBER::text),'.',''),6,'0'), null) geoid
      from h)
select yr::text yr, iff(left(geoid,2)='09','CT','rest') grp, sum(n) rows_, sum(iff(geoid is null, n, 0)) rows_no_tract,
  sum(iff(d.TRACT_GEOID is not null, n, 0)) rows_landed, round(100*sum(iff(d.TRACT_GEOID is not null, n, 0))/nullif(sum(iff(geoid is not null, n, 0)),0),1) pct_landed_of_coded,
  count(distinct geoid) tracts, count(distinct iff(d.TRACT_GEOID is not null, geoid, null)) tracts_landed,
  any_value(STATE_CODE)::text st_eg, any_value(COUNTY_CODE)::text cty_eg, any_value(CENSUS_TRACT_NUMBER)::text tr_eg
from k left join LIBRARY_MARTS.CORE.DIM_TRACT d on d.TRACT_GEOID = k.geoid
group by 1,2 order by 1,2;

-- [q16] statement 17
-- Spain: re-parse the Spanish text dates properly (year is the 4 digits after the month abbreviation), issued and modified
with t as (select regexp_substr(ISSUED, '[0-9]{1,2} [a-z]{3} ([0-9]{4})', 1, 1, 'e', 1) iy,
                  regexp_substr(MODIFIED, '[0-9]{1,2} [a-z]{3} ([0-9]{4})', 1, 1, 'e', 1) my, SECTOR, PUBLISHER
           from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_ES_DATOSGOB)
select 'issued' k, coalesce(iy,'unparsed') yr, count(*) n from t group by 2
union all select 'modified', coalesce(my,'unparsed'), count(*) from t group by 2
order by 1,2;
