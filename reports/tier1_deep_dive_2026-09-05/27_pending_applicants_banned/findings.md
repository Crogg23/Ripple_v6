# Hunch 27 — are any pending Medicare applicants already banned for past fraud?

Snapshot: pending list landed 2026-07-26; LEIE landed late Aug 2026 (max exclusion date 2026-08-20).
Terms, once: NPI = the 10-digit National Provider Identifier every clinician gets once. LEIE = the HHS OIG list of people currently banned from billing federal health programs. CCN = CMS Certification Number, one per facility.

## What was checked
- Pending list = two CMS files, physicians (7,240 rows) + non-physicians (6,880). 14,120 rows, 14,103 distinct NPIs. 17 NPIs sit in both files under the same name. Zero blanks, zero malformed, zero sentinel.
- LEIE mart: 83,747 rows. 74,908 have a blank NPI (the landing file has 75,001 rows of NPI `0000000000`; the mart blanks them). 8,660 distinct real NPIs.
- Join: deduped pending NPI = LEIE NPI, real NPIs only.
- Names compared on both sides. Facility affiliation and NPPES checked for the hits.

## The number
- **9 people.** Rebuilt two ways: union-then-dedupe join = 9; EXISTS per file with no union = 7 physician + 3 non-physician = 9 distinct. First pass reproduces.
- The naive row join says 12: Tommy Louisville is in both pending files and carries two exclusions, so he counts 4 times. 12 rows, 10 exclusions, 9 people.
- Last and first name match LEIE exactly on all 10 rows. Not an NPI typo.

## The nine

| Name | NPI | pending file | LEIE category | code | what the code means | excluded | state, city |
|---|---|---|---|---|---|---|---|
| Daniel Hauser | 1861424954 | physician | Physician (MD/DO), general practice | 1128a4 | felony, controlled substance | 2013-04-18 | FL, Miami |
| Gary Kushner | 1366450280 | physician | Physician (MD/DO), general practice | 1128a1 | conviction, program-related crime | 2013-10-20 | NC, Butner |
| Tommy Louisville | 1225139496 | both | Physician (MD/DO), general practice | 1128b4 then 1128a1 | license revoked (2020), then conviction (2024) | 2020-09-20, 2024-05-20 | FL, Pembroke Pines |
| Enrique Rodriguez | 1336103548 | physician | Chiropractor | 1128b4 | license revoked | 2020-10-20 | FL, Pembroke Pines |
| Ingrid Sanchez | 1083786099 | non-physician | Business owner/exec, mental health (LCSW) | 1128a1 | conviction, program-related crime | 2021-11-18 | NV, Henderson |
| Clara Salazar-Vust | 1689740714 | physician | Physician assistant | 1128a3 | felony, health care fraud | 2022-06-20 | FL, Miami |
| Gerald Abraham | 1386606325 | physician | Physician (MD/DO), pain management | 1128a4 | felony, controlled substance | 2022-08-18 | FL, Coleman |
| Michael Scheer | 1639294796 | physician | Physician (MD/DO), internal medicine | 1128b4 | license revoked | 2022-10-20 | FL, Jacksonville |
| Eugene Lewis | 1164538013 | non-physician | Nurse (CRNP) | 1128a4 | felony, controlled substance | 2025-11-20 | PA, Leeper |

## Reinstated?
- **None.** But not because a check said so: the LEIE monthly file only holds people currently excluded. Reinstated people leave the file.
- REINDATE is `00000000` on all 83,842 landing rows. Mart `WAS_REINSTATED` is false on all 83,747, `REINSTATEMENT_DATE` blank on all. Those two mart columns are dead. Trap.
- Mandatory (1128a) exclusions have a 5-year floor and end only on application. Hauser and Kushner: 13 years and still listed.

## Physician vs non-physician
- 6 only in the physician file, 2 only in the non-physician file, 1 in both (Louisville).
- The file label is loose: Rodriguez (chiropractor, NPPES taxonomy 111N) and Salazar-Vust (physician assistant, PA-C) are in the physician file. Do not use the file as a credential.

## Exclusion class
- 7 of 9 mandatory (1128a: a conviction or felony), 2 of 9 permissive (1128b4: license lost). Louisville counted on his latest, 2024, exclusion.
- Base rate across the 8,810 real-NPI LEIE rows with a 1128 code: 63% mandatory. Nine is too few for the gap to mean anything. What it does say: these are not soft cases.

## State
- FL 6, NC 1, NV 1, PA 1.
- Base rates (no limit, `queries4.py`; NC 3.3% pending / 1.5% LEIE, NV 0.95% / 2.4%, PA 4.4% / 4.7%): Florida is 12.3% of the pending list (by NPPES practice state, 13,290 of 14,103 resolve) and 9.6% of real-NPI LEIE rows. Six of nine is well above both. Nine is still nine; Florida would be the modal state at either base rate.
- Cities: Miami x2, Pembroke Pines x2, Jacksonville, Coleman FL, Butner NC, Henderson NV, Leeper PA. LEIE address is the address at exclusion time.

## Facility affiliation
- **0 of 9** appear in HEALTH__FED_CMS_FACILITY_AFFILIATION (2,260,193 rows, 940,350 distinct NPIs, no sentinel).
- Expected miss: only 152 of 14,103 pending applicants (1.1%) are in that file at all. It lists people already billing Medicare; pending applicants by definition mostly are not.

## New: two dead NPIs
- NPPES says Kushner's NPI was deactivated 2015-08-31 and Hauser's 2018-06-19; name and state are blanked on both records. Neither has a reactivation date.
- A first-time Medicare application pending in July 2026 on an NPI that has been dead for 8 and 11 years. Either CMS's pending file carries stale rows, or someone applied on a dead number. Not answerable from here.

## What a hit means / what a miss means
- Hit: a person OIG currently bars from all federal health programs has a Medicare enrollment application in the queue. CMS is required to deny; the pending file is a snapshot of the queue before that decision, so the hit is "the screen has not fired yet," not "CMS enrolled them."
- Miss (the other 14,094): not on LEIE by NPI. It does not mean clean; LEIE rows without an NPI (75,001 of 83,842, 89%) cannot be matched this way. Nine is a floor.
- Ceiling, not a finding: the skeptic's first+last name match against the no-NPI LEIE rows returns 450 hits, 37 with a matching state. Common names make both noisy (2026-09-03 surname trap). The true count sits between 9 and 37; nothing above 9 is verified.

## What a skeptic would attack
- "12 hits in the first join." Answered: 12 rows, 10 exclusions, 9 people.
- "Same NPI, different person." Answered: names match exactly on all 10 rows.
- "Maybe reinstated." Answered by construction: reinstated people are not in this file. The mart's reinstatement columns are empty and cannot answer it.
- "Nine of 14,103 is 0.06%, why care?" Fair. The value is the list itself, nine names with codes, not a rate. The seven-of-nine felony/fraud share and the two dead NPIs are what make it more than a rounding error.
- "The pending file may be stale." Real. The two dead NPIs are evidence for it. Cannot tell a stale queue row from a live bad application without a second snapshot of the pending file.
- "Only 88% of pending NPIs resolve to an NPPES state." The 813 that do not are excluded from the state base rate, which is a share of 13,290 not 14,103.

## Traps found
- LEIE mart `WAS_REINSTATED` false on 100% of rows and `REINSTATEMENT_DATE` blank on 100%: the source file is active-exclusions only; landing `REINDATE` = `00000000` on all 83,842 rows. The columns exist, the data does not.
- LEIE mart blanks the `0000000000` sentinel (landing 75,001 sentinel rows, mart 74,908 blank; the mart is 95 rows short of landing, 93 of them sentinel rows, distinct real NPIs equal at 8,660). Filter by `NPI_IS_REAL` or `trim(NPI)<>''` in the mart; filter the literal sentinel in landing.
- Landing `INGESTED_AT` on LEIE is epoch microseconds (1787843027544807), same as the 2026-09-02 trap, one more table.
- The physician/non-physician file split is not a credential: a chiropractor and a PA sit in the physician file.

STATUS: confirmed as written
HEADLINE: 9 pending Medicare applicants (of 14,103) are on the OIG ban list under the same NPI and name; 10 active exclusions, 0 reinstated, 7 of 9 for a felony or fraud conviction, 6 of 9 in Florida, and 2 of the 9 NPIs were deactivated years ago.
