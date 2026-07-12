---
title: Providers By Taxonomy And State
---

```sql rows
select * from library.providers_by_taxonomy_and_state
```

```sql n
select count(*) as row_count from library.providers_by_taxonomy_and_state
```

NPPES national provider registry rolled to primary TAXONOMY_CODE x practice STATE x ENTITY_TYPE_CODE (1=individual, 2=organization).

Source: `THE_LIBRARY.HEALTH.PROVIDERS_BY_TAXONOMY_AND_STATE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
