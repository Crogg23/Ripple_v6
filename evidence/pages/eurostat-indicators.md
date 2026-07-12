---
title: Eurostat Indicators
---

```sql rows
select * from library.eurostat_indicators
```

```sql n
select count(*) as row_count from library.eurostat_indicators
```

EU statistical indicators from Eurostat -- geo, time, value across domains (450-row probe).

Source: `THE_LIBRARY.GEOGRAPHY.EUROSTAT_INDICATORS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
