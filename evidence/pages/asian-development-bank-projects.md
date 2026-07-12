---
title: Asian Development Bank Projects
---

```sql rows
select * from library.asian_development_bank_projects
```

```sql n
select count(*) as row_count from library.asian_development_bank_projects
```

ADB development projects and economic indicators for Asia-Pacific -- project, country, sector, loan amount (41 rows).

Source: `THE_LIBRARY.PROCUREMENT.ASIAN_DEVELOPMENT_BANK_PROJECTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
