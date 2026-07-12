---
title: Un Vote Agreement Pairs
---

```sql n
select 1823352 as row_count
```

How often every pair of countries voted the same way at the UN General Assembly -- 1.8M pairs.

Source: `THE_LIBRARY.GOVERNMENT.UN_VOTE_AGREEMENT_PAIRS` (raw, 1,823,352 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.un_vote_agreement_pairs
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Un Vote Agreement Pairs by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
