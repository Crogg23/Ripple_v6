---
title: Pac Contributions To Candidates
---

```sql n
select 866730 as row_count
```

PAC and party money to (and spent for/against) federal candidates -- 867k transactions.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.PAC_CONTRIBUTIONS_TO_CANDIDATES` (raw, 866,730 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />

```sql agg
select * from library.pac_contributions_to_candidates
```

<BarChart
    data={agg}
    x=year
    y=records
    title="Pac Contributions To Candidates by year"
    fmt="#,##0"
/>

<DataTable data={agg} rows=25 />
