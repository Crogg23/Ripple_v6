P = "LIBRARY_MARTS.HEALTH."
POS = P + "HEALTH__FED_CMS_POS_OTHER"
QUERIES = [
("pos_chow_churn_by_exit_type", f"""
select case when PGM_TRMNTN_CD='00' then 'a active'
            when PGM_TRMNTN_CD in ('05','06') and TRMNTN_EXPRTN_DT>='2015-01-01' then 'b ended 05/06 since 2015'
            when PGM_TRMNTN_CD='01' and TRMNTN_EXPRTN_DT>='2015-01-01' then 'c ended 01 since 2015'
            else 'd other ended' end grp,
 count(*) n, count_if(CHOW_CNT>=3) chow3, round(count_if(CHOW_CNT>=3)/count(*),3) share_chow3,
 count_if(CHOW_CNT>=1) chow1, round(count_if(CHOW_CNT>=1)/count(*),3) share_chow1, median(CHOW_CNT) med_chow,
 count_if(CHOW_DT>=dateadd(year,-3,TRMNTN_EXPRTN_DT)) chow_within_3y_of_end,
 median(year(ORGNL_PRTCPTN_DT)) med_join_year,
 count_if(CHOW_CNT>=3 and year(ORGNL_PRTCPTN_DT)=1966) chow3_joined_1966, count_if(year(ORGNL_PRTCPTN_DT)=1966) joined_1966
from {POS} where PRVDR_CTGRY_CD='01' and PRVDR_CTGRY_SBTYP_CD='01'
group by 1 order by 1"""),
]
