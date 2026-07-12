---
title: Ghana Open Data Catalog
---

```sql rows
select * from library.ghana_open_data_catalog
```

```sql n
select count(*) as row_count from library.ghana_open_data_catalog
```

Catalog sample from Ghana's open-data portal (10 rows).

Source: `THE_LIBRARY.OPEN_DATA.GHANA_OPEN_DATA_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
