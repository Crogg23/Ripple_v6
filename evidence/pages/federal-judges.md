---
title: Federal Judges
---

```sql rows
select * from library.federal_judges
```

```sql n
select count(*) as row_count from library.federal_judges
```

```sql trend
select date_trunc('month', "RECESS_APPOINTMENT_DATE_1") as period, count(*) as records
from library.federal_judges
where "RECESS_APPOINTMENT_DATE_1" is not null
group by 1
order by 1
```

Every Article III federal judge since 1789 -- who appointed them, when, and their record.

Source: `THE_LIBRARY.GOVERNMENT.FEDERAL_JUDGES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Federal Judges over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
