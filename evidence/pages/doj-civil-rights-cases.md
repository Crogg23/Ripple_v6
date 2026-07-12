---
title: Doj Civil Rights Cases
---

```sql rows
select * from library.doj_civil_rights_cases
```

```sql n
select count(*) as row_count from library.doj_civil_rights_cases
```

Heads up: 1-row scrape stub of DOJ Civil Rights Division cases -- not the real dataset yet.

Source: `THE_LIBRARY.JUSTICE.DOJ_CIVIL_RIGHTS_CASES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
