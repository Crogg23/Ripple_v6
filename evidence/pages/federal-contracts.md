---
title: Federal Contracts
---

```sql n
select 6325622 as row_count
```

Every federal prime contract award for FY2025 -- who got paid, how much, for what.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.FEDERAL_CONTRACTS` (raw, 6,325,622 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.federal_contracts
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Federal Contracts by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
