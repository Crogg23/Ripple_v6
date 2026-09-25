P = "LIBRARY_MARTS.HEALTH."
N = P + "HEALTH__FED_CDC_NNDSS_WEEKLY_2024"
HG = P + "HEALTH__FED_CMS_HOSPITAL_GENERAL"
DMF = P + "HEALTH__FED_FDA_DRUG_MASTER_FILES"
ENF = P + "HEALTH__FED_FDA_DRUG_ENFORCEMENT"
WK = "try_to_number(MMWR_WEEK::varchar)"
AREA = "replace(upper(REPORTING_AREA),'.','')"
YTD = ("coalesce(try_to_double(CUMULATIVE_YTD_CURRENT_MMWR_YEAR::varchar), "
       "iff(CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG='-',0,null))")
QUERIES = [
("dmf_holder_recalled_own_ingredient", f"""
with d as (select regexp_replace(upper(HOLDER),'[^A-Z0-9]','') hk, HOLDER,
                  regexp_substr(upper(SUBJECT),'[A-Z]{{6,}}') w
           from {DMF} where DMF_TYPE='II'),
e as (select regexp_replace(upper(RECALLING_FIRM),'[^A-Z0-9]','') hk, EVENT_ID, RECALL_INITIATION_DATE dt, COUNTRY,
             upper(PRODUCT_DESCRIPTION) pd, CLASSIFICATION from {ENF}),
firm_hit as (select count(distinct e.hk) firms_all, count(distinct iff(d.hk is not null, e.hk, null)) firms_are_holders
             from (select distinct hk from e) e left join (select distinct hk from d) d on d.hk=e.hk),
m as (select d.HOLDER, e.COUNTRY, e.EVENT_ID, e.dt, e.CLASSIFICATION, d.w
      from e join d on d.hk=e.hk and d.w is not null and position(d.w in e.pd)>0)
select (select firms_all from firm_hit) firms_all, (select firms_are_holders from firm_hit) firms_are_holders,
 HOLDER, max(COUNTRY) country, count(distinct EVENT_ID) events, listagg(distinct w, ',') ingredients,
 min(dt) first_recall, max(dt) last_recall, count_if(CLASSIFICATION='Class I') class1_rows
from m group by 3 order by events desc, last_recall desc limit 30"""),

("nndss_cyclo_by_state", f"""
with w as (select max({WK}) wk from {N} where CURRENT_MMWR_YEAR=2026),
x as (select {AREA} st, CURRENT_MMWR_YEAR yr, max({YTD}) ytd
      from {N}, w where {WK}=w.wk and LABEL='Cyclosporiasis' and LOCATION1 is not null and LOCATION1<>'' group by 1,2),
s as (select st, max(iff(yr=2026,ytd,null)) y26, max(iff(yr=2025,ytd,null)) y25,
        greatest(coalesce(max(iff(yr=2022,ytd,null)),0),coalesce(max(iff(yr=2023,ytd,null)),0),
                 coalesce(max(iff(yr=2024,ytd,null)),0),coalesce(max(iff(yr=2025,ytd,null)),0)) prior_max
      from x group by 1)
select st, y26, y25, prior_max, round(y26/greatest(prior_max,1),1) ratio,
 sum(y26) over () us26, count_if(y26>0) over () states_any, count_if(y26>2*greatest(prior_max,1)) over () states_doubled,
 median(y26) over () median_state_26, median(prior_max) over () median_state_prior
from s qualify y26>=10 order by y26 desc"""),

("ms_hospitals_mortality", f"""
select STATE, FACILITY_NAME, CITY_TOWN, HOSPITAL_OWNERSHIP own, HOSPITAL_OVERALL_RATING star,
 COUNT_OF_FACILITY_MORT_MEASURES mort_n, COUNT_OF_MORT_MEASURES_WORSE mort_worse, COUNT_OF_MORT_MEASURES_BETTER mort_better,
 COUNT_OF_SAFETY_MEASURES_WORSE saf_worse, COUNT_OF_READM_MEASURES_WORSE readm_worse, COUNT_OF_READM_MEASURES_BETTER readm_better
from {HG} where STATE in ('MS','AR') and COUNT_OF_FACILITY_MORT_MEASURES>=7
order by STATE, mort_worse desc, mort_better"""),
]
