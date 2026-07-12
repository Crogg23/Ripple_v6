---
title: Bill Cosponsors
---

```sql n
select 367735 as row_count
```

367K links between bills and the members of Congress who cosponsored them.

Source: `THE_LIBRARY.GOVERNMENT.BILL_COSPONSORS` (curated, 367,735 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.bill_cosponsors
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Bill Cosponsors by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
