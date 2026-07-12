---
title: Federal Judge Appointments
---

```sql rows
select * from library.federal_judge_appointments_federal_judge_appointments
```

```sql n
select count(*) as row_count from library.federal_judge_appointments_federal_judge_appointments
```

```sql trend
select date_trunc('month', "CONFIRMATION_DT") as period, count(*) as records
from library.federal_judge_appointments_federal_judge_appointments
where "CONFIRMATION_DT" is not null
group by 1
order by 1
```

Every federal judge appointment: who, which court, which president, and the confirmation vote.

Source: `THE_LIBRARY.JUSTICE.FEDERAL_JUDGE_APPOINTMENTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Federal Judge Appointments over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
