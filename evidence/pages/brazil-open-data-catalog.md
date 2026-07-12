---
title: Brazil Open Data Catalog
---

```sql rows
select * from library.brazil_open_data_catalog
```

```sql n
select count(*) as row_count from library.brazil_open_data_catalog
```

Catalog sample from Brazil's national open-data portal (10 rows).

Source: `THE_LIBRARY.OPEN_DATA.BRAZIL_OPEN_DATA_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
