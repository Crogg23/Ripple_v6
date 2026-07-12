---
title: Ecuador Gov Contracts
---

```sql n
select 132995 as row_count
```

Ecuador's government contracts -- 133K records of who bought what, from which company, for how much.

Source: `THE_LIBRARY.PROCUREMENT.ECUADOR_GOV_CONTRACTS` (curated, 132,995 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.ecuador_gov_contracts
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Ecuador Gov Contracts by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
