---
title: Pharma Payments To Doctors
---

```sql n
select 15385047 as row_count
```

Every payment drug and device makers gave doctors and hospitals in 2024 -- 15.4M records of industry money.

Source: `THE_LIBRARY.HEALTH.PHARMA_PAYMENTS_TO_DOCTORS` (raw, 15,385,047 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.pharma_payments_to_doctors
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Pharma Payments To Doctors by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
