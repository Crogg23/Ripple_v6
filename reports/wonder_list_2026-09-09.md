# The wonder list, 2026-09-09

125 "I wonder if" questions from a riff session. No status, no results. Ideas only.

Tags per line:
- picture: MAP (county choropleth, two layers) | ANIM (map by year) | SCAT (dot per unit, fit line, residuals) | RANK (ranked bar, repeat stacked) | NET (who links to who)
- hub: the join key or place column
- plaus: A (both tables named, key known) | B (one side unsure, check registry) | C (needs data I doubt is landed)

## Shape 1: five arcs of the American experience

### Arc 1: PLACE, where you live decides
| # | wonder | picture | hub | plaus |
|---|---|---|---|---|
| 1 | Flood-aid zips denied mortgages more the next year | ANIM | ZIP | A |
| 2 | 1930s redline maps predict today's water violations | MAP | tract/county | A |
| 3 | PE landlords and CFPB complaints rise together | ANIM | ZIP | B |
| 4 | Counties aided three times and rebuilt again | MAP | FIPS | A |
| 5 | Lenders pull out of a county after the first big storm | ANIM | FIPS | A |
| 6 | Counties that lost doctors, banks, factories same decade | ANIM | FIPS | A |
| 7 | Single P.O. box hosts clinics, PACs, contractors | NET | ADDRESS | A |
| 8 | Counties with one doctor per thousand and shrinking | ANIM | FIPS | A |
| 9 | Rural clinics close where the only bank branch closed | MAP | FIPS | A |
| 10 | Rural counties send most to DC, get least back | SCAT | FIPS | A |
| 11 | Rural water systems violate more per capita than urban | SCAT | PWSID to FIPS | A |
| 12 | Mine closed, overdoses rose within three years | ANIM | FIPS | A |
| 13 | Counties host most plants, get least federal money | SCAT | FIPS | A |
| 14 | Water violations rise where a hospital just closed | ANIM | FIPS | A |
| 15 | Unsafe dams upstream of nursing homes or schools | MAP | coords | A |
| 16 | Fracking counties see water violations climb after boom | ANIM | FIPS | A |
| 17 | Discharge permits upstream of poorest water systems | MAP | coords | B |
| 18 | Water systems violate yearly, never enforced | RANK | PWSID | A |
| 19 | Highway deaths rise where trauma centers closed | ANIM | FIPS | C |
| 20 | For-profit colleges cluster near bases and vets | MAP | ZIP | B |
| 21 | Counties lost only hospital and community college | MAP | FIPS | B |
| 22 | Counties run elections on smallest budget per voter | MAP | FIPS | A |
| 23 | Where coal plants closed, respiratory claims fell | ANIM | FIPS | A |
| 24 | Plants run dirtiest on hottest days | ANIM | EIA_PLANT | C |
| 25 | Plant-county water systems violate more after hot summer | ANIM | FIPS | C |

### Arc 2: BODY, what happens to your health
| # | wonder | picture | hub | plaus |
|---|---|---|---|---|
| 26 | 2010 pill counties become 2024 overdose counties, or not | ANIM | FIPS | A |
| 27 | Power plant bad-air day shows in local Part B claims | SCAT | ZIP | A |
| 28 | Nursing homes chart sicker right after a chain buys them | SCAT | CCN | A |
| 29 | Dialysis chains arrive, local kidney doctor count falls | ANIM | FIPS | A |
| 30 | Water violations cluster where hospitals closed | MAP | FIPS | A |
| 31 | Hospices in chains discharge alive more or less | RANK | CCN | B |
| 32 | Nursing census drops, hospice enrollments rise same year | SCAT | FIPS | A |
| 33 | Sickest-charted homes also carry most fire violations | SCAT | CCN | A |
| 34 | Counties with more nursing beds than doctors to staff | MAP | FIPS | A |
| 35 | Dementia charting jumps after reimbursement rule change | ANIM | CCN | B |
| 36 | Nonprofit hospitals pay least charity per surplus dollar | RANK | EIN | A |
| 37 | Hospitals closed, where doctors showed up next year | MAP | NPI | A |
| 38 | Hospital mergers precede local Part B price rises | ANIM | CCN | C |
| 39 | Hospitals own the home health agency they refer to most | NET | CCN/NPI | A |
| 40 | Hospitals near pollution bill more respiratory per patient | SCAT | ZIP | A |
| 41 | Pharmacies took most pills per resident 2012, by county | MAP | DEA_NO to FIPS | A |
| 42 | Top 2012 distributor counties saw steepest death rise | SCAT | FIPS | A |
| 43 | Adverse events through 2014 cluster by prescriber state | MAP | state | A |
| 44 | Drugs leading Part D cost growth, who prescribes most | RANK | NPI | A |
| 45 | Antipsychotic scripts per nursing bed track chain ownership | SCAT | CCN | A |
| 46 | After poverty explains overdoses, which counties stand out | SCAT | FIPS | A |
| 47 | After age explains Part D, which counties prescribe more | SCAT | FIPS | A |
| 48 | Open Payments dinners precede prescribing shifts by a quarter | SCAT | NPI | A |
| 49 | Doctors excluded, reinstated, and paid again by pharma | RANK | NPI | A |
| 50 | Device recalls follow surgeon royalty payments by product | ANIM | product | A |

### Arc 3: MONEY, who gets it, who gives it
| # | wonder | picture | hub | plaus |
|---|---|---|---|---|
| 51 | 13F ownership shifts the quarter before a contract lands | SCAT | CIK to UEI | A |
| 52 | Congressional trades cluster around committee hearings | ANIM | ticker | A |
| 53 | Zips give most to politics, get least back | SCAT | ZIP | A |
| 54 | CFPB complaint spikes lead enforcement by a year | ANIM | company | A |
| 55 | Disaster contractors win same counties every storm | RANK | UEI/FIPS | A |
| 56 | Banks under orders keep lending in same zips | MAP | FDIC_CERT/ZIP | A |
| 57 | Banks finance most polluting sites per asset dollar | RANK | FDIC/FRS_ID | A |
| 58 | Small-business loans dry up where local bank absorbed | ANIM | FIPS | A |
| 59 | Denial rates diverge most between neighboring counties | MAP | FIPS | A |
| 60 | Failed banks cluster where complaints rose beforehand | ANIM | FIPS | A |
| 61 | Firms with going-concern doubt win new contracts | RANK | CIK to UEI | A |
| 62 | 13F holders exit before the first big fine | SCAT | CIK | A |
| 63 | Pension plans collapsed after a buyout | RANK | EIN | A |
| 64 | Failed banks financed most polluting sites by state | MAP | state | A |
| 65 | Parents hide behind most subsidiaries per contract | RANK | UEI parent | A |
| 66 | Charities pay top officer most per program dollar | RANK | EIN | A |
| 67 | Nonprofit revenues spike after disaster declaration | ANIM | FIPS | A |
| 68 | Nonprofits win grants and register lobbyists | NET | EIN | A |
| 69 | Hospital foundations donate to members who fund hospitals | NET | EIN/FEC | A |
| 70 | After population explains contracts, which counties get more | SCAT | FIPS | A |
| 71 | After income explains denials, which lenders deny more | SCAT | lender | A |
| 72 | Contractors suspended and win again under a new name | RANK | UEI/ADDRESS | A |
| 73 | Pandemic loans went to firms already excluded | RANK | EIN/NAME | A |
| 74 | Universities hold NIH grants and pharma-paid faculty | NET | EIN/NPI | A |
| 75 | NIH grants land where pharma dinners land | SCAT | NPI | A |

### Arc 4: POWER, who decides, who watches
| # | wonder | picture | hub | plaus |
|---|---|---|---|---|
| 76 | Immigration judge grant rate drifts with administration | ANIM | judge | A |
| 77 | Judges hold stock in companies on their own docket | NET | CL_PERSON/CIK | A |
| 78 | Court filings against a chain rise before Medicare fines | ANIM | DOCKET/CCN | A |
| 79 | Mine fines unpaid longer under certain operators | RANK | MINE_ID | A |
| 80 | Detention contractors donate where they house detainees | NET | UEI/FEC | A |
| 81 | Votes drift toward donors after donation, by member | SCAT | member | A |
| 82 | Bills lobbied hardest before markup, and by whom | RANK | bill | A |
| 83 | 527 groups spend most per registered voter | MAP | state | A |
| 84 | Foreign agents register before trade or arms votes | ANIM | date | A |
| 85 | Plant owners donate to regulators' overseers by state | NET | EIA/FEC | A |
| 86 | Lag from complaint spike to enforcement, by bank | RANK | company | A |
| 87 | Lobbying spikes before agency rules, by how many weeks | ANIM | agency | A |
| 88 | Judges' former firms appear most on their dockets | NET | CL_PERSON | A |
| 89 | Lobbyists who were regulators and vice versa | NET | NAME | A |
| 90 | Detention contracts grow where ICE detainers grow | ANIM | FIPS | A |
| 91 | Immigration judges who reverse most, and who appointed | RANK | judge | A |
| 92 | Foreign-owned contractors win more in certain agencies | RANK | UEI | A |
| 93 | Foreign-owned contractors, defense versus health | RANK | UEI | A |
| 94 | Foreign agent filings track arms sales by country | ANIM | country | B |
| 95 | Political nonprofits share addresses with PACs | NET | ADDRESS | A |
| 96 | Years from redline map to shortage-area designation | MAP | FIPS | A |
| 97 | Doctors also donors, contractors, nursing owners | NET | NPI/EIN/FEC | A |
| 98 | Offshore-leak names in US federal contracts | NET | NAME | A |
| 99 | Hospital execs on boards of their own suppliers | NET | NAME | B |
| 100 | Universities patent on federal money, license to donor | NET | EIN | C |

### Arc 5: WORK and THINGS, the machine running
| # | wonder | picture | hub | plaus |
|---|---|---|---|---|
| 101 | Injury rates jump the year after a chain buys the plant | SCAT | EIN | B |
| 102 | Visa sponsors carry unpaid wage judgments | NET | EIN/NAME | A |
| 103 | Union locals shrink where county contracts grow | SCAT | FIPS | A |
| 104 | Mines delinquent on fines, injuries climb next year | SCAT | MINE_ID | A |
| 105 | Visa sponsors cluster in wage-violation zips | MAP | ZIP | A |
| 106 | Drug price spike after generic count drops to one | ANIM | NDC | A |
| 107 | Fast-track devices recall more than standard | RANK | product | A |
| 108 | Ships visit sanctioned ports then US ports | ANIM | vessel | C |
| 109 | Rail crossing crashes cluster where rail owner fined | MAP | crossing | A |
| 110 | Shell-owned aircraft fly contractor routes | NET | tail no | B |
| 111 | Vehicle recalls hit models sold heaviest in poorer states | MAP | state | B |
| 112 | Ships loiter off ports before a spill report | ANIM | vessel | B |
| 113 | UK shell controls a US nursing home | NET | COMPANY_NO/CCN | A |
| 114 | UK controllers of US firms share address with sanctions | NET | ADDRESS | C |
| 115 | UK controllers also control US contractors | NET | COMPANY_NO/UEI | A |
| 116 | Offshore-leak names hold US property or nonprofits | NET | NAME | A |
| 117 | US doctors control UK companies, what sector | NET | NPI/COMPANY_NO | A |
| 118 | Student-loan complaints rise where servicer changed | ANIM | company | B |
| 119 | Research patents track federal or donor money more | SCAT | EIN | C |
| 120 | Operators fined, paid, fined again for same thing | RANK | FRS_ID/MINE_ID | A |
| 121 | Zips file same complaint against same firm yearly | RANK | ZIP/company | A |
| 122 | Counties flood, rebuild, flood again on federal money | ANIM | FIPS | A |
| 123 | 990 hospital charity rises where wages fall | SCAT | EIN/FIPS | A |
| 124 | After plant count explains emissions, which operators dirtier | SCAT | EIA_PLANT | A |
| 125 | Workplaces with rising injury rates, by owner | RANK | EIN | B |

## Shape 2: by picture

| picture | count | what the viewer sees |
|---|---|---|
| ANIM | 38 | a map that moves; the year slider is the story |
| SCAT | 27 | a cloud, a line, and the dots that refuse the line |
| NET | 24 | one name in three worlds |
| RANK | 22 | the same names at the top, year after year |
| MAP | 14 | two layers, one county, the overlap |

## Shape 3: by hub

FIPS 41 · EIN 17 · NPI 12 · CCN 10 · ZIP 9 · UEI 9 · NAME/ADDRESS 12 · CIK 4 · CL_PERSON 3 · MINE_ID 3 · PWSID 3 · EIA_PLANT 3 · other 9

## Plausibility

A 100 · B 17 · C 8
