---
title: Credit Union Call Reports
---

```sql n
select 121713 as row_count
```

122K quarterly call-report records for federally insured credit unions -- the financial vitals, 1994 to present.

Source: `THE_LIBRARY.MONEY.CREDIT_UNION_CALL_REPORTS` (raw, 121,713 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.credit_union_call_reports
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Credit Union Call Reports by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
