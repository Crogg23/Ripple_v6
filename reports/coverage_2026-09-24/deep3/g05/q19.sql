-- CDC portal: datasets whose own description says they update weekly/monthly, and how many have not had new data in 6 or 12 months before the 2026-08-11 pull; last-data-update month since mid-2024; top stale 'weekly' non-COVID datasets
with t as (select *, case when DESCRIPTION ilike '%updated weekly%' or DESCRIPTION ilike '%weekly basis%' or DESCRIPTION ilike '%updated each week%' or DESCRIPTION ilike '%updated every week%' then 'weekly'
                         when DESCRIPTION ilike '%updated monthly%' or DESCRIPTION ilike '%monthly basis%' or DESCRIPTION ilike '%updated each month%' then 'monthly' else 'other' end freq,
                    (DATASET_NAME ilike '%covid%' or DESCRIPTION ilike '%covid%' or DATASET_NAME ilike '%sars-cov%') covid
           from LIBRARY_MARTS.HEALTH.HEALTH__FED_CDC_DATA_PORTAL where RESOURCE_TYPE='dataset')
select 'freq' k, freq a, covid::text b, count(*) n, count_if(DATA_UPDATED_AT < '2026-02-11') stale6m, count_if(DATA_UPDATED_AT < '2025-08-11') stale12m, sum(DOWNLOAD_COUNT) dl, null c
from t group by 2,3
union all select 'lastdata_month', to_char(DATA_UPDATED_AT,'YYYY-MM'), null, count(*), count_if(freq='weekly'), count_if(covid), sum(DOWNLOAD_COUNT), null from t where DATA_UPDATED_AT >= '2024-07-01' group by 2
union all select * from (select 'stale_weekly', left(DATASET_NAME,60), DOMAIN_CATEGORY, DOWNLOAD_COUNT, null, null, null, to_char(DATA_UPDATED_AT,'YYYY-MM-DD')||' created '||to_char(CREATED_AT,'YYYY-MM-DD')
  from t where freq='weekly' and not covid and DATA_UPDATED_AT < '2026-02-11' order by DOWNLOAD_COUNT desc limit 15)
order by 1, 2
