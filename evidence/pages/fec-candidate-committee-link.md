---
title: Fec Candidate Committee Link
---

```sql rows
select * from library.fec_candidate_committee_link
```

```sql n
select count(*) as row_count from library.fec_candidate_committee_link
```

The bridge tying candidates to their campaign committees -- 16,229 links between CAND_ID and CMTE_ID.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CANDIDATE_COMMITTEE_LINK` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
