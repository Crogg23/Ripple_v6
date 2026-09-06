# Data holes that killed or dimmed the politics probes, and what closing each takes

2026-09-05. Scoped from the loaders in scripts/, the registry, and the probe results. No warehouse writes.
Effort = one person, loader plus load plus mart. Cost = warehouse credits; "no real number" where nothing comparable has run.

| # | hole | unlocks | source | loader today | size | effort | cost | risk |
|---|---|---|---|---|---|---|---|---|
| 1 | Senate trades stop 2020-12 | 78 91, plus any trade-vs-vote | efdsearch.senate.gov PTRs, HTML since 2012, PDF earlier; Senate Stock Watcher dataset is dead after 2020 | none; SENATE_STOCK_WATCHER was a one-shot GitHub pull | ~15k filings 2021-26, 1 row per trade line | 2-3 days: session cookie, paged search, HTML table parse; PDF filers dropped | no real number; tiny table | site blocks bots; ~20% of senators file paper PDFs |
| 2 | House trade lines are PDFs | 35 91 | clerk.house.gov PTR PDFs; House Stock Watcher dataset parsed them through 2023 | FD_PTR_INDEX exists, no lines | ~40k filings, ~250k lines | 3-5 days if OCR; 1 day if HouseStockWatcher JSON is taken as-is to 2023 | no real number | OCR error on tickers and amounts |
| 3 | FEC indiv is 2023-26 only | 32 87 89 92 94 backfill, any pre-2023 donor question | fec.gov bulk indivYY.zip, cycles 2000-2022 | scripts/fec_itcont_load.py, CYCLES dict hardcoded 2024/2026 | ~4-8 GB per cycle, 20-40M rows; 12 cycles ~350M rows | 1 day: extend CYCLES, run per cycle, dedupe SUB_ID | 2024+2026 load logged in git c19036ec; pull its price from query history before go | doubles landing size; needs the union mart rebuilt |
| 4 | FEC IE mart totals 20x high | 84 | same FEC bulk; rebuild the mart with amendment dedupe | scripts/fec_independent_expenditure_load.py exists | 350k rows | 0.5 day: dedupe on latest AMNDT per FILE_NUM+TRAN_ID | trivial | none |
| 5 | LDA missing 2011-2019 | 83, any lobby-vs-rule | lda.senate.gov API by filing_year, or bulk XML | scripts/senate_lda_load.py, --start-year flag | 1.1M filings | 0.5 day of crawl at 120 req/min with key; ~10 hours wall | trivial | rate limit; registrant names differ pre-2016 |
| 6 | Federal Register only 2023-26 | 83 | federalregister.gov API, docs since 1994 | loader exists for 2023+ | ~100k CMS docs | 0.5 day | trivial | none |
| 7 | HCRIS one vintage | E43 E47 E48 trends, hunch 11 | CMS HCRIS annual files FY2011-2023, ~60 MB each | one-vintage loader | 12 files, ~6k rows each | 1 day: loop years, add FY column, mart union | trivial | worksheet layout changed 2010 |
| 8 | No congressional district shapes | 34, any by-district map | Census TIGER GENZ cb_us_cd118_500k | scripts/census_boundaries_load.py, add one entry | 435 polygons | 1 hour | trivial | redistricting: pick 118th and 119th |
| 9 | Committee roster is current-only | 78 36 84 by year | unitedstates/congress-legislators committees-historical.yaml | scripts/congress_committee_membership_load.py, add the historical file | ~30k rows | 2 hours | trivial | none |
| 10 | Bills only 118th-119th | 91 | govinfo BILLSTATUS bulk, 113th-117th | loader exists for 118+ | ~50k bills, 400k cosponsors | 0.5 day | trivial | none |
| 11 | Revolving-door has no names | 90 | Revolving Door Project's people pages, or OpenSecrets revolving-door CSV | none | ~10k people | 1 day; OpenSecrets needs an API key and terms | trivial | licensing on OpenSecrets |
| 12 | 527 Schedule A/B not landed | 88 dollars | IRS POFD full file, same zip already used for 8871/8872 | scripts/irs527_load.py, add two record types | 17.9M rows | 0.5 day | no real number; itcont-sized | none |
| 13 | Sanctions have no US address | 37 | not fixable; FEC never carries DOB | n/a | n/a | dead | n/a | n/a |

## Order I'd do them

1. Cheap and unblocking today, one afternoon total: 4, 8, 9, 6, 7. Rebuild IE mart, district shapes, committee history, Federal Register back-years, HCRIS back-years. Every one has a loader.
2. One day each, big payoff: 3 FEC back-cycles, 12 527 dollars, 5 LDA gap.
3. The scrapers, 1 and 2: Senate PTR HTML crawl first. It is the only fix for every stock-trade hunch and nobody else's dataset covers 2021+.
4. Skip 11 and 13.

## Before any of it runs

Loads are warehouse writes. Each one gets a one-line price from the query log for the nearest prior load, then waits for "go", per CLAUDE.md. Item 3 is the only one with a comparable prior run to price.
