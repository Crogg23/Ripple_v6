P = "LIBRARY_MARTS.HEALTH."
QUERIES = [
("pos_profile_by_category", f"""
select PRVDR_CTGRY_CD, count(*) n, count(distinct CCN) ccns, count_if(PGM_TRMNTN_CD='00') active,
 count_if(CHOW_CNT>0) chow_any, max(CHOW_CNT) chow_max, count_if(CHOW_DT is not null) chow_dt_filled,
 count_if(CHOW_DT>='2021-01-01') chow_since21, max(CHOW_DT) chow_max_dt,
 min(ORGNL_PRTCPTN_DT) first_join, max(ORGNL_PRTCPTN_DT) last_join, count_if(SKLTN_REC_SW='Y') skeleton,
 count_if(MLT_FAC_ORG_NAME is not null and MLT_FAC_ORG_NAME<>'') has_org_name
from {P}HEALTH__FED_CMS_POS_OTHER group by 1 order by 2 desc"""),

("pos_hosp_chow_by_year", f"""
select year(CHOW_DT) yr, count(*) n, count_if(PGM_TRMNTN_CD='00') still_active,
 count_if(PRVDR_CTGRY_SBTYP_CD='01') short_term, count_if(PRVDR_CTGRY_SBTYP_CD='11') cah,
 count_if(GNRL_CNTL_TYPE_CD in ('04','05','06')) ctl_04_06
from {P}HEALTH__FED_CMS_POS_OTHER where PRVDR_CTGRY_CD='01' and CHOW_DT>='2010-01-01'
group by 1 order by 1"""),

("hg_profile_by_type_owner", f"""
select HOSPITAL_TYPE, HOSPITAL_OWNERSHIP, count(*) n, count(HOSPITAL_OVERALL_RATING) rated,
 round(avg(HOSPITAL_OVERALL_RATING),2) avg_star, count_if(HOSPITAL_OVERALL_RATING=1) one_star,
 count_if(HOSPITAL_OVERALL_RATING=5) five_star,
 count(distinct MORT_GROUP_MEASURE_COUNT) d_mort, count(distinct SAFETY_GROUP_MEASURE_COUNT) d_saf,
 count(distinct READM_GROUP_MEASURE_COUNT) d_readm, count(distinct PT_EXP_GROUP_MEASURE_COUNT) d_ptexp
from {P}HEALTH__FED_CMS_HOSPITAL_GENERAL group by 1,2 order by 3 desc"""),

("hg_to_pos_land_rate", f"""
with p as (select CCN, max(CHOW_CNT) chow_cnt, max(CHOW_DT) chow_dt, max(PGM_TRMNTN_CD) trm, count(*) k
           from {P}HEALTH__FED_CMS_POS_OTHER group by 1)
select h.HOSPITAL_TYPE, count(*) hospitals, count(p.CCN) landed, count_if(p.k>1) dup_pos,
 count_if(p.trm='00') landed_active, count_if(p.chow_cnt>0) chow_any, count_if(p.chow_dt>='2021-01-01') chow_since21,
 count_if(p.chow_dt>='2021-01-01' and h.HOSPITAL_OVERALL_RATING is not null) chow21_rated
from {P}HEALTH__FED_CMS_HOSPITAL_GENERAL h left join p on p.CCN=h.CCN
group by 1 order by 2 desc"""),

("dmf_by_year_type", f"""
select year(SUBMIT_DATE) yr, count(*) n, count_if(DMF_TYPE='II') t2, count_if(DMF_TYPE='III') t3,
 count_if(DMF_TYPE='IV') t4, count_if(DMF_TYPE='V') t5, count_if(STATUS_CODE='A') active,
 count(distinct HOLDER) holders
from {P}HEALTH__FED_FDA_DRUG_MASTER_FILES where SUBMIT_DATE>='1995-01-01' or SUBMIT_DATE<'1960-01-01'
group by 1 order by 1"""),

("dmf_subject_surge", f"""
with s as (select regexp_substr(upper(SUBJECT),'[A-Z]{{4,}}') w, year(SUBMIT_DATE) yr, HOLDER
           from {P}HEALTH__FED_FDA_DRUG_MASTER_FILES where DMF_TYPE='II')
select w, count_if(yr between 2019 and 2022) f19_22, count_if(yr between 2023 and 2026) f23_26,
 count(distinct iff(yr between 2023 and 2026, HOLDER, null)) holders23_26, count(*) all_time
from s where w is not null group by 1
having count_if(yr between 2023 and 2026)>=12
order by f23_26 - f19_22 desc limit 30"""),

("nndss_integrity_by_year", f"""
select CURRENT_MMWR_YEAR yr, count(*) n,
 count(distinct REPORTING_AREA||'|'||LABEL||'|'||MMWR_WEEK) keys,
 count(distinct REPORTING_AREA) areas, count(distinct LABEL) labels,
 min(try_to_number(MMWR_WEEK)) wk_min, max(try_to_number(MMWR_WEEK)) wk_max,
 count(distinct _SOURCE_RUN_ID) runs,
 count_if(LOCATION1 is not null and LOCATION1<>'') single_place_rows
from {P}HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1 order by 1"""),

("nndss_flags", f"""
select CURRENT_WEEK_FLAG, CUMULATIVE_YTD_CURRENT_MMWR_YEAR_FLAG ytd_flag, count(*) n,
 count_if(CURRENT_WEEK is not null and CURRENT_WEEK<>'') wk_filled,
 count_if(CUMULATIVE_YTD_CURRENT_MMWR_YEAR is not null and CUMULATIVE_YTD_CURRENT_MMWR_YEAR<>'') ytd_filled,
 max(try_to_number(CUMULATIVE_YTD_CURRENT_MMWR_YEAR)) ytd_max
from {P}HEALTH__FED_CDC_NNDSS_WEEKLY_2024 group by 1,2 order by 3 desc limit 20"""),

("ihs_lookup_check", f"""
select STATUS, ITU_CODE, count(*) n, count(distinct ASUFAC_CODE) codes, count(distinct FACILITY_NAME) names,
 count_if(BED_COUNT>0) with_beds, sum(BED_COUNT) beds, count(distinct FACILITY_TYPE) types,
 count(distinct AREA) areas, count(distinct APC_FLAG) apc_vals
from {P}HEALTH__FED_IHS_SCB_FACILITY group by 1,2 order by 3 desc"""),
]
