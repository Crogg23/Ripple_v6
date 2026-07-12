---
title: Fec Committees Fed Fec Bulk
---

```sql rows
select * from library.fec_committees_fed_fec_bulk
```

```sql n
select count(*) as row_count from library.fec_committees_fed_fec_bulk
```

Every federal political committee registered with the FEC for 2024 -- PACs, party orgs, campaign committees.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_COMMITTEES_FED_FEC_BULK` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
