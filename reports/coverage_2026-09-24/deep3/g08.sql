-- g08 deep pass 3, 2026-09-24. Every statement run, in order. Read-only.
-- Each connection first ran: ALTER SESSION SET STATEMENT_TIMEOUT_IN_SECONDS = 300; ALTER SESSION SET QUERY_TAG = 'deep3-2026-09-24';

-- [1] pos_profile_by_category
select PRVDR_CTGRY_CD, count(*) n, count(distinct CCN) ccns, count_if(PGM_TRMNTN_CD='00') active,
 count_if(CHOW_CNT>0) chow_any, max(CHOW_CNT) chow_max, count_if(CHOW_DT is not null) chow_dt_filled,
 count_if(CHOW_DT>='2021-01-01') chow_since21, max(CHOW_DT) chow_max_dt,
 min(ORGNL_PRTCPTN_DT) first_join, max(ORGNL_PRTCPTN_DT) last_join, count_if(SKLTN_REC_SW='Y') skeleton,
 count_if(MLT_FAC_ORG_NAME is not null and MLT_FAC_ORG_NAME<>'') has_org_name
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER group by 1 order by 2 desc;

-- [2] pos_hosp_chow_by_year
select year(CHOW_DT) yr, count(*) n, count_if(PGM_TRMNTN_CD='00') still_active,
 count_if(PRVDR_CTGRY_SBTYP_CD='01') short_term, count_if(PRVDR_CTGRY_SBTYP_CD='11') cah,
 count_if(GNRL_CNTL_TYPE_CD in ('04','05','06')) ctl_04_06
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='01' and CHOW_DT>='2010-01-01'
group by 1 order by 1;

-- [3] hg_profile_by_type_owner
select HOSPITAL_TYPE, HOSPITAL_OWNERSHIP, count(*) n, count(HOSPITAL_OVERALL_RATING) rated,
 round(avg(HOSPITAL_OVERALL_RATING),2) avg_star, count_if(HOSPITAL_OVERALL_RATING=1) one_star,
 count_if(HOSPITAL_OVERALL_RATING=5) five_star,
 count(distinct MORT_GROUP_MEASURE_COUNT) d_mort, count(distinct SAFETY_GROUP_MEASURE_COUNT) d_saf,
 count(distinct READM_GROUP_MEASURE_COUNT) d_readm, count(distinct PT_EXP_GROUP_MEASURE_COUNT) d_ptexp
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL group by 1,2 order by 3 desc;

-- [4] hg_to_pos_land_rate
with p as (select CCN, max(CHOW_CNT) chow_cnt, max(CHOW_DT) chow_dt, max(PGM_TRMNTN_CD) trm, count(*) k
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER group by 1)
select h.HOSPITAL_TYPE, count(*) hospitals, count(p.CCN) landed, count_if(p.k>1) dup_pos,
 count_if(p.trm='00') landed_active, count_if(p.chow_cnt>0) chow_any, count_if(p.chow_dt>='2021-01-01') chow_since21,
 count_if(p.chow_dt>='2021-01-01' and h.HOSPITAL_OVERALL_RATING is not null) chow21_rated
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL h left join p on p.CCN=h.CCN
group by 1 order by 2 desc;

-- [5] dmf_by_year_type
select year(SUBMIT_DATE) yr, count(*) n, count_if(DMF_TYPE='II') t2, count_if(DMF_TYPE='III') t3,
 count_if(DMF_TYPE='IV') t4, count_if(DMF_TYPE='V') t5, count_if(STATUS_CODE='A') active,
 count(distinct HOLDER) holders
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where SUBMIT_DATE>='1995-01-01' or SUBMIT_DATE<'1960-01-01'
group by 1 order by 1;

-- [6] dmf_subject_surge
with s as (select regexp_substr(upper(SUBJECT),'[A-Z]{4,}') w, year(SUBMIT_DATE) yr, HOLDER
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where DMF_TYPE='II')
select w, count_if(yr between 2019 and 2022) f19_22, count_if(yr between 2023 and 2026) f23_26,
 count(distinct iff(yr between 2023 and 2026, HOLDER, null)) holders23_26, count(*) all_time
from s where w is not null group by 1
having count_if(yr between 2023 and 2026)>=12
order by f23_26 - f19_22 desc limit 30;

-- [7] nndss_integrity_by_year
select CURRENT_MMWR_YEAR yr, count(*) n,
 count(distinct REPORTING_AREA||'|'||LABEL||'|'||MMWR_WEEK) keys,
 count(distinct REPORTING_AREA) areas, count(distinct LABEL) labels,
 min(try_to_number(MMWR_WEEK)) wk_min, max(try_to_number(MMWR_WEEK)) wk_max,
 count(distinct _SOURCE_RUN_ID) runs,
 count_if(LOCATION1 is not null and LOCATION1<>'') single_place_rows
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1 order by 1;

-- [8] nndss_flags
select CURRENT_WEEK_FLAG, CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG ytd_flag, count(*) n,
 count_if(CURRENT_WEEK is not null and CURRENT_WEEK<>'') wk_filled,
 count_if(CUMULATIVE_YTD_CURRENT_MMWR_YEAR is not null and CUMULATIVE_YTD_CURRENT_MMWR_YEAR<>'') ytd_filled,
 max(try_to_number(CUMULATIVE_YTD_CURRENT_MMWR_YEAR)) ytd_max
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1,2 order by 3 desc limit 20;

-- [9] ihs_lookup_check
select STATUS, ITU_CODE, count(*) n, count(distinct ASUFAC_CODE) codes, count(distinct FACILITY_NAME) names,
 count_if(BED_COUNT>0) with_beds, sum(BED_COUNT) beds, count(distinct FACILITY_TYPE) types,
 count(distinct AREA) areas, count(distinct APC_FLAG) apc_vals
from LIBRARY_MARTS.HEALTH.HEALTH__FED_IHS_SCB_FACILITY group by 1,2 order by 3 desc;

-- [10] nndss_integrity_by_year
select CURRENT_MMWR_YEAR yr, count(*) n,
 count(distinct REPORTING_AREA||'|'||LABEL||'|'||MMWR_WEEK) keys,
 count(distinct REPORTING_AREA) areas, count(distinct LABEL) labels,
 min(try_to_number(MMWR_WEEK::varchar)) wk_min, max(try_to_number(MMWR_WEEK::varchar)) wk_max,
 count_if(LOCATION1 is not null and LOCATION1<>'') single_place_rows,
 count_if(upper(REPORTING_AREA)='US RESIDENTS') us_rows
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1 order by 1;

-- [11] nndss_flags
select CURRENT_WEEK_FLAG wk_flag, CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG ytd_flag, count(*) n,
 count(CURRENT_WEEK) wk_filled, count(CUMULATIVE_YTD_CURRENT_MMWR_YEAR) ytd_filled,
 max(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar)) ytd_max
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1,2 order by 3 desc limit 20;

-- [12] nndss_group_rows
select REPORTING_AREA, LOCATION2, count(*) n from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024
where LOCATION1 is null or LOCATION1='' group by 1,2 order by 3 desc limit 25;

-- [13] nndss_us_same_week
with w as (select max(try_to_number(MMWR_WEEK::varchar)) wk from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 where CURRENT_MMWR_YEAR=2026),
x as (select LABEL, CURRENT_MMWR_YEAR yr, max(coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))) ytd, count(*) k
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024, w where try_to_number(MMWR_WEEK::varchar)=w.wk and upper(REPORTING_AREA)='US RESIDENTS' group by 1,2)
select (select wk from w) wk, LABEL, max(iff(yr=2022,ytd,null)) y22, max(iff(yr=2023,ytd,null)) y23,
 max(iff(yr=2024,ytd,null)) y24, max(iff(yr=2025,ytd,null)) y25, max(iff(yr=2026,ytd,null)) y26, max(k) k
from x group by 1,2 having max(iff(yr=2026,ytd,null))>=50
order by y26/greatest(coalesce(greatest(y22,y23,y24,y25),1),1) desc limit 45;

-- [14] nndss_state_surge
with w as (select max(try_to_number(MMWR_WEEK::varchar)) wk from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 where CURRENT_MMWR_YEAR=2026),
x as (select REPORTING_AREA st, LABEL, CURRENT_MMWR_YEAR yr, max(coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))) ytd
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024, w where try_to_number(MMWR_WEEK::varchar)=w.wk and LOCATION1 is not null and LOCATION1<>'' group by 1,2,3),
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
order by s.y26/greatest(s.prior_max,1) / greatest(d.d26/greatest(d.dprior,1),0.1) desc limit 40;

-- [15] dmf_glp1_holders
select case when upper(SUBJECT) like '%TIRZEPATIDE%' then 'TIRZEPATIDE' when upper(SUBJECT) like '%SEMAGLUTIDE%' then 'SEMAGLUTIDE'
  when upper(SUBJECT) like '%LIRAGLUTIDE%' then 'LIRAGLUTIDE' end drug, HOLDER, count(*) files,
 min(SUBMIT_DATE) first_dt, max(SUBMIT_DATE) last_dt, count_if(STATUS_CODE='A') active,
 listagg(distinct DMF_TYPE, ',') types
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where upper(SUBJECT) like any ('%TIRZEPATIDE%','%SEMAGLUTIDE%','%LIRAGLUTIDE%')
group by 1,2 order by 1, 4;

-- [16] dmf_trap_checks
select 'dup_dmf_number' k, count(*)-count(distinct DMF_NUMBER) v, null x from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
union all select 'blank_subject', count_if(SUBJECT is null or SUBJECT=''), null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
union all select 'pre1960_rows', count_if(SUBMIT_DATE<'1960-01-01'), null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
union all select 'rows_1960_1994', count_if(SUBMIT_DATE between '1960-01-01' and '1994-12-31'), null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
union all select 'null_date', count_if(SUBMIT_DATE is null), null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
union all select * from (select 'top_pre1970_date', count(*), SUBMIT_DATE::varchar from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where SUBMIT_DATE<'1970-01-01' group by 3 order by 2 desc limit 4)
union all select * from (select 'pre1960_sample', try_to_number(DMF_NUMBER), HOLDER||' | '||SUBJECT||' | '||SUBMIT_DATE from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where SUBMIT_DATE<'1960-01-01' order by DMF_NUMBER limit 5)
union all select 'type_I_count', count_if(DMF_TYPE='I'), null from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES;

-- [17] hosp_sold_vs_state_peers
with h as (
 select h.CCN, h.STATE, h.HOSPITAL_OVERALL_RATING r, case when p.CHOW_DT>='2024-01-01' then 'sold 2024-26' when p.CHOW_DT>='2023-01-01' then 'sold 2023'
  when p.CHOW_DT>='2021-01-01' then 'sold 2021-22' else 'not sold since 2021' end sold,
  case when h.HOSPITAL_OWNERSHIP='Proprietary' then 'for-profit' when h.HOSPITAL_OWNERSHIP like 'Voluntary%' then 'non-profit' else 'gov/other' end own,
  (sum(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - h.HOSPITAL_OVERALL_RATING)
    / nullif(count(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - 1, 0) st_loo,
  coalesce(h.COUNT_OF_MORT_MEASURES_WORSE,0)+coalesce(h.COUNT_OF_SAFETY_MEASURES_WORSE,0) worse
 from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL h join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p on p.CCN=h.CCN
 where h.HOSPITAL_TYPE='Acute Care Hospitals' and h.HOSPITAL_OVERALL_RATING is not null)
select coalesce(own,'ALL') own, sold, count(*) n, round(avg(r),2) avg_star, median(r) med_star,
 round(avg(r - st_loo),2) vs_state_peers, round(count_if(r<=2)/count(*),2) share_1_2,
 round(avg(worse),2) avg_worse_mort_safety, count(distinct STATE) states
from h group by grouping sets ((own, sold), (sold)) order by 1, 2;

-- [18] hosp_sold_margin
with h as (select h.CCN, case when p.CHOW_DT>='2024-01-01' then 'sold 2024-26' when p.CHOW_DT>='2023-01-01' then 'sold 2023'
  when p.CHOW_DT>='2021-01-01' then 'sold 2021-22' else 'not sold since 2021' end sold, h.HOSPITAL_OWNERSHIP own
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL h join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p on p.CCN=h.CCN where h.HOSPITAL_TYPE='Acute Care Hospitals')
select sold, count(*) n, count(c.CCN) landed, median(c.OPERATING_MARGIN_PCT) med_margin,
 round(count_if(c.OPERATING_MARGIN_PCT<0)/nullif(count(c.OPERATING_MARGIN_PCT),0),2) share_negative,
 min(c.FY_END) fy_min, max(c.FY_END) fy_max, mode(left(c.FY_END,4)) fy_mode
from h left join LIBRARY_MARTS.FINDINGS.HOSPITAL_CLOSURE_RISK c on c.CCN=h.CCN group by 1 order by 1;

-- [19] pos_termination_codes
select PRVDR_CTGRY_CD cat, PGM_TRMNTN_CD code, count(*) n,
 count_if(TRMNTN_EXPRTN_DT between '2015-01-01' and '2019-12-31') t15_19,
 count_if(TRMNTN_EXPRTN_DT >= '2020-01-01') t20_26, min(TRMNTN_EXPRTN_DT) first_dt, max(TRMNTN_EXPRTN_DT) last_dt,
 count_if(TRMNTN_EXPRTN_DT is null) no_date
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD in ('01','12') group by 1,2 order by 1,3 desc;

-- [20] hosp_sold_clusters
select p.CHOW_DT, p.STATE_CD, count(*) n, listagg(h.FACILITY_NAME||' ['||coalesce(h.HOSPITAL_OVERALL_RATING::varchar,'-')||'*]', '; ') within group (order by h.FACILITY_NAME) hospitals,
 listagg(distinct h.HOSPITAL_OWNERSHIP, ', ') own_now
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL h on h.CCN=p.CCN
where p.PRVDR_CTGRY_CD='01' and p.CHOW_DT>='2021-01-01' and h.HOSPITAL_TYPE='Acute Care Hospitals'
group by 1,2 order by 3 desc, 1 limit 30;

-- [21] nndss_us_same_week_v2
with w as (select max(try_to_number(MMWR_WEEK::varchar)) wk from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 where CURRENT_MMWR_YEAR=2026),
x as (select LABEL, CURRENT_MMWR_YEAR yr, max(coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))) ytd, count(*) k
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024, w where try_to_number(MMWR_WEEK::varchar)=w.wk and replace(upper(REPORTING_AREA),'.','')='US RESIDENTS' group by 1,2)
select (select wk from w) wk, LABEL, max(iff(yr=2022,ytd,null)) y22, max(iff(yr=2023,ytd,null)) y23,
 max(iff(yr=2024,ytd,null)) y24, max(iff(yr=2025,ytd,null)) y25, max(iff(yr=2026,ytd,null)) y26, max(k) k
from x group by 1,2 having max(iff(yr=2026,ytd,null))>=30
order by max(iff(yr=2026,ytd,null))/greatest(coalesce(max(iff(yr<2026,ytd,null)),1),1) desc limit 40;

-- [22] nndss_state_surge_v2
with w as (select max(try_to_number(MMWR_WEEK::varchar)) wk from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 where CURRENT_MMWR_YEAR=2026),
x as (select replace(upper(REPORTING_AREA),'.','') st, LABEL, CURRENT_MMWR_YEAR yr, max(coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))) ytd
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024, w where try_to_number(MMWR_WEEK::varchar)=w.wk and LOCATION1 is not null and LOCATION1<>'' group by 1,2,3),
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
order by s.y26/greatest(s.prior_max,1) / greatest(d.d26/greatest(d.dprior,1),0.1) desc limit 40;

-- [23] nndss_label_drift_week53
select LABEL, min(CURRENT_MMWR_YEAR) first_yr, max(CURRENT_MMWR_YEAR) last_yr, count(distinct CURRENT_MMWR_YEAR) yrs,
 count_if(try_to_number(MMWR_WEEK::varchar)=53) wk53_rows, count(distinct replace(upper(REPORTING_AREA),'.','')) areas
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1 having count(distinct CURRENT_MMWR_YEAR)<5 or count_if(try_to_number(MMWR_WEEK::varchar)=53)>0
order by 3, 2, 1 limit 60;

-- [24] dmf_busiest_4yr_window
with s as (select regexp_substr(upper(SUBJECT),'[A-Z]{5,}') w, year(SUBMIT_DATE) yr
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where DMF_TYPE='II' and SUBMIT_DATE>='1980-01-01'),
y as (select w, yr, count(*) n from s where w is not null group by 1,2),
win as (select a.w, a.yr start_yr, sum(b.n) n4 from y a join y b on b.w=a.w and b.yr between a.yr and a.yr+3 group by 1,2),
best as (select w, start_yr, n4, row_number() over (partition by w order by n4 desc, start_yr) rn from win)
select w, start_yr, n4 from best where rn=1 order by n4 desc limit 30;

-- [25] glp1_recalls_vs_dmf_holders
with r as (select year(RECALL_INITIATION_DATE) yr, upper(trim(RECALLING_FIRM)) firm, COUNTRY, CLASSIFICATION, EVENT_ID,
             case when upper(PRODUCT_DESCRIPTION) like '%TIRZEPATIDE%' then 'TIRZEPATIDE'
                  when upper(PRODUCT_DESCRIPTION) like '%SEMAGLUTIDE%' then 'SEMAGLUTIDE' else 'LIRAGLUTIDE' end drug
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT where upper(PRODUCT_DESCRIPTION) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%','%LIRAGLUTIDE%')),
h as (select distinct upper(trim(HOLDER)) holder from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
      where upper(SUBJECT) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%','%LIRAGLUTIDE%'))
select yr, drug, count(*) recall_rows, count(distinct EVENT_ID) events, count(distinct firm) firms,
 count_if(h.holder is not null) rows_firm_is_dmf_holder,
 listagg(distinct firm, '; ') within group (order by firm) firm_list, listagg(distinct COUNTRY, ',') countries
from r left join h on h.holder=r.firm group by 1,2 order by 1,2;

-- [26] hosp_sold_deal_vs_lone
with p as (select CCN, CHOW_DT, count(*) over (partition by CHOW_DT, STATE_CD) deal_n
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='01' and CHOW_DT is not null),
h as (select h.CCN, h.STATE, h.HOSPITAL_OVERALL_RATING r,
        case when h.HOSPITAL_OWNERSHIP='Proprietary' then 'for-profit' when h.HOSPITAL_OWNERSHIP like 'Voluntary%' then 'non-profit' else 'gov/other' end own,
        (sum(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - h.HOSPITAL_OVERALL_RATING)
          / nullif(count(h.HOSPITAL_OVERALL_RATING) over (partition by h.STATE) - 1, 0) st_loo,
        case when p.CHOW_DT>='2023-01-01' and p.deal_n>=2 then 'b sold 2023-26, multi-hospital same-day deal'
             when p.CHOW_DT>='2023-01-01' then 'c sold 2023-26, lone sale' else 'a not sold since 2023' end grp
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL h left join p on p.CCN=h.CCN
      where h.HOSPITAL_TYPE='Acute Care Hospitals' and h.HOSPITAL_OVERALL_RATING is not null)
select grp, coalesce(own,'ALL') own, count(*) n, round(avg(r),2) avg_star, median(r) med_star,
 round(avg(r - st_loo),2) vs_state_peers, round(count_if(r<=2)/count(*),2) share_1_2, count(distinct STATE) states
from h group by grouping sets ((grp), (grp, own)) order by 1, 2;

-- [27] hosp_worst_mortality_safety
select h.FACILITY_NAME, h.CITY_TOWN, h.STATE, h.HOSPITAL_OWNERSHIP own, h.HOSPITAL_OVERALL_RATING star,
 h.COUNT_OF_FACILITY_MORT_MEASURES mort_n, h.COUNT_OF_MORT_MEASURES_WORSE mort_worse,
 h.COUNT_OF_SAFETY_MEASURES_WORSE saf_worse, h.COUNT_OF_READM_MEASURES_WORSE readm_worse,
 p.CHOW_DT, p.CHOW_CNT,
 count_if(h.COUNT_OF_MORT_MEASURES_WORSE>=1) over () n_mort_worse_1plus,
 count_if(h.COUNT_OF_MORT_MEASURES_WORSE>=2) over () n_mort_worse_2plus,
 count(h.COUNT_OF_MORT_MEASURES_WORSE) over () n_mort_scored
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL h left join LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER p on p.CCN=h.CCN
qualify h.COUNT_OF_MORT_MEASURES_WORSE>=2 or (coalesce(h.COUNT_OF_MORT_MEASURES_WORSE,0)+coalesce(h.COUNT_OF_SAFETY_MEASURES_WORSE,0))>=4
order by h.COUNT_OF_MORT_MEASURES_WORSE desc, h.COUNT_OF_SAFETY_MEASURES_WORSE desc limit 40;

-- [28] nndss_weekly_drill
select replace(upper(REPORTING_AREA),'.','') st, LABEL, CURRENT_MMWR_YEAR yr,
 listagg(coalesce(CURRENT_WEEK::varchar, CURRENT_WEEK_FLAG), ',') within group (order by try_to_number(MMWR_WEEK::varchar)) weekly_1_30,
 listagg(iff(mod(try_to_number(MMWR_WEEK::varchar),5)=0, coalesce(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar, CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG), null), ',')
   within group (order by try_to_number(MMWR_WEEK::varchar)) ytd_every5,
 sum(try_to_double(CURRENT_WEEK::varchar)) sum_weekly
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024
where CURRENT_MMWR_YEAR in (2025, 2026) and try_to_number(MMWR_WEEK::varchar)<=30
 and ((LABEL='Cyclosporiasis' and replace(upper(REPORTING_AREA),'.','') in ('MICHIGAN','OHIO','NEW JERSEY','US RESIDENTS'))
   or (LABEL='Arboviral diseases, Chikungunya virus disease' and replace(upper(REPORTING_AREA),'.','')='FLORIDA')
   or (LABEL='Candida auris, clinical' and replace(upper(REPORTING_AREA),'.','')='TENNESSEE')
   or (LABEL='Measles, Indigenous' and replace(upper(REPORTING_AREA),'.','') in ('VIRGINIA','PENNSYLVANIA')))
group by 1,2,3 order by 2,1,3;

-- [29] glp1_recall_detail
with h as (select distinct regexp_replace(upper(HOLDER),'[^A-Z0-9]','') hk, HOLDER from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES
           where upper(SUBJECT) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%','%LIRAGLUTIDE%'))
select e.EVENT_ID, min(e.RECALL_INITIATION_DATE) started, e.RECALLING_FIRM, max(e.CITY) city, max(e.COUNTRY) country,
 max(e.CLASSIFICATION) class, max(e.STATUS) status, count(*) rows_n, max(h.HOLDER) dmf_holder_match,
 left(max(e.PRODUCT_DESCRIPTION),160) product, left(max(e.REASON_FOR_RECALL),260) reason, left(max(e.DISTRIBUTION_PATTERN),120) distribution
from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT e left join h on h.hk=regexp_replace(upper(e.RECALLING_FIRM),'[^A-Z0-9]','')
where upper(e.PRODUCT_DESCRIPTION) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%') and e.RECALL_INITIATION_DATE>='2025-01-01'
group by 1,3 order by 2;

-- [30] hosp_mortality_worse_by_state
select coalesce(STATE,'US') st, count(*) scored_7plus,
 count_if(COUNT_OF_MORT_MEASURES_WORSE>=1) worse_1plus, count_if(COUNT_OF_MORT_MEASURES_WORSE>=2) worse_2plus,
 count_if(COUNT_OF_MORT_MEASURES_BETTER>=1) better_1plus,
 round(count_if(COUNT_OF_MORT_MEASURES_WORSE>=1)/count(*),3) share_worse,
 round(count_if(COUNT_OF_MORT_MEASURES_BETTER>=1)/count(*),3) share_better,
 sum(COUNT_OF_MORT_MEASURES_WORSE) worse_measures, sum(COUNT_OF_MORT_MEASURES_BETTER) better_measures
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL where COUNT_OF_FACILITY_MORT_MEASURES>=7
group by grouping sets ((STATE), ())
having count(*)>=10
order by iff(STATE is null,0,1), share_worse desc limit 16;

-- [31] dmf_holder_recalled_own_ingredient
with d as (select regexp_replace(upper(HOLDER),'[^A-Z0-9]','') hk, HOLDER,
                  regexp_substr(upper(SUBJECT),'[A-Z]{6,}') w
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_MASTER_FILES where DMF_TYPE='II'),
e as (select regexp_replace(upper(RECALLING_FIRM),'[^A-Z0-9]','') hk, EVENT_ID, RECALL_INITIATION_DATE dt, COUNTRY,
             upper(PRODUCT_DESCRIPTION) pd, CLASSIFICATION from LIBRARY_MARTS.HEALTH.HEALTH__FED_FDA_DRUG_ENFORCEMENT),
firm_hit as (select count(distinct e.hk) firms_all, count(distinct iff(d.hk is not null, e.hk, null)) firms_are_holders
             from (select distinct hk from e) e left join (select distinct hk from d) d on d.hk=e.hk),
m as (select d.HOLDER, e.COUNTRY, e.EVENT_ID, e.dt, e.CLASSIFICATION, d.w
      from e join d on d.hk=e.hk and d.w is not null and position(d.w in e.pd)>0)
select (select firms_all from firm_hit) firms_all, (select firms_are_holders from firm_hit) firms_are_holders,
 HOLDER, max(COUNTRY) country, count(distinct EVENT_ID) events, listagg(distinct w, ',') ingredients,
 min(dt) first_recall, max(dt) last_recall, count_if(CLASSIFICATION='Class I') class1_rows
from m group by 3 order by events desc, last_recall desc limit 30;

-- [32] nndss_cyclo_by_state
with w as (select max(try_to_number(MMWR_WEEK::varchar)) wk from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024 where CURRENT_MMWR_YEAR=2026),
x as (select replace(upper(REPORTING_AREA),'.','') st, CURRENT_MMWR_YEAR yr, max(coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))) ytd
      from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_NNDSS_WEEKLY_2024, w where try_to_number(MMWR_WEEK::varchar)=w.wk and LABEL='Cyclosporiasis' and LOCATION1 is not null and LOCATION1<>'' group by 1,2),
s as (select st, max(iff(yr=2026,ytd,null)) y26, max(iff(yr=2025,ytd,null)) y25,
        greatest(coalesce(max(iff(yr=2022,ytd,null)),0),coalesce(max(iff(yr=2023,ytd,null)),0),
                 coalesce(max(iff(yr=2024,ytd,null)),0),coalesce(max(iff(yr=2025,ytd,null)),0)) prior_max
      from x group by 1)
select st, y26, y25, prior_max, round(y26/greatest(prior_max,1),1) ratio,
 sum(y26) over () us26, count_if(y26>0) over () states_any, count_if(y26>2*greatest(prior_max,1)) over () states_doubled,
 median(y26) over () median_state_26, median(prior_max) over () median_state_prior
from s qualify y26>=10 order by y26 desc;

-- [33] ms_hospitals_mortality
select STATE, FACILITY_NAME, CITY_TOWN, HOSPITAL_OWNERSHIP own, HOSPITAL_OVERALL_RATING star,
 COUNT_OF_FACILITY_MORT_MEASURES mort_n, COUNT_OF_MORT_MEASURES_WORSE mort_worse, COUNT_OF_MORT_MEASURES_BETTER mort_better,
 COUNT_OF_SAFETY_MEASURES_WORSE saf_worse, COUNT_OF_READM_MEASURES_WORSE readm_worse, COUNT_OF_READM_MEASURES_BETTER readm_better
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_GENERAL where STATE in ('MS','AR') and COUNT_OF_FACILITY_MORT_MEASURES>=7
order by STATE, mort_worse desc, mort_better;

-- [34] pos_code05_06_since_2015
select PRVDR_CTGRY_CD cat, PRVDR_CTGRY_SBTYP_CD sub, PGM_TRMNTN_CD code, TRMNTN_EXPRTN_DT ended, FAC_NAME, CITY_NAME, STATE_CD,
 CHOW_CNT, CHOW_DT, ORGNL_PRTCPTN_DT joined, GNRL_CNTL_TYPE_CD ctl, BED_CNT
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PGM_TRMNTN_CD in ('05','06') and TRMNTN_EXPRTN_DT>='2015-01-01'
order by TRMNTN_EXPRTN_DT desc;

-- [35] pos_chow_churn_by_exit_type
select case when PGM_TRMNTN_CD='00' then 'a active'
            when PGM_TRMNTN_CD in ('05','06') and TRMNTN_EXPRTN_DT>='2015-01-01' then 'b ended 05/06 since 2015'
            when PGM_TRMNTN_CD='01' and TRMNTN_EXPRTN_DT>='2015-01-01' then 'c ended 01 since 2015'
            else 'd other ended' end grp,
 count(*) n, count_if(CHOW_CNT>=3) chow3, round(count_if(CHOW_CNT>=3)/count(*),3) share_chow3,
 count_if(CHOW_CNT>=1) chow1, round(count_if(CHOW_CNT>=1)/count(*),3) share_chow1, median(CHOW_CNT) med_chow,
 count_if(CHOW_DT>=dateadd(year,-3,TRMNTN_EXPRTN_DT)) chow_within_3y_of_end,
 median(year(ORGNL_PRTCPTN_DT)) med_join_year,
 count_if(CHOW_CNT>=3 and year(ORGNL_PRTCPTN_DT)=1966) chow3_joined_1966, count_if(year(ORGNL_PRTCPTN_DT)=1966) joined_1966
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='01' and PRVDR_CTGRY_SBTYP_CD='01'
group by 1 order by 1;

-- Notes: [7] failed (no _SOURCE_RUN_ID column), [8] failed (TRY_CAST on a FLOAT); both rerun fixed as [10], [11].
-- [13] and [14] returned zero rows because area names change case in 2025 (the trap); rerun fixed as [21], [22].
-- 35 SELECT/WITH statements over 7 connections; each connection also ran the 2 required ALTER SESSION lines.
