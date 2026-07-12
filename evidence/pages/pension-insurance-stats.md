---
title: Pension Insurance Stats
---

```sql n
select 149771 as row_count
```

150K rows of PBGC pension insurance statistics -- claims, payments, and program finances by year.

Source: `THE_LIBRARY.ECONOMY.PENSION_INSURANCE_STATS` (raw, 149,771 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.pension_insurance_stats
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Pension Insurance Stats by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
