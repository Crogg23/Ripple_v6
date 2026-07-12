---
title: Food Security Indicators
---

```sql n
select 279470 as row_count
```

Chronic-hunger stats by country over 60+ years -- undernourishment and food-insecurity scales.

Source: `THE_LIBRARY.ECONOMY.FOOD_SECURITY_INDICATORS` (raw, 279,470 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.food_security_indicators
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Food Security Indicators by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
