---
title: Echr Court Cases
---

```sql rows
select * from library.echr_court_cases
```

```sql n
select count(*) as row_count from library.echr_court_cases
```

```sql trend
select date_trunc('month', "JUDGMENT_DATE") as period, count(*) as records
from library.echr_court_cases
where "JUDGMENT_DATE" is not null
group by 1
order by 1
```

European Court of Human Rights rulings: who sued which country, over what right, and who won.

Source: `THE_LIBRARY.JUSTICE.ECHR_COURT_CASES` (sample).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Echr Court Cases over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
