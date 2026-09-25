-- HHA enrollments: profile of keys, flags, sentinel dates, ownership
select count(*) n, count(distinct ENROLLMENT_ID) enr, count(distinct CCN) ccn, count(distinct NPI) npi, count(distinct ASSOCIATE_ID) assoc,
  count_if(CCN is null or trim(CCN)='') ccn_blank, count_if(NPI is null or trim(NPI)='') npi_blank,
  count_if(MULTIPLE_NPI_FLAG='Y') multi_y, count_if(MULTIPLE_NPI_FLAG='N') multi_n,
  count_if(PROPRIETARY_NONPROFIT='P') forprofit, count_if(PROPRIETARY_NONPROFIT='N') nonprofit,
  count_if(INCORPORATION_DATE is null) inc_null, count_if(year(INCORPORATION_DATE)<1900) inc_pre1900,
  count_if(year(INCORPORATION_DATE)>=2019) inc_2019on,
  listagg(distinct PRACTICE_LOCATION_TYPE, '|') plt_vals, count(distinct ENROLLMENT_STATE) states,
  count(distinct upper(trim(ADDRESS_LINE_1))||'|'||left(ZIP_CODE,5)) addrs
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS
