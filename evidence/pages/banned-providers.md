---
title: Banned Healthcare Providers
---

```sql by_year
select * from library.banned_providers
```

```sql total
select sum(exclusions) as total from library.banned_providers
```

The HHS Office of Inspector General's **List of Excluded Individuals and Entities
(LEIE)** — providers banned from federal healthcare programs. Source:
`fed_hhs_oig_leie` (raw view; exclusion dates cast from `YYYYMMDD` text at
extraction).

<BigValue data={total} value=total title="Exclusions on the list" fmt="#,##0" />

<BarChart
    data={by_year}
    x=excl_year
    y=exclusions
    series=provider_kind
    title="Exclusions by year, individuals vs businesses"
    type=stacked
/>

This list is one leg of the Library's flagship join: LEIE × Open Payments on NPI
finds excluded providers who still took pharma money — a hard-ID match, not a
name guess. That join lives in the connect layer and will get its own page once
the graph rebuild lands.
