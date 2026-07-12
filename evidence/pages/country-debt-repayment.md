---
title: Country Debt Repayment
---

```sql rows
select * from library.country_debt_repayment
```

```sql n
select count(*) as row_count from library.country_debt_repayment
```

How much each country owes each year in debt payments -- and which years are dangerous repayment spikes.

Source: `THE_LIBRARY.MONEY.COUNTRY_DEBT_REPAYMENT` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
