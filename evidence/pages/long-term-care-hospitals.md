---
title: Long Term Care Hospitals
---

```sql rows
select * from library.long_term_care_hospitals
```

```sql n
select count(*) as row_count from library.long_term_care_hospitals
```

```sql trend
select date_trunc('month', "CERTIFICATION_DATE") as period, count(*) as records
from library.long_term_care_hospitals
where "CERTIFICATION_DATE" is not null
group by 1
order by 1
```

Every long-term care hospital in America -- name, address, beds, owner.

Source: `THE_LIBRARY.HEALTH.LONG_TERM_CARE_HOSPITALS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Long Term Care Hospitals over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
