# sweep-b: 25 pairs rows

**Result: 2 live, 16 probed, 7 dead.** All 25 rows are marked.
**Statements used: 40 of 120.** Five of those errored: the first batch used the table name without its schema prefix. Each connection also ran the one allowed `ALTER SESSION`.
The queries are in `sweep-b.sql`.

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| IRS527 × OSHA case detail 2023 | dead | 0 shared EINs. The 527 EIN belongs to the political group, not the donor |
| IRS527 × OSHA case detail 2024 | dead | 0 shared EINs |
| IRS527 × OSHA case detail 2025 | dead | 0 shared EINs |
| IRS527 × OSHA 300A 2023 | dead | 0 shared EINs |
| IRS527 × OSHA 300A 2024 | dead | 0 shared EINs |
| IRS527 × OSHA 300A 2025 | dead | 0 shared EINs |
| Hospital officer pay × 300A 2023 | probed | 1,249 of 3,918 hospitals (32%). State agrees 91%, name 57% |
| Hospital officer pay × 300A 2024 | probed | 1,230 hospitals. State 92% |
| Hospital officer pay × 300A 2025 | probed | 1,195 hospitals. State 91% |
| Hospital officer pay × case detail 2023 | probed | 949 hospitals, 87,547 cases |
| Hospital officer pay × case detail 2024 | probed | 934 hospitals, 70,817 cases |
| Hospital officer pay × case detail 2025 | probed | 694 hospitals, 46,582 cases |
| Form 5500 × 300A 2023 | probed | 4,561 of 29,069 plan sponsors (16%). Name agrees 88%, state 86% |
| Form 5500 × 300A 2024 | probed | 4,365 sponsors. Name 88% |
| Form 5500 × 300A 2025 | probed | 4,115 sponsors. Name 88% |
| Form 5500 × case detail 2023 | probed | 1,537 sponsors. Name 87% |
| Form 5500 × case detail 2024 | probed | 1,237 sponsors. Name 88% |
| Form 5500 × case detail 2025 | probed | 878 sponsors. Name 89% |
| **SAM exclusions × SBIR** | **live** | 5 SBIR firms at one Newington, CT address: $13.35M in SBIR awards, then all excluded by the Air Force the same day |
| **Contracts R2 × SAM excluded providers** | **live** | ATI Government Solutions: +$6.8M in new obligations after its SBA suspension |
| Contracts FULL × SAM exclusions | probed | 344 excluded UEIs, 75 paid inside a ban window. This is the capped table; R2 replaces it |
| Contracts (FY2025) × SAM exclusions | probed | 104 excluded UEIs, 50 with actions inside a ban window, net −$3.5M |
| Assistance FULL × SAM exclusions | probed | 77 excluded UEIs got assistance. 15 were paid inside a ban window, +$4.6M gross |
| Assistance FULL × SAM excluded providers | probed | 13 were paid inside a ban window, net +$3.05M. Same two EPA-listed firms |
| SAM exclusions × NIH RePORTER | dead | 2 excluded UEIs, no grant started after either ban |

How the EIN join was run: EINs were stripped to digits and padded to 9. Rows of `000000000` were dropped. In 2023, 7% of OSHA 300A EINs had only 8 digits.
How the UEI join was run: a dollar counts as "inside the ban window" when the action date falls between `ACTIVATION_DATE` and `TERMINATION_DATE`. A blank termination date means the ban has no end.

---

## Live 1: the Newington, CT cluster (SAM exclusions × SBIR)

**What was checked**
- 14 excluded UEIs hold SBIR awards.
  - Every one of the 14 names agrees with its SAM record (Jaro-Winkler 85 or higher).
  - None of the 14 got an award after its exclusion.
- 5 of the 14 list the same street address: **549 Cedar St, Newington, CT**. They are Beacon Industries, Neoskye, Syrnatec, Skystocks and Bryka.
- SBIR money to those 5 firms: **$13.35M in 41 awards, 2021-2025**, from:
  - Air Force, Army, Navy, Missile Defense Agency, DLA, DARPA, Space Development Agency
  - NASA
  - CDC
- The Mirchandani family is listed as principal investigator (lead researcher) at all 5 firms: Yash, Suresh, Nishita and Karishma.
- On 2026-07-17 the Air Force excluded **11 firms and 5 people** at that address. The status is "proceedings pending."
  - The 11 firms include two firms with no SBIR awards (Myoniks and Fabulous R&D) and Bryka arms in Mumbai and Newington.
  - The 5 people include four Mirchandanis.
- In contracts R2, the same UEIs hold **$38.7M** in obligations. Beacon has $28.1M of it, going back to 2006.
- No contract action is dated after the exclusion. R2 only runs to 2026-08-21, five weeks after the ban, so that zero is a floor.

**What a hit means:** one family ran five SBIR firms from one address and won across a dozen agencies. The Air Force has now barred all of them. This is the known pattern of an "SBIR mill" (duplicate or recycled proposals).

**What a miss means:** the firms are legitimately separate and the Air Force case gets dropped. "Proceedings pending" is not a finding of fault.

**Boring explanation:** small tech families often run several SBIR firms, and that is legal. The exclusion is already public. The new part is the total across agencies that never flagged the firms.

## Live 2: ATI Government Solutions after its SBA suspension (Contracts R2 × SAM excluded providers)

**What was checked**
- 384 excluded UEIs appear in contracts R2. Of those, 366 are in the SAM excluded providers table. Names agree on 94%.
- Lifetime obligations to them: $5.19B.
- 138 of them had actions dated inside a ban window:
  - net −$102M, mostly de-obligations (money pulled back)
  - gross **+$16.2M** in new money
- ATI Government Solutions was suspended by SBA on 2025-10-21, "proceedings pending."
  - After that date: 51 actions, net −$52.6M.
  - But **+$6.8M in positive obligations**, from DOE, Treasury, DOL, USDA and DoD, through 2026-08-11.
  - ATI's lifetime total in R2 is $261M.

**What a hit means:** agencies kept adding money to a suspended contractor.

**What a miss means:** the positive lines are funding added to task orders that already existed. FAR 9.405-1 allows that during a suspension.

**Boring explanation:** that FAR 9.405-1 rule, plus clawbacks on the same contracts landing as offsetting lines. The next check is to read the 51 transaction descriptions.

## Nearest third (probed, not live): money after an EPA listing

Bonus Environmental has been EPA-listed since 2012. Since then it got $839K over 28 contract actions in R2, through 2026-05.
Two firms got grant or loan money after an EPA listing: Overseas Shipholding ($2.9M, listed in 2007) and Amerihost ($1.54M, listed in 2021).
**Boring explanation:** an EPA listing under the Clean Air Act or Clean Water Act bars only the facility that broke the law. The company can still get federal work done anywhere else. I left these as probed for that reason.

---

## New data traps

1. **Three Form 5500 columns are 100% empty: `EIN`, `NET_ASSETS_EOY_AMT` and `TOTAL_ASSETS_EOY_AMT`.** 33,484 rows. `FORM_YEAR` is empty too.
   - The employer's EIN is in `SPONS_DFE_EIN`.
   - There are no dollars in this table. They live in Schedules H and I, which aren't loaded here.
   - Participant counts are filled.
2. **`DATE_OF_DEATH` in OSHA case detail 2024 is blank on every row.** Deaths show only as `INCIDENT_OUTCOME = '1'`: 201 rows.
   - In 2023 and 2025, the date is filled on all the death rows (282 and 130).
   - So a death count built on the date column reads 0 for 2024.
3. **SAM_EXCLUDED_PROVIDERS is not a table of health providers.**
   - All 16,144 of its rows are also in SAM_EXCLUSIONS, matched on `SAM_NUMBER`.
   - It holds exclusions by agencies other than HHS, OFAC and OPM, with a guessed NPI attached. Its rows include Air Force and EPA contractors.
4. **The memory note on the assistance cap looks stale** (`trap-usaspending-assistance-1m-per-year-cap`).
   - FED_USASPENDING_ASSISTANCE_FULL now holds 128M rows.
   - Row counts vary by year: 25.2M in FY2020, 1.0M in FY2007.
   - Every fiscal year runs from Oct 1 to Sep 30.
   - Not checked day by day. It looks reloaded, not verified.
5. Smaller: OSHA 300A `TOTAL_DEATHS` sometimes claims deaths the case log doesn't have. Rosen Hotels reported 10 in its 2025 summary and 0 death cases.
   - Where a site has case rows, the two sources mostly agree: 11 of 286 death sites disagreed in 2023.
   - Most sites that report a death have no case rows at all, so they can't be checked.

## Other notes

- The IRS527 EIN is the political group's own: RGA, DGA, ActBlue, the AFSCME and SEIU political funds. There are 3,299 groups. The donor's employer is free text with no EIN, so a join to employers can't happen through this column.
- Hospital officer pay × OSHA: in the 20-row sample, nearly every name "miss" was a hospital system name against a campus name. Taylor Regional Hospital's EIN lands on a nursing home it owns.
- FED_USASPENDING_CONTRACTS covers FY2025 only: 2024-10-01 to 2025-09-30.
