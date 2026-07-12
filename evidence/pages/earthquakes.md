---
title: Earthquakes
---

```sql n
select 443274 as row_count
```

Every recorded earthquake magnitude 2.5+ worldwide -- 443K events with time, place, and depth.

Source: `THE_LIBRARY.SCIENCE.EARTHQUAKES` (raw, 443,274 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.earthquakes
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Earthquakes by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
