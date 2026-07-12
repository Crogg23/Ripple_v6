---
title: Sovereign Debt By Creditor
---

```sql rows
select * from library.sovereign_debt_by_creditor
```

```sql n
select count(*) as row_count from library.sovereign_debt_by_creditor
```

How much each developing country owes, and to whom -- World Bank external-debt panel, 1970-2032.

Source: `THE_LIBRARY.MONEY.SOVEREIGN_DEBT_BY_CREDITOR` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
