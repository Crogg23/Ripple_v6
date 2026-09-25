-- @landing_countryba_blank_2026q1
select count(*) n, count_if(countryba is null or trim(countryba::string) = '') ba_blank,
  count_if((countryba is null or trim(countryba::string) = '') and cityba = 'VANCOUVER') ba_blank_vancouver,
  count_if(countryma is null or trim(countryma::string) = '') ma_blank
from LIBRARY_RAW.LANDING.FED_SEC_DERA_SUB_2026Q1
