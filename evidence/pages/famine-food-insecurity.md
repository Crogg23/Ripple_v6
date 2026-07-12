---
title: Famine Food Insecurity
---

```sql rows
select * from library.famine_food_insecurity
```

```sql n
select count(*) as row_count from library.famine_food_insecurity
```

How many people are in famine or emergency-level hunger, by country and analysis period.

Source: `THE_LIBRARY.ECONOMY.FAMINE_FOOD_INSECURITY` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
