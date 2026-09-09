# Tool Box hunt — 2026-09-08

Live recon against the warehouse, Python door, `connect/db.py`.
Role ACCOUNTADMIN, warehouse DBT_WH. Read-only, SELECT only.

Five hunts in the end. Four kept as findings, one killed at the wire,
plus a pile of clean misses. Hunts 1 to 4 came from the Tool Box by hand;
hunt 5 came out of the machine sweep and did not survive.
Every number below came from a query run this session. Queries at the bottom.

**This file has been through a skeptic pass and rewritten.** The skeptic
returned DISAGREE. Findings 1, 3, 4 and 5 survived; finding 2's two
headline numbers were artifacts and are struck, with the struck version
kept visible in that section. Every counter-claim the skeptic made was
re-run against the warehouse before being accepted. The scoreboard is at
the very bottom.

---

## What was hunted

| # | Move | Lens | Subject | Verdict |
|---|---|---|---|---|
| 1 | Verb 4, the impossible zero | Poisson / duplicate near-miss | LABOR, OSHA 300A | trap found, hypothesis dead |
| 2 | Verb 18, every line in the sand | Round-number clustering | ECONOMICS, SBA PPP | finding, cut down by the skeptic |
| 3 | Verb 17, warehouse contradicts itself | Provenance skepticism | ENVIRONMENT, EPA FRS | finding |
| 4 | Verb 5, one EIN two agencies | External baseline | LABOR x ECONOMICS | finding, evidence swapped |

---

# Finding 1 — one employer, hundreds of rows, the same hours on every one

**Subject area: LABOR. Tables: `LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023`,
`_2024`, `_2025`.**

## The chain

**What was checked.**
Every US employer who files an OSHA 300A injury summary reports two things
side by side: total hours worked, and whether anyone got hurt. A workplace
with a thousand full-time people works two million hours a year. Reporting
zero recordable injuries across two million hours is a claim, not a number.
So: band every establishment by hours worked, and ask what share of each
band ticked the zero box.

**The first answer, 2024, 398,620 rows.**

```
BAND                 ESTABLISHMENTS   REPORTED ZERO   PCT
under 25 FTE               126,310          87,009   68.9
25-100 FTE                 143,218          44,636   31.2
100-250 FTE                 53,431           6,087   11.4
250-500 FTE                 17,264           1,403    8.1
500-1000 FTE                 6,912             741   10.7   <- turns back up
1000-2500 FTE                3,413             313    9.2
2500+ FTE                    1,261             146   11.6
```

The rate falls the way it should, then stops at 250 FTE and climbs again.
It repeated in all three filing years: 2023, 2024, 2025, same shape.

**Then the sector split at 1,000+ FTE broke it open.**
NAICS 23, construction, came in at 30.4% zero. NAICS 33, manufacturing,
came in at 3.0%. NAICS 49, warehousing and couriers, came in at 0.0% on
311 establishments. Construction is not ten times safer than a warehouse.

**Pulling the actual construction rows named the mechanic.**

```
ESTABLISHMENT_NAME                                    HOURS       EMPLOYEES
California Department of Transportation Facility 982  11,190,000      5,595
California Department of Transportation Facility 485  11,190,000      5,595
California Department of Transportation Facility 4    11,190,000      5,595
California Department of Transportation Facility 570  11,190,000      5,595
... 470 Caltrans rows in the 2024 file, 14 distinct hour values between them
```

Caltrans files one row per facility and stamps the whole district's hours
and headcount on every single one. The hours column is not the
establishment's hours. It is the district's, copied down the page.

**Two more things fell out of that.**

`COMPANY_NAME` on those rows holds the string `Facility 982`, not the
company. The employer's name lives only inside `ESTABLISHMENT_NAME`.
A dedupe keyed on `COMPANY_NAME` does nothing here.

`TOTAL_HOURS_WORKED` has a junk tail: 117 rows in 2024 exceed 100 million
hours, which would be 50,000 full-time people at one address. Hours divided
by employees has a plausible median of 1,780 and 88% of rows land between
800 and 3,000, so the column is real with garbage on the end.

**Sizing the copy-paste block.**
Group every row at 250+ FTE by its exact hours, employees, state and NAICS
tuple. Rows that are alone in their tuple are real filings. Rows sitting in
a block of identical tuples are one employer's page repeated.

```
TUPLE BLOCK SIZE     GROUPS   ROWS   ZERO FILINGS   PCT ZERO
1, unique            26,403  26,403        1,781       6.7
2-4                     595   1,232          129      10.5
5-20                     36     361          178      49.3
21-100                   20     735          421      57.3
100+                      1     119           94      79.0
```

Ten to one. 2,447 rows out of 28,850 sit in duplicate blocks, and they
carry 822 of the 2,603 zero filings at that size.

**The biggest blocks, named.**

```
NAICS   STATE   HOURS       EMP     ROWS   ZERO   EXAMPLE NAME
812930  CA      1,565,272     897    119     94   0000 CORPORATE
237310  CA      5,196,000   2,598     79     37   Caltrans Facility 1
237310  CA      6,008,000   3,004     70     47   Caltrans Facility 100
924120  CA      6,616,000   3,308     45      0   Head Quarters - Sacramento NRA
622110  NY      2,129,994   1,176     44     41   CMH Lafayette Family Care
624110  NY      2,574,078   1,643     43     38   Bronx Career and College Prep
622110  TN     10,580,031   6,743     40     19   Allergy Clinic
711510  FL      1,354,329     868     30     17   Amway Center
531311  TX        530,724     255     30     21   Albion Apartments
```

**Now strip them and re-run, three years pooled.**

```
BAND                 CLEAN ROWS   ZERO     PCT    RECORDABLES PER 100 FTE
under 25 FTE            357,310  241,835  67.7                       7.67
25-100 FTE              415,986  129,601  31.2                       7.27
100-250 FTE             150,742   17,329  11.5                       6.45
250-500 FTE              49,235    3,723   7.6                       6.06
500-1000 FTE             18,365    1,204   6.6                       5.13
1000-2500 FTE             8,755      370   4.2                       5.61
2500+ FTE                 2,875       70   2.4                       3.50
```

The turn-up is gone. The curve falls straight from 67.7% to 2.4%.
Construction at 2,500+ FTE drops from 30.4% to 2.8% once the Caltrans
block is out, and manufacturing sits at 0.2%, one establishment in 498.
The 70 survivors at 2,500+ FTE concentrate in office sectors: NAICS 52
finance at 25.0%, NAICS 55 holding companies at 14.3%, NAICS 51
information at 17.1%.

## What a hit meant
Big employers systematically under-report injuries, and the tell is a
zero-injury rate that stops falling as the workplace grows.

## What the miss means
That is not what is in the file. The whole turn-up was multi-site
employers repeating one page. Once they are stripped, injury reporting
behaves the way a Poisson process should: the bigger the workplace, the
rarer a true zero. The residual big-employer zeros sit in banks, holding
companies and insurance offices, which is where a real zero is plausible.

**This is a miss on the zero-flag test and a hit on the pipeline.**

**One thing the zero-flag test hid.** Look at the last column of the clean
table above. Recordables per 100 FTE fall 7.67, 7.27, 6.45, 6.06, 5.13,
5.61, 3.50 across the same bands, after the dedupe. The biggest employers
report roughly half the injury rate of the smallest. That gradient is the
version of "big employers report fewer injuries" that survived, and this
hunt did not test it. Real safety programmes and real under-reporting both
predict it, and nothing here separates them. Parked, not resolved.

## Trap risk
No prior trap-log entry covers OSHA ITA 300A. Two new ones belong in
`.claude/traps.md`, written below.

---

# Finding 2 — the $10,000 rounding survives every control the lender explains away

**Subject area: ECONOMICS. Table:
`LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS`, 968,524 rows,
968,524 distinct `LOANNUMBER`.**

> **Rewritten after the skeptic pass.** The first version of this finding
> claimed round numbers ran 116 to 2,210 times chance, and that the biggest
> loans were the roundest. Both were wrong and both are struck. What follows
> is the smaller finding that survived. The struck version is at the bottom
> of this section so the error is on the record.

## The chain

**What was checked.**
A PPP loan was not a number anyone chose. The rule was two and a half times
average monthly payroll, computed to the dollar. Payroll is messy. So a loan
landing on an exact round number means the payroll figure was worked
backwards from the loan, not forwards from the books.

Count exact multiples of 100, 1,000 and 10,000 among first-draw loans.

**The raw numbers, 673,227 first-draw loans at 150,000 dollars and up.**

```
MULTIPLE OF        SHARE OF LOANS
$10                    61.245%
$100                   52.348%
$1,000                 11.642%
$10,000                 3.860%
```

Half of every first-draw PPP loan in the country is an exact multiple of
one hundred dollars. That looked like the headline. It is not.

**Red team one, and it kills the $100 number.**
Split the 205 lenders with 500 or more loans by how often they round.

```
                                          MIN     P10   MEDIAN     P90    MAX
share of loans that are multiples of $100  1.2%   9.2%   66.7%   98.6%  100.0%
```

53 of 205 big lenders sit under 25%. Some sit at 100.0%. That is not
borrower behaviour, that is a bank's loan system rounding its own
disbursements. Whether a PPP loan ends in "00" depends mostly on which
bank the borrower walked into.

**Red team two — so control for it.** Bucket every loan by its lender's
own rounding habit and re-measure.

```
LENDER ROUNDING REGIME           LOANS    MULT $100   MULT $1K   MULT $10K   $10K GIVEN $1K
rounds rarely, under 25% at $100 174,704     13.67%      7.17%       4.01%           56.0%
middle, 25-75%                   152,748     49.90%     11.40%       3.70%           32.5%
rounds always, 75% and up        146,040     93.09%     16.70%       4.46%           26.7%
```

Read the columns.

The $100 column swings sevenfold, 13.67% to 93.09%, entirely on the
lender. Confirmed convention, not a finding.

**The $10,000 column does not move.** 4.01%, 3.70%, 4.46%. Flat across a
sevenfold change in lender rounding. Whatever puts a PPP loan on an exact
ten-thousand-dollar line, it is not the bank's rounding rule.

And the conditional runs the wrong way for the lender story. Given a loan
is already a multiple of $1,000, it lands on $10,000 **56.0%** of the time
at the lenders who almost never round, against 10% by chance. At the
lenders who round everything it is 26.7%. The banks that touch the number
least produce the strongest excess.

**Red team three: is it a handful of lenders?**
No. Of the 205 lenders with 500 or more loans, the median rate on
$10,000 multiples is 3.20%, the minimum 0.23%. Only 7 exceed 10%, and
those 7 carry 9.0% of all round-$10,000 loans.

**Red team four: did SBA catch it?**

```
GROUP              LOANS      HAS FORGIVENESS   FORGIVEN IN FULL   AVG LOAN
not round        594,852               97.2%              92.8%   $560,281
round $1k         52,392               97.6%              93.5%   $578,443
round $10k        17,889               95.4%              90.1%   $494,527
round $100k        8,094               93.8%              87.6% $1,656,052
```

A five-point dip at the roundest. Effectively no scrutiny.

## What a hit means
About one first-draw PPP loan in twenty-five is an exact multiple of ten
thousand dollars, that rate is identical whether the lender rounds
everything or nothing, and it is strongest where the lender rounds least.
The number came from the borrower's side. It was picked, then the payroll
was written to match. And forgiveness barely noticed.

## What a miss would have meant
The $10,000 rate would track the lender's own rounding habit the way the
$100 rate does, and the whole pattern would be bank plumbing.

## What was struck, and why
Kept visible on purpose.

| Struck claim | Why it died |
|---|---|
| "$1,000 multiples run 116x chance, $1M runs 2,210x" | the 0.1% and 0.0001% baselines assume a uniform digit spread; the file's own 52.3% rate at $100 refutes it. Real per-digit excess is 2-3x, not hundreds |
| "the biggest loans are the roundest" | a fixed $100,000 modulus is a far harder constraint on a $150k loan than a $5M one. At constant relative precision the gradient is flat at 2 significant figures and **falls by half above $1M** at 3 |
| "the floor is Truist at 1.42%" | that was the floor of the 15 lenders displayed, not of the 205 measured. True minimum is 0.23%, and 12 of 205 sit under 1% |
| "$100 clustering at 52.3%" as a finding | lender convention, min 1.2% to max 100.0% across lenders |

The roundness-by-loan-size table at constant precision, which is what
killed the size claim:

```
LOAN SIZE        LOANS     2 SIG FIGS   3 SIG FIGS
$150k-250k     264,634          3.52%       11.06%
$250k-500k     212,857          3.81%       11.68%
$500k-1M       111,091          3.58%       11.54%
$1M-2M          54,247          2.16%        4.30%
$2M-5M          25,247          2.84%        5.03%
$5M-10M          4,402          3.16%        5.13%
```

## Trap risk
None known. No trap-log entry covers the PPP tables.
One caution measured this session, not a trap: 4,092 rows in the
"150K plus" file are under 150,000 dollars, so the file's own name is a
label, not a filter.


# Miss inside Finding 2 — the two thresholds that looked like structuring and were not

Worth keeping because both look like a finding until you check.

**The $150,000 disclosure line.** 6,596 loans sit at exactly 150,000
dollars. The first 1,000-dollar bucket above the line holds 11,597 loans,
the second holds 5,197, the tenth holds 4,911. That reads like bunching
until you see 6,596 of the 11,597 are the single round number. It is
round-number clustering, not structuring around a disclosure rule.

**The $2,000,000 audit line.** SBA said loans of two million or more get
their necessity certification reviewed. The histogram looks damning:

```
BUCKET               LOANS
$1,950,000-1,975k    931
$1,975,000-2,000k  1,289
$2,000,000-2,025k  6,411   <- 6x spike
$2,025,000-2,050k    567   <- and the floor drops out
$2,050,000-2,075k    501
```

Split it by draw type and it dies:

```
DRAW TYPE                       LOANS   AT EXACTLY $2M   ABOVE $2M   MAX
PPP, first draw               676,853              193      30,205   $10,000,000
PPS, second draw              291,671            5,678           0    $2,000,000
```

Second-draw PPP had a hard statutory ceiling of two million dollars.
5,678 borrowers hit the cap. Zero exceeded it. The spike is the ceiling
and the collapse after it is second-draw loans simply ending.

**What the miss means.** No evidence of structuring below the audit
trigger. The cliff has a boring legal cause, and anyone charting that
histogram without splitting `PROCESSINGMETHOD` publishes a false claim.

---

# Finding 3 — two EPA facility tables, same name, neither contains the other

**Subject area: ENVIRONMENT. Tables:
`LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES` and
`LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES`.**

## The chain

**What was checked.**
The Tool Box, Part 1 verb 17, states that about 85,000 registry IDs appear
in only one of these two tables. That claim had never been run. Both tables
are named for the same EPA source, the Facility Registry Service, and both
key on `REGISTRY_ID`. Take the distinct ID sets and intersect them.

**The claim is right, and it is the smaller half of the story.**

```
                                         REGISTRY IDS
FED_EPA_FRS_FACILITIES, the big one         5,300,149
FED_EPA_FRS_FRS_FACILITIES, the small one   3,277,557
in both                                     3,192,631
only in the big one                         2,107,518
only in the small one                          84,926
```

84,926 matches the Tool Box's "about 85,000" exactly. But the Tool Box
frames it as two copies with a small disagreement. It is not. The small
table is missing 2.1 million facilities the big one has, while still
holding 84,926 the big one does not.

**Neither table contains the other.** Whichever one you open, you lose
facilities.

**Not a dedupe artifact.** Both tables are exactly one row per registry ID:
5,300,149 rows to 5,300,149 IDs, and 3,277,557 to 3,277,557.

**Most of the 84,926 orphans are address-less stubs.**

The first version of this section missed that, because `FAC_STATE` is NULL
on 61,485 rows, not an empty string, and the state rollup joined them away.
Counted properly:

```
                                        ROWS
orphans, in the small table only      84,926
  no state at all                     61,485   72.4%
  no street address                   61,294
  placeable, carries a state          23,441   27.6%
```

Sampling the state-less ones: `DOLLAR GENERAL ALTMAR`, `ARK ACTIVITY
CENTER`, `BARBS RESTAURANT`, `SCHARER RANCH` — a name and nothing else.
So on the small table's side of the disagreement, only 23,441 of the
84,926 can be put on a map.

**Where the 23,441 placeable orphans sit.**

```
STATE   IN SMALL TABLE   MISSING FROM BIG   PCT
OH              75,051              7,682  10.2
CA             676,505              3,900   0.6
DM               3,790              3,790 100.0
TX             177,477                954   0.5
FL             166,258                558   0.3
XF                 382                382 100.0
GE                 367                367 100.0
```

Ohio loses one facility in ten if you use the big table. That one holds up.

**DM, XF and GE are not states.** Pulled the rows: they are Gulf of Mexico
offshore oil platforms, named like
`CHEVRON USA INC. (BOEM ID=00078 PLATFORM=23088-1)` with `FAC_CITY` set to
`GULF OF MEXICO`. 4,539 offshore platforms that exist only in the small
table. The small table carries 88 distinct `FAC_STATE` values.

## What a hit means
Any Ripple sentence of the form "there are N EPA-regulated facilities"
depends on which of two same-named tables was opened, and the two differ
by 2.1 million. Same for any coverage percentage with facilities in the
denominator. An Ohio map built off the big table is missing 10% of the
state's facilities, and every Gulf offshore platform.

## What was NOT tested
The title of the first draft was "there is no complete list of EPA
facilities in the warehouse." That went past the evidence. Two tables were
compared. Seven other `LIBRARY_MARTS` tables carry a `REGISTRY_ID` column
and none was checked. The provable claim is the one now in the heading:
these two do not contain each other.

## What a miss would have meant
One table was a clean subset of the other, and the redundancy was just
storage.

## Column note
The two tables do not even share column names. The big one uses
`FACILITY_NAME` and `ADDRESS`. The small one uses `FAC_NAME`, `FAC_STREET`,
`FAC_CITY`, `FAC_STATE`. A query written for one will not run against the
other.

## Trap risk
The 2026-08-31 entry, identical row counts do not mean identical tables,
is the same discipline pointed at a different pair. No existing entry
covers this pair.

---

# Finding 4 — two agencies, one tax ID, and the headcounts agree

**Subject areas: LABOR x ECONOMICS. Tables:
`LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024` and
`LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL`.**

The Tool Box, Part 1 verb 5, calls this "the warehouse's single best
structural advantage" and says nobody else has the forms side by side.
It had never been run.

## The chain

**What was checked.**
An employer tells OSHA how many people work at each site. The same employer
tells the Labor Department, on a completely separate form, how many active
people are in its benefit plan. The two forms share nothing but the tax ID.
Match on EIN, compare the headcounts.

**The key first.**
Form 5500 for filing year 2024 holds 224,434 filings, 144,875 distinct
EINs, and every one is nine digits. OSHA 2024 holds 398,620 establishments
carrying 109,146 usable nine-digit EINs after dropping blanks and the
all-zeros sentinel. 43,260 OSHA rows carry no EIN at all.

```
                                   COUNT
OSHA 2024 distinct EINs          109,146
Form 5500 2024 distinct EINs     144,875
matched on EIN                    20,756
percent of OSHA EINs matched        19.0%
```

**19%, not the 86-100% the shelf promises for EIN.** The shelf's key-rule
table puts EIN in the "chain freely" class. Against this pair it is not.
The reason is population, not junk keys: Form 5500 only covers employers
who sponsor an ERISA benefit plan, and OSHA 300A only covers
injury-reporting industries. The two populations barely overlap.

**Now the collision, on the 20,376 pairs where both numbers are positive.**

```
                                                     COUNT      PCT
matched pairs with both counts > 0                  20,376
median ratio, plan participants to OSHA headcount     1.01
within 2x of each other, either direction           15,082     74.0
plan count more than 5x OSHA headcount               1,658      8.1
plan count more than 20x OSHA headcount                485      2.4
OSHA headcount more than 5x plan count                 431      2.1
```

**The median is not the evidence.** A median of 1.01 sounds like a match
and is nearly free: any two similar employer-size distributions give it.
The shuffle placebo proves that. Take the same 20,376 pairs and randomly
re-pair the plan counts against the headcounts:

```
                        MEDIAN   WITHIN 2x   WITHIN 1.25x
real matched pairs       1.012       74.0%         46.9%
placebo, shuffled        1.192       32.6%         10.6%
```

The median barely moves. **The concentration does.** Within 2x, 74.0%
against 32.6%. Within 1.25x, 46.9% against 10.6%, a 4.4x lift. That is
the external-baseline check from Part 5 passing on live data, and the
concentration is the number to quote, not the median.

**Red team: what is in the 20x tail?**

```
OSHA ESTABLISHMENT                  PLAN SPONSOR                     OSHA   PLAN      X
1650 Building                       GOVERNMENT EMPLOYEES HEALTH ASSN  1,352  493,410   365
Portsmouth Regional Hospital        HCA INC.                          1,171  310,762   265
LOWE'S MARKETPLACE                  COMPASS GROUP USA, INC.             123  292,038 2,374
00001W JUPITER                      WALGREEN CO                       8,712  256,056    29
Metcon Inc.                         PAYCHEX BUSINESS SOLUTIONS LLC      124  232,458 1,875
Atalanta Therapeutics, Inc          TRINET HR III, INC.                  65  220,810 3,397
Building Service 32BJ Benefit Funds BOARD OF TRUSTEES 32BJ HEALTH FUND  865  124,984   144
Courtyard by Marriott Fort Worth    MARRIOTT INTERNATIONAL, INC.      2,642  114,079    43
General Dynamics - OTS Garland TX   GENERAL DYNAMICS CORPORATION        304   90,809   299
State Farm MRSF-CENTRAL             STATE FARM MUTUAL AUTOMOBILE INS    147   68,117   463
```

Three mechanics, all legitimate, none of them fraud.

- One site files OSHA under the parent's EIN, and the parent's plan covers
  the whole company. HCA, Walgreens, Marriott, General Dynamics, State Farm.
- A staffing co-employer sponsors the plan. Paychex Business Solutions,
  TriNet HR III. The EIN on the OSHA row belongs to the leasing company,
  not the client whose workers got hurt.
- A multi-employer union fund. Building Service 32BJ.

**Sizing the staffing-company case.** Searched the OSHA 2024 file for every
EIN belonging to a 2024 Form 5500 sponsor named TriNet, Paychex Business
Solutions, Insperity, ADP TotalSource or Justworks. Exactly two
establishments came back, 124 employees and 65. Real in kind, tiny in size.

**Red team two: does filing more sites close the gap?** No. Flat.

```
OSHA SITES FILED    PAIRS   MEDIAN RATIO   WITHIN 2X
1 site             12,467           1.00       75.6%
2-3 sites           3,333           1.06       69.0%
4-10 sites          2,700           1.05       73.1%
11+ sites           1,876           1.00       73.5%
```

The agreement holds whether an employer files one site or eleven. So the
tail is not a systematic scope effect. It is a named handful of large
corporations, and the mechanic is per-company, not structural.

## What a hit means
The EIN bridge between LABOR and ECONOMICS is real and independently
corroborated at the median. It is also thin: 19% of OSHA employers, and
you must eyeball the tail before quoting any ratio.

## What a miss would have meant
Ratios all over the place, which would say the EINs are typed junk on at
least one side and the bridge does not exist.

## Known lossy step
The `length(ein)=9` filter drops EINs whose leading zero was stripped
somewhere upstream: 14,083 OSHA rows, 5,439 distinct EINs. Zero-padding
both sides gives 22,013 matches of 114,585, or 19.2% instead of 19.0%.
It moves nothing, but the filter is silently lossy and the next person
should pad.

## Trap risk
The 2026-09-01 FCC entry, `EIN` 100% empty string, is the same discipline.
OSHA's EIN is not empty. Counted this session, 2024: 43,260 of 398,620
rows blank, 89.1% non-blank, 85.6% parsing to nine digits, and **zero rows
carry the all-zeros sentinel** in 2023, 2024 or 2025. The LEIE and SAM
sentinel does not appear here. Checked because the first draft of this
report asserted it without counting.

---

# Dry lenses — what turned up nothing, and why

| Lens or move | Where | Why it came back empty |
|---|---|---|
| Regression discontinuity, $150k | SBA PPP | the spike is one round number, not bunching below a rule |
| Regression discontinuity, $2M | SBA PPP | the cliff is the second-draw statutory cap, split by PROCESSINGMETHOD and it vanishes |
| Impossible zero at scale | OSHA 300A | the turn-up was copy-paste rows, gone after dedupe |
| Peer-group outlier, construction | OSHA 300A | 30.4% zero was one filer, Caltrans, 470 rows |
| Staffing-company EIN leak | OSHA x 5500 | real mechanic, 2 rows in the whole 2024 file |
| Site-count scope effect | OSHA x 5500 | median ratio flat at 1.00 from 1 site to 11+ |
| Lender rounding convention at $10k | SBA PPP | 4,117 lenders, only 7 of 205 big ones over 10%, and those 7 carry 9% of round loans |
| Round numbers as a fraud tell at $100 | SBA PPP | it IS the lender: 1.2% to 100.0% across lenders, median 66.7% |
| Roundness rising with loan size | SBA PPP | fixed-modulus artifact; flat at 2 sig figs, falls by half above $1M at 3 |
| Median headcount agreement | OSHA x 5500 | a shuffle placebo gives median 1.19; the median proves nothing |

A miss is worth a line. Ten of these rule out a story that would have
looked publishable from one query, and four of the ten were caught by the
skeptic pass after this file's first draft already claimed them as findings.

---

# New trap-log entries

Written to the trap log 2026-09-08. Nine entries in total: seven under the dated heading, two more appended after the machine sweep. The two late ones are NOT under that heading's skeptic-checked claim.

```
2026-09-08 — LABOR__FED_OSHA_ITA_300A_SUMMARY_* TOTAL_HOURS_WORKED is not
per-establishment for multi-site filers. Caltrans files 470 rows in the 2024
file carrying only 14 distinct hour values, each row stamped with its whole
district's hours and headcount. At 250+ FTE, rows sharing an identical
(hours, employees, state, NAICS) tuple in a block of 5 or more report zero
injuries 49-79% of the time against 6.7% for rows unique in that tuple.
Any per-establishment injury rate off those rows is wrong. Dedupe on the
tuple, never on COMPANY_NAME.

2026-09-08 — LABOR__FED_OSHA_ITA_300A_SUMMARY_* COMPANY_NAME is not the
company. On the Caltrans rows it holds 'Facility 982'; the employer's name
lives only inside ESTABLISHMENT_NAME. Also: TOTAL_HOURS_WORKED has a junk
tail, 117 rows over 100M hours in 2024. Hours divided by
ANNUAL_AVERAGE_EMPLOYEES has median 1,780 and 88% of rows fall between 800
and 3,000; filter on that before any rate. EIN is blank on 43,260 of
398,620 rows in 2024, 89.1% non-blank, 85.6% parsing to nine digits. It
does NOT carry the LEIE/SAM all-zeros sentinel: zero rows in 2023, 2024
or 2025. Leading zeros are stripped on 14,083 rows, so pad before joining.

2026-09-08 — ENVIRONMENT__FED_EPA_FRS_FACILITIES (5,300,149 registry IDs)
and ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES (3,277,557) are not two copies
of one file and neither contains the other: 3,192,631 shared, 2,107,518 only
in the big one, 84,926 only in the small one. But 61,485 of those 84,926
are name-only stubs with no state and no street, and FAC_STATE is NULL not
'' so a state rollup joins them away — only 23,441 are placeable. Ohio
loses 10.2% of its facilities in the big table, and 4,539 Gulf of Mexico
offshore platforms sit under FAC_STATE codes DM/XF/GE that exist only in
the small table. Column names differ too — FACILITY_NAME/ADDRESS against
FAC_NAME/FAC_STREET/FAC_CITY/FAC_STATE. Say which table any facility count
came from. Seven other LIBRARY_MARTS tables carry REGISTRY_ID and were not
checked, so this is not a statement about the whole warehouse.

2026-09-08 — EIN across LABOR__FED_OSHA_ITA_300A_SUMMARY_2024 and
LANDING.FED_DOL_FORM5500_FULL matches on 20,756 of 109,146 OSHA EINs, 19.0%.
The shelf's key-rule table puts EIN at 86-100% "chain freely"; that does not
hold for this pair, because Form 5500 only covers ERISA plan sponsors. The
matched pairs are sound — median participant-to-headcount ratio 1.01 — but
the 2.4% tail above 20x is one site filing under a parent's EIN, a staffing
co-employer, or a multi-employer union fund. Eyeball the tail before quoting
any ratio. And do not quote the median as evidence of agreement: a shuffle
placebo on the same pairs gives median 1.19. The real signal is the
concentration, 46.9% within 1.25x against 10.6% shuffled.

2026-09-08 — round numbers in ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS are
mostly the LENDER, not the borrower. 52.3% of first-draw amounts are exact
multiples of $100, but across the 205 lenders with 500+ loans that share
runs from 1.2% to 100.0%, median 66.7% — it is a bank disbursement
convention. Never compute a "times chance" figure against a uniform digit
baseline here; the file's own mod-100 rate refutes it, and real per-digit
excess is 2-3x, not hundreds. Bucket by the lender's own rounding habit
before claiming anything. The $10,000 rate survives that control, flat at
4.01/3.70/4.46% across the three regimes.

2026-09-08 — measuring "roundness" with a fixed modulus manufactures a size
gradient: a fixed $100,000 modulus is a far harder constraint on a $150k
loan than a $5M one, so mult-of-$100k rises 0.78%→3.16% across PPP loan
sizes and means nothing. At constant relative precision the gradient is
flat at 2 significant figures and FALLS by half above $1M at 3. Use
significant figures, never a fixed modulus, when comparing across scales.

2026-09-08 — ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS holds 4,092 rows under
$150,000; the file name is a label, not a filter. Any histogram of
INITIALAPPROVALAMOUNT must split PROCESSINGMETHOD: PPS second-draw loans are
hard-capped at exactly $2,000,000 with 5,678 sitting on the cap and zero
above, so an unsplit chart shows a 6x spike and a cliff that read as
structuring around the SBA audit trigger and are neither.
```

---

# Every query that produced a kept finding

Run through `connect/db.py`, read-only.

## F1.1 — grain and key check, OSHA 2024

```sql
select
  count(*) rows_,
  count(distinct ID) d_id,
  count(distinct ESTABLISHMENT_ID) d_estab,
  count(distinct EIN) d_ein,
  count_if(nullif(trim(EIN),'') is null) ein_blank,
  count_if(TOTAL_HOURS_WORKED is null) hrs_null,
  count_if(TOTAL_HOURS_WORKED = 0) hrs_zero,
  count(distinct NO_INJURIES_ILLNESSES) d_flag,
  count(distinct YEAR_FILING_FOR) d_year
from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024;
```

## F1.2 — hours per employee sanity

```sql
with b as (
  select *, TOTAL_HOURS_WORKED/nullif(ANNUAL_AVERAGE_EMPLOYEES,0) hpe
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
)
select
  count(*) n,
  count_if(hpe is null) hpe_null,
  count_if(hpe between 800 and 3000) plausible,
  count_if(hpe > 3000) too_high,
  count_if(hpe < 800) too_low,
  round(median(hpe)) med_hpe,
  count_if(TOTAL_HOURS_WORKED > 100000000) hrs_over_100m,
  count_if(ANNUAL_AVERAGE_EMPLOYEES > 100000) emp_over_100k
from b;
```

## F1.3 — the raw size curve, 2024

```sql
with b as (
  select TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e, NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where TOTAL_HOURS_WORKED/nullif(ANNUAL_AVERAGE_EMPLOYEES,0) between 800 and 3000
),
band as (
  select case
    when h <   50000 then '1. under 25 FTE'
    when h <  200000 then '2. 25-100 FTE'
    when h <  500000 then '3. 100-250 FTE'
    when h < 1000000 then '4. 250-500 FTE'
    when h < 2000000 then '5. 500-1000 FTE'
    when h < 5000000 then '6. 1000-2500 FTE'
    else                  '7. 2500+ FTE' end bnd, f
  from b
)
select bnd, count(*) n, count_if(f='2') zero_filers,
       round(100.0*count_if(f='2')/count(*),1) pct_zero
from band group by 1 order by 1;
```

## F1.4 — replication across 2023, 2024, 2025

```sql
with u as (
  select 2023 yr, TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e, NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023
  union all
  select 2024, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES, NO_INJURIES_ILLNESSES
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  union all
  select 2025, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES, NO_INJURIES_ILLNESSES
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025
),
b as (select * from u where h/nullif(e,0) between 800 and 3000),
band as (select yr, case
    when h <   50000 then '1. under 25 FTE'
    when h <  200000 then '2. 25-100 FTE'
    when h <  500000 then '3. 100-250 FTE'
    when h < 1000000 then '4. 250-500 FTE'
    when h < 2000000 then '5. 500-1000 FTE'
    when h < 5000000 then '6. 1000-2500 FTE'
    else                  '7. 2500+ FTE' end bnd, f from b)
select bnd,
  round(100.0*count_if(f='2' and yr=2023)/nullif(count_if(yr=2023),0),1) y2023,
  round(100.0*count_if(f='2' and yr=2024)/nullif(count_if(yr=2024),0),1) y2024,
  round(100.0*count_if(f='2' and yr=2025)/nullif(count_if(yr=2025),0),1) y2025
from band group by 1 order by 1;
```

## F1.5 — the construction rows that named the mechanic

```sql
select ESTABLISHMENT_NAME nm, STATE st, NAICS_CODE nc,
       coalesce(nullif(INDUSTRY_DESCRIPTION,''),'(blank)') ind,
       round(TOTAL_HOURS_WORKED) hrs, ANNUAL_AVERAGE_EMPLOYEES emp,
       ESTABLISHMENT_TYPE etype
from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
where TOTAL_HOURS_WORKED/nullif(ANNUAL_AVERAGE_EMPLOYEES,0) between 800 and 3000
  and TOTAL_HOURS_WORKED >= 2000000
  and left(NAICS_CODE,2)='23'
  and NO_INJURIES_ILLNESSES='2'
order by TOTAL_HOURS_WORKED desc limit 20;
```

## F1.6 — sizing the copy-paste block

```sql
with b as (
  select TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e, STATE st,
         NAICS_CODE nc, NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where TOTAL_HOURS_WORKED/nullif(ANNUAL_AVERAGE_EMPLOYEES,0) between 800 and 3000
    and TOTAL_HOURS_WORKED >= 500000
),
g as (select h,e,st,nc,count(*) n, count_if(f='2') z from b group by 1,2,3,4)
select case when n=1 then 'a. 1 (unique)' when n<=4 then 'b. 2-4'
            when n<=20 then 'c. 5-20' when n<=100 then 'd. 21-100'
            else 'e. 100+' end grp,
       count(*) groups_, sum(n) rows_, sum(z) zero_,
       round(100.0*sum(z)/sum(n),1) pct_zero
from g group by 1 order by 1;
```

## F1.7 — naming the biggest blocks

```sql
with b as (
  select ESTABLISHMENT_NAME nm, TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e,
         STATE st, NAICS_CODE nc, NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where TOTAL_HOURS_WORKED/nullif(ANNUAL_AVERAGE_EMPLOYEES,0) between 800 and 3000
    and TOTAL_HOURS_WORKED >= 500000
)
select nc, st, round(h) hrs, e emp, count(*) n_rows, count_if(f='2') n_zero,
       min(nm) example_name
from b group by nc,st,h,e having count(*) >= 15 order by n_rows desc limit 15;
```

## F1.8 — the clean curve, duplicates stripped, three years pooled

```sql
with u as (
  select 2023 yr, TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e, STATE st, NAICS_CODE nc,
         NO_INJURIES_ILLNESSES f, TOTAL_INJURIES ti, TOTAL_DAFW_CASES dc, TOTAL_OTHER_CASES oc
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023
  union all select 2024, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES, STATE, NAICS_CODE,
         NO_INJURIES_ILLNESSES, TOTAL_INJURIES, TOTAL_DAFW_CASES, TOTAL_OTHER_CASES
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  union all select 2025, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES, STATE, NAICS_CODE,
         NO_INJURIES_ILLNESSES, TOTAL_INJURIES, TOTAL_DAFW_CASES, TOTAL_OTHER_CASES
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025
),
b as (select * from u where h/nullif(e,0) between 800 and 3000),
tag as (select b.*, count(*) over (partition by yr,h,e,st,nc) dupn from b),
d as (select * from tag where dupn = 1),
band as (select case
    when h <   50000 then '1. under 25 FTE'
    when h <  200000 then '2. 25-100 FTE'
    when h <  500000 then '3. 100-250 FTE'
    when h < 1000000 then '4. 250-500 FTE'
    when h < 2000000 then '5. 500-1000 FTE'
    when h < 5000000 then '6. 1000-2500 FTE'
    else                  '7. 2500+ FTE' end bnd, f, h,
    (coalesce(ti,0)+coalesce(dc,0)+coalesce(oc,0)) cases from d)
select bnd, count(*) n, count_if(f='2') zero_,
  round(100.0*count_if(f='2')/count(*),1) pct_zero,
  round(100.0*sum(cases)/nullif(sum(h)/2000,0),2) rate_per_100fte
from band group by 1 order by 1;
```

## F1.9 — sector mix of the survivors at 2,500+ FTE

```sql
with u as (
  select 2023 yr, TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e,
         STATE st, NAICS_CODE nc, NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2023
  union all select 2024, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES,
         STATE, NAICS_CODE, NO_INJURIES_ILLNESSES
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  union all select 2025, TOTAL_HOURS_WORKED, ANNUAL_AVERAGE_EMPLOYEES,
         STATE, NAICS_CODE, NO_INJURIES_ILLNESSES
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2025
),
b as (select * from u where h/nullif(e,0) between 800 and 3000 and h >= 5000000),
t as (select b.*, count(*) over (partition by yr,h,e,st,nc) dupn from b)
select left(nc,2) sector, count(*) n, count_if(f='2') zero_,
       round(100.0*count_if(f='2')/count(*),1) pct
from t where dupn=1 group by 1 order by zero_ desc limit 12;
```

## F2.1 — the $150k line

```sql
select
  count(*) n,
  min(INITIALAPPROVALAMOUNT) mn, max(INITIALAPPROVALAMOUNT) mx,
  count_if(INITIALAPPROVALAMOUNT < 150000) below_150k,
  count_if(INITIALAPPROVALAMOUNT = 150000) exactly_150k,
  count_if(INITIALAPPROVALAMOUNT between 150000 and 150999) in_first_1k,
  count_if(INITIALAPPROVALAMOUNT between 151000 and 151999) in_second_1k,
  count_if(INITIALAPPROVALAMOUNT between 159000 and 159999) in_tenth_1k,
  count(distinct LOANNUMBER) d_loan
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS;
```

## F2.2 — the $2M histogram

```sql
select floor(INITIALAPPROVALAMOUNT/25000)*25000 bucket_lo, count(*) n
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
where INITIALAPPROVALAMOUNT between 1700000 and 2299999
group by 1 order by 1;
```

## F2.3 — the cap, split by draw type

```sql
select PROCESSINGMETHOD pm,
  count(*) n,
  count_if(INITIALAPPROVALAMOUNT = 2000000) at_2m_exact,
  count_if(INITIALAPPROVALAMOUNT between 1975000 and 1999999) just_below,
  count_if(INITIALAPPROVALAMOUNT between 2000001 and 2024999) just_above,
  count_if(INITIALAPPROVALAMOUNT > 2000000) over_2m,
  max(INITIALAPPROVALAMOUNT) mx
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
group by 1 order by n desc;
```

## F2.4 — round-number share

```sql
select PROCESSINGMETHOD pm, count(*) n,
  round(100.0*count_if(INITIALAPPROVALAMOUNT = round(INITIALAPPROVALAMOUNT))/count(*),2) pct_whole_dollar,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,1000)=0)/count(*),2) pct_mult_1k,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,10000)=0)/count(*),2) pct_mult_10k,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,100000)=0)/count(*),2) pct_mult_100k,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,1000000)=0)/count(*),3) pct_mult_1m
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
where INITIALAPPROVALAMOUNT >= 150000
group by 1 order by n desc;
```

## F2.5 — lender spread

```sql
select ORIGINATINGLENDER ldr, count(*) n,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,10000)=0)/count(*),2) pct_r10k,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,1000)=0)/count(*),2) pct_r1k
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000
group by 1 order by n desc limit 15;
```

## F2.6 — roundness by loan size

```sql
with b as (
  select INITIALAPPROVALAMOUNT a from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
  where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000 and INITIALAPPROVALAMOUNT < 10000000
)
select case when a<250000 then '1. 150k-250k' when a<500000 then '2. 250k-500k'
            when a<1000000 then '3. 500k-1M' when a<2000000 then '4. 1M-2M'
            when a<5000000 then '5. 2M-5M' else '6. 5M-10M' end band,
  count(*) n,
  round(100.0*count_if(mod(a,1000)=0)/count(*),2) pct_r1k,
  round(100.0*count_if(mod(a,10000)=0)/count(*),2) pct_r10k,
  round(100.0*count_if(mod(a,100000)=0)/count(*),2) pct_r100k
from b group by 1 order by 1;
```

## F2.7 — forgiveness by roundness

```sql
with b as (
  select CURRENTAPPROVALAMOUNT amt, FORGIVENESSAMOUNT fa, LOANSTATUS ls,
         case when mod(INITIALAPPROVALAMOUNT,100000)=0 then 'c. round 100k'
              when mod(INITIALAPPROVALAMOUNT,10000)=0  then 'b. round 10k'
              when mod(INITIALAPPROVALAMOUNT,1000)=0   then 'a2. round 1k'
              else 'a1. not round' end grp
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
  where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000
)
select grp, count(*) n,
  round(100.0*count_if(fa is not null)/count(*),1) pct_has_forgiveness,
  round(100.0*count_if(fa >= amt)/count(*),1) pct_forgiven_full,
  round(avg(amt)) avg_loan
from b group by 1 order by 1;
```

## F3.1 — the FRS ID overlap

```sql
with a as (select distinct trim(REGISTRY_ID) id
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES
           where trim(coalesce(REGISTRY_ID,'')) <> ''),
     b as (select distinct trim(REGISTRY_ID) id
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES
           where trim(coalesce(REGISTRY_ID,'')) <> '')
select (select count(*) from a) a_ids,
       (select count(*) from b) b_ids,
       (select count(*) from a join b using(id)) both_,
       (select count(*) from a where id not in (select id from b)) only_a,
       (select count(*) from b where id not in (select id from a)) only_b;
```

## F3.2 — one row per registry ID, both tables

```sql
select
 (select count(*) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES) big_rows,
 (select count(*) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) small_rows,
 (select count(distinct REGISTRY_ID) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES) big_ids,
 (select count(distinct REGISTRY_ID) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) small_ids,
 (select count(distinct FAC_STATE) from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES) small_states;
```

## F3.3 — where the orphans sit

```sql
with a as (select distinct trim(REGISTRY_ID) id
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES
           where trim(coalesce(REGISTRY_ID,'')) <> ''),
onlyb as (
  select b.FAC_STATE st, count(*) n
  from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES b
  where trim(coalesce(b.REGISTRY_ID,'')) <> ''
    and trim(b.REGISTRY_ID) not in (select id from a)
  group by 1
),
tot as (select FAC_STATE st, count(*) n
        from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES group by 1)
select t.st, t.n total_in_small, coalesce(o.n,0) missing_from_big,
       round(100.0*coalesce(o.n,0)/t.n,1) pct_missing
from tot t left join onlyb o using(st)
order by missing_from_big desc limit 12;
```

## F4.1 — Form 5500 year coverage and EIN quality

```sql
with f as (
  select regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein, SRC_YEAR yr,
         try_to_number(TOT_ACTIVE_PARTCP_CNT) p
  from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL
)
select yr, count(*) n, count(distinct ein) d_ein,
       count_if(length(ein)=9) ein9, count_if(p is null) p_null, round(median(p)) med_p
from f group by 1 order by 1 desc limit 12;
```

## F4.2 — the EIN overlap

```sql
with o as (
  select regexp_replace(EIN,'[^0-9]','') ein, ANNUAL_AVERAGE_EMPLOYEES e
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where trim(coalesce(EIN,'')) <> ''
),
oc as (select ein, sum(e) osha_emp, count(*) sites from o
       where length(ein)=9 and ein <> '000000000' group by 1),
f as (
  select regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein,
         max(try_to_number(TOT_ACTIVE_PARTCP_CNT)) p5500
  from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL where SRC_YEAR='2024' group by 1
)
select (select count(*) from oc) osha_eins,
       (select count(*) from f) f5500_eins,
       (select count(*) from oc join f using(ein)) matched,
       round(100.0*(select count(*) from oc join f using(ein))/(select count(*) from oc),1) pct_of_osha;
```

## F4.3 — the headcount collision

```sql
with o as (
  select regexp_replace(EIN,'[^0-9]','') ein, sum(ANNUAL_AVERAGE_EMPLOYEES) osha_emp, count(*) sites
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where length(regexp_replace(EIN,'[^0-9]',''))=9 and regexp_replace(EIN,'[^0-9]','') <> '000000000'
  group by 1
),
f as (
  select regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein,
         max(try_to_number(TOT_ACTIVE_PARTCP_CNT)) p5500
  from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL where SRC_YEAR='2024' group by 1
),
j as (select o.ein, o.osha_emp, o.sites, f.p5500, f.p5500/nullif(o.osha_emp,0) ratio
      from o join f using(ein) where o.osha_emp > 0 and f.p5500 > 0)
select count(*) pairs,
  round(median(ratio),2) med_ratio,
  count_if(ratio between 0.5 and 2) plausible,
  count_if(ratio > 5) plan_over_5x,
  count_if(ratio > 20) plan_over_20x,
  count_if(ratio < 0.2) plan_under_5th,
  round(100.0*count_if(ratio between 0.5 and 2)/count(*),1) pct_plausible
from j;
```

## F4.4 — naming the tail

```sql
with o as (
  select regexp_replace(EIN,'[^0-9]','') ein, sum(ANNUAL_AVERAGE_EMPLOYEES) osha_emp,
         count(*) sites, min(ESTABLISHMENT_NAME) nm, min(left(NAICS_CODE,2)) n2
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where length(regexp_replace(EIN,'[^0-9]',''))=9 and regexp_replace(EIN,'[^0-9]','') <> '000000000'
  group by 1
),
f as (
  select regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein,
         max(try_to_number(TOT_ACTIVE_PARTCP_CNT)) p5500, min(SPONSOR_DFE_NAME) sp
  from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL where SRC_YEAR='2024' group by 1
)
select o.nm osha_name, f.sp plan_sponsor, o.n2 sector, o.sites,
       o.osha_emp osha_headcount, f.p5500 plan_participants,
       round(f.p5500/o.osha_emp) x
from o join f using(ein)
where o.osha_emp >= 50 and f.p5500/o.osha_emp > 20
order by f.p5500 desc limit 12;
```

## F4.5 — the staffing-company search

```sql
with peo as (
  select distinct regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein, SPONSOR_DFE_NAME nm
  from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL
  where SRC_YEAR='2024'
    and (SPONSOR_DFE_NAME ilike '%TRINET%' or SPONSOR_DFE_NAME ilike '%PAYCHEX BUSINESS%'
         or SPONSOR_DFE_NAME ilike '%INSPERITY%' or SPONSOR_DFE_NAME ilike '%ADP TOTALSOURCE%'
         or SPONSOR_DFE_NAME ilike '%JUSTWORKS%')
),
o as (
  select regexp_replace(EIN,'[^0-9]','') ein, ESTABLISHMENT_NAME nm,
         ANNUAL_AVERAGE_EMPLOYEES e, NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
)
select p.nm peo_name, count(*) osha_establishments, sum(o.e) headcount_attributed,
       count(distinct o.nm) distinct_client_names
from o join peo p using(ein) group by 1 order by 2 desc;
```

## F4.6 — does site count explain the tail

```sql
with o as (
  select regexp_replace(EIN,'[^0-9]','') ein, sum(ANNUAL_AVERAGE_EMPLOYEES) osha_emp, count(*) sites
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where length(regexp_replace(EIN,'[^0-9]',''))=9 and regexp_replace(EIN,'[^0-9]','') <> '000000000'
  group by 1
),
f as (select regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein,
             max(try_to_number(TOT_ACTIVE_PARTCP_CNT)) p
      from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL where SRC_YEAR='2024' group by 1),
j as (select o.sites, f.p/o.osha_emp r from o join f using(ein)
      where o.osha_emp>0 and f.p>0)
select case when sites=1 then '1 site' when sites<=3 then '2-3 sites'
            when sites<=10 then '4-10 sites' else '11+ sites' end grp,
       count(*) n, round(median(r),2) median_ratio,
       round(100.0*count_if(r between 0.5 and 2)/count(*),1) pct_within_2x
from j group by 1 order by 1;
```

## F5.1 — Caltrans row count and hour values

```sql
select coalesce(nullif(trim(COMPANY_NAME),''),'(blank)') co,
       count(*) rows_, count(distinct TOTAL_HOURS_WORKED) d_h,
       count(distinct ANNUAL_AVERAGE_EMPLOYEES) d_e,
       count_if(NO_INJURIES_ILLNESSES='2') zero_,
       min(TOTAL_HOURS_WORKED) min_h, max(TOTAL_HOURS_WORKED) max_h
from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
where ESTABLISHMENT_NAME ilike '%California Department of Transportation%'
group by 1 order by 2 desc;
```

## F5.2 — sector split at 1,000+ FTE, pre-dedupe

```sql
with b as (
  select left(NAICS_CODE,2) n2, TOTAL_HOURS_WORKED h, ANNUAL_AVERAGE_EMPLOYEES e,
         NO_INJURIES_ILLNESSES f
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where TOTAL_HOURS_WORKED/nullif(ANNUAL_AVERAGE_EMPLOYEES,0) between 800 and 3000
    and TOTAL_HOURS_WORKED >= 2000000
)
select n2, count(*) n, count_if(f='2') zero_,
       round(100.0*count_if(f='2')/count(*),1) pct
from b group by 1 having count(*) >= 20 order by pct desc;
```

## F5.3 — OSHA EIN population and sentinel count

```sql
select count(*) n,
  count_if(regexp_replace(EIN,'[^0-9]','') = '000000000') zeros_sentinel,
  count_if(trim(coalesce(EIN,''))='') blank,
  round(100.0*count_if(trim(coalesce(EIN,''))<>'')/count(*),1) pct_nonblank,
  round(100.0*count_if(length(regexp_replace(EIN,'[^0-9]',''))=9)/count(*),1) pct_9digit
from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024;
```

## F5.4 — PPP digit ladder and conditionals

```sql
select count(*) n,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,10)=0)/count(*),3) mod10,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,100)=0)/count(*),3) mod100,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,1000)=0)/count(*),3) mod1k,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,1000)=0)
        /nullif(count_if(mod(INITIALAPPROVALAMOUNT,100)=0),0),1) cond_1k_given_100,
  round(100.0*count_if(mod(INITIALAPPROVALAMOUNT,100)=0)
        /nullif(count_if(mod(INITIALAPPROVALAMOUNT,10)=0),0),1) cond_100_given_10
from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000;
```

## F5.5 — lender rounding spread

```sql
with l as (
  select ORIGINATINGLENDER ldr, count(*) n,
    100.0*count_if(mod(INITIALAPPROVALAMOUNT,100)=0)/count(*) p100,
    100.0*count_if(mod(INITIALAPPROVALAMOUNT,10000)=0)/count(*) p10k
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
  where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000
  group by 1 having count(*) >= 500
)
select count(*) lenders_500plus,
  round(min(p100),1) min_mod100,
  round(percentile_cont(0.1) within group (order by p100),1) p10_mod100,
  round(median(p100),1) med_mod100,
  round(percentile_cont(0.9) within group (order by p100),1) p90_mod100,
  round(max(p100),1) max_mod100,
  count_if(p100 < 25) lenders_under_25pct,
  round(min(p10k),2) min_mod10k, round(median(p10k),2) med_mod10k
from l;
```

## F5.6 — the lender-regime control, the query finding 2 now rests on

```sql
with l as (
  select ORIGINATINGLENDER ldr, count(*) n,
    100.0*count_if(mod(INITIALAPPROVALAMOUNT,100)=0)/count(*) p100
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
  where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000
  group by 1 having count(*) >= 500
),
b as (
  select p.INITIALAPPROVALAMOUNT a, l.p100
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS p
  join l on l.ldr = p.ORIGINATINGLENDER
  where p.PROCESSINGMETHOD='PPP' and p.INITIALAPPROVALAMOUNT >= 150000
)
select case when p100 < 25 then 'a. lender rounds rarely, <25% mod100'
            when p100 < 75 then 'b. lender mid, 25-75%'
            else 'c. lender rounds always, 75%+' end grp,
  count(*) loans,
  round(100.0*count_if(mod(a,100)=0)/count(*),2) pct_mod100,
  round(100.0*count_if(mod(a,1000)=0)/count(*),2) pct_mod1k,
  round(100.0*count_if(mod(a,10000)=0)/count(*),2) pct_mod10k,
  round(100.0*count_if(mod(a,10000)=0)
        /nullif(count_if(mod(a,1000)=0),0),1) cond_10k_given_1k
from b group by 1 order by 1;
```

## F5.7 — roundness at constant relative precision

```sql
with b as (
  select INITIALAPPROVALAMOUNT a,
         power(10, floor(log(10, INITIALAPPROVALAMOUNT))-1) u2,
         power(10, floor(log(10, INITIALAPPROVALAMOUNT))-2) u3
  from LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_SBA_PPP_LOANS_150K_PLUS
  where PROCESSINGMETHOD='PPP' and INITIALAPPROVALAMOUNT >= 150000
    and INITIALAPPROVALAMOUNT < 10000000
)
select case when a<250000 then '1. 150k-250k' when a<500000 then '2. 250k-500k'
            when a<1000000 then '3. 500k-1M' when a<2000000 then '4. 1M-2M'
            when a<5000000 then '5. 2M-5M' else '6. 5M-10M' end band,
  count(*) n,
  round(100.0*count_if(mod(a,u2)=0)/count(*),2) pct_2sigfig,
  round(100.0*count_if(mod(a,u3)=0)/count(*),2) pct_3sigfig,
  round(100.0*count_if(mod(a,100)=0)/count(*),2) pct_mod100
from b group by 1 order by 1;
```

## F5.8 — FRS orphans, the null-safe version

```sql
with a as (select distinct trim(REGISTRY_ID) id
           from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FACILITIES
           where trim(coalesce(REGISTRY_ID,'')) <> '')
select count(*) orphans,
       count_if(FAC_STATE is null) no_state,
       count_if(trim(coalesce(FAC_STREET,''))='') no_street,
       count_if(FAC_STATE is not null) has_state
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES b
where trim(coalesce(b.REGISTRY_ID,'')) <> ''
  and trim(b.REGISTRY_ID) not in (select id from a);
```

## F5.9 — what DM, XF and GE actually are

```sql
select FAC_STATE st, FAC_NAME nm, FAC_CITY ct
from LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__FED_EPA_FRS_FRS_FACILITIES
where FAC_STATE in ('DM','XF','GE') order by FAC_STATE limit 9;
```

## F5.10 — the shuffle placebo behind finding 4

```sql
with o as (
  select regexp_replace(EIN,'[^0-9]','') ein, sum(ANNUAL_AVERAGE_EMPLOYEES) osha_emp
  from LIBRARY_MARTS.LABOR.LABOR__FED_OSHA_ITA_300A_SUMMARY_2024
  where length(regexp_replace(EIN,'[^0-9]',''))=9
    and regexp_replace(EIN,'[^0-9]','') <> '000000000'
  group by 1
),
f as (select regexp_replace(SPONS_DFE_EIN,'[^0-9]','') ein,
             max(try_to_number(TOT_ACTIVE_PARTCP_CNT)) p
      from LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL where SRC_YEAR='2024' group by 1),
j as (select o.osha_emp oe, f.p pp from o join f using(ein)
      where o.osha_emp>0 and f.p>0),
r as (select oe, pp, row_number() over (order by oe) i,
             row_number() over (order by hash(pp)) k from j),
shuf as (select a.oe, b.pp from r a join r b on a.i = b.k)
select 'real' which, count(*) n, round(median(pp/oe),3) med,
       round(100.0*count_if(pp/oe between 0.5 and 2)/count(*),1) within_2x,
       round(100.0*count_if(pp/oe between 0.8 and 1.25)/count(*),1) within_125
from j
union all
select 'placebo', count(*), round(median(pp/oe),3),
       round(100.0*count_if(pp/oe between 0.5 and 2)/count(*),1),
       round(100.0*count_if(pp/oe between 0.8 and 1.25)/count(*),1)
from shuf;
```

---

# Skeptic scoreboard

A fresh-context reviewer got Chris's request verbatim, this file, and the
five claims. It returned **DISAGREE**. Every counter-claim it made was
re-run against the warehouse before being accepted or rejected.

| Claim | Skeptic verdict | Re-checked | Outcome |
|---|---|---|---|
| 1, OSHA dedupe | survives | dedupe objection tested both ways, same curve | kept, two errors fixed |
| 2, PPP roundness | weakened badly | mod-100 rate 52.348% confirmed, sig-figs confirmed | headline struck, smaller finding kept |
| 3, EPA FRS | survives on arithmetic, weakened on meaning | 61,485 null states confirmed | kept, retitled, stubs disclosed |
| 4, EIN bridge | survives on wrong evidence | placebo run, median 1.192 confirmed | kept, evidence swapped |
| 5, PPP misses | survives clean | every number reproduced | kept unchanged |

A second skeptic ran at session close over everything, including Finding 5,
which the first pass never saw. It returned DISAGREE and killed Finding 5
as a story. Scoreboard row "5" above refers to the PPP misses, not to
Finding 5. Finding 5's own verdict is in its section.

**What the skeptic caught that mattered most.** The "116x to 2,210x chance"
figure in the first draft of finding 2 used a uniform-digit baseline that
the file's own data refutes. It was the most quotable number in the report
and it was wrong. Second-worst: an all-zeros EIN sentinel asserted from
memory of the LEIE trap and never counted. It was zero rows, and it was
already written into a proposed trap-log entry.

**Where the skeptic was tested and held.** It claimed the state rollup in
F3.3 hid 72% of the orphan finding behind a NULL join. Re-run: 61,485 of
84,926, exactly as stated.

**Standing disagreement: none.** Both passes now agree on all five.

---

# Finding 5 — DEAD as a story, kept as a trap

**Subject area: HEALTH. Table:
`LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE`,
503,917 rows, 453,202 distinct NPIs, 503,917 distinct PROVIDER_KEY.**

> **Killed by the session-close skeptic, kept visible on purpose.**
> I wrote this up as "57% of American doctors are graded as a crowd."
> The arithmetic was right and the framing was wrong twice. The file
> carries a column, `PARTICIPATION_OPTION`, that already says whether a
> clinician reported as an individual or as a group. My charges-block
> heuristic was a lossy reconstruction of that column, and it undercounted
> the real figure. The trap underneath survives. The discovery does not.

## The chain

**What was checked.**
Medicare scores every participating clinician on quality, and that score
moves their pay up or down. The score is published per NPI, one row per
doctor, so it reads as a judgment on that individual.

The sweep flagged 1,060 rows sharing one `ALLOWED_CHARGES` value. That is
the Caltrans shape: a number that should vary per person, repeating.

**Opening the biggest block.**

```
                                    VALUE
ALLOWED_CHARGES                  $329,265,077
rows carrying it                        5,357
distinct NPIs                           5,357
distinct clinician specialties             69
distinct MEDICARE_PATIENTS values           1
distinct SERVICES values                    1
distinct FINAL_SCORE values                 2
distinct PAYMENT_ADJUSTMENT values          2
practice state                        Florida
practice size                          11,212
final score                             93.07
payment adjustment                      0.76%
```

5,357 separate doctors across 69 specialties. One patient count between
them. One service count. Two scores. A cardiologist and a podiatrist in
that group carry the same number in every performance column.

**What the file already says, which I should have read first.**

```sql
select PARTICIPATION_OPTION po, count(*) n, count(distinct NPI) npis,
       count(distinct FINAL_SCORE) d_score
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE
group by 1 order by n desc;
```

```
PARTICIPATION_OPTION      ROWS      NPIS   DISTINCT SCORES
Group                  360,752   327,190             3,248
APM Entity              99,343    93,821               221
Individual              43,142    42,720             6,417
Subgroup                   569       569                15
Virtual Group              111       107                 2
```

91.4% of rows report as something other than an individual. The $329M
block is an APM Entity, an accountable care organisation, and the row
says so. There was nothing to discover.

**Sizing it the hard way, which is what I did.**

```
                                              CLINICIANS   SHARE
all rows in the file                             503,917
in a charges-block of 50 or more                 353,369   70.1%
those blocks carrying 2 or fewer scores           353,216   70.1%
and spanning 10 or more specialties               286,888   56.9%
distinct charges-blocks                           55,291
biggest block                                      5,357
```

Of the 353,369 clinicians sitting in a group of 50 or more, all but 153
share their group's score. Not most. Effectively all of them.

## Why it died

| What I claimed | What is true |
|---|---|
| 57% of clinicians share a group score | 91.4% of rows are non-individual, straight off a labelled column |
| the file is one row per NPI | 503,917 rows, 453,202 NPIs; the grain is PROVIDER_KEY |
| an individual's performance is absent | 42,720 NPIs report as Individual, and a doctor can appear twice |
| grouping by ALLOWED_CHARGES finds the practice | it collides across states on 26% of blocks of 2 to 10 |

The heuristic did work at scale. Of 43,142 Individual rows, exactly one
lands in a charges-block of 50 or more. But a column that already exists
does the same job exactly, and quoting the proxy instead of the column
undercounts by 34 points.

## What survives, and it is worth keeping
Inside a block every money, volume and score column is constant while
`CLINICIAN_TYPE` and `YEARS_IN_MEDICARE` vary. So `ALLOWED_CHARGES`,
`MEDICARE_PATIENTS`, `SERVICES` and `FINAL_SCORE` are group-level values
printed on a per-clinician row. Any per-doctor chart off them is wrong.
That is the trap, and it is real.

## What a miss meant
The story was already published on the tin. Absence of a discovery is
still information: this file is honest about its own grain, and I did
not read it before writing it up.

## Trap risk
No prior entry covered this table. The entry written to the trap log at
first draft asserted the per-NPI grain and told a reader to group by
ALLOWED_CHARGES. Both were wrong and both are corrected in the log.

## The query

```sql
-- the block
select count(*) rows_, count(distinct NPI) npis,
       count(distinct FINAL_SCORE) d_final,
       count(distinct QUALITY_CATEGORY_SCORE) d_qual,
       count(distinct PAYMENT_ADJUSTMENT_PERCENTAGE) d_adj,
       count(distinct MEDICARE_PATIENTS) d_patients,
       count(distinct SERVICES) d_services,
       count(distinct CLINICIAN_SPECIALTY) d_specialty,
       max(FINAL_SCORE) score, max(PAYMENT_ADJUSTMENT_PERCENTAGE) adj
from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE
where ALLOWED_CHARGES = 329265077;

-- the whole file
with g as (
  select ALLOWED_CHARGES ac, count(*) n, count(distinct FINAL_SCORE) ds,
         count(distinct CLINICIAN_SPECIALTY) dsp
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE
  where ALLOWED_CHARGES is not null and ALLOWED_CHARGES > 0
  group by 1
)
select count(*) groups_, sum(n) clinicians,
  sum(iff(n>=50, n, 0)) in_groups_50plus,
  sum(iff(n>=50 and ds<=2, n, 0)) share_one_score,
  sum(iff(n>=50 and ds<=2 and dsp>=10, n, 0)) one_score_10plus_specialties,
  max(n) biggest_group
from g;
```
