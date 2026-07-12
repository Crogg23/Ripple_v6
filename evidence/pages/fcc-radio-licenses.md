---
title: Fcc Radio Licenses
---

```sql n
select 1689338 as row_count
```

1.7M FCC radio and wireless licenses -- call sign, licensee, status, grant and expiry dates.

Source: `THE_LIBRARY.GOVERNMENT.FCC_RADIO_LICENSES` (raw, 1,689,338 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.fcc_radio_licenses
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Fcc Radio Licenses by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
