---
title: Congressional Rollcall Votes Fed Voteview Rollcall Meta
---

```sql rows
select * from library.congressional_rollcall_votes_fed_voteview_rollcall_meta
```

```sql n
select count(*) as row_count from library.congressional_rollcall_votes_fed_voteview_rollcall_meta
```

```sql trend
select date_trunc('month', "DATE") as period, count(*) as records
from library.congressional_rollcall_votes_fed_voteview_rollcall_meta
where "DATE" is not null
group by 1
order by 1
```

Every recorded House and Senate roll-call vote -- date, question, bill, yea/nay counts, result.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESSIONAL_ROLLCALL_VOTES_FED_VOTEVIEW_ROLLCALL_META` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Congressional Rollcall Votes Fed Voteview Rollcall Meta over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
