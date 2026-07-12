---
title: Fec Candidates Fed Fec Bulk Candidates
---

```sql rows
select * from library.fec_candidates_fed_fec_bulk_candidates
```

```sql n
select count(*) as row_count from library.fec_candidates_fed_fec_bulk_candidates
```

Every federal candidate who filed with the FEC -- ID, office, party, state, incumbent or challenger.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATES_FED_FEC_BULK_CANDIDATES` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
