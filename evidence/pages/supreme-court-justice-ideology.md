---
title: Supreme Court Justice Ideology
---

```sql rows
select * from library.supreme_court_justice_ideology
```

```sql n
select count(*) as row_count from library.supreme_court_justice_ideology
```

Ideology score for every Supreme Court justice by year, 1937-2022 -- how left/right they leaned.

Source: `THE_LIBRARY.GOVERNMENT.SUPREME_COURT_JUSTICE_IDEOLOGY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
