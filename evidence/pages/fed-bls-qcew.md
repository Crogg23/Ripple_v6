---
title: Fed Bls Qcew
---

```sql n
select 3619437 as row_count
```

County-level quarterly and annual employment and wage statistics by industry (NAICS) and ownership sector, derived from unemployment insurance tax records.

Source: `THE_LIBRARY.ECONOMY.FED_BLS_QCEW` (raw, 3,619,437 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.fed_bls_qcew
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Fed Bls Qcew by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
