-- deep-13: coverage round 2, hand queries, 2026-09-24
-- Tables: JUSTICE__INTL_UK_SANCTIONS_LIST, JUSTICE__RACIAL_JAIL_DISPARITY,
--         JUSTICE__XC_RANSOMWARELIVE_VICTIMS, JUSTICE__XC_UK_SANCTIONS_LIST,
--         JUSTICE__XC_VERA_INCARCERATION_TRENDS
-- Door: Python (connect/db.py). Every connection opened with:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'coverage-r2-2026-09-24';
-- Read-only. Numbered in the order run.

-- [1] UK INTL: size, targets, IMOs, date range, types
select count(*) n, count(distinct OFSI_GROUP_ID) targets, count(distinct nullif(trim(IMO_NUMBER::string),'')) imos,
 min(LAST_UPDATED::string) min_upd, max(LAST_UPDATED::string) max_upd,
 count_if(nullif(trim(DATE_DESIGNATED::string),'') is not null) designated_filled,
 listagg(distinct DESIGNATION_TYPE,'|') types, listagg(distinct DESIGNATION_SOURCE,'|') sources, count(distinct REGIME_NAME) regimes
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UK_SANCTIONS_LIST;

-- [2] UK INTL: sample 5
select * from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UK_SANCTIONS_LIST limit 5;

-- [3] UK XC: size, targets, IMOs, date range, types
select count(*) n, count(distinct OFSI_GROUP_ID) targets, count(distinct nullif(trim(IMO_NUMBER::string),'')) imos,
 min(DATE_DESIGNATED::string) min_des, max(DATE_DESIGNATED::string) max_des, max(LAST_UPDATED::string) max_upd,
 count_if(nullif(trim(DATE_DESIGNATED::string),'') is not null) designated_filled,
 count(distinct iff(DESIGNATION_TYPE='Ship', OFSI_GROUP_ID, null)) ship_targets,
 count(distinct iff(DESIGNATION_TYPE='Entity', OFSI_GROUP_ID, null)) entity_targets,
 count(distinct iff(DESIGNATION_TYPE='Individual', OFSI_GROUP_ID, null)) person_targets,
 listagg(distinct DESIGNATION_SOURCE,'|') sources, count(distinct REGIME_NAME) regimes, count(distinct _SOURCE_RUN_ID) runs
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST;

-- [4] UK XC: sample 5 ship rows
select * from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST where DESIGNATION_TYPE='Ship' limit 5;

-- [5] UK INTL vs XC: target overlap by OFSI_GROUP_ID
with a as (select distinct OFSI_GROUP_ID g from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UK_SANCTIONS_LIST),
     b as (select distinct OFSI_GROUP_ID g from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST)
select count_if(a.g is not null and b.g is not null) in_both, count_if(b.g is null) intl_only, count_if(a.g is null) xc_only
from a full outer join b on a.g=b.g;

-- [6] RACIAL: by year, fill and flags
select YEAR, count(*) n, count(distinct FIPS) counties, count(BLACK_JAIL_RATE) black_rate, count(WHITE_JAIL_RATE) white_rate,
 count_if(BW_RATIO=0) bw0, count(BW_RATIO) bw_filled, count_if(IS_MEASURABLE_COHORT) measurable, count_if(IS_CANONICAL_YEAR) canonical, count_if(IS_STUB_YEAR) stub,
 count_if(BLACK_WORKING_AGE_POP>=5000) blk5k
from LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY group by YEAR order by YEAR;

-- [7] RACIAL: sample 5
select * from LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY where BLACK_JAIL_RATE is not null limit 5;

-- [8] VERA: by year, fill
select YEAR, count(*) n, count(distinct COUNTY_FIPS) counties, count(TOTAL_JAIL_POP) jail, count(BLACK_JAIL_POP) blk_jail,
 count(try_to_number(TOTAL_JAIL_FROM_ICE::string)) ice, sum(try_to_number(TOTAL_JAIL_FROM_ICE::string)) ice_sum,
 count(try_to_number(TOTAL_JAIL_FROM_FED::string)) fed, count(BLACK_POP_15TO64) blk_pop, sum(TOTAL_JAIL_POP) jail_sum,
 count(TOTAL_PRISON_POP) prison
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS group by YEAR order by YEAR;

-- [9] VERA: sample 5
select * from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where TOTAL_JAIL_POP is not null and YEAR=2018 limit 5;

-- [10] RANSOM: size, dates, countries
select count(*) n, count(distinct POST_TITLE) titles, count(distinct nullif(WEBSITE,'')) sites, count(distinct GROUP_NAME) gangs,
 min(DISCOVERED) min_d, max(DISCOVERED) max_d, count_if(COUNTRY='US') us, count(distinct COUNTRY) countries,
 count_if(COUNTRY='US' and ACTIVITY ilike '%health%') us_health, count(distinct ACTIVITY) activities
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS;

-- [11] RANSOM: sample 5
select * from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS where COUNTRY='US' limit 5;

-- [12] UK XC ships vs OFAC SDN by IMO, by regime and designation year
with uk as (
 select regexp_substr(IMO_NUMBER::string,'[0-9]{7}') imo, max(DESIGNATION_ID) did,
   min(try_to_date(DATE_DESIGNATED::string)) des, max(split_part(REGIME_NAME,' (',1)) regime,
   max(iff(upper(NAME_TYPE)='PRIMARY NAME', NAME_PRIMARY, null)) nm, max(DESIGNATION_SOURCE) src,
   max(CURRENT_FLAG_OF_SHIP) flag, max(CURRENT_OWNER_OPERATOR) owner, count(*) name_rows
 from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST where DESIGNATION_TYPE='Ship' group by 1 having imo is not null),
sdn as (
 select coalesce(regexp_substr(IMO_NUMBER::string,'[0-9]{7}'), regexp_substr(REMARKS,'IMO ([0-9]{7})',1,1,'e',1)) imo,
   max(SDN_NAME) sdn_name, max(PROGRAM) prog
 from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN group by 1 having imo is not null)
select uk.regime, year(uk.des) yr, count(*) ships, count(sdn.imo) on_sdn, count_if(sdn.imo is null) uk_only,
 count_if(sdn.imo is not null and regexp_replace(upper(uk.nm),'[^A-Z0-9]','') = regexp_replace(upper(sdn.sdn_name),'[^A-Z0-9]','')) name_agree,
 sum(uk.name_rows) name_rows, (select count(*) from sdn) sdn_imos,
 (select max(_INGESTED_AT)::string from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN) sdn_loaded
from uk left join sdn on uk.imo=sdn.imo group by 1,2 order by 1,2;

-- [13] UK ships seen in NOAA AIS pings (Jan 1-8 2024, US waters)
with uk as (
 select regexp_substr(IMO_NUMBER::string,'[0-9]{7}') imo, max(DESIGNATION_ID) did,
   min(try_to_date(DATE_DESIGNATED::string)) des, max(split_part(REGIME_NAME,' (',1)) regime,
   max(iff(upper(NAME_TYPE)='PRIMARY NAME', NAME_PRIMARY, null)) nm, max(DESIGNATION_SOURCE) src,
   max(CURRENT_FLAG_OF_SHIP) flag, max(CURRENT_OWNER_OPERATOR) owner, count(*) name_rows
 from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST where DESIGNATION_TYPE='Ship' group by 1 having imo is not null),
sdn as (
 select coalesce(regexp_substr(IMO_NUMBER::string,'[0-9]{7}'), regexp_substr(REMARKS,'IMO ([0-9]{7})',1,1,'e',1)) imo,
   max(SDN_NAME) sdn_name, max(PROGRAM) prog
 from LIBRARY_MARTS.JUSTICE.JUSTICE__FED_OFAC_SDN group by 1 having imo is not null),
a as (select IMO_NORMALIZED::string imo, count(*) pings, count(distinct MMSI) mmsis, min(BASE_DATETIME)::string first_ping,
        max(BASE_DATETIME)::string last_ping, max(VESSEL_NAME) ais_name, min(VESSEL_NAME) ais_name2,
        round(avg(LATITUDE),2) lat, round(avg(LONGITUDE),2) lon, max(VESSEL_TYPE_CODE) vtype
      from LIBRARY_MARTS.MARITIME.MARITIME__FED_NOAA_AIS where IMO_NORMALIZED::string in (select imo from uk) group by 1)
select uk.imo, uk.nm, uk.des::string des, uk.regime, uk.src, uk.flag, uk.owner, iff(sdn.imo is null,'UK-only','also SDN') us_status, sdn.sdn_name, a.*
from uk join a on uk.imo=a.imo left join sdn on uk.imo=sdn.imo order by a.pings desc;

-- [14] OpenSanctions DATASETS labels naming UK or US OFAC lists
select trim(d.value::string, ' "[]') ds, count(*) n
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT, lateral split_to_table(DATASETS::string, ';') d
where d.value::string ilike any ('%kingdom%','% uk %','uk %','%ofac%','%hm treasury%','%fcdo%','%ofsi%','%british%','"uk%')
group by 1 order by 2 desc limit 25;

-- [15] UK INTL vs XC: LAST_UPDATED agreement (day/month swap check)
with i as (select UNIQUE_ID id, max(LAST_UPDATED::string) lu_raw, max(try_to_date(LAST_UPDATED::string)) lu, max(try_to_date(DATE_DESIGNATED::string)) dd from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_UK_SANCTIONS_LIST group by 1),
     x as (select DESIGNATION_ID id, max(try_to_date(LAST_UPDATED::string)) lu, max(try_to_date(DATE_DESIGNATED::string)) dd from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST group by 1)
select count(*) intl_ids, count(x.id) matched_ids, count_if(i.lu > current_date()) intl_future,
 count_if(i.lu = x.lu) same_lu, count_if(i.lu <> x.lu) diff_lu,
 count_if(i.lu <> x.lu and day(i.lu)=month(x.lu) and month(i.lu)=day(x.lu)) swapped_dm,
 count_if(i.lu < x.lu and not (day(i.lu)=month(x.lu) and month(i.lu)=day(x.lu))) intl_older,
 count_if(i.dd is not null) intl_dd_filled, count_if(i.dd = x.dd) same_dd,
 max(iff(i.lu > current_date(), i.id||' intl='||i.lu_raw||' xc='||x.lu::string, null)) future_example
from i left join x on i.id=x.id;

-- [16] RANSOM: by year discovered, US, US health, bulk-timestamp rows
with r as (select *, count(*) over (partition by DISCOVERED) same_ts, count(*) over (partition by POST_TITLE, GROUP_NAME) dup_pair
           from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS)
select year(try_to_timestamp_tz(DISCOVERED)) yr, count(*) n, count_if(same_ts>=50) bulk_ts_rows, count_if(dup_pair>1) dup_title_gang,
 count_if(COUNTRY='US') us, count_if(COUNTRY='US' and ACTIVITY ilike '%health%') us_health,
 count_if(COUNTRY='US' and ACTIVITY ilike '%health%' and same_ts<50) us_health_nonbulk, count(distinct GROUP_NAME) gangs
from r group by 1 order by 1;

-- [17] RANSOM: US victims by ACTIVITY, 2024 on
select ACTIVITY, count(*) n, count_if(try_to_timestamp_tz(DISCOVERED) >= '2024-01-01'::timestamp_tz) since_2024
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS where COUNTRY='US' group by 1 order by 2 desc;

-- [18] RANSOM: US health posts matched to CMS hospitals by exact cleaned name
with v as (select POST_TITLE, WEBSITE, GROUP_NAME, left(DISCOVERED,10) disc, left(DESCRIPTION,80) descr,
             regexp_replace(upper(POST_TITLE),'[^A-Z0-9]','') k
           from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS where COUNTRY='US' and ACTIVITY ilike '%health%'),
     h as (select regexp_replace(upper(FACILITY_NAME),'[^A-Z0-9]','') k, count(*) n_hosp, max(FACILITY_NAME) fname,
             max(CITY_TOWN) city, max(STATE) st, max(CCN) ccn from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL group by 1)
select v.POST_TITLE, v.WEBSITE, v.GROUP_NAME, v.disc, v.descr, h.fname, h.city, h.st, h.ccn, h.n_hosp
from v join h on v.k=h.k order by v.disc;

-- [19] RACIAL: 2019 top Black/white jail-rate ratios, 5k+ Black working-age, with state peers, 2010/2023 and fed holds
with r as (select FIPS, YEAR, COUNTY_NAME, STATE_ABBR, URBANICITY, BLACK_JAIL_RATE b, WHITE_JAIL_RATE w, BLACK_JAIL_POP bp,
             WHITE_JAIL_POP wp, BLACK_WORKING_AGE_POP bpop from LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY
           where YEAR in (2010,2019,2023) and BLACK_JAIL_RATE is not null and WHITE_JAIL_RATE>0
             and BLACK_WORKING_AGE_POP>=5000 and BLACK_JAIL_POP>=20 and WHITE_JAIL_POP>=20),
y as (select *, b/w ratio, median(b/w) over (partition by STATE_ABBR) st_med, count(*) over (partition by STATE_ABBR) st_n,
             median(b/w) over () nat_med, count(*) over () nat_n from r where YEAR=2019),
v as (select COUNTY_FIPS, TOTAL_JAIL_POP j, try_to_double(TOTAL_JAIL_FROM_FED::string) fed, try_to_double(TOTAL_JAIL_FROM_ICE::string) ice,
             try_to_double(TOTAL_JAIL_FROM_PRISON::string) pris from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where YEAR=2019)
select y.FIPS, y.COUNTY_NAME, y.STATE_ABBR, y.URBANICITY, y.bpop, round(y.bp) bjail, round(y.wp) wjail, round(y.b) brate, round(y.w) wrate,
 round(y.ratio,1) ratio19, round(y.st_med,1) state_med, y.st_n, round(y.nat_med,1) nat_med, y.nat_n,
 round(r10.b/r10.w,1) ratio10, round(r23.b/r23.w,1) ratio23, round(v.fed/nullif(v.j,0),3) fed_share, round(v.pris/nullif(v.j,0),3) prison_share
from y left join r r10 on r10.FIPS=y.FIPS and r10.YEAR=2010 left join r r23 on r23.FIPS=y.FIPS and r23.YEAR=2023
left join v on v.COUNTY_FIPS=y.FIPS
order by y.ratio desc limit 20;

-- [20] RACIAL: fixed cohort trend 2010-2023, median ratio and pooled rates
with r as (select FIPS, YEAR, BLACK_JAIL_RATE b, WHITE_JAIL_RATE w, BLACK_JAIL_POP bp, WHITE_JAIL_POP wp,
             BLACK_WORKING_AGE_POP bpop, WHITE_WORKING_AGE_POP wpop from LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY
           where YEAR between 2010 and 2023 and BLACK_JAIL_RATE is not null and WHITE_JAIL_RATE>0
             and BLACK_WORKING_AGE_POP>=5000 and BLACK_JAIL_POP>=20 and WHITE_JAIL_POP>=20),
c as (select FIPS from r where YEAR in (2010,2015,2019,2023) group by 1 having count(distinct YEAR)=4)
select YEAR, count(*) counties, round(median(b/w),2) med_ratio, count_if(b/w>=5) ge5, count_if(b/w>=10) ge10,
 round(sum(bp)/sum(bpop)*1e5) pooled_black, round(sum(wp)/sum(wpop)*1e5) pooled_white,
 round((sum(bp)/sum(bpop))/(sum(wp)/sum(wpop)),2) pooled_ratio, (select count(*) from c) cohort
from r where FIPS in (select FIPS from c) group by 1 order by 1;

-- [21] VERA: fixed cohort jail rate by urbanicity 2010/2015/2019/2023, share held for others
with v as (select COUNTY_FIPS f, YEAR y, URBANICITY u, TOTAL_JAIL_POP j, TOTAL_POP_15TO64 p,
             try_to_double(TOTAL_JAIL_FROM_ICE::string) ice, try_to_double(TOTAL_JAIL_FROM_FED::string) fed,
             try_to_double(TOTAL_JAIL_FROM_PRISON::string) pris, try_to_double(TOTAL_JAIL_FROM_OTHER_JAIL::string) oj
           from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where YEAR in (2010,2015,2019,2023) and TOTAL_JAIL_POP is not null and TOTAL_POP_15TO64>0),
c as (select f from v group by f having count(distinct y)=4)
select u, y, count(*) counties, round(sum(j)) jail, round(sum(j)/sum(p)*1e5) rate_per100k_15to64,
 round(sum(fed)/sum(iff(fed is null,null,j)),3) fed_share, count(fed) fed_n, round(sum(ice)/sum(iff(ice is null,null,j)),3) ice_share,
 count(ice) ice_n, round(sum(pris)/sum(iff(pris is null,null,j)),3) prison_share
from v where f in (select f from c) group by 1,2 order by 1,2;

-- [22] VERA: top jail-rate growers 2010->2023 (15-64 pop 10k+), local vs held-for-others, capacity
with v as (select COUNTY_FIPS f, YEAR y, COUNTY_NAME n, STATE_ABBR s, URBANICITY u, TOTAL_JAIL_POP j, TOTAL_POP_15TO64 p,
             coalesce(try_to_double(TOTAL_JAIL_FROM_FED::string),0)+coalesce(try_to_double(TOTAL_JAIL_FROM_PRISON::string),0)
               +coalesce(try_to_double(TOTAL_JAIL_FROM_OTHER_JAIL::string),0) held, try_to_double(JAIL_RATED_CAPACITY::string) cap,
             try_to_double(BLACK_JAIL_POP_RATE::string) brate, try_to_double(WHITE_JAIL_POP_RATE::string) wrate
           from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where YEAR in (2010,2023) and TOTAL_JAIL_POP is not null and TOTAL_POP_15TO64>=10000),
w as (select a.f, a.n, a.s, a.u, a.p p10, b.p p23, a.j j10, b.j j23, a.held h10, b.held h23, b.cap cap23,
        a.j/a.p*1e5 r10, b.j/b.p*1e5 r23, (a.j-a.held)/a.p*1e5 l10, (b.j-b.held)/b.p*1e5 l23, b.brate, b.wrate
      from v a join v b on a.f=b.f and a.y=2010 and b.y=2023)
select f, n, s, u, round(p10) p10, round(p23) p23, round(j10) j10, round(j23) j23, round(h10) held10, round(h23) held23,
 round(r10) rate10, round(r23) rate23, round(r23/nullif(r10,0),2) growth, round(l10) local10, round(l23) local23, cap23,
 round(j23/nullif(cap23,0),2) pop_over_cap, round(brate) brate23, round(wrate) wrate23,
 round(median(r23/nullif(r10,0)) over (partition by u),2) urb_med_growth, count(*) over () n_counties
from w where j23>=100 order by (l23-l10) desc limit 20;

-- [23] RACIAL vs VERA: same county-year, do counts agree
select count(*) joined, count_if(abs(r.TOTAL_JAIL_POP - v.TOTAL_JAIL_POP) > 0.5) total_diff,
 count_if(r.BLACK_JAIL_POP is not null) r_black_filled, count(try_to_double(v.BLACK_JAIL_POP::string)) v_black_num,
 count_if(abs(r.BLACK_JAIL_POP - try_to_double(v.BLACK_JAIL_POP::string)) > 0.5) black_diff,
 count_if(abs(r.BLACK_JAIL_RATE - try_to_double(v.BLACK_JAIL_POP_RATE::string)) > 1) black_rate_diff,
 count_if(abs(r.BLACK_WORKING_AGE_POP - try_to_double(v.BLACK_POP_15TO64::string)) > 0.5) black_pop_diff
from LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY r join LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS v on r.FIPS=v.COUNTY_FIPS and r.YEAR=v.YEAR;

-- [24] OpenSanctions: targets on UK FCDO list, how many also on US OFAC SDN, by type
select ENTITY_TYPE, count(*) uk_fcdo,
 count_if(DATASETS::string ilike '%US OFAC Specially Designated Nationals%') also_sdn,
 count_if(DATASETS::string not ilike '%US OFAC Specially Designated Nationals%' and DATASETS::string ilike '%US OFAC Consolidated (non-SDN)%') non_sdn_only,
 count_if(COUNTRIES::string ilike '%ru%') ru_linked,
 count_if(COUNTRIES::string ilike '%ru%' and DATASETS::string ilike '%US OFAC Specially Designated Nationals%') ru_also_sdn,
 min(FIRST_SEEN)::string first_seen_min, max(LAST_SEEN)::string last_seen_max
from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT where DATASETS::string ilike '%UK FCDO Sanctions List%' group by 1 order by 2 desc;

-- [25] UK ships seen in AIS: second field check, UK names/aliases, type, flags
select regexp_substr(IMO_NUMBER::string,'[0-9]{7}') imo, listagg(distinct upper(NAME_PRIMARY), ' / ') uk_names,
 max(PREVIOUS_FLAGS) prev_flags, max(CURRENT_FLAG_OF_SHIP) flag, max(TYPE_OF_SHIP) ship_type, max(YEAR_BUILT) built,
 max(PREVIOUS_OWNER_OPERATOR) prev_owner, max(left(UK_STATEMENT_OF_REASONS,160)) reason
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_UK_SANCTIONS_LIST where regexp_substr(IMO_NUMBER::string,'[0-9]{7}') in ('9266877','9308833','9333785','9439383','9385831','9389095','9419450','9333400')
group by 1;

-- [26] RANSOM: US victims posted by 2+ different gangs (same cleaned title)
with v as (select regexp_replace(upper(POST_TITLE),'[^A-Z0-9]','') k, POST_TITLE t, WEBSITE w, GROUP_NAME g, ACTIVITY a,
             try_to_timestamp_tz(DISCOVERED) d from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS where COUNTRY='US'),
agg as (select k, max(t) title, max(w) site, max(a) activity, count(distinct g) gangs, listagg(distinct g, ',') gang_list,
          min(d)::date first_post, max(d)::date last_post, count(*) posts from v group by k having count(distinct g)>=2)
select *, count(*) over () n_repeat, sum(iff(activity ilike '%health%',1,0)) over () n_repeat_health,
 sum(iff(posts>10,1,0)) over () n_bulk_keys
from agg order by iff(activity ilike '%health%',0,1), gangs desc, posts desc limit 30;

-- [27] RANSOM: blank country by year, hospital-like US health titles, bulk sites
select year(try_to_timestamp_tz(DISCOVERED)) yr, count(*) n, count_if(nullif(trim(COUNTRY),'') is null) no_country, count_if(COUNTRY='US') us,
 count_if(COUNTRY='US' and ACTIVITY ilike '%health%' and regexp_like(upper(POST_TITLE),'.*(HOSPITAL|MEDICAL CENTER|HEALTH SYSTEM|HEALTHCARE SYSTEM|REGIONAL HEALTH|MEDICAL CTR).*')) us_hosp_like,
 count_if(WEBSITE in ('maersk.com','fedex.com','renault.fr')) bulk_sites
from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_RANSOMWARELIVE_VICTIMS group by 1 order by 1;

-- [28] VERA: top jail-rate risers 2010->2019 (same-source years), state+urbanicity peers, held-for-others share, capacity
with v as (select COUNTY_FIPS f, YEAR y, COUNTY_NAME n, STATE_ABBR s, URBANICITY u, TOTAL_JAIL_POP j, TOTAL_POP_15TO64 p,
             try_to_double(TOTAL_JAIL_FROM_FED::string) fed, try_to_double(TOTAL_JAIL_FROM_ICE::string) ice,
             try_to_double(TOTAL_JAIL_FROM_PRISON::string) pris, try_to_double(JAIL_RATED_CAPACITY::string) cap
           from LIBRARY_MARTS.JUSTICE.JUSTICE__XC_VERA_INCARCERATION_TRENDS where YEAR in (2010,2019,2023) and TOTAL_JAIL_POP is not null and TOTAL_POP_15TO64>=10000),
w as (select a.f, a.n, a.s, a.u, a.p p10, b.p p19, a.j j10, b.j j19, c.j j23, a.j/a.p*1e5 r10, b.j/b.p*1e5 r19, c.j/c.p*1e5 r23,
        (coalesce(a.fed,0)+coalesce(a.pris,0))/nullif(a.j,0) held10, (coalesce(b.fed,0)+coalesce(b.pris,0))/nullif(b.j,0) held19,
        b.ice ice19, b.cap cap19
      from v a join v b on a.f=b.f and a.y=2010 and b.y=2019 left join v c on c.f=a.f and c.y=2023),
x as (select *, median(r19/nullif(r10,0)) over (partition by s,u) peer_med, count(*) over (partition by s,u) peer_n, count(*) over () n_all,
        median(r19/nullif(r10,0)) over () nat_med from w where j19>=100 and j10>0)
select f, n, s, u, round(p10) p10, round(p19) p19, round(j10) j10, round(j19) j19, round(j23) j23, round(r10) r10, round(r19) r19, round(r23) r23,
 round(r19/r10,2) growth, round(peer_med,2) peer_med, peer_n, round(nat_med,2) nat_med, n_all, round(held10,2) held10, round(held19,2) held19,
 round(ice19) ice19, round(j19/nullif(cap19,0),2) over_cap19
from x order by (r19-r10) desc limit 20;

-- [29] RACIAL: biggest Black/white ratio risers 2019->2023 in fixed cohort, plus NYC borough 2019 check
with r as (select FIPS, YEAR, COUNTY_NAME, STATE_ABBR, BLACK_JAIL_RATE b, WHITE_JAIL_RATE w, BLACK_JAIL_POP bp, WHITE_JAIL_POP wp,
             TOTAL_JAIL_POP tj, BLACK_WORKING_AGE_POP bpop, TOTAL_WORKING_AGE_POP tpop from LIBRARY_MARTS.JUSTICE.JUSTICE__RACIAL_JAIL_DISPARITY where YEAR in (2019,2023)),
f as (select * from r where b is not null and w>0 and bpop>=5000 and bp>=20 and wp>=20),
m as (select a.FIPS, a.COUNTY_NAME, a.STATE_ABBR, a.b/a.w r19, c.b/c.w r23, a.bp bp19, c.bp bp23, a.wp wp19, c.wp wp23,
        a.tj tj19, c.tj tj23, count(*) over () n
      from f a join f c on a.FIPS=c.FIPS and a.YEAR=2019 and c.YEAR=2023),
top as (select * from m qualify row_number() over (order by r23-r19 desc) <= 12)
select 'riser' tag, FIPS, COUNTY_NAME, STATE_ABBR, round(r19,1) ratio19, round(r23,1) ratio23, round(bp19) bjail19, round(bp23) bjail23,
 round(wp19) wjail19, round(wp23) wjail23, round(tj19) tj19, round(tj23) tj23, null tpop19, n from top
union all
select 'nyc', FIPS, COUNTY_NAME, STATE_ABBR, round(b/nullif(w,0),1), null, round(bp), null, round(wp), null, round(tj), null, tpop, null
from r where YEAR=2019 and FIPS in ('36005','36047','36061','36081','36085')
order by 1 desc, 6 desc;

-- Budget: 29 SELECT/WITH statements above + 6 session statements (2 ALTER SESSION per connection x 3 connections) = 35.
-- Note: [22] is superseded by [28]. The held-for-others columns go blank after 2020, so subtracting them 2010 vs 2023 made fake "local" growth.
