---
title: Revoked Nonprofits
---

```sql n
select 1206628 as row_count
```

Nonprofits that lost their tax-exempt status -- 1.2M orgs the IRS auto-revoked, keyed by EIN.

Source: `THE_LIBRARY.COMPANIES.REVOKED_NONPROFITS` (raw, 1,206,628 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.revoked_nonprofits
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Revoked Nonprofits by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
