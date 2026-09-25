-- France: the no-twin archive events. Twin under ANY publisher (not just same org), owner for no-org rows, sample titles
with t as (select *, try_to_timestamp(ARCHIVED) arch_ts, lower(regexp_replace(trim(TITLE),'\s+',' ')) nt, coalesce(ORGANIZATION_NAME,'(no org)') org
  from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_FR_DATA_GOUV)
, live as (select nt, min(CREATED_AT) c, listagg(distinct org, '; ') within group (order by org) orgs from t where ARCHIVED='False' group by 1)
, a as (select t.*, l.c twin_created, l.orgs twin_orgs from t left join live l on l.nt=t.nt
        where (t.org='Région Hauts-de-France' and t.arch_ts>='2026-06-01' and t.arch_ts<'2026-07-01')
           or (t.org='Région GRAND EST' and t.arch_ts>='2026-08-01')
           or (t.org='(no org)' and t.arch_ts>='2025-01-01' and t.arch_ts<'2025-02-01')
           or (t.org like 'Communaut% du Saint-Quentinois' and t.arch_ts>='2024-06-01' and t.arch_ts<'2024-07-01'))
select org, count(*) n, count_if(twin_created is not null) twin_any, left(any_value(iff(twin_created is not null and twin_orgs<>org, twin_orgs, null)),120) other_org_twin,
  count(distinct OWNER) owners, left(listagg(distinct OWNER, '; '),200) owner_list, count_if(OWNER like 'deleted%') owner_deleted,
  count(distinct split_part(HARVEST_REMOTE_URL,'/',3)) harvest_hosts, left(listagg(distinct split_part(HARVEST_REMOTE_URL,'/',3), '; '),200) hosts,
  left(listagg(distinct left(TITLE,50), ' || ') within group (order by left(TITLE,50)),500) titles
from a group by 1
