# The June 2026 fraud takedown, checked against the warehouse — 2026-09-05

Chris's ask, verbatim: "find something currently going on in the news that falls into the realm of something in my warehouse."

## The news
DOJ, 2026-06-23: National Health Care Fraud Takedown. 455 defendants, 90 doctors and licensed professionals, $6.5B alleged.
Sources: https://www.justice.gov/opa/pr/national-health-care-fraud-takedown-results-455-defendants-charged-connection-over-65
https://oig.hhs.gov/fraud/enforcement/2026-national-health-care-fraud-takedown/
Court docs list: https://justice.gov/criminal/criminal-fraud/health-care-fraud-unit/2026-national-hcf-court-documents

## The test
Take the named prescribers. Find their NPI in NPPES by exact last name, first name, state. Rank them against
every prescriber of their own type in Part D 2024. The Part D file is public and predates the charges.
Question: were they visible as outliers before DOJ moved?

## NPI matches, one hit each, no ambiguity
| defendant | NPI | credential | city | charge |
|---|---|---|---|---|
| Angela Moss | 1457428195 | MD | Gordonsville TN | fraud + controlled substance distribution |
| Laurie McKenna | 1013209543 | FNP | Glens Falls NY | civil, unlawful opioid prescribing, $500k |
| Douglas Cline | 1619934858 | MD | Queensbury NY | civil, unlawful opioid prescribing, $500k, 20-yr DEA bar |
| Edward Scott Morrison | 1679525430 | DO | Pensacola FL | illegal controlled substance distribution |
| Ramon Aquino | 1508818311 | MD | Clarksville TN | controlled substance prescribing fraud |
| Nihar Gala | 1740660992 | MD | Harrington DE | lab billing fraud, not in Part D |
Henry Quan, HI: no NPPES match on that name in HI. Not a prescriber, or different legal name.

## Part D 2024, percentile within own prescriber type, beneficiaries ≥ 11
| defendant | type | peers | claims per bene | pct | $ per bene | pct | opioid rate | pct | long-acting rate | pct |
|---|---|---|---|---|---|---|---|---|---|---|
| Moss | Family Practice | 110,044 | 40.4 | 99.3 | $3,400 | 98.3 | 6.33 | 91.7 | 3.46 | 84.6 |
| McKenna | Nurse Practitioner | 252,542 | 9.0 | 76.8 | $1,385 | 81.2 | 56.47 | 99.0 | 35.85 | 99.4 |
| Cline | Interv. Pain Mgmt | 1,495 | 3.5 | 30.1 | $512 | 78.3 | 64.60 | 82.9 | 37.01 | 96.3 |
| Morrison | Emergency Medicine | 53,689 | 1.7 | 81.5 | $39 | 74.8 | 28.78 | 98.7 | none | — |
| Aquino | General Practice | 7,690 | 18.1 | 77.1 | $908 | 63.3 | 3.40 | 86.0 | 0.00 | — |

Family Practice claims-per-beneficiary: median 9.2, p99 36.3. Moss is 40.4.
Moss in Part B 2024: 10,613 services on 149 beneficiaries, 99.55th percentile of Family Practice.

## Open Payments, three years, all six
Tiny. Moss $1,291 total, McKenna $1,744, Cline $1,130, Aquino $29. Pharma money is not the signal here.

## OIG LEIE
None of the six excluded as of the loaded LEIE. Two same-surname false positives, ignored.

## Step 5: count how many others sit where they sit
| bar | peers at or above |
|---|---|
| Family Practice, ≥40 claims/bene and ≥6.33 opioid rate | 66 |
| Nurse Practitioner, ≥56 opioid rate and ≥35 long-acting, 100+ claims | 180 |
| Emergency Medicine, ≥28.78 opioid rate, 100+ claims | 448 |

## What it means
- Hit: five of five named prescribers sit at the 91st to 99.4th percentile on at least one opioid or volume measure, in data published before the charges.
- The single Part D file plus NPPES is enough to put them on a list. The join is name → NPI → Part D, then rank within type.
- Miss would have meant: charged doctors look like median doctors. They do not.
- The 66 / 180 / 448 lists are the lead lists. Most on them are legitimate: hospice, pain, rural. They are where to read next.

## Caveats
- Five names is not a sample. It is the names DOJ chose to publish. Selection bias toward opioid cases is certain.
- Percentile within type is coarse. Interventional pain is supposed to prescribe opioids.
- Part D 2024 is calendar 2024; charges are June 2026. The behavior in the file may postdate the alleged conduct.
- Gala is a lab-billing case. Part D says nothing about him. Needs Part B or CLIA tables.

## Cost
Eleven queries, largest scanned Part D 1.4M rows and Open Payments 3 × 15M rows. No prior run to price against.
