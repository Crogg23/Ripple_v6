-- CDC data portal: created per year, last data update per year, resource types, categories
with t as (select * from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DATA_PORTAL)
select 'ids' k, 'rows/ids/pv_nonnull' a, count(*) n, count(distinct DATASET_ID) m, count(PAGE_VIEWS) x from t
union all select 'created', year(CREATED_AT)::text, count(*), count_if(RESOURCE_TYPE='dataset'), sum(DOWNLOAD_COUNT) from t group by 2
union all select 'data_upd', year(DATA_UPDATED_AT)::text, count(*), count_if(RESOURCE_TYPE='dataset'), sum(DOWNLOAD_COUNT) from t group by 2
union all select 'rtype', RESOURCE_TYPE, count(*), count(distinct DATASET_ID), sum(DOWNLOAD_COUNT) from t group by 2
union all select 'cat', DOMAIN_CATEGORY, count(*), count_if(RESOURCE_TYPE='dataset'), sum(DOWNLOAD_COUNT) from t group by 2
order by 1, 2
