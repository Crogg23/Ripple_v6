---
title: Congressional Rollcall Votes
---

```sql rows
select * from library.congressional_rollcall_votes
```

```sql n
select count(*) as row_count from library.congressional_rollcall_votes
```

```sql trend
select date_trunc('month', "VOTE_DATE") as period, count(*) as records
from library.congressional_rollcall_votes
where "VOTE_DATE" is not null
group by 1
order by 1
```

Every recorded floor vote in Congress: what the question was, the yea/nay count, and whether it passed.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESSIONAL_ROLLCALL_VOTES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Congressional Rollcall Votes over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
