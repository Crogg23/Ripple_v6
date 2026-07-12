---
title: Cms Dataset Catalog
---

```sql rows
select * from library.cms_dataset_catalog
```

```sql n
select count(*) as row_count from library.cms_dataset_catalog
```

Index of datasets on the CMS data portal -- title, publisher, update cadence, access URL (158 rows).

Source: `THE_LIBRARY.HEALTH.CMS_DATASET_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
