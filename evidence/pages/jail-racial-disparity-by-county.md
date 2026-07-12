---
title: Jail Racial Disparity By County
---

```sql n
select 128507 as row_count
```

County-by-year jail rates by race -- how much more often Black residents are jailed than white ones.

Source: `THE_LIBRARY.JUSTICE.JAIL_RACIAL_DISPARITY_BY_COUNTY` (curated, 128,507 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.jail_racial_disparity_by_county
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Jail Racial Disparity By County by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
