# E62 - the sprinkler checkbox that can't say No

**The question.** Homes whose CMS directory says "automatic sprinkler systems in all required areas: Yes" - are they still being told by inspectors to install a sprinkler system?

**The two files.**
- `HEALTH__FED_CMS_NURSING_HOME` - one row per home, 14,700. Carries the flag. LANDING says the file is dated 2026-05-01 (the mart's PROCESSING_DATE is null on every row - see traps).
- `HEALTH__FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES` - 200,030 Life Safety citations, K-tags (fire) and E-tags (emergency prep), surveys 2016-07-28 to 2026-05-21, file dated 2026-06-01.
- The hunch's listed tables (`NURSINGHOME411`, `NURSING_HOME_DEFICIENCIES`) hold neither the flag nor a single sprinkler tag. Zero hits for 'sprinkler' in the health (F-tag) file.
- Join key: CCN, the CMS Certification Number, a home's federal ID. 14,700 rows / 14,700 distinct / 6 chars / zero orphans from the fire file. Clean.

## The chain

**1. The flag has three values and none of them is No.**
Yes 14,638 (99.58%). Partial 34. Data Not Available 28.
Selecting on Yes selects the whole directory. Cited homes are 99.62% Yes vs 99.58% overall - zero lift. The flag cannot find bad homes; the inspection file has to.

**2. The exact tag codes.** Eight K-tags mention sprinklers. Only one says "you don't have an approved system":

| Tag | Text | Lifetime cites, all homes | Homes |
|---|---|---|---|
| K0353 | Inspect, test, and maintain automatic sprinkler systems | 16,205 | 9,647 |
| **K0351** | **Install an approved automatic sprinkler system** | **3,781** | **3,144** |
| K0354 | Out of service more than 10 hours, wrong procedure | 1,226 | 1,072 |
| K0342 | Alarm not tied to sprinkler connection | 583 | 540 |
| K0352 | Supervisory attachments | 435 | 417 |
| K0400 | Tall-building sprinkler rule | 15 | 15 |
| K0112 / K0322 | Renovation / lab sprinklers | 3 / 1 | 3 / 1 |

(At Yes-flagged homes only, K0351 is 3,764 cites / 3,132 homes - the story chart uses that cut.)

A `LIKE '%sprinkler%'` filter blends upkeep into absence and inflates the count about 4x. This is K0351 only.

**3. First pass reproduced, a different way.** First pass used LANDING text columns with a since-2024-06-01 window. Rebuilt on the typed marts: 1,605 K0351 cites / 1,504 homes in the window, 1,500 of them flagged Yes; 64 homes open at the snapshot. Same digits.

**4. Open on flag day, no window.** Open = survey on or before 2026-05-01 AND (no correction date OR correction date after 2026-05-01).
Dropping the 2024-06-01 window adds the old waivers; adding the survey-date bound drops two homes cited after the flag existed.
**68 citations at 67 homes. 30 with no date at all.**

**5. What kind of open.**

| Status (CMS's own column) | Cites | No date | Avg days open |
|---|---|---|---|
| Deficient, provider has date of correction | 22 | 1 | 64 |
| Deficient, provider has plan of correction | 19 | 4 | 48 |
| **Deficient, provider has NO plan of correction** | **14** | 14 | 179 |
| **Waiver has been granted** | **11** | 11 | 857 |
| No revisit needed | 2 | 0 | 128 |

The 22 "date of correction" rows are promises, not revisits: four of the dates are after 2026-06-01, the fire file's own date.

**6. By state.** 23 states. Indiana 15 (all 2026 surveys, avg 35 days). Missouri 7, every one a waiver, avg 717 days. Texas 7. Minnesota 5. Hawaii 4 of just 42 Yes homes. New York 4, avg 752 days. Everyone else 1-3.
State order tracks who got surveyed in March-April 2026, not anything about the flag.

**7. How long.** Median 49.5 days. 45 of 68 under 90 days. 15 over a year: 11 waivers, 3 no-plan, 1 promised date that never came (Pearl of Crystal Lake, IL, 415 days).
Oldest row: Eddy Village Green, NY, waiver since 2019-10-09, 2,396 days - but stale, a 2025-04-03 survey did not re-cite it. Oldest that holds: Vermont Veterans' Home, no plan since 2023-10-25, 919 days.

**8. Scope.** B 1, C 3, D 12, E 32, F 20. Zero at G or above (actual harm / immediate jeopardy). 20 F-scope = widespread. None of the 68 was judged dangerous on the day.

## What a hit means
On the day CMS printed "Yes, sprinklers in all required areas" for a home, its own inspector's finding that the home needs to install an approved system was still on the books. For 14 homes the operator hadn't even filed a plan. For 11 CMS had granted a waiver - which is the case where the flag most plainly should read Partial, and doesn't.

## What a miss means
K0351 is also written for a sprinklered building missing coverage in one spot (the D/E scope rows say "isolated" or "pattern"). A Yes home with a 30-day-old K0351 and a promised date is a home going through the normal cite-fix-revisit loop, not a lie. That is 45 of the 68.

## What a skeptic would attack, and the answer
- *"68 is the normal revisit backlog."* Mostly yes. Strip everything with a plan or a date, and the candidate contradiction is 25 homes: 11 waivers + 14 no-plan. (Of the 30 no-date rows, those 25 plus 4 plan-filed and 1 date-status row with the date blank.)
- *"Some of those 25 are just stale rows."* Checked. For each of the 25, look for a later K-tag survey at the same home, on or before the flag day, and whether it re-cited K0351. **3 are stale** - a later full survey came and did not re-cite: Eddy Village Green (NY, surveyed 2025-04-03), Baisch (MO, 2025-02-28), Lakehouse (MN, 2025-08-15). Three others had a later survey that re-cited K0351, so they stand. **Durable contradiction: 22 homes - 8 waivers + 14 no-plan.** Say 22, not 68, if the claim is "flag lies."

| Home | St | K0351 survey | Status | Days open | Later K survey before flag day | Verdict |
|---|---|---|---|---|---|---|
| Vermont Veterans' Home | VT | 2023-10-25 | No plan | 919 | - | no later survey |
| OAK PARK NURSING AND REHAB CENTER | WI | 2024-07-16 | No plan | 654 | 2025-09-09 | re-cited at later survey |
| NORTHEAST CTR FOR REHABILITATION AND BRAIN INJURY | NY | 2024-11-21 | No plan | 526 | - | no later survey |
| MOUNTAIN VILLA NURSING CENTER | TX | 2025-12-04 | No plan | 148 | - | no later survey |
| NUUANU HALE | HI | 2026-02-27 | No plan | 63 | - | no later survey |
| HALE KUPUNA HERITAGE HOME, LLC | HI | 2026-03-12 | No plan | 50 | - | no later survey |
| HEBREW HOME FOR THE AGED AT RIVERDALE | NY | 2026-03-25 | No plan | 37 | - | no later survey |
| GARDENS NURSING AND REHAB CENTER | FL | 2026-03-26 | No plan | 36 | - | no later survey |
| BYRON HEALTH CENTER | IN | 2026-03-31 | No plan | 31 | - | no later survey |
| ALLISONVILLE MEADOWS | IN | 2026-04-15 | No plan | 16 | - | no later survey |
| WELLBROOKE OF SOUTH BEND | IN | 2026-04-20 | No plan | 11 | - | no later survey |
| GARNET HILL REHABILITATION AND SKILLED CARE | TX | 2026-04-23 | No plan | 8 | - | no later survey |
| Avir at Coronado | TX | 2026-04-24 | No plan | 7 | - | no later survey |
| PARK RIVER HEALTHCARE AND REHABILITATION CENTER LL | MN | 2026-04-27 | No plan | 4 | - | no later survey |
| EDDY VILLAGE GREEN | NY | 2019-10-09 | Waiver | 2396 | 2025-04-03 | STALE (later survey, no re-cite) |
| BAISCH NURSING CENTER | MO | 2022-08-05 | Waiver | 1365 | 2025-02-28 | STALE (later survey, no re-cite) |
| ASPIRE SENIOR LIVING ROARING RIVER | MO | 2024-03-01 | Waiver | 791 | - | no later survey |
| Anchorage Rehabilitation and Wellness Center | MD | 2024-03-29 | Waiver | 763 | 2025-12-10 | re-cited at later survey |
| MARANATHA VILLAGE, INC | MO | 2024-04-19 | Waiver | 742 | - | no later survey |
| SURREY PLACE ST LUKES HOSPITAL SKILLED NURSING | MO | 2024-08-01 | Waiver | 638 | - | no later survey |
| LAKEHOUSE HEALTHCARE & REHABILITATION CENTER | MN | 2024-08-01 | Waiver | 638 | 2025-08-15 | STALE (later survey, no re-cite) |
| LAKELAND HEALTH CARE CTR | WI | 2024-08-29 | Waiver | 610 | 2026-01-26 | re-cited at later survey |
| CASSVILLE HEALTH CARE CENTER | MO | 2024-10-01 | Waiver | 577 | - | no later survey |
| ST SOPHIA HEALTH & REHABILITATION CENTER | MO | 2025-01-28 | Waiver | 458 | - | no later survey |
| SUNTERRA SPRINGS INDEPENDENCE | MO | 2025-02-10 | Waiver | 445 | - | no later survey |

- *"Waivers are legal."* They are. CMS lets old buildings run under a waiver. That is exactly why the flag is the problem: the column has a Partial value and CMS printed Yes anyway on 11 waived homes.
- *"You can't see what the flag said before."* Correct. One vintage, 2026-05-01. No history. The claim is about one day.
- *"Correction dates are self-reported."* Yes; there is no revisit record in the warehouse. "Open" here means CMS's published date, nothing more.
- *"Base rate."* Conceded in step 1. The number of interest is an absolute count of one day's contradictions, not a rate.

## Traps found
- `HEALTH__FED_CMS_NURSING_HOME.PROCESSING_DATE` is null on all 14,700 mart rows; LANDING carries '2026-05-01'. Take the date from LANDING.
- `AUTOMATIC_SPRINKLER_SYSTEMS_IN_ALL_REQUIRED_AREAS` has no No value; any Yes filter is 99.58% of the directory.
- `DEFICIENCY_CORRECTED` is a status, not a boolean; 'Waiver has been granted' (2,869 rows fire-wide) is "open forever by permission." Count it separately or every old-building waiver reads as neglect.
- 4 CORRECTION_DATEs in this set are later than the file's own publication date: the column is a promise, not an event.
- The hunch's table list is wrong: flag lives in FED_CMS_NURSING_HOME, K-tags in FED_CMS_NURSING_HOME_FIRE_DEFICIENCIES.

STATUS: confirmed but reframed
HEADLINE: On the day CMS printed "sprinklers: Yes" for 14,638 homes, 67 had an open order to install one; 22 of those hold up after a stale-row check - 14 with no plan filed and 8 on a CMS waiver, the oldest sitting 919 days.
