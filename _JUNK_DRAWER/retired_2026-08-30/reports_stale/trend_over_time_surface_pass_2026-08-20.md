# Trending over time — a full surface pass

*2026-08-20. Built from the Aug-17 census fill plus a fresh column-name sweep.
No warehouse compute. Per-table verdicts: `trendability_inventory_2026-08-20.csv`.*

## The clock census (589 shelf tables)

| verdict | tables | meaning |
|---|---:|---|
| CLEAN | 164 | real event dates, sane range, >1yr span — trend these today |
| UNMEASURED_CLOCK | 143 | a real time column exists but the census never measured it (stored as TEXT/year/quarter) |
| CORRUPT_RANGE | 89 | dates present but poisoned (year 0001, year 9999, 2000-yr spans) — floor/ceiling filter or repair |
| LOAD_DATE_ONLY | 73 | the only "date" is when we loaded it — a fake clock |
| NO_CLOCK | 108 | no time column at all — snapshots only |
| SHORT_SPAN | 12 | real dates, under a year |

- 164 clean tables = **345.5M rows**; 134 of them run into 2026.
- 125 clean tables carry a **10-year-or-longer** span (281.3M rows).
- The 143 unmeasured clocks hold **229M rows** and include pharma payments to
  doctors, all federal grants and contracts, all drug adverse-event reports,
  fracking disclosures, quarterly water compliance, storm events, and 80 years
  of UN votes.

## The eight trend shapes (the vocabulary, not just "count per year")

1. **by_time** — how many per year/month
2. **first_last** — earliest and latest (where does the record actually start)
3. **gaps** — missing periods (a reporting outage is itself a finding)
4. **seasonality** — by month / day-of-week
5. **births** — new ones per period (first seen)
6. **deaths** — disappeared per period (last seen)
7. **age_distribution** — how old the living ones are
8. **mix_over_time** — the category mix shifting (the most under-used shape)

## Surface pass by family — the trend list

### Enforcement & violations
- Mine safety violations — 3.1M, 1994-2026 (32y) — per year; type mix over time; seasonality.
- Drinking-water violations w/ enforcement — 15.4M, 1900-2028 — per year; violation-type mix; the enforcement columns sit on the same row, so "share drawing enforcement over time" is surface.
- Water-discharge violations — 397k + 305k, 50-52y, two violation types — per year, per type.
- Nursing-home deficiencies — 418k health + 200k fire, 24y / 11y — per year; severity-scope mix over time.
- Air formal actions 106k (54y) and informal actions 176k (corrupt floor) — actions per year.
- EPA penalty-gap screen — 93.8k, 122y — flagged facilities per year.
- IRS auto-revocations — 1.2M, 16y — nonprofits stripped per month; batch seasonality.
- Federal contractor exclusions — 168k, far-future trap — debarments per year; exclusion length over time.
- Hazardous-waste violations/enforcement — 708k/383k, year-0001-to-9999 — repair first.

### Harm & safety events
- Consumer-finance complaints — 17.2M, 2011-2026 (15.6y) — per month; product mix; company-response mix; seasonality. Cleanest big harm series we own.
- Pollution/spill calls — 1.03M, 36.6y — per year; material mix; seasonality.
- Mine accidents — 274k, 26.6y — per year; severity mix.
- Rail: casualties 1.15M (29.6y), crossing incidents 251k (51.6y), equipment accidents 225k (51.6y) — three clean half-century series.
- Aviation accidents — 31k events (18.6y) + 179k injury rows — per year; severity mix.
- Fatal police encounters — 10.4k, 2015-2024, complete decade — per month; seasonality.
- Drug adverse events — 37M — clock unmeasured (event date + source quarter). Measure it.
- Device adverse events — 2.7M, needs a year floor — per year.
- ER product injuries — 9.8M — far-future poisoned. Repair.
- Malpractice/disciplinary reports — 1.9M — four year-columns, none measured. Measure it.
- Vehicle safety complaints — 2.2M — corrupt range. Repair.

### Money
- Opioid pill shipments — 178.6M, 2006-2026 (20.6y), clean — the best trend asset we own. Pills per month; drug mix over time; seasonality; the rise and the fall.
- Individual campaign contributions — 84M, floor 2000, corrupt tail — per cycle; size distribution over time; round-number rate over time.
- NYC campaign contributions — four clean cycle tables, 12-15y each.
- Treasury daily deposits — 478k, 20.8y — daily government cash in; tax-day seasonality is the whole point.
- Treasury interest rates 25.4y / debt-to-penny 33.2y / debt outstanding 235.7y.
- SBA loans — 2.17M, 41.2y — per year; loan size over time. PPP is a separate 4.5y bubble (968k).
- Bank branch deposits — 2.8M, epoch trap on 26k rows — deposits per year.
- Google political ad spend — 299k weekly rows, 8.2y — spend per week; advertiser churn.
- Texas lobbying spend on officials — 38.7k, 26.5y — plus gifts/food/events/entertainment/awards, 21-22y each — spend per year; category mix.
- CFTC futures positions — 287k, 40.6y weekly.
- Pharma payments to doctors — 43M — clock unmeasured. Highest-value measure on the board.
- Federal contracts 20M / assistance 19.9M — epoch-poisoned and unmeasured. Repair.

### Courts & justice
- Federal case outcomes — bankruptcy 7.0M (103y), criminal 6.3M (126y), appellate 988k (126y), civil 10.9M (corrupt tail) — filings per year; case-type mix; disposition mix. A multi-decade backbone.
- Court dockets — 71.7M, 1697-2026 — dockets per year; per court over time (court is on the row).
- Supreme Court justice votes — 83.6k, 80.7y — votes per term; direction mix over time.
- FBI crime data — 238.7k, 41.6y.
- Immigration detention stints — 2.57M, 107.6y — stints per year; length of stay over time; facility mix.
- Foreign labor certifications — 664.6k, 2012-2023 — per year; employer mix.
- Case citations — 18.1M but the only date is ingest. No clock.
- Immigration court cases — 12.6M, four columns, no date at all.
- Judge financial disclosures — epoch-poisoned. Repair.

### Organizations — births, deaths, age (the most under-used shape we own)
- UK companies — 5.7M with incorporation dates to 1327 — company births per year; dissolutions; age distribution of the living.
- UK people with significant control — 7M, to 2026 — control registrations per year.
- Irish companies — 821.7k, 280y.
- IRS exempt-org master file — 2.0M, ruling dates, 126y — nonprofit births per year.
- IRS revocations — 1.2M, 16y — nonprofit deaths per year.
- Dark-money 527 orgs — 77.6k, floor 1808 — registrations per year; cycle spikes.
- Failed banks — 3,584, 56.4y — failures per year; the 2008-2010 spike.
- Global legal-entity relationships — 484k, 127y — parent links registered per year.
- Credit-union charter/merger events — 53 rows, tiny but clean.
- Research org registry — 135.7k, 7.7y.

### Facilities & infrastructure lifecycle
- Drinking-water systems 434k + facilities 1.55M + site visits 2.5M (~126y) — activations/deactivations per year; visits per year.
- EPA facility registry 5.3M and compliance snapshot 3.1M — corrupt floors; facilities registered per year after flooring.
- Mines — 91.9k, 101.6y — openings and closures per year; status mix. The coal decline is directly visible.
- Air-quality monitoring sites — 20.9k, 69.9y — monitors online per year (measurement capacity as its own trend).
- Dams — 92.8k, completion years 1901+ — dams built per year.
- Superfund boundaries — 2,114, 22.8y.
- Orphaned oil & gas wells — 117.7k, 3.4y only.
- Power plants, generators, hospitals, nursing homes, health centers — load-date only. Real operating dates likely exist in unmeasured columns.

### People & careers
- Federal judges — 4,067 judges / 4,766 service rows, 1789-2026 (237y) — appointments per year; by appointing president; tenure length over time; age at appointment.
- Judge political affiliations — 8,486, 224y — party mix of the bench over time.
- 527 directors/officers 189.6k and SEC insider owners 1.9M — load-date only.

### Filings & registrations
- Foreign-agent registrations — 48.1k, 84.5y — registrations per year; country mix over time. Clean and interesting.
- Federal Register documents — 94.7k, 22.2y — rules published per year; agency mix. The regulatory-volume series.
- SEC filing index — 48.9k, 31.1y — filings per year.
- SEC insider transactions — 2.7M + 1.0M — corrupt spans; floor then trades per month; insider selling waves.
- 13F filers — 344k, 14.6y — new institutional filers per quarter.
- Single audits of federal money — 411.6k, 24.1y — audits per year; findings rate over time.
- Union annual reports — 617.7k, epoch trap on 589k rows — repair unlocks the union-decline series.
- Pension filings + actuarial schedules — 33.5k / 41.8k, corrupt. Repair.
- Federal lobbying filings — 174.9k but only 2020-2021 (known 9% load). Not trendable until refilled.
- California lobbying 524.8k / Texas lobbying 283.8k — corrupt tails, floor-filter first.
- IRS 990 e-file index — 5.5M, 50y span but 3.2M epoch rows and stops 2020.

### Products & recalls
- Device clearances — 175.7k, 1976-2026 (50.2y) — clearances per year. The device-approval curve, clean.
- Device approvals (PMA) — 56.9k, 126y span.
- Recalls — device 39.6k (95.6y), drug 17.8k (20.4y), vehicle 243k (corrupt tail) — per year; class mix over time.
- Retracted papers — 71.6k, floor 1753 — retractions per year; the reproducibility curve. Two independent copies to cross-check.
- Unique device IDs — 5.1M, 13.5y — devices registered per year.
- Drug pricing — 359.5k, 2.1y weekly.

### Measurements & statistical series
- Lead/copper water samples — 927.4k, 42.5y — samples per year; exceedance rate over time.
- Earthquakes — 443.3k, 13.3y — per year (detection capacity as much as seismicity).
- Health-shortage designations — 165.5k areas + 79.2k scores, 56.5y — designations per year.
- Electricity generation mix — 369.3k, 2000-2025 — fuel mix by country over time.
- CDC anxiety/depression + health insurance — 2020-2024 weekly pandemic series.
- Air emissions 10.4M, stream gauge 6.7M, storm events 1.78M, UN votes 1.82M — all have real time columns, none measured. Cheap wins.
- Slave voyages — 36.1k + 11.5k — voyages per year over centuries.

### Codes & taxonomy (the sleeper)
- Species taxonomy — 993k units + 11 sibling tables, all ~30y — new species described per year; name churn; synonym rate over time.
- Known-exploited vulnerabilities — 1,631, 4.7y — added per week.
- Market identifier codes — 2,864, 23.3y — exchanges registered and retired per year.

### Places
- Geographic names — 1.25M, 1700-2026 — place names recorded per year.
- Flood-program communities — 25.1k, 99.7y — communities joining per year.
- Water service and geographic areas — 578k + 422k, 30.9y.
- Watersheds 2,456 (14.2y); rural housing projects 13.6k (164y, far-future trap).

### Sanctions & screening
- Designations per year across five regimes: consolidated screening 25.9k (81.6y), EU 42.3k (101y), UK 33.8k (26.3y), UN 1,011 (26.3y), OpenSanctions 71k (ends 2022).
- Prop 65 chemical listings — 952, 39.4y — chemicals listed per year.

## The parking lot (branches parked during this pass, by vote count)

| votes | branch | why parked |
|---:|---|---|
| ~40 | rate per noun over time (violations per facility, complaints per company) | needs the noun table alongside the event table |
| ~30 | is the trend real, or did the counting change? | needs a denominator series (inspections, monitors, filers) |
| ~25 | trend by owner/parent, not by site | needs the entity spine |
| ~20 | before/after an enforcement action | needs two event tables aligned on one actor |
| ~12 | births minus deaths (net formation) | births and deaths live in separate tables |
| ~10 | same event across sources (sanctions across 5 regimes) | needs a crosswalk |
| ~8 | did the trend break when the law changed | needs a policy calendar we do not hold |

## Caveats (capped, at the end)

Every count-per-year line above measures reporting as much as reality; the
denominator question is parked, not solved. Corrupt-range tables need a floor
and ceiling filter before any chart is believable. Nothing here has been
queried — these are shapes the metadata says exist.
