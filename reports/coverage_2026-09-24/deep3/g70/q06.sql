-- Swiss catalog sample: ids, constants, sort order of the 5,000 (modified year), old ISSUED dates, issued-by-year, language, load stamps
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CH_OPENDATASWISS)
select 'profile' k, count(*)::text a, count(distinct ID)::text b, count(distinct NAME)::text c, min(METADATA_MODIFIED)::text d, max(METADATA_MODIFIED)::text e, min(METADATA_CREATED)::text f, max(METADATA_CREATED)::text g from t
union all select 'private_type', PRIVATE::text, TYPE, count(*)::text, null, null, null, null from t group by 2, 3
union all select 'mod_year', year(METADATA_MODIFIED)::text, count(*)::text, null, null, null, null, null from t group by 2
union all select 'created_year', year(METADATA_CREATED)::text, count(*)::text, null, null, null, null, null from t group by 2
union all select * from (select 'issued_old', ISSUED::text, NAME, C_ORGANIZATION, left(TITLE, 120), null, null, null from t where ISSUED < '1950-01-01' order by ISSUED limit 8)
union all select 'issued_null', count_if(ISSUED is null)::text, count_if(ISSUED < '1950-01-01')::text, count_if(ISSUED > '2026-09-24')::text, null, null, null, null from t
union all select * from (select 'lang', LANGUAGE, count(*)::text, null, null, null, null, null from t group by 2 order by count(*) desc limit 8)
union all select 'load', _LOADED_AT::text, _SOURCE_URL, count(*)::text, null, null, null, null from t group by 2, 3
