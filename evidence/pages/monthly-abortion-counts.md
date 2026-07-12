---
title: Monthly Abortion Counts
---

```sql rows
select * from library.monthly_abortion_counts
```

```sql n
select count(*) as row_count from library.monthly_abortion_counts
```

Monthly estimated abortion counts by US state, with low/high uncertainty bounds.

Source: `THE_LIBRARY.HEALTH.MONTHLY_ABORTION_COUNTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
