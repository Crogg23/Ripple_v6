---
title: Outside Spending
---

```sql rows
select * from library.outside_spending
```

```sql n
select count(*) as row_count from library.outside_spending
```

```sql trend
select date_trunc('month', "EXP_DATE") as period, count(*) as records
from library.outside_spending
where "EXP_DATE" is not null
group by 1
order by 1
```

Money spent FOR or AGAINST candidates by outside groups -- who, how much, which side.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.OUTSIDE_SPENDING` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Outside Spending over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
