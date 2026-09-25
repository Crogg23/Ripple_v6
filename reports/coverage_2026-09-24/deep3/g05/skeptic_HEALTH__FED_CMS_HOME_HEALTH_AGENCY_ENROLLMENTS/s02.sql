-- headline re-derivation: rows vs CCN vs org (ASSOCIATE_ID) vs org name, branches, by Valley ZIP3 912-916 and era; zip hygiene; id dates
with t as (select CCN, ASSOCIATE_ID, upper(trim(ORGANIZATION_NAME)) org, STATE, trim(ZIP_CODE) zip, left(trim(ZIP_CODE),3) z3,
             PRACTICE_LOCATION_TYPE plt, MULTIPLE_NPI_FLAG mnf, ENROLLMENT_ID, try_to_date(substr(ENROLLMENT_ID,2,8),'YYYYMMDD') d
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS),
r as (select *, iff(STATE='CA' and z3 between '912' and '916','valley','rest') rg,
        case when year(d)<2013 then 'a_pre2013' when year(d)<2019 then 'b_2013_18' else 'c_2019on' end era from t)
select 'grp' k, rg a, era b, count(*) n, count(distinct CCN) ccn, count(distinct ASSOCIATE_ID) assoc, count(distinct org) orgs, count_if(plt='HHA BRANCH') branch, count_if(mnf='Y') multinpi from r group by 2,3
union all select 'nat', 'all', era, count(*), count(distinct CCN), count(distinct ASSOCIATE_ID), count(distinct org), count_if(plt='HHA BRANCH'), count_if(mnf='Y') from r group by 3
union all select 'ziplen', length(zip)::text, iff(STATE='CA','CA','nonCA'), count(*), count_if(z3 between '912' and '916'), count_if(not regexp_like(zip,'^[0-9]+$')), null, null, null from r group by 2,3
union all select 'z3_912_916_notCA', STATE, z3, count(*), null, null, null, null, null from r where z3 between '912' and '916' and STATE<>'CA' group by 2,3
union all select 'dates', min(d)::text, max(d)::text, count_if(d is null), count_if(d>current_date()), count_if(left(ENROLLMENT_ID,1)<>'O'), count(*)-count(distinct ENROLLMENT_ID), null, null from r
union all select 'org_dupe_names_2019on', rg, null, count(*), count(distinct org), null, null, null, null from r where era='c_2019on' group by 2
order by 1,2,3
