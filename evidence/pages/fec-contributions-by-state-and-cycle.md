---
title: Fec Contributions By State And Cycle
---

```sql rows
select * from library.fec_contributions_by_state_and_cycle
```

```sql n
select count(*) as row_count from library.fec_contributions_by_state_and_cycle
```

FEC individual contributions rolled to contributor STATE x CYCLE_YEAR (calendar year of the transaction).

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FEC_CONTRIBUTIONS_BY_STATE_AND_CYCLE` (curated).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
