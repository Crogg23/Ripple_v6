-- [9] geo_vs_census_v2  (rerun of [6], alias fixed; also maps the '00xxx' rows through their own STATE_ABBR)
with cb as (select GEOID, NAME, STUSPS, STATEFP from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY
            where VINTAGE=(select max(VINTAGE) from LIBRARY_MARTS.REFERENCE.REFERENCE__CENSUS_CB_COUNTY)),
st as (select distinct STUSPS, STATEFP from cb),
g as (select g0.FIPS_CODE, g0.FACILITY_COUNT,
             case when regexp_like(g0.FIPS_CODE,'^[0-9]{5}$') and left(g0.FIPS_CODE,2)<>'00' then 'num'
                  when regexp_like(g0.FIPS_CODE,'^[A-Z]{2}[0-9]{3}$') then 'let'
                  when left(g0.FIPS_CODE,2)='00' and regexp_like(g0.FIPS_CODE,'^[0-9]{5}$') then 'z00'
                  else 'other' end form,
             case when form='num' then g0.FIPS_CODE
                  when form='let' then s1.STATEFP||right(g0.FIPS_CODE,3)
                  when form='z00' then s2.STATEFP||right(g0.FIPS_CODE,3) end geoid
      from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY g0
      left join st s1 on s1.STUSPS=left(g0.FIPS_CODE,2)
      left join st s2 on s2.STUSPS=g0.STATE_ABBR),
agg as (select geoid, count_if(form='num') n_num, count_if(form='let') n_let, count_if(form='z00') n_z00, sum(FACILITY_COUNT) fac,
               sum(iff(form='num',FACILITY_COUNT,0)) fac_num
        from g where geoid is not null group by 1)
select case when cb.GEOID is null then 'dim_only_not_census'
            when agg.geoid is null then 'census_county_missing'
            else iff(n_num>0,'N','-')||iff(n_let>0,'L','-')||iff(n_z00>0,'Z','-') end bucket,
       count(*) n, sum(agg.fac) fac, sum(agg.fac_num) fac_on_numeric_row,
       max(n_num) max_num_rows, max(n_let) max_let_rows,
       (select count(*) from cb) census_counties,
       (select count(*) from g where geoid is null) dim_rows_unmapped,
       array_slice(array_agg(coalesce(cb.GEOID,agg.geoid)||' '||coalesce(cb.NAME,'')||' '||coalesce(cb.STUSPS,'')||' fac='||coalesce(agg.fac::string,'')),0,40) smp
from cb full outer join agg on agg.geoid=cb.GEOID group by 1 order by 2 desc;

-- [10] geo_split_examples  (every row that could be San Diego, Harris, Hillsborough FL, Maricopa, Prince George's)
select FIPS_CODE, STATE_FIPS, COUNTY_NAME, STATE_ABBR, STATE_NAME, EPA_REGION, FACILITY_COUNT, CENTROID_LATITUDE, CENTROID_LONGITUDE
from LIBRARY_MARTS.REFERENCE.REF__DIM_GEOGRAPHY
where FIPS_CODE in ('06073','CA073','00073','48201','TX201','00201','12057','FL057','00057','04013','AZ013','00013','24033','MD033','00033')
   or (upper(COUNTY_NAME) like '%HILLSB%' and STATE_ABBR='FL')
   or (upper(COUNTY_NAME) like 'SAN DIEGO%') or (upper(COUNTY_NAME) like 'HARRIS%' and STATE_ABBR='TX')
order by right(FIPS_CODE,3), FIPS_CODE;

-- [11] fda_unii_itis_join  (the one warehouse table with an ITIS key: does it land, and on current names?)
with f0 as (select ITIS_TSN from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_UNII_GSRS_SUBSTANCES),
f as (select distinct try_to_number(trim(ITIS_TSN)) tsn from f0 where try_to_number(trim(ITIS_TSN)) is not null)
select (select count(*) from f0) fda_rows,
       (select count_if(nullif(nullif(trim(ITIS_TSN),''),'None') is not null) from f0) fda_rows_with_tsn,
       (select count_if(nullif(nullif(trim(ITIS_TSN),''),'None') is not null and try_to_number(trim(ITIS_TSN)) is null) from f0) tsn_not_numeric,
       count(*) distinct_tsn, count(u.TSN) landed,
       count_if(u.NAME_USAGE in ('valid','accepted')) current_name, count_if(u.NAME_USAGE in ('invalid','not accepted')) retired_name,
       array_slice(array_agg(iff(u.NAME_USAGE in ('invalid','not accepted'), u.COMPLETE_NAME||' ['||coalesce(u.UNACCEPT_REASON,'')||']', null)),0,12) retired_sample
from f left join LIBRARY_MARTS.REFERENCE.REFERENCE__FED_ITIS_TAXONOMIC_UNITS u on u.TSN=f.tsn;
