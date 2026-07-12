---
title: Federal Court Caseloads
---

```sql rows
select * from library.federal_court_caseloads
```

```sql n
select count(*) as row_count from library.federal_court_caseloads
```

US federal court caseload statistics tables -- filings, terminations, and pending cases by court (50 table-rows).

Source: `THE_LIBRARY.JUSTICE.FEDERAL_COURT_CASELOADS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
