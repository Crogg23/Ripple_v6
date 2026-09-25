-- Canada: organization x year created, and subject lists
with t as (select * from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_CA_OPEN_CANADA)
select * from (select 'org_year' k, left(C_ORGANIZATION,60) a, year(METADATA_CREATED)::text b, count(*) n,
   min(METADATA_MODIFIED)::text c, max(METADATA_MODIFIED)::text d from t group by 2,3 order by 2,3)
union all select * from (select 'subject', SUBJECT, null, count(*), null, null from t group by 2 order by 4 desc limit 8)
union all select * from (select 'mod_month', to_char(METADATA_MODIFIED,'YYYY-MM'), null, count(*), null, null from t group by 2 order by 4 desc limit 10);
