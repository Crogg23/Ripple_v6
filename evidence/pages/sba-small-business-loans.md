---
title: Sba Small Business Loans
---

```sql n
select 2174502 as row_count
```

2.2M SBA 7(a) and 504 loans since 1991 -- borrower name, address, lender, and amount, released under FOIA.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.SBA_SMALL_BUSINESS_LOANS` (raw, 2,174,502 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.sba_small_business_loans
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Sba Small Business Loans by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
