---
title: Foreign Aid Transactions
---

```sql n
select 3967456 as row_count
```

4M transaction-level US foreign assistance records -- who got aid money, from which agency, for what, by country and year.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.FOREIGN_AID_TRANSACTIONS` (raw, 3,967,456 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.foreign_aid_transactions
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Foreign Aid Transactions by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
