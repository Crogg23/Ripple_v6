---
title: Member Money Raised
---

```sql rows
select * from library.member_money_raised
```

```sql n
select count(*) as row_count from library.member_money_raised
```

How much each member of Congress raised -- gross receipts, net, and cash on hand, by cycle.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.MEMBER_MONEY_RAISED` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
