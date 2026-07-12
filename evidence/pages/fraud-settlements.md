---
title: Fraud Settlements
---

```sql rows
select * from library.fraud_settlements
```

```sql n
select count(*) as row_count from library.fraud_settlements
```

DOJ False Claims Act settlements -- defendant, amount, qui tam / relator, fraud type, agency defrauded, district.

Source: `THE_LIBRARY.JUSTICE.FRAUD_SETTLEMENTS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
