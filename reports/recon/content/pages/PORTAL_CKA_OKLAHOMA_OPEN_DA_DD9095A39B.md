# PORTAL_CKA_OKLAHOMA_OPEN_DA_DD9095A39B

rows 10.0K  columns 54  scan 5.4s

roles: amount 1, audit 2, category 15, date 6, empty 19, id 1, other 4, state 1, who 6

## when

EFFDT
  2021     10.0K  ##############################

INVOICE_DT
  2017         1  
  2018         1  
  2019         2  
  2020        90  
  2021      9.9K  ##############################

PYMNT_DT
  2021     10.0K  ##############################

CANCEL_DT
  2021        18  ##############################

OCP_DS_DATE
  2021     10.0K  ##############################

INGESTED_AT
  2026     10.0K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PYMNT_AMT | 10.0K | -41.8K | 165 | 101.4K | 5.29M | 63.48M |

## who

VENDOR_NAME by rows
      4.7K  PROTECTED INFORMATION
       395  STAPLES BUSINESS ADVANTAGE
       313  THERMO FISHER SCIENTIFIC
       253  OG&E
       160  ONE GAS INC
       134  MUNICIPAL UTILITIES BOARD - PRYOR
       126  LAKE REGION ELECTRIC COOPERATIVE INC
       116  BANK OF AMERICA NA
       107  CITY OF OKLAHOMA CITY
        78  XEROX CORP
        67  DELL MARKETING LP
        64  B&C BUSINESS PRODUCTS INC
        56  CDW GOVERNMENT INC
        49  B & H PHOTO-VIDEO INC.
        47  PUBLIC SERVICE COMPANY OF OKLAHOMA
        45  STANDLEY SYSTEMS INC
        43  WW GRAINGER INC
        41  OKLAHOMA STATE UNIVERSITY
        36  JACKSON BOILER & TANK CO
        33  COMDATA INC

VENDOR_NAME by dollars
      35.64M     4.7K rows  PROTECTED INFORMATION
       9.18M       41 rows  OKLAHOMA STATE UNIVERSITY
       7.56M       14 rows  BANK OF OKLAHOMA, NA
      539.5K        3 rows  INTERNET 2
      464.0K        4 rows  CMSWILLOWBROOK INC
      413.4K       25 rows  OK STATE REGENTS FOR HIGHER EDUCATION
      399.9K        2 rows  MANHATTAN CONSTRUCTION CO
      373.0K        1 rows  LANDMARK GSI
      320.4K       67 rows  DELL MARKETING LP
      318.6K       30 rows  UNIVERSITY OF OKLAHOMA
      236.3K      313 rows  THERMO FISHER SCIENTIFIC
      222.8K        1 rows  Lippert Bros., Inc
      220.3K        2 rows  TIMBERLAKE CONSTRUCTION CO INC
      213.9K        1 rows  SUMMIT TRUCK GROUP
      203.5K       10 rows  EBSCO SUBSCRIPTION SERVICE
      182.7K      253 rows  OG&E
      175.6K        1 rows  TECNIPLAST USA INC
      164.0K        1 rows  NTL MERIT SCHOLARSHIP CORP
      157.4K        5 rows  MACARTHUR ASSOC-CONSULTANTS LLC
      140.6K        3 rows  STUDIO ARCHITECTURE

POSTAL by rows
      4.8K  73105
       393  60696-3689
       316  30384-4705
       253  73124-0990
       166  64121-9296
       146  74078-0001
       134  74362-0249
       126  74441-0127
       116  28202-2196
       107  73126-0570
        79  60680-2555
        68  15250-7496
        67  75267-6021
        64  74074-4606
        56  60675-1515
        51  73023-0460
        49  10087-8072
        46  64141-6267
        36  73154-0824
        35  74078-1027

POSTAL by dollars
      35.69M     4.8K rows  73105
       9.18M       35 rows  74078-1027
       7.56M       14 rows  73196-0200
      539.5K        3 rows  48107-7855
      412.9K       24 rows  73104-6217
      399.9K        2 rows  73104-2244
      373.0K        1 rows  74337-5305
      320.4K       67 rows  75267-6021
      315.9K       18 rows  73019-5300
      239.3K        2 rows  73018-7214
      238.8K      316 rows  30384-4705
      224.6K        2 rows  73023-0807
      222.8K        1 rows  73136-1450
      220.3K        2 rows  73154-0297
      213.9K        1 rows  73106-3215
      203.5K       10 rows  75320-4661
      182.7K      253 rows  73124-0990
      175.6K        1 rows  19380-5964
      164.0K        1 rows  60693-9389
      157.4K        5 rows  73013-2472

ACCTDESCR by rows
      2.2K  Mdse-Resale-Raw Mat.,Stk/Supp.
       543  In-State Mileage-Motor Vehicle
       491  Utility Charge-Electrictiy
       470  Lab,Medical Supplies-Materials
       451  Mtce-Rep.-Bldgs-grnds-Vendor
       341  Office Supplies (Expendable)
       308  In-State Meals-Subsistence Exp
       299  Utility Charge-Other Utilities
       266  Utility Charge Natural Gas
       228  Scholarships-Students
       220  Data Processing Equipment
       211  In-State Miscellaneous Charges
       154  Mtce-Rep.-DP Equip-Vendor
       154  Out-of-State Meals-Subsistence
       149  Educational Services
       148  Mtce-Rep.-Equipment-Vendors
       142  Rent-Elec Data Processing Eq.
       128  Office Supplies Non-Expendable
       100  W/H-Other (Garnish,levies,etc)
        94  Out-of-State Lodging

ACCTDESCR by dollars
      10.13M       31 rows  Principal Payments-Bond Debt
       8.59M       23 rows  Trsf to Treasury Fund-ONUS
       6.69M       45 rows  W/H-Cafeteria
       5.91M       28 rows  W/H-Other Retirement-No Fee
       4.44M     2.2K rows  Mdse-Resale-Raw Mat.,Stk/Supp.
       2.59M       61 rows  Admin Mgmt-Gen.Mgmt Consulting
       2.41M      149 rows  Educational Services
       2.20M       12 rows  Bldgs,Struct.-Constr.-Renov.
       1.58M       50 rows  Mtce-Rep.-Dp Software-Vendors
       1.51M        2 rows  W/H-403b Tax Def Retirement
       1.37M       13 rows  State Income Tax W/H
      818.2K      341 rows  Office Supplies (Expendable)
      795.2K        4 rows  Equip-MV-Comm.Trucks,Buses
      759.0K      451 rows  Mtce-Rep.-Bldgs-grnds-Vendor
      741.1K        2 rows  W/H-457 Tax Def Retirement
      643.1K      100 rows  W/H-Other (Garnish,levies,etc)
      633.9K        2 rows  Prem-Property,Liab.Ins.-Hed
      583.3K       68 rows  Equip-Lab
      522.7K      148 rows  Mtce-Rep.-Equipment-Vendors
      472.0K      491 rows  Utility Charge-Electrictiy

C_ACCOUNT by rows
      2.2K  564110
       543  521110
       491  531370
       470  537190
       451  533110
       341  536140
       308  521120
       299  531350
       266  531360
       228  552110
       220  541120
       211  521140
       154  521230
       154  533140
       149  515660
       148  533120
       142  532160
       128  536130
       100  585390
        94  521260

C_ACCOUNT by dollars
      10.13M       31 rows  548110
       8.59M       23 rows  562120
       6.69M       45 rows  585350
       5.91M       28 rows  585325
       4.44M     2.2K rows  564110
       2.59M       61 rows  515400
       2.41M      149 rows  515660
       2.20M       12 rows  546210
       1.58M       50 rows  533150
       1.51M        2 rows  585370
       1.37M       13 rows  585140
      818.2K      341 rows  536140
      795.2K        4 rows  541280
      759.0K      451 rows  533110
      741.1K        2 rows  585360
      643.1K      100 rows  585390
      633.9K        2 rows  531520
      583.3K       68 rows  541250
      522.7K      148 rows  533120
      472.0K      491 rows  531370

## who x when

VENDOR_NAME by INVOICE_DT, dollars = PYMNT_AMT
  B & H PHOTO-VIDEO INC.                    2021:29.9K
  B&C BUSINESS PRODUCTS INC                 2020:548.69 2021:17.0K
  BANK OF AMERICA NA                        2021:117.6K
  BANK OF OKLAHOMA, NA                      2021:7.56M
  CDW GOVERNMENT INC                        2021:64.1K
  CITY OF OKLAHOMA CITY                     2021:20.1K
  CMSWILLOWBROOK INC                        2021:464.0K
  COMDATA INC                               2021:22.6K
  DELL MARKETING LP                         2021:320.4K
  INTERNET 2                                2021:539.5K
  JACKSON BOILER & TANK CO                  2021:87.2K
  LAKE REGION ELECTRIC COOPERATIVE INC      2021:59.0K
  LANDMARK GSI                              2021:373.0K
  Lippert Bros., Inc                        2021:222.8K
  MANHATTAN CONSTRUCTION CO                 2021:399.9K
  MUNICIPAL UTILITIES BOARD - PRYOR         2021:9.3K
  OG&E                                      2021:182.7K
  OK STATE REGENTS FOR HIGHER EDUCATION     2021:413.4K
  OKLAHOMA STATE UNIVERSITY                 2021:9.18M
  ONE GAS INC                               2019:88.92 2021:17.9K
  PROTECTED INFORMATION                     2017:125 2020:89.9K 2021:35.55M
  PUBLIC SERVICE COMPANY OF OKLAHOMA        2021:52.5K
  STANDLEY SYSTEMS INC                      2021:7.0K
  STAPLES BUSINESS ADVANTAGE                2020:-20.06 2021:60.5K
  SUMMIT TRUCK GROUP                        2021:213.9K
  THERMO FISHER SCIENTIFIC                  2021:236.3K
  TIMBERLAKE CONSTRUCTION CO INC            2021:220.3K
  UNIVERSITY OF OKLAHOMA                    2021:318.6K
  WW GRAINGER INC                           2021:10.3K
  XEROX CORP                                2021:8.2K

POSTAL by INVOICE_DT, dollars = PYMNT_AMT
  10087-8072                                2021:29.9K
  15250-7496                                2021:131.1K
  28202-2196                                2021:117.6K
  30384-4705                                2020:2.4K 2021:236.3K
  48107-7855                                2021:539.5K
  60675-1515                                2021:64.1K
  60680-2555                                2021:7.9K
  60696-3689                                2020:-20.06 2021:45.5K
  64121-9296                                2019:88.92 2021:20.4K
  64141-6267                                2020:1.5K 2021:10.4K
  73018-7214                                2021:239.3K
  73019-5300                                2021:315.9K
  73023-0460                                2021:10.2K
  73023-0807                                2021:224.6K
  73104-2244                                2021:399.9K
  73104-6217                                2021:412.9K
  73105                                     2017:125 2020:89.9K 2021:35.60M
  73124-0990                                2021:182.7K
  73126-0570                                2021:20.1K
  73136-1450                                2021:222.8K
  73154-0297                                2021:220.3K
  73154-0824                                2021:87.2K
  73196-0200                                2021:7.56M
  74074-4606                                2020:548.69 2021:17.0K
  74078-0001                                2021:29.4K
  74078-1027                                2021:9.18M
  74337-5305                                2021:373.0K
  74362-0249                                2021:9.3K
  74441-0127                                2021:59.0K
  75267-6021                                2021:320.4K

## where

STATE: OK 7.6K, IL 712, GA 402, TX 258, MO 243, PA 141, NC 126, NY 66, CA 64, TN 44, KS 43, CO 31

## what

AGENCYNBR: 01000 69%, 02500 15%, 01400 4%, 01100 4%, 01200 3%, 01500 2%, 01300 2%, 01600 1%, 02000 0%, 02200 0%

AGENCYNAME: OKLAHOMA STATE UNIVERSITY 69%, OKLAHOMA MILITARY DEPARTMENT 15%, OSU COLLEGE OF VETERINARY MEDI 4%, OSU-EXPERIMENT STATION 4%, OSU-EXTENSION DIVISION 3%, OSU-OKLAHOMA CITY 2%, OSU-TECHNICAL BRANCH, OKMULGEE 2%, OSU-TULSA 1%, OKLAHOMA ACCOUNTANCY BOARD 0%, OKLAHOMA ABSTRACTORS BOARD 0%

VOUCHER_STYLE: REG 100%, JRNL 0%

VCHR_STYLE_DESCR: Regular Voucher 100%

VOUCHER_ID_RELATED: 00152934 33%, 00152409 27%, 00152784 13%, 00152761 13%, 00151818 13%

TRANSACTION_TYPE: P 100%, W 0%, B 0%

FUND_CODE: 9000 84%, 1000 16%

FUNDDESCR: Higher Educ Component Unit 84%, General Fund - No Divisions 16%

CLASS_FLD: 70100 45%, 29000 26%, 43000 11%, 40000 7%, 19902 6%, 40500 2%, 78900 2%, 20000 0%, 19101 0%, 29500 0%, 21000 0%, 70200 0%

CLASSDESCR: OSU 700 Fund 45%, Educational & Gen Operations 24%, Agency Relationship Fund 11%, Army Federal Reimbursement 7%, GRF - Officer Incentive Progra 6%, Air Guard Reimbursement Funds 2%, ACA Payroll Processing 2%, Educational And Gen Operations 2%, Accountancy Fund 0%, GRF - Duties 0%, Capital Improvements Rev Fund 0%, OK AB BRD REVOLVING FUND 0%

DEPTID: 1000001 46%, 1100001 26%, 2100001 11%, 0200201 5%, 0600607 2%, 0300301 2%, 8900001 2%, 0500502 2%, 0600605 1%, 0600609 1%, 9000001 1%, 8800001 1%

DEPTDESCR: 700 Funds 46%, Instruction 26%, Sponsored Programs 11%, State Accounting-OKSRM-SP 5%, OKC Air Base-Ops & Maintenance 2%, Facilities Maint. (OKSRM-FM) 2%, ACA Payroll Processing 2%, Thunderbird Youth Academy 2%, Training Site - Camp Gruber 1%, Tulsa Air Base-Ops&Maintenance 1%, Capital Improvements 1%, ISD DP - Admin 1%

PROGRAM_CODE: C0103 84%, E0200 8%, D0200 5%, C0100 2%, NP000 0%, C0003 0%, D0103 0%, B0202 0%, B0002 0%

PGMDESCR: HIGHER EDUCATION 84%, AEROSPACE AND DEFENSE 8%, REVENUES & EXPENDITURES 5%, HIGH SCHOOL COMPLETION 2%, No_Program 0%, ADVANCED OFFERINGS 0%, STATE PERSONNEL 0%, LAND 0%, EMERGENCY MANAGEMENT 0%

ITEM_DESCRIPTION: SERVICE: Utilities - All Armor 78%, MAINT:CAP- Over Statutory Amt, 6%, TRADE/MANUAL LABOR/WAREHOUSE:  4%, MAINT:CAP- As Needed, Maintena 3%, IT Utilities - NOT PCARD - FY  2%, Fire Sprinkler System Test & I 2%, MAINT:CAP- Over Statutory Amt, 2%, AUTHORITY ORDER: Interagency / 1%, SERVICE:  Solid Waste - Trash  1%, SERVICE: EA - Janitorial & Cus 1%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCYNBR | category | 10 | 0 | 01000 6.9K; 02500 1.5K; 01400 376; 01100 362 |
| AGENCYNAME | category | 10 | 0 | OKLAHOMA STATE UNIVERSITY 6.9K; OKLAHOMA MILITARY DEPARTM 1.5K; OSU COLLEGE OF VETERINARY 376; OSU-EXPERIMENT STATION 362 |
| CALENDAR_YEAR | other | 1 | 0 | 2021 10.0K |
| CALENDAR_MONTH | other | 1 | 0 | 07 10.0K |
| VENDOR_NAME | who | 1.2K | 0 | PROTECTED INFORMATION 4.7K; STAPLES BUSINESS ADVANTAG 395; THERMO FISHER SCIENTIFIC 313; OG&E 261 |
| CITY | who | 322 | 0 | OKLAHOMA CITY 5.7K; STILLWATER 667; CHICAGO 654; ATLANTA 394 |
| STATE | state | 44 | 4 | OK 7.6K; IL 712; GA 402; TX 258 |
| POSTAL | who | 1.0K | 0 | 73105 4.8K; 60696-3689 393; 30384-4705 316; 73124-0990 260 |
| EFFDT | date | 19 | 0 | 07/08/2021 1.0K; 07/07/2021 847; 07/13/2021 763; 07/28/2021 734 |
| VOUCHER_ID | other | 8.4K | 0 | 00152797 141; 00153187 76; 00152940 55; 00152949 54 |
| VOUCHER_STYLE | category | 2 | 0 | REG 10.0K; JRNL 15 |
| VCHR_STYLE_DESCR | category | 2 | 15 | Regular Voucher 10.0K |
| VOUCHER_ID_RELATED | category | 6 | 10.0K | 00152934 5; 00152409 4; 00152784 2; 00152761 2 |
| INVOICE_DT | date | 200 | 15 | 07/07/2021 660; 06/30/2021 586; 07/06/2021 509; 07/01/2021 507 |
| TRANSACTION_TYPE | category | 3 | 0 | P 10.0K; W 18; B 15 |
| PYMNT_AMT | amount | 7.4K | 0 | 25 167; 90 91; 1000 69; 0 67 |
| PYMNT_DT | date | 20 | 33 | 07/08/2021 1.0K; 07/07/2021 845; 07/13/2021 763; 07/28/2021 734 |
| CANCEL_DT | date | 7 | 10.0K | 07/06/2021 7; 07/26/2021 5; 07/09/2021 3; 07/30/2021 1 |
| FUND_CODE | category | 2 | 0 | 9000 8.4K; 1000 1.6K |
| FUNDDESCR | category | 3 | 15 | Higher Educ Component Uni 8.4K; General Fund - No Divisio 1.6K |
| CLASS_FLD | category | 27 | 0 | 70100 4.5K; 29000 2.6K; 43000 1.1K; 40000 660 |
| CLASSDESCR | category | 28 | 0 | OSU 700 Fund 4.5K; Educational & Gen Operati 2.4K; Agency Relationship Fund 1.1K; Army Federal Reimbursemen 660 |
| DEPTID | category | 29 | 0 | 1000001 4.5K; 1100001 2.6K; 2100001 1.1K; 0200201 495 |
| DEPTDESCR | category | 33 | 15 | 700 Funds 4.5K; Instruction 2.6K; Sponsored Programs 1.1K; State Accounting-OKSRM-SP 494 |
| C_ACCOUNT | who | 157 | 0 | 564110 2.2K; 521110 543; 531370 491; 537190 470 |
| ACCTDESCR | who | 160 | 0 | Mdse-Resale-Raw Mat.,Stk/ 2.2K; In-State Mileage-Motor Ve 543; Utility Charge-Electricti 491; Lab,Medical Supplies-Mate 470 |
| OPERATING_UNIT | empty | 1 | 10.0K |  |
| OPERUNITDESCR | empty | 1 | 10.0K |  |
| PRODUCT | empty | 1 | 10.0K |  |
| PRODUCTDESCR | empty | 1 | 10.0K |  |
| PROGRAM_CODE | category | 9 | 0 | C0103 8.4K; E0200 790; D0200 518; C0100 193 |
| PGMDESCR | category | 9 | 0 | HIGHER EDUCATION 8.4K; AEROSPACE AND DEFENSE 790; REVENUES & EXPENDITURES 518; HIGH SCHOOL COMPLETION 193 |
| BUDGET_REF | empty | 1 | 10.0K |  |
| CHARTFIELD1 | empty | 1 | 10.0K |  |
| CF1DESCR | empty | 1 | 10.0K |  |
| CHARTFIELD2 | empty | 1 | 10.0K |  |
| CF2DESCR | empty | 1 | 10.0K |  |
| PROJECT_ID | empty | 1 | 10.0K |  |
| PROJDESCR | empty | 1 | 10.0K |  |
| ACTIVITY | empty | 1 | 10.0K |  |
| ACTVDESCR | empty | 1 | 10.0K |  |
| RESTYPE | empty | 1 | 10.0K |  |
| RESDESCR | empty | 1 | 10.0K |  |
| RCAT | empty | 1 | 10.0K |  |
| RCATDESCR | empty | 1 | 10.0K |  |
| RSUBCAT | empty | 1 | 10.0K |  |
| RSUBCATDESCR | empty | 1 | 10.0K |  |
| PO_ID | other | 54 | 9.3K | 0259006735 437; 0259007038 44; 0259006328 34; 0259006713 22 |
| ITEM_DESCRIPTION | category | 48 | 9.3K | SERVICE: Utilities - All  481; MAINT:CAP- Over Statutory 36; TRADE/MANUAL LABOR/WAREHO 22; MAINT:CAP- As Needed, Mai 20 |
| OCP_DS_DATE | date | 2 | 15 | 08/14/2021 10.0K |
| ROWID | id | 10.0K | 0 | AAATM9AAEAALJzKAAB 50; AAATM9AAEAALJzKAAA 50; AAATM9AAEAALJzJAAN 50; AAATM9AAEAALJzJAAM 50 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 23:02:19.55389 10.0K |
| SOURCE_RUN_ID | audit | 1 | 0 | 03c37918-4609-4475-9152-b 10.0K |
| SRC_SHA256 | who | 1 | 0 | 4e7874f6501d917b1c237ba18 10.0K |
