# Sweep 2026-09-24: sweep3-c

20 rows, all hops.
**0 live · 11 probed · 5 dead · 4 skip · 0 untouched.**
16 SELECTs (one was a column-name error, rerun), plus one `ALTER SESSION` timeout per connection. Queries in `sweep3-c.sql`.

Reused, not re-measured:
- The Open Payments → hospital crosswalk → OSHA route (sweep-c, sweep2-c). About 24-30% of CCNs land, and the EIN is the health system's.
- `XC_EPA_CORPORATE_CROSSWALK.PARENT_UEI` is the recipient's own UEI, taken from CONTRACTS_FULL. So any CONTRACTS_FULL land rate is circular.

The crosswalk, measured once for all EPA tables. These are the facility IDs that reach a UEI:

| EPA table | Facility IDs | IDs in crosswalk | UEIs | UEIs in SAM exclusions |
|---|---|---|---|---|
| ICIS-air facilities | 266,026 | 4,250 | 4,193 | 2 |
| FEC case conclusions (`FACILITY_UIN`) | 105,113 | 2,460 | 2,427 | 3 |
| FEC informal actions | 14,606 | 464 | 461 | 0 |
| ECHO | 3,135,554 | 24,916 | 23,084 | 13 |
| Penalty gap | 93,808 | 1,251 | 1,244 | 1 |

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| H: OP2023 → OSHA CD2025 | probed | 202 of 1,207 CCNs (17%). At hospitals, patient violence is 7.9% of cases where the EIN took drug-company money, vs 6.4% elsewhere |
| H: OP (2024) → OSHA CD2025 | probed | 211 of 1,251 (17%). Same violence gap: 0.31 vs 0.26 cases per 100 full-time workers |
| H: OP → 300A 2023 | dead | 358 of 1,251 (29%). No gap on the 2024 file; 2023 not rerun |
| H: OP → 300A 2024 | dead | 371 of 1,251 (30%). Hospital median injury rate is flat by drug-money tier: 3.8 / 4.5 / 4.4 vs 4.3. Only 2 hospital deaths in the whole file |
| H: OP → 300A 2025 | dead | 350 of 1,251 (28%). Same as 2024; not rerun |
| H: ASSISTANCE_FULL → ICIS-air | probed | 939 of 354,619 UEIs; $183B |
| H: CONTRACTS_FULL_R2 → ICIS-air | probed | 4,147 of 582,656 UEIs; $602B. 98 contractor sites have an open air-violation status |
| H: CONTRACTS_FULL → ICIS-air | probed | 4,193 of 31,685. Circular |
| H: CONTRACTS → ICIS-air | probed | 1,237 of 92,833 (1.3%); $52B |
| H: ASSISTANCE_FULL → FEC case | probed | 677 of 354,619; $132B |
| H: CONTRACTS_FULL_R2 → FEC case | probed | 2,394 of 582,656; $845B. Names agree 20/20 |
| H: CONTRACTS_FULL → FEC case | probed | 2,427 of 31,685. Circular |
| H: CONTRACTS → FEC case | probed | 762 of 92,833 (0.8%); $79B |
| H: ASSISTANCE_FULL → FEC informal | dead | 96 UEIs. They're one-off hazardous-waste (RCRA) notices at colleges and hospitals, 2002-2015 |
| H: ECHO → SAM exclusions | probed | 13 of 23,084 UEIs are excluded; names agree 13/13 |
| H: PENALTY_GAP → SAM exclusions | dead | 1 of 1,244: Seattle Barrel. EPA's own case |
| H: AIR_EMISSIONS → USASPENDING_BULK | skip | BULK is 10 days of contracts, 50K rows |
| H: ICIS-air → USASPENDING_BULK | skip | same |
| H: NPDES informal → USASPENDING_BULK | skip | same |
| H: FEC case → USASPENDING_BULK | skip | same |

---

## Top three rows

None earned live. These are the three strongest leads, all left at probed.

### 1. Contractors whose plants have an open air violation (CONTRACTS_FULL_R2 → ICIS-air)

- **Checked:** `CURRENT_HPV` values first. It's a status label, not a Y/N flag. 96.5% of sites read "No Violation Identified".
  - Any violation status: 109 of 4,618 contractor-linked sites (2.4%), vs 2,756 of 275,110 other sites (1.0%).
  - Major sources only: 34 of 394 (8.6%) vs 1,391 of 18,681 (7.4%). So the gap is mostly size.
- **Lead list:** 98 contractor sites with a live status. Contract money since 2024:

  | Site | Status | Since 2024 |
  |---|---|---|
  | Electric Boat, Groton CT | Violation within 1 year | $38.2B |
  | BAE Ordnance, Kingsport TN | Violation within 1 year | $438M |
  | Marinette Marine, WI | Violation within 1 year | $403M |
  | Blue Bird Body, Fort Valley GA | Violation-Unresolved | $108M |
  | Zimmer Biomet, Warsaw IN | Unaddressed-State | $50M |

- **Hit means:** the government keeps paying firms whose plants are in open high-priority air violation.
- **Miss means:** each violation is minor, or already settled by the state.
- **Boring explanation:** air violations don't bar anyone from contracts. Only a Clean Air Act §306 listing does. Big defense plants are big emitters.

### 2. Workplace violence at hospitals that take drug-company money (OP → CD2025)

- **Checked:** OSHA case detail 2025, hospitals only (NAICS 6221). A regex on the incident text flags assault, combative patients, punches, kicks, bites and patient strikes.
  - EINs that took drug-company money: 2,110 of 26,814 cases (7.9%), 0.31 per 100 full-time workers.
  - Other hospital EINs: 2,998 of 46,878 cases (6.4%), 0.26 per 100.
- **Hit means:** a small real gap.
- **Miss means:** the regex is picking up words that aren't violence.
- **Boring explanation:** these are teaching hospitals. Their median site has 1,396 workers vs 585, with more ERs and psych units. The next step is to compare within size bands.

### 3. EPA-banned firms among EPA facilities (ECHO → SAM)

- 13 of 23,084 crosswalk UEIs are excluded. 7 of the 13 bans are EPA's.
- View Inc. and Seattle Barrel are both current EPA bans.
- A&S Skill Machinist is sweep-c's runner-up (it got DLA awards during a voluntary exclusion).
- **Boring explanation:** the crosswalk only covers contractors, so this is a tiny slice. Sweep-c already ran the full SAM × USAspending check.

---

## New data traps

1. **`ECHO.TOTAL_PENALTIES` is not the facility total.**
   - 121,824 sites have a `DATE_LAST_PENALTY`. 100,701 of those read `TOTAL_PENALTIES = 0` while `LAST_PENALTY_AMT > 0`.
   - `LAST_PENALTY_AMT` is bigger than `TOTAL_PENALTIES` on 101,253 rows.
   - `TOTAL_PENALTIES > 0` on exactly the 21,125 rows with `PENALTY_COUNT > 0`.
   - This extends sweep3-b's "recent years only" trap. Use `LAST_PENALTY_AMT` for "ever penalized".
2. **`FEC_CASE_ENFORCEMENT_CONCLUSION_FACILITIES` has no `REGISTRY_ID`.**
   - The FRS key is `FACILITY_UIN`: 149,682 of 150,866 are 110-prefixed.
   - It also has no dates and no penalty amount, so "money after the case" can't be run off this table.
3. **`ICIS_AIR.CURRENT_HPV` is a 10-value status label.** A "not N" filter counts all 279,728 rows as violators.
4. **`PROCUREMENT__FED_USASPENDING_BULK`** is 10 days of contract actions (2026-05-26 to 06-04), 10,216 UEIs. Every hop into it is a sample.
5. **Reminder, not new:** ASSISTANCE_FULL sums to $61.3T because of the $9,999,999,999 ceiling rows. My matched-dollar totals include them, but the medians don't care.

Statement count: **16** (plus 16 `ALTER SESSION`).
