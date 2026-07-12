---
title: Web Page Changes
---

```sql n
select 203305 as row_count
```

203K archived-webpage snapshots flagging when a page appeared, changed, or went dead.

Source: `THE_LIBRARY.INVESTIGATIONS.WEB_PAGE_CHANGES` (curated, 203,305 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.web_page_changes
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Web Page Changes by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
