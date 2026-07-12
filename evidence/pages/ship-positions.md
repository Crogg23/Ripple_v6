---
title: Ship Positions
---

```sql n
select 7296017 as row_count
```

7.3M GPS pings from ships in US waters in 2024 -- where, when, how fast, and what they were carrying.

Source: `THE_LIBRARY.TRANSPORT.SHIP_POSITIONS` (curated, 7,296,017 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.ship_positions
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Ship Positions by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
