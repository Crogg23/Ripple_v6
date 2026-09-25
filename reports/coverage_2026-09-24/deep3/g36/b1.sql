-- [n1_noaa_profile]
select count(*) n, count(distinct id) ids, min(sent) first_sent, max(sent) last_sent,
  datediff('hour', min(sent), max(sent)) span_hours,
  count_if(message_type = 'Alert') alerts, count_if(message_type = 'Update') updates,
  count_if(message_type not in ('Alert','Update')) other_mt,
  count_if(event ilike '%heat%') heat_rows, count(distinct sender_name) offices,
  count_if(geometry is not null and geometry <> '') has_geom,
  count_if(expires < sent) expires_before_sent
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_NOAA_WEATHER_API

-- [f1_frsf_state_links]
with l as (
  select registry_id, count(*) n_links, count(distinct pgm_sys_acrnm) n_prog, min(pgm_sys_acrnm) p1
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS group by 1)
select coalesce(f.fac_state, '(null)') st, count(*) facs,
  round(100 * ratio_to_report(count(*)) over (), 1) pct,
  count_if(l.registry_id is null) unlinked, count_if(l.n_prog = 1) one_prog,
  mode(iff(l.n_prog = 1, l.p1, null)) top_single_prog
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES f
left join l on l.registry_id = f.registry_id
group by 1 order by facs desc limit 15

-- [f2_frsf_ca_programs]
select iff(f.fac_state = 'CA', 'CA', 'rest') g, l.pgm_sys_acrnm, count(distinct f.registry_id) facs
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES f
join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS l on l.registry_id = f.registry_id
group by 1, 2
qualify row_number() over (partition by g order by facs desc) <= 12
order by g, facs desc

-- [f3_frsf_traps]
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
  (select latitude_measure || ',' || longitude_measure from pt order by c desc limit 1) top_point

-- [l1_links_by_program]
with p as (
  select pgm_sys_acrnm a, pgm_sys_id i, count(*) nrow, count(distinct registry_id) nreg
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS group by 1, 2)
select a, count(*) ids, sum(nrow) rows_, count_if(nreg > 1) ids_on_2plus_regs, max(nreg) max_regs,
  count_if(nrow > nreg) ids_with_dup_rows
from p group by a order by rows_ desc limit 25

-- [l2_links_top_registry]
select registry_id, count(*) links, count(distinct pgm_sys_acrnm) progs, any_value(primary_name) nm,
  mode(city_name) city, mode(state_code) st, mode(pgm_sys_acrnm) top_prog
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_PROGRAM_LINKS
group by 1 order by links desc limit 8

-- [i1_insp_traps]
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
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS

-- [i2_insp_by_year]
select year(coalesce(actual_end_date, actual_begin_date)) yr, count(*) n,
  count_if(state_epa_flag = 'E') epa, count_if(state_epa_flag = 'S') state_, count_if(state_epa_flag = 'L') local_,
  count(distinct npdes_id) permits, count_if(substr(npdes_id, 3, 1) = '0') indiv,
  count_if(comp_monitor_type_code = 'CEI') cei
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
where yr between 1985 and 2026
group by 1 order by 1

-- [i3_insp_state_step]
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
order by ratio asc

-- [i4_qncr_profile]
select 'yr' k, left(yearqtr, 4) v, count(*) rows_, count(distinct npdes_id) permits,
  count_if(try_to_number(nume90_q) > 0) q_e90
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY group by 2
union all
select 'hlrnc', hlrnc, count(*), count(distinct npdes_id), count_if(try_to_number(nume90_q) > 0)
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_QNCR_HISTORY
where yearqtr >= '20230' group by 2
order by 1, 2

-- [s1_sdwaf_traps]
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
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES

-- [s2_sdwaf_source_codes]
select facility_type_code, water_type_code, filtration_status_code, is_source_treated_ind, facility_activity_code, count(*) n
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_SDWA_SDWA_FACILITIES
where is_source_ind = 'Y'
group by all order by n desc limit 60

-- [s3_sdwaf_mif_by_state]
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
from j group by st order by mif desc, sources desc limit 60
