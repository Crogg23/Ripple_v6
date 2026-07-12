---
title: Doj Archived Page Snapshots
---

```sql rows
select * from library.doj_archived_page_snapshots
```

```sql n
select count(*) as row_count from library.doj_archived_page_snapshots
```

24,897 Wayback Machine snapshots of DOJ web pages -- an archive trail of what Justice published, and when.

Source: `THE_LIBRARY.INVESTIGATIONS.DOJ_ARCHIVED_PAGE_SNAPSHOTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
