---
title: Corruption Perceptions Index
---

```sql rows
select * from library.corruption_perceptions_index
```

```sql n
select count(*) as row_count from library.corruption_perceptions_index
```

Transparency International's yearly corruption score for each country (0 = worst, 100 = clean).

Source: `THE_LIBRARY.GOVERNMENT.CORRUPTION_PERCEPTIONS_INDEX` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
