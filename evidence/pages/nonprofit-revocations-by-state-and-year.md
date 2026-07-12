---
title: Nonprofit Revocations By State And Year
---

```sql rows
select * from library.nonprofit_revocations_by_state_and_year
```

```sql n
select count(*) as row_count from library.nonprofit_revocations_by_state_and_year
```

IRS automatic revocations of tax-exempt status rolled to org STATE x REVOCATION_YEAR.

Source: `THE_LIBRARY.COMPANIES.NONPROFIT_REVOCATIONS_BY_STATE_AND_YEAR` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
