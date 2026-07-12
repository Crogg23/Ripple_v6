---
title: Anxiety Depression Rates
---

```sql rows
select * from library.anxiety_depression_rates
```

```sql n
select count(*) as row_count from library.anxiety_depression_rates
```

```sql trend
select date_trunc('month', "TIME_PERIOD_START_DATE") as period, count(*) as records
from library.anxiety_depression_rates
where "TIME_PERIOD_START_DATE" is not null
group by 1
order by 1
```

CDC survey estimates of Americans reporting anxiety or depression, by state, group, and time.

Source: `THE_LIBRARY.HEALTH.ANXIETY_DEPRESSION_RATES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Anxiety Depression Rates over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
