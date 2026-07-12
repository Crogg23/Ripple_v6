---
title: Immigration Court Cases
---

```sql n
select 12631225 as row_count
```

12.6M immigration court case rows -- but only the case-type column landed. Big row count, thin substance; needs a re-pour.

Source: `THE_LIBRARY.IMMIGRATION.IMMIGRATION_COURT_CASES` (raw, 12,631,225 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
