---
title: Weather Alerts
---

```sql rows
select * from library.weather_alerts
```

```sql n
select count(*) as row_count from library.weather_alerts
```

Active National Weather Service alerts -- event, severity, urgency, and affected area (287-row snapshot).

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.WEATHER_ALERTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
