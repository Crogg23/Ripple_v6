---
title: Illicit Financial Flows
---

```sql rows
select * from library.illicit_financial_flows
```

```sql n
select count(*) as row_count from library.illicit_financial_flows
```

GFI estimates of trade-related illicit financial flows by country and year (25 rows).

Source: `THE_LIBRARY.ECONOMY.ILLICIT_FINANCIAL_FLOWS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
