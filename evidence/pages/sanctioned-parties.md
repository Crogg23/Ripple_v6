---
title: Sanctioned Parties
---

```sql rows
select * from library.sanctioned_parties
```

```sql n
select count(*) as row_count from library.sanctioned_parties
```

The U.S. Treasury sanctions blacklist: every person, company, and ship Americans are barred from dealing with.

Source: `THE_LIBRARY.SANCTIONS.SANCTIONED_PARTIES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
