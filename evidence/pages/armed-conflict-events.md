---
title: Armed Conflict Events
---

```sql n
select 385918 as row_count
```

Every dated, mapped event of organized violence worldwide since 1989 -- 386K events with death tolls.

Source: `THE_LIBRARY.CRIME_SECURITY.ARMED_CONFLICT_EVENTS` (raw, 385,918 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.armed_conflict_events
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Armed Conflict Events by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
