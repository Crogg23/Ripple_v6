-- deep3 / g37: proper look at five glance-only tables, 2026-09-24
-- Tables: ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES, ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS,
--         ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS, ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS,
--         ENVIRONMENT__FED_EPA_TRI_FACILITY
-- Door: Python (connect/db.py) via g37/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g37/<label>.json.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- NPDES facilities: keys, permit-type letter, impaired flag, facility types, placeholders, the FRS IDs that hold thousands of permits
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES)
select 'profile' k, count(*)::text a, count(distinct NPDES_ID)::text b, count(distinct FACILITY_UIN)::text c,
  count(distinct ICIS_FACILITY_INTEREST_ID)::text d, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text e,
  count_if(GEOCODE_LATITUDE is null or GEOCODE_LATITUDE=0)::text f, count(distinct STATE_CODE)::text g from t
union all select 'impaired_val', IMPAIRED_WATERS, count(*)::text, null, null, null, null, null from t group by 2
union all select 'ptype3', substr(NPDES_ID,3,1), count(*)::text, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text, count_if(FACILITY_TYPE_CODE='MWD')::text, null, null, null from t group by 2
union all select 'ftype', FACILITY_TYPE_CODE, count(*)::text, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text, count_if(substr(NPDES_ID,3,1)='0')::text, null, null, null from t group by 2
union all select * from (select 'topuin', FACILITY_UIN, count(*)::text, any_value(FACILITY_NAME), any_value(LOCATION_ADDRESS), listagg(distinct STATE_CODE, ',') within group (order by STATE_CODE), count(distinct FACILITY_NAME)::text, min(NPDES_ID)||'..'||max(NPDES_ID) from t group by 2 order by count(*) desc limit 6)
union all select * from (select 'state', STATE_CODE, count(*)::text, count_if(IMPAIRED_WATERS is not null and trim(IMPAIRED_WATERS)<>'')::text, count_if(substr(NPDES_ID,3,1)='0')::text, count_if(FACILITY_TYPE_CODE='MWD')::text, null, null from t group by 2 order by count(*) desc limit 70);

-- [q02] statement 2
-- NPDES quarterly noncompliance history: quarters covered, HLRNC codes, how many rows carry effluent violations
with q as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY)
select 'qtr' k, YEARQTR a, count(*) n, count(distinct NPDES_ID) m, count_if(try_to_number(NUME90_Q)>0) x, count_if(HLRNC in ('S','E')) y from q group by 2
union all select 'hlrnc', HLRNC, count(*), count(distinct NPDES_ID), count_if(try_to_number(NUME90_Q)>0), count_if(try_to_number(NUMD8090_Q)>0) from q group by 2
union all select 'e90vals', case when NUME90_Q is null then 'null' when try_to_number(NUME90_Q) is null then 'text:'||left(NUME90_Q,10) else 'num' end, count(*), max(try_to_number(NUME90_Q)), null, null from q group by 2
order by 1, 2;

-- [q03] statement 3
-- ICIS-Air programs: program x status, date text parse, the default date, mixed statuses per facility, duplicate rows
with t as (select *, try_to_date(BEGIN_DATE,'MM/DD/YYYY') bd, try_to_date(UPDATED_DATE,'MM/DD/YYYY') ud from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS),
f as (select PGM_SYS_ID, count(distinct AIR_OPERATING_STATUS_CODE) nst, count(*) n, count(distinct PROGRAM_CODE) np from t group by 1)
select 'profile' k, count(*)::text a, count(distinct PGM_SYS_ID)::text b, count_if(bd is null and BEGIN_DATE is not null)::text c, count_if(BEGIN_DATE is null)::text d,
  count_if(BEGIN_DATE='10/19/2014')::text e, count_if(ud is null)::text f, (select count_if(nst>1)||' mixed; '||count_if(n>np)||' dup-program' from f) g from t
union all select 'pgm_status', PROGRAM_CODE, AIR_OPERATING_STATUS_CODE, count(*)::text, count(distinct PGM_SYS_ID)::text, count_if(BEGIN_DATE='10/19/2014')::text, null, null from t group by 2,3
union all select 'begin_yr', year(bd)::text, count(*)::text, count_if(PROGRAM_CODE='CAATVP')::text, count_if(AIR_OPERATING_STATUS_CODE='CLS')::text, null, null, null from t group by 2
union all select 'upd_yr', year(ud)::text, count(*)::text, count_if(AIR_OPERATING_STATUS_CODE='CLS')::text, count_if(AIR_OPERATING_STATUS_CODE='OPR')::text, null, null, null from t group by 2
union all select * from (select 'topbegin', BEGIN_DATE, count(*)::text, null, null, null, null, null from t group by 2 order by count(*) desc limit 8);

-- [q04] statement 4
-- NRC secondary copy vs main copy: per-year counts, SEQNOS overlap, duplicate reports, the empty extra columns, blanks
with s as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS),
m as (select SEQNOS, DATE_TIME_RECEIVED, RESPONSIBLE_COMPANY from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS),
sy as (select year(DATE_TIME_RECEIVED) y, count(*) n, count(distinct SEQNOS) d, count_if(RESPONSIBLE_COMPANY is null or trim(RESPONSIBLE_COMPANY)='') blank from s group by 1),
my as (select year(DATE_TIME_RECEIVED) y, count(*) n, count(distinct SEQNOS) d, count_if(RESPONSIBLE_COMPANY is null or trim(RESPONSIBLE_COMPANY)='') blank from m group by 1)
select 'year' k, coalesce(sy.y,my.y)::text a, sy.n b, sy.d c, sy.blank d, my.n e, my.d f, my.blank g from sy full outer join my on sy.y=my.y
union all select 'overlap', 'secondary seqnos in main', count(distinct s.SEQNOS), count(distinct m.SEQNOS), count_if(s.DATE_TIME_RECEIVED=m.DATE_TIME_RECEIVED), count_if(coalesce(s.RESPONSIBLE_COMPANY,'')=coalesce(m.RESPONSIBLE_COMPANY,'')), null, null
  from s left join m on s.SEQNOS=m.SEQNOS
union all select 'extras', 'nonnull 1-5', count(EXTRA_COL_1), count(EXTRA_COL_2), count(EXTRA_COL_3), count(EXTRA_COL_4), count(EXTRA_COL_5), count(distinct _SOURCE_RUN_ID) from s
union all select 'calltype', CALL_TYPE||' / '||SOURCE, count(*), count(distinct SEQNOS), median(datediff('minute',DATE_TIME_RECEIVED,DATE_TIME_COMPLETE)), null, null, null from s group by 2
union all select 'orgtype', RESPONSIBLE_ORG_TYPE, count(*), count_if(RESPONSIBLE_COMPANY is null or trim(RESPONSIBLE_COMPANY)=''), null, null, null, null from s group by 2
order by 1, 2;

-- [q05] statement 5
-- TRI facility: IDs, closed flag, parents, and land rates into TRI 2023 releases and ECHO
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY),
b as (select distinct C_2_TRIFD id, C_3_FRS_ID frs from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023),
e as (select distinct FRS_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO)
select 'profile' k, count(*)::text a, count(distinct TRI_FACILITY_ID)::text b, count(distinct EPA_REGISTRY_ID)::text c,
  count_if(EPA_REGISTRY_ID is null or trim(EPA_REGISTRY_ID) = '')::text d, count(FRS_ID)::text e,
  count_if(PREF_LATITUDE is null)::text f, count_if(nullif(trim(STANDARDIZED_PARENT_COMPANY), '') is not null)::text g from t
union all select 'closed', FAC_CLOSED_IND, count(*)::text, count_if(TRI_FACILITY_ID in (select id from b))::text, count_if(EPA_REGISTRY_ID in (select FRS_ID from e))::text, null, null, null from t group by 2
union all select 'land', 'tri2023 ids in facility', (select count(*) from b)::text, (select count(*) from b where id in (select TRI_FACILITY_ID from t))::text,
   (select count(*) from b where frs in (select EPA_REGISTRY_ID from t))::text, null, null, null
union all select * from (select 'parent', STANDARDIZED_PARENT_COMPANY, count(*)::text, count_if(FAC_CLOSED_IND = '0')::text, count_if(TRI_FACILITY_ID in (select id from b))::text, count(distinct STATE_ABBR)::text, null, null from t
   where nullif(trim(STANDARDIZED_PARENT_COMPANY), '') is not null group by 2 order by count(*) desc limit 15)
union all select * from (select 'dupregid', EPA_REGISTRY_ID, count(*)::text, listagg(distinct FACILITY_NAME, ' | '), null, null, null, null from t where EPA_REGISTRY_ID is not null group by 2 having count(*) > 1 order by count(*) desc limit 5);

-- [q06] statement 6
-- SDWA geographic areas: confirm it is a crosswalk; area types, fill by type, rows per system, coverage of active community systems
with g as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_GEOGRAPHIC_AREAS),
p as (select PWSID, PWS_TYPE_CODE, PWS_ACTIVITY_CODE, POPULATION_SERVED_COUNT from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS),
gc as (select PWSID, count_if(AREA_TYPE_CODE = 'CN') cn, count(*) n from g group by 1)
select 'atype' k, AREA_TYPE_CODE a, count(*) b, count(distinct PWSID) c, count_if(nullif(trim(COUNTY_FIPS), '') is not null) d, count_if(ZIP_CODE_SERVED is not null) e, count_if(CITY_SERVED is not null) f from g group by 2
union all select 'quarter', SUBMISSIONYEARQUARTER, count(*), count(distinct PWSID), count(distinct GEO_ID), min(year(LAST_REPORTED_DATE)), max(year(LAST_REPORTED_DATE)) from g group by 2
union all select 'cws_cover', p.PWS_TYPE_CODE || '/' || p.PWS_ACTIVITY_CODE, count(*), count_if(gc.PWSID is not null), count_if(gc.cn > 0), sum(p.POPULATION_SERVED_COUNT), sum(iff(gc.cn > 0, p.POPULATION_SERVED_COUNT, 0)) from p left join gc on p.PWSID = gc.PWSID group by 2
union all select 'orphans', 'geo pwsid not in pws', count(distinct gc.PWSID), null, null, null, null from gc left join p on gc.PWSID = p.PWSID where p.PWSID is null;

-- [q07] statement 7
-- PHMSA flagged incidents: NRC report number fill and format, years, and land rate into both NRC copies
with ph as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS),
s as (select distinct SEQNOS from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS),
m as (select distinct SEQNOS from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS)
select INCIDENT_YEAR k, REPORT_TYPE a, count(*) n, count(distinct REPORT_NUMBER) reports, count_if(nullif(trim(NRC_REPORT_NUMBER), '') is not null) nrc_filled,
  count_if(trim(NRC_REPORT_NUMBER) in (select SEQNOS from s)) in_secondary, count_if(trim(NRC_REPORT_NUMBER) in (select SEQNOS from m)) in_main,
  min(NRC_REPORT_NUMBER) mn, max(NRC_REPORT_NUMBER) mx, sum(TOTAL_FATALITIES) fat, sum(TOTAL_INJURIES) inj
from ph group by 1, 2 order by 1, 2;

-- [q08] statement 8
-- NPDES formal enforcement actions: dates, agencies, penalties; and informal actions by year, to know what "enforcement" can mean
with fa as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS),
ia as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS)
select 'formal' k, iff(year(SETTLEMENT_ENTERED_DATE) < 2010, '<2010', coalesce(year(SETTLEMENT_ENTERED_DATE)::text, 'null')) a, AGENCY b,
  count(*) n, count(distinct NPDES_ID) permits, count(distinct ENF_IDENTIFIER) cases,
  sum(coalesce(FED_PENALTY_ASSESSED_AMT, 0)) fed_pen, sum(coalesce(STATE_LOCAL_PENALTY_AMT, 0)) st_pen, max(STATE_LOCAL_PENALTY_AMT) st_max
from fa group by 2, 3
union all
select 'informal', iff(year(ACHIEVED_DATE) < 2010, '<2010', coalesce(year(ACHIEVED_DATE)::text, 'null')), AGENCY, count(*), count(distinct NPDES_ID), count(distinct ENF_IDENTIFIER), null, null, null
from ia group by 2, 3
order by 1, 2, 3;

-- [q09] statement 9
-- NPDES chronic effluent violators by state: permits reporting 2023Q3-2026Q2, how many had effluent violations in 8+ of those 12 quarters,
-- how many of those also did in 8+ of the 12 quarters before, and how many got any formal action (since mid-2021, or ever) or informal action since mid-2021
with q as (
  select NPDES_ID,
    count_if(YEARQTR between '20233' and '20262') rep_a,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    sum(iff(YEARQTR between '20233' and '20262', try_to_number(NUME90_Q), 0)) ea,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' group by 1),
fa as (select NPDES_ID, count(*) n_all, count_if(SETTLEMENT_ENTERED_DATE >= '2021-07-01') n_recent,
         sum(coalesce(FED_PENALTY_ASSESSED_AMT, 0) + coalesce(STATE_LOCAL_PENALTY_AMT, 0)) pen
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS group by 1),
ia as (select NPDES_ID, count_if(ACHIEVED_DATE >= '2021-07-01') n_recent
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS group by 1),
f as (select NPDES_ID, STATE_CODE, FACILITY_TYPE_CODE, IMPAIRED_WATERS, substr(NPDES_ID, 3, 1) p3
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select f.*, q.rep_a, q.qa, q.ea, q.qb, coalesce(fa.n_all, 0) fa_all, coalesce(fa.n_recent, 0) fa_recent, coalesce(fa.pen, 0) pen,
         coalesce(ia.n_recent, 0) ia_recent
      from q left join f on q.NPDES_ID = f.NPDES_ID left join fa on q.NPDES_ID = fa.NPDES_ID left join ia on q.NPDES_ID = ia.NPDES_ID
      where q.rep_a > 0)
select coalesce(STATE_CODE, '(no facility row)') st, count(*) reporting, count_if(qa >= 8) chronic, count_if(qa >= 8 and qb >= 8) chronic6,
  count_if(qa >= 8 and fa_recent > 0) chr_formal_recent, count_if(qa >= 8 and fa_all > 0) chr_formal_ever,
  count_if(qa >= 8 and ia_recent > 0) chr_informal_recent, count_if(qa >= 8 and fa_all = 0 and ia_recent = 0) chr_nothing,
  count_if(qa >= 8 and FACILITY_TYPE_CODE = 'MWD') chr_mwd, count_if(qa >= 8 and p3 = '0') chr_individual,
  count_if(qa >= 8 and IMPAIRED_WATERS is not null) chr_impaired, count_if(IMPAIRED_WATERS is not null) rep_impaired,
  sum(iff(qa >= 8, ea, 0)) chr_e90, count_if(p3 = '0') rep_individual, count_if(p3 = '0' and qa >= 8) ind_chronic
from j group by rollup(coalesce(STATE_CODE, '(no facility row)')) order by chronic desc nulls first;

-- [q10] statement 10
-- ICIS-Air violation history joined to the programs table: HPV vs FRV rows by year, resolved share, and how many sit on operating Title V sources
with v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP', 1, 0)) tv, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr,
        max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr, min(iff(AIR_OPERATING_STATUS_CODE = 'CLS', 1, 0)) all_cls
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1)
select v.ENF_RESPONSE_POLICY_CODE k, year(coalesce(v.HPV_DAYZERO_DATE, v.EARLIEST_FRV_DETERM_DATE)) yr, count(*) n, count(distinct v.PGM_SYS_ID) fac,
  count(distinct v.ACTIVITY_ID) acts, count_if(v.HPV_DAYZERO_DATE is not null) dz, count_if(v.HPV_RESOLVED_DATE is not null) resolved,
  count_if(p.PGM_SYS_ID is not null) in_programs, count_if(p.tv_opr = 1) on_tv_opr, count_if(p.all_cls = 1) on_all_closed,
  count(distinct v.STATE_CODE) states, min(v.AGENCY_TYPE_DESC) ag_min, max(v.AGENCY_TYPE_DESC) ag_max
from v left join p on v.PGM_SYS_ID = p.PGM_SYS_ID
group by 1, 2 order by 1, 2;

-- [q11] statement 11
-- ICIS-Air by state: operating Title V sources (denominator, from the programs table), facilities with an HPV that began 2019-2022,
-- how many still have one open today, how many of those got no formal action since day zero; control: share of 2015-2018 HPV facilities ever resolved
with p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr,
             max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where ENF_RESPONSE_POLICY_CODE = 'HPV'),
h as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz, count(*) n_hpv, count_if(HPV_RESOLVED_DATE is null) n_open
      from v where HPV_DAYZERO_DATE between '2019-01-01' and '2022-12-31' group by 1),
old as (select PGM_SYS_ID, count(*) n, count_if(HPV_RESOLVED_DATE is not null) n_res from v where HPV_DAYZERO_DATE between '2015-01-01' and '2018-12-31' group by 1),
fa as (select h.PGM_SYS_ID, count(a.ACTIVITY_ID) n_fa, sum(coalesce(a.PENALTY_AMOUNT, 0)) pen
       from h left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a
         on a.PGM_SYS_ID = h.PGM_SYS_ID and a.SETTLEMENT_ENTERED_DATE >= h.dz group by 1),
u as (select PGM_SYS_ID from p union select PGM_SYS_ID from h union select PGM_SYS_ID from old),
j as (select u.PGM_SYS_ID, coalesce(f.st, '??') st, coalesce(p.tv_opr, 0) tv_opr, coalesce(p.any_opr, 0) any_opr,
        h.dz, h.n_hpv, h.n_open, fa.n_fa, fa.pen, old.n old_n, old.n_res old_res
      from u left join p on u.PGM_SYS_ID = p.PGM_SYS_ID left join f on u.PGM_SYS_ID = f.PGM_SYS_ID left join h on u.PGM_SYS_ID = h.PGM_SYS_ID
        left join fa on u.PGM_SYS_ID = fa.PGM_SYS_ID left join old on u.PGM_SYS_ID = old.PGM_SYS_ID)
select st, count_if(tv_opr = 1) tv_opr_fac, count_if(dz is not null) hpv_fac_19_22, count_if(dz is not null and tv_opr = 1) hpv_fac_tv,
  count_if(n_open > 0) open_fac, count_if(n_open > 0 and tv_opr = 1) open_fac_tv, count_if(n_open > 0 and coalesce(n_fa, 0) = 0) open_no_fa,
  count_if(n_open > 0 and any_opr = 0) open_fac_not_operating,
  count_if(dz is not null and coalesce(n_fa, 0) > 0) hpv_with_fa, sum(iff(dz is not null, pen, 0)) pen_since_dz,
  count_if(old_n > 0) old_fac, count_if(old_n > 0 and old_res > 0) old_fac_any_resolved, sum(old_n) old_hpv_rows, sum(old_res) old_res_rows
from j group by rollup(st) order by hpv_fac_19_22 desc nulls first;

-- [q12] statement 12
-- NPDES individual permits only (3rd character 0; the permits every state must report DMRs for):
-- per state, chronic (8+ of 12 quarters with effluent violations, 2023Q3-2026Q2), six-year chronic, formal action ever / since mid-2021, median violations;
-- plus the 40 six-year chronic individual permits with the most effluent violations and no formal action ever
with q as (
  select NPDES_ID,
    count_if(YEARQTR between '20233' and '20262') rep_a,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    sum(iff(YEARQTR between '20233' and '20262', try_to_number(NUME90_Q), 0)) ea,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1),
fa as (select NPDES_ID, count(*) n_all, count_if(SETTLEMENT_ENTERED_DATE >= '2021-07-01') n_recent, max(SETTLEMENT_ENTERED_DATE) last_dt,
         sum(coalesce(FED_PENALTY_ASSESSED_AMT, 0) + coalesce(STATE_LOCAL_PENALTY_AMT, 0)) pen
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS group by 1),
ia as (select NPDES_ID, count_if(ACHIEVED_DATE >= '2021-07-01') n_recent from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS group by 1),
f as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select q.*, f.STATE_CODE, f.FACILITY_NAME, f.CITY, f.FACILITY_TYPE_CODE, f.IMPAIRED_WATERS, f.FACILITY_UIN,
        coalesce(fa.n_all, 0) fa_all, coalesce(fa.n_recent, 0) fa_recent, fa.last_dt, coalesce(fa.pen, 0) pen, coalesce(ia.n_recent, 0) ia_recent
      from q left join f on q.NPDES_ID = f.NPDES_ID left join fa on q.NPDES_ID = fa.NPDES_ID left join ia on q.NPDES_ID = ia.NPDES_ID where q.rep_a > 0)
select 'state' k, coalesce(STATE_CODE, 'ALL') a, count(*)::text b, count_if(qa >= 8)::text c, count_if(qa >= 8 and qb >= 8)::text d,
  count_if(qa >= 8 and fa_all > 0)::text e, count_if(qa >= 8 and fa_recent > 0)::text f, count_if(qa >= 8 and qb >= 8 and fa_all = 0)::text g,
  count_if(qa >= 8 and FACILITY_TYPE_CODE = 'MWD')::text h, median(iff(qa >= 8, ea, null))::text i, count_if(qa >= 8 and ia_recent > 0)::text m,
  count_if(ia_recent > 0)::text n2
from j group by rollup(STATE_CODE)
union all
select * from (select 'top', NPDES_ID, FACILITY_NAME, CITY || ', ' || STATE_CODE, coalesce(FACILITY_TYPE_CODE, '-') || ' / ' || coalesce(IMPAIRED_WATERS, '-'),
  qa::text || '+' || qb::text, ea::text, ia_recent::text, FACILITY_UIN, null, null, null
  from j where qa >= 8 and qb >= 8 and fa_all = 0 order by ea desc limit 40);

-- [q13] statement 13
-- NRC secondary copy: company-by-year counts for the 30 companies with most reports 2020-2024 (names cleaned of punctuation),
-- plus 2019 and 2025 from the main copy for the before/after; biggest one-year jumps
with s as (select regexp_replace(upper(trim(RESPONSIBLE_COMPANY)), '[^A-Z0-9 ]', '') co, year(DATE_TIME_RECEIVED) y, RESPONSIBLE_ORG_TYPE ot
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS where nullif(trim(RESPONSIBLE_COMPANY), '') is not null),
m as (select regexp_replace(upper(trim(RESPONSIBLE_COMPANY)), '[^A-Z0-9 ]', '') co, year(DATE_TIME_RECEIVED) y
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS where year(DATE_TIME_RECEIVED) in (2019, 2025) and nullif(trim(RESPONSIBLE_COMPANY), '') is not null),
sc as (select co, count(*) tot, count_if(y = 2020) y20, count_if(y = 2021) y21, count_if(y = 2022) y22, count_if(y = 2023) y23, count_if(y = 2024) y24, any_value(ot) ot from s group by 1),
mc as (select co, count_if(y = 2019) y19, count_if(y = 2025) y25 from m group by 1),
k as (select sc.*, coalesce(mc.y19, 0) y19, coalesce(mc.y25, 0) y25,
        greatest(y20, y21, y22, y23, y24) mx, least(y20, y21, y22, y23, y24) mn from sc left join mc on sc.co = mc.co)
select * from (select 'top' t, * from k order by tot desc limit 30)
union all
select * from (select 'jump' t, * from k where tot >= 60 order by mx / (mn + 1) desc limit 15);

-- [q14] statement 14
-- PHMSA gas transmission/gathering accidents 2020-2024 joined to the NRC secondary copy on report number:
-- hours from the accident's local time (shifted to Eastern by TIME_ZONE) to the NRC call; plus operators who wrote "required but not made"
with ph as (select *, row_number() over (partition by REPORT_NUMBER order by SUPPLEMENTAL_NUMBER desc nulls last) rn
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_PHMSA_FLAGGED_INCIDENTS),
p as (select * from ph where rn = 1),
n as (select SEQNOS, DATE_TIME_RECEIVED, RESPONSIBLE_COMPANY from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENT_REPORTS),
j as (select p.REPORT_NUMBER, p.OPERATOR_NAME, p.INCIDENT_YEAR, p.LOCAL_DATETIME, p.TIME_ZONE, p.TOTAL_FATALITIES, p.TOTAL_INJURIES, p.COMMODITY_RELEASED_TYPE,
        p.UNINTENTIONAL_RELEASE_VOLUME, p.OPERATOR_STATE, n.DATE_TIME_RECEIVED, n.RESPONSIBLE_COMPANY,
        datediff('minute', dateadd('hour', case upper(p.TIME_ZONE) when 'EASTERN' then 0 when 'CENTRAL' then 1 when 'MOUNTAIN' then 2 when 'PACIFIC' then 3
                    when 'ALASKA' then 4 when 'HAWAII' then 6 else 1 end, p.LOCAL_DATETIME), n.DATE_TIME_RECEIVED) / 60.0 lag_h
      from p join n on trim(p.NRC_REPORT_NUMBER) = n.SEQNOS)
select 'bucket' k, case when lag_h < 0 then 'a <0h' when lag_h <= 1 then 'b 0-1h' when lag_h <= 2 then 'c 1-2h' when lag_h <= 6 then 'd 2-6h'
    when lag_h <= 24 then 'e 6-24h' when lag_h <= 168 then 'f 1-7d' else 'g >7d' end a, count(*)::text b, count_if(TIME_ZONE is null)::text c,
  sum(TOTAL_FATALITIES)::text d, sum(TOTAL_INJURIES)::text e, null f, null g, null h
from j group by 2
union all
select * from (select 'late', REPORT_NUMBER, OPERATOR_NAME, LOCAL_DATETIME::text || ' ' || coalesce(TIME_ZONE, '?'), DATE_TIME_RECEIVED::text, round(lag_h, 1)::text,
  coalesce(TOTAL_FATALITIES, 0)::text || 'd/' || coalesce(TOTAL_INJURIES, 0)::text || 'i', COMMODITY_RELEASED_TYPE, UNINTENTIONAL_RELEASE_VOLUME::text
  from j where lag_h > 24 order by lag_h desc limit 25)
union all
select * from (select 'op', OPERATOR_NAME, count(*)::text, median(lag_h)::text, count_if(lag_h > 6)::text, count_if(lag_h > 24)::text, null, null, null
  from j group by 2 having count(*) >= 5 order by median(lag_h) desc limit 20)
union all
select 'notmade', OPERATOR_NAME, count(*)::text, listagg(distinct INCIDENT_YEAR::text, ',') within group (order by INCIDENT_YEAR::text), sum(TOTAL_FATALITIES)::text, sum(TOTAL_INJURIES)::text,
  listagg(distinct REPORT_NUMBER, ',') within group (order by REPORT_NUMBER), null, null
from p where NRC_REPORT_NUMBER ilike '%NOT MADE%' group by 2
union all
select 'nrcvals', iff(try_to_number(trim(NRC_REPORT_NUMBER)) is null, coalesce(NRC_REPORT_NUMBER, '(null)'), 'numeric'), count(*)::text, null, null, null, null, null, null from p group by 2;

-- [q15] statement 15
-- TRI facility -> ECHO (EPA_REGISTRY_ID = FRS_ID) -> 2023 TRI industry sector: parent companies with 15+ open TRI facilities,
-- share of their facilities out of compliance 6+ of the last 12 quarters, and formal actions; grouped by sector so parents meet their peers
with t as (select TRI_FACILITY_ID, EPA_REGISTRY_ID, STANDARDIZED_PARENT_COMPANY par from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY
           where FAC_CLOSED_IND = '0' and nullif(trim(STANDARDIZED_PARENT_COMPANY), '') is not null),
e as (select FRS_ID, max(QUARTERS_WITH_NONCOMPLIANCE) qnc, max(FORMAL_ACTION_COUNT) fac, count(*) erows
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select EPA_REGISTRY_ID from t) group by 1),
s as (select C_2_TRIFD id, any_value(C_23_INDUSTRY_SECTOR) sector, sum(C_65_ON_SITE_RELEASE_TOTAL) onsite
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 group by 1),
j as (select t.*, e.qnc, e.fac, e.erows, s.sector, s.onsite from t left join e on t.EPA_REGISTRY_ID = e.FRS_ID left join s on t.TRI_FACILITY_ID = s.id)
select 'parent' k, par, count(*) fac_n, count_if(qnc is not null) in_echo, count_if(qnc >= 6) qnc6, avg(qnc) avg_qnc, sum(fac) formal,
  count_if(sector is not null) filed23, mode(sector) top_sector, sum(onsite) onsite_lb, max(erows) max_erows
from j group by 2 having count(*) >= 15
union all
select 'sector', sector, count(*), count_if(qnc is not null), count_if(qnc >= 6), avg(qnc), sum(fac), count(*), null, sum(onsite), max(erows)
from j where sector is not null group by 2
union all
select 'all', 'open TRI facilities with a parent', count(*), count_if(qnc is not null), count_if(qnc >= 6), avg(qnc), sum(fac), count_if(sector is not null), null, sum(onsite), max(erows) from j
order by 1, 5 desc;

-- [q16] statement 16
-- ICIS-Air eyeball: Nebraska's 2019-2022 HPVs (who found them, dates, programs, status), Nebraska and Wisconsin formal actions by year,
-- and which states the bulk BEGIN_DATE values belong to
with v as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY where ENF_RESPONSE_POLICY_CODE = 'HPV'),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(FACILITY_NAME) nm, any_value(CITY) city, any_value(CURRENT_HPV) chpv, any_value(NAICS_CODES) naics
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
p as (select PGM_SYS_ID, listagg(distinct PROGRAM_CODE || ':' || AIR_OPERATING_STATUS_CODE, ',') within group (order by PROGRAM_CODE || ':' || AIR_OPERATING_STATUS_CODE) pgms
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
a as (select a.*, f.st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS a left join f on a.PGM_SYS_ID = f.PGM_SYS_ID)
select * from (select 'ne_hpv' k, v.PGM_SYS_ID a, f.nm b, f.city || ' / ' || coalesce(f.naics, '') c, v.AGENCY_TYPE_DESC d, v.HPV_DAYZERO_DATE::text e,
  coalesce(v.HPV_RESOLVED_DATE::text, 'open') g, left(v.PROGRAM_DESCS, 60) || ' | ' || left(coalesce(v.POLLUTANT_DESCS, ''), 40) h, p.pgms || ' | hpv=' || coalesce(f.chpv, '') i
  from v left join f on v.PGM_SYS_ID = f.PGM_SYS_ID left join p on v.PGM_SYS_ID = p.PGM_SYS_ID
  where f.st = 'NE' and v.HPV_DAYZERO_DATE >= '2015-01-01' order by v.HPV_DAYZERO_DATE limit 45)
union all
select 'fa_by_year', st, year(SETTLEMENT_ENTERED_DATE)::text, count(*)::text, count(distinct PGM_SYS_ID)::text, sum(coalesce(PENALTY_AMOUNT, 0))::text, listagg(distinct STATE_EPA_FLAG, ','), null, null
from a where st in ('NE', 'WI') and (SETTLEMENT_ENTERED_DATE >= '2015-01-01' or SETTLEMENT_ENTERED_DATE is null) group by 2, 3
union all
select * from (select 'bulkdate', pr.BEGIN_DATE, f.st, count(*)::text, count(distinct pr.PGM_SYS_ID)::text, listagg(distinct pr.PROGRAM_CODE, ',') within group (order by pr.PROGRAM_CODE), null, null, null
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS pr left join f on pr.PGM_SYS_ID = f.PGM_SYS_ID
  where pr.BEGIN_DATE in ('09/29/2025', '03/19/2026', '10/27/2015', '01/01/1969') group by 2, 3 qualify row_number() over (partition by pr.BEGIN_DATE order by count(*) desc) <= 3);

-- [q17] statement 17
-- NPDES Missouri and Ohio eyeball: six-year chronic individual permits with no formal action on that permit.
-- Robustness: formal actions on ANY permit sharing the same FRS ID; informal actions ever; compliance-schedule or permit-schedule records; facility type
with q as (
  select NPDES_ID,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    sum(iff(YEARQTR between '20233' and '20262', try_to_number(NUME90_Q), 0)) ea,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb,
    sum(iff(YEARQTR between '20203' and '20232', try_to_number(NUME90_Q), 0)) eb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1 having qa >= 8 and qb >= 8),
fac as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
fa as (select NPDES_ID, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS group by 1),
fa_uin as (select f2.FACILITY_UIN, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS a
           join fac f2 on a.NPDES_ID = f2.NPDES_ID where f2.FACILITY_UIN is not null group by 1),
ia as (select NPDES_ID, count(*) n, max(ACHIEVED_DATE) last_ia from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS group by 1),
cs as (select NPDES_ID, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_CS_VIOLATIONS group by 1),
ps as (select NPDES_ID, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_PS_VIOLATIONS group by 1),
j as (select q.*, f.STATE_CODE st, f.FACILITY_NAME, f.CITY, f.FACILITY_TYPE_CODE ft, f.IMPAIRED_WATERS imp, f.FACILITY_UIN,
        coalesce(fa.n, 0) fa_n, coalesce(fu.n, 0) fa_uin_n, coalesce(ia.n, 0) ia_n, ia.last_ia, coalesce(cs.n, 0) cs_n, coalesce(ps.n, 0) ps_n
      from q join fac f on q.NPDES_ID = f.NPDES_ID left join fa on q.NPDES_ID = fa.NPDES_ID left join fa_uin fu on f.FACILITY_UIN = fu.FACILITY_UIN
        left join ia on q.NPDES_ID = ia.NPDES_ID left join cs on q.NPDES_ID = cs.NPDES_ID left join ps on q.NPDES_ID = ps.NPDES_ID)
select 'sum' k, st a, count(*)::text b, count_if(fa_n = 0)::text c, count_if(fa_n = 0 and fa_uin_n = 0)::text d, count_if(fa_n = 0 and ia_n = 0)::text e,
  count_if(fa_n = 0 and (cs_n > 0 or ps_n > 0))::text g, count_if(fa_n = 0 and ft = 'MWD')::text h, count_if(fa_n = 0 and ft in ('CTG', 'MWD', 'STF', 'FDF'))::text i,
  median(iff(fa_n = 0, ea + eb, null))::text m
from j group by rollup(st) having count(*) >= 40 or st is null
union all
select * from (select 'row', NPDES_ID, FACILITY_NAME || ' / ' || CITY, coalesce(ft, '-') || ' / ' || coalesce(imp, '-'), qa::text || '+' || qb::text || ' q; ' || ea::text || '+' || eb::text || ' viol',
  'fa_uin=' || fa_uin_n::text, 'ia=' || ia_n::text || ' last ' || coalesce(last_ia::text, '-'), 'cs=' || cs_n::text || ' ps=' || ps_n::text, st, null
  from j where st in ('MO', 'OH') and fa_n = 0 order by st, ea + eb desc limit 30);

-- [q18] statement 18
-- TRI peer group: ethanol plants (primary NAICS 325193 in the 2023 TRI file). Per parent: plants, ECHO match, quarters out of compliance,
-- formal actions; plus each POET plant's ECHO row (programs, 12-quarter history string) to see what kind of violation it is
with b as (select C_2_TRIFD id, any_value(C_30_PRIMARY_NAICS) naics from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 group by 1),
t as (select t.TRI_FACILITY_ID, t.EPA_REGISTRY_ID, t.FACILITY_NAME, t.CITY_NAME, t.STATE_ABBR, coalesce(nullif(trim(t.STANDARDIZED_PARENT_COMPANY), ''), '(no parent)') par
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY t join b on t.TRI_FACILITY_ID = b.id where b.naics = '325193' and t.FAC_CLOSED_IND = '0'),
e as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO where FRS_ID in (select EPA_REGISTRY_ID from t)),
j as (select t.*, e.QUARTERS_WITH_NONCOMPLIANCE qnc, e.FORMAL_ACTION_COUNT fac, e.THREE_YR_COMPLIANCE_HISTORY h, e.HAS_AIR_PROGRAM air, e.HAS_WATER_PROGRAM wat,
        e.COMPLIANCE_STATUS cst, e.LAST_PENALTY_AMT_ALLOCATED pen, e.DATE_LAST_FORMAL_ACTION dlfa
      from t left join e on t.EPA_REGISTRY_ID = e.FRS_ID)
select 'par' k, par a, count(*)::text b, count_if(qnc is not null)::text c, count_if(qnc >= 6)::text d, round(avg(qnc), 2)::text e, sum(fac)::text f,
  count_if(qnc >= 1)::text g, null h, null i
from j group by rollup(par) having count(*) >= 4 or par is null
union all
select * from (select 'poet', FACILITY_NAME, CITY_NAME || ', ' || STATE_ABBR, qnc::text, h, fac::text, 'air=' || air::text || ' water=' || wat::text, cst, coalesce(pen::text, '-') || ' ' || coalesce(dlfa::text, '-'), EPA_REGISTRY_ID
  from j where par ilike 'POET%' order by qnc desc nulls last limit 40);

-- [q19] statement 19
-- NRC name variants: every spelling containing NORFOLK SOUTHERN, COX, TARGA per year in the main copy 2017-2025,
-- to test whether the company-level breaks in the secondary copy are real or name drift
with m as (select upper(trim(RESPONSIBLE_COMPANY)) co, year(DATE_TIME_RECEIVED) y
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS
           where year(DATE_TIME_RECEIVED) between 2017 and 2025
             and (RESPONSIBLE_COMPANY ilike '%NORFOLK SOUTHERN%' or RESPONSIBLE_COMPANY ilike 'COX %' or RESPONSIBLE_COMPANY ilike '%TARGA%')),
m2 as (select case when co like '%NORFOLK%' then 'NS' when co like '%TARGA%' then 'TARGA' else 'COX' end fam, co, y from m)
select fam, co,
  count_if(y = 2017) y17, count_if(y = 2018) y18, count_if(y = 2019) y19, count_if(y = 2020) y20, count_if(y = 2021) y21,
  count_if(y = 2022) y22, count_if(y = 2023) y23, count_if(y = 2024) y24, count_if(y = 2025) y25, count(*) tot
from m2 group by rollup(fam, co) having count(*) >= 5 order by fam, tot desc;

-- [q20] statement 20
-- ICIS-Air peer check: facilities flagged Unaddressed HPV today (facility table CURRENT_HPV), per state,
-- against operating Title V sources and all operating facilities from the programs table; plus the national CURRENT_HPV value list
with p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr,
             max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st, any_value(CURRENT_HPV) chpv from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
j as (select f.*, coalesce(p.tv_opr, 0) tv_opr, coalesce(p.any_opr, 0) any_opr from f left join p on f.PGM_SYS_ID = p.PGM_SYS_ID)
select 'state' k, st a, count_if(tv_opr = 1) tv_opr, count_if(any_opr = 1) any_opr, count_if(chpv ilike 'Unaddressed%') unaddr,
  count_if(chpv ilike 'Unaddressed%' and tv_opr = 1) unaddr_tv, count_if(chpv ilike 'Unaddressed-State%') unaddr_state,
  count_if(chpv ilike 'Unaddressed%' and any_opr = 0) unaddr_not_operating, count_if(chpv ilike 'Addressed%') addressed
from j group by 2 having count_if(chpv ilike 'Unaddressed%') > 0 or st in ('TX', 'PA', 'OH', 'IN', 'IA', 'KS', 'MO', 'SD', 'MN')
union all
select 'value', chpv, count(*), count_if(tv_opr = 1), count_if(any_opr = 1), null, null, null, null from j group by 2
order by 1, 5 desc;

-- [q21] statement 21
-- NPDES data-flow test for the Missouri/Ohio gap: formal and informal actions on individual permits per year, MO, OH vs all other states.
-- If MO or OH simply stopped sending actions to ICIS, their yearly counts would fall to near zero
with fa as (select substr(NPDES_ID, 1, 2) st, year(SETTLEMENT_ENTERED_DATE) y, count(*) n, count(distinct NPDES_ID) permits
            from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS
            where substr(NPDES_ID, 3, 1) = '0' and year(SETTLEMENT_ENTERED_DATE) between 2012 and 2026 group by 1, 2),
ia as (select substr(NPDES_ID, 1, 2) st, year(ACHIEVED_DATE) y, count(*) n
       from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS
       where substr(NPDES_ID, 3, 1) = '0' and year(ACHIEVED_DATE) between 2012 and 2026 group by 1, 2)
select coalesce(fa.y, ia.y) y,
  sum(iff(coalesce(fa.st, ia.st) = 'MO', fa.n, 0)) mo_formal, sum(iff(coalesce(fa.st, ia.st) = 'MO', ia.n, 0)) mo_informal,
  sum(iff(coalesce(fa.st, ia.st) = 'OH', fa.n, 0)) oh_formal, sum(iff(coalesce(fa.st, ia.st) = 'OH', ia.n, 0)) oh_informal,
  sum(iff(coalesce(fa.st, ia.st) not in ('MO', 'OH'), fa.n, 0)) rest_formal, sum(iff(coalesce(fa.st, ia.st) not in ('MO', 'OH'), ia.n, 0)) rest_informal,
  sum(iff(coalesce(fa.st, ia.st) = 'TX', fa.n, 0)) tx_formal, sum(iff(coalesce(fa.st, ia.st) = 'PA', fa.n, 0)) pa_formal
from fa full outer join ia on fa.st = ia.st and fa.y = ia.y
group by 1 order by 1;

-- [q22] statement 22
-- NRC main copy, rail peers by year 2015-2025: Norfolk Southern (any spelling incl. NS abbreviations) vs CSX, Union Pacific, BNSF,
-- all railroads by org name, and the org type / source of NS calls, to test whether NS's 2020 fall is name drift
with m as (select upper(trim(RESPONSIBLE_COMPANY)) co, year(DATE_TIME_RECEIVED) y, RESPONSIBLE_ORG_TYPE ot, SOURCE src
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS where year(DATE_TIME_RECEIVED) between 2015 and 2025),
c as (select y, ot, src,
        case when co like '%NORFOLK SOUTHERN%' or co like '%NORFOLK SO%' or co like 'NS RAIL%' or co like 'N S RAIL%' or co like 'NSRR%' or co = 'NS' or co like 'NS %' then 'NS'
             when co like '%CSX%' then 'CSX' when co like '%UNION PACIFIC%' or co like 'UPRR%' then 'UP' when co like '%BNSF%' or co like '%BURLINGTON NORTHERN%' then 'BNSF'
             when co like '%CANADIAN NATIONAL%' or co like 'CN RAIL%' then 'CN' when co like '%RAIL%' then 'OTHER_RAIL' else null end fam, co
      from m)
select fam, count_if(y = 2015) y15, count_if(y = 2016) y16, count_if(y = 2017) y17, count_if(y = 2018) y18, count_if(y = 2019) y19,
  count_if(y = 2020) y20, count_if(y = 2021) y21, count_if(y = 2022) y22, count_if(y = 2023) y23, count_if(y = 2024) y24, count_if(y = 2025) y25,
  count(distinct co) spellings, listagg(distinct iff(y in (2019, 2020), ot || '/' || src, null), '; ') types_19_20
from c where fam is not null group by 1 order by 1;

-- [q23] statement 23
-- NRC main copy: Norfolk Southern (any spelling) calls by month 2018-2021 and by responsible state 2019 vs 2020, with CSX alongside,
-- to see whether the 2020 fall is a one-month switch (practice or data change) or a slide, and whether 2019's peak is one place
with m as (select upper(trim(RESPONSIBLE_COMPANY)) co, DATE_TIME_RECEIVED d, RESPONSIBLE_STATE st
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_USCG_NRC_INCIDENTS where year(DATE_TIME_RECEIVED) between 2018 and 2021),
c as (select d, st, case when co like '%NORFOLK SOUTHERN%' or co like '%NORFOLK SO%' or co like 'NS RAIL%' or co like 'N S RAIL%' or co like 'NSRR%' or co = 'NS' or co like 'NS %' then 'NS'
                         when co like '%CSX%' then 'CSX' else null end fam from m)
select 'month' k, to_char(date_trunc('month', d), 'YYYY-MM') a, count_if(fam = 'NS') ns, count_if(fam = 'CSX') csx, count(*) all_calls from c group by 2
union all
select 'state', st, count_if(fam = 'NS' and year(d) = 2019), count_if(fam = 'NS' and year(d) = 2020), count_if(fam = 'CSX' and year(d) = 2019) from c
where fam is not null group by 2 having count_if(fam = 'NS') >= 10
order by 1, 2;

-- [q24] statement 24
-- NPDES sensitivity: does the Missouri/Ohio share of chronic-with-no-formal-action survive other thresholds?
-- Individual permits; thresholds 6, 8, 10 of 12 quarters in both windows; share of no-formal-action permits in MO, OH, rest; plus MO/OH/all impaired and MWD counts at 8
with q as (
  select NPDES_ID, substr(NPDES_ID, 1, 2) st,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1, 2),
fa as (select distinct NPDES_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS),
f as (select NPDES_ID, FACILITY_TYPE_CODE ft, IMPAIRED_WATERS imp from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select q.*, iff(fa.NPDES_ID is null, 1, 0) nofa, f.ft, f.imp from q left join fa on q.NPDES_ID = fa.NPDES_ID left join f on q.NPDES_ID = f.NPDES_ID),
t as (select 6 thr union all select 8 union all select 10 union all select 12)
select t.thr, iff(j.st in ('MO', 'OH'), j.st, 'REST') grp, count(*) chronic_both, sum(nofa) no_formal, round(sum(nofa) / count(*), 3) share_no_formal,
  count_if(nofa = 1 and imp is not null) no_formal_impaired, count_if(nofa = 1 and ft = 'MWD') no_formal_mwd
from j join t on j.qa >= t.thr and j.qb >= t.thr
group by 1, 2 order by 1, 2;

-- [q25] statement 25
-- ICIS-Air sensitivity: HPV facilities with day zero before 2024-07-01 (so past EPA's 180-day window by far), still unresolved,
-- with NO formal action on file at any date (null settlement dates included), by state; denominator operating Title V sources
with v as (select PGM_SYS_ID, min(HPV_DAYZERO_DATE) dz from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY
           where ENF_RESPONSE_POLICY_CODE = 'HPV' and HPV_RESOLVED_DATE is null and HPV_DAYZERO_DATE < '2024-07-01' group by 1),
fa as (select PGM_SYS_ID, count(*) n, count_if(SETTLEMENT_ENTERED_DATE is null) n_nulldate from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS group by 1),
p as (select PGM_SYS_ID, max(iff(PROGRAM_CODE = 'CAATVP' and AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) tv_opr, max(iff(AIR_OPERATING_STATUS_CODE = 'OPR', 1, 0)) any_opr
      from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS group by 1),
f as (select PGM_SYS_ID, any_value(STATE) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES group by 1),
j as (select coalesce(f.st, '??') st, p.PGM_SYS_ID, coalesce(p.tv_opr, 0) tv_opr, coalesce(p.any_opr, 0) any_opr, v.dz, coalesce(fa.n, 0) fa_n, coalesce(fa.n_nulldate, 0) fa_null
      from p left join f on p.PGM_SYS_ID = f.PGM_SYS_ID left join v on p.PGM_SYS_ID = v.PGM_SYS_ID left join fa on p.PGM_SYS_ID = fa.PGM_SYS_ID)
select st, count_if(tv_opr = 1) tv_opr, count_if(dz is not null and any_opr = 1) open_old_operating, count_if(dz is not null and any_opr = 1 and fa_n = 0) open_old_no_fa_ever,
  count_if(dz is not null and any_opr = 1 and fa_n = 0 and tv_opr = 1) same_on_tv, min(iff(dz is not null and any_opr = 1 and fa_n = 0, dz, null)) oldest_dz,
  count_if(fa_null > 0) fac_with_nulldate_fa
from j group by rollup(st) having count_if(dz is not null and any_opr = 1) > 0 or st is null order by open_old_no_fa_ever desc nulls first;

-- [q26] statement 26
-- TRI facility traps: coordinate formats (the DDMMSS / positive-longitude trap), closed-flag facilities that still filed for 2023, blank parents
with t as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY),
b as (select C_2_TRIFD id, any_value(C_4_FACILITY_NAME) nm, sum(C_65_ON_SITE_RELEASE_TOTAL) onsite from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_BASIC_2023 group by 1)
select 'coords' k, count_if(FAC_LATITUDE > 1000)::text a, count_if(FAC_LATITUDE between 1 and 90)::text b, count_if(FAC_LATITUDE = 0 or FAC_LATITUDE is null)::text c,
  count_if(PREF_LONGITUDE > 0)::text d, count_if(PREF_LONGITUDE < 0)::text e, count_if(PREF_ACCURACY = '99999.00')::text f, count_if(nullif(trim(PARENT_CO_NAME), '') is null)::text g from t
union all
select * from (select 'closed_filed', t.TRI_FACILITY_ID, t.FACILITY_NAME, t.CITY_NAME || ', ' || t.STATE_ABBR, round(b.onsite)::text, t.FAC_CLOSED_IND, t.STANDARDIZED_PARENT_COMPANY, null
  from t join b on t.TRI_FACILITY_ID = b.id where t.FAC_CLOSED_IND = '1' order by b.onsite desc nulls last limit 8);

-- [q27] statement 27
-- Second-table cross-check on named examples: ECHO's own row (formal actions, penalties, status) for the top Missouri no-action permits
-- and the Nebraska HPV plants named in the write-up, plus each NPDES permit's primary SIC
with ids as (select column1 id, column2 lbl from values
  ('110009339288', 'MO0098752 Madison Mine'), ('110006728292', 'MO0104256 Leadwood WWTP'), ('110009872094', 'MO0107719 Center WWTF'),
  ('110012962357', 'MO0035742 Lake Forest CWD'), ('110009823236', 'OH0021032 Bloomville WWTP')),
air as (select REGISTRY_ID id, PGM_SYS_ID || ' ' || FACILITY_NAME lbl from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES
        where PGM_SYS_ID in ('NE0000003114100032', 'NE0000003105900030', 'NE0000003108100030', 'NE0000003107900144', 'NE0000003105300146')),
allids as (select * from ids union all select * from air),
sic as (select NPDES_ID, listagg(SIC_CODE || ' ' || SIC_DESC, '; ') s from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SICS
        where NPDES_ID in ('MO0098752', 'MO0104256', 'MO0107719', 'MO0035742', 'OH0021032') and PRIMARY_INDICATOR_FLAG = 'Y' group by 1)
select a.lbl, e.FRS_ID, e.FACILITY_NAME, e.CITY || ', ' || e.STATE loc, e.COMPLIANCE_STATUS, e.QUARTERS_WITH_NONCOMPLIANCE qnc, e.THREE_YR_COMPLIANCE_HISTORY h,
  e.FORMAL_ACTION_COUNT fac, e.INFORMAL_ACTION_COUNT iac, e.DATE_LAST_FORMAL_ACTION dlfa, e.LAST_PENALTY_AMT_ALLOCATED pen, e.IS_MAJOR_FACILITY major, e.PCT_MINORITY pct_min,
  sic.s primary_sic
from allids a left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on a.id = e.FRS_ID
  left join sic on left(a.lbl, 9) = sic.NPDES_ID
order by 1;

-- [q28] statement 28
-- Robustness for the NPDES lead against a second table: six-year chronic individual permits with no NPDES formal action,
-- joined to ECHO by FRS ID. How many does ECHO say had any formal action (any program), and do those sites also carry drinking-water or air programs?
with q as (
  select NPDES_ID, substr(NPDES_ID, 1, 2) st,
    count_if(YEARQTR between '20233' and '20262' and try_to_number(NUME90_Q) > 0) qa,
    count_if(YEARQTR between '20203' and '20232' and try_to_number(NUME90_Q) > 0) qb
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where YEARQTR between '20203' and '20262' and substr(NPDES_ID, 3, 1) = '0' group by 1, 2 having qa >= 8 and qb >= 8),
fa as (select distinct NPDES_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS),
f as (select NPDES_ID, FACILITY_UIN from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
j as (select iff(q.st in ('MO', 'OH'), q.st, 'REST') grp, q.NPDES_ID, e.FRS_ID, e.FORMAL_ACTION_COUNT fac, e.DATE_LAST_FORMAL_ACTION dlfa,
        e.HAS_DRINKING_WATER_PROGRAM dw, e.HAS_AIR_PROGRAM air, e.HAS_HAZWASTE_PROGRAM rcra, e.QUARTERS_WITH_NONCOMPLIANCE qnc
      from q left join fa on q.NPDES_ID = fa.NPDES_ID left join f on q.NPDES_ID = f.NPDES_ID left join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ECHO e on f.FACILITY_UIN = e.FRS_ID
      where fa.NPDES_ID is null)
select grp, count(*) no_npdes_formal, count(FRS_ID) in_echo, count_if(fac > 0) echo_formal_any, count_if(fac > 0 and dlfa >= '2021-07-01') echo_formal_recent,
  count_if(fac > 0 and (dw or air or rcra)) echo_formal_multi_program, count_if(fac > 0 and not (coalesce(dw, false) or coalesce(air, false) or coalesce(rcra, false))) echo_formal_water_only,
  count_if(qnc >= 8) echo_qnc8
from j group by rollup(grp) order by grp;
