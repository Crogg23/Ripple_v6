# 93 Rejected ballots and jail counties
- Checked: POLITICS__FED_EAC_EAVS (6,460 jurisdictions, 55 states, one vintage; FIPSCODE is 10-digit county+sub except WI 1,851 five-digit muni rows and one ME state row); C1B, C8A, C9A; JUSTICE__XC_VERA_INCARCERATION_TRENDS by year; join on left(fipscode,5)=COUNTY_FIPS.
- Codebook stand-in: C8A + C9A = C1B on 6,014 of 6,460 rows, so C1B = mail ballots returned, C8A = counted, C9A = rejected. Sentinels -99/-88 on 231 rows, blank on 6. The vintage reads as the 2022 general (comments cite 2020 as past).
- First number: on 1,632 counties (EAVS x Vera 2018, ballots returned >= 500), median rejected share runs 0.00% in decile 1 to 3.80% in decile 10. Jail rate per 100k across those deciles: 340, 285, 334, 348, 354, 332, 331, 348, 370, 391. Black share of 15-64 pop: 2.2% -> 7.8%.
- Read: the jail gradient is weak (+15% top vs bottom, non-monotonic); the race gradient is 3.5x. Same shape on Vera 2024 but only 740 counties join (Vera 2024 carries jail rate on 1,440 counties vs 2,865 in 2018).
- A hit would be top-rejection counties with markedly higher jail rates. What shows: rejection tracks Black population share, jail rate barely moves. That is a race/region signal, likely Southern signature-law states, not a jail signal.
- Traps hit: no codebook, columns validated by arithmetic only; Vera 2024 is half-coverage; WI reports by municipality so a county join drops all of Wisconsin unless aggregated by 5-digit code.
STATUS: dim
HEADLINE: top-decile rejection counties (3.8% of mail ballots) sit at 391 jailed per 100k vs 340 in the zero-rejection decile, but Black share goes 2.2% -> 7.8%; race moves, jail barely does, 1,632 counties, one EAVS vintage.
