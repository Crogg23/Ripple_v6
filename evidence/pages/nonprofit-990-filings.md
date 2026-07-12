---
title: Nonprofit 990 Filings
---

```sql rows
select * from library.nonprofit_990_filings
```

```sql n
select count(*) as row_count from library.nonprofit_990_filings
```

Index of nonprofit Form 990 e-filings -- EIN, org name, tax year, revenue, assets (200-row probe).

Source: `THE_LIBRARY.COMPANIES.NONPROFIT_990_FILINGS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
