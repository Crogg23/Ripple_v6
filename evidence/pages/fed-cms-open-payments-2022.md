---
title: Fed Cms Open Payments 2022
---

```sql n
select 13250000 as row_count
```

CMS Open Payments - General Payments Detail (PY2022)

Source: `THE_LIBRARY.HEALTH.FED_CMS_OPEN_PAYMENTS_2022` (raw, 13,250,000 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.fed_cms_open_payments_2022
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Fed Cms Open Payments 2022 by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
