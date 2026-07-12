---
title: Scotus Justices
---

```sql rows
select * from library.scotus_justices
```

```sql n
select count(*) as row_count from library.scotus_justices
```

40 Supreme Court justices with their terms and how many cases and votes they've cast.

Source: `THE_LIBRARY.JUSTICE.SCOTUS_JUSTICES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
