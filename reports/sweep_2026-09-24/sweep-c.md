# Sweep 2026-09-24: sweep-c

25 rows: 15 hops, 10 rollups.
**1 live · 15 probed · 9 dead · 0 untouched.**
61 SELECTs (3 of them errors, rerun), plus one `ALTER SESSION` timeout per connection. Queries in `sweep-c.sql`.

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| H: ASSISTANCE_FULL → OSHA 2023 | dead | bridge `FED_US_USASPENDING_API`: 300 rows, **0** EIN, 0 DUNS, 0 UEI |
| H: CONTRACTS_FULL_R2 → OSHA 2023 | dead | same empty bridge |
| H: CONTRACTS_FULL → OSHA 2023 | dead | same empty bridge |
| H: CONTRACTS → OSHA 2023 | dead | same empty bridge |
| H: ASSISTANCE_FULL → OSHA 2024 | dead | same empty bridge |
| H: CONTRACTS_FULL_R2 → OSHA 2024 | dead | same empty bridge |
| H: CONTRACTS_FULL → OSHA 2024 | dead | same empty bridge |
| H: CONTRACTS → OSHA 2024 | dead | same empty bridge |
| H: CONTRACTS → air emissions | probed | 1,206 of 92,833 UEIs reach air (1.3%) |
| H: CONTRACTS_FULL → air emissions | probed | 31,685 of 31,685 crosswalk UEIs land. It's circular: the crosswalk was built from this table |
| H: CONTRACTS_FULL_R2 → air emissions | probed | 3,535 UEIs reach air; $631B to them; 19/20 names agree |
| H: ASSISTANCE_FULL → air emissions | probed | 857 of 354,619 UEIs reach air |
| H: OPEN_PAYMENTS_2022 → OSHA 2023 | probed | 291 of 1,217 CCNs reach OSHA (24%); years one apart |
| H: OPEN_PAYMENTS_2023 → OSHA 2023 | probed | 293 of 1,207 (24%); years line up |
| H: OPEN_PAYMENTS (2024) → OSHA 2023 | probed | 303 of 1,251 (24%) |
| R:UEI:harm-money | **live** | Amerihost Services: EPA-debarred, still got **$1.54M** in HUD Section 8 payments during the ban |
| R:UEI:worst | dead | SAM_EXCLUDED_PROVIDERS is a slice of SAM_EXCLUSIONS: 16,144/16,144 rows in both |
| R:NPI:harm-money | probed | only 1 of 6,591 LEIE-excluded NPIs drew 2024 Part B money, and he has a waiver |
| R:NPI:worst | probed | no NPI on all 3 tables; the 123 on two tables overlap by construction |
| R:CCN:harm-money | dead | 0 CCNs overlap: nursing homes and home health on one side, hospitals on the other |
| R:CCN:worst | probed | 14,632 of 14,700 homes have citations, so "on 3+ tables" catches nearly everyone |
| R:FRS_ID:harm-money | probed | penalized share goes 14% → 97% as harm-table count rises, but that's circular |
| R:FRS_ID:worst | probed | 279 sites on all 5 tables; Westlake/Shell Deer Park: 151 actions, last penalty $7.6K |
| R:NPDES_ID:worst | probed | 2,420 permits on all 5 tables; top single-event violators are city sewer plants |
| R:EIN:harm-money | probed | 5,275 OSHA EINs file single audits. They're governments |

---

## Top live rows

Only one row earned live. The two below it are the next-strongest leads, left at probed.

### 1. R:UEI:harm-money: HUD kept paying an EPA-debarred landlord (live)

- **Checked:** excluded UEIs in `FED_SAM_EXCLUSIONS` against contracts (`CONTRACTS_FULL_R2`) and grants (`ASSISTANCE_FULL`). Kept only actions dated between the ban's start and end.
  - 384 of 38,427 excluded UEIs were ever paid.
  - 138 had contract actions during a ban. Those net to −$102M: mostly contracts being wound down.
  - 38 got brand-new contracts during a ban: $1.49M in total.
- **The lead:** Amerihost Services LLC, Pittsburgh.
  - EPA ban: "Ineligible (Proceedings Completed)", 2021-09-08 to 2026-09-07.
  - HUD Section 8 project-based rental aid: 27 actions, $1.54M, dated 2021-11 to 2026-03.
  - A new FAIN each year (`WV15M000029-22Z`, `-23Z`...), so these are yearly renewals, not just the tail of an old contract.
  - UEI and name agree on both sides.
- **Runner-up:** A&S Skill Machinist, Gardena CA. Took a DLA voluntary exclusion from 2023-10-26, then got 18 new DoD contract awards ($150K) during it.
- **Hit means:** a federal agency renewed money to a firm the system had banned.
- **Miss means:** the ban had a carve-out, or the payments count as tenant aid, not a covered transaction.
- **Boring explanation:** Section 8 housing payments follow the tenants and the building. HUD may keep paying to protect tenants even when the landlord is banned. The EPA ban is likely a lead-paint disclosure case. The dollars are a floor, because this table keeps only 1M rows per year.

### 2. R:NPI:harm-money: the Medicare exclusion list holds up (probed)

- **Checked:** OIG exclusion list (LEIE) NPIs excluded before the data year, against 2024 Part B, 2022 Part D and 2024 Open Payments.
  - 6,591 excluded before 2024. **1** drew 2024 Part B money: Eduardo Miranda, Laredo, $1.23M.
  - 2 drew 2022 Part D money: Miranda ($7.7M) and Aswad, Deming.
  - All of them have `HAS_WAIVER = true`.
  - 193 excluded NPIs took 839 drug-company payments in 2024: $166K.
- **Hit means:** Medicare money went to banned doctors. It didn't, except where OIG allowed it.
- **Boring explanation:** waivers keep sole providers in underserved towns working. The drug-company payments are mostly small, and legal.

### 3. H: CONTRACTS_FULL_R2 → XC_EPA_CORPORATE_CROSSWALK → air emissions (probed, a usable join)

- **Checked:** what share of contractor UEIs reach an EPA facility through the crosswalk, and then the air-emissions table.
  - 3,535 of 582,656 UEIs reach air, covering 3,748 facilities and 223K of 10.4M air rows.
  - Names agree 19/20 on a 20-row sample.
  - The matched firms got $631B.
- **Hit means:** you can line up federal contractors with their smokestacks.
- **Miss means:** nothing yet.
- **Boring explanation:** the dollar gap between matched and unmatched firms (median $633K vs $52K) is just size: big manufacturers are both big contractors and big emitters. `POLLUTANT_NAME` is 100% filled, so the planned pollutant-name gap has nothing in it.

---

## New data traps

1. **`XC_EPA_CORPORATE_CROSSWALK.PARENT_UEI` is not a parent UEI.** It's the recipient's own UEI, matched by name from `CONTRACTS_FULL`.
   - All 31,685 values land in `CONTRACTS_FULL.RECIPIENT_UEI`.
   - Sample: Saft America's parent is TOTAL SE, but the crosswalk holds Saft's own UEI.
   - `MATCH_METHOD` and the name columns are blank on all 37,934 of those rows.
   - So any land rate measured against CONTRACTS_FULL is circular.
2. **`SAM_EXCLUDED_PROVIDERS.NPI` is a first+last+state guess against NPPES.** It gets applied even to people banned by EPA, HUD, DOJ or DOI.
   - 804 rows are name-matched; only 10 NPIs came from the SAM record itself.
   - Among the 24 top-paid matches, the SAM city and the Medicare city disagree on 24 of 24. Example: an EPA-banned "Richard Nichols, Irving TX" is paired with a Grapevine podiatrist paid $4.3M.
   - Treat these NPIs as namesakes until proven otherwise.
3. **`FED_US_USASPENDING_API` has 300 rows and blank EIN, DUNS and UEI on every row.** Eight hops list it as their bridge; it bridges nothing.
4. **Minor:** 19 rows of `NPDES_INFORMAL_ENFORCEMENT_ACTIONS.REGISTRY_ID` hold the NPDES permit ID instead of an FRS ID (like `RIU000622`).

## Checks applied

- EINs were padded to 9 digits, and zero/blank EINs dropped.
- NPIs were regex-checked for 10 digits.
- Each join got a second-field check: names, ZIPs or cities.
- Years were lined up per row, and the 1M-rows-per-year cap was noted on ASSISTANCE_FULL.
- The `IS_EXCLUDED`, `HAS_WAIVER` and `NPI_IS_REAL` flags were read before filtering on them.
