-- [i5_insp_dupes]
with d as (
  select activity_id, npdes_id, count(*) c, count(distinct comp_monitor_type_code) ct,
    count(distinct actual_end_date) de, count(distinct state_epa_flag) df
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
  group by 1, 2 having count(*) > 1)
select count(*) dup_pairs, sum(c) rows_in, sum(c - 1) extra_rows, count_if(ct > 1) differ_type,
  count_if(ct = 1 and de = 1 and df = 1) identical_on_type_date_flag, max(c) max_rows
from d

-- [i6_insp_same_months]
select year(actual_end_date) yr,
  count(distinct iff(state_epa_flag = 'E', activity_id, null)) epa_jan_jun,
  count(distinct iff(state_epa_flag = 'S', activity_id, null)) state_jan_jun,
  count(distinct iff(state_epa_flag = 'E' and month(actual_end_date) = 7, activity_id, null)) epa_jul,
  count(distinct iff(state_epa_flag = 'S' and month(actual_end_date) = 7, activity_id, null)) state_jul
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
where month(actual_end_date) <= 7 and yr between 2014 and 2026
group by 1 order by 1

-- [i7_insp_state_halves]
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
order by (h25b + h26a) / nullif(h23b + h24a, 0) asc

-- [i8_violators_no_insp_by_state]
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
order by chronic desc

-- [i9_violators_no_insp_named]
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
order by q.qe desc, q.e90 desc limit 25

-- [f4_frsf_stacked_points]
with pt as (
  select latitude_measure la, longitude_measure lo, count(*) c
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES
  where latitude_measure is not null group by 1, 2 order by c desc limit 4)
select pt.la, pt.lo, pt.c, count(distinct f.fac_zip) zips, count(distinct f.fac_city) cities,
  mode(f.fac_city) city, mode(f.fac_state) st, mode(f.fac_zip) zip, min(f.fac_name) nm_a, max(f.fac_name) nm_z,
  mode(f.fac_street) street
from pt join LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES f
  on f.latitude_measure = pt.la and f.longitude_measure = pt.lo
group by 1, 2, 3 order by 3 desc

-- [s4_seller_violation_passdown_totals]
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
from bl

-- [s5_seller_violation_passdown_named]
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
order by sl.clean_pop desc limit 25
