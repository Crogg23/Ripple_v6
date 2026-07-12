---
title: Mineral Production By Country
---

```sql n
select 304632 as row_count
```

Global mineral commodity statistics -- production, reserves, and US import reliance by country, commodity, and year (305K rows).

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.MINERAL_PRODUCTION_BY_COUNTRY` (raw, 304,632 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.mineral_production_by_country
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Mineral Production By Country by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
