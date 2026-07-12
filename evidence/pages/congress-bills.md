---
title: Congress Bills
---

```sql rows
select * from library.congress_bills
```

```sql n
select count(*) as row_count from library.congress_bills
```

```sql trend
select date_trunc('month', "INTRODUCED_DATE") as period, count(*) as records
from library.congress_bills
where "INTRODUCED_DATE" is not null
group by 1
order by 1
```

Every bill introduced in Congress: sponsor, subject, how far it got, and whether it became law.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_BILLS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Congress Bills over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
