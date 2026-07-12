---
title: Densho Incarceration Archive
---

```sql rows
select * from library.densho_incarceration_archive
```

```sql n
select count(*) as row_count from library.densho_incarceration_archive
```

Densho's digital archive of Japanese American WWII incarceration -- photos, documents, and oral histories (25-item probe).

Source: `THE_LIBRARY.HISTORY.DENSHO_INCARCERATION_ARCHIVE` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
