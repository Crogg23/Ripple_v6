
-- [q01] statement 1
-- SDWA service areas: shape, codes x primary flag, duplicates, orphans vs PUB_WATER_SYSTEMS, primaries per system, sibling tables named like it
with t as (select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS),
p as (select PWSID, PWS_TYPE_CODE, PWS_ACTIVITY_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS)
select 'profile' k, count(*)::text a, count(distinct PWSID)::text b, count(distinct PWSID||'|'||SERVICE_AREA_TYPE_CODE)::text c, count(distinct SUBMISSIONYEARQUARTER)::text d, min(FIRST_REPORTED_DATE)::text e, max(LAST_REPORTED_DATE)::text f from t
union all select 'orphans', count(*)::text, count(distinct t.PWSID)::text, null, null, null, null from t left join p on p.PWSID = t.PWSID where p.PWSID is null
union all select 'pws_total_active_without_sa', count(*)::text, count_if(PWS_ACTIVITY_CODE = 'A')::text, count_if(PWS_ACTIVITY_CODE = 'A' and PWSID not in (select PWSID from t))::text, count_if(PWSID not in (select PWSID from t))::text, null, null from p
union all select * from (select 'code', SERVICE_AREA_TYPE_CODE, count(*)::text, count_if(IS_PRIMARY_SERVICE_AREA_CODE = 'Y')::text, count_if(IS_PRIMARY_SERVICE_AREA_CODE = 'N')::text, count_if(IS_PRIMARY_SERVICE_AREA_CODE is null or trim(IS_PRIMARY_SERVICE_AREA_CODE) = '')::text, count(distinct PWSID)::text from t group by 2 order by count(*) desc limit 60)
union all select 'primaries_per_pws', n::text, count(*)::text, null, null, null, null from (select PWSID, count_if(IS_PRIMARY_SERVICE_AREA_CODE = 'Y') n from t group by 1) group by 2
union all select 'sibling', TABLE_CATALOG||'.'||TABLE_SCHEMA||'.'||TABLE_NAME, ROW_COUNT::text, null, null, null, null from LIBRARY_MARTS.INFORMATION_SCHEMA.TABLES where TABLE_NAME ilike '%SERVICE_AREA%';

-- [q02] statement 2
-- SDWA service areas: primary service type x water-system type, active systems only, with people served and groundwater share
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code, count(*) nprim from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1),
p as (select PWSID, PWS_TYPE_CODE, POPULATION_SERVED_COUNT pop, GW_SW_CODE, IS_SCHOOL_OR_DAYCARE_IND from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS where PWS_ACTIVITY_CODE = 'A')
select sa.code, p.PWS_TYPE_CODE, count(*) systems, sum(p.pop) people, median(p.pop) med_pop, count_if(p.GW_SW_CODE = 'GW') gw, count_if(p.IS_SCHOOL_OR_DAYCARE_IND = 'Y') school_flag, count_if(sa.nprim > 1) multi_primary
from sa join p on p.PWSID = sa.PWSID group by 1, 2 having count(*) >= 200 order by systems desc;

-- [q03] statement 3
-- ICE facility codes: confirm lookup; land rate of detention-stint codes; stints by facility type
with s as (select DETENTION_FACILITY_CODE code, count(*) n, min(BOOK_IN_AT) mn, max(BOOK_IN_AT) mx from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS group by 1),
f as (select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES)
select 'profile' k, count(*)::text a, count(distinct DETENTION_FACILITY_CODE)::text b, count(distinct TYPE_GROUPED)::text c, count(distinct TYPE_DETAILED)::text d from f
union all select 'land', count(*)::text, count_if(f.DETENTION_FACILITY_CODE is not null)::text, sum(n)::text, sum(iff(f.DETENTION_FACILITY_CODE is not null, n, 0))::text from s left join f on f.DETENTION_FACILITY_CODE = s.code
union all select 'type', f.TYPE_GROUPED||' / '||coalesce(f.TYPE_DETAILED, '(null)'), count(distinct f.DETENTION_FACILITY_CODE)::text, count(distinct s.code)::text, coalesce(sum(s.n), 0)::text from f left join s on s.code = f.DETENTION_FACILITY_CODE group by 2
union all select 'stint_range', min(mn)::text, max(mx)::text, null, null from s
union all select * from (select 'unmatched_top', s.code, s.n::text, null, null from s left join f on f.DETENTION_FACILITY_CODE = s.code where f.DETENTION_FACILITY_CODE is null order by s.n desc limit 10);

-- [q04] statement 4
-- ICE facility list: confirm lookup; types; duplicate name+city; name+state match to the facility-code table; load stamps
with l as (select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_LIST),
f as (select upper(trim(DETENTION_FACILITY_NAME)) nm, upper(trim(STATE)) st, min(DETENTION_FACILITY_CODE) code, min(TYPE_DETAILED) td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES group by 1, 2)
select 'profile' k, count(*)::text a, count(distinct FACILITY_NAME)::text b, count(distinct FACILITY_NAME||'|'||CITY)::text c, count(distinct STATE)::text d from l
union all select 'type', FACILITY_TYPE_DETAILED, count(*)::text, null, null from l group by 2
union all select 'name_state_match', count(*)::text, count_if(f.code is not null)::text, null, null from l left join f on f.nm = upper(trim(l.FACILITY_NAME)) and f.st = upper(trim(l.STATE))
union all select 'dupe', FACILITY_NAME, CITY, count(*)::text, null from l group by 2, 3 having count(*) > 1
union all select 'load', _INGESTED_AT::text, _SOURCE_RUN_ID, count(*)::text, null from l group by 2, 3;

-- [q05] statement 5
-- CBP encounters: read all nine rows
select * from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CBP_ENCOUNTERS;

-- [q06] statement 6
-- Swiss catalog sample: ids, constants, sort order of the 5,000 (modified year), old ISSUED dates, issued-by-year, language, load stamps
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CH_OPENDATASWISS)
select 'profile' k, count(*)::text a, count(distinct ID)::text b, count(distinct NAME)::text c, min(METADATA_MODIFIED)::text d, max(METADATA_MODIFIED)::text e, min(METADATA_CREATED)::text f, max(METADATA_CREATED)::text g from t
union all select 'private_type', PRIVATE::text, TYPE, count(*)::text, null, null, null, null from t group by 2, 3
union all select 'mod_year', year(METADATA_MODIFIED)::text, count(*)::text, null, null, null, null, null from t group by 2
union all select 'created_year', year(METADATA_CREATED)::text, count(*)::text, null, null, null, null, null from t group by 2
union all select * from (select 'issued_old', ISSUED::text, NAME, C_ORGANIZATION, left(TITLE, 120), null, null, null from t where ISSUED < '1950-01-01' order by ISSUED limit 8)
union all select 'issued_null', count_if(ISSUED is null)::text, count_if(ISSUED < '1950-01-01')::text, count_if(ISSUED > '2026-09-24')::text, null, null, null, null from t
union all select * from (select 'lang', LANGUAGE, count(*)::text, null, null, null, null, null from t group by 2 order by count(*) desc limit 8)
union all select 'load', _LOADED_AT::text, _SOURCE_URL, count(*)::text, null, null, null, null from t group by 2, 3;

-- [q07] statement 7
-- ICE hold rooms and staging sites (type from FACILITY_CODES): stint length, same Oct 1 - Feb 28 window in FY23-FY26; drop rows ICE's own file flags as duplicates; midnight book-outs counted to catch date-only stamps
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES where TYPE_GROUPED = 'Hold/Staging'),
s as (select DETENTION_FACILITY_CODE code, BOOK_IN_AT, BOOK_OUT_AT, datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs,
        case when BOOK_IN_AT >= '2022-10-01' and BOOK_IN_AT < '2023-03-01' then 'FY23'
             when BOOK_IN_AT >= '2023-10-01' and BOOK_IN_AT < '2024-03-01' then 'FY24'
             when BOOK_IN_AT >= '2024-10-01' and BOOK_IN_AT < '2025-03-01' then 'FY25'
             when BOOK_IN_AT >= '2025-10-01' and BOOK_IN_AT < '2026-03-01' then 'FY26' end fy
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True')
select coalesce(f.td, '(blank)') td, s.fy, count(*) stints, count(distinct s.code) sites, count_if(BOOK_OUT_AT is null) still_open,
  round(median(hrs), 1) med_hrs, round(percentile_cont(0.9) within group (order by hrs), 1) p90_hrs,
  count_if(hrs > 12) gt12h, round(100 * count_if(hrs > 12) / count_if(hrs is not null), 1) pct_gt12h,
  count_if(hrs > 24) gt24h, round(100 * count_if(hrs > 24) / count_if(hrs is not null), 1) pct_gt24h,
  count_if(hrs > 72) gt72h, count_if(hrs > 168) gt7d, round(max(hrs), 0) max_hrs,
  count_if(hrs < 0) neg, count_if(to_time(BOOK_OUT_AT) = '00:00:00') midnight_out
from s join f on f.code = s.code where s.fy is not null group by 1, 2 order by 1, 2;

-- [q08] statement 8
-- ICE hold rooms (TYPE_DETAILED = Hold) ranked against each other: Oct 1 - Feb 28 window FY24, FY25, FY26; stints over 24 and 72 hours, median hours, name and place from FACILITY_CODES
with f as (select DETENTION_FACILITY_CODE code, DETENTION_FACILITY_NAME nm, CITY, STATE, AOR from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES where TYPE_DETAILED = 'Hold'),
s as (select DETENTION_FACILITY_CODE code, datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs,
        case when BOOK_IN_AT >= '2023-10-01' and BOOK_IN_AT < '2024-03-01' then 'FY24'
             when BOOK_IN_AT >= '2024-10-01' and BOOK_IN_AT < '2025-03-01' then 'FY25'
             when BOOK_IN_AT >= '2025-10-01' and BOOK_IN_AT < '2026-03-01' then 'FY26' end fy
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_OUT_AT is not null),
g as (select f.code, f.nm, f.CITY, f.STATE, f.AOR,
        count_if(fy = 'FY24') n24, count_if(fy = 'FY24' and hrs > 24) o24_24,
        count_if(fy = 'FY25') n25, count_if(fy = 'FY25' and hrs > 24) o24_25, count_if(fy = 'FY25' and hrs > 72) o72_25,
        count_if(fy = 'FY26') n26, count_if(fy = 'FY26' and hrs > 24) o24_26, count_if(fy = 'FY26' and hrs > 72) o72_26,
        round(median(iff(fy = 'FY26', hrs, null)), 1) med26, round(median(iff(fy = 'FY25', hrs, null)), 1) med25, round(max(iff(fy = 'FY26', hrs, null)), 0) max26
      from s join f on f.code = s.code group by 1, 2, 3, 4, 5)
select * from (select 'site' k, g.*, round(100 * o24_26 / nullif(n26, 0), 1) pct24_26, round(100 * o24_25 / nullif(n25, 0), 1) pct24_25 from g where n26 >= 100 or n25 >= 100 order by o24_26 desc limit 25)
union all select 'all_sites', null, count(*)::text, null, null, null, sum(n24), sum(o24_24), sum(n25), sum(o24_25), sum(o72_25), sum(n26), sum(o24_26), sum(o72_26), null, null, null,
  round(median(iff(n26 >= 100, 100 * o24_26 / n26, null)), 1), round(median(iff(n25 >= 100, 100 * o24_25 / n25, null)), 1) from g;

-- [q09] statement 9
-- Swiss sample: is the 5,000 an alphabetical or created-date slice? name range, created by month in 2023, newest created rows, top orgs
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CH_OPENDATASWISS)
select 'name_range' k, min(NAME) a, max(NAME) b, min(ID) c, max(ID) d from t
union all select 'created_2023_by_month', to_char(METADATA_CREATED, 'YYYY-MM'), count(*)::text, null, null from t where METADATA_CREATED >= '2023-01-01' group by 2
union all select * from (select 'newest_created', METADATA_CREATED::text, NAME, C_ORGANIZATION, METADATA_MODIFIED::text from t order by METADATA_CREATED desc limit 5)
union all select * from (select 'org', C_ORGANIZATION, count(*)::text, min(METADATA_CREATED)::text, max(METADATA_CREATED)::text from t group by 2 order by count(*) desc limit 8);

-- [q10] statement 10
-- SDWA service-area codes checked against system names: share of active systems per primary code whose name says mobile home / school / daycare / restaurant / camp / motel
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, upper(PWS_NAME) nm, OWNER_TYPE_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS where PWS_ACTIVITY_CODE = 'A')
select sa.code, count(*) systems,
  round(100 * count_if(nm like any ('%MOBILE%', '%MHP%', '%TRAILER%', '%MANUFACTURED%', '%M.H.P%', '%MH PARK%', '%HOME PARK%', '%RV PARK%')) / count(*), 1) pct_mobile,
  round(100 * count_if(nm like any ('%SCHOOL%', '%ELEM%', '%ACADEMY%', '% HIGH%', '% MIDDLE%', '% HS', '% ES')) / count(*), 1) pct_school,
  round(100 * count_if(nm like any ('%DAY CARE%', '%DAYCARE%', '%CHILD%', '%PRESCHOOL%', '%LEARNING%', '%KIDS%', '%MONTESSORI%', '%NURSERY%')) / count(*), 1) pct_daycare,
  round(100 * count_if(nm like any ('%RESTAURANT%', '%CAFE%', '%DINER%', '%GRILL%', '%TAVERN%', '% BAR%', '%PIZZA%', '% INN%')) / count(*), 1) pct_food,
  round(100 * count_if(nm like any ('%CAMP%')) / count(*), 1) pct_camp,
  round(100 * count_if(nm like any ('%MOTEL%', '%HOTEL%', '%LODGE%', '%RESORT%')) / count(*), 1) pct_lodging,
  round(100 * count_if(nm like any ('%SUBDIVISION%', '%ESTATES%', '%HOA%', '%HOMEOWNERS%', '%WATER ASSOC%', '%WATER CO%', '%WATER SUPPLY%', '%WSC%', '%UTILIT%', '%CITY OF%', '%TOWN OF%', '%VILLAGE OF%')) / count(*), 1) pct_residential_word,
  round(100 * count_if(OWNER_TYPE_CODE = 'P') / count(*), 1) pct_private, any_value(nm) example
from sa join p on p.PWSID = sa.PWSID group by 1 having count(*) >= 300 order by systems desc;

-- [q11] statement 11
-- SDWA peer test: mobile home park (MH+MP) vs other residential community systems, and schools/daycares vs other non-transient systems; active groundwater systems; health-based and monitoring violations with compliance periods starting 2021-2025, deduped by VIOLATION_ID
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, PWS_TYPE_CODE, POPULATION_SERVED_COUNT pop, OWNER_TYPE_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS where PWS_ACTIVITY_CODE = 'A' and GW_SW_CODE = 'GW'),
v as (select PWSID, count(distinct iff(IS_HEALTH_BASED_IND = 'Y', VIOLATION_ID, null)) hb, count(distinct iff(VIOLATION_CATEGORY_CODE in ('MR', 'MON'), VIOLATION_ID, null)) mr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where COMPL_PER_BEGIN_DATE >= '2021-01-01' and COMPL_PER_BEGIN_DATE < '2026-01-01' and VIOLATION_ID is not null group by 1),
x as (select p.*, case when sa.code in ('MH', 'MP') then 'MHP' when sa.code in ('RA', 'SU', 'HA', 'OR', 'MU') then 'RES' else sa.code end grp,
        iff(OWNER_TYPE_CODE = 'P', 'private', 'other') own,
        case when pop <= 100 then 'a 25-100' when pop <= 500 then 'b 101-500' when pop <= 3300 then 'c 501-3300' else 'd 3301+' end band,
        coalesce(v.hb, 0) hb, coalesce(v.mr, 0) mr
      from p join sa on sa.PWSID = p.PWSID left join v on v.PWSID = p.PWSID)
select PWS_TYPE_CODE, grp, iff(PWS_TYPE_CODE = 'CWS', own, 'all') own, band, count(*) systems, sum(pop) people,
  count_if(hb > 0) any_hb, round(100 * count_if(hb > 0) / count(*), 1) pct_hb, sum(hb) hb_viol, count_if(mr > 0) any_mr, round(100 * count_if(mr > 0) / count(*), 1) pct_mr
from x where (PWS_TYPE_CODE = 'CWS' and grp in ('MHP', 'RES')) or (PWS_TYPE_CODE = 'NTNCWS' and grp in ('SC', 'DC', 'IA', 'ON', 'OA', 'MF'))
group by 1, 2, 3, 4 order by 1, 4, 3, 2;

-- [q12] statement 12
-- ICE hold rooms by book-in month, Oct 2022 - Feb 2026: all Hold sites, the top four sites, and Staging sites as the control; stints and stints over 24 / 72 hours
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES where TYPE_GROUPED = 'Hold/Staging'),
s as (select DETENTION_FACILITY_CODE code, to_char(BOOK_IN_AT, 'YYYY-MM') ym, datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_IN_AT >= '2022-10-01' and BOOK_IN_AT < '2026-03-01')
select ym,
  count_if(f.td = 'Hold') hold_n, count_if(f.td = 'Hold' and hrs > 24) hold_24, count_if(f.td = 'Hold' and hrs > 72) hold_72,
  count_if(f.td = 'Hold' and hrs > 24 and s.code not in ('BALHOLD', 'IWAHOLD', 'DALHOLD', 'ATLHOLD')) hold_24_ex_top4,
  count_if(s.code = 'BALHOLD') bal_n, count_if(s.code = 'BALHOLD' and hrs > 24) bal_24,
  count_if(s.code = 'IWAHOLD') mesa_n, count_if(s.code = 'IWAHOLD' and hrs > 24) mesa_24,
  count_if(s.code = 'DALHOLD') dal_n, count_if(s.code = 'DALHOLD' and hrs > 24) dal_24,
  count_if(s.code = 'ATLHOLD') atl_n, count_if(s.code = 'ATLHOLD' and hrs > 24) atl_24,
  count_if(f.td = 'Staging') stg_n, round(100 * count_if(f.td = 'Staging' and hrs > 24) / nullif(count_if(f.td = 'Staging' and hrs is not null), 0), 1) stg_pct24,
  count(distinct iff(f.td = 'Hold' and hrs > 24, s.code, null)) hold_sites_with_24
from s join f on f.code = s.code group by 1 order by 1;

-- [q13] statement 13
-- ICE hold-room stints over 24 hours, Oct 2025 - Feb 2026: distinct people, how the stint ended, what kind of place came next in the same stay, and the same for Oct 2024 - Feb 2025
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td, TYPE_GROUPED tg from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES),
s as (select STAY_ID, PERSON_HASH, DETENTION_FACILITY_CODE code, BOOK_IN_AT, BOOK_OUT_AT, DETENTION_RELEASE_REASON rr, GENDER, BIRTH_YEAR,
        datediff(minute, BOOK_IN_AT, BOOK_OUT_AT) / 60.0 hrs,
        lead(DETENTION_FACILITY_CODE) over (partition by STAY_ID order by BOOK_IN_AT, BOOK_OUT_AT) next_code
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_IN_AT >= '2024-10-01' and STAY_ID is not null),
h as (select s.*, iff(BOOK_IN_AT >= '2025-10-01', 'FY26', 'FY25') fy from s join f on f.code = s.code
      where f.td = 'Hold' and hrs > 24 and ((BOOK_IN_AT >= '2025-10-01' and BOOK_IN_AT < '2026-03-01') or (BOOK_IN_AT < '2025-03-01')))
select 'people' k, fy, count(*)::text a, count(distinct PERSON_HASH)::text b, count_if(GENDER = 'Female')::text c, count_if(BIRTH_YEAR >= 2008)::text d from h group by 2
union all select * from (select 'release_reason', fy, rr, count(*)::text, null, null from h group by 2, 3 order by 4 desc limit 16)
union all select 'next_place', fy, coalesce(nf.tg, iff(h.next_code is null, '(none: stay ended)', '(code not in lookup)')), count(*)::text, null, null from h left join f nf on nf.code = h.next_code group by 2, 3;

-- [q14] statement 14
-- SDWA within-state test: private groundwater community systems serving 25-500 people, mobile home parks (MH+MP) vs other residential (RA, SU, HA, OR, MU), per state; health-based and monitoring violations 2021-2025
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, PRIMACY_AGENCY_CODE st, POPULATION_SERVED_COUNT pop from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
      where PWS_ACTIVITY_CODE = 'A' and GW_SW_CODE = 'GW' and PWS_TYPE_CODE = 'CWS' and OWNER_TYPE_CODE = 'P' and POPULATION_SERVED_COUNT between 25 and 500),
v as (select PWSID, count(distinct iff(IS_HEALTH_BASED_IND = 'Y', VIOLATION_ID, null)) hb, count(distinct iff(VIOLATION_CATEGORY_CODE in ('MR', 'MON'), VIOLATION_ID, null)) mr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where COMPL_PER_BEGIN_DATE >= '2021-01-01' and COMPL_PER_BEGIN_DATE < '2026-01-01' and VIOLATION_ID is not null group by 1),
x as (select p.st, case when sa.code in ('MH', 'MP') then 'MHP' when sa.code in ('RA', 'SU', 'HA', 'OR', 'MU') then 'RES' end grp, iff(pop <= 100, 'small', 'mid') band,
        coalesce(v.hb, 0) > 0 anyhb, coalesce(v.mr, 0) > 0 anymr
      from p join sa on sa.PWSID = p.PWSID left join v on v.PWSID = p.PWSID where sa.code in ('MH', 'MP', 'RA', 'SU', 'HA', 'OR', 'MU')),
cell as (select st, band, count_if(grp = 'MHP') m_n, count_if(grp = 'MHP' and anyhb) m_hb, count_if(grp = 'MHP' and anymr) m_mr,
           count_if(grp = 'RES') r_n, count_if(grp = 'RES' and anyhb) r_hb, count_if(grp = 'RES' and anymr) r_mr from x group by 1, 2),
st as (select st, sum(m_n) m_n, sum(m_hb) m_hb, sum(m_mr) m_mr, sum(r_n) r_n, sum(r_hb) r_hb, sum(r_mr) r_mr,
          sum(iff(r_n > 0, m_n * r_hb / r_n, null)) m_hb_expected, sum(iff(r_n > 0, m_n * r_mr / r_n, null)) m_mr_expected from cell group by 1)
select * from (select 'state' k, st, m_n, m_hb, round(100 * m_hb / nullif(m_n, 0), 1) m_pct_hb, r_n, r_hb, round(100 * r_hb / nullif(r_n, 0), 1) r_pct_hb,
  round(100 * m_mr / nullif(m_n, 0), 1) m_pct_mr, round(100 * r_mr / nullif(r_n, 0), 1) r_pct_mr, round(m_hb_expected, 0) m_hb_exp from st where m_n >= 40 order by m_n desc limit 30)
union all select 'all_states_matched', null, sum(m_n), sum(m_hb), round(100 * sum(m_hb) / sum(m_n), 1), sum(r_n), sum(r_hb), round(100 * sum(r_hb) / sum(r_n), 1),
  round(100 * sum(m_mr) / sum(m_n), 1), round(100 * sum(m_mr_expected) / sum(m_n), 1), round(sum(m_hb_expected), 0) from st where r_n > 0 and m_n > 0
union all select 'states_mhp_worse_hb', null, count_if(m_n >= 40 and r_n >= 40), count_if(m_n >= 40 and r_n >= 40 and m_hb / m_n > r_hb / r_n), null,
  count_if(m_n >= 40 and r_n >= 40 and m_mr / m_n > r_mr / r_n), null, round(median(iff(m_n >= 40 and r_n >= 40, 100 * (m_hb / m_n - r_hb / r_n), null)), 1), null, null, null from st;

-- [q15] statement 15
-- ICE hold-room stints over 24 hours, Oct 2025 - Feb 2026: is the person booked somewhere else at the same time (a paper booking, not a body in the room)? overlap with any other stint of the same person at another code; by site for the top six
with f as (select DETENTION_FACILITY_CODE code, TYPE_DETAILED td from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_FACILITY_CODES),
all_s as (select STINT_ID, PERSON_HASH, DETENTION_FACILITY_CODE code, BOOK_IN_AT, coalesce(BOOK_OUT_AT, '2026-03-12'::timestamp) BOOK_OUT_AT
      from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_ICE_DETENTION_STINTS
      where coalesce(DUPLICATE_DROP_ROW, 'False') <> 'True' and BOOK_IN_AT >= '2025-06-01'),
h as (select a.* from all_s a join f on f.code = a.code
      where f.td = 'Hold' and a.BOOK_IN_AT >= '2025-10-01' and a.BOOK_IN_AT < '2026-03-01' and datediff(minute, a.BOOK_IN_AT, a.BOOK_OUT_AT) > 24 * 60),
ov as (select h.STINT_ID, max(datediff(minute, greatest(h.BOOK_IN_AT, o.BOOK_IN_AT), least(h.BOOK_OUT_AT, o.BOOK_OUT_AT))) / 60.0 ov_hrs
       from h join all_s o on o.PERSON_HASH = h.PERSON_HASH and o.STINT_ID <> h.STINT_ID and o.code <> h.code
         and o.BOOK_IN_AT < h.BOOK_OUT_AT and o.BOOK_OUT_AT > h.BOOK_IN_AT group by 1)
select iff(h.code in ('BALHOLD', 'IWAHOLD', 'DALHOLD', 'ATLHOLD', 'PHOHOLD', 'LOSHOLD'), h.code, 'all other hold sites') site,
  count(*) stints_over_24h, count(ov.STINT_ID) with_any_overlap, count_if(ov.ov_hrs > 1) overlap_over_1h, count_if(ov.ov_hrs > 12) overlap_over_12h,
  round(median(datediff(minute, h.BOOK_IN_AT, h.BOOK_OUT_AT)) / 60.0, 1) med_hrs
from h left join ov on ov.STINT_ID = h.STINT_ID group by 1 order by 2 desc;

-- [q16] statement 16
-- SDWA inside North Carolina and Texas (the two biggest mobile-home-park gaps): split by operator size (systems per ORG_NAME in the peer set) to test the dull reason (big professional operators run the subdivisions); plus top rules behind MHP health violations
with sa as (select PWSID, min(SERVICE_AREA_TYPE_CODE) code from LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_EPA_SDWA_SDWA_SERVICE_AREAS where IS_PRIMARY_SERVICE_AREA_CODE = 'Y' group by 1 having count(*) = 1),
p as (select PWSID, PRIMACY_AGENCY_CODE st, upper(trim(ORG_NAME)) org from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
      where PWS_ACTIVITY_CODE = 'A' and GW_SW_CODE = 'GW' and PWS_TYPE_CODE = 'CWS' and OWNER_TYPE_CODE = 'P' and POPULATION_SERVED_COUNT between 25 and 500 and PRIMACY_AGENCY_CODE in ('NC', 'TX')),
vv as (select PWSID, VIOLATION_ID, RULE_CODE, CONTAMINANT_CODE from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
      where COMPL_PER_BEGIN_DATE >= '2021-01-01' and COMPL_PER_BEGIN_DATE < '2026-01-01' and VIOLATION_ID is not null and IS_HEALTH_BASED_IND = 'Y' and (PWSID like 'NC%' or PWSID like 'TX%')),
v as (select PWSID, count(distinct VIOLATION_ID) hb from vv group by 1),
x as (select p.*, iff(sa.code in ('MH', 'MP'), 'MHP', 'RES') grp, coalesce(v.hb, 0) hb, count(*) over (partition by p.st, p.org) org_n
      from p join sa on sa.PWSID = p.PWSID left join v on v.PWSID = p.PWSID where sa.code in ('MH', 'MP', 'RA', 'SU', 'HA', 'OR', 'MU'))
select 'split' k, st, grp, iff(org_n >= 10, 'operator with 10+ systems', 'operator with <10') a, count(*)::text b, count_if(hb > 0)::text c, round(100 * count_if(hb > 0) / count(*), 1)::text d from x group by 2, 3, 4
union all select * from (select 'top_org', st, grp, org, count(*)::text, count_if(hb > 0)::text, sum(hb)::text from x group by 2, 3, 4 order by count(*) desc limit 16)
union all select * from (select 'mhp_rules', x.st, vv.RULE_CODE, vv.CONTAMINANT_CODE, count(distinct vv.PWSID||vv.VIOLATION_ID)::text, count(distinct vv.PWSID)::text, null from x join vv on vv.PWSID = x.PWSID where x.grp = 'MHP' group by 2, 3, 4 order by count(distinct vv.PWSID) desc limit 12);
