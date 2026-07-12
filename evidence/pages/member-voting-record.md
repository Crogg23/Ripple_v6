---
title: Member Voting Record
---

```sql rows
select * from library.member_voting_record
```

```sql n
select count(*) as row_count from library.member_voting_record
```

Each member of Congress scored: how often they show up to vote and how often they toe the party line.

Source: `THE_LIBRARY.GOVERNMENT.MEMBER_VOTING_RECORD` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
