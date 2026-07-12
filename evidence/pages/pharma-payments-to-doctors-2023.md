---
title: Pharma Payments To Doctors 2023
---

```sql n
select 14700786 as row_count
```

Every 2023 payment drug and device makers gave to US doctors and hospitals -- 14.7 million records.

Source: `THE_LIBRARY.HEALTH.PHARMA_PAYMENTS_TO_DOCTORS_2023` (raw, 14,700,786 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.pharma_payments_to_doctors_2023
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Pharma Payments To Doctors 2023 by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
