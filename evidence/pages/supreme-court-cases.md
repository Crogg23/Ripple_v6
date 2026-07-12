---
title: Supreme Court Cases
---

```sql rows
select * from library.supreme_court_cases
```

```sql n
select count(*) as row_count from library.supreme_court_cases
```

```sql trend
select date_trunc('month', "DATE") as period, count(*) as records
from library.supreme_court_cases
where "DATE" is not null
group by 1
order by 1
```

U.S. Supreme Court cases: who argued, how each justice voted, the ruling, plus audio/transcripts.

Source: `THE_LIBRARY.JUSTICE.SUPREME_COURT_CASES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Supreme Court Cases over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
