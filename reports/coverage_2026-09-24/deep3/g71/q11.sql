-- Greece: creation by day (the migration-date test), top 12 days with orgs and top org
with d as (select DATE_CREATED::date d, ORGANISATION_NAME o, count(*) n from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_GR_DATAGOV group by 1,2)
, r as (select *, row_number() over (partition by d order by n desc) rk from d)
select d, sum(n) n, count(*) orgs, max(iff(rk=1, o||' '||n, null)) top_org from r group by 1 order by n desc limit 12
