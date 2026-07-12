---
title: Irs Income Stats By Zip
---

```sql n
select 179796 as row_count
```

IRS Statistics of Income by ZIP code -- returns filed, income brackets, and totals per ZIP (180K rows).

Source: `THE_LIBRARY.MONEY.IRS_INCOME_STATS_BY_ZIP` (raw, 179,796 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.irs_income_stats_by_zip
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Irs Income Stats By Zip by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
