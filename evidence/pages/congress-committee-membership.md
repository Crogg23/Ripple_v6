---
title: Congress Committee Membership
---

```sql rows
select * from library.congress_committee_membership
```

```sql n
select count(*) as row_count from library.congress_committee_membership
```

Who sits on and chairs each committee in Congress -- the map of who holds real power.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_COMMITTEE_MEMBERSHIP` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
