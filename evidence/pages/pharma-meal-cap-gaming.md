---
title: Pharma Meal Cap Gaming
---

```sql rows
select * from library.pharma_meal_cap_gaming
```

```sql n
select count(*) as row_count from library.pharma_meal_cap_gaming
```

Drug/device makers whose meals for doctors bunch suspiciously just under the $125 reporting cap.

Source: `THE_LIBRARY.HEALTH.PHARMA_MEAL_CAP_GAMING` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
