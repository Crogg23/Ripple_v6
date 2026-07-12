---
title: Member Pac Money
---

```sql rows
select * from library.member_pac_money
```

```sql n
select count(*) as row_count from library.member_pac_money
```

Per member of Congress, per cycle: PAC money raised and outside spending for and against them.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.MEMBER_PAC_MONEY` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
