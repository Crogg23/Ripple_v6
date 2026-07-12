---
title: Income Inequality Gini
---

```sql rows
select * from library.income_inequality_gini
```

```sql n
select count(*) as row_count from library.income_inequality_gini
```

The Gini index by country and year -- one number for how unequal each country's incomes are.

Source: `THE_LIBRARY.ECONOMY.INCOME_INEQUALITY_GINI` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
