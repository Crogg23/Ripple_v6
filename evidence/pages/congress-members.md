---
title: Congress Members
---

```sql rows
select * from library.congress_members
```

```sql n
select count(*) as row_count from library.congress_members
```

The master list of every member of Congress with party, state, tenure, and ideology score.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_MEMBERS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
