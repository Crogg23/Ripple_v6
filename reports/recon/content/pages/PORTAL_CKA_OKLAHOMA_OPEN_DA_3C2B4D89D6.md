# PORTAL_CKA_OKLAHOMA_OPEN_DA_3C2B4D89D6

rows 10.0K  columns 14  scan 4.1s

roles: amount 1, audit 2, category 7, date 1, other 1, who 3

## when

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| AMOUNT | 10.0K | -13.68M | 3.2K | 1.62M | 29.76M | 971.00M |

## who

C_ACCOUNT by rows
       166  512110
       158  521110
       144  521140
       144  533120
       141  531130
       137  521260
       137  521230
       130  521250
       130  513110
       127  521240
       122  513120
       119  531370
       119  521120
       118  521210
       118  531170
       117  521150
       117  533110
       114  532140
       111  511110
       109  531360

C_ACCOUNT by dollars
     366.98M      111 rows  511110
      65.40M       90 rows  562120
      62.95M       58 rows  546210
      49.58M       37 rows  564110
      36.21M      103 rows  513240
      21.04M      166 rows  512110
      20.36M      130 rows  513110
      20.33M       40 rows  548110
      19.73M       12 rows  554110
      17.80M      103 rows  515660
      16.91M       84 rows  512120
      16.59M       16 rows  555110
      14.25M       89 rows  513320
      12.11M       24 rows  511390
      10.44M       24 rows  511330
       8.98M       16 rows  554120
       8.53M       55 rows  541250
       8.34M       99 rows  541120
       7.77M       63 rows  515400
       7.22M       58 rows  515220

ACCOUNT_DESCRIPTION by rows
       166  INSUR.PREM-HLTH-LIFE-STATE PLN
       158  IN-STATE MILEAGE-MOTOR VEHICLE
       144  MTCE-REP.-EQUIPMENT-VENDORS
       144  IN-STATE MISCELLANEOUS CHARGES
       141  TELECOMMUNICATION SERVICES
       137  OUT-OF-STATE LODGING
       137  OUT-OF-STATE MEALS-SUBSISTENCE
       130  STATE SHARE-FICA
       130  OUT-OF-STATE MISC.CHARGES
       127  OUT-OF-STATE LOCAL TRANSP.
       122  STATE SHARE-MQFE/FICA
       119  UTILITY CHARGE-ELECTRICTIY
       119  IN-STATE MEALS-SUBSISTENCE EXP
       118  OUT OF STATE MILEAGE-PRIV.VEH.
       118  INFORMATIONAL SERVICE
       117  IN-STATE LODGING
       117  MTCE-REP.-BLDGS-GRNDS-VENDOR
       114  RENT-EQUIPMENT AND MACHINERY
       111  SALS-REGULAR PAY
       109  REGISTRATION - AGENCY DIRECT

ACCOUNT_DESCRIPTION by dollars
     366.98M      111 rows  SALS-REGULAR PAY
      65.40M       90 rows  TRSF TO TREASURY FUND-ONUS
      62.95M       58 rows  BLDGS,STRUCT.-CONSTR.-RENOV.
      49.58M       37 rows  MDSE-RESALE-RAW MAT.,STK/SUPP.
      36.21M      103 rows  STATE SHARE-OTHER AUTH.RET.SYS
      21.04M      166 rows  INSUR.PREM-HLTH-LIFE-STATE PLN
      20.36M      130 rows  STATE SHARE-FICA
      20.33M       40 rows  PRINCIPAL PAYMENTS-BOND DEBT
      19.73M       12 rows  WITHDRAWALS AGCY/TRUST MONIES
      17.80M      103 rows  EDUCATIONAL SERVICES
      16.91M       84 rows  INSUR.PREM-HLTH-LIFE-OTHER
      16.59M       16 rows  PMTS-LOCAL GOV'T-GEN GOVT
      14.25M       89 rows  SUPPLEMENTAL RETMT PLANS-HED
      12.11M       24 rows  CAFETERIA PLAN - OTHER
      10.44M       24 rows  DEFERRED COMP - EDUCATION
       8.98M       16 rows  APPROVED PROGRAM REIMBURSEMENT
       8.53M       55 rows  EQUIP-LAB
       8.34M       99 rows  DATA PROCESSING EQUIPMENT
       7.77M       63 rows  ADMIN MGMT-GEN.MGMT CONSULTING
       7.22M       58 rows  ARCHITECTURAL SERVICES

SRC_SHA256 by rows
     10.0K  8354f79849c50cfbb63e617b4b6f20c38070fd6cc4bacbd33905716026a6c753

SRC_SHA256 by dollars
     971.00M    10.0K rows  8354f79849c50cfbb63e617b4b6f20c38070fd6cc4bacbd33905716026a6

## who x when

C_ACCOUNT by INGESTED_AT  LOAD STAMP, not an event date, dollars = AMOUNT
  511110                                    2026:366.98M
  512110                                    2026:21.04M
  512120                                    2026:16.91M
  513110                                    2026:20.36M
  513120                                    2026:5.19M
  513240                                    2026:36.21M
  513320                                    2026:14.25M
  515660                                    2026:17.80M
  521110                                    2026:1.47M
  521120                                    2026:384.0K
  521140                                    2026:81.6K
  521150                                    2026:331.8K
  521210                                    2026:358.5K
  521230                                    2026:1.41M
  521240                                    2026:352.4K
  521250                                    2026:641.7K
  521260                                    2026:2.30M
  531130                                    2026:2.48M
  531170                                    2026:775.2K
  531360                                    2026:7.09M
  531370                                    2026:4.61M
  532140                                    2026:2.13M
  533110                                    2026:5.17M
  533120                                    2026:2.95M
  546210                                    2026:62.95M
  548110                                    2026:20.33M
  554110                                    2026:19.73M
  555110                                    2026:16.59M
  562120                                    2026:65.40M
  564110                                    2026:49.58M

ACCOUNT_DESCRIPTION by INGESTED_AT  LOAD STAMP, not an event date, dollars = AMOUNT
  BLDGS,STRUCT.-CONSTR.-RENOV.              2026:62.95M
  EDUCATIONAL SERVICES                      2026:17.80M
  IN-STATE LODGING                          2026:331.8K
  IN-STATE MEALS-SUBSISTENCE EXP            2026:384.0K
  IN-STATE MILEAGE-MOTOR VEHICLE            2026:1.47M
  IN-STATE MISCELLANEOUS CHARGES            2026:81.6K
  INFORMATIONAL SERVICE                     2026:775.2K
  INSUR.PREM-HLTH-LIFE-OTHER                2026:16.91M
  INSUR.PREM-HLTH-LIFE-STATE PLN            2026:21.04M
  MDSE-RESALE-RAW MAT.,STK/SUPP.            2026:49.58M
  MTCE-REP.-BLDGS-GRNDS-VENDOR              2026:5.17M
  MTCE-REP.-EQUIPMENT-VENDORS               2026:2.95M
  OUT OF STATE MILEAGE-PRIV.VEH.            2026:358.5K
  OUT-OF-STATE LOCAL TRANSP.                2026:352.4K
  OUT-OF-STATE LODGING                      2026:2.30M
  OUT-OF-STATE MEALS-SUBSISTENCE            2026:1.41M
  OUT-OF-STATE MISC.CHARGES                 2026:641.7K
  PMTS-LOCAL GOV'T-GEN GOVT                 2026:16.59M
  PRINCIPAL PAYMENTS-BOND DEBT              2026:20.33M
  REGISTRATION - AGENCY DIRECT              2026:1.09M
  RENT-EQUIPMENT AND MACHINERY              2026:2.13M
  SALS-REGULAR PAY                          2026:366.98M
  STATE SHARE-FICA                          2026:20.36M
  STATE SHARE-MQFE/FICA                     2026:5.19M
  STATE SHARE-OTHER AUTH.RET.SYS            2026:36.21M
  SUPPLEMENTAL RETMT PLANS-HED              2026:14.25M
  TELECOMMUNICATION SERVICES                2026:2.48M
  TRSF TO TREASURY FUND-ONUS                2026:65.40M
  UTILITY CHARGE-ELECTRICTIY                2026:4.61M
  WITHDRAWALS AGCY/TRUST MONIES             2026:19.73M

## what

AGENCY_NUMBER: 1000 20%, 4000 15%, 2500 11%, 4100 11%, 1100 7%, 1500 6%, 1300 6%, 1400 5%, 1200 5%, 3000 5%, 2000 5%, 3900 5%

AGENCY_NAME: OKLAHOMA STATE UNIVERSITY 20%, DEPARTMENT OF AGRICULTURE 15%, OKLAHOMA MILITARY DEPARTMENT 11%, WESTERN OKLA. STATE COLLEGE 11%, OSU-EXPERIMENT STATION 7%, OSU-OKLAHOMA CITY 6%, OSU-TECHNICAL BRANCH, OKMULGEE 6%, OSU COLLEGE OF VETERINARY MEDI 5%, OSU-EXTENSION DIVISION 5%, ALCOHOLIC BEV. LAWS ENFORCE. 5%, OKLAHOMA ACCOUNTANCY BOARD 5%, BOLL WEEVIL ERADICATION ORG. 5%

ACCOUNT_MAJOR_CLASS: 530000 39%, 510000 30%, 520000 17%, 540000 10%, 550000 3%, 560000 2%

ACCOUNT_DESCRIPTION_MAJOR_CLASS: ADMINISTRATIVE EXPENSE         39%, PERSONAL SERVICES              30%, TRAVEL                         17%, PROP,FURN,EQUIP & RELATED DEBT 10%, GEN ASST, AWDS, PROG-DIRECTED  3%, TRANSFERS & OTHER DISBURSMNTS  2%

ACCOUNT_SUB_CLASS: 531000 18%, 521000 16%, 515000 14%, 533000 9%, 541000 8%, 511000 8%, 513000 7%, 536000 5%, 532000 5%, 512000 4%, 522000 3%, 537000 3%

ACCOUNT_DESCRIPTION_SUB_CLASS: MISC. ADMINISTRATIVE EXPENSES  18%, TRAVEL - REIMBURSEMENTS        16%, PROFESSIONAL SERVICES          14%, MAINTENANCE & REPAIR EXPENSE   9%, OFFICE FURNITURE & EQUIPMENT   8%, SALARY EXPENSE                 8%, FICA-RETIREMENT CONTRIBUTIONS  7%, GENERAL OPERATING EXPENSES     5%, RENT EXPENSE                   5%, INSUR.PREM-HLTH-LIFE,ETC       4%, TRAVEL - AGENCY DIRECT PMTS    3%, SHOP EXPENSE                   3%

ACCOUNTING_PERIOD: 2 9%, 12 9%, 11 9%, 4 9%, 7 8%, 8 8%, 9 8%, 5 8%, 10 8%, 6 8%, 3 8%, 1 8%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCY_NUMBER | category | 17 | 0 | 1000 1.7K; 4000 1.4K; 2500 1.0K; 4100 940 |
| AGENCY_NAME | category | 17 | 0 | OKLAHOMA STATE UNIVERSITY 1.7K; DEPARTMENT OF AGRICULTURE 1.4K; OKLAHOMA MILITARY DEPARTM 1.0K; WESTERN OKLA. STATE COLLE 940 |
| ACCOUNT_MAJOR_CLASS | category | 6 | 0 | 530000 3.9K; 510000 3.0K; 520000 1.7K; 540000 952 |
| ACCOUNT_DESCRIPTION_MAJOR_CLASS | category | 6 | 0 | ADMINISTRATIVE EXPENSE    3.9K; PERSONAL SERVICES         3.0K; TRAVEL                    1.7K; PROP,FURN,EQUIP & RELATED 952 |
| ACCOUNT_SUB_CLASS | category | 36 | 0 | 531000 1.6K; 521000 1.4K; 515000 1.2K; 533000 763 |
| ACCOUNT_DESCRIPTION_SUB_CLASS | category | 36 | 0 | MISC. ADMINISTRATIVE EXPE 1.6K; TRAVEL - REIMBURSEMENTS   1.4K; PROFESSIONAL SERVICES     1.2K; MAINTENANCE & REPAIR EXPE 763 |
| C_ACCOUNT | who | 226 | 0 | 512110 166; 521110 158; 533120 144; 521140 144 |
| ACCOUNT_DESCRIPTION | who | 232 | 0 | INSUR.PREM-HLTH-LIFE-STAT 166; IN-STATE MILEAGE-MOTOR VE 158; MTCE-REP.-EQUIPMENT-VENDO 144; IN-STATE MISCELLANEOUS CH 144 |
| FISCAL_YEAR | other | 1 | 0 | 2008 10.0K |
| ACCOUNTING_PERIOD | category | 12 | 0 | 2 885; 12 885; 11 883; 4 875 |
| AMOUNT | amount | 8.6K | 0 | $33.52 60; $53.30 59; $13208.19 59; $311.29 57 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:57:44.34405 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 1fff5129-5a95-452a-b6cd-a 10.0K |
| SRC_SHA256 | who | 1 | 0 | 8354f79849c50cfbb63e617b4 10.0K |
