---
title: Doj Archived Pages
---

```sql rows
select * from library.doj_archived_pages
```

```sql n
select count(*) as row_count from library.doj_archived_pages
```

Raw: 2,542 archived Justice Dept web pages pulled from the Wayback Machine.

Source: `THE_LIBRARY.INVESTIGATIONS.DOJ_ARCHIVED_PAGES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
