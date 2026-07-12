---
title: Slave Narratives 1936 1938
---

```sql rows
select * from library.slave_narratives_1936_1938
```

```sql n
select count(*) as row_count from library.slave_narratives_1936_1938
```

```sql trend
select date_trunc('month', "INTERVIEW_DATE") as period, count(*) as records
from library.slave_narratives_1936_1938
where "INTERVIEW_DATE" is not null
group by 1
order by 1
```

First-person interviews with formerly enslaved Americans, recorded by the WPA in 1936-1938.

Source: `THE_LIBRARY.HISTORY.SLAVE_NARRATIVES_1936_1938` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Slave Narratives 1936 1938 over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
