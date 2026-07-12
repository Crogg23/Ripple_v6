---
title: Congressional Bills
---

```sql rows
select * from library.congressional_bills
```

```sql n
select count(*) as row_count from library.congressional_bills
```

```sql trend
select date_trunc('month', "INTRODUCED_DATE") as period, count(*) as records
from library.congressional_bills
where "INTRODUCED_DATE" is not null
group by 1
order by 1
```

Every bill in Congress -- sponsor, cosponsors, action history, and if it became law.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESSIONAL_BILLS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Congressional Bills over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
