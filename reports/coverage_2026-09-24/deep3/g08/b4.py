P = "LIBRARY_MARTS.HEALTH."
N = P + "HEALTH__FED_CDC_NNDSS_WEEKLY_2024"
HG = P + "HEALTH__FED_CMS_HOSPITAL_GENERAL"
DMF = P + "HEALTH__FED_FDA_DRUG_MASTER_FILES"
ENF = P + "HEALTH__FED_FDA_DRUG_ENFORCEMENT"
WK = "try_to_number(MMWR_WEEK::varchar)"
AREA = "replace(upper(REPORTING_AREA),'.','')"
QUERIES = [
("nndss_weekly_drill", f"""
select {AREA} st, LABEL, CURRENT_MMWR_YEAR yr,
 listagg(coalesce(CURRENT_WEEK::varchar, CURRENT_WEEK_FLAG), ',') within group (order by {WK}) weekly_1_30,
 listagg(iff(mod({WK},5)=0, coalesce(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar, CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG), null), ',')
   within group (order by {WK}) ytd_every5,
 sum(try_to_double(CURRENT_WEEK::varchar)) sum_weekly
from {N}
where CURRENT_MMWR_YEAR in (2025, 2026) and {WK}<=30
 and ((LABEL='Cyclosporiasis' and {AREA} in ('MICHIGAN','OHIO','NEW JERSEY','US RESIDENTS'))
   or (LABEL='Arboviral diseases, Chikungunya virus disease' and {AREA}='FLORIDA')
   or (LABEL='Candida auris, clinical' and {AREA}='TENNESSEE')
   or (LABEL='Measles, Indigenous' and {AREA} in ('VIRGINIA','PENNSYLVANIA')))
group by 1,2,3 order by 2,1,3"""),

("glp1_recall_detail", f"""
with h as (select distinct regexp_replace(upper(HOLDER),'[^A-Z0-9]','') hk, HOLDER from {DMF}
           where upper(SUBJECT) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%','%LIRAGLUTIDE%'))
select e.EVENT_ID, min(e.RECALL_INITIATION_DATE) started, e.RECALLING_FIRM, max(e.CITY) city, max(e.COUNTRY) country,
 max(e.CLASSIFICATION) class, max(e.STATUS) status, count(*) rows_n, max(h.HOLDER) dmf_holder_match,
 left(max(e.PRODUCT_DESCRIPTION),160) product, left(max(e.REASON_FOR_RECALL),260) reason, left(max(e.DISTRIBUTION_PATTERN),120) distribution
from {ENF} e left join h on h.hk=regexp_replace(upper(e.RECALLING_FIRM),'[^A-Z0-9]','')
where upper(e.PRODUCT_DESCRIPTION) like any ('%SEMAGLUTIDE%','%TIRZEPATIDE%') and e.RECALL_INITIATION_DATE>='2025-01-01'
group by 1,3 order by 2"""),

("hosp_mortality_worse_by_state", f"""
select coalesce(STATE,'US') st, count(*) scored_7plus,
 count_if(COUNT_OF_MORT_MEASURES_WORSE>=1) worse_1plus, count_if(COUNT_OF_MORT_MEASURES_WORSE>=2) worse_2plus,
 count_if(COUNT_OF_MORT_MEASURES_BETTER>=1) better_1plus,
 round(count_if(COUNT_OF_MORT_MEASURES_WORSE>=1)/count(*),3) share_worse,
 round(count_if(COUNT_OF_MORT_MEASURES_BETTER>=1)/count(*),3) share_better,
 sum(COUNT_OF_MORT_MEASURES_WORSE) worse_measures, sum(COUNT_OF_MORT_MEASURES_BETTER) better_measures
from {HG} where COUNT_OF_FACILITY_MORT_MEASURES>=7
group by grouping sets ((STATE), ())
having count(*)>=10
order by iff(STATE is null,0,1), share_worse desc limit 16"""),
]
