-- GLEIF join prep: do the OpenSanctions tables carry LEIs? Count LEI-shaped tokens and sample the IDENTIFIERS text
with a as (
  select 'OPENSANCTIONS' src, SCHEMA typ, DATASET ds, (SANCTIONS is not null and SANCTIONS::text not in ('','[]')) has_sanc, IDENTIFIERS::text ids
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS
  union all
  select 'DEFAULT', ENTITY_TYPE, DATASETS::text, (SANCTIONS is not null and SANCTIONS::text not in ('','[]')), IDENTIFIERS::text
  from LIBRARY_MARTS.JUSTICE.JUSTICE__INTL_OPENSANCTIONS_DEFAULT
)
select src, typ, has_sanc, count(*) n, count_if(regexp_like(ids, '.*[A-Z0-9]{18}[0-9]{2}.*', 's')) lei_shaped,
  any_value(iff(regexp_like(ids, '.*[A-Z0-9]{18}[0-9]{2}.*', 's'), left(ids, 300), null)) sample_ids,
  any_value(left(ds, 200)) sample_ds
from a group by 1,2,3 order by 1, n desc
