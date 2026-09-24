# Fable hunt — findings, 2026-09-23

Door: Python scripts only. Read-only. Every number below came from a SELECT in `sql/`.
Every person and company named is a **data match, not verified against primary records.**
The five strongest candidates each got a fresh-context skeptic; both verdicts are recorded. B6 to B10 were not sent, and say so. A closing skeptic read the whole file; its ten gaps are fixed or noted below.

## Ranked summary

| # | Tier | Finding | Tables | Skeptic |
|---|---|---|---|---|
| 1 | A | Judge Gilstrap held stock in Apple, Microsoft, AT&T and Walmart while assigned to 183 cases naming them; 240 judges, 1,157 cases in all | disclosures, investments, judges, dockets | broken, fixed; Gilstrap holds, aggregate not re-checked |
| 2 | A | Counties with the most opioid pills in 2006-12 have 2.7x the overdose deaths in 2019-24 | ARCOS, CDC injury, DIM_COUNTY | broken, fixed, confirmed |
| 3 | A | 27% of nonprofit hospitals pay one officer more than their whole charity-care cost | 990 officer pay, HCRIS, CCN-EIN crosswalk | confirmed with caveats |
| 4 | B | Doctors paid by the challenger drug's maker prescribe more of it; half the gap is targeting | Open Payments 2022, Part D 2022 | correlation only |
| 5 | B | 23 excluded firms kept getting delivery orders, $800K, mostly DoD | SAM exclusions, USAspending R2 | broken, narrowed |
| 6 | B | 5,362 corporate insiders gave $555M in 2021-26; the CEO of a coal firm with 932 serious violations per 1,000 miners and six deaths gave $8.2M | SEC insiders, FEC individuals, FEC committees, MSHA | not sent, bridge only |
| 7 | B | Black applicants denied at 2x the White rate at every big 2017 mortgage lender | HMDA historic, ARID-LEI xref | not sent, known shape |
| 8 | B | 76 co-authors of ORI-retracted papers got $187M of NIH money after the retraction | Retraction Watch, NIH Reporter | not sent, framing caveat |
| 9 | B | Banking Committee senators made 34% of bank-stock trades while being 19% of traders | Senate trades, committee membership, EDGAR tickers, SIC | not sent, thin |
| 10 | B | Eight coal controllers with 900-1,960 serious violations per 1,000 miners; one paid under half its fines | MSHA violations, accidents, mines | not sent, single domain |
| C | C | Nine clean misses, listed at the bottom | | |

Stop rule: ten A or B findings. Met. Wave three probes stopped turning up new shapes.

---

## A1. Judges held stock in companies that were parties in their own cases

**Headline:** Judge Rodney Gilstrap of the Eastern District of Texas reported common stock in Apple, Microsoft, AT&T, Walmart and eleven other companies every year 2013-2020 and is listed as the assigned judge on 300 cases naming them as parties; 240 judges and 1,157 cases show the same pattern, a count the skeptic has not re-checked since the fixes.

```
after skeptic fixes          judges   cases   companies
first tightened pass           331    1,700     116
final                          240    1,157     106   not re-skepticked
Gilstrap, E.D. Tex, patent docket, stock held every year 2013-2020
  Apple                      58 cases   "Apple Inc. common stock"
  Microsoft                  45
  AT&T                       44
  Walmart                    36
  Verizon                    28
  Target                     23
  Cisco                      17
  Wells Fargo                15
  Oracle                     12
  Honeywell                  10
  IBM 9, Schlumberger 8, Qualcomm 6, Nike 6, American Express 6
others that survive
  Mashburn, bankr. M.D. Tenn   Bank of America  32   2011 row, no value shown
  Marks, M.D. Ala              Walmart          18   WMT
  Martinotti, D.N.J.           Walmart          16
  Snyder, C.D. Cal             Wells Fargo 15, Target 6, Travelers 6
  Cecchi, D.N.J.               Wells Fargo 12, Prudential 6
  Barrett, S.D. Ohio           Abbott            7
  Zouhary, N.D. Ohio           Zimmer            6
dropped by the skeptic
  Evans, Schell                bank-branded funds and a cash account
  Beyer, Dorsey, Helmick       cases filed after the stock was sold
  Helmick                      inherited a 2,564-case MDL from a judge who died
```

- **Checked:** judge id join is real: 105,327 of 105,327 dockets for the named judges carry the judge's name in the assigned-to text. 20 of 20 sampled Gilstrap Apple and Microsoft dockets are patent suits with the company as defendant, including Optis v. Apple. Disclosure year is the calendar year covered; every dated transaction falls inside it.
- **Hit means:** the judge reported the stock at year end and is listed as assigned on a case naming that company, filed before any reported sale. Under 28 USC 455 any financial interest, however small, requires recusal.
- **Miss means:** the docket shows the last assigned judge, not the judge at filing. Recusals after assignment are not in this table. A managed account or a spouse's holding looks the same. Patent dockets come in waves; 58 dockets is not 58 matters.
- **Fixes applied after the skeptic:** one-letter form codes like "(X)" no longer count as tickers; fund words "FD", "Adv", "Cking", "Mtg", "depo" now exclude; cases filed after a full Sold or Redeemed date drop; MDL and reassigned dockets drop. One gap stays: a prior-year row can still admit a case filed after a mid-year sale. Dorsey's 5 may be 1.
- **Prior art:** WSJ 2021 found 131 judges this way through 2018. This warehouse gets 249 through 2020 from CourtListener.

Tables: `JUSTICE__FED_COURTLISTENER_INVESTMENTS` → `_FINANCIAL_DISCLOSURES` (29,073 of 66,287 rows carry a judge id) → `_JUDGES`, and `_DOCKETS` (32.4M of 71.7M rows carry an assigned judge). Join agreement: judge id 100% on 105,327 dockets; named judge-company pairs 7 of 12 held before fixes.
Skeptic: **BROKEN as written, Gilstrap holds.** Three fixes applied, counts restated; the closing skeptic found the fund-word regex was dead, fixed and rerun, 249/1,180 became 240/1,157. The A tier rests on Gilstrap; the aggregate is B until re-checked. Names: data match, not verified against primary records. SQL: `sql/02_judges_stock_in_parties.sql`.

---

## A2. Counties with the most opioid pills in 2006-12 have the most overdose deaths in 2019-24

**Headline:** the top tenth of counties by pharmacy opioid dose per person in 2006-2012 averaged 51 overdose deaths per 100,000 a year in 2019-2024; the bottom tenth averaged 19. Deciles are ranked by morphine-equivalent milligrams per person; the tablets column is shown beside it. The skeptic's rerun ranked by tablets and got 20.0 and 53.0.

```
counties               789   (20,000+ people, all six death years reported)
                pills/person/yr   OD deaths per 100k, 2019-24 avg
decile 1                 17               18.7
decile 5                 36               28.9
decile 10                83               51.1
ratio top/bottom                          2.7x
correlation, skeptic run                  0.53  (0.60 on logs)
join rate ARCOS county → DIM_COUNTY       99.0%
named
  Logan WV        200 pills/person/yr    127 deaths per 100k
  Boone WV        123                     97
  Wyoming WV      120                    106
  Cabell WV        99                    120
  Mingo WV        232                    111  (skeptic rerun)
```

- **Checked:** ARCOS is 2006-2012 only, 178.6M rows, all transaction code S. Buyers are chain and retail pharmacies only, no hospitals, no distributors, so no warehouse pill mountains. MEASURE is TAB on every row. CDC rate rows kept only where the count is present and RATE >= 0, six years required.
- **Hit means:** where pharmacies dispensed the most pills per head fifteen years ago, people die of overdoses at the highest rates now. Dose-response holds across all ten deciles, with small dips at 2 and 9.
- **Miss means:** a county with high pills and low deaths is likely a mail-order or prison pharmacy. Charleston SC and Leavenworth KS sit in the top tenth with low death rates.
- **Boring explanation:** rural Appalachian poverty drives both, and the 2019-24 deaths are fentanyl. Not ruled out. These tables carry no income, age or drug-type columns. The finding is a correlation, not a cause.
- **Population:** 2020 population divides 2006-12 pills. Shrinking counties get inflated pills per head. Goes in the claim's favour; minor.

Tables: `HEALTH__FED_DEA_ARCOS` → `CORE.DIM_COUNTY` ← `HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY`. Join agreement: 99.0% of pills land on a county.
Names: data match, not verified against primary records.
Skeptic: **BROKEN on first pass, then CONFIRMED.** First run filtered `COUNT_SUP is null` thinking it meant unsuppressed. It is the count itself, null when suppressed. That kept only the small-number years. Mingo read 42 instead of 111. Fixed, rerun, saved as a trap memory. Skeptic's own rerun: bottom tenth 20.0, top tenth 53.0. SQL: `sql/03_arcos_pills_vs_overdose.sql`.

---

## A3. A quarter of nonprofit hospitals pay one officer more than their whole charity-care cost

**Headline:** among 919 nonprofit hospitals matched across the 990 and the Medicare cost report, 27% reported less charity-care cost in 2022 than they paid their single top officer, and 45% less than they paid their officers combined.

```
hospitals matched                     919
top officer pay > charity care        249   27.1%
all officers pay > charity care       417   45.4%
median top officer pay           $400,546
median charity care cost       $1,241,655
officer pay from the hospital, total   $2.05B
charity care cost, total               $5.59B
fiscal-year aligned rerun, skeptic     874 hospitals, 27.5% / 46.3%
named, top officer pay vs charity care
  MelroseWakefield Healthcare, MA   president   $0.63M vs $0.02M
  Cayuga Medical Center, NY         CEO         $1.05M vs $0.20M
  Griffin Hospital, CT              CEO         $4.45M vs $1.29M
  Emerson Hospital, MA              CEO         $1.69M vs $0.77M
  Valley Presbyterian, CA           CEO         $1.27M vs $0.85M
```

- **Checked:** pay is reportable pay from the hospital itself plus other pay, for rows flagged officer or key employee, not former, not group returns. Charity is HCRIS `COST_OF_CHARITY_CARE`, the S-10 cost line, rows above zero only. Crosswalk tiers 1-2, nonprofit only. Only 4 EINs share across hospitals.
- **Hit means:** the hospital's own filing says it spent less on free care than on one executive.
- **Miss means:** charity care as defined here excludes bad debt and Medicaid shortfall. Against all uncompensated care the share falls to 5%. Say "S-10 charity care cost", never "community benefit".
- **Boring explanation:** hospital size. ND, KS and MN hospitals in the match are 22-25 bed rural places with tiny charity lines; TX and FL are 160-290 beds with $8-10M. It is not Medicaid expansion alone: Kansas never expanded and still shows 25 of 32. Massachusetts near-zeros likely reflect the state Health Safety Net paying charity back.
- **Dropped:** Ochsner. Its 990 is a $6B system return mapped to one $2B hospital, and the CEO left that year. NY Community Hospital of Brooklyn and Summit Healthcare: top earner is a physician, not an executive.

Tables: `HEALTH__HOSPITAL_OFFICER_PAY` ← `CORE.XWALK_HOSPITAL_CCN_EIN` → `HEALTH__FED_CMS_HCRIS`. Join agreement: crosswalk tiers 1-2 are name and ZIP matched; 990 revenue exceeds twice HCRIS net patient revenue on 4.9% of rows, the system-return cases.
Names: data match, not verified against primary records.
Skeptic: **CONFIRMED WITH CAVEATS.** Numbers reproduce. Title mix of top earners: CEO or president 610, physician 94, CFO or COO 72, other 143. SQL: `sql/05_hospital_officer_pay_vs_charity.sql`.

---

## B4. Doctors paid by the challenger drug's maker prescribe more of it

**Headline:** in 2022, prescribers paid only by Novo Nordisk wrote 54% Ozempic against Trulicity; prescribers paid by neither wrote 41%; prescribers paid only by Lilly wrote 40%.

```
pair, 50+ combined claims       neither   own-maker only   rival-maker only
Ozempic vs Trulicity              41.1        53.9              39.7
Jardiance vs Farxiga              76.2        73.4              46.6   (AZ money moves Farxiga)
Eliquis vs Xarelto                76.2        77.0              69.6   (Janssen money moves Xarelto)
Januvia vs Tradjenta              70.1        72.9              67.9
skeptic, money tagged to the drug itself
Ozempic                           42.1        52.8              35.2
Jardiance                         74.9        70.2              48.8
skeptic, doctors Novo first paid in 2023, no money in 2022
  Ozempic share already in 2022   46.5   vs 40.4 never paid, 53.9 paid in 2022
```

- **Checked:** same-year tables, both 2022. Payer aliases caught, including "Eli Lilly and Company". Teaching hospitals and ownership rows excluded. One prescriber type per NPI, so no double count. Pooled percentages recomputed from claim counts by the skeptic and matched.
- **Hit means:** the underdog's money goes with a bigger share of the underdog's drug, in every specialty. Family practice 51 vs 39, internal medicine 55 vs 40, nurse practitioners 56 vs 39.
- **Miss means:** the leader's money does nothing. Lilly money on Trulicity, BMS money on Eliquis, Merck money on Januvia: flat. Jardiance-tagged money goes with less Jardiance.
- **Boring explanation:** reps pay doctors who already like their drug. Half survives. Doctors Novo first paid in 2023 already sat at 46.5% Ozempic in 2022, halfway between never-paid and paid. No 2021 payments in the warehouse, so it cannot be split further.
- **Fix available:** the staging table names the drug on each payment. Money can be tagged to the drug, not the company. The skeptic did that and the Ozempic result held.

Tables: `HEALTH__FED_CMS_OPEN_PAYMENTS_2022` ← NPI → `HEALTH__FED_CMS_PARTD_PRESCRIBERS`. Join on NPI, 10-digit both sides.
Names: data match, not verified against primary records.
Skeptic: **BROKEN as worded, correlation holds.** "Moves" is causal; "goes with" is what the data says. SQL: `sql/01_pharma_money_moves_own_drug.sql`.

---

## B5. Excluded contractors kept getting delivery orders

**Headline:** 23 firms under government-wide SAM exclusions received about $800K in federal contract obligations after their exclusion date, almost all as orders under contracts signed before the exclusion.

```
first pass, all exclusion types, "new" by first action date     33 firms   168 actions   $2.10M
government-wide exclusions only, sql/04c rerun                   23 firms    71 actions   $0.80M
  orders under a parent contract first seen before the exclusion 16 firms    43 actions  $692K
  orders under a parent first seen after the exclusion            7 firms    10 actions   $65K
  standalone new purchase orders                                  9 firms    18 actions   $43K, all under $10K
  skeptic's own split of the same $0.80M                          $479K pre-exclusion parents, $266K same-year, $43K standalone
named, whole-firm reciprocal exclusions
  A&S Skill Machinist, DLA voluntary exclusion 2023-10   16 orders, 15 under FY20-23 DLA contracts
  JML Logistics, Army 2023-12                           $68,735 order under a FY2020 contract
  Mud Lake Oil and Kit Contracting, USDA 2024           Forest Service equipment orders 3-6 days after
```

- **Checked:** join on UEI. Company name on the contract matches the exclusion name for 30 of 33. `EXCLUSION_PROGRAM` is the flag that matters, not `EXCLUSION_TYPE`: Reciprocal means barred everywhere. All named examples are Reciprocal, whole firm.
- **Hit means:** an agency placed an order with a firm SAM said was barred. FAR 9.405-1(b) generally bars new orders under existing contracts with debarred firms unless an agency head signs off.
- **Miss means:** SAM listings post with a lag of days; orders within a week may predate the posting. Null end dates were treated as forever, which keeps stale 2011-14 SBA listings open.
- **Boring explanation:** modifications on old contracts. Removed: ATI Government Solutions' $6.8M vanished when mods were dropped. What is left is delivery orders, which are their own question.

Tables: `PROCUREMENT__FED_SAM_EXCLUSIONS` ← UEI → `ECONOMICS__FED_USASPENDING_CONTRACTS_FULL_R2`. Join agreement: names match on 30 of 33.
Skeptic: **BROKEN as worded, narrowed.** Facility listings and orders on old contracts inflated "new awards". Names: data match, not verified against primary records. SQL: `sql/04c_debarred_firms_narrowed.sql` produces the $0.80M block; `04_...new_awards.sql` and `04b_...all_actions.sql` are the first passes.

---

## B6. Corporate insiders as political donors, and the coal chain

**Headline:** 5,362 SEC-registered officers and directors matched to $555M of FEC giving in the 2022-2026 cycles, $184M of it to super PACs; the CEO of Alliance Resource Partners, a coal firm with 932 serious violations per 1,000 miners and six deaths in 2018-24, gave $8.2M. Five controllers in B10 have higher violation rates than Alliance; none of their executives gave more.

```
insiders matched            5,362
gifts, deduped             36,301
dollars                    $555.5M
to super PACs              $183.5M
to Republican committees    $33.6M   to Democratic committees $27.9M   rest: super PACs, hybrids, party
coal chain, MSHA 2018-24 → SEC Form 4 → FEC 2020-26
  Alliance Resource Partners   932 S&S per 1,000 miners, 6 deaths, 82% of fines paid
    Joseph Craft III, CEO      $8.19M, biggest recipient Congressional Leadership Fund
  Ramaco Resources           1,454 S&S per 1,000
    Randall Atkins, CEO        $306K
  Alpha Metallurgical          925 S&S per 1,000, 3 deaths
    Andrew Eidson, CFO         $37K
  Freeport-McMoRan              53 S&S per 1,000, 5 deaths
    Richard Adkerson, CEO      $446K
```

- **Checked:** match on last name, first name, state, and employer starting with the issuer's first word. Insider names like "DIMON JAMES" split on the first space; FEC names "DIMON, JAMES" split on the comma. Earmark memo rows dropped. Gifts deduped by FEC SUB_ID.
- **Hit means:** the same person, at the same company, in the same state, gave that money. The issuer can be tied to its EPA, MSHA or contract record by name.
- **Miss means:** insiders who list a different employer, or who moved states, are missed. Common names in big states can collide; the employer test limits that.
- **Boring explanation:** rich executives give money. True. The bridge is the asset: it turns any company table into a donor table.

Tables: `FINANCE__FED_SEC_INSIDER_REPORTINGOWNER` → `_SUBMISSION` → `FINANCE__FED_FEC_INDIV_CONTRIBUTIONS` → `FINANCE__FED_FEC_COMMITTEES_DIM`; coal names from `LABOR__FED_MSHA_VIOLATIONS`. Join agreement: three fields plus employer.
Names: data match, not verified against primary records.
Skeptic: **not sent.** Bridge, not a story on its own. SQL: `sql/07_insiders_fec_donors.sql`, `07b_insiders_fec_dedupe_and_coal_execs.sql`.

---

## B7. Black applicants denied at twice the White rate at every big 2017 lender

**Headline:** in 2017 home-purchase applications, every large lender denied Black applicants at roughly twice the White rate; PNC 30% vs 15%, Wells Fargo 25% vs 12%, JPMorgan Chase 25% vs 12%, M&T 22% vs 8%.

```
2017 owner-occupied purchase, lenders with 500+ Black and 2,000+ White applications
lender                        Black apps  denied%   White apps  denied%   ratio
PNC Bank                        1,004      30.4      13,083     14.9     2.04
Wells Fargo Bank                8,700      25.3     117,183     11.9     2.12
JPMorgan Chase Bank             2,357      24.5      44,532     11.9     2.07
Fifth Third Mortgage              625      24.5      10,358     11.3     2.16
Manufacturers and Traders       1,133      22.2       5,243      8.4     2.64
NVR Mortgage Finance            3,253      17.2       7,820      6.4     2.68
Barrington Bank & Trust           550      15.1       6,220      4.5     3.33
```

- **Checked:** HMDA historic is 2015-2017 with respondent ids, not LEIs. Lender names came through the ARID-to-LEI crosswalk once the key was rebuilt as agency code plus respondent id without leading zeros. Denial is action 3 over actions 1-3.
- **Hit means:** the raw denial gap, before income or credit. Reveal reported this shape in 2018 from the same file.
- **Miss means:** the FDIC LEI link did not connect, so no branch-deposit column. The crosswalk carries LEIs the FDIC file does not.
- **Boring explanation:** income and credit score. Not in this table for 2017. Needs the modern LAR, which here is DC-only.

Tables: `HOUSING__FED_CFPB_HMDA_HISTORIC` → `HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF`. Join agreement: names resolve for most banks and nonbanks; EIN-style respondent ids stay unnamed.
Names: data match, not verified against primary records.
Skeptic: **not sent.** Known shape, single source. SQL: `sql/10_hmda_2017_denial_gap_by_lender.sql`.

---

## B8. Co-authors of ORI-retracted papers kept getting NIH money

**Headline:** 76 US authors named on papers retracted after an Office of Research Integrity investigation received $187M in NIH awards after the retraction date.

```
ORI-retracted paper authors, US, 2010-2025        757 names
matched to exactly one NIH investigator profile   131
with NIH awards after the retraction               76
NIH dollars after                                  $187.2M
top, awards after retraction
  Roger J Colbran, Vanderbilt        7 retractions 2015   15 awards  $32.4M
  Richard I Fisher, Fox Chase        4 retractions 2019   18 awards  $21.3M
  Amy J Wagers, Joslin               1 retraction 2012    45 awards  $20.1M
```

- **Checked:** author names split on ";", last word and first word matched to NIH PI names. Kept only names that map to one NIH profile id, so "Wei Wang" and "Mark Anderson" dropped out. Award notice date must be after the retraction date.
- **Hit means:** a named co-author of a paper ORI found tainted went on to win NIH grants. It does not mean that person committed the misconduct. ORI usually names one respondent, often a trainee; senior authors are co-authors.
- **Miss means:** the respondent list is not in the warehouse. Without it the finding cannot separate the guilty party from the lab head.
- **Boring explanation:** NIH keeps funding senior scientists whose trainees fabricated data. That is the expected policy and it is what the data shows.

Tables: `SCIENCE_RESEARCH__FED_RETRACTION_WATCH` → name → `SCIENCE_RESEARCH__FED_NIH_REPORTER`. Join agreement: profile-id uniqueness enforced; middle initials not compared.
Names: data match, not verified against primary records.
Skeptic: **not sent.** Framing caveat is the whole story. The closing skeptic reads this as C by its own text; kept at B under the prompt's definition, real but needs outside reporting. Chris decides. SQL: `sql/06_ori_retraction_coauthors_nih_after.sql`.

---

## B9. Banking Committee senators traded bank stocks above their share

**Headline:** senators on the Banking Committee were 19% of trading senators but made 34% of senators' bank-stock trades in 2012-2020.

```
sector       trades   by overseeing-committee members   share of traders on that committee
banking        391          133   34.0%                 19.4%
health         484          197   40.7%                 43.2%
energy         403           99   24.6%                 44.6%
defense         87            7    8.0%                 29.5%
named
  Perdue, Banking       78 bank trades 2017-20   JPM, BAC, C, WFC, USB, STT
  Toomey, Banking       25                        BBT, BAC
  Moran, Banking        24                        WFC, JPM, USB, GS, BAC
```

- **Checked:** 8,350 trades, 57 senators, 2012-06 to 2020-12. Ticker to CIK via EDGAR tickers, CIK to SIC via EDGAR financials, 4,576 of 6,239 ticker trades got a sector. Committee membership by Congress from the unitedstates project.
- **Hit means:** banking is the one sector where committee members over-trade their own turf. Health and energy sit at or under base rate.
- **Miss means:** the SIC map is hand-made and coarse; "other" holds 2,273 trades. Three senators drive the banking number.
- **Boring explanation:** Perdue. Remove him and the banking share drops toward base rate. Say so.

Tables: `POLITICS__SENATE_TRADES` → `FINANCE__FED_SEC_EDGAR_COMPANY_TICKERS_EXCHANGE` → `FINANCE__FED_SEC_EDGAR_FINANCIALS` → `POLITICS__FED_CONGRESS_COMMITTEE_MEMBERSHIP`. Join agreement: 73% of ticker trades reach a SIC; CIK widths differ, joined as numbers.
Names: data match, not verified against primary records.
Skeptic: **not sent.** Thin. The closing skeptic reads this as C because Perdue drives it; kept at B because the base-rate test is real and the boring explanation is named. Chris decides. SQL: `sql/08_senate_trades_vs_committees.sql`, `08b_senate_base_rate.sql`.

---

## B10. Coal controllers with the most serious violations per miner

**Headline:** among mine controllers with 500+ employees, eight coal owners logged 900 to 1,960 significant-and-substantial violations per 1,000 miners in 2018-2024; Foresight Energy paid 48% of its proposed fines, Warrior Met 60%, the rest 70-84%.

```
controller                      miners   S&S per 1,000   deaths   fines proposed   paid
Sev.en Global Investments        1,775      1,963           2        $15.6M         75%
Foresight Energy Labor             558      1,955           0         $6.2M         48%
Coronado Coal                      824      1,757           1         $4.7M         77%
Warrior Met Coal                 1,302      1,513           1         $6.4M         60%
Ramaco Resources                   810      1,454           1         $4.9M         70%
ACNR Holdings                    2,287        962           2         $9.1M         77%
Alliance Resource Partners       2,979        932           6         $7.1M         82%
Alpha Metallurgical              3,185        925           3        $15.2M         84%
```

- **Checked:** violations 1994-2026, accidents 2000-2026, mines with current controller and employee counts. S&S is the inspector's own flag for a violation likely to cause serious injury.
- **Hit means:** per miner, these owners get cited for serious hazards at ten to forty times the rate of the big aggregate companies.
- **Miss means:** employee counts are current, violations are 2018-24; a controller that shed mines looks worse. Fines paid lag proposed fines while contests run.
- **Boring explanation:** underground coal is inspected four times a year by law; quarries twice. Rate per inspection-day would be fairer. Not run.

Tables: `LABOR__FED_MSHA_VIOLATIONS`, `LABOR__FED_MSHA_ACCIDENTS`, `LABOR__FED_MSHA_MINES`, on controller id. Join agreement: id join, names carried on every table and match.
Names: data match, not verified against primary records.
Skeptic: **not sent.** Single domain; the cross-domain half is in B6. SQL: `sql/09_msha_controllers.sql`.

---

## C. Clean misses

| # | What was tried | What happened | Why it matters |
|---|---|---|---|
| C1 | FDIC enforcement orders 2019-24 vs branch deposit growth 2018-24 | banks under orders grew 51.7%, others 49.1% | orders do not dent deposits; do not build on it |
| C2 | CFPB complaints vs FDIC-ordered banks by name | 2 of 30 bank names match | "Truist Bank" vs "Truist Financial"; needs a cert-to-company map |
| C3 | EPA corporate crosswalk, parent penalties vs PACs | UPS shows $503M; ECHO TOTAL_PENALTIES repeats shared-case penalties per facility; PAC name match fired on "United Airlines" | use LAST_PENALTY_AMT_ALLOCATED and the EPA_PENALTY_GAP mart; never first-word PAC matches |
| C4 | GHGRP top emitters vs ECHO enforcement | CO2E_EMISSION is null on about 30% of 2023 rows, including the biggest; deciles 8-10 empty | fix the emissions load before ranking emitters |
| C5 | PPP loans $150K+ vs SAM exclusions by name and state | only EPA facility listings match; they do not bar PPP | clean miss; debarred firms did not take big PPP loans under their own names |
| C6 | MSHA controller names vs FEC employer text | 1 hit | employer strings are subsidiaries ("Alliance Coal"); go through SEC insiders instead |
| C7 | LDA lobbying clients vs contract recipients by name | 995 names match 2019-24 | join works; no angle found in the time |
| C8 | ICE deaths per 100,000 stints by facility type | Federal/USMS 3.3, dedicated 1.9, hold rooms 0.5; 37 deaths total 2022-26 | too few deaths to rank facilities; Stewart, Moshannon, CCA Florence have 3 each |
| C9 | Judges, first two passes | bank names hit checking accounts; "cisco" hit "Francisco"; 300 s timeout on a 190-pattern scan of 71M dockets | filter dockets to holders first, then match; stock-only holdings |

SQL for the misses: C1 and C2 in `sql/C1_fdic_orders_vs_deposits.sql`; C3 in `C2_epa_parent_penalties_pac.sql`; C4 in `C3_ghgrp_emitters_vs_echo.sql`; C5 and C8 in `11_ice_deaths_ppp_vs_sam.sql`; C6 in `C4_msha_controller_vs_fec_employer.sql`; C7 in `C5_lda_clients_vs_contracts.sql`; C9 is the history of `02_judges_stock_in_parties.sql`.

---

## New traps found this hunt

- `HEALTH__FED_CDC_INJURY_VIOLENCE_COUNTY.COUNT_SUP` is the death count; null means suppressed. Saved to memory.
- `JUSTICE__FED_COURTLISTENER_FINANCIAL_DISCLOSURES.YEAR_COL` holds junk below 2000 and above 2030 on 300+ rows; filter to 2003-2020. `PERSON_ID` is null on 56% of rows.
- `JUSTICE__FED_COURTLISTENER_DOCKETS.DATE_FILED` runs 1871 to 2079.
- `ENVIRONMENT__FED_EPA_GHGRP_EMISSION.CO2E_EMISSION` is null on roughly a third of 2023 rows.
- `HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF.ARID_2017` = agency code + respondent id with leading zeros stripped.
- `ECONOMICS__FED_USASPENDING_CONTRACTS` is 2024-2025 only; the full history is `_FULL_R2`, 93M rows, ACTION_DATE as text, 150 s per full scan.
- `POLITICS__SENATE_TRADES` ends 2020-12.
- FEC `DONOR_NAME` has a space after the comma; split then trim, or the first name is empty.
