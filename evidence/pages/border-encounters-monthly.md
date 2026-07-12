---
title: Border Encounters Monthly
---

```sql rows
select * from library.border_encounters_monthly
```

```sql n
select count(*) as row_count from library.border_encounters_monthly
```

CBP nationwide encounter totals in pivoted month columns (9 rows -- awkward shape, thin so far).

Source: `THE_LIBRARY.IMMIGRATION.BORDER_ENCOUNTERS_MONTHLY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
