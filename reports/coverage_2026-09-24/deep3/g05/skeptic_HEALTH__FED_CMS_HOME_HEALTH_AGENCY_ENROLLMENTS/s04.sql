-- blind spot of q06: suites or spelled-out suffixes inside ADDRESS_LINE_1 split buildings. Strip them, recount clusters outside CA and state shared-3 rates
with t as (select STATE, ASSOCIATE_ID, left(trim(ZIP_CODE),5) z, upper(trim(ADDRESS_LINE_1)) raw,
             upper(regexp_replace(trim(ADDRESS_LINE_1),'[^A-Za-z0-9 ]','')) a1
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
s as (select *, trim(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(regexp_replace(
         regexp_replace(a1,' (STE|SUITE|UNIT|APT|RM|ROOM|FL|FLOOR|BLDG|BUILDING|OFFICE|OFC|SPC|BOX)( .*)?$',''),
         ' BOULEVARD( |$)',' BLVD\1'),' STREET( |$)',' ST\1'),' AVENUE( |$)',' AVE\1'),' ROAD( |$)',' RD\1'),' DRIVE( |$)',' DR\1'),' PARKWAY( |$)',' PKWY\1'),'  +',' ')) a1s
      from t),
g2 as (select a1s, z, count(distinct ASSOCIATE_ID) orgs, count(distinct a1) spellings, any_value(STATE) st from s group by 1,2),
sj as (select s.STATE, g2.orgs from s join g2 using (a1s, z))
select * from (select 'top_nonCA' k, a1s||' '||z a, st b, orgs n, spellings m from g2 where st<>'CA' order by orgs desc limit 8)
union all select * from (select 'top_CA', a1s||' '||z, st, orgs, spellings from g2 where st='CA' order by orgs desc limit 3)
union all select 'rate_shared3', STATE, round(100*count_if(orgs>=3)/count(*),1)::text, count(*), count_if(orgs>=3) from sj where STATE in ('CA','NV','OH','TX','FL','IL','MN','NY') group by 2
union all select 'rate_shared3', 'US', round(100*count_if(orgs>=3)/count(*),1)::text, count(*), count_if(orgs>=3) from sj
union all select 'suite_in_line1', iff(STATE='CA','CA','nonCA'), null, count(*), count_if(contains(raw,' STE') or contains(raw,'SUITE') or contains(raw,'#') or contains(raw,' UNIT')) from t group by 2
