with a as (
 select lpad(trim(EIN::string),9,'0') ein, ORG_NAME, upper(CONTRIBUTOR_NAME) cn, CONTRIBUTOR_STATE st, CONTRIBUTOR_CITY city, CONTRIBUTION_DATE d, CONTRIBUTION_AMOUNT amt, AGG_CONTRIBUTION_YTD ytd, FORM_ID_NUMBER fid, SOURCE_ID
 from LIBRARY_MARTS.FINANCE.FINANCE__FED_IRS527_SCHEDULE_A_CONTRIBUTIONS
 where ((upper(CONTRIBUTOR_NAME) like '%ADELSON%' and (CONTRIBUTOR_STATE = 'NV' or upper(CONTRIBUTOR_CITY) like '%LAS VEGAS%'))
    or upper(CONTRIBUTOR_NAME) like '%LAS VEGAS SANDS%' or upper(CONTRIBUTOR_NAME) like '%VENETIAN%CASINO%' or upper(CONTRIBUTOR_NAME) like 'SANDS %')
   and year(CONTRIBUTION_DATE) between 2021 and 2026 and upper(ORG_NAME) like '%GOVERNORS%')
select ein, left(ORG_NAME,40) org, cn, d, amt, ytd, count(*) raw_rows, count(distinct fid) forms, listagg(distinct fid::string, ',') fids,
 count(*) over (partition by d, amt) same_date_amt_rows_across_names
from a group by 1,2,3,4,5,6 order by d, amt desc
