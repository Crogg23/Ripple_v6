---
title: Hud Dataset Catalog
---

```sql rows
select * from library.hud_dataset_catalog
```

```sql n
select count(*) as row_count from library.hud_dataset_catalog
```

Index of HUD open datasets on huduser.gov -- what exists, where to get it (77 catalog rows).

Source: `THE_LIBRARY.HOUSING.HUD_DATASET_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
