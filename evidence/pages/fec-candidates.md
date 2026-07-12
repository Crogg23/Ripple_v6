---
title: Fec Candidates
---

```sql rows
select * from library.fec_candidates
```

```sql n
select count(*) as row_count from library.fec_candidates
```

Everyone who ran for federal office per the FEC -- 17,900 candidate-cycle records with party, office, and status.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
