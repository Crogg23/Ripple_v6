---
title: Failed Banks
---

```sql rows
select * from library.failed_banks
```

```sql n
select count(*) as row_count from library.failed_banks
```

```sql trend
select date_trunc('month', "FAIL_DATE") as period, count(*) as records
from library.failed_banks
where "FAIL_DATE" is not null
group by 1
order by 1
```

Every U.S. bank that has failed since 1934 -- when it collapsed, who bought it, and what it cost.

Source: `THE_LIBRARY.ECONOMY.FAILED_BANKS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Failed Banks over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
