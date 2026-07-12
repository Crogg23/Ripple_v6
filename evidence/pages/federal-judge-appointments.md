---
title: Federal Judge Appointments
---

```sql rows
select * from library.federal_judge_appointments
```

```sql n
select count(*) as row_count from library.federal_judge_appointments
```

```sql trend
select date_trunc('month', "RECESS_APPOINTMENT_DATE") as period, count(*) as records
from library.federal_judge_appointments
where "RECESS_APPOINTMENT_DATE" is not null
group by 1
order by 1
```

Every US federal judge's appointment -- who nominated them, the Senate vote, and when they left.

Source: `THE_LIBRARY.GOVERNMENT.FEDERAL_JUDGE_APPOINTMENTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Federal Judge Appointments over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
