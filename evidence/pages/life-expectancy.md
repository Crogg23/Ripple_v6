---
title: Life Expectancy
---

```sql rows
select * from library.life_expectancy
```

```sql n
select count(*) as row_count from library.life_expectancy
```

Life expectancy at birth for every country, by year.

Source: `THE_LIBRARY.HEALTH.LIFE_EXPECTANCY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
