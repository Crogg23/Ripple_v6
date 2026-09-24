# sweep3-b: 25 pairs rows

**Result: 1 live, 18 probed, 6 dead.** All 25 rows are marked.
**Statements used: 17 of 120.** None errored. Each of the 10 connections also ran the one allowed `ALTER SESSION`.
The queries are in `sweep3-b.sql`.

The ledger's `mark` wrote every row, but 5 marks threw `OSError` while re-rendering `ledger/ledger.html`. Another agent was writing that file at the same time. The TSV rows are correct; I re-read them to check.

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| EO BMF × OSHA 300A 2023 | probed | 7,444 of 123,211 OSHA EINs (6.0%). State agrees 95%. 36 of 757 deaths |
| EO BMF × OSHA 300A 2024 | probed | 6,857 of 114,605 (6.0%). State 95%. 28 of 687 deaths |
| EO BMF × OSHA 300A 2025 | probed | 6,457 of 106,219 (6.1%). State 95%. 26 of 671 deaths |
| EO BMF × OSHA case detail 2025 | probed | 1,652 of 13,387 (12.3%). State 91%. 7 of 119 death cases |
| Single audit × 300A 2023 | probed | 5,183 of 123,211 (4.2%). State 99%, names 20/20. 62 deaths |
| Single audit × 300A 2024 | probed | 4,904. 70 deaths |
| Single audit × 300A 2025 | probed | 4,543. 35 deaths |
| Single audit × case detail 2023 | probed | 2,065 of 33,694 (6.1%). 20 death cases |
| Single audit × case detail 2024 | probed | 1,777 of 20,524 (8.7%). 15 death cases |
| Single audit × case detail 2025 | probed | 1,232 of 13,387 (9.2%). 12 death cases |
| IRS527 Sched B × 300A 2023 / 2024 / 2025 / case detail 2025 | dead ×4 | 0 shared EINs. The EIN belongs to the political group |
| FQHC people × DME by referrer | probed | 13,800 of 173,813 (7.9%). Last name 99.7%. Median \$7.1K vs \$9.6K |
| FQHC people × DME by supplier | dead | 1 NPI. Suppliers are companies |
| FQHC people × Part B by provider and service | probed | 24,538 (14.1%), the same set as by provider |
| FQHC people × Part B by provider | probed | 24,538. Name 99.7%, state 99.1%. Median allowed \$11.0K vs \$35.3K |
| FQHC people × MEDICARE_PROVIDER | dead | A copy of Part B by provider: all 1,296,739 NPIs have the same dollars |
| FQHC people × Open Payments 2022 | probed | 21,075. Name 95.9%. Median \$97 vs \$152 |
| FQHC people × Open Payments 2023 | probed | 23,588. Median \$109 vs \$163 |
| FQHC people × Open Payments 2024 | probed | 25,636. Median \$112 vs \$166 |
| **FQHC people × Part D prescribers** | **live** | One family NP: **\$24.9M** in DY2022, #1 of 192,211 NPs |
| FQHC people × QPP | probed | 6,883 land, but only 220 report as individuals |
| ECHO × EPA case conclusion facilities | probed | 104,659 of 105,113 (99.6%). They hold \$5.05B of ECHO's \$10.9B in penalties, but 92.5% show \$0 |

How the EIN join was run: digits only, padded to 9, `000000000` dropped. State was compared on the most common OSHA state per EIN.
How the NPI join was run: the FQHC NPI must be exactly 10 digits. Name means last name. State agrees if the other table's state is any of the NPI's FQHC site states.

---

## Live 1: the top-prescribing NP in the country, at a San Antonio FQHC address

**What was checked**
- NPI 1366754715, Kim Hinojosa. Taxonomy 363LF0000X, family nurse practitioner.
- The FQHC table puts this NPI at CommuniCare Health Centers – Northwest, 8210 Callaghan Rd, San Antonio. That's a Barrio Comprehensive Family Health Care Center site with 20 people.
  - The table says "address match only". The NPPES address equals the site address. It is not a staff roster.
- Part B 2024 billing at the same address: 106 patients, \$21K allowed. That's small.
- Part D DY2022: **\$24.9M** in drug cost, from 3,075 claims across 25 drugs.
  - That's **#1 of 192,211 nurse practitioners.** The median NP is \$18K.
  - Top drugs:
    - Epclusa (sofosbuvir/velpatasvir, hep C): \$10.9M for 151 patients
    - Rifaximin: \$4.1M for 257 patients
    - Skyrizi \$2.2M, Humira \$1.2M, Cosentyx \$1.1M, Taltz \$0.9M
- Open Payments 2022-2024: about **\$45K**, almost all from **Gilead** (maker of Epclusa) and **AbbVie** (maker of Skyrizi and Humira).
  - Most of it is speaker fees, travel and meals. All of it is in San Antonio, so the city agrees.

**What a hit means:** a primary-care NP at a safety-net clinic address writes more Part D dollars than any other NP. The two drugmakers behind about 57% of those dollars pay the same NP to speak. That's the known "speaker program + high prescriber" pattern.

**What a miss means:** the NP runs a legitimate hep C and liver program. FQHCs do run hep C cure programs. Epclusa runs about \$72K per cure, so 151 cures is \$10.9M with nothing wrong. Rifaximin fits liver patients.

**Boring explanation:** a hep C/liver clinic, plus a specialty pharmacy that routes these prescriptions under the NP's NPI. The psoriasis biologics (Skyrizi, Cosentyx, Taltz) are the part the liver story doesn't explain.
**Not checked:** other data years (only DY2022 is loaded), the supervising doctor, and whether this is a 340B contract-pharmacy setup.

## Nearest to live (probed, not live)

**1. Single audit × OSHA: deaths at public employers.**
Local governments hold 108 of the 167 deaths among matched auditees. City of Chicago has 9 over 3 years.
- A 300A death with no case rows is **not** automatically junk. Burnsville MN police reported 3 deaths in 2024 and has 1 case row. That fits the February 2024 shooting (from the news, not checked in data).
- Redmond School District (4 deaths, 2023) and Taylorville CUSD North School (2, 2024) have no death cases. Those look like entry errors, but that's not verified.

**2. Part D #3 ER doctor: one prescriber for 37,902 Shingrix patients.**
Dr. Nzeogu at Southwest Virginia Community Health, Tazewell VA. \$10.1M of his \$11.1M is Shingrix.
Tazewell County has about 40K people. **Boring explanation:** he's the standing-order prescriber for a pharmacy vaccine program. That's a trap, not a story (below).

---

## New data traps

1. **`HEALTH__FED_CMS_MEDICARE_PROVIDER` is a copy of `..._PHYSICIAN_OTHER_PRACTITIONERS_BY_PROVIDER`.** It has the same 1,296,739 NPIs with the same allowed dollars. Every pair on it exists twice in the ledger.
2. **`HEALTH__FQHC_SITE_PEOPLE` is an NPPES address match, not a staff list.**
   - A third of its rows (79,396) sit on 142 "high-density campus" sites, up to 4,727 people each, like SF General.
   - Only 14% of its 173,813 NPIs bill Part B as individuals, because FQHCs bill as facilities.
   - Its `IS_EXCLUDED` rows (a few dozen; I didn't count them all) each say the NPPES address predates the exclusion. That flag doesn't mean an excluded person works there now.
3. **A Part D "prescriber" can be a standing-order NPI.** One ER doctor is the prescriber on Shingrix for 37,902 patients. So per-prescriber rankings mix real prescribing with pharmacy vaccine programs. Drop vaccines before ranking.
4. **ECHO's `TOTAL_PENALTIES` and `FORMAL_ACTION_COUNT` cover recent years only.**
   - Facilities whose EPA case (read from `CASE_NUMBER`) is before 2016: 97% show 0 formal actions.
   - Cases from 2021 on: 9% show 0.
   - `DATE_LAST_FORMAL_ACTION` has a `1900-01-01` placeholder.
   - So "in a case but \$0 penalty" is a time-window effect, not a hidden gap.
5. Smaller: FAC `AUDITOR_EIN` lands on only 18-78 OSHA EINs. It's the audit firm, so don't use it for employer joins. The FAC state for City of Chicago's EIN reads WI because MAX() picked a stray row.

## Statement count

17 statements, plus one `ALTER SESSION` per connection (10).
