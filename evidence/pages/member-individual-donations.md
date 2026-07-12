---
title: Member Individual Donations
---

```sql rows
select * from library.member_individual_donations
```

```sql n
select count(*) as row_count from library.member_individual_donations
```

Where each member of Congress's individual donor money came from -- direct, earmarked, and self-funded.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.MEMBER_INDIVIDUAL_DONATIONS` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
