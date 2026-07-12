---
title: Immigration Yearbook Tables
---

```sql rows
select * from library.immigration_yearbook_tables
```

```sql n
select count(*) as row_count from library.immigration_yearbook_tables
```

DHS Yearbook tables -- green cards, admissions, refugees, naturalizations by year and country (27 table-rows).

Source: `THE_LIBRARY.IMMIGRATION.IMMIGRATION_YEARBOOK_TABLES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
