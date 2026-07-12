---
title: Italy Statistics
---

```sql rows
select * from library.italy_statistics
```

```sql n
select count(*) as row_count from library.italy_statistics
```

```sql trend
select date_trunc('month', "DATE") as period, count(*) as records
from library.italy_statistics
where "DATE" is not null
group by 1
order by 1
```

56,096 official Italian statistics -- economy, jobs, trade, population -- pulled from Istat's data feeds.

Source: `THE_LIBRARY.ECONOMY.ITALY_STATISTICS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Italy Statistics over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
