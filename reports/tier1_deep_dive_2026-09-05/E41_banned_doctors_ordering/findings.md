# E41 — Can hospitals still order through banned doctors?

**One-line answer:** 38 banned clinicians sit on CMS's Order and Referring file. 31 are file lag. 7 are old bans CMS never pulled — and 2 of those 7 hold an OIG waiver that makes it legal.

## Words, once
- **NPI** — the ten-digit number every clinician bills Medicare under.
- **LEIE** — the OIG list of people banned from federal health programs. `HEALTH__FED_HHS_OIG_LEIE`, 83,747 rows, landed 2026-08-27, exclusions through 2026-08-20.
- **Order and Referring file** — CMS's list of every NPI allowed to order Part B tests, medical equipment (DME), power wheelchairs (PMD), home health (HHA) and hospice for Medicare patients. `HEALTH__FED_CMS_ORDER_AND_REFERRING`, 2,018,354 rows, landed 2026-08-05. No date column of its own.

## What was checked, and the number

**The join.** LEIE real NPIs (8,660 distinct — 74,908 rows carry the sentinel `0000000000`) joined to the ordering file on NPI.
- Marts: **38** matches, 38 distinct on both sides.
- Rebuilt on the raw landing tables with text dates: **38** total, **26** excluded before `20260805`, **7** before `20250101`. First pass reproduces exactly.

**Exclusion date vs the file's own date.** The ordering file has no vintage; 2026-08-05 is our load stamp, the only clock.

| bucket | n | what it means |
|---|---|---|
| excluded on/after 2026-08-05 (all 2026-08-20) | 12 | banned after the file was cut — not a finding |
| excluded Feb–Jul 2026, 1–6 months before load | 19 | inside normal lag (see next) |
| excluded before 2025 (2015, 2020, 2021, 2023, 2024 x3) | **7** | the lag story does not cover these |

**Is lag real?** Match rate by year of first exclusion, all 8,660 real NPIs:
- 2010–2024: 0 to 3 per year, 7 total across fifteen years.
- **2025: 0 of 687** (671 still active in NPPES, so it is not dead NPIs).
- **2026: 31 of 531.**
- Hit = CMS has not yet pulled the name. Miss = it has. The 2025 zero says CMS does pull them, within roughly a year. The 7 survivors from 2015–2024 are the anomaly.

**Reinstatement.** `REINDATE` is `00000000` on all 83,842 rows; the mart's `WAS_REINSTATED` is false everywhere. OIG removes reinstated people rather than dating them, so everyone on the list is still excluded as of 2026-08-27. None of the 38 are reinstated.

**Waiver.** `WAIVERDATE` is dated on 3 rows in the whole list (a fourth row has a state and no date). **2 of the 3 are among the 7:**
- Miranda, internal medicine, TX — excluded 2015-06-18 under 1128(a)(1) (program-related crime, mandatory), waiver for TX dated the same day.
- Fraser, family practice, NE — excluded 2021-08-19 under 1128(a)(4) (felony controlled substance), waiver for NC dated 2023-03-24; NPPES practice state is NC.
- A waiver lets an excluded clinician keep serving a state's program. Those two are legal by design. That leaves **5** with no cover: Patel (OR, 2020, felony drugs), Barker (IL, 2023, kickbacks), Sicuro (MO, 2024, program crime), Gray (CA, 2024, kickbacks), Syed (CT, 2024, kickbacks).

**Exclusion type.** 1128(b)(4), state license revocation, is 30% of the list but 58% of the 38 (22) — the newest, fastest-growing type, which fits lag. Among the 7 old ones it is zero: 2 mandatory program-crime, 2 felony drug, 3 kickback/fraud (b)(7).

**Ordering categories.** `DME` is Y on 2,018,350 of 2,018,354 rows — a constant, no signal. Selective flags: 21 of 38 can certify hospice, 26 home health, 27 Part B. Of the 7 old ones, 4 can order everything including hospice (Miranda, Fraser, Gray, Syed).

**State.** The 7: TX, OR, NE, IL, MO, CA, CT — no cluster. All 38: FL 8, TX 4, CA 4, then ones and twos. 10 of 38 do not match state between the exclusion record and NPPES: 9 practise elsewhere, 1 has a blank NPPES record.

**Identity.** All 38 match by last name across LEIE, the ordering file and NPPES except one: NPI 1780044115 reads Quinn on LEIE and Browning on both CMS files — same NPI, a name change, not a wrong join. 37 of 38 NPIs are live in NPPES; Adams (NC, excluded 2026-08-20) was deactivated 2025-07-29 and is still on the ordering file.

**Did they actually order?** The DME-by-referrer file (381,228 referrers, one data year, no year column, vintage unproven) lists 9 of the 38 as paid referrers, $130,153 in Medicare payments combined. Miranda is one: 1,343 services, $46,385 paid, eight years after his ban — but his Texas waiver makes that likely legal. The other 8 were excluded in 2026, so their payments predate the ban.

## What a skeptic would attack
- "2026-08-05 is your load date, not CMS's." True. The file has no vintage. But the 7 are 8 months to 11 years old; no plausible CMS publication date rescues them.
- "LEIE reloaded after the ordering file — you are comparing a newer ban list to an older permission list." True for the 12 dated 2026-08-20, which is why they are out of the count. The 7 predate both loads by over a year.
- "Maybe the 7 were reinstated and the list is stale." The list is the current monthly full file; OIG removes reinstatements. `REINDATE` carries nothing on any row, so the check is structural, not per-person.
- "Sentinel NPI." Ruled out both ways — the mart blanks it (0 rows read `0000000000`, 74,908 read empty), the landing rebuild filters it explicitly. Count distinct on both sides equals 38.
- "Is 5 of 8,660 a story?" As a system, no: CMS's scrub works — 0 of 687 for 2025. As five named people banned for fraud, drugs and kickbacks who can still certify hospice and home health, yes — but it is five people, not a loophole.

## The answer
CMS does pull banned doctors from the ordering file, and does it within a year. The loophole is not systemic.

**Limit:** only 8,839 of 83,747 LEIE rows (10.6%; 8,660 distinct NPIs) carry a usable NPI. "System works" and "5 with no cover" are statements about NPI-bearing exclusions only; the 5 is a floor. What is left is 7 old bans that slipped through, 2 of them lawful under an OIG waiver, and 5 with no paper covering them.

STATUS: confirmed but reframed
HEADLINE: 7 clinicians banned in 2015–2024 are still on CMS's ordering list — 2 hold waivers, 5 have no cover; CMS pulled all 687 banned in 2025, none remain — the system works for NPI-bearing exclusions and these are the leaks.
