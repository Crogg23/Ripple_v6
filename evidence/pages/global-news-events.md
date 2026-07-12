---
title: Global News Events
---

```sql rows
select * from library.global_news_events
```

```sql n
select count(*) as row_count from library.global_news_events
```

```sql trend
select date_trunc('month', "SQLDATE") as period, count(*) as records
from library.global_news_events
where "SQLDATE" is not null
group by 1
order by 1
```

GDELT global news event records -- who did what to whom, where, per 15-minute news scan (1,015-row probe).

Source: `THE_LIBRARY.GEOGRAPHY.GLOBAL_NEWS_EVENTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Global News Events over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
