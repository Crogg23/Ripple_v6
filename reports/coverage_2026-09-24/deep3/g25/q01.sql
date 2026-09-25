-- FHLB membership: profile by member type: rows, certs, dates, stand-in dates, blank IDs, first/last member date
select MEM_TYPE, count(*) n, count(distinct FHFA_ID) fhfa_ids, count(distinct nullif(trim(CERT),'')) certs,
  count_if(nullif(trim(CERT),'') is null) cert_blank, count_if(nullif(trim(NAIC_ID),'') is not null) naic,
  count_if(nullif(trim(NCUA_ID),'') is not null) ncua, count_if(APPR_DATE is null) appr_null,
  count_if(MEM_DATE = '1989-12-31') mem_19891231, count_if(MEM_DATE is null) mem_null,
  min(MEM_DATE) mem_min, max(MEM_DATE) mem_max,
  count_if(year(MEM_DATE) between 2000 and 2007) m00_07, count_if(year(MEM_DATE) between 2008 and 2015) m08_15,
  count_if(year(MEM_DATE) between 2016 and 2019) m16_19, count_if(year(MEM_DATE) >= 2020) m20on,
  count(distinct _SOURCE_RUN_ID) runs, max(_LOADED_AT) loaded
from LIBRARY_MARTS.FINANCE.FINANCE__FED_FHFA_FHLB_MEMBERSHIP
group by rollup(MEM_TYPE) order by n desc
