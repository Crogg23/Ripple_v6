-- [1] itis_lookup_shape  (per table: rows, distinct TSN, then table-specific columns c1..c5 as labeled)
select 'REFERENCE_LINKS' t, count(*) n, count(distinct TSN) d_tsn,
       count(distinct ITIS_REFERENCE_LINKS_KEY) c1_d_key, count_if(VERNACULAR_NAME='None') c2_vern_none,
       count_if(CHANGE_TRACK_ID=0) c3_ctid0, min(UPDATE_DATE)::string c4_min, max(UPDATE_DATE)::string c5_max,
       count(distinct _SOURCE_RUN_ID) runs
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS
union all
select 'LONGNAMES', count(*), count(distinct TSN), count(distinct COMPLETE_NAME), count_if(COMPLETE_NAME is null or COMPLETE_NAME in ('','None')),
       null, null, null, count(distinct _SOURCE_RUN_ID)
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_LONGNAMES
union all
select 'TAXONOMIC_UNITS', count(*), count(distinct TSN), count(distinct COMPLETE_NAME), count_if(NAME_USAGE in ('valid','accepted')),
       count_if(PARENT_TSN=0), min(INITIAL_TIME_STAMP)::string, max(INITIAL_TIME_STAMP)::string, count(distinct _SOURCE_RUN_ID)
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS
union all
select 'HIERARCHY', count(*), count(distinct TSN), count(distinct HIERARCHY_STRING), max(HIERARCHY_LEVEL),
       count_if(PARENT_TSN=0), sum(CHILDREN_COUNT)::string, count_if(CHILDREN_COUNT=0)::string, count(distinct _SOURCE_RUN_ID)
from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_HIERARCHY;

-- [2] itis_cross_table  (every TAXONOMIC_UNITS name: does it sit in LONGNAMES with the same name, in HIERARCHY, and have reference links)
with t as (select TSN, NAME_USAGE, COMPLETE_NAME from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS),
l as (select TSN, any_value(COMPLETE_NAME) nm from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_LONGNAMES group by 1),
h as (select TSN, count(*) k from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_HIERARCHY group by 1),
r as (select TSN, count(*) links from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS group by 1)
select t.NAME_USAGE, count(*) n, count(l.TSN) in_longnames, count_if(l.nm = t.COMPLETE_NAME) same_name,
       count(h.TSN) in_hierarchy, count(r.TSN) has_links, sum(coalesce(r.links,0)) links
from t left join l on l.TSN=t.TSN left join h on h.TSN=t.TSN left join r on r.TSN=t.TSN
group by 1 order by 2 desc;

-- [3] itis_orphans  (TSNs in the child tables that are not in TAXONOMIC_UNITS)
select 'links_tsn_not_in_units' what, count(*) n
from (select distinct TSN from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS) r
where not exists (select 1 from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS u where u.TSN=r.TSN)
union all
select 'hierarchy_tsn_not_in_units', count(*)
from (select distinct TSN from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_HIERARCHY) h
where not exists (select 1 from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS u where u.TSN=h.TSN)
union all
select 'longnames_tsn_not_in_units', count(*)
from (select distinct TSN from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_LONGNAMES) l
where not exists (select 1 from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS u where u.TSN=l.TSN);

-- [4] itis_time  (new names by creation year, last-update year, reference-link update year; Jan-Jul share for a fair 2026 compare)
with a as (select year(INITIAL_TIME_STAMP) yr, count(*) new_names, count_if(month(INITIAL_TIME_STAMP)<=7) new_jan_jul,
                  count_if(NAME_USAGE in ('valid','accepted')) new_accepted
           from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS group by 1),
b as (select year(UPDATE_DATE) yr, count(*) upd, count_if(month(UPDATE_DATE)<=7) upd_jan_jul
      from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS group by 1),
r as (select year(UPDATE_DATE) yr, count(*) links, count_if(month(UPDATE_DATE)<=7) links_jan_jul
      from LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_REFERENCE_LINKS group by 1)
select coalesce(a.yr,b.yr,r.yr) yr, a.new_names, a.new_jan_jul, a.new_accepted, b.upd, b.upd_jan_jul, r.links, r.links_jan_jul
from a full outer join b on b.yr=a.yr full outer join r on r.yr=coalesce(a.yr,b.yr)
order by 1;

-- [5] geo_forms  (what shapes FIPS_CODE comes in, and the facilities each shape carries)
select case when regexp_like(FIPS_CODE,'^[0-9]{5}$') and STATE_FIPS<>'00' then 'numeric_5'
            when regexp_like(FIPS_CODE,'^[A-Z]{2}[0-9]{3}$') then 'letters_plus_3'
            when STATE_FIPS='00' then 'state_00'
            else 'other' end form,
       count(*) n, sum(FACILITY_COUNT) fac, median(FACILITY_COUNT) med_fac, count(distinct STATE_ABBR) states,
       min(FIPS_CODE) mn, max(FIPS_CODE) mx,
       array_slice(array_agg(FIPS_CODE||':'||coalesce(COUNTY_NAME,'')||':'||coalesce(STATE_ABBR,'')||':'||FACILITY_COUNT)
                   within group (order by FACILITY_COUNT desc),0,8) top8
from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY group by 1 order by 2 desc;

-- [6] geo_vs_census  (map each dim row to a Census county GEOID; letter codes via the Census state abbreviation)
with cb as (select GEOID, NAME, STUSPS, STATEFP from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY
            where VINTAGE=(select max(VINTAGE) from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY)),
st as (select distinct STUSPS, STATEFP from cb),
g as (select g0.FIPS_CODE, g0.FACILITY_COUNT,
             iff(regexp_like(g0.FIPS_CODE,'^[0-9]{5}$'),'num',iff(regexp_like(g0.FIPS_CODE,'^[A-Z]{2}[0-9]{3}$'),'let','other')) form,
             case when form='num' then g0.FIPS_CODE when form='let' then st.STATEFP||right(g0.FIPS_CODE,3) end geoid
      from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY g0 left join st on st.STUSPS=left(g0.FIPS_CODE,2)),
agg as (select geoid, count_if(form='num') n_num, count_if(form='let') n_let, sum(FACILITY_COUNT) fac,
               sum(iff(form='let',FACILITY_COUNT,0)) fac_let
        from g where geoid is not null group by 1)
select case when cb.GEOID is null then 'dim_only_not_census' when agg.geoid is null then 'census_county_missing'
            when n_num>0 and n_let>0 then 'both_forms' when n_num>0 then 'numeric_only' else 'letter_only' end bucket,
       count(*) n, sum(agg.fac) fac, sum(agg.fac_let) fac_on_letter_rows,
       (select count(*) from cb) census_counties, (select count(*) from g where geoid is null) dim_rows_unmapped,
       array_slice(array_agg(coalesce(cb.GEOID,agg.geoid)||' '||coalesce(cb.NAME,'')||' '||coalesce(cb.STUSPS,'')||' '||coalesce(agg.fac::string,'')),0,40) sample
from cb full outer join agg on agg.geoid=cb.GEOID group by 1 order by 2 desc;

-- [7] geo_centroid_and_name_check  (dim centroid vs Census polygon centroid, and county name agreement, by form)
with cb as (select GEOID, NAME, STUSPS, STATEFP, GEOMETRY from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY
            where VINTAGE=(select max(VINTAGE) from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY)),
st as (select distinct STUSPS, STATEFP from cb),
g as (select g0.*,
             iff(regexp_like(g0.FIPS_CODE,'^[0-9]{5}$'),'num',iff(regexp_like(g0.FIPS_CODE,'^[A-Z]{2}[0-9]{3}$'),'let','other')) form,
             case when form='num' then g0.FIPS_CODE when form='let' then st.STATEFP||right(g0.FIPS_CODE,3) end geoid
      from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY g0 left join st on st.STUSPS=left(g0.FIPS_CODE,2)),
j as (select g.form, g.FIPS_CODE, g.COUNTY_NAME, g.STATE_ABBR, g.FACILITY_COUNT, cb.NAME cb_name, cb.STUSPS,
             iff(g.CENTROID_LONGITUDE is null, null,
                 st_distance(st_centroid(cb.GEOMETRY), st_makepoint(g.CENTROID_LONGITUDE, g.CENTROID_LATITUDE))/1000) km_off,
             contains(upper(coalesce(g.COUNTY_NAME,'')), upper(cb.NAME)) name_ok,
             coalesce(g.STATE_ABBR,'')=cb.STUSPS state_ok
      from g join cb on cb.GEOID=g.geoid)
select form, count(*) n, count_if(km_off<25) lt25, count_if(km_off>=25 and km_off<100) km25_100,
       count_if(km_off>=100 and km_off<500) km100_500, count_if(km_off>=500) km500plus, count_if(km_off is null) no_centroid,
       median(km_off) med_km, count_if(not name_ok) name_mismatch, count_if(not state_ok) state_mismatch,
       array_slice(array_agg(FIPS_CODE||' '||coalesce(COUNTY_NAME,'')||'/'||cb_name||' '||coalesce(STATE_ABBR,'')||'/'||STUSPS||' km='||round(km_off)||' fac='||FACILITY_COUNT)
                   within group (order by km_off desc nulls last),0,10) worst10
from j group by 1 order by 2 desc;

-- [8] geo_top_counties  (the biggest FACILITY_COUNT rows: real counties or code debris?)
select FIPS_CODE, STATE_FIPS, COUNTY_NAME, STATE_ABBR, STATE_NAME, EPA_REGION, FACILITY_COUNT, CENTROID_LATITUDE, CENTROID_LONGITUDE
from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY order by FACILITY_COUNT desc limit 25;
