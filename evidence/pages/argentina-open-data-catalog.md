---
title: Argentina Open Data Catalog
---

```sql rows
select * from library.argentina_open_data_catalog
```

```sql n
select count(*) as row_count from library.argentina_open_data_catalog
```

Catalog of 3,556 datasets on Argentina's national open-data portal, plus time-series samples.

Source: `THE_LIBRARY.OPEN_DATA.ARGENTINA_OPEN_DATA_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
