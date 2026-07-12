---
title: American South Texts
---

```sql rows
select * from library.american_south_texts
```

```sql n
select count(*) as row_count from library.american_south_texts
```

Full-text corpora from Documenting the American South -- slave narratives, Southern literature, church records (144 texts).

Source: `THE_LIBRARY.HISTORY.AMERICAN_SOUTH_TEXTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
