---
title: Health Insurance Coverage
---

```sql rows
select * from library.health_insurance_coverage
```

```sql n
select count(*) as row_count from library.health_insurance_coverage
```

```sql trend
select date_trunc('month', "TIME_PERIOD_START_DATE") as period, count(*) as records
from library.health_insurance_coverage
where "TIME_PERIOD_START_DATE" is not null
group by 1
order by 1
```

CDC estimates of how many Americans have health insurance, by state and demographic group over time.

Source: `THE_LIBRARY.HEALTH.HEALTH_INSURANCE_COVERAGE` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Health Insurance Coverage over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
