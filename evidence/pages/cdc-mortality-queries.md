---
title: Cdc Mortality Queries
---

```sql rows
select * from library.cdc_mortality_queries
```

```sql n
select count(*) as row_count from library.cdc_mortality_queries
```

CDC WONDER mortality/health query results (1-row stub -- needs a real pour).

Source: `THE_LIBRARY.HEALTH.CDC_MORTALITY_QUERIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
