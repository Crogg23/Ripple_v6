---
title: Individual Donations
---

```sql n
select 84172112 as row_count
```

The 84M-row firehose: every itemized donation individuals gave to federal committees. The rawest follow-the-money.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.INDIVIDUAL_DONATIONS` (raw, 84,172,112 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.individual_donations
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Individual Donations by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
