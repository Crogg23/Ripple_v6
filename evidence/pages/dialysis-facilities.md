---
title: Dialysis Facilities
---

```sql rows
select * from library.dialysis_facilities
```

```sql n
select count(*) as row_count from library.dialysis_facilities
```

```sql trend
select date_trunc('month', "CERTIFICATION_DATE") as period, count(*) as records
from library.dialysis_facilities
where "CERTIFICATION_DATE" is not null
group by 1
order by 1
```

Every Medicare dialysis center in the U.S. with quality, mortality, and infection stats.

Source: `THE_LIBRARY.HEALTH.DIALYSIS_FACILITIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Dialysis Facilities over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
