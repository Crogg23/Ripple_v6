---
title: Hhs Grant Awards
---

```sql rows
select * from library.hhs_grant_awards
```

```sql n
select count(*) as row_count from library.hhs_grant_awards
```

HHS TAGGS grant awards -- award number, recipient (name/EIN/geo), amount, assistance-listing (CFDA) number.

Source: `THE_LIBRARY.SPENDING.HHS_GRANT_AWARDS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
