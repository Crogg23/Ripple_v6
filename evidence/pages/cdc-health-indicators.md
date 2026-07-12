---
title: Cdc Health Indicators
---

```sql rows
select * from library.cdc_health_indicators
```

```sql n
select count(*) as row_count from library.cdc_health_indicators
```

15K public-health indicator records from the CDC open data portal -- topic, place, year, value.

Source: `THE_LIBRARY.HEALTH.CDC_HEALTH_INDICATORS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
