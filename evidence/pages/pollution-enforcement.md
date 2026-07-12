---
title: Pollution Enforcement
---

```sql n
select 3157891 as row_count
```

Every EPA-regulated facility -- inspections, violations, and fines, 3.2M sites.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.POLLUTION_ENFORCEMENT` (raw, 3,157,891 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.pollution_enforcement
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Pollution Enforcement by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
