# PORTAL_CKA_OKLAHOMA_OPEN_DA_B1C8714A03

rows 2.9K  columns 53  scan 5.9s

roles: amount 1, audit 2, category 13, date 5, empty 20, other 4, state 1, who 8

## when

EFFDT
  2024      2.9K  ##############################

INVOICE_DT
  2021         1  
  2023         1  
  2024       163  ##############################

PYMNT_DT
  2024       165  ##############################

OCP_DS_DATE
  2024       165  ##############################

INGESTED_AT
  2026      2.9K  ##############################

## how big
| column | n | min | median | p99 | max | sum |
|---|---|---|---|---|---|---|
| PYMNT_AMT | 2.9K | -1 | 0 | 73.3K | 4.02M | 25.48M |

## who

VENDOR_NAME by rows
       365  OFFICE OF MANAGEMENT & ENTERPRISE SVCS
       265  MULTIPLE PAYEE
       256  BANK OF AMERICA NA
       111  GALT FOUNDATION
       103  AT&T CORP
        97  LOCALPEOPLE LLC
        86  APFS STAFFING INC
        72  ICETECH INC
        61  OKLAHOMA STATE DEPARTMENT OF HEALTH
        45  OKLAHOMA HEALTH CARE AUTHORITY
        45  OKLAHOMA CAREER AND TECHNOLOGY EDUCATION
        36  PROTECTED INFORMATION
        34  OKLA PARTNERSHIP SCHL READINESS FDTN INC
        33  UNIVERSITY OF OKLAHOMA
        30  MEYERCORD REVENUE INC
        29  XEROX CORPORATION
        28  PRESORT FIRST CLASS INCORPORATED
        27  JP MORGAN CHASE
        26  OKLA LAW ENFORCEMENT RETIREMENT SYSTEM
        26  COX COMMUNICATIONS INC

VENDOR_NAME by dollars
      21.46M       45 rows  OKLAHOMA HEALTH CARE AUTHORITY
       1.42M        6 rows  DEPARTMENT OF HUMAN SERVICES
      660.7K       33 rows  UNIVERSITY OF OKLAHOMA
      374.2K        3 rows  STATE AUDITOR AND INSPECTOR
      300.9K      365 rows  OFFICE OF MANAGEMENT & ENTERPRISE SVCS
      251.1K       24 rows  BOARD OF REGENTS OF THE UNIV OF OK HSC
      219.8K        2 rows  DISTRICT ATTORNEYS COUNCIL
      199.5K       36 rows  PROTECTED INFORMATION
      150.5K        4 rows  CAPITOL IMPROVEMENT AUTHORITY
      118.8K        7 rows  OKLAHOMA CORRECTIONAL INDUSTRIES
      103.2K       45 rows  OKLAHOMA CAREER AND TECHNOLOGY EDUCATION
       71.7K        1 rows  SOUTHWESTERN OKLAHOMA STATE UNIVERSITY
       39.5K        2 rows  ONENET
       26.3K        1 rows  EAST CENTRAL UNIVERSITY
       24.8K        1 rows  DEPARTMENT OF LIBRARIES
       15.6K        1 rows  UNIVERSITY OF SCIENCE & ARTS OF OKLAHOMA
       11.3K        2 rows  OFFICE OF THE ATTORNEY GENERAL
       11.0K        4 rows  DEPARTMENT OF ENVIRONMENTAL QUALITY
        7.9K       18 rows  OKLAHOMA DEPARTMENT OF CORRECTIONS
        1.1K        1 rows  STATE BUREAU OF INVESTIGATION

POSTAL by rows
       435  73105
       365  73124-8984
       256  28202-2196
       111  73003-5006
       103  73108-2066
        97  73025-1877
        86  60677-7000
        72  73127-6118
        65  73102-6406
        45  73105-5101
        45  74074-4364
        34  73106-5488
        32  73019-4039
        30  60188-1830
        29  73134-2630
        28  73101-2280
        27  60197-4475
        26  73101-2027
        26  30328-4524
        26  30384-8568

POSTAL by dollars
      21.46M       45 rows  73105-5101
       1.41M        1 rows  73125-0352
      657.3K        1 rows  73019-9705
      374.2K        3 rows  73105-4805
      300.9K      365 rows  73124-8984
      251.1K       24 rows  73126-0901
      219.8K        2 rows  73103-3710
      199.5K      435 rows  73105
      150.6K       10 rows  73105-4801
      126.5K        8 rows  73111-4219
      103.2K       45 rows  74074-4364
       71.7K        1 rows  73096-3001
       39.5K        2 rows  73101-8800
       26.3K        1 rows  74820-6999
       24.8K        1 rows  73105-3205
       15.6K        1 rows  73018-5322
       12.7K        5 rows  73124-8893
       11.3K        2 rows  73105-3207
       11.0K        4 rows  73102-6010
        3.3K       32 rows  73019-4039

C_ACCOUNT by rows
       252  551250
       130  532140
       128  531130
       125  512310
       124  515570
        95  552110
        95  552120
        89  515440
        78  515430
        74  532110
        72  543110
        63  555110
        60  515380
        56  536130
        48  537190
        47  531150
        45  521110
        44  532160
        44  533150
        42  515610

C_ACCOUNT by dollars
      13.24M       29 rows  551120
       8.28M       22 rows  551110
       1.61M       14 rows  562120
      981.1K       20 rows  515660
      374.2K       29 rows  515060
      219.8K        2 rows  555140
      133.9K       74 rows  532110
      121.5K       56 rows  536130
       76.4K        2 rows  548120
       74.1K        2 rows  548110
       71.7K       12 rows  515540
       56.3K       24 rows  519130
       43.0K        2 rows  515460
       40.8K       60 rows  515380
       40.3K      128 rows  531130
       33.0K        2 rows  515370
       32.9K        9 rows  535180
       11.0K        6 rows  515290
        7.9K       34 rows  554120
        5.9K       19 rows  515010

ACCTDESCR by rows
       252  OthHlth Svc.-(Non-DHS)
       130  Rent-Equipment And Machinery
       128  Telecommunication Services
       125  Insur.Prem-Workers Comp.
       124  Employment Placement Services
        95  Scholarships-Students
        95  Teacher Stipends
        89  Other Mgmt Consulting Services
        78  Process,Logistic Consult. Svc
        74  Rent of Office Space
        72  Lease Purchase-Furniture,Equip
        63  Pmts-Local Gov't-Gen Govt
        60  Other Computer Related Svc
        56  Office Supplies Non-Expendable
        48  Lab,Medical Supplies-Materials
        47  Printing & Binding Contrs
        45  In-State Mileage-Motor Vehicle
        44  Mtce-Rep.-Dp Software-Vendors
        44  Rent-Elec Data Processing Eq.
        42  Business Service Centers

ACCTDESCR by dollars
      13.24M       29 rows  Assistance-Misc. Medical
       8.28M       22 rows  Assistance Payments
       1.61M       14 rows  Trsf to Treasury Fund-ONUS
      981.1K       20 rows  Educational Services
      374.2K       29 rows  Acctg,Tax,Books,Payroll Svc
      219.8K        2 rows  Pmts-Local Gov't-Hlth,Soc Svc
      133.9K       74 rows  Rent of Office Space
      121.5K       56 rows  Office Supplies Non-Expendable
       76.4K        2 rows  Interest Payments-Bond Debt
       74.1K        2 rows  Principal Payments-Bond Debt
       71.7K       12 rows  Other Prof, Sc. & Tech.Svc
       56.3K       24 rows  Flexible Benefits-Adminis.
       43.0K        2 rows  Other Scientific-Tech.Cons.Svc
       40.8K       60 rows  Other Computer Related Svc
       40.3K      128 rows  Telecommunication Services
       33.0K        2 rows  Computer Facilities Mgmt Svc
       32.9K        9 rows  Safety and Security Supplies
       11.0K        6 rows  Testing Laboratories
        7.9K       34 rows  Approved Program Reimbursement
        5.9K       19 rows  Offices Of Lawyers

## who x when

VENDOR_NAME by INVOICE_DT, dollars = PYMNT_AMT
  BOARD OF REGENTS OF THE UNIV OF OK HSC    2023:11.2K 2024:239.9K
  CAPITOL IMPROVEMENT AUTHORITY             2024:150.5K
  DEPARTMENT OF HUMAN SERVICES              2024:1.42M
  DEPARTMENT OF LIBRARIES                   2024:24.8K
  DISTRICT ATTORNEYS COUNCIL                2024:219.8K
  EAST CENTRAL UNIVERSITY                   2024:26.3K
  OFFICE OF MANAGEMENT & ENTERPRISE SVCS    2021:-1 2024:300.9K
  OKLAHOMA CAREER AND TECHNOLOGY EDUCATION  2024:103.2K
  OKLAHOMA CORRECTIONAL INDUSTRIES          2024:118.8K
  OKLAHOMA HEALTH CARE AUTHORITY            2024:21.46M
  OKLAHOMA STATE DEPARTMENT OF HEALTH       2024:342
  ONENET                                    2024:39.5K
  PROTECTED INFORMATION                     2024:199.5K
  SOUTHWESTERN OKLAHOMA STATE UNIVERSITY    2024:71.7K
  STATE AUDITOR AND INSPECTOR               2024:374.2K
  UNIVERSITY OF OKLAHOMA                    2024:660.7K

POSTAL by INVOICE_DT, dollars = PYMNT_AMT
  73019-4039                                2024:3.3K
  73019-9705                                2024:657.3K
  73096-3001                                2024:71.7K
  73101-8800                                2024:39.5K
  73102-6406                                2024:342
  73103-3710                                2024:219.8K
  73105                                     2024:199.5K
  73105-4801                                2024:150.6K
  73105-4805                                2024:374.2K
  73105-5101                                2024:21.46M
  73111-4219                                2024:126.5K
  73124-8984                                2021:-1 2024:300.9K
  73125-0352                                2024:1.41M
  73126-0901                                2023:11.2K 2024:239.9K
  74074-4364                                2024:103.2K
  74820-6999                                2024:26.3K

## where

STATE: OK 2.2K, NC 258, IL 177, TX 89, GA 72, CT 29, TN 27, FL 26, NY 14, KS 10, CO 8, PA 5

## what

AGENCYNBR: 34000 35%, 22000 17%, 26500 11%, 83000 8%, 80000 7%, 67700 7%, 69500 5%, 29000 2%, 45200 2%, 27000 2%, 51000 2%, 08500 2%

AGENCYNAME: OKLAHOMA STATE DEPARTMENT OF H 35%, DISTRICT ATTORNEYS COUNCIL 17%, DEPARTMENT OF EDUCATION 11%, DEPARTMENT OF HUMAN SERVICES 8%, OKLA. CAREER AND TECHNOLOGY ED 7%, SUPREME COURT 7%, OKLAHOMA TAX COMMISSION 5%, EMPLOYMENT SECURITY COMMISSION 2%, MENTAL HEALTH AND SUBSTANCE AB 2%, STATE ELECTION BOARD 2%, OKLA. BOARD OF NURSING 2%, OKLAHOMA BROADBAND OFFICE 2%

VOUCHER_STYLE: JRNL 94%, REG 6%

VCHR_STYLE_DESCR: Regular Voucher 100%

TRANSACTION_TYPE: B 94%, P 6%

FUND_CODE: 1000 95%, 9000 4%, 7300 1%, 5400 0%, 1130 0%

FUNDDESCR: General Fund - No Divisions 90%, Assets Held for Beneficiaries 10%

CLASS_FLD: 40000 23%, 21000 17%, 19401 16%, 20000 9%, 45000 8%, 24000 5%, 22500 5%, 32400 4%, 19311 4%, 43000 4%, 49000 3%, 29000 2%

DEPTDESCR: Support Services 24%, 700 Fund Budget 13%, Waiver Services 12%, State Share 9%, Programs 8%, Administration IT 7%, Financial Services 6%, Child Support Services 6%, Medicaid 6%, TANF 6%, General Operations 4%

PROGRAM_CODE: D0001 23%, NP000 19%, C0201 12%, D0101 9%, B0003 7%, B0100 7%, A0100 6%, C0103 5%, A0200 5%, E0102 3%, A0201 2%, A0104 2%

PGMDESCR: ADMINISTRATION AND PENSIONS 23%, NO_PROGRAM 19%, STUDENT PERFORMANCE 12%, LICENSING AND REGULATION 9%, LEGAL AND JUDICIAL 7%, CRIME 7%, IMMUNIZATIONS & INFECTIOUS DIS 6%, HIGHER EDUCATION 5%, HEALTH SERVICES 5%, WORKFORCE PARTICIPATION 3%, BEHAVIORAL HEALTH 2%, COVID 19 2%

PO_ID: 8309026606 19%, 8309026516 12%, 8309026863 12%, 8309027062 12%, 8309026779 12%, 8309026685 6%, 8309026592 6%, 8309027163 6%, 8309026875 6%, 8309027047 6%

ITEM_DESCRIPTION: AO IT Landlines FY-24 19%, AUTHORITY ORDER: Emergency Pur 12%, Wardrobe,Office Tables,Accesso 12%, SERVICE: Consultant contracts~ 12%, OCCY  9/1/2023-6/30/2024 12%, Romeo Standard Table 30"H x 72 6%, Romeo Standard Table 24"H x 60 6%, FY-25 AO IT Landlines 6%, Romeo Flip Top Table 24"Hx60"W 6%, 03/01/24-02/28/25 OMES Credit  6%

## every column
| column | roles | distinct | blank | top values |
|---|---|---|---|---|
| AGENCYNBR | category | 46 | 0 | 34000 875; 22000 416; 26500 264; 83000 201 |
| AGENCYNAME | category | 46 | 0 | OKLAHOMA STATE DEPARTMENT 875; DISTRICT ATTORNEYS COUNCI 416; DEPARTMENT OF EDUCATION 264; DEPARTMENT OF HUMAN SERVI 201 |
| CALENDAR_YEAR | other | 1 | 0 | 2024 2.9K |
| CALENDAR_MONTH | other | 1 | 0 | 07 2.9K |
| VENDOR_NAME | who | 298 | 0 | OFFICE OF MANAGEMENT & EN 365; MULTIPLE PAYEE 265; BANK OF AMERICA NA 256; GALT FOUNDATION 111 |
| CITY | who | 98 | 0 | OKLAHOMA CITY 1.4K; CHARLOTTE 256; EDMOND 219; TULSA 95 |
| STATE | state | 20 | 0 | OK 2.2K; NC 258; IL 177; TX 89 |
| POSTAL | who | 255 | 0 | 73105 435; 73124-8984 365; 28202-2196 256; 73003-5006 111 |
| EFFDT | date | 22 | 0 | 7/30/2024 0:00 389; 7/3/2024 0:00 218; 7/10/2024 0:00 214; 7/11/2024 0:00 211 |
| VOUCHER_ID | other | 1.3K | 0 | 00505795 60; 00505054 32; 00116761 32; 00116744 31 |
| VOUCHER_STYLE | category | 2 | 0 | JRNL 2.7K; REG 165 |
| VCHR_STYLE_DESCR | category | 2 | 2.7K | Regular Voucher 165 |
| VOUCHER_ID_RELATED | other | 1.0K | 286 | 00502933 60; 00500004 31; 00115032 31; 00115031 30 |
| INVOICE_DT | date | 44 | 2.7K | 7/10/2024 0:00 19; 7/3/2024 0:00 16; 6/26/2024 0:00 11; 6/13/2024 0:00 10 |
| TRANSACTION_TYPE | category | 2 | 0 | B 2.7K; P 165 |
| PYMNT_AMT | amount | 153 | 0 | 0 2.7K; 100 4; 40 2; 125 2 |
| PYMNT_DT | date | 22 | 2.7K | 7/22/2024 0:00 29; 7/23/2024 0:00 16; 7/25/2024 0:00 16; 7/10/2024 0:00 12 |
| CANCEL_DT | empty | 1 | 2.9K |  |
| FUND_CODE | category | 6 | 2 | 1000 2.8K; 9000 124; 7300 18; 5400 4 |
| FUNDDESCR | category | 3 | 2.7K | General Fund - No Divisio 149; Assets Held for Beneficia 16 |
| CLASS_FLD | category | 46 | 0 | 40000 584; 21000 451; 19401 422; 20000 233 |
| CLASSDESCR | who | 86 | 0 | Federal Funds 518; GRF- Duties 285; Public Health Special Fun 281; Federal Educational Progr 190 |
| DEPTID | who | 245 | 0 | 1010001 351; 0600003 190; 0100001 185; 6000003 146 |
| DEPTDESCR | category | 34 | 2.7K | Support Services 30; 700 Fund Budget 16; Waiver Services 15; State Share 11 |
| C_ACCOUNT | who | 145 | 0 | 551250 252; 532140 130; 531130 128; 512310 125 |
| ACCTDESCR | who | 145 | 0 | OthHlth Svc.-(Non-DHS) 252; Rent-Equipment And Machin 130; Telecommunication Service 128; Insur.Prem-Workers Comp. 125 |
| OPERATING_UNIT | empty | 1 | 2.9K |  |
| OPERUNITDESCR | empty | 1 | 2.9K |  |
| PRODUCT | empty | 1 | 2.9K |  |
| PRODUCTDESCR | empty | 1 | 2.9K |  |
| PROGRAM_CODE | category | 43 | 0 | D0001 544; NP000 457; C0201 282; D0101 201 |
| PGMDESCR | category | 45 | 0 | ADMINISTRATION AND PENSIO 544; NO_PROGRAM 457; STUDENT PERFORMANCE 282; LICENSING AND REGULATION 201 |
| BUDGET_REF | empty | 1 | 2.9K |  |
| CHARTFIELD1 | empty | 1 | 2.9K |  |
| CF1DESCR | empty | 1 | 2.9K |  |
| CHARTFIELD2 | empty | 1 | 2.9K |  |
| CF2DESCR | empty | 1 | 2.9K |  |
| PROJECT_ID | empty | 1 | 2.9K |  |
| PROJDESCR | empty | 1 | 2.9K |  |
| ACTIVITY | empty | 1 | 2.9K |  |
| ACTVDESCR | empty | 1 | 2.9K |  |
| RESTYPE | empty | 1 | 2.9K |  |
| RESDESCR | empty | 1 | 2.9K |  |
| RCAT | empty | 1 | 2.9K |  |
| RCATDESCR | empty | 1 | 2.9K |  |
| RSUBCAT | empty | 1 | 2.9K |  |
| RSUBCATDESCR | empty | 1 | 2.9K |  |
| PO_ID | category | 17 | 2.9K | 8309026606 3; 8309026516 2; 8309026863 2; 8309027062 2 |
| ITEM_DESCRIPTION | category | 17 | 2.9K | AO IT Landlines FY-24 3; AUTHORITY ORDER: Emergenc 2; Wardrobe,Office Tables,Ac 2; SERVICE: Consultant contr 2 |
| OCP_DS_DATE | date | 2 | 2.7K | 8/17/2024 0:00 165 |
| INGESTED_AT | audit date | 1 | 0 | 2026-07-02 22:04:49.01915 2.9K |
| SOURCE_RUN_ID | audit | 1 | 0 | 635ddec2-ee83-4cb9-b236-d 2.9K |
| SRC_SHA256 | who | 1 | 0 | 051d2c33b08afb5d1876b24c3 2.9K |
