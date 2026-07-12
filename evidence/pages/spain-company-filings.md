---
title: Spain Company Filings
---

```sql rows
select * from library.spain_company_filings
```

```sql n
select count(*) as row_count from library.spain_company_filings
```

Spanish BORME company filings -- one row per registry act (company, act type, province, CVE, PDF).

Source: `THE_LIBRARY.COMPANIES.SPAIN_COMPANY_FILINGS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
