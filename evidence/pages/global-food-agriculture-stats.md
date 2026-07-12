---
title: Global Food Agriculture Stats
---

```sql rows
select * from library.global_food_agriculture_stats
```

```sql n
select count(*) as row_count from library.global_food_agriculture_stats
```

```sql trend
select date_trunc('month', "DATEUPDATE") as period, count(*) as records
from library.global_food_agriculture_stats
where "DATEUPDATE" is not null
group by 1
order by 1
```

FAOSTAT food and agriculture statistics (4-row stub -- raw content only, dead probe).

Source: `THE_LIBRARY.ECONOMY.GLOBAL_FOOD_AGRICULTURE_STATS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Global Food Agriculture Stats over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
