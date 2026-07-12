---
title: Epstein File Manifest
---

```sql rows
select * from library.epstein_file_manifest
```

```sql n
select count(*) as row_count from library.epstein_file_manifest
```

A monthly index of every file the DOJ's Epstein Library lists publicly.

Source: `THE_LIBRARY.GOVERNMENT.EPSTEIN_FILE_MANIFEST` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
