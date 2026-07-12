---
title: Incarceration Trends By County
---

```sql n
select 128507 as row_count
```

Jail and prison populations for every US county over time, broken out by race and sex.

Source: `THE_LIBRARY.JUSTICE.INCARCERATION_TRENDS_BY_COUNTY` (raw, 128,507 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.incarceration_trends_by_county
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Incarceration Trends By County by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
