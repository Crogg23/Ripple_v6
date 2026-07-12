---
title: Nursing Homes
---

```sql rows
select * from library.nursing_homes
```

```sql n
select count(*) as row_count from library.nursing_homes
```

```sql trend
select date_trunc('month', "DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES") as period, count(*) as records
from library.nursing_homes
where "DATE_FIRST_APPROVED_TO_PROVIDE_MEDICARE_AND_MEDICAID_SERVICES" is not null
group by 1
order by 1
```

Every Medicare/Medicaid nursing home: star ratings, staffing, inspections, fines, and abuse flags.

Source: `THE_LIBRARY.HEALTH.NURSING_HOMES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Nursing Homes over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
