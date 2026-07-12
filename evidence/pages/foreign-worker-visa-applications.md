---
title: Foreign Worker Visa Applications
---

```sql n
select 664616 as row_count
```

665K employer applications for foreign workers -- H-1B, PERM, H-2A/B -- with employer, job, wage, and outcome.

Source: `THE_LIBRARY.IMMIGRATION.FOREIGN_WORKER_VISA_APPLICATIONS` (raw, 664,616 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.foreign_worker_visa_applications
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Foreign Worker Visa Applications by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
