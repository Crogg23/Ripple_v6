---
title: Fec Candidate Committee Links
---

```sql rows
select * from library.fec_candidate_committee_links
```

```sql n
select count(*) as row_count from library.fec_candidate_committee_links
```

The official bridge tying FEC candidates to their committees -- which committee raises money for whom.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATE_COMMITTEE_LINKS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
