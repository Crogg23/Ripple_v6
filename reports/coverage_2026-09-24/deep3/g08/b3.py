P = "LIBRARY_MARTS.HEALTH."
N = P + "HEALTH__FED_CDC_NNDSS_WEEKLY_2024"
POS = P + "HEALTH__FED_CMS_POS_OTHER"
HG = P + "HEALTH__FED_CMS_HOSPITAL_GENERAL"
DMF = P + "HEALTH__FED_FDA_DRUG_MASTER_FILES"
ENF = P + "HEALTH__FED_FDA_DRUG_ENFORCEMENT"
WK = "try_to_number(MMWR_WEEK::varchar)"
YTD = ("coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), "
       "iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))")
AREA = "replace(upper(REPORTING_AREA),'.','')"
QUERIES = [
("nndss_us_same_week_v2", f"""
with w as (select max({WK}) wk from {N} where CURRENT_MMWR_YEAR=2026),
x as (select LABEL, CURRENT_MMWR_YEAR yr, max({YTD}) ytd, count(*) k
      from {N}, w where {WK}=w.wk and {AREA}='US RESIDENTS' group by 1,2)
select (select wk from w) wk, LABEL, max(iff(yr=2022,ytd,null)) y22, max(iff(yr=2023,ytd,null)) y23,
 max(iff(yr=2024,ytd,null)) y24, max(iff(yr=2025,ytd,null)) y25, max(iff(yr=2026,ytd,null)) y26, max(k) k
from x group by 1,2 having max(iff(yr=2026,ytd,null))>=30
order by max(iff(yr=2026,ytd,null))/greatest(coalesce(max(iff(yr<2026,ytd,null)),1),1) desc limit 40"""),

("nndss_state_surge_v2", f"""
with w as (select max({WK}) wk from {N} where CURRENT_MMWR_YEAR=2026),
x as (select {AREA} st, LABEL, CURRENT_MMWR_YEAR yr, max({YTD}) ytd
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

("nndss_label_drift_week53", f"""
select LABEL, min(CURRENT_MMWR_YEAR) first_yr, max(CURRENT_MMWR_YEAR) last_yr, count(distinct CURRENT_MMWR_YEAR) yrs,
 count_if({WK}=53) wk53_rows, count(distinct {AREA}) areas
from {N} group by 1 having count(distinct CURRENT_MMWR_YEAR)<5 or count_if({WK}=53)>0
order by 3, 2, 1 limit 60"""),

("dmf_busiest_4yr_window", f"""
with s as (select regexp_substr(upper(SUBJECT),'[A-Z]{{5,}}') w, year(SUBMIT_DATE) yr
           from {DMF} where DMF_TYPE='II' and SUBMIT_DATE>='1980-01-01'),
y as (select w, yr, count(*) n from s where w is not null group by 1,2),
win as (select a.w, a.yr start_yr, sum(b.n) n4 from y a join y b on b.w=a.w and b.yr between a.yr and a.yr+3 group by 1,2),
best as (select w, start_yr, n4, row_number() over (partition by w order by n4 desc, start_yr) rn from win)
select w, start_yr, n4 from best where rn=1 order by n4 desc limit 30"""),

("glp1_recalls_vs_dmf_holders", f"""
with r as (select year(RECALL_INITIATION_DATE) yr, upper(trim(RECALLING_FIRM)) firm, COUNTRY, CLASSIFICATION, EVENT_ID,
             case when upper(PRODUCT_DESCRIPTION) like '%TIRZEPATIDE%' then 'TIRZEPATIDE'
                  when upper(PRODUCT_DESCRIPTION) like '%SEMAGLUTIDE%' then 'SEMAGLUTIDE' else 'LIRAGLUTIDE' end drug
           from {ENF} where upper(PRODUCT_DESCRIPTION) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%','%LIRAGLUTIDE%')),
h as (select distinct upper(trim(HOLDER)) holder from {DMF}
      where upper(SUBJECT) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%','%LIRAGLUTIDE%'))
select yr, drug, count(*) recall_rows, count(distinct EVENT_ID) events, count(distinct firm) firms,
 count_if(h.holder is not null) rows_firm_is_dmf_holder,
 listagg(distinct firm, '; ') within group (order by firm) firm_list, listagg(distinct COUNTRY, ',') countries
from r left join h on h.holder=r.firm group by 1,2 order by 1,2"""),

("hosp_sold_deal_vs_lone", f"""
with p as (select CCN, CHOW_DT, count(*) over (partition by CHOW_DT, STATE_CD) deal_n
           from {POS} where PRVDR_CTGRY_CD='01' and CHOW_DT is not null),
h as (select h.CCN, h.STATE, h.HOSPITAL_OVERALL_RATING r,
        case when h.HOSPITAL_OWNERSHIP='Proprietary' then 'for-profit' when h.HOSPITAL_OWNERSHIP like 'Voluntary%' then 'non-profit' else 'gov/other' end own,
        (sum(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - h.HOSPITAL_OVERALL_RATING)
          / nullif(count(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - 1, 0) st_loo,
        case when p.CHOW_DT>='2023-01-01' and p.deal_n>=2 then 'b sold 2023-26, multi-hospital same-day deal'
             when p.CHOW_DT>='2023-01-01' then 'c sold 2023-26, lone sale' else 'a not sold since 2023' end grp
      from {HG} h left join p on p.CCN=h.CCN
      where h.HOSPITAL_TYPE='Acute Care Hospitals' and h.HOSPITAL_OVERALL_RATING is not null)
select grp, coalesce(own,'ALL') own, count(*) n, round(avg(r),2) avg_star, median(r) med_star,
 round(avg(r - st_loo),2) vs_state_peers, round(count_if(r<=2)/count(*),2) share_1_2, count(distinct STATE) states
from h group by grouping sets ((grp), (grp, own)) order by 1, 2"""),

("hosp_worst_mortality_safety", f"""
select h.FACILITY_NAME, h.CITY_TOWN, h.STATE, h.HOSPITAL_OWNERSHIP own, h.HOSPITAL_OVERALL_RATING star,
 h.COUNT_OF_FACILITY_MORT_MEASURES mort_n, h.COUNT_OF_MORT_MEASURES_WORSE mort_worse,
 h.COUNT_OF_SAFETY_MEASURES_WORSE saf_worse, h.COUNT_OF_READM_MEASURES_WORSE readm_worse,
 p.CHOW_DT, p.CHOW_CNT,
 count_if(h.COUNT_OF_MORT_MEASURES_WORSE>=1) over () n_mort_worse_1plus,
 count_if(h.COUNT_OF_MORT_MEASURES_WORSE>=2) over () n_mort_worse_2plus,
 count(h.COUNT_OF_MORT_MEASURES_WORSE) over () n_mort_scored
from {HG} h left join {POS} p on p.CCN=h.CCN
qualify h.COUNT_OF_MORT_MEASURES_WORSE>=2 or (coalesce(h.COUNT_OF_MORT_MEASURES_WORSE,0)+coalesce(h.COUNT_OF_SAFETY_MEASURES_WORSE,0))>=4
order by h.COUNT_OF_MORT_MEASURES_WORSE desc, h.COUNT_OF_SAFETY_MEASURES_WORSE desc limit 40"""),
]
