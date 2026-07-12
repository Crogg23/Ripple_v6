---
title: Preprints
---

```sql rows
select * from library.preprints
```

```sql n
select count(*) as row_count from library.preprints
```

```sql trend
select date_trunc('month', "PREPRINT_POSTED_DATE") as period, count(*) as records
from library.preprints
where "PREPRINT_POSTED_DATE" is not null
group by 1
order by 1
```

Biology and medical preprints from bioRxiv/medRxiv: authors, funders, and download counts.

Source: `THE_LIBRARY.SCIENCE.PREPRINTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<LineChart
    data={trend}
    x=period
    y=records
    title="Preprints over time (records per month)"
/>

<DataTable data={rows} search=true rows=20 />
