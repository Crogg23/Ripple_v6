# E40 — Brand-new NPIs billing Medicare for skin substitutes, DY2024

**One-line version:** the strict number is **$452M** to 114 NPIs that did not exist before 2022. The $1.35B is everything those clinicians billed, most of it not grafts. And once you compare new NP/PAs to the old NP/PAs already billing grafts, they bill the same per patient. The wave is real; "brand-new" is not what drives it.

Words, once:
- **NPI** — the ten-digit number Medicare uses to identify one clinician. NPPES is the registry that says when each one was created.
- **Skin substitute** — a lab-grown or donor-tissue graft laid on a wound, billed per square centimeter. HCPCS codes Q4100 and up.
- **Allowed** — what Medicare agreed the service was worth (the paid figure is about 80% of it).
- **New** — NPI enumerated 2022-01-01 or later. **Veteran** — before that.

## The chain

| Step | What was checked | Number | Hit means | Miss means |
|---|---|---|---|---|
| Keys | BY_PROVIDER rows vs distinct NPI; NPPES rows vs distinct NPI; all 10 chars | 1,296,739 = 1,296,739; 9,606,683 = 9,606,683 | joins can't fan out | any total would be inflated |
| Vintage | newest enumeration year present in both Part B files | 2024 in both (17,317 / 14,457 NPIs), zero 2025 | both files are DY2024 | a year mismatch would fake "new" |
| Loose rebuilt | top 1% of 1,235,757 individual billers by allowed, `percent_rank` not `ntile`, joined to NPPES type 1, enumerated 2022+ | **354 NPIs, $1,352,392,029** — exact match to first pass | first pass is arithmetically sound | — |
| Strict, same cohort | skin lines (Q4100+) for those 354, dollars = services x avg allowed | **94 NPIs, $443,922,367** — exact match | 32.8% of the loose number is provably grafts | — |
| Strict, every new NPI | drop the top-1% filter; every type-1 NPI enumerated 2022+ with any Q4100+ line | **114 NPIs, $452,122,168**, 24 codes, 302,162 sq cm | this is the headline; the cut hid only $8.2M | — |
| Q4 leakage | Q4001–Q4099 (casting supplies) among new NPIs | 64 lines, $37,877 — excluded | the >=4100 rule matters, but not to the number | — |
| Codes | top 15 Q4 codes used by new NPIs | all "per square centimeter" grafts; Q4271 Complete FT $121M, Q4205 Membrane Wrap $78M, Q4262 Impax $52M | the label "skin substitute" is right | — |
| Base rate | new NPIs as share of individual Part B billers vs share of skin dollars | 7.2% of billers, 9.9% of skin dollars | over-represented by half, not tenfold | — |
| By birth year | skin dollars per Part B biller, by year the NPI was created | 2018 $5,906 · 2019 $5,186 · 2020 $6,150 · 2021 $3,764 · 2022 $5,893 · 2023 $6,244 · 2024 $939 (partial year) | 2022-23 sit at the top of the 2018-20 plateau (2023 is the series high), not off it | a spike at 2022+ would say "rented NPIs" |
| Per patient, all specialties | median allowed per beneficiary among skin billers | new $31,843 vs veteran $7,110 | matches first pass's 5.5x shape | — |
| Per patient, like for like | same, veterans restricted to NP/PA skin billers | **new $30,472 vs veteran $27,133** | the gap was job title, not birth year | — |
| Per patient, whole trade | every NP/PA Part B biller, skin or not | new $149 vs veteran $158 | the 114 are ~200x their trade; being in the graft business is the whole effect | — |
| A2 codes | HCPCS A2001–A2999, the 2023-24 skin-substitute family, among new NPIs | 11 lines, 11 NPIs, $7.5M — excluded from the headline | headline is Q4100+ only; add $7.5M for the wider definition | — |
| NP/PA base rate | new share of NP/PA Part B billers vs of NP/PA skin dollars | 17% of billers, 21% of skin dollars, 23% of skin billers | mild over-representation | — |
| Concentration | top 10 / top 50 of the 114 | $191M (42%) / $385M (85%); 85 of 114 over $1M | the individuals are the story | — |
| Addresses | new billers sharing a practice address | 96 addresses; 30 NPIs share one with another new biller ($62M); 37 veteran skin billers sit at those addresses ($78M) | wound-care clinics adding staff, not solo operators | — |
| Ramp | skin dollars by enumeration half-year | 2022: 52 NPIs $220M; H1 2023: 28, $128M; Jul 2023+: 34, $104M (median $1.8M) | an NPI created in late 2023 clears $1.8M by end of 2024 | — |

## Top states (new-NPI skin dollars, from results.json `states`)

| State | New NPIs | New $ | Veteran NPIs | Veteran $ | New share |
|---|---|---|---|---|---|
| CA | 24 | $122M | 179 | $1,093M | 10% |
| AZ | 11 | $109M | 44 | $197M | 36% |
| FL | 18 | $69M | 200 | $808M | 8% |
| TX | 15 | $34M | 108 | $478M | 7% |
| IL | 4 | $34M | 37 | $152M | 18% |
| NV | 7 | $29M | 23 | $181M | 14% |
| MS | 6 | $9M | 19 | $31M | 23% |
| KY | 3 | $7M | 14 | $46M | 14% |
| VA | 2 | $7M | 22 | $18M | 27% |
| NJ | 2 | $6M | 21 | $105M | 5% |

California leads on dollars; Arizona is where new NPIs carry the biggest share. Florida is the veteran capital. (The first-pass "AZ 21 NPIs $166M" was a state-by-provider-type cell inside the top-1% cohort, not a state total; the skeptic caught the first draft of this table repeating it.)

## Top 10 new billers

| NPI | Name | Type | State | Created | Skin $ | All Part B benes |
|---|---|---|---|---|---|---|
| 1215678495 | Allison Charles | NP | AZ, Sun City | 2022-04-05 | $47.4M | 78 |
| 1902544240 | Chibuikem Okoro | PA | CA, Temecula | 2022-05-26 | $23.7M | 176 |
| 1275217952 | Gina Palacios | NP | AZ, Phoenix | 2023-06-13 | $23.2M | 33 |
| 1992489728 | Elisabeth Balken | NP | AZ, Mesa | 2023-06-12 | $18.0M | 25 |
| 1043087182 | Tiffany Hyde | NP | IL | 2023-12-08 | $17.3M | 48 |
| 1932849049 | Nelson Uy | NP | IL, Park Ridge | 2022-03-29 | $14.3M | 820 |
| 1316688260 | Tara Howard | Internal Med | FL, Fort Lauderdale | 2022-04-05 | $13.1M | 38 |
| 1497416184 | Surany Thompson | NP | FL, Boca Raton | 2022-01-04 | $12.1M | 105 |
| 1073229746 | Hiren Patel | PA | CA, Los Angeles | 2023-01-26 | $11.7M | 123 |
| 1245934967 | Nicole Castillo | PA | CA, Pomona | 2023-03-28 | $10.7M | 176 |

Tiffany Hyde's NPI was created 2023-12-08 and billed $17.3M of grafts in the following calendar year.

## What a skeptic attacks, and the answer

- **"$452M is a floor, not a number."** True, and it excludes the A2xxx family (+$7.5M). CMS deletes any NPI-by-code line under 11 beneficiaries; 114 NPIs show only 144 visible skin lines. For the 354 cohort, only 43.7% of provider-file dollars have a visible service line at all. The strict number can only go up; the loose number is the ceiling.
- **"DY2024 is inferred."** True. Neither Part B file has a year column. Carbon-dated: newest NPIs in both files are 2024, none 2025. Same finding as the first pass.
- **"New NPI is not a new person."** True and unresolved. NPPES says when the number was issued, not when the person started practising. A nurse who worked under a group's billing for a decade and got her own NPI in 2022 reads as "new." Nothing in the warehouse links a person to a prior NPI.
- **"Per-bene medians on 114 vs 368 NPIs."** Small but the direction is clear: pooled gives $36,025 vs $25,873 — new still a bit higher, 1.4x, not 5.5x.
- **"You compared them to veterans who are also in the graft business — that conditions on the outcome."** Correct, and it is the point: the median NP/PA of either vintage bills about $150 per patient. The graft billers are 200x that whatever their birth year. Newness adds nothing once someone is in the trade; the trade is the anomaly.
- **"Skin billers per 1,000 Part B billers is 1.39 for the 2022 cohort vs 1.08 for 2018."** Real, modest, and partly denominator attrition (older cohorts have retired billers still counted). It cuts against 'no spike' by a third, not by an order of magnitude.
- **"Line dollars = services x average allowed is an estimate."** It is. CMS publishes averages per line; the product reproduces the provider-file totals to within suppression, per the first-pass skeptic.
- **"Address matching on a street string."** Exact-string on ST1+city+state, uppercased and trimmed. Suites split one building; that undercounts sharing, never overcounts.

## What changed vs the first pass

- Headline moves from $1.35B to $452M (strict, all new NPIs), with the first pass's $444M reproduced exactly as the top-1% subset.
- The per-beneficiary "5.5x" collapses to 1.1x (medians) once veterans are the same job title and the same trade. The first pass compared new NP/PAs to veteran surgeons and oncologists.
- Enumeration-year view added: 2022-23 cohorts bill grafts at the same per-biller rate as 2018-20 cohorts. No newborn spike.

STATUS: confirmed but reframed
HEADLINE: At least $452M of DY2024 Medicare skin-substitute billing went to 114 NPIs that did not exist before 2022 — 85 of them over $1M each — but per patient they bill like the clinicians already in the graft business ($30k vs $27k), so the story is the graft wave and the ten individuals, not the birth year of the NPI.
