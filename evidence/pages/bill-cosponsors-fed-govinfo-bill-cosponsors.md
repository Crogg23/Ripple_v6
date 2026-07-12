---
title: Bill Cosponsors Fed Govinfo Bill Cosponsors
---

```sql n
select 367742 as row_count
```

Who cosponsored which bill in Congress -- 368K links between members and bills.

Source: `THE_LIBRARY.GOVERNMENT.BILL_COSPONSORS_FED_GOVINFO_BILL_COSPONSORS` (raw, 367,742 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.bill_cosponsors_fed_govinfo_bill_cosponsors
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Bill Cosponsors Fed Govinfo Bill Cosponsors by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
