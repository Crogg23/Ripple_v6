---
title: Sec Filing Submissions
---

```sql rows
select * from library.sec_filing_submissions
```

```sql n
select count(*) as row_count from library.sec_filing_submissions
```

Header details for company financial filings to the SEC -- who filed, when, and what form.

Source: `THE_LIBRARY.MONEY.SEC_FILING_SUBMISSIONS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
