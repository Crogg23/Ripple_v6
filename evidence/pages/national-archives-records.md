---
title: National Archives Records
---

```sql rows
select * from library.national_archives_records
```

```sql n
select count(*) as row_count from library.national_archives_records
```

A catalog of high-value electronic records the National Archives put online -- military, diplomatic, personnel files.

Source: `THE_LIBRARY.HISTORY.NATIONAL_ARCHIVES_RECORDS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
