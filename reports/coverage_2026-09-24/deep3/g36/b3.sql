-- [i10_epa_type_mix]
select comp_monitor_type_code code, any_value(comp_monitor_type_desc) descr,
  count(distinct iff(year(actual_end_date) = 2019, activity_id, null)) y2019,
  count(distinct iff(year(actual_end_date) = 2024, activity_id, null)) y2024,
  count(distinct iff(year(actual_end_date) = 2025, activity_id, null)) y2025,
  count(distinct iff(year(actual_end_date) = 2026, activity_id, null)) y2026
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_NPDES_NPDES_INSPECTIONS
where state_epa_flag = 'E' and month(actual_end_date) <= 6 and year(actual_end_date) in (2019, 2024, 2025, 2026)
group by 1 order by y2026 desc

-- [i11_flowstop_check]
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
order by 1, 2

-- [i12_chronic_enforcement_by_state]
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
from j group by 1 order by chronic_indiv desc

-- [s6_passdown_pure_buyers]
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
order by sb.pop desc
