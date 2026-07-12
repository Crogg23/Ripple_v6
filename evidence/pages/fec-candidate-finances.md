---
title: Fec Candidate Finances
---

```sql rows
select * from library.fec_candidate_finances
```

```sql n
select count(*) as row_count from library.fec_candidate_finances
```

Federal candidates' campaign money per cycle: total raised, spent, cash on hand, and debt.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATE_FINANCES` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
