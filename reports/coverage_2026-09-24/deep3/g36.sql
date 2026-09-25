-- g36 deep pass 3, 2026-09-24. Every statement run, in order. Python door (connect/db.py). Read-only.
-- Tables: FRS_FRS_FACILITIES, FRS_FRS_PROGRAM_LINKS, NOAA_WEATHER_API, NPDES_NPDES_INSPECTIONS, SDWA_SDWA_FACILITIES (all LIBRARY_MARTS.ENVIRONMENT).
-- Join tables read: NPDES_QNCR_HISTORY, NPDES_ICIS_FACILITIES, NPDES_INFORMAL_ENFORCEMENT_ACTIONS, NPDES_FORMAL_ENFORCEMENT_ACTIONS,
--   SDWA_PUB_WATER_SYSTEMS, SDWA_VIOLATIONS_ENFORCEMENT.
-- Budget: 35 of 35 = 27 SELECTs + 8 session-setup statements (4 connections x 2).

-- ===== connection: b0.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [q01_coltypes] (2.0s)
select table_name, column_name, data_type
from LIBRARY_MARTS.INFORMATION_SCHEMA.COLUMNS
where table_schema = 'ENVIRONMENT'
  and table_name in ('ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES','ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS',
    'ENVIRONMENT__FED_NOAA_WEATHER_API','ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS','ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES',
    'ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY','ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS',
    'ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT','ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES')
  and data_type <> 'TEXT'
order by table_name, ordinal_position;

-- [q02_samples] (3.4s)
select 'INSP' t, object_construct(*)::varchar o from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS limit 2)
union all select 'SDWAF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES where seller_pwsid is not null and seller_pwsid <> '' limit 1)
union all select 'SDWAF2', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES where filtration_status_code is not null and filtration_status_code <> '' limit 1)
union all select 'QNCR', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY limit 1)
union all select 'SDWAV', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT where violation_id is not null limit 1)
union all select 'PWS', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS limit 1)
union all select 'FRSF', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES limit 1)
union all select 'FRSL', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS limit 1)
union all select 'NOAA', object_construct(*)::varchar from (select * from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_WEATHER_API limit 1);

-- ===== connection: b1.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [n1_noaa_profile] (0.3s)
select count(*) n, count(distinct id) ids, min(sent) first_sent, max(sent) last_sent,
  datediff('hour', min(sent), max(sent)) span_hours,
  count_if(message_type = 'Alert') alerts, count_if(message_type = 'Update') updates,
  count_if(message_type not in ('Alert','Update')) other_mt,
  count_if(event ilike '%heat%') heat_rows, count(distinct sender_name) offices,
  count_if(geometry is not null and geometry <> '') has_geom,
  count_if(expires < sent) expires_before_sent
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_WEATHER_API;

-- [f1_frsf_state_links] (1.8s)
with l as (
  select registry_id, count(*) n_links, count(distinct pgm_sys_acrnm) n_prog, min(pgm_sys_acrnm) p1
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS group by 1)
select coalesce(f.fac_state, '(null)') st, count(*) facs,
  round(100 * ratio_to_report(count(*)) over (), 1) pct,
  count_if(l.registry_id is null) unlinked, count_if(l.n_prog = 1) one_prog,
  mode(iff(l.n_prog = 1, l.p1, null)) top_single_prog
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES f
left join l on l.registry_id = f.registry_id
group by 1 order by facs desc limit 15;

-- [f2_frsf_ca_programs] (0.8s)
select iff(f.fac_state = 'CA', 'CA', 'rest') g, l.pgm_sys_acrnm, count(distinct f.registry_id) facs
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES f
join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS l on l.registry_id = f.registry_id
group by 1, 2
qualify row_number() over (partition by g order by facs desc) <= 12
order by g, facs desc;

-- [f3_frsf_traps] (1.1s)
with pt as (
  select latitude_measure, longitude_measure, count(*) c
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES
  where latitude_measure is not null group by 1, 2)
select (select count(*) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) n,
  (select count_if(fac_name is null or upper(fac_name) in ('RESIDENCE','UNKNOWN','')) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) filler_name,
  (select count_if(latitude_measure is null) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) no_point,
  (select count_if(fac_street is null or upper(fac_street) in ('UNKNOWN','NOT AVAILABLE','')) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) no_street,
  (select count(*) from pt where c >= 100) points_100plus,
  (select sum(c) from pt where c >= 100) facs_on_100plus_points,
  (select max(c) from pt) top_point_n,
  (select latitude_measure || ',' || longitude_measure from pt order by c desc limit 1) top_point;

-- [l1_links_by_program] (1.1s)
with p as (
  select pgm_sys_acrnm a, pgm_sys_id i, count(*) nrow, count(distinct registry_id) nreg
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS group by 1, 2)
select a, count(*) ids, sum(nrow) rows_, count_if(nreg > 1) ids_on_2plus_regs, max(nreg) max_regs,
  count_if(nrow > nreg) ids_with_dup_rows
from p group by a order by rows_ desc limit 25;

-- [l2_links_top_registry] (3.6s)
select registry_id, count(*) links, count(distinct pgm_sys_acrnm) progs, any_value(primary_name) nm,
  mode(city_name) city, mode(state_code) st, mode(pgm_sys_acrnm) top_prog
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS
group by 1 order by links desc limit 8;

-- [i1_insp_traps] (1.0s)
select count(*) n, count(distinct activity_id) acts, count(distinct activity_id || '|' || npdes_id) act_permit_pairs,
  count(distinct npdes_id) permits, count(distinct registry_id) regs,
  count_if(registry_id is null or registry_id = '') no_reg,
  count_if(actual_begin_date is null) no_begin, count_if(actual_end_date is null) no_end,
  min(actual_end_date) min_end, max(actual_end_date) max_end,
  count_if(actual_end_date < '1970-01-01') end_pre1970, count_if(actual_begin_date < '1970-01-01') begin_pre1970,
  count_if(actual_end_date > current_date) end_future,
  count_if(state_epa_flag = 'S') s, count_if(state_epa_flag = 'E') e, count_if(state_epa_flag = 'L') l,
  count_if(state_epa_flag is null or state_epa_flag not in ('S','E','L')) other_flag,
  count_if(activity_outcome_code is not null and activity_outcome_code <> '') has_outcome,
  count(distinct activity_type_code) n_act_types,
  count_if(substr(npdes_id, 3, 1) = '0') individual_permit_rows
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS;

-- [i2_insp_by_year] (0.9s)
select year(coalesce(actual_end_date, actual_begin_date)) yr, count(*) n,
  count_if(state_epa_flag = 'E') epa, count_if(state_epa_flag = 'S') state_, count_if(state_epa_flag = 'L') local_,
  count(distinct npdes_id) permits, count_if(substr(npdes_id, 3, 1) = '0') indiv,
  count_if(comp_monitor_type_code = 'CEI') cei
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
where yr between 1985 and 2026
group by 1 order by 1;

-- [i3_insp_state_step] (0.5s)
with s as (
  select left(npdes_id, 2) st, year(coalesce(actual_end_date, actual_begin_date)) yr,
    count(*) n, count_if(substr(npdes_id, 3, 1) = '0') indiv, count_if(state_epa_flag = 'E') epa
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
  where yr between 2012 and 2025 group by 1, 2)
select st,
  round(sum(iff(yr between 2015 and 2017, n, 0)) / 3) a1517,
  round(sum(iff(yr between 2018 and 2019, n, 0)) / 2) a1819,
  round(sum(iff(yr between 2020 and 2021, n, 0)) / 2) a2021,
  round(sum(iff(yr between 2022 and 2024, n, 0)) / 3) a2224,
  sum(iff(yr = 2025, n, 0)) y2025,
  round(sum(iff(yr between 2015 and 2017, indiv, 0)) / 3) i1517,
  round(sum(iff(yr between 2022 and 2024, indiv, 0)) / 3) i2224,
  sum(iff(yr = 2025, indiv, 0)) i2025,
  round(sum(iff(yr between 2022 and 2024, n, 0)) / 3 / nullif(sum(iff(yr between 2015 and 2017, n, 0)) / 3, 0), 2) ratio
from s group by st
having a1517 >= 100
order by ratio asc;

-- [i4_qncr_profile] (0.6s)
select 'yr' k, left(yearqtr, 4) v, count(*) rows_, count(distinct npdes_id) permits,
  count_if(try_to_number(nume90_q) > 0) q_e90
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY group by 2
union all
select 'hlrnc', hlrnc, count(*), count(distinct npdes_id), count_if(try_to_number(nume90_q) > 0)
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
where yearqtr >= '20230' group by 2
order by 1, 2;

-- [s1_sdwaf_traps] (0.9s)
select count(*) n, count(distinct pwsid) sys, count(distinct pwsid || '|' || facility_id) fac_keys,
  count_if(facility_activity_code = 'A') active, count_if(facility_activity_code = 'I') inactive,
  count_if(facility_activity_code not in ('A','I')) other_act,
  count_if(facility_deactivation_date > current_date) deact_future,
  count_if(facility_deactivation_date < '1950-01-01') deact_pre1950,
  count_if(facility_activity_code = 'A' and facility_deactivation_date is not null) active_with_deact,
  count_if(facility_activity_code = 'I' and facility_deactivation_date is null) inactive_no_deact,
  count_if(is_source_ind = 'Y') src, count_if(seller_pwsid is not null and seller_pwsid <> '') has_seller,
  count_if(filtration_status_code is not null and filtration_status_code <> '') has_filt,
  count_if(is_source_treated_ind is not null and is_source_treated_ind <> '') has_treated,
  count_if(water_type_code is not null and water_type_code <> '') has_wt,
  count(distinct submissionyearquarter) n_sub,
  count_if(first_reported_date > last_reported_date) first_after_last
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES;

-- [s2_sdwaf_source_codes] (0.3s)
select facility_type_code, water_type_code, filtration_status_code, is_source_treated_ind, facility_activity_code, count(*) n
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
where is_source_ind = 'Y'
group by all order by n desc limit 60;

-- [s3_sdwaf_mif_by_state] (1.1s)
with sys as (
  select pwsid, pws_type_code, population_served_count pop, primacy_agency_code, pws_activity_code
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
  qualify row_number() over (partition by pwsid order by last_reported_date desc) = 1),
src as (
  select pwsid, filtration_status_code fs, water_type_code wt
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
  where facility_activity_code = 'A' and is_source_ind = 'Y' and water_type_code in ('SW','GU')
    and facility_type_code <> 'CC'),
j as (
  select s.primacy_agency_code st, src.pwsid, src.fs, src.wt, s.pop, s.pws_type_code
  from src join sys s on s.pwsid = src.pwsid and s.pws_activity_code = 'A')
select st, count(*) sources, count_if(fs = 'FIL') fil, count_if(fs = 'SAF') saf, count_if(fs = 'MIF') mif,
  count_if(fs is null or fs = '') blank,
  count(distinct iff(fs = 'MIF', pwsid, null)) mif_systems,
  count(distinct iff(fs = 'MIF' and pws_type_code = 'CWS', pwsid, null)) mif_cws
from j group by st order by mif desc, sources desc limit 60;

-- ===== connection: b2.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [i5_insp_dupes] (1.8s)
with d as (
  select activity_id, npdes_id, count(*) c, count(distinct comp_monitor_type_code) ct,
    count(distinct actual_end_date) de, count(distinct state_epa_flag) df
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
  group by 1, 2 having count(*) > 1)
select count(*) dup_pairs, sum(c) rows_in, sum(c - 1) extra_rows, count_if(ct > 1) differ_type,
  count_if(ct = 1 and de = 1 and df = 1) identical_on_type_date_flag, max(c) max_rows
from d;

-- [i6_insp_same_months] (0.5s)
select year(actual_end_date) yr,
  count(distinct iff(state_epa_flag = 'E', activity_id, null)) epa_jan_jun,
  count(distinct iff(state_epa_flag = 'S', activity_id, null)) state_jan_jun,
  count(distinct iff(state_epa_flag = 'E' and month(actual_end_date) = 7, activity_id, null)) epa_jul,
  count(distinct iff(state_epa_flag = 'S' and month(actual_end_date) = 7, activity_id, null)) state_jul
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
where month(actual_end_date) <= 7 and yr between 2014 and 2026
group by 1 order by 1;

-- [i7_insp_state_halves] (0.6s)
with s as (
  select left(npdes_id, 2) st, year(actual_end_date) y, iff(month(actual_end_date) <= 6, 1, 2) h,
    state_epa_flag f, activity_id
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
  where actual_end_date >= '2023-01-01')
select st,
  count(distinct iff(y = 2023 and h = 1, activity_id, null)) h23a,
  count(distinct iff(y = 2023 and h = 2, activity_id, null)) h23b,
  count(distinct iff(y = 2024 and h = 1, activity_id, null)) h24a,
  count(distinct iff(y = 2024 and h = 2, activity_id, null)) h24b,
  count(distinct iff(y = 2025 and h = 1, activity_id, null)) h25a,
  count(distinct iff(y = 2025 and h = 2, activity_id, null)) h25b,
  count(distinct iff(y = 2026 and h = 1, activity_id, null)) h26a,
  count(distinct iff(y = 2024 and h = 1 and f = 'E', activity_id, null)) e24a,
  count(distinct iff(y = 2025 and h = 1 and f = 'E', activity_id, null)) e25a,
  count(distinct iff(y = 2026 and h = 1 and f = 'E', activity_id, null)) e26a
from s group by st
having h23a + h23b + h24a >= 60
order by (h25b + h26a) / nullif(h23b + h24a, 0) asc;

-- [i8_violators_no_insp_by_state] (0.7s)
with q as (
  select npdes_id, count(*) nq, count_if(try_to_number(nume90_q) > 0) qe, sum(try_to_number(nume90_q)) e90
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where yearqtr between '20231' and '20254' group by 1),
ins as (
  select npdes_id, max(actual_end_date) last_ins, count_if(actual_end_date >= '2021-01-01') n21
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS group by 1),
j as (
  select q.npdes_id, q.qe, q.e90, left(q.npdes_id, 2) st, substr(q.npdes_id, 3, 1) = '0' indiv,
    ins.last_ins, coalesce(ins.n21, 0) n21
  from q left join ins on ins.npdes_id = q.npdes_id
  where q.qe >= 6)
select st, count(*) chronic, count_if(indiv) chronic_indiv,
  count_if(n21 = 0) no_ins_since21, count_if(indiv and n21 = 0) indiv_no_ins,
  count_if(last_ins is null) never_in_table,
  round(100 * count_if(n21 = 0) / count(*), 1) pct_no_ins,
  round(100 * count_if(indiv and n21 = 0) / nullif(count_if(indiv), 0), 1) pct_indiv_no_ins
from j group by rollup(st)
order by chronic desc;

-- [i9_violators_no_insp_named] (1.4s)
with q as (
  select npdes_id, count(*) nq, count_if(try_to_number(nume90_q) > 0) qe, sum(try_to_number(nume90_q)) e90
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where yearqtr between '20231' and '20254' group by 1),
ins as (
  select npdes_id, max(actual_end_date) last_ins, count_if(actual_end_date >= '2021-01-01') n21, count(*) n_all
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS group by 1),
fac as (
  select npdes_id, any_value(facility_name) nm, any_value(city) city, any_value(facility_type_code) ft,
    any_value(facility_uin) uin
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES group by 1)
select q.npdes_id, fac.nm, fac.city, fac.ft, q.nq, q.qe, q.e90, ins.last_ins, coalesce(ins.n_all, 0) n_all_ins
from q left join ins on ins.npdes_id = q.npdes_id
left join fac on fac.npdes_id = q.npdes_id
where q.qe >= 6 and substr(q.npdes_id, 3, 1) = '0' and coalesce(ins.n21, 0) = 0
order by q.qe desc, q.e90 desc limit 25;

-- [f4_frsf_stacked_points] (1.0s)
with pt as (
  select latitude_measure la, longitude_measure lo, count(*) c
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES
  where latitude_measure is not null group by 1, 2 order by c desc limit 4)
select pt.la, pt.lo, pt.c, count(distinct f.fac_zip) zips, count(distinct f.fac_city) cities,
  mode(f.fac_city) city, mode(f.fac_state) st, mode(f.fac_zip) zip, min(f.fac_name) nm_a, max(f.fac_name) nm_z,
  mode(f.fac_street) street
from pt join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES f
  on f.latitude_measure = pt.la and f.longitude_measure = pt.lo
group by 1, 2, 3 order by 3 desc;

-- [s4_seller_violation_passdown_totals] (3.2s)
with b as (
  select distinct pwsid buyer, seller_pwsid seller
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
  where seller_pwsid is not null and seller_pwsid <> '' and seller_pwsid <> pwsid and facility_activity_code = 'A'),
nsel as (select buyer, count(distinct seller) n_sellers from b group by 1),
own as (
  select distinct pwsid from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
  where facility_activity_code = 'A' and is_source_ind = 'Y' and facility_type_code <> 'CC'),
sys as (
  select pwsid, pws_activity_code act, pws_type_code typ, population_served_count pop
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
  qualify row_number() over (partition by pwsid order by last_reported_date desc) = 1),
v as (
  select pwsid, contaminant_code c, count(distinct violation_id) nv
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  where is_health_based_ind = 'Y' and violation_category_code = 'MCL' and rule_group_code = '300'
    and non_compl_per_begin_date between '2021-01-01' and '2025-12-31'
    and violation_id is not null and violation_id <> ''
  group by 1, 2),
x as (
  select b.buyer, b.seller, v.c, iff(vb.pwsid is null, 0, 1) buyer_has
  from b join v on v.pwsid = b.seller
  left join v vb on vb.pwsid = b.buyer and vb.c = v.c),
bl as (
  select x.buyer, max(x.buyer_has) any_has, s.pop, s.typ, iff(own.pwsid is null, 0, 1) has_own, n.n_sellers
  from x join sys s on s.pwsid = x.buyer and s.act = 'A'
  join nsel n on n.buyer = x.buyer
  left join own on own.pwsid = x.buyer
  group by x.buyer, s.pop, s.typ, own.pwsid, n.n_sellers)
select count(*) buyers, sum(pop) buyer_pop, count_if(any_has = 0) clean, sum(iff(any_has = 0, pop, 0)) clean_pop,
  count_if(any_has = 0 and has_own = 0 and n_sellers = 1) clean_pure,
  sum(iff(any_has = 0 and has_own = 0 and n_sellers = 1, pop, 0)) clean_pure_pop,
  count_if(any_has = 1) hit, sum(iff(any_has = 1, pop, 0)) hit_pop,
  count_if(typ = 'CWS') cws, count_if(typ = 'CWS' and any_has = 0) cws_clean,
  (select count(distinct seller) from x) sellers_with_viol,
  (select count(*) from v) viol_sys_contam_pairs,
  (select count(distinct pwsid) from v) viol_systems
from bl;

-- [s5_seller_violation_passdown_named] (1.8s)
with b as (
  select distinct pwsid buyer, seller_pwsid seller
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
  where seller_pwsid is not null and seller_pwsid <> '' and seller_pwsid <> pwsid and facility_activity_code = 'A'),
sys as (
  select pwsid, pws_activity_code act, pws_type_code typ, population_served_count pop, pws_name, primacy_agency_code st
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
  qualify row_number() over (partition by pwsid order by last_reported_date desc) = 1),
v as (
  select pwsid, contaminant_code c, count(distinct violation_id) nv,
    min(non_compl_per_begin_date) first_v, max(non_compl_per_begin_date) last_v
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  where is_health_based_ind = 'Y' and violation_category_code = 'MCL' and rule_group_code = '300'
    and non_compl_per_begin_date between '2021-01-01' and '2025-12-31'
    and violation_id is not null and violation_id <> ''
  group by 1, 2),
x as (
  select b.buyer, b.seller, v.c, iff(vb.pwsid is null, 0, 1) buyer_has
  from b join v on v.pwsid = b.seller
  left join v vb on vb.pwsid = b.buyer and vb.c = v.c),
xs as (select seller, buyer, max(buyer_has) bh from x group by 1, 2),
sl as (
  select xs.seller, count(*) buyers, count_if(xs.bh = 0) clean_buyers, sum(s.pop) buyer_pop,
    sum(iff(xs.bh = 0, s.pop, 0)) clean_pop
  from xs join sys s on s.pwsid = xs.buyer and s.act = 'A' group by 1),
vv as (
  select pwsid, listagg(c || ':' || nv, ',') cs, sum(nv) nv, min(first_v) first_v, max(last_v) last_v
  from v group by 1)
select sl.seller, ss.pws_name, ss.st, ss.pop seller_pop, ss.act seller_act, ss.typ, vv.cs, vv.nv, vv.first_v, vv.last_v,
  sl.buyers, sl.clean_buyers, sl.buyer_pop, sl.clean_pop
from sl left join sys ss on ss.pwsid = sl.seller
left join vv on vv.pwsid = sl.seller
order by sl.clean_pop desc limit 25;

-- ===== connection: b3.sql (2 session-setup statements: STATEMENT_TIMEOUT 300, QUERY_TAG deep3-2026-09-24)

-- [i10_epa_type_mix] (0.5s)
select comp_monitor_type_code code, any_value(comp_monitor_type_desc) descr,
  count(distinct iff(year(actual_end_date) = 2019, activity_id, null)) y2019,
  count(distinct iff(year(actual_end_date) = 2024, activity_id, null)) y2024,
  count(distinct iff(year(actual_end_date) = 2025, activity_id, null)) y2025,
  count(distinct iff(year(actual_end_date) = 2026, activity_id, null)) y2026
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
where state_epa_flag = 'E' and month(actual_end_date) <= 6 and year(actual_end_date) in (2019, 2024, 2025, 2026)
group by 1 order by y2026 desc;

-- [i11_flowstop_check] (1.4s)
with a as (
  select left(npdes_id, 2) st, year(actual_end_date) y,
    count(distinct iff(state_epa_flag = 'S', activity_id, null)) state_ins,
    count(distinct iff(state_epa_flag = 'E', activity_id, null)) epa_ins
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
  where actual_end_date >= '2023-01-01' and left(npdes_id, 2) in ('OR','IA','CA','VT','HI','WA','MN','IL')
  group by 1, 2),
b as (
  select left(npdes_id, 2) st, left(yearqtr, 4)::int y, count(distinct npdes_id) qncr_permits,
    count_if(try_to_number(nume90_q) > 0) e90_quarters
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where yearqtr between '20231' and '20264' and left(npdes_id, 2) in ('OR','IA','CA','VT','HI','WA','MN','IL')
  group by 1, 2),
c as (
  select left(npdes_id, 2) st, year(try_to_date(achieved_date::varchar)) y, count(distinct activity_id) informal_actions
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS
  where left(npdes_id, 2) in ('OR','IA','CA','VT','HI','WA','MN','IL')
    and year(try_to_date(achieved_date::varchar)) between 2023 and 2026
  group by 1, 2)
select coalesce(a.st, b.st, c.st) st, coalesce(a.y, b.y, c.y) y, a.state_ins, a.epa_ins, b.qncr_permits, b.e90_quarters, c.informal_actions
from a full join b on a.st = b.st and a.y = b.y
full join c on c.st = coalesce(a.st, b.st) and c.y = coalesce(a.y, b.y)
order by 1, 2;

-- [i12_chronic_enforcement_by_state] (3.6s)
with q as (
  select npdes_id, count_if(try_to_number(nume90_q) > 0) qe
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
  where yearqtr between '20231' and '20254' group by 1),
ins as (
  select npdes_id, count_if(actual_end_date >= '2021-01-01') n21
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS group by 1),
inf as (
  select npdes_id, count(distinct activity_id) n_inf
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INFORMAL_ENFORCEMENT_ACTIONS
  where try_to_date(achieved_date::varchar) between '2021-01-01' and '2026-12-31' group by 1),
frm as (
  select npdes_id, count(distinct activity_id) n_frm
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_FORMAL_ENFORCEMENT_ACTIONS
  where try_to_date(settlement_entered_date::varchar) between '2021-01-01' and '2026-12-31' group by 1),
fac as (
  select npdes_id, any_value(facility_type_code) ft
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_ICIS_FACILITIES group by 1),
j as (
  select q.npdes_id, left(q.npdes_id, 2) st, coalesce(ins.n21, 0) n21, coalesce(inf.n_inf, 0) n_inf,
    coalesce(frm.n_frm, 0) n_frm, fac.ft
  from q left join ins on ins.npdes_id = q.npdes_id
  left join inf on inf.npdes_id = q.npdes_id
  left join frm on frm.npdes_id = q.npdes_id
  left join fac on fac.npdes_id = q.npdes_id
  where q.qe >= 6 and substr(q.npdes_id, 3, 1) = '0')
select iff(st in ('IL','MO','AR','WI','OR','CA','MA'), st, 'other') grp, count(*) chronic_indiv,
  count_if(n21 = 0) no_ins, count_if(n21 = 0 and n_inf = 0 and n_frm = 0) no_ins_no_enf,
  count_if(n21 > 0 and n_inf = 0 and n_frm = 0) ins_but_no_enf,
  count_if(n_inf > 0 or n_frm > 0) any_enf,
  count_if(n21 = 0 and ft in ('MWD','CTG','CNG')) no_ins_public,
  count_if(n21 = 0 and ft = 'POF') no_ins_private
from j group by 1 order by chronic_indiv desc;

-- [s6_passdown_pure_buyers] (1.5s)
with ball as (
  select distinct pwsid buyer, seller_pwsid seller, availability_code av
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
  where seller_pwsid is not null and seller_pwsid <> '' and seller_pwsid <> pwsid and facility_activity_code = 'A'),
nsel as (
  select buyer, count(distinct seller) n_sellers, max(iff(av = 'P', 1, 0)) has_perm from ball group by 1),
own as (
  select distinct pwsid from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
  where facility_activity_code = 'A' and is_source_ind = 'Y' and facility_type_code <> 'CC'),
sys as (
  select pwsid, pws_activity_code act, pws_type_code typ, population_served_count pop, pws_name, primacy_agency_code st
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_PUB_WATER_SYSTEMS
  qualify row_number() over (partition by pwsid order by last_reported_date desc) = 1),
v as (
  select pwsid, contaminant_code c, count(distinct violation_id) nv
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_VIOLATIONS_ENFORCEMENT
  where is_health_based_ind = 'Y' and violation_category_code = 'MCL' and rule_group_code = '300'
    and non_compl_per_begin_date between '2021-01-01' and '2025-12-31'
    and violation_id is not null and violation_id <> ''
  group by 1, 2),
x as (
  select b.buyer, b.seller, v.c, v.nv, iff(vb.pwsid is null, 0, 1) buyer_has
  from (select distinct buyer, seller from ball) b
  join v on v.pwsid = b.seller
  left join v vb on vb.pwsid = b.buyer and vb.c = v.c),
xp as (
  select buyer, seller, listagg(c || ':' || nv, ',') cs, max(buyer_has) bh from x group by 1, 2)
select xp.buyer, sb.pws_name buyer_name, sb.st, sb.pop, sb.typ, xp.seller, ss.pws_name seller_name, xp.cs, xp.bh, n.has_perm
from xp
join sys sb on sb.pwsid = xp.buyer and sb.act = 'A'
join nsel n on n.buyer = xp.buyer and n.n_sellers = 1
left join own on own.pwsid = xp.buyer
left join sys ss on ss.pwsid = xp.seller
where own.pwsid is null
order by sb.pop desc;

-- ===== notes
-- [i6_insp_same_months]: the WHERE keeps months 1-7, so the columns named *_JAN_JUN are really Jan-Jul.
--   Jan-Jun in g36.md = *_JAN_JUN minus *_JUL. Cross-checked against [i10_epa_type_mix] (Jan-Jun, month <= 6): within 6 per year.
