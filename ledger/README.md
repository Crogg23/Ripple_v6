# The ledger

A checklist of every place a story could hide in `LIBRARY_MARTS`, one row per question, with a status.
Goal: shave the whole warehouse, layer by layer, and prove nothing got skipped.

Open `ledger.html` in a browser. That's the working view.

## The seven layers

| Layer | One row per | What it catches | Example shape |
|---|---|---|---|
| 1 singles | mart table | top earners, worst actors, outliers, group gaps, bunching under thresholds, spikes | one doctor billing 10x peers |
| 2 pairs | two tables sharing an entity ID | does it land, gap between matched and not; siblings give year over year | barred firm still paid |
| 3 hops | two tables with different IDs, linked by a crosswalk carrying both | the same, one step further | hospital officer pay to cost report |
| 4 place | table with county, ZIP, state, country or map points; county pairs; point-near-point pairs | where it's worst, what moves with it, what sits near what | pill counties are now death counties |
| 5 names | table with names or addresses | who repeats, shared addresses, which ID table to bridge to | fifty firms at one P.O. box |
| 6 time | table with an event date | before and after the ban, fine, crash or sale | fined, then kept winning contracts |
| 7 chains | path of four or more tables | grown by hand from live rows | mine violations to CEO to super PAC |

Every question carries the chart that would tell it: ranked bar, share curve, choropleth, decile staircase, before-after line, network and so on.
`findings.tsv` is the "what was found" section. Every finding names its chart and links back to its rows.

## Status words

untouched, claimed, probed, live, finding, dead, skip. A dead or skip row always carries a note saying why.
Rows marked skip by `build` are auto-skips: a key label that means different things on each side, or a key a known trap proves empty, like the NPPES EIN column. They're shown apart and never count as progress.

## Commands, from the repo root

```
python scripts/ledger.py status                          coverage per layer
python scripts/ledger.py next all 20                     best 20 untouched rows across every layer
python scripts/ledger.py next place 20 --tag decile      filter by tag or chart word
python scripts/ledger.py next all 20 --claim agent1      reserve rows for one parallel agent
python scripts/ledger.py mark ID live "what you saw"
python scripts/ledger.py found pairs B "headline as a fact" --rows ID,ID --chart "paired bars" --sql path
python scripts/ledger.py chain "A -> B -> C -> D" "what to look for" --from F-003
python scripts/ledger.py build                           after the catalog changes; keeps every status
```

`mark` takes a full ID or any piece of one that matches a single row.
Every write takes a lock, so parallel agents never overwrite each other.
The page rebuilds itself after every mark, found, chain or claim.

## What it is not

- Score is sort order only. Money, harm, officials, people and group gaps float up. Nothing is hidden by it.
- "Look for" and "where" are generated from column names. They're hints. Count a column's values before you build on it.
- Category codes like SIC, NAICS, drug name, HCPCS and CFDA are not pair keys. They group rows; they don't identify a thing. The page lists the count.
- The state-level panel isn't enumerated pair by pair: 200+ state tables would make about 20,000 rows. County pairs and point-near-point pairs are enumerated.
