---
title: Georgia Open Data Catalog
---

```sql rows
select * from library.georgia_open_data_catalog
```

```sql n
select count(*) as row_count from library.georgia_open_data_catalog
```

Catalog stub from Georgia's (country) open-data portal (1 row).

Source: `THE_LIBRARY.OPEN_DATA.GEORGIA_OPEN_DATA_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
