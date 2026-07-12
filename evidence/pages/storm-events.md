---
title: Storm Events
---

```sql n
select 1780730 as row_count
```

Every US severe-weather event -- deaths, injuries, property/crop damage, location -- 1.8M records.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.STORM_EVENTS` (raw, 1,780,730 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.storm_events
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Storm Events by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
