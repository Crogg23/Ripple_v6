-- deep3 / g71: proper look at five open-data catalog tables, 2026-09-24
-- Tables: OPEN_DATA__INTL_GR_DATAGOV, OPEN_DATA__INTL_FR_DATA_GOUV, OPEN_DATA__INTL_AR_DATOSGOB,
--         OPEN_DATA__INTL_DE_GOVDATA, OPEN_DATA__INTL_CL_DATOSGOB
-- Door: Python (connect/db.py) via g71/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g71/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- Column names and types for all five tables, plus catalog row counts
select c.TABLE_NAME, t.ROW_COUNT, listagg(c.COLUMN_NAME || ':' || c.DATA_TYPE, ', ') within group (order by c.ORDINAL_POSITION) cols
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS c
join LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES t on t.TABLE_SCHEMA=c.TABLE_SCHEMA and t.TABLE_NAME=c.TABLE_NAME
where c.TABLE_SCHEMA='OPEN_DATA' and c.TABLE_NAME in ('OPEN_DATA__INTL_GR_DATAGOV','OPEN_DATA__INTL_FR_DATA_GOUV','OPEN_DATA__INTL_AR_DATOSGOB','OPEN_DATA__INTL_DE_GOVDATA','OPEN_DATA__INTL_CL_DATOSGOB')
group by 1,2 order by 1;

-- [q02] statement 2
-- France: profile. Key uniqueness, archived, owners, dates out of range, usage counters, harvest share
select count(*) n, count(distinct DATASET_ID) ids, count(distinct SLUG) slugs,
  count_if(ARCHIVED is null or ARCHIVED in ('','False','false')) live_rows, count_if(ARCHIVED not in ('','False','false') and ARCHIVED is not null) archived_rows,
  min(iff(ARCHIVED not in ('','False','false'), ARCHIVED, null)) arch_min, max(iff(ARCHIVED not in ('','False','false'), ARCHIVED, null)) arch_max,
  count_if(ORGANIZATION_NAME is null or ORGANIZATION_NAME in ('','None')) org_blank, count_if(OWNER like 'deleted%') owner_deleted,
  count_if(year(CREATED_AT)<1990) created_pre1990, count_if(CREATED_AT>'2026-08-12') created_future, min(CREATED_AT) cmin, max(CREATED_AT) cmax,
  count_if(LAST_MODIFIED>'2026-08-12') mod_future,
  count_if(NB_VIEWS is null) views_null, count_if(NB_VIEWS=0) views0, median(NB_VIEWS) views_med, sum(NB_VIEWS) views_sum, max(NB_VIEWS) views_max,
  count_if(NB_RESOURCE_DOWNLOADS is null) dl_null, count_if(NB_RESOURCE_DOWNLOADS=0) dl0, median(NB_RESOURCE_DOWNLOADS) dl_med, sum(NB_RESOURCE_DOWNLOADS) dl_sum, max(NB_RESOURCE_DOWNLOADS) dl_max,
  count_if(NB_RESOURCES=0) res0, count_if(HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harvested,
  min(QUALITY_SCORE) qmin, median(QUALITY_SCORE) qmed, max(QUALITY_SCORE) qmax, count(distinct ORGANIZATION_ID) orgs
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV;

-- [q03] statement 3
-- France: ARCHIVED raw values (top 15) to learn the format before parsing
select ARCHIVED, count(*) n from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV group by 1 order by 2 desc limit 15;

-- [q04] statement 4
-- France: archiving over time. Month of ARCHIVED (parsed), harvested vs native, distinct orgs, top org share
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, iff(HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'', 'harv', 'native') src
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV where ARCHIVED not in ('False','false',''))
, m as (select to_char(date_trunc('month', arch_ts),'YYYY-MM') mon, ORGANIZATION_NAME org, count(*) n from t group by 1,2)
, top as (select mon, org, n, row_number() over (partition by mon order by n desc) rk from m)
select to_char(date_trunc('month', t.arch_ts),'YYYY-MM') mon, count(*) n, count_if(src='harv') harv, count_if(src='native') native,
  count(distinct t.ORGANIZATION_NAME) orgs, count_if(arch_ts is null) unparsed,
  max(iff(top.rk=1, top.org||' '||top.n, null)) top_org
from t left join top on top.mon=to_char(date_trunc('month', t.arch_ts),'YYYY-MM') and top.rk=1
group by 1 order by 1;

-- [q05] statement 5
-- France: the big archive events (org-month with 300+ archived). Did the same org create a like number of new datasets
-- in that month or the next (re-harvest churn = dull), and how many live datasets does it hold now?
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, (HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harv
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, ev as (select coalesce(ORGANIZATION_NAME,'(no org)') org, date_trunc('month', arch_ts) mon, count(*) arch_n, count_if(harv) arch_harv,
         min(arch_ts)::date first_day, max(arch_ts)::date last_day, count(distinct arch_ts::date) days,
         sum(NB_RESOURCE_DOWNLOADS) arch_dl, median(NB_RESOURCE_DOWNLOADS) arch_dl_med, min(CREATED_AT)::date cr_min, max(CREATED_AT)::date cr_max
       from t where arch_ts is not null group by 1,2 having count(*)>=300)
select ev.org, to_char(ev.mon,'YYYY-MM') mon, arch_n, arch_harv, first_day, last_day, days, cr_min, cr_max, arch_dl, arch_dl_med,
  (select count(*) from t t2 where coalesce(t2.ORGANIZATION_NAME,'(no org)')=ev.org and t2.CREATED_AT >= ev.mon and t2.CREATED_AT < dateadd(month,2,ev.mon)) created_same_2mo,
  (select count(*) from t t3 where coalesce(t3.ORGANIZATION_NAME,'(no org)')=ev.org and t3.arch_ts is null) live_now
from ev order by arch_n desc;

-- [q06] statement 6
-- France: March 2024 archive wave by day, harvested flag, org families (DDT/DDTM/DREAL/other), downloads
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
select arch_ts::date d, count(*) n, count(distinct ORGANIZATION_NAME) orgs,
  count_if(ORGANIZATION_NAME ilike 'Direction D%partementale%' or ORGANIZATION_NAME ilike 'DDT%') ddt,
  count_if(ORGANIZATION_NAME ilike 'DREAL%' or ORGANIZATION_NAME ilike 'Direction R%gionale%') dreal,
  count_if(RESOURCES_FORMATS ilike '%ogc:w%' or RESOURCES_FORMATS ilike '%wms%' or RESOURCES_FORMATS ilike '%wfs%') ogc,
  min(CREATED_AT)::date cr_min, median(year(CREATED_AT)) cr_med_year, max(CREATED_AT)::date cr_max,
  sum(NB_RESOURCE_DOWNLOADS) dl_sum, median(NB_RESOURCE_DOWNLOADS) dl_med, sum(NB_REUSES) reuses,
  any_value(TITLE) sample_title
from t where arch_ts >= '2024-03-01' and arch_ts < '2024-04-01' group by 1 order by 2 desc limit 12;

-- [q07] statement 7
-- France: the dull test. For each big archive event, how many archived titles have a LIVE twin
-- (same org + same normalized title), and when was the twin created? Replaced = housekeeping; no twin = gone from the portal.
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, coalesce(ORGANIZATION_NAME,'(no org)') org
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live as (select org, nt, min(CREATED_AT) twin_created, count(*) k from t where arch_ts is null and ARCHIVED='False' group by 1,2)
, ev as (select org, date_trunc('month', arch_ts) mon from t where arch_ts is not null group by 1,2 having count(*)>=300)
, a as (select t.org, to_char(date_trunc('month', t.arch_ts),'YYYY-MM') mon, t.nt, t.NB_RESOURCE_DOWNLOADS dl, l.twin_created
        from t join ev on ev.org=t.org and ev.mon=date_trunc('month', t.arch_ts) left join live l on l.org=t.org and l.nt=t.nt)
select org, mon, count(*) arch_n, count_if(twin_created is not null) with_live_twin,
  round(100*count_if(twin_created is not null)/count(*),1) twin_pct,
  min(twin_created)::date twin_first, median(year(twin_created)) twin_med_year, max(twin_created)::date twin_last,
  sum(iff(twin_created is null, dl, 0)) dl_on_untwinned
from a group by 1,2 order by arch_n desc limit 25;

-- [q08] statement 8
-- France: the no-twin archive events. Twin under ANY publisher (not just same org), owner for no-org rows, sample titles
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, coalesce(ORGANIZATION_NAME,'(no org)') org
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live as (select nt, min(CREATED_AT) c, listagg(distinct org, '; ') within group (order by org) orgs from t where ARCHIVED='False' group by 1)
, a as (select t.*, l.c twin_created, l.orgs twin_orgs from t left join live l on l.nt=t.nt
        where (t.org='Région Hauts-de-France' and t.arch_ts>='2026-06-01' and t.arch_ts<'2026-07-01')
           or (t.org='Région GRAND EST' and t.arch_ts>='2026-08-01')
           or (t.org='(no org)' and t.arch_ts>='2025-01-01' and t.arch_ts<'2025-02-01')
           or (t.org like 'Communaut% du Saint-Quentinois' and t.arch_ts>='2024-06-01' and t.arch_ts<'2024-07-01'))
select org, count(*) n, count_if(twin_created is not null) twin_any, left(any_value(iff(twin_created is not null and twin_orgs<>org, twin_orgs, null)),120) other_org_twin,
  count(distinct OWNER) owners, left(listagg(distinct OWNER, '; '),200) owner_list, count_if(OWNER like 'deleted%') owner_deleted,
  count(distinct split_part(HARVEST_REMOTE_URL,'/',3)) harvest_hosts, left(listagg(distinct split_part(HARVEST_REMOTE_URL,'/',3), '; '),200) hosts,
  left(listagg(distinct left(TITLE,50), ' || ') within group (order by left(TITLE,50)),500) titles
from a group by 1;

-- [q09] statement 9
-- France: usage concentration on LIVE datasets (downloads), harvested vs native, plus the top 8 by downloads and the date sentinels
with t as (select *, (HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harv from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV where ARCHIVED='False')
, r as (select *, row_number() over (order by NB_RESOURCE_DOWNLOADS desc nulls last) rk, sum(NB_RESOURCE_DOWNLOADS) over () tot from t)
select 'split' k, iff(harv,'harvested','native') a, count(*)::text b, median(NB_RESOURCE_DOWNLOADS)::text c, count_if(coalesce(NB_RESOURCE_DOWNLOADS,0)=0)::text d,
  count_if(coalesce(NB_RESOURCE_DOWNLOADS,0)<10)::text e, round(100*sum(NB_RESOURCE_DOWNLOADS)/any_value(tot),1)::text f, median(NB_VIEWS)::text g
from r group by 2
union all select 'top', left(TITLE,70), coalesce(ORGANIZATION_NAME, OWNER), NB_RESOURCE_DOWNLOADS::text, NB_VIEWS::text, CREATED_AT::date::text, round(100*NB_RESOURCE_DOWNLOADS/tot,2)::text, rk::text from r where rk<=8
union all select 'top10share', null, null, round(100*sum(iff(rk<=10,NB_RESOURCE_DOWNLOADS,0))/any_value(tot),1)::text, round(100*sum(iff(rk<=100,NB_RESOURCE_DOWNLOADS,0))/any_value(tot),1)::text, any_value(tot)::text, null, count(*)::text from r
union all select 'datesent', left(TITLE,70), coalesce(ORGANIZATION_NAME, OWNER), CREATED_AT::text, harv::text, ARCHIVED, null, null
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV x, lateral (select (x.HARVEST_REMOTE_URL is not null and x.HARVEST_REMOTE_URL<>'') harv)
where year(CREATED_AT)<1970 or CREATED_AT>'2026-08-12';

-- [q10] statement 10
-- Greece: profile. Key uniqueness, date span, fill rates, placeholder descriptions, flags, languages, sample-source URL
select count(*) n, count(distinct DATASET_ID) ids, count(distinct lower(trim(TITLE))) titles, count(distinct ORGANISATION_ID) org_ids, count(distinct ORGANISATION_NAME) org_names,
  min(DATE_CREATED) c_min, max(DATE_CREATED) c_max, count(distinct DATE_CREATED::date) c_days,
  min(METADATA_MODIFIED) m_min, max(METADATA_MODIFIED) m_max,
  count_if(DESCRIPTION like 'Δεν παρέχεται%') desc_none, count_if(DESCRIPTION is null or DESCRIPTION='') desc_blank,
  count_if(IS_HVD is not null and IS_HVD not in ('','[]')) hvd, count_if(THEMATIC_CATEGORY is not null and THEMATIC_CATEGORY not in ('','[]')) theme,
  count_if(LICENSE_ID is not null and LICENSE_ID<>'') lic, listagg(distinct LICENSE_ID, '|') lic_vals,
  count_if(TAGS is null or TAGS in ('','[]')) tags_blank, count_if(NUM_RESOURCES=0) res0, max(NUM_RESOURCES) res_max, sum(NUM_RESOURCES) res_sum,
  left(listagg(distinct LANGUAGE, ' | '),300) langs, count(distinct _SOURCE_URL) src_urls, left(listagg(distinct _SOURCE_URL, ' | '),300) src, count(distinct _LOADED_AT) loads
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV;

-- [q11] statement 11
-- Greece: creation by day (the migration-date test), top 12 days with orgs and top org
with d as (select DATE_CREATED::date d, ORGANISATION_NAME o, count(*) n from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV group by 1,2)
, r as (select *, row_number() over (partition by d order by n desc) rk from d)
select d, sum(n) n, count(*) orgs, max(iff(rk=1, o||' '||n, null)) top_org from r group by 1 order by n desc limit 12;

-- [q12] statement 12
-- Greece: padding check. Per top org: datasets, distinct titles, share whose files are only map-service links (WMS/WFS), median files
select ORGANISATION_NAME org, count(*) n, count(distinct lower(trim(TITLE))) titles,
  count_if(RESOURCE_FORMATS ilike '%WMS%' or RESOURCE_FORMATS ilike '%WFS%') map_svc, count_if(RESOURCE_FORMATS ilike '%CSV%' or RESOURCE_FORMATS ilike '%XLS%' or RESOURCE_FORMATS ilike '%JSON%') tabular,
  median(NUM_RESOURCES) med_files, min(DATE_CREATED)::date first_c, max(DATE_CREATED)::date last_c, count(distinct DATE_CREATED::date) days,
  count_if(DESCRIPTION like 'Δεν παρέχεται%') no_desc, left(any_value(TITLE),60) sample_title
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV group by 1 order by 2 desc limit 10;

-- [q13] statement 13
-- Germany: profile. Keys, date spans, fill rates, HVD, publishers, source URL, load count
select count(*) n, count(distinct DATASET_ID) ids, count(distinct NAME) names, count(distinct lower(trim(TITLE))) titles, count(distinct PUBLISHER) pubs,
  min(METADATA_CREATED) c_min, max(METADATA_CREATED) c_max, min(METADATA_MODIFIED) m_min, max(METADATA_MODIFIED) m_max,
  count_if(TEMPORAL_START is not null) t_start, min(TEMPORAL_START) ts_min, max(TEMPORAL_END) te_max,
  count_if(IS_HVD is not null and IS_HVD not in ('','[]','null')) hvd, count_if(LICENSE_ID is not null and LICENSE_ID<>'') lic,
  count_if(SPATIAL is not null and SPATIAL not in ('','null')) spatial, count_if(RESOURCES is null or RESOURCES in ('','[]')) res_blank,
  count_if(PUBLISHER is null or PUBLISHER='') pub_blank, count(distinct _SOURCE_URL) src_n, left(listagg(distinct _SOURCE_URL,' | '),200) src, count(distinct _LOADED_AT) loads
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA;

-- [q14] statement 14
-- Chile: profile. Keys, date spans, fills, publishers, STATE values, formats, source URL
select count(*) n, count(distinct DATASET_ID) ids, count(distinct NAME) names, count(distinct lower(trim(TITLE))) titles, count(distinct PUBLISHER_INSTITUTION) pubs,
  min(METADATA_CREATED) c_min, max(METADATA_CREATED) c_max, min(METADATA_MODIFIED) m_min, max(METADATA_MODIFIED) m_max,
  listagg(distinct STATE,'|') states, count_if(CATEGORY is not null and CATEGORY<>'') cat, count_if(LICENSE_ID is not null and LICENSE_ID<>'') lic, left(listagg(distinct LICENSE_ID,'|'),200) lics,
  count_if(NUM_RESOURCES=0) res0, median(NUM_RESOURCES) res_med, max(NUM_RESOURCES) res_max,
  count_if(DESCRIPTION is null or DESCRIPTION='') desc_blank, count(distinct _SOURCE_URL) src_n, left(listagg(distinct _SOURCE_URL,' | '),200) src, count(distinct _LOADED_AT) loads
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB;

-- [q15] statement 15
-- Argentina: profile. Grain (dataset vs file), orgs, formats, LAST_MODIFIED text parse, empty columns, geo codes
select count(*) n, count(distinct DATASET_ID) ids, count(distinct RESOURCE_URL) urls, count(distinct DATASET_ID||'|'||RESOURCE_URL) id_url,
  count(distinct lower(trim(DATASET_TITLE))) titles, count(distinct C_ORGANIZATION) orgs,
  count_if(LAST_MODIFIED is null or trim(LAST_MODIFIED)='') lm_blank, count_if(try_to_timestamp(LAST_MODIFIED) is null and trim(LAST_MODIFIED)<>'') lm_unparsed,
  min(try_to_timestamp(LAST_MODIFIED)) lm_min, max(try_to_timestamp(LAST_MODIFIED)) lm_max,
  count_if(SERIE_ID is not null and SERIE_ID<>'') serie, count_if(PROVINCIA_ID is not null and PROVINCIA_ID<>'') prov, count_if(MUNICIPIO_ID is not null and MUNICIPIO_ID<>'') muni,
  count_if(C_ORGANIZATION is null or trim(C_ORGANIZATION)='') org_blank, count_if(DESCRIPTION is null or DESCRIPTION='') desc_blank,
  count_if(RESOURCE_URL ilike '%datos.gob.ar%') url_portal, count_if(RESOURCE_URL ilike '%infra.datos.gob.ar%') url_infra
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB;

-- [q16] statement 16
-- Sample-order test for the three capped tables: how was the slice chosen? Load date, modified-date spread, name order
select 'DE' t, to_timestamp(max(_LOADED_AT)/1000000)::date loaded, min(NAME) name_min, max(NAME) name_max,
  percentile_cont(0.1) within group (order by METADATA_MODIFIED::date::int) p10_dummy,
  min(METADATA_MODIFIED)::date m_min, (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA order by METADATA_MODIFIED limit 1 offset 2500) m_median,
  max(METADATA_MODIFIED)::date m_max, count_if(year(METADATA_MODIFIED)=2025) m_2025, count_if(year(METADATA_CREATED)=2025) c_2025, count(distinct PUBLISHER) pubs
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
union all
select 'CL', to_timestamp(max(_LOADED_AT)/1000000)::date, min(NAME), max(NAME), null, min(METADATA_MODIFIED)::date,
  (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB order by METADATA_MODIFIED limit 1 offset 500),
  max(METADATA_MODIFIED)::date, count_if(year(METADATA_MODIFIED)=2026), count_if(year(METADATA_CREATED)=2026), count(distinct PUBLISHER_INSTITUTION)
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
union all
select 'GR', to_timestamp(max(_LOADED_AT)/1000000)::date, min(TITLE), max(TITLE), null, min(METADATA_MODIFIED)::date,
  (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV order by METADATA_MODIFIED limit 1 offset 2494),
  max(METADATA_MODIFIED)::date, count_if(year(METADATA_MODIFIED)=2026), count_if(year(DATE_CREATED)=2026), count(distinct ORGANISATION_NAME)
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV;

-- [q17] statement 17
-- (rerun of q16 after a compile error) Sample-order test for the three capped tables: how was the slice chosen? Load date, modified-date spread, name order
select 'DE' t, to_timestamp(max(_LOADED_AT)/1000000)::date loaded, min(NAME) name_min, max(NAME) name_max,
  min(METADATA_MODIFIED)::date m_min, (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA order by METADATA_MODIFIED limit 1 offset 2500) m_median,
  max(METADATA_MODIFIED)::date m_max, count_if(year(METADATA_MODIFIED)=2025) m_2025, count_if(year(METADATA_CREATED)=2025) c_2025, count(distinct PUBLISHER) pubs
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
union all
select 'CL', to_timestamp(max(_LOADED_AT)/1000000)::date, min(NAME), max(NAME), min(METADATA_MODIFIED)::date,
  (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB order by METADATA_MODIFIED limit 1 offset 500),
  max(METADATA_MODIFIED)::date, count_if(year(METADATA_MODIFIED)=2026), count_if(year(METADATA_CREATED)=2026), count(distinct PUBLISHER_INSTITUTION)
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
union all
select 'GR', to_timestamp(max(_LOADED_AT)/1000000)::date, min(TITLE), max(TITLE), min(METADATA_MODIFIED)::date,
  (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV order by METADATA_MODIFIED limit 1 offset 2494),
  max(METADATA_MODIFIED)::date, count_if(year(METADATA_MODIFIED)=2026), count_if(year(DATE_CREATED)=2026), count(distinct ORGANISATION_NAME)
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV;

-- [q18] statement 18
-- France peer check: every regional council (Région ...). Live vs archived now, archived in 2026, harvested share, live downloads
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, (HARVEST_REMOTE_URL is not null and HARVEST_REMOTE_URL<>'') harv
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV where ORGANIZATION_NAME ilike 'R_gion %')
select ORGANIZATION_NAME org, count(distinct ORGANIZATION_ID) org_ids, count(*) n, count_if(ARCHIVED='False') live, count_if(arch_ts is not null) archived,
  count_if(year(arch_ts)=2026) arch_2026, round(100*count_if(year(arch_ts)=2026)/nullif(count_if(ARCHIVED='False')+count_if(year(arch_ts)=2026),0),1) pct_lost_2026,
  count_if(harv) harvested, count_if(ARCHIVED='False' and CREATED_AT>='2026-01-01') live_new_2026,
  sum(iff(ARCHIVED='False', NB_RESOURCE_DOWNLOADS, 0)) live_dl
from t group by 1 having count(*)>=20 order by arch_2026 desc;

-- [q19] statement 19
-- France time: datasets created per year on the portal (native only; harvested rows carry the source's own date), and how many of each year are archived now
select year(CREATED_AT) yr, count(*) native_created, count_if(ARCHIVED='False') still_live, round(100*count_if(ARCHIVED<>'False')/count(*),1) pct_archived,
  count(distinct ORGANIZATION_ID) orgs, median(NB_RESOURCE_DOWNLOADS) med_dl, median(QUALITY_SCORE) med_quality
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV
where (HARVEST_REMOTE_URL is null or HARVEST_REMOTE_URL='') and year(CREATED_AT) between 2010 and 2026
group by 1 order by 1;

-- [q20] statement 20
-- Germany: per publisher. Rows, rows touched on 2025-08-12 exactly, created span, HVD flags, temporal sentinels, grant-data titles
select PUBLISHER pub, count(*) n, count_if(METADATA_MODIFIED::date='2025-08-12') mod_0812, min(METADATA_CREATED)::date c_min, max(METADATA_CREATED)::date c_max,
  count_if(IS_HVD is not null and IS_HVD not in ('','[]','null')) hvd, count_if(year(TEMPORAL_END)>=9000 or year(TEMPORAL_START)<1000) t_sentinel,
  count_if(TITLE ilike '%zuwendung%') zuwendung, count_if(TAGS ilike '%lebensmittel%') food_tag, count_if(TAGS ilike '%kriminalstat%') pks_tag,
  count(distinct lower(trim(TITLE))) titles, left(any_value(TITLE),70) sample_title
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA group by 1 order by 2 desc limit 15;

-- [q21] statement 21
-- Chile: per publisher. Datasets, created by year, contest-tagged rows (Concurso Transparenta), files per dataset, formats
select PUBLISHER_INSTITUTION pub, count(*) n, count_if(CATEGORY ilike '%Transparenta%') contest,
  count_if(year(METADATA_CREATED)<=2020) c_to2020, count_if(year(METADATA_CREATED) between 2021 and 2024) c_21_24, count_if(year(METADATA_CREATED)=2025) c_2025, count_if(year(METADATA_CREATED)=2026) c_2026,
  count(distinct METADATA_CREATED::date) c_days, median(NUM_RESOURCES) med_files, sum(NUM_RESOURCES) files,
  count_if(RESOURCE_FORMATS ilike '%pdf%') pdf, count_if(RESOURCE_FORMATS ilike '%csv%' or RESOURCE_FORMATS ilike '%xls%') tabular, left(any_value(TITLE),60) sample_title
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB group by 1 order by 2 desc limit 12;

-- [q22] statement 22
-- Argentina: the two row types. Rows with no org vs with org; exact-duplicate rows; top orgs by distinct datasets and files
with t as (select *, iff(C_ORGANIZATION is null or trim(C_ORGANIZATION)='', 'no_org', 'org') kind from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB)
select 'kind' k, kind a, count(*)::text b, count(distinct DATASET_ID)::text c, count(distinct RESOURCE_URL)::text d, left(any_value(DATASET_TITLE),60) e,
  left(any_value(RESOURCE_URL),90) f, count(distinct PROVINCIA_ID)::text g
from t group by 2
union all
select 'dups', null, count(*)::text, count(distinct DATASET_ID||'|'||RESOURCE_URL||'|'||coalesce(FORMAT,''))::text, null, null, null, null from t
union all
select 'org', trim(C_ORGANIZATION), count(*)::text, count(distinct DATASET_ID)::text, count(distinct RESOURCE_URL)::text, left(any_value(DATASET_TITLE),60),
  max(LAST_MODIFIED), min(LAST_MODIFIED) from t where kind='org' group by 2 having count(*)>=100;

-- [q23] statement 23
-- France: the most-used datasets that left the portal. Archived, native (not harvested), no live dataset with the same title anywhere; top 25 by downloads
with t as (select *, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, try_to_timestamp(ARCHIVED) arch_ts from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live as (select distinct nt from t where ARCHIVED='False')
select left(t.TITLE,80) title, coalesce(t.ORGANIZATION_NAME, t.OWNER) org, t.arch_ts::date archived, t.CREATED_AT::date created, t.NB_RESOURCE_DOWNLOADS dl, t.NB_VIEWS views, t.NB_REUSES reuses,
  t.LAST_MODIFIED::date last_mod
from t left join live l on l.nt=t.nt
where t.arch_ts is not null and (t.HARVEST_REMOTE_URL is null or t.HARVEST_REMOTE_URL='') and l.nt is null
order by t.NB_RESOURCE_DOWNLOADS desc nulls last limit 25;

-- [q24] statement 24
-- France dull test on the vanished headline datasets: any LIVE dataset (any publisher) whose title carries the same key words?
with k as (select column1 topic, column2 pat from values
  ('Alim confiance (restaurant hygiene inspections)', '%alim%confiance%'), ('Alim confiance', '%contr_les officiels sanitaires%'),
  ('Musees de France list', '%mus_es de france%'), ('Foundations of public utility', '%utilit_ publique%'),
  ('Sitadel building permits', '%sitadel%'), ('Social housing RPLS', '%locatifs des bailleurs%'), ('Social housing RPLS', '%rpls%'),
  ('Pegase energy stats', '%p_gase%'), ('Meteo-France station obs', '%observation%stations m_t_orologiques%'), ('Meteo-France station obs', '%synop%'))
, t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
select k.topic, k.pat, count_if(t.ARCHIVED='False') live_hits, count_if(t.ARCHIVED<>'False') archived_hits,
  left(listagg(distinct iff(t.ARCHIVED='False', left(t.TITLE,60)||' ['||coalesce(t.ORGANIZATION_NAME,t.OWNER,'?')||', '||t.CREATED_AT::date||', dl '||coalesce(t.NB_RESOURCE_DOWNLOADS,0)||']', null), ' || '),700) live_titles
from k left join t on lower(t.TITLE) like k.pat
group by 1,2 order by 1;

-- [q25] statement 25
-- Read the words: enforcement / money / force keywords in titles across the four sampled catalogs. Hits and sample titles (source-scouting, not a story)
with u as (
  select 'AR' t, DATASET_TITLE title, C_ORGANIZATION pub from (select distinct DATASET_ID, DATASET_TITLE, C_ORGANIZATION from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB)
  union all select 'CL', TITLE, PUBLISHER_INSTITUTION from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
  union all select 'DE', TITLE, PUBLISHER from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
  union all select 'GR', TITLE, ORGANISATION_NAME from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV)
, k as (select column1 theme, column2 pat from values
  ('fines/sanctions', '(sanci|multa|bu(ss|ß)geld|sanktion|πρόστιμ|κυρώσ)'),
  ('contracts/purchasing', '(licitaci|contrataci|compras p|vergabe|auftr(a|ä)ge|συμβάσ|προμήθει)'),
  ('police/force/prisons', '(fuerza|armas|polic|penitenci|c(á|a)rcel|kriminal|gef(a|ä)ngnis|αστυνομ|φυλακ)'),
  ('grants/subsidies', '(subsidi|subvenci|zuwendung|f(ö|o)rder|επιχορήγ|ενίσχυσ)'),
  ('pollution/inspections', '(contamina|emision|emisi(ó|o)n|inspecci|fiscalizaci|kontrolle|schadstoff|ρύπαν|επιθεώρ)'))
select u.t, k.theme, count(*) hits, count(distinct u.pub) pubs, left(listagg(distinct left(u.title,55)||' ['||left(coalesce(u.pub,'?'),30)||']', ' || '),600) sample
from u join k on regexp_like(lower(u.title), '.*'||k.pat||'.*')
group by 1,2 order by 1,3 desc;

-- [q26] statement 26
-- (rerun of q25; "sample" is a reserved word) Read the words: enforcement / money / force keywords in titles across the four sampled catalogs. Hits and sample titles (source-scouting, not a story)
with u as (
  select 'AR' t, DATASET_TITLE title, C_ORGANIZATION pub from (select distinct DATASET_ID, DATASET_TITLE, C_ORGANIZATION from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB)
  union all select 'CL', TITLE, PUBLISHER_INSTITUTION from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
  union all select 'DE', TITLE, PUBLISHER from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
  union all select 'GR', TITLE, ORGANISATION_NAME from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV)
, k as (select column1 theme, column2 pat from values
  ('fines/sanctions', '(sanci|multa|bu(ss|ß)geld|sanktion|πρόστιμ|κυρώσ)'),
  ('contracts/purchasing', '(licitaci|contrataci|compras p|vergabe|auftr(a|ä)ge|συμβάσ|προμήθει)'),
  ('police/force/prisons', '(fuerza|armas|polic|penitenci|c(á|a)rcel|kriminal|gef(a|ä)ngnis|αστυνομ|φυλακ)'),
  ('grants/subsidies', '(subsidi|subvenci|zuwendung|f(ö|o)rder|επιχορήγ|ενίσχυσ)'),
  ('pollution/inspections', '(contamina|emision|emisi(ó|o)n|inspecci|fiscalizaci|kontrolle|schadstoff|ρύπαν|επιθεώρ)'))
select u.t, k.theme, count(*) hits, count(distinct u.pub) pubs, left(listagg(distinct left(u.title,55)||' ['||left(coalesce(u.pub,'?'),30)||']', ' || '),600) smp
from u join k on regexp_like(lower(u.title), '.*'||k.pat||'.*')
group by 1,2 order by 1,3 desc;

-- [q27] statement 27
-- France: whole-wave dull test for 2024-03-21. Share of the 12,190 archived with a live same-title twin (same office / any publisher)
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, coalesce(ORGANIZATION_NAME,'(no org)') org
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live_same as (select distinct org, nt from t where ARCHIVED='False')
, live_any as (select distinct nt from t where ARCHIVED='False')
, w as (select t.*, (s.nt is not null) twin_same, (a.nt is not null) twin_any from t left join live_same s on s.org=t.org and s.nt=t.nt left join live_any a on a.nt=t.nt
        where t.arch_ts::date='2024-03-21')
select count(*) n, count_if(twin_same) twin_same, round(100*count_if(twin_same)/count(*),1) pct_same, count_if(twin_any) twin_any, round(100*count_if(twin_any)/count(*),1) pct_any,
  count_if(TITLE ilike 'PPR%' or TITLE ilike '%risque%inond%' or TITLE ilike '%PPRI%') flood_risk, count_if((TITLE ilike 'PPR%' or TITLE ilike '%risque%inond%' or TITLE ilike '%PPRI%') and twin_any) flood_twin,
  sum(NB_RESOURCE_DOWNLOADS) dl, sum(iff(twin_any, 0, NB_RESOURCE_DOWNLOADS)) dl_no_twin
from w;
