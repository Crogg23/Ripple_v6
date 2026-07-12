---
title: Aircraft Registry
---

```sql n
select 314417 as row_count
```

The FAA registry of all 314K US civil aircraft -- N-number, owner name and address, make/model, registration dates.

Source: `THE_LIBRARY.TRANSPORT.AIRCRAFT_REGISTRY` (raw, 314,417 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.aircraft_registry
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Aircraft Registry by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
