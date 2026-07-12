---
title: Fed Sba Ppp
---

```sql n
select 968524 as row_count
```

Loan-level records of Paycheck Protection Program (PPP) loans of $150,000 or more, including borrower, lender, amounts, and forgiveness status.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.FED_SBA_PPP` (raw, 968,524 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.fed_sba_ppp
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Fed Sba Ppp by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
