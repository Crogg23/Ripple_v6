P = "LIBRARY_MARTS.HEALTH."
N = P + "HEALTH__FED_CDC_NNDSS_WEEKLY_2024"
POS = P + "HEALTH__FED_CMS_POS_OTHER"
HG = P + "HEALTH__FED_CMS_HOSPITAL_GENERAL"
DMF = P + "HEALTH__FED_FDA_DRUG_MASTER_FILES"
WK = "try_to_number(MMWR_WEEK::varchar)"
YTD = ("coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), "
       "iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))")
SOLD = """case when p.CHOW_DT>='2024-01-01' then 'sold 2024-26' when p.CHOW_DT>='2023-01-01' then 'sold 2023'
  when p.CHOW_DT>='2021-01-01' then 'sold 2021-22' else 'not sold since 2021' end"""
QUERIES = [
("nndss_integrity_by_year", f"""
select CURRENT_MMWR_YEAR yr, count(*) n,
 count(distinct REPORTING_AREA||'|'||LABEL||'|'||MMWR_WEEK) keys,
 count(distinct REPORTING_AREA) areas, count(distinct LABEL) labels,
 min({WK}) wk_min, max({WK}) wk_max,
 count_if(LOCATION1 is not null and LOCATION1<>'') single_place_rows,
 count_if(upper(REPORTING_AREA)='US RESIDENTS') us_rows
from {N} group by 1 order by 1"""),

("nndss_flags", f"""
select CURRENT_WEEK_FLAG wk_flag, CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG ytd_flag, count(*) n,
 count(CURRENT_WEEK) wk_filled, count(CUMULATIVE_YTD_CURRENT_MMWR_YEAR) ytd_filled,
 max(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar)) ytd_max
from {N} group by 1,2 order by 3 desc limit 20"""),

("nndss_group_rows", f"""
select REPORTING_AREA, LOCATION2, count(*) n from {N}
where LOCATION1 is null or LOCATION1='' group by 1,2 order by 3 desc limit 25"""),

("nndss_us_same_week", f"""
with w as (select max({WK}) wk from {N} where CURRENT_MMWR_YEAR=2026),
x as (select LABEL, CURRENT_MMWR_YEAR yr, max({YTD}) ytd, count(*) k
      from {N}, w where {WK}=w.wk and upper(REPORTING_AREA)='US RESIDENTS' group by 1,2)
select (select wk from w) wk, LABEL, max(iff(yr=2022,ytd,null)) y22, max(iff(yr=2023,ytd,null)) y23,
 max(iff(yr=2024,ytd,null)) y24, max(iff(yr=2025,ytd,null)) y25, max(iff(yr=2026,ytd,null)) y26, max(k) k
from x group by 1,2 having max(iff(yr=2026,ytd,null))>=50
order by y26/greatest(coalesce(greatest(y22,y23,y24,y25),1),1) desc limit 45"""),

("nndss_state_surge", f"""
with w as (select max({WK}) wk from {N} where CURRENT_MMWR_YEAR=2026),
x as (select REPORTING_AREA st, LABEL, CURRENT_MMWR_YEAR yr, max({YTD}) ytd
      from {N}, w where {WK}=w.wk and LOCATION1 is not null and LOCATION1<>'' group by 1,2,3),
s as (select st, LABEL, max(iff(yr=2026,ytd,null)) y26, max(iff(yr=2025,ytd,null)) y25,
        greatest(coalesce(max(iff(yr=2022,ytd,null)),0),coalesce(max(iff(yr=2023,ytd,null)),0),
                 coalesce(max(iff(yr=2024,ytd,null)),0),coalesce(max(iff(yr=2025,ytd,null)),0)) prior_max,
        count(iff(yr<2026,ytd,null)) prior_years
      from x group by 1,2),
d as (select LABEL, sum(y26) d26, sum(prior_max) dprior, count_if(y26>0) states_hit from s group by 1)
select s.st, s.LABEL, s.y26, s.y25, s.prior_max, s.prior_years,
 round(s.y26/greatest(s.prior_max,1),1) ratio, round(d.d26/greatest(d.dprior,1),2) disease_ratio_all_states,
 d.states_hit, round(s.y26/nullif(d.d26,0),3) share_of_us
from s join d using(LABEL)
where s.y26>=15 and s.prior_years>=3
order by s.y26/greatest(s.prior_max,1) / greatest(d.d26/greatest(d.dprior,1),0.1) desc limit 40"""),

("dmf_glp1_holders", f"""
select case when upper(SUBJECT) like '%TIRZEPATIDE%' then 'TIRZEPATIDE' when upper(SUBJECT) like '%SEMAGLUTIDE%' then 'SEMAGLUTIDE'
  when upper(SUBJECT) like '%LIRAGLUTIDE%' then 'LIRAGLUTIDE' end drug, HOLDER, count(*) files,
 min(SUBMIT_DATE) first_dt, max(SUBMIT_DATE) last_dt, count_if(STATUS_CODE='A') active,
 listagg(distinct DMF_TYPE, ',') types
from {DMF} where upper(SUBJECT) like any ('%TIRZEPATIDE%','%SEMAGLUTIDE%','%LIRAGLUTIDE%')
group by 1,2 order by 1, 4"""),

("dmf_trap_checks", f"""
select 'dup_dmf_number' k, count(*)-count(distinct DMF_NUMBER) v, null x from {DMF}
union all select 'blank_subject', count_if(SUBJECT is null or SUBJECT=''), null from {DMF}
union all select 'pre1960_rows', count_if(SUBMIT_DATE<'1960-01-01'), null from {DMF}
union all select 'rows_1960_1994', count_if(SUBMIT_DATE between '1960-01-01' and '1994-12-31'), null from {DMF}
union all select 'null_date', count_if(SUBMIT_DATE is null), null from {DMF}
union all select * from (select 'top_pre1970_date', count(*), SUBMIT_DATE::varchar from {DMF} where SUBMIT_DATE<'1970-01-01' group by 3 order by 2 desc limit 4)
union all select * from (select 'pre1960_sample', try_to_number(DMF_NUMBER), HOLDER||' | '||SUBJECT||' | '||SUBMIT_DATE from {DMF} where SUBMIT_DATE<'1960-01-01' order by DMF_NUMBER limit 5)
union all select 'type_I_count', count_if(DMF_TYPE='I'), null from {DMF}"""),

("hosp_sold_vs_state_peers", f"""
with h as (
 select h.CCN, h.STATE, h.HOSPITAL_OVERALL_RATING r, {SOLD} sold,
  case when h.HOSPITAL_OWNERSHIP='Proprietary' then 'for-profit' when h.HOSPITAL_OWNERSHIP like 'Voluntary%' then 'non-profit' else 'gov/other' end own,
  (sum(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - h.HOSPITAL_OVERALL_RATING)
    / nullif(count(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - 1, 0) st_loo,
  coalesce(h.COUNT_OF_MORT_MEASURES_WORSE,0)+coalesce(h.COUNT_OF_SAFETY_MEASURES_WORSE,0) worse
 from {HG} h join {POS} p on p.CCN=h.CCN
 where h.HOSPITAL_TYPE='Acute Care Hospitals' and h.HOSPITAL_OVERALL_RATING is not null)
select coalesce(own,'ALL') own, sold, count(*) n, round(avg(r),2) avg_star, median(r) med_star,
 round(avg(r - st_loo),2) vs_state_peers, round(count_if(r<=2)/count(*),2) share_1_2,
 round(avg(worse),2) avg_worse_mort_safety, count(distinct STATE) states
from h group by grouping sets ((own, sold), (sold)) order by 1, 2"""),

("hosp_sold_margin", f"""
with h as (select h.CCN, {SOLD} sold, h.HOSPITAL_OWNERSHIP own
           from {HG} h join {POS} p on p.CCN=h.CCN where h.HOSPITAL_TYPE='Acute Care Hospitals')
select sold, count(*) n, count(c.CCN) landed, median(c.OPERATING_MARGIN_PCT) med_margin,
 round(count_if(c.OPERATING_MARGIN_PCT<0)/nullif(count(c.OPERATING_MARGIN_PCT),0),2) share_negative,
 min(c.FY_END) fy_min, max(c.FY_END) fy_max, mode(left(c.FY_END,4)) fy_mode
from h left join LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK c on c.CCN=h.CCN group by 1 order by 1"""),

("pos_termination_codes", f"""
select PRVDR_CTGRY_CD cat, PGM_TRMNTN_CD code, count(*) n,
 count_if(TRMNTN_EXPRTN_DT between '2015-01-01' and '2019-12-31') t15_19,
 count_if(TRMNTN_EXPRTN_DT >= '2020-01-01') t20_26, min(TRMNTN_EXPRTN_DT) first_dt, max(TRMNTN_EXPRTN_DT) last_dt,
 count_if(TRMNTN_EXPRTN_DT is null) no_date
from {POS} where PRVDR_CTGRY_CD in ('01','12') group by 1,2 order by 1,3 desc"""),

("hosp_sold_clusters", f"""
select p.CHOW_DT, p.STATE_CD, count(*) n, listagg(h.FACILITY_NAME||' ['||coalesce(h.HOSPITAL_OVERALL_RATING::varchar,'-')||'*]', '; ') within group (order by h.FACILITY_NAME) hospitals,
 listagg(distinct h.HOSPITAL_OWNERSHIP, ', ') own_now
from {POS} p join {HG} h on h.CCN=p.CCN
where p.PRVDR_CTGRY_CD='01' and p.CHOW_DT>='2021-01-01' and h.HOSPITAL_TYPE='Acute Care Hospitals'
group by 1,2 order by 3 desc, 1 limit 30"""),
]
