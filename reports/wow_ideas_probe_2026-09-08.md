# Preliminary investigation — all 15 wow ideas, 2026-09-08

Door used: the Python scripts, `connect/db.py`. Role ACCOUNTADMIN,
warehouse COMPUTE_WH, database LIBRARY_MARTS. The chat plug-in door
is still dead at 401 and was not used.

30 probes run. Every number below came back from a live query today.
Nothing here is quoted from the tool box without being re-checked.

---

## Verdicts

| # | idea | verdict | the number that decided it |
|---:|---|---|---|
| 2 | Never once looked at | **GO** | 2,929,890 of 3,135,554 facilities, zero inspections |
| 3 | The address that is 400 things | **GO** | 141,512 companies at one London street |
| 4 | Rename, record resets | **GO** | 9,504 mines changed controller, 1994-2026 |
| 7 | Regulator is the variable | **GO** | KY collects 61.1%, WI 85.7%, same law |
| 12 | Who moved first | **GO** | 283.72M contributions with sane dates |
| 13 | Smokestack to county | **GO** | ECHO FIPS_CODE, zero nulls, 3,233 counties |
| 9 | Complaint predicted the recall | **GO, upgraded** | NHTSA headers are real now, 1,761 makers |
| 5 | Redlined to branch closing | **GO, reshaped** | FDIC 32 years is the spine, not HMDA |
| 8 | The twin study | **GO, capped** | 6,628 of 14,700 fined, 3-year window |
| 6 | Round-number sweep | **GO, narrowed** | 17.8% of MSHA penalties end in 00 |
| 11 | Transparency theater | **GO, unproven** | one dead column confirmed, no sweep run |
| 1 | The lie ledger | **PIVOT** | only 648 EINs bridge OSHA to SEC |
| 14 | The ships that wait | **RESHAPE** | 8 days of data, not a time series |
| 15 | Offshore on the donor list | **PARK** | no key from GLEIF to FEC |
| 10 | Government heartbeat | **PARK** | TIMELINE is 405 views, a plumbing layer |

---

## What each probe actually ran

### 2 · Never once looked at — the strongest thing found today

```
ENVIRONMENT__FED_EPA_ECHO            3,135,554 facilities
  TOTAL_INSPECTION_COUNT = 0         2,929,890   93.4%
  DATE_LAST_INSPECTION is null       2,570,106   82.0%
  IS_ACTIVE                          1,637,810
  active AND major AND never seen        3,321

ENVIRONMENT__EPA_PENALTY_GAP            93,808 curated facilities
  NEVER_INSPECTED_NONCOMPLIANT           53,587   57.1%
  CHRONIC_NO_PENALTY                     49,622   52.9%
  PCT_MINORITY null                      29,702   31.7%
```

- Checked: a count of facilities whose inspection count is zero
- Hit means: the facility is registered and has never been visited
- Miss would mean: zero is a not-loaded placeholder, not a real zero
- Why it is a real zero: `TOTAL_INSPECTION_COUNT` has **no nulls at all**.
  The loader distinguishes null from zero everywhere else in this table,
  and 60,438 rows carry a null latitude. So zero is a value, not a gap.
- The 3,321 figure is the headline. Active, classed major, never inspected.
- Half the work is already done. `NEVER_INSPECTED_NONCOMPLIANT` is a
  built column on the penalty-gap mart, not something to derive.

Caveat that must be stated: ECHO's 3.1M includes small and dormant
registrants. The honest denominator is the 93,808 curated mart, where
the never-inspected-and-noncompliant share is 57.1%.

### 3 · The address that is four hundred things

```
UK_COMPANIES_HOUSE_PSC              15,804,611 rows
  addresses holding 50+ companies         16,666
  companies sitting at those           3,404,591

worst five addresses, by company count
  WC2H 9JQ  SHELTON STREET             141,512
  N1 7GU    WENLOCK ROAD               125,126
  EC1V 2NX  CITY ROAD                  102,645
  EC2A 4NE  PAUL STREET                 51,414
  WC1N 3AX  OLD GLOUCESTER STREET       39,196
```

- Checked: distinct company numbers per postcode plus address line
- Hit means: one door is the registered control address for many firms
- Miss means: these are formation agents, which is the boring answer
- Honest read: Shelton Street is a known company-formation address.
  The finding is not that it exists. The finding is the **shape** —
  16,666 doors hold 3.4M companies, so a fifth of the register sits
  at addresses that are mailboxes.
- US leg is dead. USASpending has exactly **one** ZIP with 100+
  distinct recipients, holding 2,019 of them. Drop the contractor leg.
- Correction to the tool box: PSC is 15.8M rows now, not the ~7M the
  trap log records. The stopped load was re-run at some point.

### 4 · Rename, and the record resets

```
LABOR__FED_MSHA_VIOLATIONS
  mines                31,277        controllers      19,430
  violators            43,275        span   1994-09-09 to 2026-07-18

controllers per mine        mines
  1                        21,623
  2                         6,358
  3                         2,091
  4                           658
  5                           245
  6+                          152
```

- Checked: distinct CONTROLLER_ID per MINE_ID across 3.09M violations
- Hit means: ~9,504 mines changed hands with the record still attached
- Miss means: controller id churns for filing reasons, not real sales
- The second signal nobody named yet: **43,275 violators against 19,430
  controllers.** More than twice as many operating entities as owners.
  That gap is where a rename would hide.
- The CMS leg stays dead. `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS`
  reads 'N' on all 14,700 rows, re-confirmed today. Build on MSHA only.

### 7 · The regulator is the variable

```
MSHA penalty collection rate, states with 20,000+ violations

  worst                          best
  KY   487,106 viols  61.1%      WI   35,756 viols  85.7%
  TN    44,374        61.7%      AZ   63,474        82.3%
  VA   155,314        66.0%      MN   58,743        82.3%
  WV   499,955        66.6%      IA   33,590        82.3%
  PA   163,019        67.0%      NM   36,531        81.9%
```

- Checked: amount paid over penalty proposed, grouped by mine state
- Hit means: where you are decides what enforcement actually costs
- Miss means: the spread tracks operator size or bankruptcy, not place
- A 24.6-point spread on one federal statute, on 1.4M violations in
  the states shown. The coal states sit at the bottom together, which
  is a pattern, not scatter.
- The OSHA version of this test came back flat. Deaths per million
  hours ran 0.01 to 0.02 across every state with 3,000+ establishments.
  No spread, no story. Drop the OSHA leg.

### 12 · Who moved first

```
FINANCE__FED_FEC_INDIV_CONTRIBUTIONS
  rows                      283,771,819
  dates in 1975-2026        283,720,211    99.98%
  before 1975                         9
  after 2026                         44
  null date                      51,555
  committees                     40,136
```

- Checked: date range and sanity on the full contribution file
- Hit means: a clean daily clock across the whole money side
- Miss means: dates are text-parsed junk and every window is wrong
- The min and max read 0031-04-10 and 9206-07-02, which looks like
  corruption until you count. It is 53 rows out of 283.8M.
- Correction to the tool box: this table is **283.8M rows now, not
  84.2M.** The 84.2M figure is the `__PREV_20260906` snapshot sitting
  beside it. Every count written against the old number is stale.

### 13 · Smokestack to county

```
ENVIRONMENT__FED_EPA_ECHO
  FIPS_CODE null                    0
  distinct counties             3,233
  null latitude                60,438
```

- Checked: county fill on the facility table before designing the hop
- Hit means: the county rollup needs no crosswalk at all
- Miss means: FIPS is sparse and the chain needs ZCTA in the middle
- Zero nulls on 3.1M rows. 3,233 counties against 3,222 in DIM_COUNTY,
  so there are 11 codes to reconcile before trusting a join.
- FIPS stays terminal. Aggregate at the county and stop, per the rules.

### 9 · The complaint that predicted the recall — upgraded

```
CONSUMER_SAFETY__FED_NHTSA_COMPLAINTS   2,227,941 rows
  distinct manufacturers                    1,761
  distinct makes                            2,117
  real column names   CMPLID, ODINO, MFR_NAME, MAKE, RIPPLE_*

CONSUMER_SAFETY__FED_NHTSA_RECALLS        241,861
CONSUMER_SAFETY__FED_NHTSA_INVESTIGATIONS 154,209

CONSUMER_PROTECTION__FED_CFPB_COMPLAINTS
  with narrative                        3,825,161
  distinct narrative text               2,572,889   67.3%
  span                        2015-03-19 to 2026-07-03
```

- Checked: whether NHTSA still has the headerless C1..C54 shape
- Hit means: complaint text can be joined to a later recall by maker
- Miss means: positional columns and the join has nothing to key on
- **The headerless trap is dead for this table.** It carries named
  columns now. Two more NHTSA tables exist alongside it, so the
  complaint-to-recall arc has both ends.
- CFPB templating is confirmed. A third of narratives are duplicates
  of another narrative. Any text model has to dedupe first.

### 5 · Redlined to branch closing — reshaped

```
FINANCE__FED_FDIC_SOD_BRANCH_DEPOSITS
  rows            2,822,977      span   1994 to 2025   32 years
  counties            3,236      null coordinates    226,932   8.0%

HOUSING__FED_CFPB_HMDA_HISTORIC
  span            2015 to 2017    only 3 years
  loan originated            23,121,222
  application denied          6,967,834
  preapproval denied            336,482
  withdrawn                   4,919,862
  null county code              821,865

HOUSING__FED_MAPPING_INEQUALITY   1,155 rows, 42 states
```

- Checked: the year span and outcome mix on each layer
- Hit means: a continuous line from a 1930s map to a 2020s closure
- Miss means: the layers do not overlap in time and the arc is fake
- **The originations-only trap is dead here.** This table holds 6.97M
  denials with race and income on the row. The reload worked.
- But the span is 2015-2017, not 2007-2017. Three years, not eleven.
- So the long arc has to be carried by FDIC branches, which run 32
  years across 3,236 counties. HMDA becomes a three-year detail panel
  inside it, not the spine.
- HOLC mart is still 1,155 rows against 10,154 in landing. Use landing.

### 8 · The twin study

```
HEALTH__FED_CMS_NURSING_HOME       14,700 facilities, 53 states
  ever fined                         6,628
  null staffing rating                 208
  null certified beds                    9
  blank chain name                   4,221

HEALTH__FED_CMS_NURSING_HOME_PENALTIES
  penalties      16,180      facilities penalised   6,831
  span           2023-06-17 to 2026-05-13
```

- Checked: whether matched pairs can actually be formed
- Hit means: a fined facility has a near-identical unfined twin
- Miss means: fined facilities differ systematically and no twin exists
- Matching covariates are effectively complete. 9 null bed counts out
  of 14,700 is nothing. 45% of facilities have been fined, so both
  arms are large.
- The cap is time. 2 years 11 months of penalties means short arms on
  both sides of the event. State any effect as within-window only.

### 6 · Round-number sweep — narrowed to one source

```
LABOR__FED_MSHA_VIOLATIONS
  violations with a penalty          3,019,763
  penalty ends in 00                   537,701    17.8%
  penalty ends in 000                   13,918     0.46%
  proposed                          $1,820.2M
  paid                              $1,271.7M     69.9%

HEALTH__FED_CMS_NURSING_HOME_PENALTIES
  fines with an amount                  13,710
  ends in 00                               276     2.0%
  ends in 000                               45     0.33%

LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  hours worked ends in 000              13,438     3.4%
  hours worked ends in 0000              2,650     0.66%
```

- Checked: share of dollar values landing on a round boundary
- Hit means: the number was chosen by a person, not computed
- Miss means: the agency's own formula produces round outputs anyway
- 17.8% on MSHA is roughly 18x what an unstructured amount would give.
- **This one needs its chain walked before it is a finding.** MSHA has
  a regular assessment formula and a special assessment path. If the
  formula emits round hundreds, 17.8% is the formula, not a negotiation.
  Split by assessment type before claiming anything.
- Nursing-home fines came back at 2.0%, which is the null result. That
  source does not bunch.

### 11 · Transparency theater — confirmed in the small, unproven at scale

- `PROVIDER_CHANGED_OWNERSHIP_IN_LAST_12_MONTHS` reads 'N' on all
  14,700 nursing homes. Re-confirmed today. A genuine dead column.
- The NPPES EIN trap has moved. That column **no longer exists** on
  `HEALTH__FED_CMS_NPPES` — the query failed on an invalid identifier.
  The trap log entry describes a table shape that is gone.
- No warehouse-wide sweep was run. That is the actual work, and it is
  a per-column scan across 676 marts. Do not quote a number until it
  has run.

### 1 · The lie ledger — pivot

```
LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  rows / establishments        398,620
  distinct EIN                 114,606
  blank EIN                     43,260    10.9%

FINANCE__FED_SEC_EDGAR_FINANCIALS
  rows                          55,635
  distinct EIN                   5,773      blank 0
  distinct CIK                   8,112

EIN overlap, normalised to 9 digits
  OSHA side                    114,534
  SEC side                       5,773
  matched                          648
```

- Checked: whether an EIN actually bridges the two filings
- Hit means: the same firm's numbers can be lined up across agencies
- Miss means: the two files barely share companies and it is anecdote
- The bridge is real but tiny. 648 companies. That is a named list a
  reporter can work, not a rate anyone can publish.
- The reason is the SEC side, not the key. `EDGAR_FINANCIALS` is a
  DERA extract with 8,112 filers, not all of EDGAR. A wider SEC source
  would widen this. That is a load question, not an idea question.
- **The pivot:** the contradiction inside OSHA alone is stronger.
  3,667 establishments report more than 4,000 hours per employee per
  year, which is over 76 hours a week for every worker, all year.
  196 more report zero employees and non-zero hours. Same form, same
  filer, numbers that cannot both be true.

### 14 · The ships that wait — reshape

```
MARITIME__FED_NOAA_AIS            58,104,610 positions
  span                 2024-01-01 to 2024-01-08     8 days
  distinct MMSI                         22,759
  distinct IMO                           6,630
  speed under 0.5 knots             43,735,926     75.3%
  null geography                             0
  latitude range              0.06 to 85.18
  longitude range          -174.26 to 147.34
```

- Checked: the date span before designing anything with a calendar
- Hit would mean: years of vessel history to find seasonal loitering
- Miss means: it is one week and no calendar question can be asked
- **It is one week.** Every seasonality, cadence, or before-and-after
  idea against this table is dead on arrival.
- What survives: 22,759 vessels, 58.1M positions, zero missing
  geography, and three quarters of all positions effectively stopped.
  That is a very dense one-week anchorage map, and it is global —
  the longitude range spans the Pacific both ways.

### 15 · Offshore on the donor list — park

```
ECONOMICS__INTL_GLEIF_RELATIONSHIPS
  IS_FUND-MANAGED_BY            149,428  active
  IS_ULTIMATELY_CONSOLIDATED_BY 132,558  active
  IS_DIRECTLY_CONSOLIDATED_BY   126,406  active
  IS_SUBFUND_OF                  73,179  active

FEC contributions with a non two-letter state code   203,283
```

- Checked: whether the ownership edges and the donor file share a key
- Hit would mean: donor money traceable to a foreign ultimate parent
- Miss means: the only path is name matching, which clears 8%
- There is no key. GLEIF speaks LEI, FEC speaks committee id and donor
  name. Nothing bridges them. The 203,283 odd-state contributions are
  a lead, not a link.
- Park until an LEI-to-employer bridge exists. Nobody has built one.

### 10 · Government heartbeat — park

```
LIBRARY_MARTS.TIMELINE
  views                405
  base tables           36
```

- Checked: what the TIMELINE schema is actually made of
- Hit would mean: 400+ sources already sharing one time axis
- Miss means: it is a view layer, so the axis is a query, not a fact
- The 403-sources figure is a view count. Views carry no row count and
  freeze their column list at create time.
- It is plumbing worth having. It is not a finding.

---

## Corrections to the tool box, found today

| what it says | what is true now |
|---|---|
| FEC contributions 84.2M rows | 283.8M — the 84.2M is the PREV snapshot |
| UK PSC ~7M rows, load stopped | 15,804,611 rows |
| NHTSA complaints are headerless C1..C54 | named columns, 1,761 manufacturers |
| HMDA historic is originations only | 6.97M denials present, but span is 2015-2017 |
| NPPES EIN column is empty | the column is gone entirely |
| AIS is a vessel time series | one week, 2024-01-01 to 2024-01-08 |

Still true, re-confirmed today:

- Nursing-home ownership-change column is 'N' on all 14,700 rows
- HOLC mart is 1,155 rows against 10,154 in landing
- ECHO PCT_MINORITY is null on 29,702 of 93,808 penalty-gap rows
- MSHA collects 69.9% of what it proposes, $1.82B against $1.27B

---

## Cost

30 aggregate queries on COMPUTE_WH. Total query time under 30 seconds
across all three batches. No table was written, dropped or altered.
