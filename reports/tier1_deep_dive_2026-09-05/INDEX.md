# Tier 1 deep dive, 2026-09-05

21 hunches. Each folder: story.html, findings.md, queries.py, queries.log.
Every folder had a fresh-context skeptic pass, recorded in its skeptic.md; fixes applied before this index was cut. Stories are standalone: Plotly is inlined, no internet needed.

| status | count |
|---|---|
| confirmed as written | 1 |
| confirmed but reframed | 19 |
| dead | 1 |

## 2. Which nursing home owners get fined the most per home, and does it repeat?
- **confirmed but reframed**
- Bria Health Services, 15 Illinois homes, draws 5.9 fines per home and $2,172 per bed since June 2023, 2.6x its own hard state (Illinois $825 a bed, rest of US $261), first of 21 Illinois chains and of 301 nationally; its 38% repeat-tag share is survey frequency (20 visits per home vs 5), not a worse per-visit record.
- [story](02_owner_fines_per_home/story.html) · [findings](02_owner_fines_per_home/findings.md)

## 5. Do people get worse loan terms right after a hurricane or flood?
- **confirmed but reframed**
- After 2016 disasters, hit counties saw 1.1 pts more mortgage denials than the rest of their state — all of it "no reason given" — and zero change in higher-priced (rate-spread) loan share (-0.2 pts); HOEPA +1.8 per 10k rides a nationwide 2017 jump.
- [story](05_disaster_loan_terms/story.html) · [findings](05_disaster_loan_terms/findings.md)

## 15. Are banned companies still getting paid on disaster relief contracts?
- **dead**
- 26 banned companies, $169M in "disaster contracts" shrinks to $12,232 (one court-transcript vendor) once award dates are checked against ban dates; net money inside ban windows is -$403K of clawbacks.
- [story](15_banned_disaster_contractors/story.html) · [findings](15_banned_disaster_contractors/findings.md)

## 22. Do those same neighborhoods have more toxic factories today?
- **confirmed but reframed**
- Redlined (D) land is the most toxic residential land on the 1930s maps: 448 reporting toxic sites to grade A's 1, 10x the site density of A on the full facility list, and 17x the release pounds per km² within 500 m (19,670 vs 1,137 lb); an association, with ungraded industrial land as the confounder, not a cause.
- [story](22_redlined_toxic_sites/story.html) · [findings](22_redlined_toxic_sites/findings.md)

## 23. How much money did banned suppliers still collect?
- **confirmed but reframed**
- 8 DME suppliers now on the OIG exclusion list were paid $1.43B — 13% of all Medicare DME dollars in the file — with Sunshine Senior Solutions (FL) alone at $860M; all 8 were banned in June 2026, after the billing, not before.
- [story](23_banned_dme_suppliers/story.html) · [findings](23_banned_dme_suppliers/findings.md)

## 27. Are any of them already banned for past fraud?
- **confirmed as written**
- 9 pending Medicare applicants (of 14,103) are on the OIG ban list under the same NPI and name; 10 active exclusions, 0 reinstated, 7 of 9 for a felony or fraud conviction, 6 of 9 in Florida, and 2 of the 9 NPIs were deactivated years ago.
- [story](27_pending_applicants_banned/story.html) · [findings](27_pending_applicants_banned/findings.md)

## 30. Do new owners appear right after a home gets penalized, like a shell game?
- **confirmed but reframed**
- Penalized nursing homes change hands the next year at 7.9% vs 5.1% for the rest (2023 cohort; 6.0% vs 3.8% for 2024), 650 penalized homes carry a post-penalty operator record — but the first pass's 39 read a clock that stops in Sept 2024 and 13 of them are one Oregon-Washington deal.
- [story](30_penalty_then_new_owner/story.html) · [findings](30_penalty_then_new_owner/findings.md)

## 31. Do hospital-owned home health agencies perform worse but cost more?
- **confirmed but reframed**
- Among 4,766 agencies with 100+ episodes, hospital-owned home health costs 3% more per agency and 1.9% more per episode (0.9945 vs 0.9755), and on the 4,471 rated ones scores a tenth of a star lower (3.06 vs 3.17, median 3.0 both, an upper bound), but sends 5 more patients per hundred home; the 37% blank-star gap was small independents, not a bias against owned.
- [story](31_hospital_owned_hha/story.html) · [findings](31_hospital_owned_hha/findings.md)

## E38. Are drug and device companies still paying them anyway?
- **confirmed but reframed**
- $216M in industry money reached 27,547 clinicians who had opted out of Medicare before 2023, PY2022-24 — but 53% went to ten surgeons' royalties, the total fell 13% on recurring money (33% counting a one-time 2022 buyout), and the median recipient got $251.
- [story](E38_optout_doctors_paid/story.html) · [findings](E38_optout_doctors_paid/findings.md)

## E39. Do the paid ones prescribe way more opioids than unpaid ones?
- **confirmed but reframed**
- 6,477 prescribers on an opioid maker's lunch list write 38.7% of their Medicare scripts as opioids vs 3.1% unpaid, 15.8% once you match their specialty mix (2.4x, carried by NPs and PAs) — 0.46% of prescribers, 14.1% to 14.9% of Medicare opioid claims — while industry money in general moves it only 3.1% to 3.6%.
- [story](E39_paid_opioid_prescribers/story.html) · [findings](E39_paid_opioid_prescribers/findings.md)

## E40. Are brand-new doctors billing Medicare for millions in expensive wound-care products?
- **confirmed but reframed**
- At least $452M of DY2024 Medicare skin-substitute billing went to 114 NPIs that did not exist before 2022 — 85 of them over $1M each — but per patient they bill like the clinicians already in the graft business ($30k vs $27k), so the story is the graft wave and the ten individuals, not the birth year of the NPI.
- [story](E40_new_doctors_skin_substitutes/story.html) · [findings](E40_new_doctors_skin_substitutes/findings.md)

## E41. Can hospitals still legally order tests and equipment through them?
- **confirmed but reframed**
- 7 clinicians banned in 2015–2024 are still on CMS's ordering list — 2 hold waivers, 5 have no cover; CMS pulled all 687 banned in 2025, none remain — the system works for NPI-bearing exclusions and these are the leaks.
- [story](E41_banned_doctors_ordering/story.html) · [findings](E41_banned_doctors_ordering/findings.md)

## E42. Is drug industry money still being sent to them?
- **confirmed but reframed**
- $4,187,435 of PY2024 industry money went to 1,325 switched-off NPIs, 94% of it to 10 people — eight device royalties that ran the same in 2022 and 2023, one practice acquisition, one optometrist paid $538k for speaking and consulting a year after his NPI went dark; none reactivated, none excluded, none billing Part B.
- [story](E42_pharma_money_dead_npis/story.html) · [findings](E42_pharma_money_dead_npis/findings.md)

## E43. Were they already losing money before the sale?
- **confirmed but reframed**
- 55% of hospitals sold in 2023-24 (mostly 2024 sales, of those with a readable prior report: 62 of 128) were losing money on their last full-year cost report, vs 34% of hospitals not sold in the window — the first pass's 60% leans on seller stub reports.
- [story](E43_losses_before_sale/story.html) · [findings](E43_losses_before_sale/findings.md)

## E44. Did its safety violations get worse right before the fines hit?
- **confirmed but reframed**
- Bria's homes draw roughly 10x the national harm-citation rate (7.8x to 11.2x) and 13x the fine rate per home every year; immediate jeopardy went 7, 5, 17 events (2.4x 2023) while national was flat; nationally fines land in the same month as the citations (r = 0.67 at lag 0), and Bria's own series is too noisy to date the lag.
- [story](E44_violations_before_fines/story.html) · [findings](E44_violations_before_fines/findings.md)

## E47. Were they already in financial trouble before converting?
- **confirmed but reframed**
- 20 of the 24 Rural Emergency Hospital converters with a readable cost report (83%, of 48 converters total; floor 20 of 48 = 42% if every unmeasured one was profitable) were losing money in their last full year before switching, against 807 of 2,418 rural hospitals (33%); median margin -9.5% of cost vs +4.7%.
- [story](E47_conversion_finances/story.html) · [findings](E47_conversion_finances/findings.md)

## E48. Were their financial reports already bad beforehand?
- **confirmed but reframed**
- 67.4% of the 141 hospitals terminated 2024-26 lost money on their last cost report (33.9% of active); below -20% margin, 8.4% terminated within two years — a loss streak can't be measured, no hospital has two 350-380 day reports.
- [story](E48_closures_predicted/story.html) · [findings](E48_closures_predicted/findings.md)

## E49. Did they win government contracts specifically during their ban?
- **confirmed but reframed**
- 172 awards worth $8.35M began while the company was on the SAM ban list, and one company, Nova Datacom, holds 67% of that; strip it and $2.76M is spread over 168 awards to 36 companies.
- [story](E49_contracts_during_ban/story.html) · [findings](E49_contracts_during_ban/findings.md)

## E57. Are they also the ones industry pays the most?
- **confirmed but reframed**
- 18.1% of top-decile Medicare Part B billers are also top-decile industry payees vs 7.7% of peers (2.4x, 22,342 clinicians, $356.1M PY2024) — but only 19% of that money is royalty; it is 53% consulting and speaking, and the royalty story is orthopedics ($84.9M, 65% royalty).
- [story](E57_volume_and_money/story.html) · [findings](E57_volume_and_money/findings.md)

## E62. Are they still getting cited for missing sprinkler systems?
- **confirmed but reframed**
- On the day CMS printed "sprinklers: Yes" for 14,638 homes, 67 had an open order to install one; 22 of those hold up after a stale-row check - 14 with no plan filed and 8 on a CMS waiver, the oldest sitting 919 days.
- [story](E62_sprinkler_flag_lies/story.html) · [findings](E62_sprinkler_flag_lies/findings.md)

## E68. Do they give very little free care to the poor despite huge profits?
- **confirmed but reframed**
- 89 nonprofit hospitals made over $50M and spent under 1% of costs on charity care in their latest cost report; the IRS name-join identifies 37 of them, and the richest nonprofit tier gives a median 1.8%, barely above the 1.5% of hospitals losing money, and a quarter of what the richest for-profits give
- [story](E68_nonprofit_charity_care/story.html) · [findings](E68_nonprofit_charity_care/findings.md)
