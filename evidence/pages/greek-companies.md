---
title: Greek Companies
---

```sql rows
select * from library.greek_companies
```

```sql n
select count(*) as row_count from library.greek_companies
```

Heads up: 40-row sample of Greece's official company registry (GEMI) -- shape only, not the full country.

Source: `THE_LIBRARY.COMPANIES.GREEK_COMPANIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
