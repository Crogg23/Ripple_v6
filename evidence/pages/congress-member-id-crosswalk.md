---
title: Congress Member Id Crosswalk
---

```sql rows
select * from library.congress_member_id_crosswalk
```

```sql n
select count(*) as row_count from library.congress_member_id_crosswalk
```

The Rosetta Stone linking each member of Congress across every ID system (FEC, ICPSR, Wikidata, etc.).

Source: `THE_LIBRARY.GOVERNMENT.CONGRESS_MEMBER_ID_CROSSWALK` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
