---
title: Calendar Dates
---

```sql rows
select * from library.calendar_dates
```

```sql n
select count(*) as row_count from library.calendar_dates
```

```sql trend
select date_trunc('month', "DATE_DAY") as period, count(*) as records
from library.calendar_dates
where "DATE_DAY" is not null
group by 1
order by 1
```

One row per calendar day (31,411 days) with year, quarter, month, weekday, and fiscal year.

Source: `THE_LIBRARY.GEOGRAPHY.CALENDAR_DATES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Calendar Dates over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
