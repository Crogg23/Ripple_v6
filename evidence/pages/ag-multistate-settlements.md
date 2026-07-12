---
title: Ag Multistate Settlements
---

```sql rows
select * from library.ag_multistate_settlements
```

```sql n
select count(*) as row_count from library.ag_multistate_settlements
```

NAAG multistate settlements -- one row per multistate AG settlement (defendants, amounts, participating states, issue area, NAICS).

Source: `THE_LIBRARY.JUSTICE.AG_MULTISTATE_SETTLEMENTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
