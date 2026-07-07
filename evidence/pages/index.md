---
title: The Library
---

```sql totals
select
    count(*) as datasets,
    count(distinct shelf) as shelves,
    sum(row_count) as total_rows
from library.catalog
```

```sql shelves
select
    shelf,
    count(*) as datasets,
    sum(row_count) as rows
from library.catalog
group by shelf
order by rows desc
```

```sql catalog
select shelf, dataset, what_it_is, row_count, status
from library.catalog
order by shelf, dataset
```

The reading room of the Ripple Library — every dataset below is live in Snowflake,
landed and cataloged by the onboarding agent. This site reads the curated
`THE_LIBRARY` views. Pick a shelf, or search the card catalog.

<BigValue data={totals} value=datasets title="Datasets on the shelves" />
<BigValue data={totals} value=shelves title="Topic shelves" />
<BigValue data={totals} value=total_rows title="Rows across the reading room" fmt="#,##0" />

## First exhibits

A handful of datasets, straight off the shelves:

- [The national debt, daily since 2001](/national-debt) — Treasury's Debt to the Penny
- [Banned healthcare providers](/banned-providers) — the OIG exclusion list (LEIE)
- [Gun background checks](/gun-checks) — FBI NICS, monthly since 1998
- [Fatal police shootings](/fatal-force) — Washington Post Fatal Force database
- [Foreign agents](/foreign-agents) — FARA registrations by country represented
- [The Supreme Court](/scotus) — every case and vote since 1946 (SCDB)

## Shelves by volume

<BarChart
    data={shelves}
    x=shelf
    y=rows
    swapXY=true
    title="Rows per shelf"
    fmt="#,##0"
/>

## The card catalog

Every dataset in the reading room. `status = curated` means a typed, cleaned mart
sits behind the view; `raw` means the view still reads the as-landed text table
(numbers and dates in raw views need casting — the typed layer is being built out).

<DataTable data={catalog} search=true rows=25>
    <Column id=shelf />
    <Column id=dataset />
    <Column id=what_it_is title="What it is" />
    <Column id=row_count fmt="#,##0" />
    <Column id=status />
</DataTable>
