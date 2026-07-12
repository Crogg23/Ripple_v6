---
title: Clinical Trials
---

```sql rows
select * from library.clinical_trials
```

```sql n
select count(*) as row_count from library.clinical_trials
```

```sql trend
select date_trunc('month', "FIRST_POSTED_DATE") as period, count(*) as records
from library.clinical_trials
where "FIRST_POSTED_DATE" is not null
group by 1
order by 1
```

Registered clinical studies -- who sponsors them, the drug/condition, phase, and whether results were posted.

Source: `THE_LIBRARY.HEALTH.CLINICAL_TRIALS` (sample).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Clinical Trials over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
