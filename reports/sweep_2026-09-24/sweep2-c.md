# Sweep 2026-09-24: sweep2-c

25 rows: 19 hops, 6 rollups.
**0 live · 19 probed · 6 dead · 0 untouched.**
34 SELECTs, plus one `ALTER SESSION` timeout per connection. Queries in `sweep2-c.sql`.

Each crosswalk was probed once, and the answer reused:
- `CORE.XWALK_HOSPITAL_CCN_EIN`: 4,003 hospital CCNs. Only 1 is in the nursing-home CCN range and 3 are in the home-health range.
- `XC_EPA_CORPORATE_CROSSWALK`: 5.3M FRS rows, 31,685 UEIs. 1,599 of those UEIs reach an NPDES informal action.
- `COURTLISTENER_SCHOOLS`: 6,011 colleges that judges attended. 3,495 rows have a usable EIN.

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| H: HOME_HEALTH → SCHOOLS | dead | 0 of 12,392 home-health CCNs are in the hospital crosswalk |
| H: NH_PENALTIES → SCHOOLS | dead | 0 of 6,831 CCNs are in the crosswalk |
| H: NURSING_HOME → SCHOOLS | dead | 1 of 14,700 is in the crosswalk; 0 reach a school |
| H: NURSINGHOME411 → SCHOOLS | dead | 1 of 14,713 is in the crosswalk; 0 reach a school |
| H: IRS527 → NH_DEFICIENCIES | dead | 0 of 3,299 political-group EINs are in the hospital crosswalk |
| H: OP2022 → OSHA CD2024 | probed | 314 of 1,217 CCNs (26%). The years are 2 apart |
| H: OP2023 → OSHA CD2024 | probed | 318 of 1,207 (26%) |
| H: OP (2024) → OSHA CD2024 | probed | 326 of 1,251 (26%). The years line up |
| H: OP2022 → 300A 2023 | probed | 346 of 1,217 (28%) |
| H: OP2022 → 300A 2024 | probed | 359 of 1,217 (30%) |
| H: OP2022 → 300A 2025 | probed | 337 of 1,217 (28%). Penn is missing from 2025, so matched $ falls from $888M to $157M |
| H: OP2022 → OSHA CD2025 | probed | 207 of 1,217 (17%). CD2025 is a partial year |
| H: OP2023 → 300A 2023 | probed | 343 of 1,207 (28%) |
| H: OP2023 → 300A 2024 | probed | 360 of 1,207 (30%) |
| H: OP2023 → 300A 2025 | probed | 338 of 1,207 (28%) |
| H: CONTRACTS → NPDES informal | probed | 564 of 92,833 UEIs (0.6%). $34B to them |
| H: CONTRACTS_FULL → NPDES informal | probed | 1,599 of 31,685 crosswalk UEIs. Circular: the crosswalk was built from this table |
| H: CONTRACTS_FULL_R2 → NPDES informal | probed | 1,590 of 582,656 UEIs; $334B. Names agree 20/20 |
| H: ASSISTANCE_FULL → NPDES informal | probed | 385 of 354,619 UEIs (0.11%) |
| R:LEI:worst | dead | 380 lenders are on all 3 tables by construction: DC-only mortgage files, one a row copy of another |
| R:EIN:worst | probed | 26,821 EINs are on both OSHA tables. Top is size: Amazon, Walmart, UPS |
| R:ICE_FACILITY:worst | probed | 593 codes are on both tables. Alexandria has 125K stints but 1 detainer |
| R:MINE_ID:worst | probed | 13,338 of 13,489 accident mines also have violations. Upper Big Branch has 31 deaths |
| R:MSHA_CONTROLLER_ID:worst | probed | Massey: 55 deaths, $73M due. Alpha has $3.7M due and not paid |
| R:PWSID:worst | probed | The PN table is a subset of violations: 387,627 of 387,627 IDs land |

---

## Top three rows

None earned live. These are the three strongest leads, all left at probed.

### 1. R:MSHA_CONTROLLER_ID: mine-safety penalties due but not paid

- **Checked:**
  - MSHA violations since 2000 and accidents, per controller.
  - 6,565 controllers are on both tables.
  - `IS_FATALITY` was read first: 1,208 true, 0 null.
- **Numbers:**

  | Controller | Deaths | Penalty due | Due minus paid |
  |---|---|---|---|
  | Massey | 55 | $73.30M | $32K |
  | Alliance | 34 | $36.77M | $0.48M |
  | CONSOL | 32 | $43.26M | $0.06M |
  | Alpha Natural Resources | 16 | $53.96M | **$3.65M** |
  | Robert E. Murray | 19 | $40.34M | **$1.92M** |

- **Hit means:** the next pass ranks controllers by penalties due but not paid, which could mean fines skipped through bankruptcy.
- **Miss means:** the gap is contested citations still open, or money paid after the snapshot.
- **Boring explanation:** Alpha and Murray both went bankrupt, so unpaid fines are expected, and already reported.
- **Also:** the per-mine list is just the known disasters: Upper Big Branch 31, Sago 12, Crandall Canyon 9.

### 2. R:PWSID: drinking-water systems that failed to warn the public

- **Checked:** whether the PN table overlaps the SDWA violations table.
  - The overlap is by construction. All 42,034 PN systems appear in violations.
  - Every `PN_VIOLATION_ID` lands as a `VIOLATION_ID`.
  - 362,005 of 387,627 `RELATED_VIOLATION_ID`s land.
- **The top list:** small PA and WV systems.
  - PA2450418 has 993 failure-to-warn violations, 2012 to 2025.
  - WV3305527 has 802.
- **Hit means:** the same systems break the rule and also never tell residents.
- **Boring explanation:** small systems, often mobile-home parks, that never file monitoring reports. Each missed report spawns its own notice violation.
- **Next:** these tables hold no system names or sizes, so the next pass needs a system-name table joined in.

### 3. H: OP → hospital crosswalk → OSHA (a usable join, but no signal)

- **Checked:**
  - 26–30% of teaching-hospital CCNs reach an OSHA filer, across all 10 year pairs.
  - Company name agrees 19/20. The site doesn't, because the EIN covers the whole system (Intermountain → an air-ambulance site in AZ).
- **Gap:** the median payment is $21K for matched CCNs, $23K for CCNs in the crosswalk that don't reach OSHA, and $12K for CCNs outside the crosswalk.
  - So the gap is a crosswalk-coverage effect (bigger hospitals get matched), not an OSHA effect.
- **Watch:** Penn's $726M 2022 royalty payment moves every matched-dollar total by itself.

---

## Other findings

- **The UEI → NPDES "after" check is moot.** The top matched contractors got their first NPDES warning letter before contract data starts in 2006:
  - Electric Boat: 1994
  - Rolls-Royce: 1990
  - Caterpillar: 1996
- **ICE facilities:** the two tables record different stages.
  - Detainers go to county jails: Harris 16.7K, Orange 7.8K.
  - Stints are in ICE centers: Alexandria 125K, Port Isabel 103K.
  - So "on both" isn't a worst list.

## New data traps

1. **`JUSTICE__FED_COURTLISTENER_SCHOOLS` is colleges, not just law schools.** The EIN is the university's.
   - Any hospital EIN that lands there is a university hospital under the same EIN, like Michigan or Penn.
   - 41 hospital CCNs land. It's a real match with no meaning.
2. **`XWALK_HOSPITAL_CCN_EIN` is hospitals only.**
   - Of 4,003 CCNs, 1 is in the nursing-home range (5000–6499) and 3 are in the home-health range (7000+).
   - So every nursing-home or home-health hop through it is dead on arrival. That's 6 routes in this batch alone.
3. **`NPDES_INFORMAL_ENFORCEMENT_ACTIONS.ACHIEVED_DATE` runs from 0001-01-01 to 8202-06-10.** Filter to 1990 through today before any "after" check.
4. **Stale trap:** the MSHA literal-quote trap no longer holds. 0 quoted `MINE_ID` or `CONTROLLER_ID` values in either table.
5. **Minor:** MSHA `CONTROLLER_ID` mixes `C02508`-style IDs with bare 7-digit ones like `0045307` (ICG) and `0041211` (Alpha).

## Checks applied

- EINs were padded to 9 digits, and zero EINs dropped.
- Company-name agreement was sampled for both crosswalks.
- Years were lined up per Open Payments / OSHA pair.
- `IS_FATALITY` values were read before filtering on them.
- Suppression: `TOTAL_DEATHS` was summed raw. Sweep-b already flagged it as inconsistent with the case log.

Statement count: **34**.
