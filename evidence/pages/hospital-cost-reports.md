---
title: Hospital Cost Reports
---

```sql rows
select * from library.hospital_cost_reports
```

```sql n
select count(*) as row_count from library.hospital_cost_reports
```

```sql trend
select date_trunc('month', "FISCAL_YEAR_END_DATE") as period, count(*) as records
from library.hospital_cost_reports
where "FISCAL_YEAR_END_DATE" is not null
group by 1
order by 1
```

Annual financial reports every Medicare hospital files: revenue, costs, beds, charity care, margins.

Source: `THE_LIBRARY.HEALTH.HOSPITAL_COST_REPORTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Hospital Cost Reports over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
