---
title: Sba Loans By State And Program
---

```sql rows
select * from library.sba_loans_by_state_and_program
```

```sql n
select count(*) as row_count from library.sba_loans_by_state_and_program
```

SBA 7(a)/504 loan approvals rolled to borrower STATE x PROGRAM x approval fiscal year.

Source: `THE_LIBRARY.GOVERNMENT_SPENDING.SBA_LOANS_BY_STATE_AND_PROGRAM` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
