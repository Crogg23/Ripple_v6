---
title: Congress Members Fed Congress Legislators
---

```sql rows
select * from library.congress_members_fed_congress_legislators
```

```sql n
select count(*) as row_count from library.congress_members_fed_congress_legislators
```

Every member of Congress, past and present, plus the ID crosswalk that links them everywhere.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_MEMBERS_FED_CONGRESS_LEGISLATORS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
