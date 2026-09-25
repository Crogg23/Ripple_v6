-- Spain datos.gob.es: fill rate of every column, distincts, date span (Spanish text dates, year = last 4 chars)
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_ES_DATOSGOB)
select count(*) n,
  count_if(nullif(trim(URI),'') is not null) uri_filled, count_if(nullif(trim(TITLE),'') is not null) title_filled,
  count_if(nullif(trim(DESCRIPTION),'') is not null) desc_filled, count_if(nullif(trim(PUBLISHER),'') is not null) pub_filled,
  count_if(nullif(trim(SECTOR),'') is not null) sector_filled, count_if(nullif(trim(GEOGRAPHIC_COVERAGE),'') is not null) geo_filled,
  count_if(nullif(trim(DISTRIBUTION_URL),'') is not null) dist_filled, count_if(nullif(trim(FORMAT),'') is not null) fmt_filled,
  count_if(nullif(trim(LICENSE),'') is not null) lic_filled, count_if(nullif(trim(ISSUED),'') is not null) issued_filled,
  count_if(nullif(trim(MODIFIED),'') is not null) mod_filled,
  count(distinct PUBLISHER) pubs, count(distinct SECTOR) sectors, count(distinct DISTRIBUTION_URL) dist_urls,
  count(distinct FORMAT) fmts, count(distinct LICENSE) lics,
  min(try_to_number(right(trim(ISSUED),4))) issued_min_yr, max(try_to_number(right(trim(ISSUED),4))) issued_max_yr,
  min(try_to_number(right(trim(MODIFIED),4))) mod_min_yr, max(try_to_number(right(trim(MODIFIED),4))) mod_max_yr,
  count(distinct _SOURCE_URL) src_urls, any_value(_SOURCE_URL) src, min(_LOADED_AT)::text loaded_min, max(_LOADED_AT)::text loaded_max,
  any_value(ISSUED) issued_eg, any_value(FORMAT) fmt_eg, any_value(DISTRIBUTION_URL) dist_eg
from t;
