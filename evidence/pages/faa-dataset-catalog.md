---
title: Faa Dataset Catalog
---

```sql rows
select * from library.faa_dataset_catalog
```

```sql n
select count(*) as row_count from library.faa_dataset_catalog
```

Index of FAA public datasets (4-row stub).

Source: `THE_LIBRARY.TRANSPORT.FAA_DATASET_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
