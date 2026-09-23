# Hard-ID ideas — every join rides a real identifier

Cut made 2026-09-22 by Claude, at Chris's ask: ideas with two or more
join pairs on a hard identifier. Names, zips and state lines do not count.
A37 scored here too and is left out — it ran and died on name collisions.

| # | title | hard pairs | keys | rows | status |
|---|---|---|---|---|---|
| 6 | Dialysis clinic chains in rural areas | 9 of 9 | CCN, NPI | 30,613,170 | part done |
| 123 | U.S. banks and polluters with unclear corporate parents | 7 of 7 | LEI, LEI_2018 | 15,001,221 | not started |
| 27 | People applying to become Medicare providers | 6 of 6 | NPI | 2,358,060 | found something |
| 1 | Excluded doctors and the hospices/nursing homes that keep them | 6 of 6 | NPI | 2,364,431 | part done |
| 12 | Long-term care hospitals | 6 of 6 | CCN, NPI | 17,689,980 | part done |
| E74 | Home health agencies that change owners | 4 of 8 | CCN, NPI | 125,088 | part done |
| 81 | Company pension plans that collapse onto the government | 4 of 4 | ADSH, EIN, SPONS_DFE_EIN | 6,983,857 | not started |
| 31 | Hospitals that also own home health agencies | 3 of 5 | CCN, NPI | 33,075 | found a little |
| 11 | Hospitals losing money, and their doctors | 3 of 3 | NPI, PROVIDER_CCN | 16,967,082 | part done |
| 2 | Private equity-owned nursing home chains | 3 of 3 | CMS_CERTIFICATION_NUMBER_CCN | 449,372 | found something |
| 4 | Doctors treating addiction, and drug companies | 3 of 3 | NPI, Prscrbr_NPI | 39,177,643 | found something |
| 28 | Nursing homes and how sick they say their patients are | 3 of 3 | CCN, CMS_CERTIFICATION_NUMBER_CCN | 31,836,407 | part done |
| 124 | Wealthy nonprofit hospitals | 3 of 3 | EIN | 526,374 | found something |
| 125 | Political nonprofits that lost their tax status | 2 of 4 | EIN | 1,340,465 | not started |
| E37 | Doctors and the drug industry money they get | 2 of 4 | NPI | 31,502,716 | nothing there |

---

## 6. Dialysis clinic chains in rural areas

**Ask** — Do dialysis chains that dominate a rural area have worse patient outcomes?
**Why** — Would show monopoly power hurting sick people

| field | value |
|---|---|
| hard join pairs | 9 of 9 |
| keys | CCN, NPI |
| family | HEALTH |
| rows | 30,613,170 |
| window | one vintage |
| effort | Medium — partial run, needs finishing |
| status | part done |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_DIALYSIS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`

**Join on**
```
HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 34 shared]
HEALTH__FED_CMS_OPEN_PAYMENTS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 500450 shared]
HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 326347 shared]
HEALTH__FED_CMS_DIALYSIS.CCN = HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES.CCN [CCN]
HEALTH__FED_CMS_DIALYSIS.CCN = HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN [CCN]
HEALTH__FED_CMS_DIALYSIS.CCN = HEALTH__FED_CMS_OPEN_PAYMENTS.CCN [CCN]
HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES.NPI = HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE.NPI [NPI]
HEALTH__FED_CMS_MEDICARE_DIALYSIS_FACILITIES.NPI = HEALTH__FED_CMS_OPEN_PAYMENTS.NPI [NPI]
HEALTH__FED_CMS_QUALITY_PAYMENT_PROGRAM_EXPERIENCE.NPI = HEALTH__FED_CMS_OPEN_PAYMENTS.NPI [NPI]
```

**Watch out** — Partially checked, needs a full run

---

## 123. U.S. banks and polluters with unclear corporate parents

**Ask** — Who's the real parent company hiding behind them?
**Why** — Would unmask ownership nobody discloses

| field | value |
|---|---|
| hard join pairs | 7 of 7 |
| keys | LEI, LEI_2018 |
| family | CROSS 3+ |
| rows | 15,001,221 |
| window | current |
| effort | Medium — first probe query needed |
| status | not started |

**Tables**
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF_REPEX`
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__INTL_GLEIF`
- `LIBRARY_MARTS.HOUSING.HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF`
- `LIBRARY_MARTS.ENVIRONMENT.ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK`

**Join on**
```
ECONOMICS__INTL_GLEIF.LEI = ECONOMICS__INTL_GLEIF_REPEX.LEI [measured 3142422 shared]
ECONOMICS__INTL_GLEIF_REPEX.LEI = ECONOMICS__INTL_GLEIF.LEI [measured 3142422 shared]
ECONOMICS__INTL_GLEIF_REPEX.LEI = HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF.LEI_2018 [LEI]
ECONOMICS__INTL_GLEIF_REPEX.LEI = ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK.MATCHED_LEI [LEI]
ECONOMICS__INTL_GLEIF.LEI = HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF.LEI_2018 [LEI]
ECONOMICS__INTL_GLEIF.LEI = ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK.MATCHED_LEI [LEI]
HOUSING__FED_CFPB_HMDA_ARID2017_LEI_XREF.LEI_2018 = ENVIRONMENT__XC_EPA_CORPORATE_CROSSWALK.MATCHED_LEI [LEI]
```

**Watch out** — no query run yet, treat any first number as unverified

---

## 27. People applying to become Medicare providers

**Ask** — Are any of them already banned for past fraud?
**Why** — Would catch fraud before it even starts

| field | value |
|---|---|
| hard join pairs | 6 of 6 |
| keys | NPI |
| family | HEALTH |
| rows | 2,358,060 |
| window | 2026-07 snapshot |
| effort | Quick — re-run and check the number |
| status | found something |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION`

**Join on**
```
HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 49 shared]
HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 103 shared]
HEALTH__FED_HHS_OIG_LEIE.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 15 shared]
HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS.NPI = HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS.NPI [NPI]
HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_PHYSICIANS.NPI = HEALTH__FED_HHS_OIG_LEIE.NPI [NPI]
HEALTH__FED_CMS_PENDING_INITIAL_LOGGING_AND_TRACKING_NON_PHYSICIANS.NPI = HEALTH__FED_HHS_OIG_LEIE.NPI [NPI]
```

**Watch out** — 9 found, small but real

---

## 1. Excluded doctors and the hospices/nursing homes that keep them

**Ask** — Are doctors banned from Medicare still showing up on hospice paperwork?
**Why** — Banned doctors shouldn't still be treating dying patients

| field | value |
|---|---|
| hard join pairs | 6 of 6 |
| keys | NPI |
| family | HEALTH+IMMIGRATION |
| rows | 2,364,431 |
| window | affiliation snapshot 2026-07 |
| effort | Medium — partial run, needs finishing |
| status | part done |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_HHS_OIG_LEIE`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION`
- `LIBRARY_MARTS.IMMIGRATION.IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS`

**Join on**
```
HEALTH__FED_HHS_OIG_LEIE.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 15 shared]
HEALTH__FED_HHS_OIG_LEIE.NPI = IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS.NPI [NPI]
HEALTH__FED_HHS_OIG_LEIE.NPI = HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.NPI [NPI]
HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI = IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS.NPI [NPI]
HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI = HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.NPI [NPI]
IMMIGRATION__FED_CMS_HOSPICE_ENROLLMENTS.NPI = HEALTH__FED_CMS_SKILLED_NURSING_FACILITY_ENROLLMENTS.NPI [NPI]
```

**Watch out** — Found 4 so far, confirmed

---

## 12. Long-term care hospitals

**Ask** — Do hospitals with financial trouble also have padded ventilator equipment billing?
**Why** — Would show equipment fraud on the sickest patients

| field | value |
|---|---|
| hard join pairs | 6 of 6 |
| keys | CCN, NPI |
| family | HEALTH |
| rows | 17,689,980 |
| window | 2023 |
| effort | Medium — partial run, needs finishing |
| status | part done |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_LTCH`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_POS_OTHER`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`

**Join on**
```
HEALTH__FED_CMS_OPEN_PAYMENTS.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 500450 shared]
HEALTH__FED_CMS_LTCH.CCN = HEALTH__FED_CMS_POS_OTHER.CCN [CCN]
HEALTH__FED_CMS_LTCH.CCN = HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN [CCN]
HEALTH__FED_CMS_LTCH.CCN = HEALTH__FED_CMS_OPEN_PAYMENTS.CCN [CCN]
HEALTH__FED_CMS_POS_OTHER.CCN = HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN [CCN]
HEALTH__FED_CMS_POS_OTHER.CCN = HEALTH__FED_CMS_OPEN_PAYMENTS.CCN [CCN]
```

**Watch out** — Partially checked, small group so far

---

## E74. Home health agencies that change owners

**Ask** — Is there a record of who the new owner is?
**Why** — Same shell-game question as #30, for home health

| field | value |
|---|---|
| hard join pairs | 4 of 8 |
| keys | CCN, NPI |
| family | HEALTH |
| rows | 125,088 |
| window | snapshot 2026-07-17; owner arrival dates 1800-2026, 641 pre-1990 rows are sentinels |
| effort | Medium — first probe query needed |
| status | part done |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_OWNERS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH`

**Join on**
```
HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID = HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ASSOCIATE_ID [measured 8933 shared]
HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ENROLLMENT_ID = HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ENROLLMENT_ID [measured 11224 shared]
HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.NPI = HEALTH__FED_CMS_HOME_HEALTH_OWNERS.NPI [measured 11184 shared]
HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ASSOCIATE_ID = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID [measured 8933 shared]
HEALTH__FED_CMS_HOME_HEALTH_OWNERS.ENROLLMENT_ID = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ENROLLMENT_ID [measured 11224 shared]
HEALTH__FED_CMS_HOME_HEALTH_OWNERS.NPI = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.NPI [measured 11184 shared]
HEALTH__FED_CMS_HOME_HEALTH_OWNERS.CCN = HEALTH__FED_CMS_HOME_HEALTH.CCN [CCN]
HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.CCN = HEALTH__FED_CMS_HOME_HEALTH.CCN [CCN]
```

**Watch out** — Owners file landed 2026-09-07 (101,188 rows, 11,494 agencies, 97.7% carry a CCN). Key owners on ASSOCIATE_ID_OWNER not name; flags null on individuals; REIT flag is a constant N; 641 owner dates pre-1990 are sentinels. One snapshot, so "changed owner" reads off ASSOCIATION_DATE_OWNER (4,120 agencies since 2024), not a quarter-over-quarter diff.

---

## 81. Company pension plans that collapse onto the government

**Ask** — Did executives sell their own stock right before the collapse?
**Why** — Would show executives cashing out while workers' pensions failed

| field | value |
|---|---|
| hard join pairs | 4 of 4 |
| keys | ADSH, EIN, SPONS_DFE_EIN |
| family | CROSS 3+ |
| rows | 6,983,857 |
| window | termination year |
| effort | Medium — first probe query needed |
| status | not started |

**Tables**
- `LIBRARY_MARTS.LABOR.LABOR__FED_PBGC_TRUSTEED_PLANS`
- `LIBRARY_RAW.LANDING.FED_DOL_FORM5500_FULL`
- `LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_DERA_SUB_2026Q1`
- `LIBRARY_MARTS.FINANCE.FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS`

**Join on**
```
LABOR__FED_PBGC_TRUSTEED_PLANS.EIN = FED_DOL_FORM5500_FULL.SPONS_DFE_EIN [EIN]
LABOR__FED_PBGC_TRUSTEED_PLANS.EIN = FINANCE__FED_SEC_DERA_SUB_2026Q1.EIN [EIN]
FED_DOL_FORM5500_FULL.SPONS_DFE_EIN = FINANCE__FED_SEC_DERA_SUB_2026Q1.EIN [EIN]
FINANCE__FED_SEC_DERA_SUB_2026Q1.ADSH = FINANCE__FED_SEC_INSIDER_NONDERIV_TRANS.ACCESSION_NUMBER [ACCESSION]
```

**Watch out** — no query run yet, treat any first number as unverified

---

## 31. Hospitals that also own home health agencies

**Ask** — Do hospital-owned home health agencies perform worse but cost more?
**Why** — Would show hospitals steering patients to their own worse service

| field | value |
|---|---|
| hard join pairs | 3 of 5 |
| keys | CCN, NPI |
| family | HEALTH |
| rows | 33,075 |
| window | snapshot |
| effort | Quick — re-run and check the number |
| status | found a little |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HOME_HEALTH`

**Join on**
```
HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID = HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.ASSOCIATE_ID [measured 475 shared]
HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.ASSOCIATE_ID = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.ASSOCIATE_ID [measured 475 shared]
HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.NPI = HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.NPI [measured 4 shared]
HEALTH__FED_CMS_HOSPITAL_ENROLLMENTS.CCN = HEALTH__FED_CMS_HOME_HEALTH.CCN [CCN]
HEALTH__FED_CMS_HOME_HEALTH_AGENCY_ENROLLMENTS.CCN = HEALTH__FED_CMS_HOME_HEALTH.CCN [CCN]
```

**Watch out** — mixed result

---

## 11. Hospitals losing money, and their doctors

**Ask** — Do money-losing hospitals still have doctors taking big drug company payments?
**Why** — Would look hypocritical — cutting care while doctors profit

| field | value |
|---|---|
| hard join pairs | 3 of 3 |
| keys | NPI, PROVIDER_CCN |
| family | HEALTH |
| rows | 16,967,082 |
| window | 2023 |
| effort | Medium — partial run, needs finishing |
| status | part done |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_HCRIS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_AFFILIATION`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023`

**Join on**
```
HEALTH__FED_CMS_OPEN_PAYMENTS_2023.NPI = HEALTH__FED_CMS_FACILITY_AFFILIATION.NPI [measured 472757 shared]
HEALTH__FED_CMS_HCRIS.PROVIDER_CCN = HEALTH__FED_CMS_FACILITY_AFFILIATION.CCN [CCN]
HEALTH__FED_CMS_HCRIS.PROVIDER_CCN = HEALTH__FED_CMS_OPEN_PAYMENTS_2023.CCN [CCN]
```

**Watch out** — Partially checked, real data found

---

## 2. Private equity-owned nursing home chains

**Ask** — Which nursing home owners get fined the most per home, and does it repeat?
**Why** — Shows which owners treat fines as a cost of doing business

| field | value |
|---|---|
| hard join pairs | 3 of 3 |
| keys | CMS_CERTIFICATION_NUMBER_CCN |
| family | HEALTH |
| rows | 449,372 |
| window | deficiencies 2017-26, penalties 2023-06 on |
| effort | Quick — re-run and check the number |
| status | found something |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_PENALTIES`

**Join on**
```
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN = HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN [CCN]
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN = HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN [CCN]
HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN = HEALTH__FED_CMS_NURSING_HOME_PENALTIES.CMS_CERTIFICATION_NUMBER_CCN [CCN]
```

**Watch out** — one chain gets fined 5x more per home than a comparable one

---

## 4. Doctors treating addiction, and drug companies

**Ask** — Do addiction doctors get paid more by drugmakers when they prescribe more?
**Why** — Would be a bribe-for-prescriptions pattern

| field | value |
|---|---|
| hard join pairs | 3 of 3 |
| keys | NPI, Prscrbr_NPI |
| family | HEALTH+RAW |
| rows | 39,177,643 |
| window | one year |
| effort | Small — mart built 2026-09-07, query it |
| status | found something |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS`
- `LIBRARY_RAW.LANDING.FED_CMS_PARTD_PRESCRIBER_DRUG`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2022`

**Join on**
```
HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS.NPI = FED_CMS_PARTD_PRESCRIBER_DRUG.Prscrbr_NPI [NPI]
HEALTH__FED_CMS_OPIOID_TREATMENT_PROGRAM_PROVIDERS.NPI = HEALTH__FED_CMS_OPEN_PAYMENTS_2022.NPI [NPI]
FED_CMS_PARTD_PRESCRIBER_DRUG.Prscrbr_NPI = HEALTH__FED_CMS_OPEN_PAYMENTS_2022.NPI [NPI]
```

**Watch out** — OTP table was the wrong leg, it lists orgs; Part D to Open Payments on NPI

---

## 28. Nursing homes and how sick they say their patients are

**Ask** — Do homes exaggerate patient sickness to get paid more?
**Why** — Would be a well-known Medicare fraud pattern

| field | value |
|---|---|
| hard join pairs | 3 of 3 |
| keys | CCN, CMS_CERTIFICATION_NUMBER_CCN |
| family | HEALTH |
| rows | 31,836,407 |
| window | one quarter |
| effort | Medium — partial run, needs finishing |
| status | part done |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_NURSINGHOME411`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES`

**Join on**
```
HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY.CCN = HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN [CCN]
HEALTH__FED_CMS_FACILITY_LEVEL_MINIMUM_DATA_SET_FREQUENCY.CCN = HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN [CCN]
HEALTH__FED_NURSINGHOME411.CMS_CERTIFICATION_NUMBER_CCN = HEALTH__FED_CMS_NURSING_HOME_DEFICIENCIES.CMS_CERTIFICATION_NUMBER_CCN [CCN]
```

**Watch out** — Partially checked, one time period only so far

---

## 124. Wealthy nonprofit hospitals

**Ask** — How much do they pay their top executives?
**Why** — Extends the charity-care question with executive pay

| field | value |
|---|---|
| hard join pairs | 3 of 3 |
| keys | EIN |
| family | CROSS 3+ |
| rows | 526,374 |
| window | tax years 2016-2025 |
| effort |  thin at both ends |
| status | found something |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__HOSPITAL_OFFICER_PAY`
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_BMF`
- `LIBRARY_RAW.LANDING.FED_IRS_990_EFILE_INDEX`

**Join on**
```
HEALTH__HOSPITAL_OFFICER_PAY.EIN = ECONOMICS__FED_IRS_BMF.EIN [EIN]
HEALTH__HOSPITAL_OFFICER_PAY.EIN = FED_IRS_990_EFILE_INDEX.EIN [EIN]
ECONOMICS__FED_IRS_BMF.EIN = FED_IRS_990_EFILE_INDEX.EIN [EIN]
```

**Watch out** — Done — 526,374 person rows, 3,918 hospital EINs, 23,810 returns

---

## 125. Political nonprofits that lost their tax status

**Ask** — Are they still operating and filing paperwork as if nothing happened?
**Why** — Would show a compliance gap

| field | value |
|---|---|
| hard join pairs | 2 of 4 |
| keys | EIN |
| family | ECONOMICS+POLITICS |
| rows | 1,340,465 |
| window | after revocation |
| effort | Medium — first probe query needed |
| status | not started |

**Tables**
- `LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8871_ORGS`
- `LIBRARY_MARTS.ECONOMICS.ECONOMICS__FED_IRS_AUTO_REVOCATIONS`
- `LIBRARY_MARTS.POLITICS.POLITICS__IRS527_8872_REPORTS`

**Join on**
```
POLITICS__IRS527_8871_ORGS.FORM_ID_NUMBER = POLITICS__IRS527_8872_REPORTS.FORM_ID_NUMBER [measured 243 shared]
POLITICS__IRS527_8872_REPORTS.FORM_ID_NUMBER = POLITICS__IRS527_8871_ORGS.FORM_ID_NUMBER [measured 243 shared]
POLITICS__IRS527_8871_ORGS.EIN = ECONOMICS__FED_IRS_AUTO_REVOCATIONS.EIN [EIN]
ECONOMICS__FED_IRS_AUTO_REVOCATIONS.EIN = POLITICS__IRS527_8872_REPORTS.EIN [EIN]
```

**Watch out** — no query run yet, treat any first number as unverified

---

## E37. Doctors and the drug industry money they get

**Ask** — Does a pay raise from a drug company lead to more prescriptions?
**Why** — The classic 'paid to prescribe' question

| field | value |
|---|---|
| hard join pairs | 2 of 4 |
| keys | NPI |
| family | HEALTH |
| rows | 31,502,716 |
| window | PY2023-24 |
| effort | Medium — partial run, needs finishing |
| status | nothing there |

**Tables**
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS_2023`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_OPEN_PAYMENTS`
- `LIBRARY_MARTS.HEALTH.HEALTH__FED_CMS_PART_D_PRESCRIBERS`

**Join on**
```
HEALTH__FED_CMS_OPEN_PAYMENTS.COVERED_RECIPIENT_PROFILE_ID = HEALTH__FED_CMS_OPEN_PAYMENTS_2023.COVERED_RECIPIENT_PROFILE_ID [measured 715581 shared]
HEALTH__FED_CMS_OPEN_PAYMENTS_2023.COVERED_RECIPIENT_PROFILE_ID = HEALTH__FED_CMS_OPEN_PAYMENTS.COVERED_RECIPIENT_PROFILE_ID [measured 715581 shared]
HEALTH__FED_CMS_OPEN_PAYMENTS_2023.NPI = HEALTH__FED_CMS_PART_D_PRESCRIBERS.NPI [NPI]
HEALTH__FED_CMS_OPEN_PAYMENTS.NPI = HEALTH__FED_CMS_PART_D_PRESCRIBERS.NPI [NPI]
```

**Watch out** — the money is mostly stock deals and consulting fees

---
