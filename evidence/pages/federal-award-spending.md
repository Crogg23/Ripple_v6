---
title: Federal Award Spending
---

```sql rows
select * from library.federal_award_spending
```

```sql n
select count(*) as row_count from library.federal_award_spending
```

```sql trend
select date_trunc('month', "START_DATE") as period, count(*) as records
from library.federal_award_spending
where "START_DATE" is not null
group by 1
order by 1
```

Federal awards from the USAspending API -- contracts, grants, loans -- with recipient, agency, and dollars (300-row probe).

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.FEDERAL_AWARD_SPENDING` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Federal Award Spending over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
