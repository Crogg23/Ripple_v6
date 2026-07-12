---
title: Fec Committees
---

```sql rows
select * from library.fec_committees
```

```sql n
select count(*) as row_count from library.fec_committees
```

Every FEC-registered political committee (PACs, party, campaign) with type and affiliation.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_COMMITTEES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
