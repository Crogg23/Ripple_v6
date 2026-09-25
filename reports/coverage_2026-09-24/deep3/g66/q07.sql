-- Google advertiser stats: what PUBLIC_IDS_LIST holds (FEC ID, EIN, other), by region, with USD spend
with a as (select ADVERTISER_ID, ADVERTISER_NAME, REGIONS, PUBLIC_IDS_LIST p, try_to_number(SPEND_USD) usd
           from LIBRARY_MARTS.EDUCATION.EDUCATION__FED_GOOGLE_POLADS_ADVERTISER_STATS)
select 'summary' k, count(*)::text n, count(distinct ADVERTISER_ID)::text ids,
  count_if(REGIONS like '%US%')::text us_rows,
  count_if(REGIONS like '%US%' and regexp_like(p, '.*C[0-9]{8}.*'))::text us_fec,
  count_if(REGIONS like '%US%' and not regexp_like(coalesce(p,''), '.*C[0-9]{8}.*') and regexp_like(p, '.*[0-9]{2}-?[0-9]{7}.*'))::text us_ein_only,
  count_if(REGIONS like '%US%' and (p is null or trim(p)=''))::text us_blank,
  sum(case when REGIONS like '%US%' then usd end)::text us_usd
from a
union all
select * from (select 'sample', ADVERTISER_NAME, REGIONS, left(p,120), usd::text, ADVERTISER_ID, null, null from a where REGIONS like '%US%' order by usd desc nulls last limit 25)
