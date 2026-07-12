---
title: Nonprofits By State And Ntee
---

```sql rows
select * from library.nonprofits_by_state_and_ntee
```

```sql n
select count(*) as row_count from library.nonprofits_by_state_and_ntee
```

IRS Business Master File (tax-exempt orgs) rolled to STATE x 501(c) SUBSECTION x NTEE_MAJOR (first letter of the NTEE code = broad nonprofit category).

Source: `THE_LIBRARY.COMPANIES.NONPROFITS_BY_STATE_AND_NTEE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
