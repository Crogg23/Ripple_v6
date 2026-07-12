---
title: Consumer Finance Complaints
---

```sql rows
select * from library.consumer_finance_complaints
```

```sql n
select count(*) as row_count from library.consumer_finance_complaints
```

```sql trend
select date_trunc('month', "DATE_RECEIVED") as period, count(*) as records
from library.consumer_finance_complaints
where "DATE_RECEIVED" is not null
group by 1
order by 1
```

Consumer complaints about banks, lenders, and credit companies filed with the federal CFPB.

Source: `THE_LIBRARY.GOVERNMENT.CONSUMER_FINANCE_COMPLAINTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Consumer Finance Complaints over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
