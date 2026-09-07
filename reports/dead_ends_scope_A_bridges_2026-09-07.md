# Dead ends, scope A: the doctor-to-facility bridge — 2026-09-07

Four docket lines marked "missing a piece": 4, 7, 17, E73.
Every number below came from a read-only query through the Python door (`connect/db.py`), run 2026-09-07.
Every query is printed under its count. Nothing was written to the warehouse.

## The verdict, one table

| Line | What must join | Physical thing missing | Best bridge landed | Measured overlap | Buildable? |
|---|---|---|---|---|---|
| 4 | OTP program (org NPI) ↔ Part D prescriber (person NPI) ↔ Open Payments (person NPI) | A person-to-program roster. OTP file is orgs, Part D is people. | None needed once the person leg is swapped: Part D buprenorphine/naltrexone/methadone prescribers ↔ Open Payments 2022, NPI = NPI | 26,645 of 44,846 prescribers (59%) paid in 2022 | **Yes, without a bridge.** Reframe the line. |
| 7 | FQHC site (org NPI / CCN) ↔ LEIE or opt-out (person NPI) | A person-to-FQHC roster. FACILITY_AFFILIATION has no FQHC facility type. | NPPES practice address = UDS site address, plus 5-digit ZIP | 90 banned people at 114 sites (of 8,660 real-NPI LEIE rows); 75 opt-outs. Bridge reaches 11,110 of 19,038 sites. | **Yes, as an address bridge with a leak caveat.** Not a roster. |
| 17 | FDIC bank (LEI) ↔ EPA corporate crosswalk (MATCHED_LEI / ULTIMATE_PARENT_LEI) | Bank LEIs — 92% blank. And the crosswalk holds owners, not lenders. | GLEIF can fill the LEI. Nothing landed says who finances a facility. | 0 banks on LEI. 2,890 banks on name, all "First National Bank" collisions. | **No.** The premise breaks: an owner crosswalk cannot answer a financing question. |
| E73 | SAM exclusions (NPI, mostly blank) ↔ NPPES (NPI) | Real NPIs on SAM rows — 88.6% blank, 7.1% sentinel. | SAM NPI = NPPES NPI for 4,866 rows; first+last+state name for the rest | 4,854 of 4,866 real NPIs hit (99.8%). Name: 9,591 clean one-hit matches of 85,218. | **Yes, but the answer is already in the file.** Almost every hit is an HHS exclusion, i.e. a doctor banned for being a doctor. |

Trap memory checked and confirmed: facility affiliation under-reports and has no FQHC/OTP rows; NPPES EIN is `<UNAVAIL>`; PECOS never puts a person and an org under one PECOS_ASCT_CNTL_ID (0 of 2,456,135, re-measured today).

---

## Existing bridges in the warehouse (step 3)

Searched LIBRARY_META, LIBRARY_MARTS.HEALTH, LIBRARY_MARTS.REFERENCE, LIBRARY_RAW.LANDING for FACILITY_AFFILIATION, PECOS, NPPES, CROSSWALK, BRIDGE, XREF, ORDER_AND_REF, ENROLL.

```sql
select table_catalog, table_schema, table_name, row_count from LIBRARY_META.information_schema.tables
 where table_name ilike any ('%FACILITY_AFFIL%','%PECOS%','%NPPES%','%CROSSWALK%','%BRIDGE%','%XREF%');
-- AUDIT.BRIDGE_CANDIDATES 74 | CONNECT.BRIDGE_ENTITIES 53,799 | CONNECT.CROSSWALK_SCRATCH 2,692,260 | CONNECT.ENTITY_XREF 2,672,384 | REGISTRY.FACET_CROSSWALK 165

select ... from LIBRARY_MARTS.information_schema.tables where table_schema in ('HEALTH','REFERENCE') and table_name ilike any (...);
-- HEALTH__FED_CMS_FACILITY_AFFILIATION 2,260,193 | FQHC_ENROLLMENTS 11,063 | HHA_ENROLLMENTS 11,508 | HOSPITAL_ENROLLMENTS 9,175
-- NPPES 9,606,683 | ORDER_AND_REFERRING 2,018,354 | PECOS_PROVIDER_ENROLLMENT 2,978,925 | RHC_ENROLLMENTS 5,530 | SNF_ENROLLMENTS 14,425
-- REFERENCE: nothing.
```

What each one actually links:

```sql
select FACILITY_TYPE, count(*), count(distinct NPI), count(distinct CCN), count_if(nullif(trim(CCN),'') is null)
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION group by 1 order by 2 desc;
```
| Facility type | rows | NPIs | CCNs | blank CCN |
|---|---|---|---|---|
| Hospital | 1,917,431 | 927,092 | 4,605 | 0 |
| Home health agency | 213,118 | 122,538 | 7,734 | 0 |
| Hospice | 42,020 | 30,511 | 5,418 | 0 |
| Nursing home | 40,841 | 22,280 | 14,501 | 0 |
| Dialysis facility | 21,457 | 8,221 | 7,384 | 0 |
| Inpatient rehab | 19,302 | 18,132 | 1,155 | 0 |
| LTCH | 6,024 | 5,803 | 309 | 0 |

**No FQHC. No opioid treatment program. No clinic of any kind.** This is the only person-NPI-to-facility table in the warehouse, and it covers seven inpatient/post-acute types only.

```sql
select KEY_A, KEY_B, SOURCE_TABLE, RELATION, count(*) from LIBRARY_META."CONNECT".ENTITY_XREF
 where KEY_A in ('NPI','CCN') or KEY_B in ('NPI','CCN') group by 1,2,3,4 order by 5 desc;
-- CCN→NPI FACILITY_AFFILIATION asserted_affiliation 2,249,953  (the one above)
-- CCN→NPI SNF_ENROLLMENTS 14,251 | HHA 11,413 | FQHC 9,955 | HOSPITAL 5,966 | RHC 5,313 | HOSPICE 4,798 | DIALYSIS 335  — all asserted_same_row
```
The seven `asserted_same_row` sets are an org's own CCN next to that same org's NPI on one enrollment row. Org-to-org. They put no person inside a facility.

CROSSWALK_SCRATCH holds the same eight pairs plus NPI→UEI from SAM (236 rows). BRIDGE_CANDIDATES has zero NPI or CCN rows.

```sql
-- PECOS: does one associate id ever hold a person and an org?
select count(distinct PECOS_ASCT_CNTL_ID), count_if(has_person and has_org) from (
  select PECOS_ASCT_CNTL_ID, boolor_agg(nullif(trim(ORG_NAME),'') is null) has_person,
         boolor_agg(nullif(trim(ORG_NAME),'') is not null) has_org
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PECOS_PROVIDER_ENROLLMENT group by 1);
-- 2,456,135 ids, 0 with both kinds
```
Trap confirmed: no org-to-person enrollment bridge. The PECOS reassignment file, which is the real one, is not landed.

**Net:** the warehouse has no table that says "this doctor works at this clinic." The only doctor-in-building signal that reaches clinics is the NPPES practice address, and that is what the bridges below use.

---

## Line 4 — addiction doctors and drug companies

Docket tables: `HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS` | `LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG` | `HEALTH__FED_CMS_OPEN_PAYMENTS_2022`. Watch-out: "the two records don't line up."

**Why they don't line up:** the OTP file is a list of programs, not doctors.

```sql
select count(*), count(distinct NPI), count_if(nullif(trim(NPI),'') is null)
  from LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS;
-- 1,558 rows, 1,340 distinct NPI, 0 blank

select n.ENTITY_TYPE_CODE, count(distinct o.NPI) from ...OTP o left join ...NPPES n on n.NPI=o.NPI group by 1;
-- type 2 (org): 1,286 | type 1 (person): 1 | not in NPPES: 53
```
1,286 of 1,340 are org NPIs. One is a person.

```sql
select count(*), count(distinct "Prscrbr_NPI"), count_if(nullif(trim("Prscrbr_NPI"),'') is null) from LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG;
-- 25,869,521 rows, 1,057,566 prescribers, 0 blank      (DY2022 file, one year)

select count(distinct o.NPI) from OTP o join PARTD p on p."Prscrbr_NPI"=o.NPI;   -- 0
select count(distinct o.NPI) from OTP o join OPEN_PAYMENTS_2022 p on p.NPI=o.NPI; -- 1
```
Zero overlap with Part D, one with Open Payments. Orgs don't prescribe and don't get Open Payments as covered recipients. The join was never going to work; nothing is broken.

**The person leg already exists.** Part D carries the drug name, so "addiction doctor" = anyone prescribing buprenorphine, naltrexone or methadone.

```sql
select count(distinct "Prscrbr_NPI") from PARTD where "Gnrc_Name" ilike '%buprenorphine%' or ilike '%naltrexone%' or ilike '%methadone%';
-- 44,846 prescribers

select count(distinct p."Prscrbr_NPI") from PARTD p join OPEN_PAYMENTS_2022 op on op.NPI=p."Prscrbr_NPI" where <same drug filter>;
-- 26,645 (59.4%) took a drug-company payment in PY2022

-- for scale: all Part D prescribers vs Open Payments
select count(distinct p."Prscrbr_NPI") from PARTD p join OPEN_PAYMENTS_2022 op on op.NPI=p."Prscrbr_NPI";  -- 570,577 of 1,057,566 (54%)
```
Open Payments 2022: 13,306,564 rows, 863,008 distinct NPI, 51,584 blank-NPI rows (trap: blank is '' not null; already handled by count distinct).

Sample, five top buprenorphine prescribers with a 2022 payment:

| NPI | Name | State | bupe claims | paid 2022 |
|---|---|---|---|---|
| 1134167455 | Kelly, Stephen | OK | 4,377 | $1,760 |
| 1588613020 | Sullivan, James | AL | 3,902 | $3,250 |
| 1235220468 | Mekhail, Mounir | TX | 3,116 | $898 |
| 1144227596 | Haber, Irving | IN | 2,746 | $1,698 |
| 1902871221 | Chen, Andre | TX | 2,390 | $374 |

**If the program matters** (doctor → OTP), the address bridge reaches it, with a leak:

```sql
select count(distinct o.NPI), count(distinct n.NPI) from OTP o join NPPES n
  on n.ENTITY_TYPE_CODE='1'
 and upper(trim(n.PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS))=upper(trim(o.ADDRESS_LINE_1))
 and left(n.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE,5)=left(o.ZIP,5);
-- 1,083 OTP orgs → 30,913 persons at the same street address
-- ...and of those persons, Part D buprenorphine prescribers: 326
```
Top fan-outs are shared campuses, not staff: NORTH CHARLES MENTAL HEALTH (Cambridge MA) 1,420 people, Nassau County 889, City and County of San Francisco 755. Address-leak trap applies.

**Plain read:** nothing is missing. The docket line put an org list where a doctor list belongs. Swap the OTP table for a Part D drug filter and the join is NPI = NPI at 59%. Part D is DY2022 and Open Payments is PY2022, so the years line up. One year only: this is targeting, not before/after (trap already on file).

---

## Line 7 — banned doctors at clinics for the poor

Docket tables: `HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES` | `HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS` | `HEALTH__FED_HHS_OIG_LEIE`. Watch-out: "can't currently tell which doctor works where."

**The two sides:**

```sql
select count(*), count(distinct FQHC_SITE_NPI_NUMBER), count_if(nullif(trim(FQHC_SITE_NPI_NUMBER),'') is null),
       count(distinct FQHC_SITE_MEDICARE_BILLING_NUMBER), count_if(nullif(trim(FQHC_SITE_MEDICARE_BILLING_NUMBER),'') is null)
  from HEALTH__FED_HRSA_UDS_SERVICE_DELIVERY_SITES;
-- 19,038 sites | 6,048 distinct NPI, 12,942 blank (68%) | 8,426 distinct CCN, 10,492 blank (55%)

select n.ENTITY_TYPE_CODE, count(distinct u.FQHC_SITE_NPI_NUMBER) from UDS u left join NPPES n ... group by 1;
-- org 5,971 | person 4 | deactivated-blank 28 | not in NPPES 45
```
The UDS NPI is the clinic's own org NPI. 68% of sites don't even carry one.

```sql
select count(*), count(distinct NPI), count_if(NPI_IS_REAL), count(distinct iff(NPI_IS_REAL,NPI,null)), count_if(not IS_ENTITY_NOT_INDIVIDUAL)
  from HEALTH__FED_HHS_OIG_LEIE;
-- 83,747 rows | 8,839 real-NPI rows, 8,660 distinct real NPIs (10.3%) | 80,323 are people

select count(*), count(distinct NPI), count_if(nullif(trim(NPI),'') is null) from HEALTH__FED_CMS_OPT_OUT_AFFIDAVITS;
-- 57,209 rows, 56,455 distinct NPI, 0 blank
```

**Direct joins:**

```sql
select count(distinct l.NPI) from LEIE l join UDS u on u.FQHC_SITE_NPI_NUMBER=l.NPI where l.NPI_IS_REAL;  -- 0
```
Person NPI vs org NPI. Zero by construction.

**Does FACILITY_AFFILIATION reach an FQHC?**

```sql
select count(distinct u.FQHC_SITE_MEDICARE_BILLING_NUMBER), count(distinct f.CCN), count(distinct f.NPI)
  from UDS u left join HEALTH__FED_CMS_FACILITY_AFFILIATION f on f.CCN=u.FQHC_SITE_MEDICARE_BILLING_NUMBER;
-- 8,426 UDS CCNs → 17 hit, 9,449 doctors
```
17 of 8,426. Those 17 are hospital-owned FQHCs whose CCN doubles as a hospital CCN. The table has no FQHC rows (see step 3).

**Does the FQHC enrollment file help?**

```sql
select count(distinct u.FQHC_SITE_NPI_NUMBER), count(distinct e.NPI) from UDS u left join FQHC_ENROLLMENTS e on e.NPI=u.FQHC_SITE_NPI_NUMBER;  -- 6,048 → 4,672 (77%)
select count(distinct u.FQHC_SITE_MEDICARE_BILLING_NUMBER), count(distinct e.CCN) from UDS u left join FQHC_ENROLLMENTS e on e.CCN=u.FQHC_SITE_MEDICARE_BILLING_NUMBER;  -- 8,426 → 7,091 (84%)
```
Good org-to-org bridge (UDS site ↔ PECOS FQHC enrollment), but still no people on the far side.

**The address bridge:** NPPES practice address (line 1 + 5-digit ZIP) = UDS site address.

```sql
-- reach
select count(distinct n.NPI), count(distinct u.BPHC_ASSIGNED_NUMBER) from NPPES n join UDS u
  on upper(trim(u.SITE_ADDRESS))=upper(trim(n.PROVIDER_FIRST_LINE_BUSINESS_PRACTICE_LOCATION_ADDRESS))
 and left(u.SITE_POSTAL_CODE,5)=left(n.PROVIDER_BUSINESS_PRACTICE_LOCATION_ADDRESS_POSTAL_CODE,5)
 where n.ENTITY_TYPE_CODE='1';
-- 173,813 people at 11,110 of 19,038 sites (58%)

-- leak check: people per site
select max(p), median(p), count_if(p>=200) from (select u.BPHC_ASSIGNED_NUMBER, count(distinct n.NPI) p from <same join> group by 1);
-- max 4,727 | median 5 | 142 sites with 200+
```
Median 5 people per site is what a clinic looks like. The 142 sites with 200+ are hospital campuses and county buildings: address-leak trap, filter or cap them.

```sql
-- banned doctors at an FQHC address
select count(distinct l.NPI), count(distinct u.BPHC_ASSIGNED_NUMBER) from LEIE l join NPPES n on n.NPI=l.NPI join UDS u on <address join> where l.NPI_IS_REAL;
-- 90 people, 114 sites

-- opted-out doctors at an FQHC address (opt-out file carries its own address)
select count(distinct o.NPI) from OPT_OUT o join UDS u on upper(trim(u.SITE_ADDRESS))=upper(trim(o.FIRST_LINE_STREET_ADDRESS)) and left(u.SITE_POSTAL_CODE,5)=left(o.ZIP_CODE,5);
-- 75
```

Sample of the 90, one row per person, with NPPES last-update next to the exclusion date:

| NPI | Last name | Excluded | Specialty | Site | St | NPPES last update |
|---|---|---|---|---|---|---|
| 1780183517 | BELL | 2024-05-20 | COUNSELOR | Health and Wellness East | OH | 2018-02-07 |
| 1649206376 | VERDELL | 2018-08-20 | PSYCHIATRY | AL-ASSIST BEHAVIORAL HEALTH CARE | PA | 2007-07-08 |
| 1043361546 | RASEKHI | 2026-05-20 | INTERNAL MEDICINE | SCMC Van Nuys | CA | 2023-03-07 |
| 1962450254 | LEE | 2026-08-20 | GYN/OBS | Fair Oaks Community Health Centers | CA | 2021-01-27 |
| 1043481138 | BRATTON | 2012-06-20 | FAMILY PRACTICE | Park DuValle Community Health Center | KY | 2008-03-17 |

**Bad news, marked:** every NPPES address predates its exclusion. The bridge says "was practising there when NPPES was last updated," not "works there now." It answers "which banned doctors listed an FQHC as their practice" — a past-tense hit, useful as a lead list, not as a headline.

**Plain read:** the missing thing is a person-to-FQHC roster; CMS publishes none, and the PECOS reassignment file that would give it is not landed. The address bridge is buildable today from NPPES + UDS at 58% site reach, and yields 90 LEIE + 75 opt-out leads. Every count is a floor: LEIE carries a real NPI on 10% of rows.

---

## Line 17 — banks and the pollution sites they finance

Docket tables: `FINANCE__FED_FDIC_BANK_DATA` | `ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK`. Watch-out: "that bank ID field is empty everywhere."

**The two sides:**

```sql
select count(*), count(distinct CERT), count_if(nullif(trim(LEI),'') is null), count(distinct nullif(trim(LEI),'')),
       count_if(nullif(trim(RSSDID),'') is null), count_if(nullif(trim(FDIC_ID),'') is null) from FINANCE__FED_FDIC_BANK_DATA;
-- 27,836 banks | LEI blank on 25,584 (91.9%), 2,241 distinct LEIs | RSSDID and FDIC_ID blank on 0

select count(*), count(distinct EPA_REGISTRY_ID), count_if(nullif(trim(MATCHED_LEI),'') is null), count(distinct nullif(trim(MATCHED_LEI),'')),
       count_if(nullif(trim(ULTIMATE_PARENT_LEI),'') is null), count(distinct nullif(trim(ULTIMATE_PARENT_LEI),'')), count_if(nullif(trim(PARENT_CIK),'') is null)
  from ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK;
-- 5,300,149 facilities | MATCHED_LEI blank 94.7%, 22,743 distinct | PARENT_LEI blank 99.3%, 1,174 distinct | PARENT_CIK blank 97.7%
```
"Empty everywhere" is 92% empty on the bank side, 95% on the facility side. The 2,241 bank LEIs that exist are the big ones.

**Join on LEI:**

```sql
select count(distinct b.CERT), count(distinct x.EPA_REGISTRY_ID) from FDIC b join CROSSWALK x
  on nullif(trim(x.MATCHED_LEI),'')=b.LEI or nullif(trim(x.ULTIMATE_PARENT_LEI),'')=b.LEI;
-- 0 banks, 0 facilities
```
Zero. Not because of blanks: the 2,241 filled bank LEIs hit none of the 22,743 facility LEIs.

**Join on name:**

```sql
select count(distinct b.CERT) from FDIC b join CROSSWALK x
  on upper(trim(x.PARENT_LEGAL_NAME))=upper(trim(b.HOLDING_COMPANY_NAME)) or upper(trim(x.MATCHED_LEGAL_NAME))=upper(trim(b.NAME));
-- 2,890 banks

select x.MATCHED_LEGAL_NAME, count(*) from <same join> group by 1 order by 2 desc limit 5;
-- First National Bank 5,740 | First State Bank 1,960 | Citizens Bank 1,643 | Farmers State Bank 1,200 | Commerce Bank 605
```
Sample: "First State Bank" hits five different holding companies (Texas United, Citizens & Northern, Henderson Citizens, Panhandle, Dumas). Generic-name collision, same shape as ST LUKES HOSPITAL. The facility on the EPA side is the bank's own building (a UST tank, a boiler permit), not a borrower.

```sql
select count_if(MATCHED_LEGAL_NAME ilike '%BANK%' or PARENT_LEGAL_NAME ilike '%BANK%'), count(distinct <that LEI>) from CROSSWALK;
-- 1,806 facility rows carry a bank-named owner, 672 distinct LEIs
```
Where a bank appears in the crosswalk, it is as the owner of its own branch's tank.

**Could GLEIF fill the bank LEIs?** Yes: `LANDING.INTL_GLEIF` (3,382,301 rows, columns `LEI`, `Entity.LegalName`, `Entity.LegalAddress.Country`) plus `FDIC.RSSDID` is filled on 100% of banks. But filling the LEI still joins bank-as-owner to facility-as-owned. It never says "financed."

**What "finances" would need:** a lender-to-borrower table. Landed candidates: `FED_SEC_13F_HOLDINGS` (101M rows, equity stakes by institutional filers, CUSIP-keyed) and `FED_SBA_LOANS` (2.17M, lender name + borrower). 13F gives "bank holds shares in polluter's parent," which is ownership, not lending. No UCC, no syndicated-loan, no bond-underwriting table exists. Line 3, which this line says it copies "through a different bank record," has the same hole.

**Plain read:** the premise is broken before the join. `XC_EPA_CORPORATE_CROSSWALK` answers "who owns this facility." No landed table answers "who lent this owner money." Filling the LEI column is a day of work and buys a join with zero real hits. **Not buildable** as asked. Buildable as a different question: "which polluters' parents does a bank hold stock in" via 13F ↔ crosswalk PARENT_CIK (filled on 2.3% of facilities, 119K rows) — a separate docket line if wanted.

---

## Line E73 — banned contractors who are also doctors

Docket tables: `PROCUREMENT__FED_SAM_EXCLUSIONS` | `HEALTH__FED_CMS_NPPES`. Watch-out: "dead end, basically no overlap."

**The SAM side:**

```sql
select count(*), count_if(nullif(trim(NPI),'') is null), count_if(NPI='0000000000'),
       count(distinct iff(nullif(trim(NPI),'') is not null and NPI<>'0000000000', NPI, null)),
       count_if(IS_ENTITY_NOT_INDIVIDUAL), count_if(not IS_ENTITY_NOT_INDIVIDUAL) from PROCUREMENT__FED_SAM_EXCLUSIONS;
-- 168,328 rows | NPI blank 149,090 (88.6%) | sentinel '0000000000' 12,027 (7.1%) | 4,866 real distinct NPIs (2.9% of rows)
-- 35,197 entities | 133,131 individuals
```

**ID join:**

```sql
select count(distinct s.NPI) from SAM s join NPPES n on n.NPI=s.NPI where s.NPI<>'0000000000' and nullif(trim(s.NPI),'') is not null;
-- 4,854 of 4,866 (99.8%)
```
Sample: PUTVIN TAMMY / GOLDEN GARY / EATOUGH PHILIP — SAM name = NPPES name on every row checked. Where SAM carries an NPI, it is right. It just carries one on 3% of rows.

**Name join, individuals only.** 133,131 individual rows, 93,998 distinct first+last, 43 with no first name.

```sql
-- single word: SAM last name exists among NPPES persons
with s as (select distinct upper(trim(LAST_NAME)) ln from SAM where not IS_ENTITY_NOT_INDIVIDUAL ...)
select count(*), count_if(hits>0), sum(hits), median(iff(hits>0,hits,null)) from (select ln, (select count(*) from NPPES n where ENTITY_TYPE_CODE='1' and upper(PROVIDER_LAST_NAME_LEGAL_NAME)=s.ln) hits from s);
-- 41,541 last names | 30,783 match (74%) | 4,599,412 NPPES rows hit | median fan-out 20

-- multi word: first + last
-- 93,998 names | 33,406 match (35.5%) | 11,874 match exactly one NPI (12.6%) | 318,841 NPPES rows hit

-- first + last + state
-- 85,218 names with a state | 14,085 match (16.5%) | 9,591 match exactly one NPI (11.3%)
```

| Key | SAM names | matched | one-hit | rows hit |
|---|---|---|---|---|
| last only | 41,541 | 30,783 (74%) | — | 4.6M |
| first+last | 93,998 | 33,406 (36%) | 11,874 | 318,841 |
| first+last+state | 85,218 | 14,085 (17%) | 9,591 | — |

Single word is noise: 74% "match" with a median 20 people behind each name. First+last+state is the usable key at 9,591 one-hit names.

Sample of one-hit first+last+state matches:

| SAM name | St | Excluding agency | NPI | Taxonomy |
|---|---|---|---|---|
| WILLIAMSON, BARBARA | TX | DOJ | 1487864211 | 1041C0700X (social worker) |
| FOX, TINA | TN | HHS | 1760632434 | 363LF0000X (NP, family) |
| DOTSON, KIMBERLY | OH | HHS | 1598417321 | 374U00000X (home health aide) |
| O'BRIEN, CHARLENE | NY | HHS | 1841443496 | 164W00000X (LPN) |
| RICHARDSON, STEVEN | CA | HHS | 1881857183 | 101YM0800X (counselor) |

**Bad news, marked:** the excluding agency.

```sql
select EXCLUDING_AGENCY, count(*) from SAM group by 1 order by 2 desc;
-- HHS 69,862 | OFAC 41,712 | OPM 40,610 | DOJ 3,219 | null 2,397 | HUD 2,315 | EPA 2,164 | USN 831
```
HHS rows are the OIG LEIE mirrored into SAM. A doctor on an HHS exclusion hitting NPPES is a doctor banned for a healthcare crime, which is the LEIE line, not a crossover. The crossover the docket wants — a construction or defense debarment that turns out to be a doctor — lives in the non-HHS, non-OFAC, non-OPM rows: 13,000-odd, and their NPI column is the blank one.

**Plain read:** the "no overlap" note was measuring NPI = NPI on a 3%-filled column. The bridge is first+last+state into NPPES persons at 11% one-hit. Buildable today. But restrict to EXCLUDING_AGENCY not in (HHS, OFAC, OPM) or the answer is "banned doctors are doctors." Every one-hit is a lead, not a match: the SAM address is the only tiebreaker and it was not used here.

---

## What is physically missing, all four

| Line | The thing | Exists anywhere landed? | Where it would come from |
|---|---|---|---|
| 4 | doctor → OTP program roster | No | Not needed; Part D drug filter replaces it |
| 7 | doctor → FQHC roster | No (FACILITY_AFFILIATION stops at hospitals/post-acute) | CMS PECOS reassignment file (Physician & Other Practitioners reassignment), not landed. Address bridge stands in. |
| 17 | lender → borrower | No | UCC filings, LSTA/DealScan, bond underwriting; none landed. 13F is ownership, not lending. |
| E73 | NPI on SAM rows | 3% filled | SAM will never fill it; name+state bridge stands in |

## Cost
Roughly 40 read-only queries, the biggest a 9.6M-row NPPES join to a 19K-row address list and three correlated-subquery name scans over NPPES; each ran under two minutes. No real number from the query log was pulled for this — call it "no real number for this" until priced.
