---
title: Country Freedom Scores
---

```sql rows
select * from library.country_freedom_scores
```

```sql n
select count(*) as row_count from library.country_freedom_scores
```

Freedom House's yearly Free / Partly Free / Not Free grade for every country, with the sub-scores behind it.

Source: `THE_LIBRARY.GOVERNMENT.COUNTRY_FREEDOM_SCORES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
