---
title: Electricity By Country
---

```sql n
select 118463 as row_count
```

Yearly electricity generation, capacity, emissions, and demand for 200+ countries.

Source: `THE_LIBRARY.ENERGY_ENVIRONMENT.ELECTRICITY_BY_COUNTRY` (curated, 118,463 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.electricity_by_country
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Electricity By Country by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
