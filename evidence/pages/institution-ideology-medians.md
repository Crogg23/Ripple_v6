---
title: Institution Ideology Medians
---

```sql rows
select * from library.institution_ideology_medians
```

```sql n
select count(*) as row_count from library.institution_ideology_medians
```

Yearly left-right ideology score for the Supreme Court, every circuit, House, Senate and president since 1937.

Source: `THE_LIBRARY.GOVERNMENT.INSTITUTION_IDEOLOGY_MEDIANS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
