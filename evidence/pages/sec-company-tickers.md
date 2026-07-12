---
title: Sec Company Tickers
---

```sql rows
select * from library.sec_company_tickers
```

```sql n
select count(*) as row_count from library.sec_company_tickers
```

Every SEC-registered company mapped to its CIK number and stock ticker symbol.

Source: `THE_LIBRARY.ECONOMY.SEC_COMPANY_TICKERS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
