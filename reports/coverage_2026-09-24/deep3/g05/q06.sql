-- HHA: street addresses shared by 3+ different organizations (distinct ASSOCIATE_ID); share by state, then the top addresses
with t as (select CCN, ASSOCIATE_ID, ORGANIZATION_NAME, STATE,
             upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1, left(ZIP_CODE,5) z, upper(CITY) city,
             try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') enr_dt
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
g as (select a1, z, count(*) n, count(distinct ASSOCIATE_ID) orgs from t group by 1,2),
tt as (select t.*, g.orgs from t join g using (a1, z)),
st as (select STATE, count(*) agencies, count_if(orgs>=3) at_shared3, count_if(orgs>=2) at_shared2 from tt group by 1),
top as (select a1, z, any_value(city) city, any_value(STATE) st, count(*) n, max(orgs) orgs, min(enr_dt) first_enr, max(enr_dt) last_enr,
          listagg(distinct left(ORGANIZATION_NAME,28), '; ') names
        from tt where orgs>=3 group by 1,2 order by orgs desc, n desc limit 25)
select 'nat' k, null a, sum(agencies)::text b, sum(at_shared3)::text c, sum(at_shared2)::text d, null e, null f, null g, null h from st
union all select * from (select 'state', STATE, agencies::text, at_shared3::text, at_shared2::text, round(100*at_shared3/agencies,1)::text, null, null, null
  from st where agencies>=100 order by at_shared3/agencies desc limit 15)
union all select 'addr', a1||' '||z, city, st, n::text, orgs::text, first_enr::text, last_enr::text, names from top
