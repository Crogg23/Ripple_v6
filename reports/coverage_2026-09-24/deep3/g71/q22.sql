-- Argentina: the two row types. Rows with no org vs with org; exact-duplicate rows; top orgs by distinct datasets and files
with t as (select *, iff(C_ORGANIZATION is null or trim(C_ORGANIZATION)='', 'no_org', 'org') kind from LIBRARY_MARTS.OPEN_DATA.OPEN_DATA__INTL_AR_DATOSGOB)
select 'kind' k, kind a, count(*)::text b, count(distinct DATASET_ID)::text c, count(distinct RESOURCE_URL)::text d, left(any_value(DATASET_TITLE),60) e,
  left(any_value(RESOURCE_URL),90) f, count(distinct PROVINCIA_ID)::text g
from t group by 2
union all
select 'dups', null, count(*)::text, count(distinct DATASET_ID||'|'||RESOURCE_URL||'|'||coalesce(FORMAT,''))::text, null, null, null, null from t
union all
select 'org', trim(C_ORGANIZATION), count(*)::text, count(distinct DATASET_ID)::text, count(distinct RESOURCE_URL)::text, left(any_value(DATASET_TITLE),60),
  max(LAST_MODIFIED), min(LAST_MODIFIED) from t where kind='org' group by 2 having count(*)>=100
