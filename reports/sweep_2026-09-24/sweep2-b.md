# sweep2-b: 25 pairs rows

**Result: 0 live, 12 probed, 12 dead, 1 skip.** All 25 rows are marked.
**Statements used: 30 of 120.** Four of them errored: a wrong column name, a missing column, and one bad dedupe. Each was rerun once.
Each of the 10 connections also ran the one allowed `ALTER SESSION`.
The queries are in `sweep2-b.sql`.

---

## Every row

| Row | Status | The number that mattered |
|---|---|---|
| Contracts FULL × SAM excluded providers | probed | Repeats the SAM_EXCLUSIONS pair: 333 UEIs land (344 for all exclusions). New base awards inside a ban window: **$553K**, 16 firms |
| Contracts FY2025 × SAM excluded providers | probed | 103 of the SAM_EXCLUSIONS pair's 104 UEIs. Awards that started after the ban: **$222K**, 8 firms |
| SAM excluded providers × USAspending BULK | skip | 50K-row sample. 6 UEIs, 8 actions, net $0 or negative |
| SAM excluded providers × NIH RePORTER | dead | 0 UEIs land |
| SAM excluded providers × SBIR | probed | 13 of the live SAM_EXCLUSIONS × SBIR row's 14 firms, all 5 Newington firms included. Nothing new |
| Home health × hospice (CCN) | dead | 0 shared CCNs, by design |
| Nursing home penalties × hospice (CCN) | dead | 0 |
| Nursing home × hospice (CCN) | dead | 0 |
| NursingHome411 × hospice (CCN) | dead | 0 |
| Form 5500 × CourtListener schools (EIN) | dead | 160 EINs, names agree 83%: universities' own staff plans. No dollars to compare |
| IRS527 Sched A × schools (EIN) | dead | 0 |
| Hospital officer pay × schools (EIN) | dead | 11 EINs: nursing colleges filed under the hospital's EIN |
| Senate trades × member individual donations | dead | 60 of 82 trading senators land, names 60/60. Median self-funding is 0 on both sides |
| Senate trades × member money raised | dead | 60 land. Median 2024 receipts: $4.40M for traders, $4.22M for non-traders |
| CL dockets × CL FJC copy | probed | The built `IDB_DATA_ID` bridge: 8.41M of 10.32M (81%). Court and docket agree 100%, date 95% |
| CL dockets × FJC criminal | probed | **Unbuilt bridge:** 1.79M of 2.22M criminal dockets (81%), same date 97%. `IDB_DATA_ID` covers only 18.6K of them |
| CL FJC copy × FJC criminal | probed | 94 FJC district codes map 1:1 to 94 CL courts. The criminal part of the copy matches 407,451 of 407,459 |
| CL FJC copy × originating court info | probed | Only 40K of 973K originating rows are federal district courts. 21.8K land (65% of the 33.8K that parse) |
| Originating court info × FJC criminal | probed | 6,960 of 7,082 (98%) |
| EO BMF × OSHA case detail 2023 | probed | 3,125 of 33,687 OSHA EINs (9.3%). State agrees 92%, name 71%. Mostly hospitals |
| IRS BMF × OSHA case detail 2023 | probed | The same 3,126. The two BMF tables are copies |
| IRS527 Sched B × OSHA case detail 2023 | dead | 0 |
| EO BMF × OSHA case detail 2024 | probed | 2,460 of 20,520 (12%). State 92%, name 69% |
| IRS BMF × OSHA case detail 2024 | probed | The same 2,460 |
| IRS527 Sched B × OSHA case detail 2024 | dead | 0 |

---

## Why nothing is live

The SAM excluded providers rows were the best bet, and they only repeat the SAM_EXCLUSIONS rows.

- All 4,789 of its UEIs are in SAM_EXCLUSIONS, as `trap-guessed-and-circular-ids` said.
- Every land count sits just under the SAM_EXCLUSIONS count: 333 vs 344, 103 vs 104, 13 vs 14, 0 vs 2.
- sweep-b already marked both live stories, Newington and ATI. Both sit inside this table too. I marked these rows probed so the live rows aren't counted twice.

The "after the ban" dollars shrink once awards and mods are split, as `trap-after-date-money-and-rate-denominators` says to:

| Table | UEIs paid in a ban window | New awards in the window | Positive mods in the window |
|---|---|---|---|
| Contracts FULL (capped) | 72 | $553K, 16 firms | $8.9M |
| Contracts FY2025 | 50 | $222K, 8 firms | $58K |

- In FULL, the top four are W. P. Mahon (SBA, $99K in 2013), MFA Inc (EPA), Bonus Environmental (EPA) and CFP Group (SBA). Each got under $100K.
- In FY2025, the top one is Bonus Environmental: $130K, on an EPA listing from 2012.
- An EPA listing bars only the facility that broke the law, so these are the boring explanation, not a finding.
- "New" in FY2025 means the award's period of performance starts on or after the ban date. That table has no modification number.

## Nearest to live: the unbuilt criminal-docket bridge

This is plumbing, not a story. It's still the most useful number from this batch.

**What was checked**
- I built the map from FJC district code to CourtListener court from the data itself.
  - Join the FJC copy to FJC criminal on office + docket + filing date.
  - Take the top CourtListener court for each FJC code.
  - Result: 94 codes to 94 courts, one-to-one (`41=txsd`, `3C=flsd`, `7-=akd`...).
- With that map, 1.79M of 2.22M CourtListener `-cr-` dockets match FJC criminal on court + office + docket core. 97% have the same filing date.
- The built `IDB_DATA_ID` link covers 18,628 of them.

**What a hit means:** any CourtListener criminal docket can reach its FJC defendant record: charges, disposition, sentence. That's about 100x the current coverage.

**What a miss means:** the other 19% are older cases, sealed cases or bad docket formats. It was not split further.

**Boring explanation:** my guess is that CourtListener built `IDB_DATA_ID` from the civil file and never ran the criminal one. Not checked. Nothing is hidden; the link just isn't there.

---

## New data traps

1. **The CourtListener FJC copy holds five dataset sources, and their docket numbers collide.**
   - Source 9 acts like civil: 9.30M rows, and it holds the amounts. Source 4 acts like criminal: 941K rows, and 99.99% of its keys match FJC criminal.
   - In one court and office, a civil case and a criminal case can carry the same docket number.
   - On court + office + docket, 1.05M civil keys "match" FJC criminal, but only 0.7% share a filing date.
   - Filter on `DATASET_SOURCE` or add the date, every time.
2. **The criminal part of the FJC copy is mostly 2010-2019.**
   - It covers 70% of 2010-14 FJC criminal cases, 45% of 2015-19 and 0 from 2020 on.
   - So any matched-vs-unmatched gap on it is really a gap between years.
3. **`IDB_DATA_ID` in CourtListener dockets is basically civil-only.** It's filled on 8.41M dockets but only 18.6K criminal ones.
4. **`CORPORATE_REGISTRY__FED_IRS_EO_BMF` and `ECONOMICS__FED_IRS_BMF` are the same IRS list.**
   - They share 1.968M of 1.984M EINs.
   - Every BMF pair row exists twice in the ledger, and one of each pair can be retired.
5. **CCN pairs between hospice and any other facility type can't land.**
   - Digits 3-6 of a CCN code the facility type. Here, hospice CCNs run 1222-1799, home health 3100-9799 and nursing homes 5000-F949. No hospice value falls in either of the other ranges.
   - Suggest `build` auto-skip CCN pairs across facility types. The org-to-org link is `ASSOCIATE_ID`.
6. Smaller:
   - `YEAR_FILING_FOR` is missing from one of the OSHA case detail tables, 2023 or 2024. The union errored on it; I didn't check which.
   - The member money tables hold only cycles 2024 and 2026, one row per member per cycle. So no "after the trade date" check can run on them.
