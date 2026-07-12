---
title: Foreign Agent Registrations
---

```sql rows
select * from library.foreign_agent_registrations
```

```sql n
select count(*) as row_count from library.foreign_agent_registrations
```

FARA filings -- who's registered as an agent of a foreign government, for whom, and the money involved (30-row probe).

Source: `THE_LIBRARY.CAMPAIGN_FINANCE.FOREIGN_AGENT_REGISTRATIONS` (raw).

<BigValue data={n} value=row_count title="Rows on the shelf" fmt="#,##0" />

<DataTable data={rows} search=true rows=20 />
