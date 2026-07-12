---
title: Congress Rollcall Votes
---

```sql n
select 945523 as row_count
```

Every recorded congressional vote, member-by-member -- 945K rows of how each one voted.

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_ROLLCALL_VOTES` (raw, 945,523 rows). This page reads a bounded pre-aggregate of that view, not every row.

<BigValue data={n} value=row_count title="Rows in the full source" fmt="#,##0" />
