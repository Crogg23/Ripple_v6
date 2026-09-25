-- (rerun of q16 after a compile error) Sample-order test for the three capped tables: how was the slice chosen? Load date, modified-date spread, name order
select 'DE' t, to_timestamp(max(_LOADED_AT)/1000000)::date loaded, min(NAME) name_min, max(NAME) name_max,
  min(METADATA_MODIFIED)::date m_min, (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA order by METADATA_MODIFIED limit 1 offset 2500) m_median,
  max(METADATA_MODIFIED)::date m_max, count_if(year(METADATA_MODIFIED)=2025) m_2025, count_if(year(METADATA_CREATED)=2025) c_2025, count(distinct PUBLISHER) pubs
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_DE_GOVDATA
union all
select 'CL', to_timestamp(max(_LOADED_AT)/1000000)::date, min(NAME), max(NAME), min(METADATA_MODIFIED)::date,
  (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB order by METADATA_MODIFIED limit 1 offset 500),
  max(METADATA_MODIFIED)::date, count_if(year(METADATA_MODIFIED)=2026), count_if(year(METADATA_CREATED)=2026), count(distinct PUBLISHER_INSTITUTION)
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CL_DATOSGOB
union all
select 'GR', to_timestamp(max(_LOADED_AT)/1000000)::date, min(TITLE), max(TITLE), min(METADATA_MODIFIED)::date,
  (select METADATA_MODIFIED::date from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV order by METADATA_MODIFIED limit 1 offset 2494),
  max(METADATA_MODIFIED)::date, count_if(year(METADATA_MODIFIED)=2026), count_if(year(DATE_CREATED)=2026), count(distinct ORGANISATION_NAME)
from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV
