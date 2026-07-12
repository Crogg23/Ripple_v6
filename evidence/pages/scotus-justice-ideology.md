---
title: Scotus Justice Ideology
---

```sql rows
select * from library.scotus_justice_ideology
```

```sql n
select count(*) as row_count from library.scotus_justice_ideology
```

Each Supreme Court justice's ideology score (JCS/Martin-Quinn style) by term.

Source: `THE_LIBRARY.JUSTICE.SCOTUS_JUSTICE_IDEOLOGY` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
