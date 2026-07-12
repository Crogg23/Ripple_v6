---
title: Sec Edgar Filings
---

```sql rows
select * from library.sec_edgar_filings
```

```sql n
select count(*) as row_count from library.sec_edgar_filings
```

49K SEC EDGAR filings -- company, ticker, form type, filing date, SIC code, and document links.

Source: `THE_LIBRARY.COMPANIES.SEC_EDGAR_FILINGS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
