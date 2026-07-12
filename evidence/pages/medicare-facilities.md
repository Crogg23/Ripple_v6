---
title: Medicare Facilities
---

```sql rows
select * from library.medicare_facilities
```

```sql n
select count(*) as row_count from library.medicare_facilities
```

```sql trend
select date_trunc('month', "CHOW_DT") as period, count(*) as records
from library.medicare_facilities
where "CHOW_DT" is not null
group by 1
order by 1
```

Master file of every Medicare-certified facility -- beds, staff, services.

Source: `THE_LIBRARY.HEALTH.MEDICARE_FACILITIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Medicare Facilities over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
