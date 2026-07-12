---
title: Fed Fhfa Nmdb
---

```sql n
select 19054246 as row_count
```

Aggregate statistics on new, outstanding, and performance characteristics of US residential mortgages drawn from the NMDB 5% national sample, published at national, regional, state, and metro levels.

Source: `THE_LIBRARY.HOUSING.FED_FHFA_NMDB` (raw, 19,054,246 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.fed_fhfa_nmdb
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Fed Fhfa Nmdb by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
