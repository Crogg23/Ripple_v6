---
title: Bank Call Reports
---

```sql rows
select * from library.bank_call_reports
```

```sql n
select count(*) as row_count from library.bank_call_reports
```

Quarterly financial condition reports for US banks -- assets, deposits, loans, capital -- keyed on RSSD ID (302-row probe).

Source: `THE_LIBRARY.MONEY.BANK_CALL_REPORTS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
