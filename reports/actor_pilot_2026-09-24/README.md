# Actor pilot — 2026-09-24

Question: can one company be followed across the warehouse's domains, cleanly enough to build "every public record about one company"?

Door: Python scripts, read-only. About 0.6 credits of COMPUTE_WH, not exact: metering buckets by the hour.

## What ran

| Pass | What | Result |
|---|---|---|
| Name | 25 companies, word-bounded regex on party-name columns of 354 tables | 3,219 table-company hits in 340 tables; ARCOS timed out at 300 s |
| ID | ticker to SEC CIK, CIK to EIN, top 20 contractor UEIs each; every CIK/EIN/UEI table counted | 966 hits, 36 tables |
| Grade | a fresh reader graded 200 random name hits | 159 clean, 17 related, 19 wrong, 5 unclear |

## Reach per company

- By name: all 25 reach 6-12 domains. Boeing and JPMorgan reach 12.
- By ID: at most 4, and always money, labor, environment or science. **No ID reaches health, politics or justice.**
- Health, politics and justice are reachable only by name: Open Payments payer names, LDA lobbying clients, FEC employer text, court case names.

## Name-match quality, from grades.csv

| Domain | Clean |
|---|---|
| environment | 90% |
| money | 85% |
| labor | 82% |
| justice | 77% |
| health, politics | 75% |
| immigration | 43% |
| companies registry | 38% |

Clean is 76% once 1-row SEC hits are left out. The grade unit is a table-column-company group, and 9 clean groups hide a namesake inside.

Worst misfires:
- A bare surname like NORTHROP, or a bare acronym like CVS
- "UNITED HEALTHCARE" catches a union
- Address and device columns leaking into the name filter
- "J P MORGAN" catches a lawyer and a limo firm

## Verdict

Worth building, with names as the engine and IDs as the check. Fixes before scale:

1. A curated alias list per company, never a bare surname or acronym
2. A column filter that drops ADDR, APT, DAM and DEVICE
3. Where a name hit's table also carries an ID, confirm the ID against ids.csv
4. A precision grade per table, so the output says how sure each link is

Files: pilot.py, id_pass.py, hits.csv, id_hits.csv, ids.csv, grade_sample.csv, grades.csv, log.txt.

## Expansion to ~570 companies, same day

Seeds came from the data: the top 80 names in eight lists, which were contracts, doctor payments, lobbying, PACs, toxic release, complaints, injuries and H-1B visas. See seeds.csv and seed_500.py.
The scanner is scan_500.py. It splits names into words, joins on a rare anchor word, then confirms the full pattern.
Two cleaning rules:
- A one-word company must be the whole party name plus legal endings
- A surname, tested against NPPES last names with 25 or more people, needs the full legal name

| Run | Hits | Graded clean | File |
|---|---|---|---|
| loose | 30,474 | not graded; one-word places and words topped the list | hits_500_loose.csv |
| strict | 26,425 | 175 of 200, 87.5% | hits_500.csv, grades_500.csv |
| strict, 16 junk seeds cut | 555 companies | about 93-95% expected | hits_500_clean.csv |

The 16 junk seeds were cut on the grader's evidence, not Claude's choice: NONE, DE LA CRUZ, WASTE MANAGEMENT, METHODIST HOSPITAL, PROVIDENCE HEALTH, SIERRA NEVADA, COMPUTER SCIENCES, HEALTH NET, DISCOUNT TIRE, CHAMBER OF COMMERCE OF THE, GOVERNMENT OF THE UNITED STATES, COMPASS, AEROSPACE, AARP LIMITED, SAFEWAY COMPANY LIMITED and ASHLAND.

Reach after cleaning:
- 454 companies in 4+ domains, 335 in 6+, 172 in 8+, 32 in 10+
- The median company appears in 26 distinct datasets, counting each dataset once

Crossings:
- 76 sit in doctor payments, court cases and politics at once
- 278 sit in contracts, EPA, OSHA, courts and politics at once

Caveat: presence is not wrongdoing. Big companies appear everywhere because they are big. Stories need magnitudes inside a crossing, like harm per contract dollar, not presence counts.

Cost: both 500-company scans together, about 1 credit.

## Harm ranking, same day

rank_harm.py pulled contract dollars. rank_osha.py compares each contractor's injury rate to other firms in its exact industry, leaving the company out of its own benchmark. The results are in injury_rank.csv.

"Harm per contract dollar" ranked commercial giants with small federal contracts, like Amazon and Delta. That's a size effect, so the fair measure is the industry ratio.

Skeptic results:

| Company | First pass | After skeptic |
|---|---|---|
| SpaceX | 2.78x | confirmed; each year alone 3.6-3.8x. Prior art: Reuters, Nov 2023, on 2022 data |
| Ford | 2.12x | confirmed, 2.01x after hours cleanup; truck plants 10.6 vs peers 5.5 |
| General Dynamics | 1.63x | narrowed to 1.19-1.36x; Bath Iron Works is the outlier |
| Huntington Ingalls | 1.38x | narrowed to about 1.1x |

The ECHO serious-violator flag is 'N' on every row, so noncompliance quarters were used instead.
