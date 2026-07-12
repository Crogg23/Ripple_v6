---
title: Transportation Data Catalog
---

```sql rows
select * from library.transportation_data_catalog
```

```sql n
select count(*) as row_count from library.transportation_data_catalog
```

Index of BTS TranStats transportation databases -- aviation, freight, rail, transit (21 rows).

Source: `THE_LIBRARY.TRANSPORT.TRANSPORTATION_DATA_CATALOG` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
