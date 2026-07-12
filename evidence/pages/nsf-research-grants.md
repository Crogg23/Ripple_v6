---
title: Nsf Research Grants
---

```sql rows
select * from library.nsf_research_grants
```

```sql n
select count(*) as row_count from library.nsf_research_grants
```

```sql trend
select date_trunc('month', "AWARD_DATE") as period, count(*) as records
from library.nsf_research_grants
where "AWARD_DATE" is not null
group by 1
order by 1
```

NSF research awards -- who got funded, at which institution, for what, and how much (125-row probe).

Source: `THE_LIBRARY.SCIENCE.NSF_RESEARCH_GRANTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Nsf Research Grants over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
