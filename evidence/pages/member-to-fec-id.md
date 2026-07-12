---
title: Member To Fec Id
---

```sql rows
select * from library.member_to_fec_id
```

```sql n
select count(*) as row_count from library.member_to_fec_id
```

Bridge from a member of Congress to their FEC candidate ID, unrolled one row per ID.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.MEMBER_TO_FEC_ID` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
