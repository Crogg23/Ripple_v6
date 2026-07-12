---
title: Global Temperature Anomaly
---

```sql rows
select * from library.global_temperature_anomaly
```

```sql n
select count(*) as row_count from library.global_temperature_anomaly
```

How far each year's temperature ran above or below the historical baseline -- the climate-change line.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.GLOBAL_TEMPERATURE_ANOMALY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
