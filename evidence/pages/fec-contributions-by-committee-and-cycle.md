---
title: Fec Contributions By Committee And Cycle
---

```sql rows
select * from library.fec_contributions_by_committee_and_cycle
```

```sql n
select count(*) as row_count from library.fec_contributions_by_committee_and_cycle
```

FEC individual contributions rolled to recipient COMMITTEE (CMTE_ID) x CYCLE_YEAR.

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CONTRIBUTIONS_BY_COMMITTEE_AND_CYCLE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
