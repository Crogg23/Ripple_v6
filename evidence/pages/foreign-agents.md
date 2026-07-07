---
title: Foreign Agents (FARA)
---

```sql by_country
select * from library.foreign_agents
```

```sql top_countries
select * from library.foreign_agents
order by registrations desc
limit 25
```

Everyone registered under the **Foreign Agents Registration Act** — lobbyists and
PR firms working for foreign governments and principals, by the country they
represent. Source: `fed_fara_bulk`, a typed curated mart.

<BarChart
    data={top_countries}
    x=country
    y={["registrations", "active_registrations"]}
    swapXY=true
    title="FARA registrations by country represented (top 25)"
/>

<DataTable data={by_country} search=true rows=15>
    <Column id=country />
    <Column id=registrations fmt="#,##0" />
    <Column id=active_registrations title="Active" fmt="#,##0" />
</DataTable>
