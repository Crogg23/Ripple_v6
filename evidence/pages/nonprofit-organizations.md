---
title: Nonprofit Organizations
---

```sql n
select 1974830 as row_count
```

Every US tax-exempt organization -- 1.97 million nonprofits with EIN, type, and finances.

Source: `THE_LIBRARY.COMPANIES.NONPROFIT_ORGANIZATIONS` (raw, 1,974,830 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.nonprofit_organizations
```

<BarChart
    data={agg}
    x=category
    y=records
    swapXY=true
    title="Nonprofit Organizations by category"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
