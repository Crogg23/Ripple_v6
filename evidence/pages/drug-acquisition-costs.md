---
title: Drug Acquisition Costs
---

```sql n
select 1497925 as row_count
```

What pharmacies actually pay per unit for each drug (by NDC) -- the true-cost benchmark for the markup story.

Source: `THE_LIBRARY.HEALTH.DRUG_ACQUISITION_COSTS` (raw, 1,497,925 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.drug_acquisition_costs
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Drug Acquisition Costs by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
