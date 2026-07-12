---
title: Healthcare Shortage Areas
---

```sql n
select 165531 as row_count
```

166K HRSA designations of health professional shortage areas -- where the US lacks doctors, dentists, and mental health care.

Source: `THE_LIBRARY.HEALTH.HEALTHCARE_SHORTAGE_AREAS` (raw, 165,531 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.healthcare_shortage_areas
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Healthcare Shortage Areas by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
