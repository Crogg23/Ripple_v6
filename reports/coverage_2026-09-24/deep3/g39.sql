-- deep3 / g39: proper look at five glance-only tables, 2026-09-24
-- Tables: ENVIRONMENT__FED_EPA_NPDES_NPDES_SICS, ENVIRONMENT__FED_EPA_ENVIROFACTS,
--         ENVIRONMENT__FED_EPA_GHGRP_EMISSION, ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS,
--         ENVIRONMENT__FED_EPA_NPDES_NPDES_NAICS
-- Door: Python (connect/db.py) via g39/run.py. Every connection first ran:
--   ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300;
--   ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';
-- Read-only: the runner refuses anything that is not SELECT / WITH. Raw results in g39/<label>.csv.
-- Statement numbers below count only SELECT/WITH statements against the 35 budget.

-- [q01] statement 1
-- Envirofacts: is it a sample, is it sorted, does it land in the full TRI facility table?
with e as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ENVIROFACTS),
t as (select distinct upper(trim(FACILITY_NAME)) nm, left(ZIP_CODE,5) z, STATE_ABBR st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY),
tri as (select count(*) n, count_if(STATE_ABBR='NJ') nj, count(distinct STATE_ABBR) sts from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY)
select 'state' k, STATE_CODE::text a, count(*)::text b, null c, null d from e group by 2
union all select 'profile', count(distinct upper(trim(FACILITY_NAME)))::text, count(*)::text, count_if(FRS_ID is not null)::text,
  count_if(LATITUDE is not null)::text || ' lat / runs ' || count(distinct _SOURCE_RUN_ID)::text || ' / tables ' || listagg(distinct TABLE_NAME, '|') from e
union all select 'land_name_zip', null, count(*)::text, count_if(t.nm is not null)::text, null from e left join t on t.nm = upper(trim(e.FACILITY_NAME)) and t.z = left(e.POSTAL_CODE,5)
union all select 'tri_full', null, n::text, nj::text, sts::text from tri;

-- [q02] statement 2
-- NPDES SIC and NAICS crosswalks: primary-flag sanity, duplicates, permit type (3rd character), land rate in the NPDES facility table
with s as (select NPDES_ID, SIC_CODE code, PRIMARY_INDICATOR_FLAG f, SIC_DESC d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_SICS),
n as (select NPDES_ID, NAICS_CODE code, PRIMARY_INDICATOR_FLAG f, NAICS_DESC d from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_NAICS),
fac as (select distinct NPDES_ID from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES),
sp as (select NPDES_ID, count(*) k, count(distinct code) kd, count_if(f='Y') y from s group by 1),
np as (select NPDES_ID, count(*) k, count(distinct code) kd, count_if(f='Y') y from n group by 1),
prof as (
  select 'SIC' t, count(*) permits, count_if(y=0) no_primary, count_if(y=1) one_primary, count_if(y>1) multi_primary, max(k) max_rows, count_if(k>kd) permits_with_dupe_code,
    count_if(substr(NPDES_ID,3,1) = 'R') third_r, count_if(substr(NPDES_ID,3,1) = 'G') third_g, count_if(substr(NPDES_ID,3,1) = '0') third_0,
    count_if(NPDES_ID in (select NPDES_ID from fac)) in_fac, count_if(NPDES_ID in (select NPDES_ID from np)) in_other from sp
  union all
  select 'NAICS', count(*), count_if(y=0), count_if(y=1), count_if(y>1), max(k), count_if(k>kd),
    count_if(substr(NPDES_ID,3,1) = 'R'), count_if(substr(NPDES_ID,3,1) = 'G'), count_if(substr(NPDES_ID,3,1) = '0'),
    count_if(NPDES_ID in (select NPDES_ID from fac)), count_if(NPDES_ID in (select NPDES_ID from sp)) from np),
codes as (
  select 'SIC_codes' t, count(distinct code) permits, count(distinct code||'|'||coalesce(d,'')) no_primary, count_if(code is null or trim(code)='') one_primary,
    count_if(f not in ('Y','N') or f is null) multi_primary, count_if(len(trim(code))<>4) max_rows, count(*) - count(distinct NPDES_ID, code, f) permits_with_dupe_code,
    null third_r, null third_g, null third_0, (select count(*) from fac) in_fac, null in_other from s
  union all
  select 'NAICS_codes', count(distinct code), count(distinct code||'|'||coalesce(d,'')), count_if(code is null or trim(code)=''),
    count_if(f not in ('Y','N') or f is null), count_if(len(trim(code))<>6), count(*) - count(distinct NPDES_ID, code, f), null, null, null, null, null from n),
top as (select 'SIC_top:' || NPDES_ID t, k permits, y no_primary, kd one_primary, null multi_primary, null max_rows, null permits_with_dupe_code, null third_r, null third_g, null third_0, null in_fac, null in_other
  from sp order by k desc limit 3)
select * from prof union all select * from codes union all select * from top;

-- [q03] statement 3
-- GHGRP emission: the whole table, slim, for local peer and time math (346,683 rows)
select EMISSION_RECORD_ID, FACILITY_ID, REPORTING_YEAR, SECTOR_ID, SUBSECTOR_ID, GAS_ID, CO2E_EMISSION
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION;

-- [q04] statement 4
-- GHGRP facility: every facility-year, slim, for names, industry, place and reporting status (136,005 rows)
select FACILITY_ID, REPORTING_YEAR, to_varchar(FRS_ID) FRS, FACILITY_NAME, PARENT_COMPANY, CITY, STATE, ZIP, COUNTY_FIPS, NAICS_CODE,
  FACILITY_TYPES, REPORTED_SUBPARTS, REPORTING_STATUS
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY;

-- [q05] statement 5
-- Title V certifications: the whole table, slim (499,113 rows), plus load lineage
select PGM_SYS_ID, ACTIVITY_ID, COMP_MONITOR_TYPE_CODE, STATE_EPA_FLAG, ACTUAL_END_DATE, FACILITY_RPT_DEVIATION_FLAG, _SOURCE_RUN_ID
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS;

-- [q06] statement 6
-- ICIS-Air facilities: slim, for state, name, size class and status (279,728 rows)
select PGM_SYS_ID, to_varchar(REGISTRY_ID) REGISTRY_ID, FACILITY_NAME, CITY, STATE, ZIP_CODE, AIR_POLLUTANT_CLASS_CODE, AIR_OPERATING_STATUS_CODE,
  NAICS_CODES, SIC_CODES, FACILITY_TYPE_CODE, CURRENT_HPV, LOCAL_CONTROL_REGION_CODE
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES;

-- [q07] statement 7
-- Title V certifications: the whole table, slim (499,113 rows). Rerun of q05, which named a lineage column this table does not have
select PGM_SYS_ID, ACTIVITY_ID, COMP_MONITOR_TYPE_CODE, STATE_EPA_FLAG, ACTUAL_END_DATE, FACILITY_RPT_DEVIATION_FLAG
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS;

-- [q08] statement 8
-- ICIS-Air programs: every facility's air programs, with status and dates (457,581 rows)
select PGM_SYS_ID, PROGRAM_CODE, AIR_OPERATING_STATUS_CODE, BEGIN_DATE, UPDATED_DATE
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_PROGRAMS;

-- [q09] statement 9
-- ICIS-Air violation history: slim (102,037 rows)
select PGM_SYS_ID, ACTIVITY_ID, AGENCY_TYPE_DESC, STATE_CODE, ENF_RESPONSE_POLICY_CODE, PROGRAM_CODES, POLLUTANT_DESCS,
  EARLIEST_FRV_DETERM_DATE, HPV_DAYZERO_DATE, HPV_RESOLVED_DATE
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY;

-- [q10] statement 10
-- ICIS-Air formal actions: slim (106,009 rows)
select PGM_SYS_ID, ACTIVITY_ID, ENF_IDENTIFIER, ACTIVITY_TYPE_CODE, STATE_EPA_FLAG, ENF_TYPE_CODE, SETTLEMENT_ENTERED_DATE, PENALTY_AMOUNT
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FORMAL_ACTIONS;

-- [q11] statement 11
-- ICIS-Air informal actions: slim (175,736 rows)
select PGM_SYS_ID, ACTIVITY_ID, STATE_EPA_FLAG, ENF_TYPE_CODE, ACHIEVED_DATE
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_INFORMAL_ACTIONS;

-- [q12] statement 12
-- ICIS-Air full and partial compliance evaluations, aggregated per facility (1.78M rows in)
select PGM_SYS_ID, count(*) n_eval,
  count_if(COMP_MONITOR_TYPE_DESC ilike 'FCE%') n_fce,
  count_if(COMP_MONITOR_TYPE_DESC ilike 'FCE%' and year(ACTUAL_END_DATE) between 2016 and 2025) n_fce_16_25,
  max(iff(COMP_MONITOR_TYPE_DESC ilike 'FCE%', ACTUAL_END_DATE, null)) last_fce,
  max(ACTUAL_END_DATE) last_eval,
  listagg(distinct COMP_MONITOR_TYPE_CODE, '|') codes
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FCES_PCES
group by 1;

-- [q13] statement 13
-- Verify in the warehouse: direct CO2e (no supplier sectors 9-13,16,17, no biogenic gas 8) for LNG terminals, 2015 vs 2023, and Sabine Pass's growth rank among facilities reporting both years
with d as (
  select FACILITY_ID, REPORTING_YEAR, sum(CO2E_EMISSION) t
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION
  where SECTOR_ID not in (9,10,11,12,13,16,17) and coalesce(GAS_ID,0) <> 8 and CO2E_EMISSION is not null
  group by 1,2),
w as (select FACILITY_ID, sum(iff(REPORTING_YEAR=2015,t,0)) y15, sum(iff(REPORTING_YEAR=2023,t,0)) y23 from d group by 1),
r as (select FACILITY_ID, y15, y23, y23-y15 chg, rank() over (order by y23-y15 desc) rk, count(*) over () n_both from w where y15>0 and y23>0)
select 'lng_all' k, count(*) n, round(sum(w.y15)/1e6,2) a, round(sum(w.y23)/1e6,2) b, null rk
from w where FACILITY_ID in ('1002259','1013179','1014135','1013553','1005420','1013753','1006016')
union all
select 'sabine', n_both, round(y15/1e6,2), round(y23/1e6,2), rk from r where FACILITY_ID = '1002259'
union all
select 'next_'||FACILITY_ID, n_both, round(y15/1e6,2), round(y23/1e6,2), rk from r where rk between 2 and 3;

-- [q14] statement 14
-- Verify in the warehouse: null-CO2e rows vs the facility's reporting status that year; sum split supplier vs direct
with e as (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_EMISSION),
f as (select FACILITY_ID, REPORTING_YEAR, max(nullif(trim(REPORTING_STATUS),'')) st from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_GHGRP_FACILITY group by 1,2)
select coalesce(f.st,'(reported)') status, iff(e.GAS_ID is null,'gas null','gas set') gas, count(*) n, count_if(e.CO2E_EMISSION is null) co2e_null,
  round(sum(iff(e.SECTOR_ID in (10,11,12,13,16), e.CO2E_EMISSION, 0))/1e9,2) supplier_bt, round(sum(e.CO2E_EMISSION)/1e9,2) all_bt
from e left join f on f.FACILITY_ID = e.FACILITY_ID and f.REPORTING_YEAR = e.REPORTING_YEAR
group by 1,2 order by 1,2;

-- [q15] statement 15
-- Verify in the warehouse: Title V certs deduped by ACTIVITY_ID, deviation-flag fill and Y rate 2020-2025 for TX, CO, LA, national; plus violations per operating major 2016-2025
with c as (select PGM_SYS_ID, ACTIVITY_ID, max(FACILITY_RPT_DEVIATION_FLAG) flag, max(ACTUAL_END_DATE) d, count(*) copies
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_TITLEV_CERTS group by 1,2),
fac as (select PGM_SYS_ID, STATE, AIR_POLLUTANT_CLASS_CODE cls, AIR_OPERATING_STATUS_CODE op from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_FACILITIES),
cs as (select f.STATE, count(*) certs, count_if(c.flag is not null) flagged, count_if(c.flag='Y') y
       from c join fac f using (PGM_SYS_ID) where year(c.d) between 2020 and 2025 group by 1),
vs as (select f.STATE, count(*) viol from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ICIS_AIR_ICIS_AIR_VIOLATION_HISTORY v join fac f using (PGM_SYS_ID)
       where coalesce(v.EARLIEST_FRV_DETERM_DATE, v.HPV_DAYZERO_DATE) between '2016-01-01' and '2025-12-31' group by 1),
ms as (select STATE, count(*) majors from fac where cls='MAJ' and op='OPR' group by 1),
st as (select ms.STATE, ms.majors, coalesce(vs.viol,0) viol, round(coalesce(vs.viol,0)/ms.majors,2) viol_per_major, cs.certs, cs.flagged, cs.y, round(cs.y/nullif(cs.flagged,0),3) y_rate
       from ms left join vs using (STATE) left join cs using (STATE) where ms.majors >= 50)
select * from st where STATE in ('TX','CO','LA','CA','NC','PA')
union all select 'MEDIAN(majors>=50)', median(majors), median(viol), median(viol_per_major), median(certs), median(flagged), median(y), median(y_rate) from st
union all select 'DUP_ACTIVITY_IDS', count_if(copies>1), sum(copies)-count(*), null, count(*), null, null, null from c;

-- [q16] statement 16
-- Envirofacts vs full TRI facility list: ZIP first digit mix (is the 5,000-row sample random or a slice?)
select 'envirofacts' src, left(POSTAL_CODE,1) z1, count(*) n from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_ENVIROFACTS group by 1,2
union all
select 'tri_full', left(ZIP_CODE,1), count(*) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_TRI_FACILITY group by 1,2
order by 1,2;

-- NOTES
-- q05 (statement 5) errored: this table has no _SOURCE_RUN_ID column. q07 is the same pull without it. It still counts against the budget.
-- q03, q04, q06-q12 are slim whole-table pulls (all under 500K rows). The peer, time and join math ran locally
-- in pandas on those pulls: g39/a1.py-a9.py (Title V), g39/b1.py-b5.py (greenhouse gas). No statements there.
-- q13-q16 re-check the headline numbers inside the warehouse. They matched the local math.
-- Total: 16 of 35 statements.
