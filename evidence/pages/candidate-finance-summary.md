---
title: Candidate Finance Summary
---

```sql rows
select * from library.candidate_finance_summary
```

```sql n
select count(*) as row_count from library.candidate_finance_summary
```

```sql trend
select date_trunc('month', "CVG_END_DT") as period, count(*) as records
from library.candidate_finance_summary
where "CVG_END_DT" is not null
group by 1
order by 1
```

How much each federal candidate raised and spent per cycle -- the money-raised stat.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.CANDIDATE_FINANCE_SUMMARY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Candidate Finance Summary over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
