---
title: Government Ideology Medians
---

```sql rows
select * from library.government_ideology_medians
```

```sql n
select count(*) as row_count from library.government_ideology_medians
```

By year: the ideological midpoint of the President, House, Senate, and Supreme Court on one scale.

Source: `THE_LIBRARY.JUSTICE.GOVERNMENT_IDEOLOGY_MEDIANS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
