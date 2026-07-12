---
title: Water Monitoring Readings
---

```sql n
select 6694816 as row_count
```

6.7M sensor readings from USGS water monitoring stations -- streamflow, groundwater, and water quality by site and time.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.WATER_MONITORING_READINGS` (raw, 6,694,816 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.water_monitoring_readings
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Water Monitoring Readings by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
