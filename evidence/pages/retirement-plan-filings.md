---
title: Retirement Plan Filings
---

```sql rows
select * from library.retirement_plan_filings
```

```sql n
select count(*) as row_count from library.retirement_plan_filings
```

```sql trend
select date_trunc('month', "DATE_RECEIVED") as period, count(*) as records
from library.retirement_plan_filings
where "DATE_RECEIVED" is not null
group by 1
order by 1
```

Form 5500 filings for 33K employer retirement and benefit plans -- sponsor, EIN, participants, and plan type.

Source: `THE_LIBRARY.ECONOMY.RETIREMENT_PLAN_FILINGS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Retirement Plan Filings over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
