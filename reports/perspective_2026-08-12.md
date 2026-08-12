# RIPPLE — PERSPECTIVE DOCUMENT
## What you actually have, 2026-08-12

Plane reading. No charts, no design. Every block follows the same four beats:

> **FROM** — the actual table(s)
> **COLUMNS** — the specific fields being looked at
> **SAYS** — what the numbers literally say
> **MEANS** — what that is, in plain words

Verified things are marked **CHECKED**. Unverified candidates are marked **CANDIDATE**.
Never confuse the two — that distinction is the whole value of this document.

---

# 0. THE PENSION DATA IS NOT BLOCKED. LAST SESSION LOOKED IN THE WRONG PLACE.

**This is a correction to last session's conclusion, found while writing this document.**

Last session declared two of your ten findings blocked — the pension paper trail
and the pension leg of the hurt-workers chain — on the grounds that "the warehouse's
PBGC table is national summary statistics with no employer/plan-level records at all"
and that the plan-level table "either doesn't exist here or was never cataloged."

**It exists. It's built. It has a tax ID column.**

The table checked was `ECONOMICS__FED_PBGC_DATA`, which is genuinely useless here —
national summary statistics, metric-name/metric-value shape, no employer. But the
plan-level table was built on 2026-08-09 in a *different subject area*:

**`LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS`**

PBGC's list of single-employer pension plans it has taken over — one row per failed
plan. Its columns, from the model:

| column | what it is |
|---|---|
| `case_number` | unique per failed plan (has both a not-null and a uniqueness test on it) |
| `sponsor_name` | the employer |
| `plan_name` | the plan |
| **`ein`** | **the employer tax ID — the join key everything needed** |
| `plan_number` | plan number within the employer |
| `city`, `state` | location |
| `date_of_plan_termination` | when the plan died |
| `date_of_pbgc_trusteeship` | when the government took it over |
| `number_of_paricipants_at_date_of_plan_termination` | how many people were in it (typo is in the source column name, preserved deliberately) |

**What this unblocks:** the original question was "how many years between a company's
last pension filing and the plan dying." Both dates now exist on hard columns —
termination date and trusteeship date on this table, filing dates on the pension-filing
table, joined on tax ID. And the sharpest harm chain on the whole platform — hurt
workers, then the pension fails, then look at what insiders were selling — has all
four legs available: injury logs by tax ID, SEC filings by tax ID, this table by tax
ID, insider filings by filer number.

**The one thing I have NOT verified, and you should not assume:** whether that `ein`
column is actually *populated*. The model has tests on the case number and sponsor
name but **no test on the tax ID**. This is exactly your recurring trap — a column
that exists and looks fine but is full of blanks or placeholder text. It has already
fooled this platform twice. So: count the distinct values and eyeball a sample before
building anything on it. One query.

**Two lessons worth more than the finding:**
1. **"I looked and it isn't there" needs to name where it looked.** Last session
   searched one subject area and concluded a table didn't exist. It was one subject
   area over. A wrong-place answer and a real absence look identical in a report.
2. When last session found the ladder claiming 381 and 18,989 tax-ID matches it
   couldn't reproduce, it concluded the ladder must be wrong. **The ladder was right.**
   Worth remembering next time a source and a session disagree.

---

# 1. THE SHAPE OF THE WHOLE THING

**FROM** — the connection map audit + the full source catalog
**COLUMNS** — n/a, this is inventory

**SAYS:**
- **558 data sources** held. 540 of them have at least one question attached.
- **4,538 measured connections** between sources.
- Of those, only **1,121 are hard-ID connections** — a real registry number on both sides.
- The other **2,606 are name-plus-address matches.** Not IDs. Guesses with good manners.
- **1,832 questions** are askable today: 1,172 need one source, 475 need two, 185 need three or more.
- Of the multi-source ones, **107 are hard-ID solid** (57 of 475 two-source, 50 of 185 three-plus).
- **376 of 558 sources have no publisher total on file** — meaning nobody knows if
  the copy held is complete.

**MEANS:** You have a very large library and a much smaller skeleton. The library is
558 sources deep. The skeleton — the part where you can say "this company here *is*
that company there" and defend it — is 1,121 connections across 14 ID families.
Everything solid you will ever publish rides that skeleton. Everything else needs a
build first, or an honest FUZZY label forever.

The second number to hold onto: **2,606 of your connections are name matches that
earlier material treated as solid.** That re-grade already happened. It moved a lot
of good-sounding questions into the "not yet" column. That was honesty, and it's why
the SOLID count looks small.

---

# 2. THE SKELETON — the 14 keys everything hangs on

These are the only ID families with measured connections. If a question doesn't
ride one of these, it isn't solid, no matter how good it sounds.

| key | plain English | what it welds together |
|---|---|---|
| **NPI** | doctor/provider number | 33 sources of doctor data — prescribing, payments, exclusions, affiliations |
| **CCN** | Medicare facility number | 25 sources of facility data — nursing homes, hospitals, hospice, home health |
| **EIN** | employer tax ID | the hinge of the whole platform: workplaces, pensions, charities, political orgs, public companies |
| **CIK** | SEC filer number | public companies, their filings, their insiders |
| **FRS_ID** | EPA facility number | 3.2M facilities' inspections, violations, toxic releases, penalties |
| **PWSID** | water system number | every water system, its samples, violations, site visits, who it serves |
| **LEI** | global company number | global corporate identity; reaches EPA facilities and mortgage lenders |
| **UEI** | federal contractor number | grants, contracts, debarment, audits |
| **MINE_ID** | mine number | mines, accidents, violations — 100% clean joins |
| **FEC_CAND_ID / FEC_CMTE_ID** | campaign IDs | donors → committees → candidates |
| **BIOGUIDE / ICPSR** | member-of-Congress IDs | legislators → votes → bills → committee seats |
| **DUNS** | old contractor number | legacy federal award rail |

**Three switchboards matter more than the rest:**

1. **The doctor-to-facility bridge** (`FED_CMS_FACILITY_AFFILIATION`) carries both
   CCN and NPI on the same row. It is the *only* verified road between doctor-world
   and facility-world. Every "the doctors at the bad nursing homes" question goes
   through this one table.
2. **The grant-audit table** (`FED_FAC_SINGLE_AUDIT`) carries both EIN and UEI on
   the same row. It is the *only* verified road between the tax world and the
   federal-money world. Every "charity/company got federal money it shouldn't have"
   question goes through this one table.
3. **SEC company financials** (`FED_SEC_EDGAR_FINANCIALS`) carries both CIK and EIN.
   It is the road between public-company world and everything keyed to a tax ID —
   workplaces, pensions, charities.

**MEANS:** Three tables are load-bearing walls. If any one of them has a quality
problem, a whole category of your work quietly breaks. Worth knowing which walls
they are.

---

# 3. THE TEN CHECKED FINDINGS

These ran live against the warehouse and then got attacked on purpose. Four came
back changed. This is the real inventory of what you can defend today.

---

### 3.1 — Nursing home stars don't watch the fire exits · **CHECKED, HELD**

**FROM** `HEALTH__FED_CMS_NURSING_HOME` (the register + star ratings),
`..._DEFICIENCIES` (418k inspection citations), `..._FIRE_DEFICIENCIES` (200k fire
citations), `..._PENALTIES` (the fines). All four joined on the Medicare facility
number.

**COLUMNS** — `OVERALL_RATING` (1-5 stars), `CMS_CERTIFICATION_NUMBER_CCN` (the join
key on every table), `FINE_AMOUNT` (summed per facility), plus a row count from each
deficiency table as the deficiency count.

**SAYS** — across 14,568 rated homes:

| stars | homes | avg fire violations | avg all violations | avg fines |
|---|---|---|---|---|
| 1 | 2,882 | 17.1 | 47.1 | $83,340 |
| 2 | 3,011 | 14.8 | 35.1 | $38,710 |
| 3 | 2,843 | 13.4 | 26.5 | $17,279 |
| 4 | 2,793 | 12.2 | 19.8 | $8,171 |
| 5 | 3,039 | 10.6 | 12.9 | $3,261 |
| **unrated** | **132** | **14.2** | **52.9** | **$154,974** |

728 five-star homes carry 16+ fire violations (641 in the 16-30 band, 87 at 31+).
Fines per home fall 28x from one star to five; fire violations fall only 1.6x.
Illinois collects $105,530 in federal fines per facility — the highest in the country,
and its $70.4M total beats Texas's $58.6M with 57% as many homes.

**MEANS** — Go from one star to five and the fines basically vanish. Go the same
distance and the fire-safety violations barely budge. The rating tracks health
inspections and money well, and fire safety badly. And the 132 homes with *no*
rating at all are the worst group on the board — most violations, biggest fines,
invisible to the rating system entirely.

**TRUST** — the register's own deficiency-count columns are 100% empty; the counts
here were rebuilt by counting rows in the detail tables. Counts span ~3 years of
surveys, not one year. 96% of the fire citations are logged low-severity — the *gap*
is real, the danger per citation isn't proven. State fines aren't included, only
federal.

---

### 3.2 — Banned doctors still getting industry money · **CHECKED, CORRECTED DOWN**

**FROM** `HEALTH__FED_HHS_OIG_LEIE` (the federal exclusion list — people banned from
billing Medicare/Medicaid) joined on provider number to
`HEALTH__FED_CMS_OPEN_PAYMENTS` plus its 2022 and 2023 vintages (every drug/device
company payment to a doctor).

**COLUMNS** — `NPI` (the join), `EXCLUSION_DATE`, `REINSTATEMENT_DATE`,
`EXCLUSION_TYPE` (the legal basis code), `PROGRAM_YEAR`,
`TOTAL_AMOUNT_OF_PAYMENT_USDOLLARS`, and — added during the correction —
`NATURE_OF_PAYMENT` (what the money was actually *for*). That last column is the one
that broke the original story.

**SAYS** — 439 banned providers received 2,938 payments totaling **$1.03M** in
program years on or after their exclusion year. Then, broken out by payment type:

| what the money was | amount |
|---|---|
| Royalty or license | $621,671 |
| Debt forgiveness | $174,422 |
| Food and beverage | $90,023 |
| Consulting fees | $64,141 |
| Speaker/faculty compensation | $61,902 |
| Travel and lodging | $6,492 |
| Education, gifts, honoraria, device loans | ~$9,500 |

The entire royalty line is **one** South Dakota neurologist, banned in 2021 for
fraud/kickback, collecting two patent payments: $318,224 in 2023 and $301,647 in 2022.
Strip the royalties and the debt write-offs and the influence-shaped money is
**~$232,000** across the other 438 providers.

**MEANS** — The million-dollar headline was one guy's patent checks. A patent license
signed before the ban keeps paying out afterward; that's contract law, not corruption.
Debt forgiveness is a company writing off what a doctor owed them — bookkeeping. What's
left, the meals and flights and speaking fees, is $232k. Still strange that banned
providers are on anyone's hospitality list. Not a scandal about a million dollars.

**TRUST** — only ~10% of the exclusion list carries a usable provider number (8,503 of
them), so this undercounts badly. Comparison is year-grain, so a same-year payment might
predate the ban date. Receiving industry money while excluded is not illegal — the ban
is on billing federal programs. The single biggest matched payment ($3.08M) is a
*pre*-exclusion payment and is correctly excluded from the total.

---

### 3.3 — A handful of mines make a third of the country's toxic releases · **CHECKED, HELD (with a caveat that matters)**

**FROM** `ENVIRONMENT__FED_EPA_TRI_BASIC_2023` (every facility's self-reported toxic
releases) joined on EPA facility number to `ENVIRONMENT__FED_EPA_ECHO` (compliance and
penalty history). The transparency half also used
`ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK`, `ECONOMICS__INTL_GLEIF_REPEX` and
`..._RELATIONSHIPS`.

**COLUMNS** — `C_17_STANDARD_PARENT_CO_NAME` (EPA's own standardized parent-company
name), `C_3_FRS_ID` (facility number), `C_107_TOTAL_RELEASES`, `C_50_UNIT_OF_MEASURE`
(grams converted at 453.592/lb), and from the compliance side
`QUARTERS_WITH_NONCOMPLIANCE`, `FORMAL_ACTION_COUNT`, `TOTAL_PENALTIES`.

**SAYS** —

| parent | pounds released 2023 | facilities | EPA penalties |
|---|---|---|---|
| Teck American | 771,294,324 | 2 | $1.19M |
| Rio Tinto America | 261,059,234 | 3 | $211k |
| Barrick Nevada | 167,400,914 | 9 | $0 |
| Hecla Mining | 113,295,860 | 2 | $461k |
| Targa Resources | 81,287,950 | 33 | **$48.4M** |
| Americas Mining | 53,158,588 | 4 | $0 |
| Freeport-McMoRan | 51,163,636 | 12 | $10,000 |

Top three — all mining — put out 1.2 billion pounds from 14 facilities: about 35% of
the 3.4-billion-pound national total. The US Department of Defense shows up as a
"parent" with 277 facilities, 925 quarters of noncompliance and $12.5M in penalties.

**MEANS** — This isn't ten thousand factories each doing a little. It's a small number
of holes in the ground doing most of it. Barrick released 167 million pounds and paid
nothing. Targa released a tenth of Teck's volume and paid forty times the fines. The
relationship between how much you release and what happens to you is close to random.

**TRUST — the big one:** this measures *weight*, mixing air, water, land and
underground injection. A pound of mine waste rock is not a pound of dioxin. Say that
out loud every time or the chart is a cheat. Also: parent names are as-reported for
2023, mergers since aren't reflected, and facilities missing from the compliance table
count as null, not zero.

**The transparency half came out backwards.** Of 73,948 EPA facilities matched to a
global company ID, 71% (52,196) belong to owners who formally filed a "reporting
exception" — legally refusing to name a parent company. The intuition is that secrecy
hides pollution. The data says the opposite: exception-filers average 73,284 lbs per
facility, named-parent owners average 153,157. **Opacity clusters in small operators,
not big polluters.** That's a real finding and an honest one, and it's the hardest kind
to explain to anyone.

---

### 3.4 — Paid prescribers write more, not pricier · **CHECKED, CORRECTED IN SHAPE**

**FROM** `HEALTH__FED_CMS_PART_D_PRESCRIBERS` (every Medicare drug prescriber),
`HEALTH__FED_CMS_OPEN_PAYMENTS` + 2022/2023 vintages (industry money),
`HEALTH__FED_CMS_MEDICARE_PROVIDER` (Part B billing),
`HEALTH__FED_HHS_OIG_LEIE` (exclusions). All joined on provider number.

**COLUMNS** — `PRSCRBR_TYPE` (specialty), `TOT_DRUG_CST`, and — added in the
correction — `TOT_CLMS` (number of prescriptions), which made cost-per-prescription
computable. That one division is what changed the answer.

**SAYS** — 109 specialties with 25+ prescribers:

| specialty | prescribers | % paid | prescriptions: paid vs unpaid | cost per prescription: paid vs unpaid |
|---|---|---|---|---|
| Nurse Practitioner | 278,577 | 72.8% | 485 vs 209 | $83.10 vs $47.23 |
| Physician Assistant | 137,246 | 69.6% | 332 vs 171 | $60.36 vs $22.29 |
| Internal Medicine | 130,220 | 58.6% | 971 vs 263 | $90.45 vs $74.62 |
| Family Practice | 117,797 | 60.0% | 2,777 vs 726 | $84.96 vs $69.93 |
| Emergency Medicine | 56,372 | 36.8% | 175 vs 130 | $16.55 vs **$17.02** |
| Dentist | 132,825 | 72.6% | 59 vs 48 | $4.60 vs $4.54 |

Also: Hematology-Oncology, 90.3% of 9,229 prescribers took industry money, median
$1.8M in drug cost each. Cardiology has the highest paid share of any large specialty
at 91.2%. And 156 providers on the exclusion list still appear as active prescribers.

**MEANS** — The original headline said paid doctors cost Medicare 2-7x more. True, and
misleading. They're not choosing pricier drugs; they're writing two to four times as
many prescriptions. Per prescription the prices are close, and in Emergency Medicine
the paid group is actually *cheaper*. So the real question isn't "were they bribed into
expensive drugs," it's "why does taking money go along with three times the volume?"
The boring answer — companies target the busiest prescribers — is probably right, and
still worth saying: in the biggest specialties in American medicine, six to nine out of
ten prescribers are on somebody's payment list.

**TRUST** — association, not causation. The drug file is one year; the payment data is
three years summed. Specialty labels are self-reported. Suppressed small cells
undercount. The 156 excluded-but-prescribing providers partly reflect exclusions dated
after the prescribing year.

---

### 3.5 — 31 million people, lead over the limit, no violation on record · **CHECKED, CORRECTED DOWN**

**FROM** `ENVIRONMENT__FED_EPA_SDWA_SDWA_LCR_SAMPLES` (927k lead/copper test results),
`..._PUB_WATER_SYSTEMS` (434k systems), `..._VIOLATIONS_ENFORCEMENT` (15.4M violation
records). Joined on water system ID.

**COLUMNS** — `PWSID` (the join), `CONTAMINANT_CODE = 'PB90'` (the lead 90th-percentile
result), `SAMPLE_MEASURE` (the reading — **stored as text**, which is where the bug
lived), `RULE_CODE = '350'` (the Lead & Copper Rule), `PWS_ACTIVITY_CODE = 'A'`
(active only), `POPULATION_SERVED_COUNT`, `PWS_TYPE_CODE`.

**SAYS** — systems whose lead reading exceeded the 15 ppb action level with zero
Lead & Copper Rule violations on file:

| | before the fix | after the fix |
|---|---|---|
| national systems | 4,515 | **3,898** |
| national population | 35.1M | **31.2M** |
| Ohio systems | 488 | **118** |
| Ohio population | 5.7M | **2.6M** |

Top states after correction: California 357 systems / 4.0M people; Massachusetts 67
systems / 3.4M (few systems, big cities); Ohio 118 / 2.6M; Michigan 138 / 1.8M;
Florida 210 / 1.6M. Separately, 3,350 covered systems serving 2.4M people have **no
lead or copper sample on file at all** — Washington has the largest never-tested
population (1.06M across 101 systems), Michigan the most never-tested systems (756).

**MEANS** — Thirty-one million people drink from systems that tested over the federal
lead limit and carry no lead violation. Not a slap on the wrist — nothing. And that's
legal: going over the limit triggers treatment steps, not a citation, so the paperwork
stays clean while the lead stays in the pipe.

**TRUST — this is the one where our own math was wrong.** Every reading is labeled
mg/L, but a chunk of them are clearly micrograms mislabeled — off by a thousand. The
tell: Ohio's worst reading was 9,900 ppb before the fix and 95 after; Mississippi's was
20,127 before and 85 after. Restricting to the plausible 15-100 ppb band dropped 913
systems and 7.7M people. **91% of Ohio's original number was our bug.** The remaining
31.2M is the honest figure. Also: absence of a violation in our copy isn't proof of
absence in EPA's full system, and 131 exceeding systems (2.1M people) have no state code.

---

### 3.6 — Brand-name prescribing only jumps at the very top · **CHECKED, CORRECTED IN SHAPE**

**FROM** `HEALTH__FED_CMS_PART_D_PRESCRIBERS` + Open Payments 2022-2024, joined on
provider number, prescribers sorted into deciles by how much industry money they got.

**COLUMNS** — `BRND_TOT_CLMS`, `GNRC_TOT_CLMS`, `BRND_TOT_DRUG_CST`,
`GNRC_TOT_DRUG_CST`, `TOT_CLMS` (filtered to 50+ for stability), `TOT_DRUG_CST`,
`PRSCRBR_TYPE`. The correction added the claim-volume column.

**SAYS** — Cardiology, brand share of prescriptions by payment decile:

| bucket | median money | brand share | median prescriptions |
|---|---|---|---|
| no payment | $0 | 17.03% | 1,492 |
| D01 | $20 | 16.77% | 2,207 |
| D04 | $223 | 16.06% | 2,568 |
| D07 | $1,071 | 16.41% | 2,918 |
| D09 | $3,063 | 17.30% | 3,488 |
| **D10** | **$9,685** | **19.95%** | 2,732 |

Internal Medicine does climb steadily (12.58% → 16.68%), but note the volume column
climbing right alongside it: 1,477 prescriptions → 6,471.

**MEANS** — The clean story would be a straight line: more money, more brand-name
drugs. That's not what's there. A cardiologist who took $20, or $200, or $1,000 writes
about the *same* share of brand-name drugs as one who took nothing — sometimes slightly
less. Flat across nearly the whole range. Then it hooks hard at the top: the top tenth,
median $9,685, jumps to 20% against 17% for the unpaid. So it isn't that a sandwich
changes prescribing. Something is different about the group getting five figures.

**TRUST** — association only; the arrow could run either way. **The manufacturer-to-drug
version of this question is impossible here** — the Open Payments tables in this
warehouse carry no drug or product columns at all, so "did Pfizer's money move Pfizer's
drug" cannot be asked. This decile shape is the fallback. Deciles are pooled across 15
specialties, so bucket sizes vary by specialty.

---

### 3.7 — Three years in violation, zero consequences · **CHECKED, HELD — the strongest one**

**FROM** `ENVIRONMENT__FED_EPA_ECHO` alone. One table, 3.2M facilities. No join, no
join risk.

**COLUMNS** — `QUARTERS_WITH_NONCOMPLIANCE` (0-12, a 3-year rolling window),
`FORMAL_ACTION_COUNT`, `INFORMAL_ACTION_COUNT`, `TOTAL_PENALTIES`, `STATE`.

**SAYS** —

| quarters in violation | facilities | with formal enforcement | zero formal enforcement | avg warning letters (unenforced) |
|---|---|---|---|---|
| 0 | 2,888,533 | 12,666 | 2,875,867 | 0.03 |
| 1-3 | 72,610 | 8,441 | 64,169 | 2.2 |
| 4-7 | 41,269 | 6,452 | 34,817 | 4.4 |
| 8-11 | 35,609 | 6,613 | 28,996 | 8.3 |
| **12 (all 3 years)** | **18,626** | **3,303** | **15,323** | **3.0** |

Of all 54,315 chronic (8+ quarter) violators, **44,319 — 82% — have no formal
enforcement on file.** Every single facility with zero formal actions also shows **$0
in penalties** — confirming warning letters never carry a fine. West Virginia has the
worst rate (91.6% of chronic violators never formally enforced), Washington the biggest
raw count (2,972).

**MEANS** — 15,323 facilities were out of compliance every single quarter for three
straight years. The EPA took formal action against none of them and collected nothing.
They got letters — about three each. Widen to everyone in violation two years or more
and it's the same picture: 82 out of 100 never faced a formal action. The rules exist.
The paperwork exists. The consequence is what's missing.

**TRUST** — the quarter counter caps at 12 and is total quarters, not necessarily
consecutive. Action counts are a 5-year window, so older enforcement wouldn't appear.
~79k facilities (2.5%) have a null quarter count and are excluded. State ranking limited
to states with 50+ chronic facilities.

---

### 3.8 — 19,043 charities revoked and still on the IRS's own safe-to-donate list · **CHECKED, HELD (and got stronger)**

**FROM** `ECONOMICS__FED_IRS_PUB78_ELIGIBLE_DONEES` (1.44M organizations the IRS says
your donation is deductible to) joined on tax ID to `ECONOMICS__FED_IRS_REVOCATION`
(1.19M revocations).

**COLUMNS** — `EIN` on both sides, normalized by stripping non-digits (formats differ —
a real join-killer); `WAS_REINSTATED`; `REVOCATION_DATE` (text, parsed as DD-MON-YYYY);
`STATE`.

**SAYS** — 125,692 tax IDs on both lists. 106,649 were reinstated. **19,043 were
revoked, never reinstated, and are still listed as eligible.** By year of revocation:

| year | never reinstated, still listed |
|---|---|
| 2010 | 2,821 |
| 2011 | 1,517 |
| 2015 | 711 |
| 2019 | 948 |
| 2020 | 1,462 |
| 2023 | 1,223 |
| 2024 | 1,346 |
| 2025 | 1,561 |

**MEANS** — The IRS keeps two lists. One says which charities are legit and deductible.
The other says whose status got pulled for not filing. Nineteen thousand names are on
both. Most of the overlap is innocent — 106,649 got reinstated and just weren't cleaned
off. The 19,043 that never got reinstated are the finding. And the trend is going the
wrong way: ~950 a year in 2019, ~1,560 in 2025. You look it up, you do the right thing,
you give — and the deduction may not be real.

**TRUST** — checked and cleared: this is *not* explained by the two files being pulled
on different dates. It got stronger under attack, not weaker. Two watch-outs: the 2010
spike is a one-time law change (the first mass auto-revocation wave after the three-year
non-filing rule), so it's history, not scandal; and the 45 never-reinstated 2026
revocations genuinely *are* file lag. Reinstatement is judged only by the reinstatement
field in the revocation file.

---

### 3.9 — The pension paper trail · **WAS CALLED BLOCKED — IT ISN'T (see section 0)**

**FROM** what was used: `ECONOMICS__FED_PBGC_DATA` (PBGC's published Data Book —
aggregate statistics, `METRIC_NAME`/`METRIC_VALUE` shape, no employer, no plan) and
`ECONOMICS__FED_DOL_FORM5500` (a partial slice of pension filings).

**COLUMNS** — the only usable ones: `FISCAL_YEAR` and a cumulative plan count scraped
from summary pages; on the filings side a final-filing indicator, `STATE`, and a
beginning-of-year participant count. The plan-year and form-year columns are **100%
empty** in this slice and asset amounts are null.

**SAYS** — plans PBGC has taken over, cumulative: 4,779 (2016) → 4,855 → 4,929 → 4,975
→ 5,041 → 5,110 → 5,129 → 5,154 (2023). About 47 more plans a year. Separately, in the
Jan-Jun 2026 filing slice, 2,590 plans filed their final-ever return covering ~626,000
participants — California 216, Texas 193 leading. Only ~141 filings in the whole slice
are classic defined-benefit plans; it's dominated by 401(k)-type plans.

**MEANS** — The question was "how long between a company's last pension filing and the
plan dying." It cannot be answered with these two tables, because one of them has no
companies in it. A gentle upward slope and a six-month snapshot of paperwork closures
is not that question. **And a final filing is not a failure** — plans close for
mergers, voluntary terminations, and ordinary wind-downs.

**BUT** — see section 0. The plan-level table exists, in the labor subject area, with
plan termination dates, trusteeship dates, participant counts and a tax ID. The real
version of this question — years between last filing and plan death — is buildable now,
pending one check that the tax ID column is actually filled.

---

### 3.10 — Injury rates at public companies · **CHECKED, CORRECTED — and half-blocked**

**FROM** `LABOR__FED_OSHA_ITA_300A_SUMMARY_2024` (employers' own injury summaries)
joined on tax ID to `FINANCE__FED_SEC_EDGAR_FINANCIALS`, then on filer number to
`FINANCE__FED_SEC_EDGAR_INSIDERS`.

**COLUMNS** — `EIN` (normalized to 9 digits — the original match found 607 companies
vs the ladder's claimed 191 purely because of that normalization),
`TOTAL_HOURS_WORKED`, `ANNUAL_AVERAGE_EMPLOYEES`, `TOTAL_DAFW_CASES` +
`TOTAL_DJTR_CASES` + `TOTAL_OTHER_CASES` (summed to recordable cases), `TOTAL_DEATHS`,
`CIK`, `SIC`. Injury rate = cases × 200,000 ÷ hours. All the OSHA numbers are stored as
text and have to be cast.

**SAYS** — 612 matched records across 607 tax IDs; 513 also have insider filings.
Rates run 0 to 31.6 per 100 full-time workers, median 1.0. **107 of 612 report exactly
0.0.** After filtering to companies with 500k+ hours worked:

| company | injuries per 100 FTE | hours | establishments |
|---|---|---|---|
| Southwest Airlines | 11.97 | 103.9M | 140 |
| Carvana | 10.46 | 7.2M | 14 |
| Tractor Supply | 9.87 | 18.5M | 623 |
| Six Flags | 9.14 | 1.9M | 2 |
| Ford Motor | 8.50 | 116.1M | 53 |
| UPS | 7.81 | 591.3M | 1,358 |
| Marriott International | 7.11 | 3.9M | 8 |

UPS: 23,080 recordable injuries and **10 deaths**.

**MEANS** — Southwest injured about twelve of every hundred full-time workers in 2024
against a median of one. These are the biggest, most-lawyered employers in the country
reporting these numbers themselves, in public, on purpose. The intended chain went
further — hurt workers, then the pension fails, then look at insider selling — and
**that leg is available after all** (section 0): the failed-pension table has the same
tax ID these injury logs are keyed on. This is a half-finished chain, not a broken one.

**TRUST — the correction here was about not getting embarrassed.** 177 of 612 companies
are below 500k hours, and the naive ranking put small operations on top: Zumiez at 31.6
off a single store, plus Ascent Industries, Sun Communities, Rush Enterprises, Marriott
Vacations, PVH. Those rates are arithmetically right and statistically meaningless.
Southwest at 11.97 on 104 million hours is the number that's safe to say out loud. Also:
OSHA covers only establishments required to e-file summaries; insider counts are
*filings* per company, not transactions or dollars — that table has no amounts.

---

# 4. THE WIDER MAP — 15 domains, thin each

This is the rest of the 1,832. **Everything below is CANDIDATE unless it says
otherwise** — the ladder graded the joins against the connection map, but nobody has
run these.

---

### 4.1 Health & medicine — the deepest bench (172 tier-1, 85 tier-2, most of the SOLID chains)

**FROM** — provider registry (`FED_CMS_NPPES`, 9.6M providers), Part D prescribing,
Part B billing, Open Payments, exclusions, the nursing-home family (25 tables), the
doctor-facility bridge, FDA device and drug tables, hospital cost reports.
**Key** — NPI and CCN, joining at 100% on most pairs (1.4M, 1.3M, 979k matched).

**Best unrun questions:**
- **Chemical restraint of the elderly** — antipsychotics into dementia wards, measured
  from both prescriber claims and facility assessment data. Sedatives given to keep
  residents quiet raise their death rate. Sedated people can't complain.
- **Weekend staffing collapse** — from payroll-based staffing data, not self-reported
  numbers. Who is actually in the building on a Saturday.
- **Recalls that never close** — how long recalls sit unterminated by severity class.
  A null termination date might mean "still open" — those nulls are the worst cases and
  must not be dropped.
- **Traveling medical directors** — doctors serving as medical director at many
  troubled homes at once. Rides the CCN+NPI bridge, 13,050 matched.
- **The 510(k) shortcut** — how many devices reached market by being declared "similar
  to" something older rather than tested. Most devices in a patient's body were never
  independently tested.

**Weak spot:** the entire opioid shipment family — 178.6M rows — is unusable for joins
(see section 5). Device injury data is 2.7M of 25.7M loaded, so any "this device is
safe, no reports" claim from it is a lie.

---

### 4.2 Environment & pollution — second strongest (131 tier-1, 43 tier-2)

**FROM** — EPA facility registry, compliance history (3.2M facilities), toxic releases,
air/water/hazardous-waste violation tables, drinking water family (9 tables), the
corporate crosswalk up to global company IDs.
**Key** — EPA facility number at 97-100% across program tables; water system ID at
99.3-100%.

**Best unrun questions:**
- **Fine per pound of poison** — penalties divided by actual released pounds, per
  facility and per parent. 99.4% join. No blockers.
- **Same facility, three kinds of poison** — facilities violating air *and* water *and*
  hazardous-waste rules simultaneously. All hard-ID.
- **Water violations without site visits** — systems with violations nobody ever
  physically inspected. 254,793 systems matched.
- **Kept in the dark** — water systems that failed to notify the public, and how long
  the silence lasted. Length of silence = length of exposure.
- **Emissions volume vs enforcement attention** — does the EPA look where the pollution
  actually is.

**Shape of this whole domain:** enforcement-vacuum questions. Not "who pollutes" —
that's public — but "where did the regulator stop regulating."

---

### 4.3 Labor & workplace — best solid ratio (49 tier-1, 28 tier-2)

**FROM** — OSHA injury logs (with a real hours-worked denominator, which is rare),
mine registry/accidents/violations, pension filings, failed pensions.
**Key** — tax ID and mine number, both clean; mine joins are 100%.

**Best unrun questions:**
- **Citation before the injury** — was the mine already cited for the exact hazard that
  later hurt someone. 100% joins, no blockers. This is as close to a smoking gun as
  this platform gets.
- **Rebranded mines, same controllers** — a mine closes with a bad record and reopens
  under a new name with the same people.
- **The penalty discount machine** — mine operators contesting fines as routine
  practice, and what the average discount is.
- **Injuries per hour worked, employer by employer** — an honest denominator, which
  most injury reporting lacks.

**Thin spot:** the OSHA-to-public-company overlap is small (191-607 employers depending
on how tax IDs are normalized).

---

### 4.4 Federal money — strong keys, capped counts (44 tier-1, 26 tier-2)

**FROM** — contracts, assistance/grants (19.9M rows), debarment list, grant audits (the
dual-key table), IRS business master file, SBIR awards, NIH grants.
**Key** — contractor number and tax ID, both hard.

**Best unrun questions:**
- **Debarred but still funded** — companies on the federal ban list still receiving
  awards. Currently 53 contract matches and 29 assistance matches, but see the caveat.
- **Bad-audit grantees keep the money** — 40,746 matched; organizations whose federal
  audits found problems, still getting checks.
- **Revoked charities still receiving federal grants** — ~1,500 tax IDs, cross-regulator
  failure entirely on hard IDs.
- **Research-award winners on the exclusion list.**

**The caveat that governs the entire domain:** federal contracts are capped at exactly
20M rows and the entity spine reads an even smaller ~6.3M copy. **Every count here is a
floor, not a total.** 30+ questions carry this stamp.

---

### 4.5 Courts & justice — highest untapped harm, zero solid chains (118 tier-1, 57 tier-2)

**FROM** — 71.7M CourtListener dockets, 21 newly modeled court tables, federal case
databases (civil, criminal, bankruptcy, appellate), judge biographical directory, judge
financial disclosures and investments.
**Key** — **none verified.** Zero connections to anything else in the platform.

**Best unrun questions (all single-source, which is fine — they work alone):**
- **The trial penalty** — 6.3M criminal cases: what it costs a defendant to exercise
  the right to a trial instead of pleading. Blocked only on a codebook.
- **The Chapter 13 trap** — 7M bankruptcies: who enters a repayment plan and never
  completes it. Also codebook-blocked.
- **Judges ruling on companies they own** — needs a name-normalization build, but is
  testable against a known ground-truth list of ~130 judge conflict cases.

**MEANS** — This is the biggest gap between harm density and readiness on the platform.
118 strong questions run fine on one source each. Everything cross-source waits on
registering the court data's internal IDs into the connection map — an afternoon of
checking, not a build.

---

### 4.6 Finance & markets — one great chain, rest keyless (81 tier-1, 24 tier-2)

**FROM** — SEC filings/financials/insiders/tickers, quarterly index files, 13F
institutional holdings (202M positions).
**Key** — filer number and tax ID.

**Best unrun:** **insider selling at pension-failure companies** — executives selling
while the retirement plan is failing. This is the sharpest harm mechanism on the
platform, and per section 0 **every table it needs is built**: failed plans with tax IDs
and termination dates, SEC financials bridging tax ID to filer number, insider filings
by filer number. It needs one column check and then it can be run.

**The 202M-position problem:** institutional holdings have no usable key to the
companies being held. "Who profits from harm" is unanswerable until a securities-ID
bridge exists. Much of the rest of this domain is disclosure-mechanics trivia.

---

### 4.7 Money in politics — split down the middle (92 tier-1, 45 tier-2)

**FROM** — FEC contributions/committees/candidates/linkages/summaries/independent
expenditures, 527 organization registrations and reports, state lobbying filings.
**Key** — campaign IDs work *internally* at 88.7-99.9%.

**Best unrun:** **who runs the 527 dark-money orgs** — registrations to money reports
to named directors and officers, 94.9% and 100% matched. One of only ~4 solid chains
here.

**The structural fact:** **not one politics question rides the verified entity map.**
The whole world runs on its own IDs plus name matching. Every chain that touches the
real economy or Congress is a name guess.

**And the cheapest big fix on the platform is here:** the congressional roster already
carries campaign-candidate IDs. Nobody has verified that column. Verify it and the
entire money-to-votes lane (donors → committees → candidate → how they voted) plus
~12 more questions flip to solid. That's a column check, not a build.

---

### 4.8 Housing — highest harm per question, no water in the pipes (36 tier-1, 22 tier-2)

**FROM** — mortgage lending records, lender-to-company crosswalk, global company
registry, HUD subsidized housing, 1930s redlining maps.
**Key** — company number at 100% for lender ownership.

**Best unrun:** **who owns the mortgage lenders** (fully solid, 100% joins), and
**modern redlining** — denial rates by neighborhood against the 1930s maps.

**The blocker:** the mortgage data held is a 17k-28k-row *sample* plus one
city-year slice. The data model file itself bans lending-pattern claims until a full
re-pull. Plumbing is solid, there's just no water in it.

---

### 4.9 Immigration — small, harm-dense, half-dead (32 tier-1, 23 tier-2)

**FROM** — 2.6M person-level detention stints, facility lists, immigration court
records.
**Key** — none verified. The designed stint-to-facility key is unchecked.

**Best unrun:** **detainers lifted because the person was a US citizen** — the
government's own record of holding citizens. And **freedom priced out of reach** —
bond amounts set against bond actually posted.

**The blocker:** the immigration-court table is 12.6M rows with **one real column** —
a husk. Judge-by-judge asylum grant-rate disparity is called the single
highest-value blocked question on the platform, and it waits entirely on a reload.

---

### 4.10 Corporate shells — the platform's thesis, thinly supplied (51 tier-1, 16 tier-2)

**FROM** — UK company registry and beneficial-ownership file, offshore leak data
(entities + 771k officers), global company registry and its parent-relationship and
exception files.

**Best unrun:** **excuses for not naming a parent** — 6.3M ownership-disclosure
exceptions, the legal reasons companies give for refusing to say who owns them. (Note:
finding 3.3 already tested this idea and got a counterintuitive answer. That's a
reason to run it wider, not to skip it.)

**Blockers:** the UK ownership join is the connection map's only probabilistic edge at
45.7%, and that file is truncated (~7M of ~10M, non-randomly). Offshore leaks are
name-only.

---

### 4.11 Sanctions — conceptually strong, zero connections (30 tier-1, 18 tier-2)

**FROM** — OFAC list, EU/UN/UK lists, OpenSanctions, the consolidated screening list,
suspended mortgage counterparties, plus 58.1M ship-position pings.
**Key** — **zero verified connections. All of it.**

**Best unrun:** sanctioned entities still receiving federal contracts or still shipping.

**Blocker:** pure name-match territory until an alias-aware matching spine is built.
The ship data's vessel IDs are ~56% sentinel-masked — one of the recurring traps that
has already fooled this platform twice.

---

### 4.12 Disasters / transport / energy (28 + 25 + 70 tier-1)

**Best unrun, and these are sharp:**
- **Aid awarded vs loss verified** — FEMA's own recorded unmet need. The government
  wrote down what people lost and what it paid. The gap is the story.
- **Defects sold for years before the recall letter** — complaint-to-recall lag per
  manufacturer.
- **Grade crossings and high-hazard dams** — infrastructure with a known hazard
  classification and a known condition rating.

**Blockers:** truncated loads, unverified utility keys, and vehicle
make/model/year vocabulary that's never been checked across the complaint, recall and
investigation tables (same publisher, finite vocabulary — a cheap fix).

---

### 4.13 Politics & government — mostly padding, sharp minority (91 tier-1, 26 tier-2)

**Best unrun:** **rejected ballots** — who gets their vote thrown out and why. And a
genuinely novel one: **1.54M archived captures of the DOJ Epstein document library** —
tracking edits to the public record over time. Nobody else is doing that.

**Standing defect:** the roll-call vote table disagrees with its own canonical twin
(113,512 rows vs 3,364). Every voting question carries a "build from the source table,
not this mart" stamp until it's rebuilt.

---

### 4.14 Nonprofits / food & ag / science-education (14 + 5 + 44 tier-1)

Thin or blocked. Nonprofit tables hit 500k-row load caps, and the 990 financial mart
holds **200 rows** while a 5.5M-row sibling table sits unwired. Nonprofit executive
compensation is one small fix away and currently impossible.

---

### 4.15 The catalog auditing itself (59 questions)

Internal quality questions. Real value for trust, zero external harm. Worth knowing
because it inflates the headline question count by 8-10% — the 1,832 includes 59
questions about Ripple's own data.

---

# 5. THE DARK MATTER — your biggest tables connect to nothing

The pattern worth seeing: **the harm-heaviest data is systematically the worst
connected.** That isn't a coincidence and it isn't malice — the influence and harm
record is genuinely the least standardized part of the public record.

| source | size | why it's dark |
|---|---|---|
| **DEA opioid shipments** | 178.6M rows | its DEA number joins nothing held; name+zip only |
| **Court dockets** | 71.7M | zero verified connections to anything |
| **13F institutional holdings** | 202M positions | no key to the companies held |
| **Ship position pings** | 58.1M | vessel ID ~56% sentinel-masked |
| **Consumer complaints** | 34M | company strings are consumer brands, not legal entities |
| **Immigration court** | 12.6M | one real column — a husk |
| **Device injury reports** | 2.7M of 25.7M | partial load; absence questions built on it *actively lie* |
| **Detention stints** | 2.6M | facility key unverified |
| **Practitioner data bank** | 1.9M | de-identified by design — will never join |
| **Fracking + orphaned wells** | 7.2M + 118k | no verified edge; well number is the candidate key |
| **Sanctions lists** | all of them | name-only |
| **PPP loans** | 968k | far below known program size; zero edges |
| **Product injuries (NEISS)** | — | gated on a code table and survey weights |
| **Credit unions** | — | out of the spine entirely; contradiction flagged, see below |

**The opioid one is the most painful.** 178.6M shipment records — pills, by pharmacy,
by month — and the reason it can't join to prescribers is a missing crosswalk between
DEA numbers and provider numbers. **CMS publishes that crosswalk.**

**One contradiction to settle:** on credit unions, one note says the tables carry
charter-number columns that one check would promote, and another says the replacement
tables carry no hard ID at all. Both can't be true. One query settles whether the
credit-union side of banking joins or stays dark forever.

---

# 6. THE UNLOCK LEDGER — cheapest fixes first

40 identified fixes. Ranked by how many questions each converts. **The top of this
list is startlingly cheap.**

### An afternoon each — column checks, not builds

1. **Verify the campaign-candidate ID in the congressional roster.** Flips the entire
   money-to-votes lane plus ~12 questions. Called the cheapest big unlock in the graph.
2. **Verify the tax ID inside hospital cost reports.** Welds the health facility world
   to the corporate/tax world. Called one of the most valuable single verifications on
   the platform.
3. **Check whether the failed-pension table's tax ID column is really populated**
   (section 0). The table is built and has the column; nobody has tested it. Two of
   your ten findings and the platform's sharpest harm chain sit behind this one query.
4. **A batch of ~12 never-measured keys** — exclusion-list IDs, court judge IDs,
   research-grant contractor numbers, device IDs, well numbers, detention facility
   codes. Each one promotes a whole family of questions. The fix line across the whole
   file is literally "one verification pass promotes."
5. **Audit the court data's internal IDs** into the connection map. ~10 court questions
   plus the judge dossier.
6. **Rail safety keys** — 8 questions plus a full railroad dossier. Same-publisher keys.
7. **Provider taxonomy crosswalk** — a published, finite code list. Clears 19 separate
   caveats in the ladder, including its very first question.
8. **Small hand-built crosswalks** — senator names to IDs (~100 people), the injury
   code table (the code list alone gates every product-injury finding), a justice-code
   mapping, an election codebook.

### Reloads and ingests — days, not weeks

9. **Lift the 20M-row federal contracts cap.** 30+ questions stop being floors. Biggest
   single count improvement available.
10. **Reload Senate lobbying** — currently 9% loaded and now key-gated. **This one needs
    your signature, not engineering: a 2-minute API signup.** ~20 questions unblock.
11. **The tax-ID-to-contractor-number crosswalk** (both IDs sit on one row in federal
    registration data). Welds the tax world to the federal-money world. Called the
    single highest-value build to make employers traceable end-to-end.
12. **Geography pack** — verified ZIP-to-county mapping and a zero-padding fix.
    ~90+ county-overlay questions across every domain. "Poor counties get dirtier
    water" is one formatting fix away from askable.
13. **The DEA-to-provider crosswalk** — CMS publishes it. Lights up 178.6M rows.
14. **Hunt the round-number load caps** — exactly 500,000 rows on charity lists, injury
    case detail, political ads; exactly 10,000 on banking tables. A round number is a
    cap, not a coincidence.
15. **Immigration court reload** — the husk. Whole domain.
16. **Full mortgage re-pull** — the redlining family stops being aspirational.

### Real builds — weeks

17. **A company/donor name resolver plus address canonicalizer.** The highest
    fuzzy-to-solid conversion available: ~80 name-only questions plus every shell-hub
    question. This is the build that would move the 2,606 name-match connections
    toward something defensible.
18. **Court party-name normalization** — testable against ~130 known judge-conflict
    cases, which is a rare luxury: a ground truth to measure precision against.
19. **Sanctions alias-aware screening spine.**

---

# 7. WHAT'S ACTUALLY BROKEN — 16 bugs found in passing

Not theory. These are live, and several silently kill joins.

**The silent join-killers — these are the dangerous ones:**
- Filer numbers are zero-padded differently between sources. Tax IDs use different dash
  formats. Untyped YYYYMMDD date text hits an epoch-parse trap. **A join that should
  match returns zero rows and looks like a finding.** "Nobody appears on both lists"
  and "the formats differ" are indistinguishable without checking.
- A number-cast wrapped over text columns nulls out country and ID values across **12+
  tables**, including a police-violence county column, an FBI county column, and a
  Medicare ownership control ID.
- Leading zeros stripped from geographic codes on both 20M-row federal spending tables,
  and from mine county codes — a known broken join.

**The captured-garbage bugs:**
- A banking mart captured page HTML instead of data (302 rows with a doctype column).
- A federal appendix mart is 144 rows of unnamed columns — headers never parsed.
- A loader ate the first data row as a header on an FDA drug-label table and renamed
  columns positionally; the same defect exists on a Canadian drug registry table.
- A rates table has its date buried inside a description field; its companion is 304
  rows of unlabeled series codes.

**The disagreements:**
- Consumer complaints: 34M vs 17M rows depending on where you look. Duplicated or
  partially reloaded.
- SEC financials: catalog row count doesn't match the mart. Suggests a partial load.
- The roll-call vote mart vs its canonical twin: 113,512 vs 3,364.

**And your own recurring trap, which has bitten twice:** a column that looks 100%
populated but is full of sentinel values — blank strings, placeholder text, masked IDs.
It happened with a provider tax-ID column and a vessel ID. Both looked complete.
Neither was. **Count distinct values and eyeball a sample before trusting any column
as a join key.** This is written into your constitution for a reason.

---

# 8. THE HONEST BOTTOM LINE

**What you have that nobody else has:** the connected version. Lots of people can
download the nursing-home file. Almost nobody has it welded to the deficiency detail,
the fire inspections, the penalties, the doctors who work there, and the pharma money
those doctors take — on hard IDs at 99-100% match rates. That welding is the asset.
It's also the part that took the longest and is hardest to copy.

**What you have less of than the headline suggests.** 1,832 askable questions, but 59
of those are the platform asking about itself, ~a quarter of the single-source tier
isn't currently buildable, and only 107 of the 660 multi-source questions ride hard IDs
today. The rest need one to three fixes each. Most of those fixes are afternoons.

**The single most important structural fact:** your solid core is health, environment,
labor, and federal money. Those four domains have working keys, high match rates, and
real harm on the other end. Everything else — courts, politics, sanctions, immigration,
housing, finance — is one to three fixes away, and the fixes are mostly *verification*,
not construction. Checking whether a column is real is cheaper than building anything.

**The uncomfortable pattern:** the data about the most harm is the least complete data
you hold. Opioids, courts, sanctions, immigration, device injuries, lobbying. That's
not a coincidence of your loading — it's what the public record actually looks like.
The influence record is the least complete record. That observation is itself a finding
about how accountability works in America, and it's arguably more interesting than any
single number in section 3.

**What's checked and defensible right now:** eight of the ten in section 3. Four of
those eight came back changed after being attacked, and one of the four changed by
enough that the original headline was wrong. That ratio — half your findings needing
correction on a second look — is the most useful number in this document. It's not a
failure rate. It's the cost of being right, measured.

---

*Receipts for everything in section 3: `reports/ladder_top10_queries/q1..q10/` —
each has the query, the result, and where corrections happened, the fixed data plus
notes on what changed and why. Section 4-7 material comes from
`reports/question_ladder_2026-08-12.md` and its ranked digest. Section 0's load spec is
at `scripts/recon_bulk_load_2026-08-07.py` line 373.*
