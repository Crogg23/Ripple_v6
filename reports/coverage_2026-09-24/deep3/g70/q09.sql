-- Swiss sample: is the 5,000 an alphabetical or created-date slice? name range, created by month in 2023, newest created rows, top orgs
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CH_OPENDATASWISS)
select 'name_range' k, min(NAME) a, max(NAME) b, min(ID) c, max(ID) d from t
union all select 'created_2023_by_month', to_char(METADATA_CREATED, 'YYYY-MM'), count(*)::text, null, null from t where METADATA_CREATED >= '2023-01-01' group by 2
union all select * from (select 'newest_created', METADATA_CREATED::text, NAME, C_ORGANIZATION, METADATA_MODIFIED::text from t order by METADATA_CREATED desc limit 5)
union all select * from (select 'org', C_ORGANIZATION, count(*)::text, min(METADATA_CREATED)::text, max(METADATA_CREATED)::text from t group by 2 order by count(*) desc limit 8)
