---
title: Supreme Court Justices Crosswalk
---

```sql rows
select * from library.supreme_court_justices_crosswalk
```

```sql n
select count(*) as row_count from library.supreme_court_justices_crosswalk
```

A bridge that ties each Supreme Court justice to their official federal-judiciary ID.

Source: `THE_LIBRARY.JUSTICE.SUPREME_COURT_JUSTICES_CROSSWALK` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
