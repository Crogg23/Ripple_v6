---
title: France Open Data Catalog
---

```sql rows
select * from library.france_open_data_catalog
```

```sql n
select count(*) as row_count from library.france_open_data_catalog
```

```sql trend
select date_trunc('month', "LAST_UPDATE") as period, count(*) as records
from library.france_open_data_catalog
where "LAST_UPDATE" is not null
group by 1
order by 1
```

Catalog of 2,765 datasets on France's national open-data portal -- title, publisher, license, freshness.

Source: `THE_LIBRARY.OPEN_DATA.FRANCE_OPEN_DATA_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="France Open Data Catalog over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
