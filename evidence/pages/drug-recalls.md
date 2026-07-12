---
title: Drug Recalls
---

```sql rows
select * from library.drug_recalls
```

```sql n
select count(*) as row_count from library.drug_recalls
```

```sql trend
select date_trunc('month', "RECALL_INITIATION_DATE") as period, count(*) as records
from library.drug_recalls
where "RECALL_INITIATION_DATE" is not null
group by 1
order by 1
```

FDA drug recalls: which product, made by whom, why it was pulled, and how dangerous it was.

Source: `THE_LIBRARY.HEALTH.DRUG_RECALLS` (sample).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Drug Recalls over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
