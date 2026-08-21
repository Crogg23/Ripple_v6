---
title: Ripple — pick anything, see it over time
---

```sql datasets
select
    s.ripple_source,
    s.ripple_grain,
    s.ripple_clock,
    s.years,
    s.n_rows,
    s.first_day,
    s.last_day,
    coalesce(c.short_name, s.ripple_source)                       as name,
    coalesce(c.subject, '')                                       as subject,
    coalesce(c.dataset, '')                                       as what_it_is,
    coalesce(c.date_means, '')                                    as what_the_date_means,
    coalesce(c.precision, '')                                     as how_precise
from ripple.timeline_sources s
left join (
    select
        "table"                 as tbl,
        any_value(short_name)   as short_name,
        any_value(subject)      as subject,
        any_value(dataset)      as dataset,
        any_value(date_means)   as date_means,
        any_value(precision)    as precision
    from catalog.series
    group by 1
) c on c.tbl = s.ripple_source
order by s.n_rows desc
```

<Dropdown
  data={datasets}
  name=pick
  value=ripple_source
  label=name
  title="Dataset"
  defaultValue="CONSUMER_PROTECTION.CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS"
/>

```sql picked
select * from ${datasets} where ripple_source = '${inputs.pick.value}'
```

```sql series
select
    month,
    n_rows as records
from ripple.timeline_monthly
where ripple_source = '${inputs.pick.value}'
order by month
```

## <Value data={picked} column=name />

<Value data={picked} column=what_it_is />

<LineChart
  data={series}
  x=month
  y=records
  yAxisTitle="records per month"
  yFmt=num0
  title="How many, month by month"
/>

<Grid cols=3>
  <BigValue data={picked} value=n_rows fmt=num0 title="Records on the timeline" />
  <BigValue data={picked} value=years fmt=num0 title="Years covered" />
  <BigValue data={picked} value=how_precise title="Precision" />
</Grid>

**What the date on this one actually means:** <Value data={picked} column=what_the_date_means />

<Alert status=warning>
This counts records, not events in the world. A line going up can mean the thing
happened more, or that more of it got written down. If the dataset says its
precision is "year", every record lands on 1 January — the shape is real, the
day is not.
</Alert>

<Details title="Where this comes from, and how to add your own chart">

The numbers come straight out of the warehouse's shared timeline — one row per
dataset per day, already counted, so no chart here ever scans the raw hundreds of
millions of rows.

To make your own page: copy this file, change the query, save. The dev server
reloads on its own. To pull fresh numbers from the warehouse, run `npm run sources`.

</Details>
