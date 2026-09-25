-- DOT_BTS: confirm it is a 21-row catalog; are the data columns all empty; list names
select count(*) n, count(distinct DATABASE_NAME) names,
  count_if(nullif(trim(MODE::varchar),'') is not null) mode_filled, count_if(nullif(trim(SUBJECT::varchar),'') is not null) subj_filled,
  count_if(nullif(trim(YEAR::varchar),'') is not null) year_filled, count_if(nullif(trim(CARRIER_CODE::varchar),'') is not null) carrier_filled,
  count_if(nullif(trim(ORIGIN::varchar),'') is not null) origin_filled, count_if(nullif(trim(STATE_FIPS::varchar),'') is not null) fips_filled,
  listagg(DATABASE_NAME, ' | ') within group (order by DATABASE_NAME) names_list
from LIBRARY_MARTS.TRANSPORT.TRANSPORT__FED_DOT_BTS;
